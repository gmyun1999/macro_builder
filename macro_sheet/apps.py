from django.apps import AppConfig


class MacroSheetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "macro_sheet"

    def ready(self):
        # 도메인 클래스를 임포트하여 레지스트리에 등록되도록 함
        from macro_sheet.domain.block.action_block.action_block import ActionBlock
        from macro_sheet.domain.block.action_block.file_action_block import (
            FileActionBlock,
        )
        from macro_sheet.domain.block.condition_block.condition_block import (
            ConditionBlock,
        )
        from macro_sheet.domain.block.condition_block.file_condition_block import (
            FileConditionBlock,
        )
        from macro_sheet.domain.block.control_block.control_block import ControlBlock
