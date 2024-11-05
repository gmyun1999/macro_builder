from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo
from macro_sheet.infra.models import Worksheet
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo


class WorksheetRepo(IWorksheetRepo):
    def fetch_worksheet(self, filter: IWorksheetRepo.Filter) -> list[WorksheetVo]:
        """filter 조건에 맞는 worksheet 가져오기"""
        queryset = Worksheet.objects.all()

        if filter.id:
            queryset = queryset.filter(id=filter.id)
        if filter.owner_id:
            queryset = queryset.filter(owner_id=filter.owner_id)

        return [
            WorksheetVo(
                id=worksheet.id,
                name=worksheet.name,
                owner_id=worksheet.owner_id,
                main_blocks=worksheet.main_blocks,
                blocks=worksheet.blocks,
            )
            for worksheet in queryset
        ]

    def create_worksheet(self, worksheet_obj: WorksheetVo) -> WorksheetVo:
        """worksheet 생성"""

        worksheet = Worksheet(
            id=worksheet_obj.id,
            name=worksheet_obj.name,
            owner_id=worksheet_obj.owner_id,
            main_blocks=worksheet_obj.main_blocks,
            blocks=worksheet_obj.blocks,
        )
        worksheet.save()

        return WorksheetVo(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_blocks=worksheet.main_blocks,
            blocks=worksheet.blocks,
        )

    def update_worksheet(self, worksheet_obj: WorksheetVo) -> WorksheetVo:
        """기존 worksheet 수정"""
        worksheet = Worksheet.objects.get(id=worksheet_obj.id)

        worksheet.name = worksheet_obj.name
        worksheet.owner_id = worksheet_obj.owner_id
        worksheet.main_blocks = worksheet_obj.main_blocks
        worksheet.blocks = worksheet_obj.blocks
        worksheet.save()

        return WorksheetVo(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_blocks=worksheet.main_blocks,
            blocks=worksheet.blocks,
        )

    def delete_worksheet(self, worksheet_obj: WorksheetVo) -> bool:
        """worksheet 삭제"""
        deleted, _ = Worksheet.objects.filter(id=worksheet_obj.id).delete()
        return deleted > 0

    def bulk_create_worksheets(
        self, worksheets: list[WorksheetVo]
    ) -> list[WorksheetVo]:
        # WorksheetVo를 실제 Worksheet 모델 객체로 변환하여 일괄 생성
        worksheet_objs = [
            Worksheet(
                id=worksheet_vo.id,
                name=worksheet_vo.name,
                owner_id=worksheet_vo.owner_id,
                main_blocks=worksheet_vo.main_blocks,
                blocks=worksheet_vo.blocks,
            )
            for worksheet_vo in worksheets
        ]
        Worksheet.objects.bulk_create(worksheet_objs)
        return worksheets
