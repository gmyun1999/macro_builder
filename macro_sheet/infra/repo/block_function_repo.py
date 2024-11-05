# macro_sheet/infra/repo/block_function_repo.py
from typing import List, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from macro_sheet.domain.Function.block_function import BlockFunction as BlockFunctionVo
from macro_sheet.infra.models import Function
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo


class BlockFunctionRepo(IBlockFunctionRepo):
    def fetch_function(
        self, filter: IBlockFunctionRepo.Filter
    ) -> List[BlockFunctionVo]:
        queryset = Function.objects.all()
        if filter.owner_id is not None:
            queryset = queryset.filter(owner_id=filter.owner_id)
        if filter.id is not None:
            queryset = queryset.filter(id=filter.id)
        functions = list(queryset)

        return [
            BlockFunctionVo(
                id=str(func.id),
                owner_id=str(func.owner_id),
                name=func.name,
                blocks=func.blocks,
            )
            for func in functions
        ]

    def create_function(self, block_function_obj: BlockFunctionVo) -> BlockFunctionVo:
        try:
            with transaction.atomic():
                function = Function.objects.create(
                    owner_id=block_function_obj.owner_id,
                    name=block_function_obj.name,
                    blocks=block_function_obj.blocks,
                )
                return BlockFunctionVo(
                    id=str(function.id),
                    owner_id=str(function.owner_id),
                    name=function.name,
                    blocks=function.blocks,
                )

        except Exception as e:
            raise ValueError(f"함수 생성 중 오류가 발생했습니다: {str(e)}")

    def update_function(self, block_function_obj: BlockFunctionVo) -> BlockFunctionVo:
        try:
            with transaction.atomic():
                function = Function.objects.get(id=block_function_obj.id)
                function.name = block_function_obj.name
                function.blocks = block_function_obj.blocks
                function.save()
                return BlockFunctionVo(
                    id=str(function.id),
                    owner_id=str(function.owner_id),
                    name=function.name,
                    blocks=function.blocks,
                )

        except ObjectDoesNotExist:
            raise ValueError("수정하려는 함수가 존재하지 않습니다.")

        except Exception as e:
            raise ValueError(f"함수 수정 중 오류가 발생했습니다: {str(e)}")

    def delete_function(self, function_id: str) -> bool:
        try:
            with transaction.atomic():
                deleted, _ = Function.objects.filter(id=function_id).delete()

                if deleted == 0:
                    raise ValueError("삭제하려는 함수가 존재하지 않습니다.")
                return True

        except Exception as e:
            raise ValueError(f"함수 삭제 중 오류가 발생했습니다: {str(e)}")
