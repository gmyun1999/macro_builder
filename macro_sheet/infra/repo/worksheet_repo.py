from macro_sheet.domain.worksheet.worksheet import Worksheet as WorksheetVo
from macro_sheet.infra.models import Worksheet
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo
from macro_sheet.service.i_repo.i_worksheet_repo import IWorksheetRepo


class WorksheetRepo(IWorksheetRepo):
    def fetch_worksheet(
        self, filter: IWorksheetRepo.Filter
    ) -> list[IWorksheetRepo.WorksheetDTO | None]:
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
                main_blocks=worksheet.main_blocks,
                blocks=worksheet.blocks,
            )
            for worksheet in queryset
        ]

    def create_worksheet(
        self, worksheet_obj: WorksheetVo
    ) -> IWorksheetRepo.WorksheetDTO:
        """worksheet 생성"""

        # TODO : 바로 밀어넣는게아니라, main_blocks랑 blocks는 다시 list[dict]로 변환한다음에 넣어줘야함
        worksheet = Worksheet(
            id=worksheet_obj.id,
            name=worksheet_obj.name,
            owner_id=worksheet_obj.owner_id,
            main_blocks=worksheet_obj.main_blocks,
            blocks=worksheet_obj.blocks,
        )
        worksheet.save()

        return self.WorksheetDTO(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_blocks=worksheet.main_blocks,
            blocks=worksheet.blocks,
        )

    def update_worksheet(
        self, worksheet_obj: WorksheetVo
    ) -> IWorksheetRepo.WorksheetDTO:
        """기존 worksheet 수정"""

        # TODO : 바로 밀어넣는게아니라, main_blocks랑 blocks는 다시 list[dict]로 변환한다음에 넣어줘야함
        worksheet = Worksheet.objects.get(id=worksheet_obj.id)

        worksheet.name = worksheet_obj.name
        worksheet.owner_id = worksheet_obj.owner_id
        worksheet.main_blocks = worksheet_obj.main_blocks  # 이부분 list[dict]로 변환
        worksheet.blocks = worksheet_obj.blocks  # 이부분 list[dict]로 변환
        worksheet.save()

        return self.WorksheetDTO(
            id=worksheet.id,
            name=worksheet.name,
            owner_id=worksheet.owner_id,
            main_blocks=worksheet.main_blocks,
            blocks=worksheet.blocks,
        )

    def delete_worksheet(self, worksheet_id: str) -> bool:
        """worksheet 삭제"""
        deleted, _ = Worksheet.objects.filter(id=worksheet_id).delete()
        return deleted > 0
