import json
from pathlib import Path
from typing import Tuple

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from macro_be import settings
from macro_sheet.domain.block.action_block.file_action_block import FileActionBlock
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block.file_condition_block import (
    FileConditionBlock,
)
from macro_sheet.domain.block.control_block.control_block import ControlBlock
from macro_sheet.service.i_code_generator.i_block_code_generator import (
    IGuiCodeGeneratorFromBlock,
)


def tojson_filter(value):
    return json.dumps(value)


class GuiCodeGeneratorFromBlock(IGuiCodeGeneratorFromBlock):
    def __init__(self, template_dir: str = "templates"):
        # Django 프로젝트의 BASE_DIR을 사용하여 절대 경로 설정
        templates_path = (
            Path(settings.BASE_DIR) / "macro_sheet" / "infra" / template_dir
        )

        # 템플릿 디렉토리 존재 여부 확인
        if not templates_path.exists():
            raise FileNotFoundError(f"템플릿 디렉토리가 존재하지 않습니다: {templates_path}")

        # 필요한 템플릿 파일들이 존재하는지 확인
        required_templates = [
            "file_action.py.j2",
            "file_condition.py.j2",
            "control_block.py.j2",
            "main.py.j2",
        ]
        for tmpl in required_templates:
            tmpl_path = templates_path / tmpl
            if not tmpl_path.exists():
                raise FileNotFoundError(f"필수 템플릿 파일이 존재하지 않습니다: {tmpl_path}")

        self.env = Environment(loader=FileSystemLoader(str(templates_path)))
        self.env.filters["tojson"] = tojson_filter
        self.imports = set()
        self.widgets = []
        self.execute_actions = []
        self.actions_definitions = []
        self.processed_blocks = set()

    def generate_gui_code(self, block: Block) -> str:
        self.process_block(block)

        # 버튼 위젯 추가 (실행 시 execute_actions 함수 호출)
        button_widget = (
            "button = QPushButton('Execute')\n"
            "button.clicked.connect(execute_actions)\n"
            "layout.addWidget(button)"
        )
        self.widgets.append(button_widget)

        # 메인 템플릿 렌더링
        try:
            template = self.env.get_template("main.py.j2")
        except TemplateNotFound:
            raise TemplateNotFound("main.py.j2 템플릿을 찾을 수 없습니다.")

        rendered_code = template.render(
            imports=sorted(self.imports),
            widgets=self.widgets,
            execute_actions=self.execute_actions,
            actions_definitions=self.actions_definitions,
        )
        return rendered_code

    def process_block(self, block: Block):
        if isinstance(block, FileActionBlock):
            action_code = self.piece_code_from_file_action(block)
            self.actions_definitions.append(action_code)
            self.execute_actions.append(f"{block.action.lower()}_file()")
            self.imports.add("from file_action import *")
        elif isinstance(block, FileConditionBlock):
            condition_code = self.piece_code_from_file_condition(block)
            self.actions_definitions.append(condition_code)
            self.execute_actions.append(f"check_{block.condition_type.lower()}()")
            self.imports.add("from file_condition import *")
        elif isinstance(block, ControlBlock):
            control_code, control_execute = self.piece_code_from_control(block)
            self.actions_definitions.append(control_code)
            self.execute_actions.append(control_execute)
            self.imports.add("from control_block import *")
        else:
            print(f"Unsupported block type: {type(block)}")

    def piece_code_from_file_action(self, block: FileActionBlock) -> str:
        try:
            template = self.env.get_template("file_action.py.j2")
        except TemplateNotFound:
            raise TemplateNotFound("file_action.py.j2 템플릿을 찾을 수 없습니다.")
        return template.render(block=block)

    def piece_code_from_file_condition(self, block: FileConditionBlock) -> str:
        try:
            template = self.env.get_template("file_condition.py.j2")
        except TemplateNotFound:
            raise TemplateNotFound("file_condition.py.j2 템플릿을 찾을 수 없습니다.")
        return template.render(block=block)

    def piece_code_from_control(self, block: ControlBlock) -> Tuple[str, str]:
        try:
            template = self.env.get_template("control_block.py.j2")
        except TemplateNotFound:
            raise TemplateNotFound("control_block.py.j2 템플릿을 찾을 수 없습니다.")

        body_code = []
        for sub_block in block.body:
            if isinstance(sub_block, FileActionBlock):
                code = self.piece_code_from_file_action(sub_block)
                self.actions_definitions.append(code)
                body_code.append(f"{sub_block.action.lower()}_file()")
                self.imports.add("from file_action import *")
            elif isinstance(sub_block, FileConditionBlock):
                code = self.piece_code_from_file_condition(sub_block)
                self.actions_definitions.append(code)
                body_code.append(f"check_{sub_block.condition_type.lower()}()")
                self.imports.add("from file_condition import *")
            elif isinstance(sub_block, ControlBlock):
                control_code, control_execute = self.piece_code_from_control(sub_block)
                self.actions_definitions.append(control_code)
                body_code.append(control_execute)
                self.imports.add("from control_block import *")
            else:
                print(f"Unsupported sub-block type: {type(sub_block)}")

        control_execute = f"{block.control_type.lower()}_control()"
        rendered_control_code = template.render(block=block, body_code=body_code)
        return rendered_control_code, control_execute
