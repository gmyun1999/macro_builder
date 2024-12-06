from urllib.parse import urljoin

import httpx

from macro_be.settings import PACKAGE_SERVER_URL
from macro_sheet.service.exception.exceptions import DownloadLinkNotFoundException
from macro_sheet.service.i_packaging_server.i_packaging_server import (
    PackagingClientInterface,
)


class PackagingClient(PackagingClientInterface):
    def __init__(self, base_url: str = PACKAGE_SERVER_URL):
        self.base_url = base_url

    def send_to_package_server(self, script_content: str) -> str:
        """
        패키징 서버에 스크립트를 문자열로 업로드하고 GUI 다운로드 링크를 반환한다.
        """
        url = urljoin(self.base_url, "/package")
        payload = {"content": script_content}

        response = httpx.post(url, json=payload, timeout=300.0)

        if response.status_code == 201:
            download_link = response.json().get("download_link")
            # print(response.json())
            if not download_link:
                raise DownloadLinkNotFoundException(
                    message="GUI 다운로드 링크가 존재하지 않습니다.",
                    detail={
                        "status_code": response.status_code,
                        "message": response.text,
                    },
                )
            return download_link

        else:
            # print(response.json())
            raise DownloadLinkNotFoundException(
                message="패키징 서버에서 GUI 다운로드 링크를 가져오는 데 실패했습니다.",
                detail={"status_code": response.status_code, "message": response.text},
            )
