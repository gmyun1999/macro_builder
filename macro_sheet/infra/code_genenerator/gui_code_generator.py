import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from macro_be import settings
from macro_sheet.domain.block.block import Block
from macro_sheet.domain.block.condition_block.condition_block import ConditionBlock
from macro_sheet.domain.block.control_block.control_block import ControlBlock
from macro_sheet.service.i_code_generator.i_block_code_generator import (
    IGuiCodeGeneratorFromBlock,
)


def tojson_filter(value):
    return json.dumps(value)


class GuiCodeGeneratorFromBlock(IGuiCodeGeneratorFromBlock):
    def __init__(self, template_dir: str = "templates"):
        templates_path = (
            Path(settings.BASE_DIR) / "macro_sheet" / "infra" / template_dir
        )
        if not templates_path.exists():
            raise FileNotFoundError(f"템플릿 디렉토리가 존재하지 않습니다: {templates_path}")

        self.env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            trim_blocks=True,  # 블록 사이의 불필요한 공백 제거
            lstrip_blocks=True,  # 줄 시작의 공백 제거
        )
        self.env.filters["tojson"] = tojson_filter
