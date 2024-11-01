import os

import httpx

from macro_sheet.infra.template_render.jinja2_template_render import (
    Jinja2TemplateRender,
)
from macro_sheet.service.block_service import BlockService
from macro_sheet.service.i_template_render.i_template_render import ITemplateRender


class GuiService:
    def __init__(self) -> None:
        self.template: ITemplateRender = Jinja2TemplateRender()
        self.block_service = BlockService()

    def generate_gui_str_code(self, execute_str_python_code: str):
        # Jinja2 템플릿에 파이썬 스크립트 문자열을 삽입
        gui_code = self.template.render_main_template(
            python_script=execute_str_python_code
        )

        # Python 파일로 저장
        script_path = "generated_gui_app.py"  # 로컬 경로에 파일 저장
        with open(script_path, "w", encoding="utf-8") as script_file:
            script_file.write(gui_code)

        return script_path

    def send_to_package_server(self, script_path: str):
        # 동기 클라이언트를 사용하여 패키징 서버로 파일 전송
        url = "http://localhost:8000/package"  # 패키징 서버 URL
        with open(script_path, "rb") as f:
            files = {"file": (script_path, f)}
            response = httpx.post(url, files=files, timeout=120.0)

        # 응답 처리
        if response.status_code == 200:
            download_link = response.json().get("download_link")
            return download_link
        else:
            return None

    def generate_and_package_gui(self, execute_str_python_code: str):
        # 1. Python 코드 파일 생성
        script_path = self.generate_gui_str_code(execute_str_python_code)

        # 2. 생성된 파일을 패키징 서버로 전송
        download_link = self.send_to_package_server(script_path)

        return download_link
