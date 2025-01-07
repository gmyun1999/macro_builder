from django.core.management.base import BaseCommand

from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.usecase.worksheet_usecase import WorksheetUseCase


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        owner_id = "2"
        worksheet_use_case = WorksheetUseCase()

        for i in range(20):
            worksheet_name = f"Worksheet_{i + 1}"
            main_block = MainBlock()
            blocks = []

            # worksheet_use_case.create_process(
            #     worksheet_name=worksheet_name,
            #     owner_id=owner_id,
            #     main_block=main_block,
            #     blocks=blocks,
            #     related_function_ids=None,
            # )

            self.stdout.write(
                self.style.SUCCESS(f"Created Worksheet with name: {worksheet_name}")
            )
