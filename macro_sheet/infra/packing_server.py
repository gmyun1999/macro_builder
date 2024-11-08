import httpx

from macro_sheet.service.i_packaging_server.i_packaging_server import (
    PackagingClientInterface,
)


class PackagingClient(PackagingClientInterface):
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def send_to_package_server(self, script_content: str) -> str | None:
        """
        패키징 서버에 스크립트를 문자열로 업로드하고 GUI 다운로드 링크를 반환한다.
        """
        url = f"{self.base_url}/package"
        payload = {"content": script_content}  # "content" 키로 변경

        response = httpx.post(url, json=payload, timeout=120.0)

        if response.status_code == 200:
            return response.json().get("download_link")
        else:
            return None
