import subprocess
from pathlib import Path
from typing import Any, Callable, Dict

from jinja2 import Environment, FileSystemLoader
from PyQt5 import QtWidgets

from macro_sheet.domain.block.block import Block, FileSystemBlock


class GuiCodeGeneratorFromBlock:
    def __init__(self, template_dir: str = "templates"):
        templates_path = (
            Path(settings.BASE_DIR) / "macro_sheet" / "infra" / template_dir
        )
        if not templates_path.exists():
            raise FileNotFoundError(f"템플릿 디렉토리가 존재하지 않습니다: {templates_path}")

        self.env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # 각 블록 타입에 따른 변환 함수 매핑
        self.block_to_gui_code_map: Dict[type, Callable[[Block], str]] = {
            FileSystemBlock: self.generate_filesystemblock_gui_code,
            # 다른 블록 타입: 해당 변환 함수 매핑 추가
            # AnotherBlock: self.generate_anotherblock_gui_code
        }

    def generate_gui_code(self, block: Block) -> str:
        """
        Block 객체를 받아 해당 블록 타입에 맞는 GUI 코드를 생성.
        """
        # 1. 블록 타입에 맞는 변환 함수 찾기
        block_type = type(block)
        if block_type not in self.block_to_gui_code_map:
            raise ValueError(f"지원되지 않는 블록 타입입니다: {block_type}")

        # 2. 변환 함수 호출하여 GUI 코드 생성
        return self.block_to_gui_code_map[block_type](block)

    def generate_filesystemblock_gui_code(self, block: FileSystemBlock) -> str:
        """
        FileSystemBlock 객체를 받아 PowerShell 명령어를 실행하는 PyQt GUI 코드를 생성.
        """
        # 1. 유효성 검사
        if not block.validate():
            raise ValueError("유효하지 않은 FileSystemBlock입니다.")

        # 2. PowerShell 명령어 생성
        try:
            command = block.to_powershell()
        except Exception as e:
            raise ValueError(f"PowerShell 명령어 생성 오류: {e}")

        # 3. Jinja2 템플릿 로드
        template = self.env.get_template("main.py.jinja")

        # 4. 템플릿 렌더링 (command 변수를 템플릿에 전달)
        rendered_code = template.render(command=command)

        return rendered_code

    def save_gui_code(self, code: str, output_path: str):
        """
        생성된 GUI 코드를 파일로 저장
        """
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"GUI 코드가 {output_path}에 저장되었습니다.")

    def run_generated_gui(self, output_path: str):
        """
        저장된 GUI 코드를 실행
        """
        subprocess.run(["python", output_path], check=True)
