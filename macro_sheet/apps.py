from django.apps import AppConfig


class MacroSheetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "macro_sheet"

    def ready(self):
        # 도메인 클래스를 임포트하여 레지스트리에 등록되도록 함
        import macro_sheet.infra.models
        from macro_sheet.domain.block.api_block.law_api_block import LawApiBlock
        from macro_sheet.domain.block.base_block.condition_block import ConditionBlock
        from macro_sheet.domain.block.base_block.loop_block import LoopBlock
        from macro_sheet.domain.block.base_block.main_block import MainBlock
        from macro_sheet.domain.block.base_block.reference_block import ReferenceBlock
        from macro_sheet.domain.block.file_system_block import file_system_block
        from macro_sheet.domain.block.mouse_keyboard_block import recorder_block
        from macro_sheet.domain.Function.block_function import BlockFunction
        from macro_sheet.domain.worksheet.worksheet import Worksheet
