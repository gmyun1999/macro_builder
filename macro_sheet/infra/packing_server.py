import json
import os
import time
import uuid

import boto3
import httpx

from macro_be import settings
from macro_be.settings import PACKAGE_SERVER_URL
from macro_sheet.service.i_packaging_server.i_packaging_server import (
    PackagingClientInterface,
)


class S3Service:
    @staticmethod
    def upload_to_s3(file_path: str, file_key: str) -> bool:
        """
        패키징된 파일을 S3에 업로드하고 링크 반환
        - file_path는 실제 로컬의 파일을 가리킨다
        """
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.COMMAND_GUI_AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.COMMAND_GUI_AWS_SECRET_ACCESS_KEY,
                region_name=settings.COMMAND_GUI_AWS_REGION,
            )
            bucket_name = settings.COMMAND_GUI_S3_BUCKET_NAME  # S3 버킷 이름

            s3_client.upload_file(file_path, bucket_name, file_key)

            return True
        except Exception as e:
            return False

    @staticmethod
    def generate_presigned_url(
        object_key,
        bucket_name=settings.COMMAND_GUI_S3_BUCKET_NAME,
        expiration=300,
    ) -> str:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.COMMAND_GUI_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.COMMAND_GUI_AWS_SECRET_ACCESS_KEY,
            region_name=settings.COMMAND_GUI_AWS_REGION,
        )

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,  # 5분
        )
        return presigned_url


class PackagingClient(PackagingClientInterface):
    def __init__(self, base_url: str = PACKAGE_SERVER_URL):
        self.base_url = base_url

    def get_gui_link(self, script_content: str) -> str:
        presigned_url, unique_id = self.send_to_package_server(script_content)
        return self.trigger_to_package_git_action(
            presigned_url=presigned_url, unique_id=unique_id
        )

    def send_to_package_server(self, script_content: str) -> tuple[str, str]:
        """
        스크립트 내용을 S3에 업로드하고 프리사인드 URL과 unique_id를 반환합니다.
        """
        unique_id = str(uuid.uuid4())
        file_key = f"script/{unique_id}_script.py"

        # 스크립트 내용을 임시 파일에 저장
        with open("temp_script.py", "w", encoding="utf-8") as temp_file:
            temp_file.write(script_content)
            temp_file_path = temp_file.name

        # S3에 업로드
        upload_result = S3Service.upload_to_s3(
            file_path=temp_file_path, file_key=file_key
        )

        # 임시 파일 삭제
        os.remove(temp_file_path)

        if not upload_result:
            raise Exception("스크립트를 S3에 업로드하지 못했습니다.")

        # 프리사인드 URL 생성
        presigned_url = S3Service.generate_presigned_url(object_key=file_key)

        return presigned_url, unique_id

    def trigger_to_package_git_action(self, presigned_url: str, unique_id: str) -> str:
        github_token = os.environ.get("GITHUB_TOKEN")
        github_repo = os.environ.get("GITHUB_REPO")

        # 워크플로 파일명을 지정하여 dispatch 엔드포인트를 호출합니다.
        github_api_url = f"https://api.github.com/repos/{github_repo}/actions/workflows/package.yml/dispatches"
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json",
        }
        payload = {
            "ref": "main",
            "inputs": {
                "script_url": presigned_url,
                "unique_id": unique_id,
            },
        }
        print("payload", payload)
        response = httpx.post(github_api_url, json=payload, headers=headers)
        if response.status_code != 204:
            raise Exception(f"GitHub Actions 워크플로 트리거 실패: {response.text}")

        # 워크플로 실행 ID를 가져오는 로직도 수정해야 합니다.
        workflow_run_id = self.get_workflow_run_id(unique_id, headers)
        if not workflow_run_id:
            raise Exception("워크플로 실행 ID를 가져올 수 없습니다.")

        # 워크플로 완료 대기
        workflow_conclusion = self.wait_for_workflow_completion(
            workflow_run_id, headers
        )
        if workflow_conclusion != "success":
            raise Exception("워크플로가 성공적으로 완료되지 않았습니다.")

        # 패키징 결과물에 대한 프리사인드 URL 생성
        packaged_file_key = f"packaging/{unique_id}_packaged.exe"
        download_url = S3Service.generate_presigned_url(object_key=packaged_file_key)

        return download_url

    def get_workflow_run_id(self, unique_id: str, headers: dict) -> int | None:
        github_repo = os.environ.get("GITHUB_REPO")
        runs_api_url = f"https://api.github.com/repos/{github_repo}/actions/runs"

        time.sleep(20)  # 워크플로 트리거 후 지연 시간 증가

        params = {
            "event": "workflow_dispatch",
            "per_page": 100,
        }

        response = httpx.get(runs_api_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Failed to get workflow runs: {response.text}")
            return None

        runs = response.json().get("workflow_runs", [])
        for run in runs:
            run_id = run.get("id")
            run_details_url = (
                f"https://api.github.com/repos/{github_repo}/actions/runs/{run_id}"
            )
            run_response = httpx.get(run_details_url, headers=headers)

            if run_response.status_code != 200:
                continue

            run_data = run_response.json()
            event = run_data.get("event", "")
            inputs = {}

            if event == "workflow_dispatch":
                inputs = run_data.get("inputs", {})

            print(f"Run ID: {run_id}, Inputs: {inputs}")
            if inputs.get("unique_id") == unique_id:
                return run_id

        return None

    def wait_for_workflow_completion(self, run_id: int, headers: dict) -> str:
        """
        워크플로가 완료될 때까지 대기하고 결론을 반환합니다.
        """
        github_repo = os.environ.get("GITHUB_REPO")
        run_api_url = (
            f"https://api.github.com/repos/{github_repo}/actions/runs/{run_id}"
        )

        timeout = 600  # 최대 대기 시간 (초)
        interval = 10  # 폴링 간격 (초)
        elapsed = 0

        while elapsed < timeout:
            response = httpx.get(run_api_url, headers=headers)
            if response.status_code != 200:
                raise Exception(f"워크플로 실행 상태를 가져올 수 없습니다: {response.text}")

            run_data = response.json()
            status = run_data.get("status")
            conclusion = run_data.get("conclusion")

            if status == "completed":
                return conclusion

            time.sleep(interval)
            elapsed += interval

        raise Exception("워크플로 실행 시간 초과")

    def process_packaging_request(self, script_content: str) -> str:
        """
        전체 패키징 요청을 처리하고 다운로드 URL을 반환합니다.
        """
        # 1단계: 스크립트 업로드 및 프리사인드 URL과 unique_id 획득
        presigned_url, unique_id = self.send_to_package_server(script_content)

        # 2단계: GitHub Actions 워크플로 트리거 및 완료 대기
        download_url = self.trigger_to_package_git_action(presigned_url, unique_id)

        return download_url
