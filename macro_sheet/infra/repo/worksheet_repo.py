from macro_sheet.domain.block.base_block.main_block import MainBlock
from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo
from macro_sheet.infra.models import Worksheet
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo


class WorksheetRepo(IWorksheetRepo):
    def fetch_worksheet(
        self, filter: IWorksheetRepo.Filter
    ) -> list[IWorksheetRepo.WorksheetDTO]:
        """filter 조건에 맞는 worksheet 가져오기"""
        queryset = Worksheet.objects.all()

        if filter.id:
            queryset = queryset.filter(id=filter.id)
        if filter.owner_id:
            queryset = queryset.filter(owner_id=filter.owner_id)

        return [
            self.WorksheetDTO(
                id=worksheet.id,
                name=worksheet.name,
                owner_id=worksheet.owner_id,
                main_block=worksheet.main_block,
                blocks=worksheet.blocks,
                raw_blocks=worksheet.raw_blocks,
                raw_main_block=worksheet.raw_main_block,
            )
            for worksheet in queryset
        ]

    def create_worksheet(
        self, worksheet_obj: WorksheetVo
    ) -> IWorksheetRepo.WorksheetDTO:
        """worksheet 생성"""

        main_block: MainBlock | None = worksheet_obj.main_block
        blocks = [block.to_dict() if block else None for block in worksheet_obj.blocks]

        if main_block is None:
            dicted_main_block = None
        else:
            dicted_main_block = main_block.to_dict()

        worksheet = Worksheet(
            id=worksheet_obj.id,
            name=worksheet_obj.name,
            owner_id=worksheet_obj.owner_id,
            main_block=dicted_main_block,
            blocks=blocks,
            raw_blocks=worksheet_obj.raw_blocks,
            raw_main_block=worksheet_obj.raw_main_block,
        )
        worksheet.save()

        return self.WorksheetDTO(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_block=dicted_main_block,
            blocks=blocks,
            raw_blocks=worksheet_obj.raw_blocks,
            raw_main_block=worksheet_obj.raw_main_block,
        )

    def update_worksheet(
        self, worksheet_obj: WorksheetVo
    ) -> IWorksheetRepo.WorksheetDTO:
        """기존 worksheet 수정"""

        worksheet = Worksheet.objects.get(id=worksheet_obj.id)

        main_block: MainBlock | None = worksheet_obj.main_block

        if main_block is None:
            dicted_main_block = None
        else:
            dicted_main_block = main_block.to_dict()

        blocks = [block.to_dict() if block else None for block in worksheet_obj.blocks]

        worksheet.name = worksheet_obj.name
        worksheet.owner_id = worksheet_obj.owner_id
        worksheet.main_block = dicted_main_block  # 이부분 dict | None 로 변환
        worksheet.blocks = blocks  # 이부분 list[dict]로 변환
        worksheet.save()

        return self.WorksheetDTO(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_block=worksheet.main_block,
            blocks=worksheet.blocks,
            raw_main_block=worksheet.raw_main_block,
            raw_blocks=worksheet.raw_blocks,
        )

    def delete_worksheet(self, worksheet_id: str) -> bool:
        """worksheet 삭제"""
        deleted, _ = Worksheet.objects.filter(id=worksheet_id).delete()
        return deleted > 0
