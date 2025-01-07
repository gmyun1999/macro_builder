import boto3

from macro_be import settings
from macro_sheet.service.exception.exceptions import (
    PresignedUrlGenerationException,
    S3ClientInitializationException,
)
from macro_sheet.service.i_storage.i_storage import IStorage


class S3Storage(IStorage):
    def __init__(
        self,
        access_key_id: str,
        secret_access_key: str,
        region_name: str | None = None,
    ):
        super().__init__(access_key_id, secret_access_key, region_name)
        if region_name is None:
            raise ValueError("s3에서 region_name은 필수 입력값입니다.")

        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name,
        )

    """
    s3 저장소를 관리하는 서비스
    """

    def delete_file(self, gui_url: str):
        """
        파일 삭제
        """
        pass

    def bulk_delete_file(self, gui_urls: list[str]):
        """
        파일 bulk 삭제
        """
        pass

    def generate_presigned_url(
        self,
        bucket_name: str,
        object_key: str,
        expiration=300,
    ) -> str | None:
        try:
            s3_client = self.s3_client

        except boto3.exceptions.NoCredentialsError as e:
            raise S3ClientInitializationException(
                message="AWS 자격 증명이 누락되었습니다.", detail={"error": str(e)}
            )

        except boto3.exceptions.Boto3Error as e:
            raise S3ClientInitializationException(
                message="S3 클라이언트 초기화 중 오류가 발생했습니다.", detail={"error": str(e)}
            )

        try:
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": object_key},
                ExpiresIn=expiration,  # 5분 (300초)
            )
            return presigned_url

        except boto3.exceptions.Boto3Error as e:
            raise PresignedUrlGenerationException(
                message="프리사인드 URL 생성 중 오류가 발생했습니다.", detail={"error": str(e)}
            )
