from django.apps import AppConfig


class MacroSheetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "macro_sheet"

    def ready(self):
        # 도메인 클래스를 임포트하여 레지스트리에 등록되도록 함
        import macro_sheet.infra.models
        from macro_sheet.domain.block.condition_block.condition_block import (
            ConditionBlock,
        )
        from macro_sheet.domain.block.file_system_block import file_system_block
        from macro_sheet.domain.block.loop_block.loop_block import LoopBlock
