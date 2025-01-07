# macro_sheet/infra/repo/block_function_repo.py
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Q

from macro_sheet.domain.block.block import Block
from macro_sheet.domain.Function.block_function import BlockFunction as BlockFunctionVo
from macro_sheet.infra.models import Function, FunctionHierarchy
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo


class BlockFunctionRepo(IBlockFunctionRepo):
    def __init__(self) -> None:
        self.function_closure = FunctionClosure()

    def fetch_function(
        self, filter: IBlockFunctionRepo.Filter
    ) -> list[BlockFunctionVo]:
        queryset = Function.objects.all()
        if filter.owner_id is not None:
            queryset = queryset.filter(owner_id=filter.owner_id)
        if filter.id is not None:
            queryset = queryset.filter(id=filter.id)

        if filter.parent_id is not None:
            children = self.function_closure.fetch(parent_id=filter.parent_id)
            child_ids = [child.child_id for child in children]
            queryset = queryset.filter(id__in=child_ids)

        if filter.child_id is not None:
            parents = self.function_closure.fetch(child_id=filter.child_id)
            parent_ids = [parent.parent_id for parent in parents]
            queryset = queryset.filter(id__in=parent_ids)

        functions = list(queryset)

        return [
            BlockFunctionVo(
                id=str(func.id),
                owner_id=str(func.owner_id),
                name=func.name,
                blocks=[Block.from_dict(block) for block in func.blocks],
                raw_blocks=func.raw_blocks,
            )
            for func in functions
        ]

    def create_function(
        self, block_function_obj: BlockFunctionVo, parent_function_ids: list[str] | None
    ) -> BlockFunctionVo:
        try:
            with transaction.atomic():
                block_function_obj.blocks
                blocks = [block.to_dict() for block in block_function_obj.blocks]

                function = Function.objects.create(
                    id=block_function_obj.id,
                    owner_id=block_function_obj.owner_id,
                    name=block_function_obj.name,
                    blocks=blocks,
                    raw_blocks=block_function_obj.raw_blocks,
                )

                # 클로저 관계 생성 (일괄 처리)
                if parent_function_ids:
                    closures_to_create = [
                        self.function_closure.Closure(
                            parent_id=parent_id, child_id=function.id
                        )
                        for parent_id in parent_function_ids
                    ]
                    self.function_closure.bulk_save(closures_to_create)

                return BlockFunctionVo(
                    id=str(function.id),
                    owner_id=str(function.owner_id),
                    name=function.name,
                    blocks=function.blocks,
                    raw_blocks=function.raw_blocks,
                )

        except Exception as e:
            raise ValueError(f"함수 생성 중 오류가 발생했습니다: {str(e)}")

    def update_function(
        self, block_function_obj: BlockFunctionVo, new_parent_function_ids: list[str]
    ) -> BlockFunctionVo:
        try:
            with transaction.atomic():
                block_function_obj.blocks
                blocks = [block.to_dict() for block in block_function_obj.blocks]

                function = Function.objects.get(id=block_function_obj.id)
                function.name = block_function_obj.name
                function.blocks = blocks
                function.raw_blocks = block_function_obj.raw_blocks
                function.save()

                # 기존 클로저 관계 삭제 (일괄 처리)
                existing_closures = self.function_closure.fetch(
                    child_id=block_function_obj.id
                )
                closures_to_delete = existing_closures
                if closures_to_delete:
                    self.function_closure.bulk_delete(closures_to_delete)

                # 새로운 클로저 관계 생성 (일괄 처리)
                if new_parent_function_ids:
                    closures_to_create = [
                        self.function_closure.Closure(
                            parent_id=parent_id, child_id=block_function_obj.id
                        )
                        for parent_id in new_parent_function_ids
                    ]
                    self.function_closure.bulk_save(closures_to_create)

                return block_function_obj

        except ObjectDoesNotExist:
            raise ValueError("수정하려는 함수가 존재하지 않습니다.")

        except Exception as e:
            raise ValueError(f"함수 수정 중 오류가 발생했습니다: {str(e)}")

    def delete_function(self, function_id: str) -> bool:
        try:
            with transaction.atomic():
                ancestor_closures = self.function_closure.fetch(parent_id=function_id)
                closures_to_delete = ancestor_closures

                # 이 함수가 하위인 클로저 관계 삭제
                descendant_closures = self.function_closure.fetch(child_id=function_id)
                closures_to_delete += descendant_closures  # 합쳐서 일괄 삭제

                if closures_to_delete:
                    self.function_closure.bulk_delete(closures_to_delete)

                deleted, _ = Function.objects.filter(id=function_id).delete()

                if deleted == 0:
                    raise ValueError("삭제하려는 함수가 존재하지 않습니다.")
                return True

        except Exception as e:
            raise ValueError(f"함수 삭제 중 오류가 발생했습니다: {str(e)}")

    def get_all_ancestors(self, root_function_id: str) -> list[str]:
        return self.function_closure.get_all_ancestors(root_function_id)


class FunctionClosure:
    class Closure:
        def __init__(self, parent_id: str, child_id: str):
            self.parent_id = parent_id
            self.child_id = child_id

    class Filter:
        def __init__(self, parent_id: str | None = None, child_id: str | None = None):
            self.parent_id = parent_id
            self.child_id = child_id

    def save(self, closure: Closure) -> None:
        try:
            FunctionHierarchy.objects.create(
                parent_id=closure.parent_id, child_id=closure.child_id
            )
        except ObjectDoesNotExist:
            raise ValueError("상위 함수 또는 하위 함수가 존재하지 않습니다.")

    def delete(self, closure: Closure) -> None:
        deleted, _ = FunctionHierarchy.objects.filter(
            parent_id=closure.parent_id, child_id=closure.child_id
        ).delete()
        if deleted == 0:
            raise ValueError(
                f"FunctionClosure 관계가 존재하지 않습니다: Ancestor={closure.parent_id}, Descendant={closure.child_id}"
            )

    def fetch(
        self, parent_id: str | None = None, child_id: str | None = None
    ) -> list[Closure]:
        """ """
        queryset = FunctionHierarchy.objects.all()
        if parent_id is not None:
            queryset = queryset.filter(parent_id=parent_id)
        if child_id is not None:
            queryset = queryset.filter(child_id=child_id)
        return [
            self.Closure(parent_id=parent_id, child_id=child_id)
            for parent_id, child_id in queryset.values_list("parent_id", "child_id")
        ]

    def bulk_save(self, closures: list[Closure]) -> None:
        """
        closures: Closure 객체 리스트
        """
        objects = []
        for closure in closures:
            try:
                parent = Function.objects.get(id=closure.parent_id)
                child = Function.objects.get(id=closure.child_id)
                objects.append(FunctionHierarchy(parent=parent, child=child))
            except ObjectDoesNotExist:
                raise ValueError(
                    f"상위 함수({closure.parent_id}) 또는 하위 함수({closure.child_id})가 존재하지 않습니다."
                )
            FunctionHierarchy.objects.bulk_create(objects)

    def bulk_delete(self, closures: list[Closure]) -> None:
        """
        closures: Closure 객체 리스트
        """
        if not closures:
            return

        q_objects = Q()
        for closure in closures:
            q_objects |= Q(parent_id=closure.parent_id, child_id=closure.child_id)
        with transaction.atomic():
            deleted_count, _ = FunctionHierarchy.objects.filter(q_objects).delete()
            if deleted_count != len(closures):
                raise ValueError("일부 FunctionClosure 관계가 존재하지 않거나 삭제되지 않았습니다.")

    def get_all_ancestors(self, root_function_id: str) -> list[str]:
        """
        Queryset.raw()를 사용하여 SQL Injection에 안전한 방식으로 모든 조상들을 조회합니다.

        Args:
            root_function_id (str): 조상을 찾고자 하는 function의 ID

        Returns:
            list[str]: 모든 조상 function들의 ID 목록
        """
        query = """
            WITH RECURSIVE ancestors AS (
                -- 초기 부모들을 선택 (base case)
                SELECT id, parent_id, child_id, 1 as depth
                FROM "FunctionHierarchy"
                WHERE child_id = %(root_id)s
                
                UNION ALL
                
                -- 재귀적으로 상위 부모들을 선택
                SELECT fh.id, fh.parent_id, fh.child_id, a.depth + 1
                FROM "FunctionHierarchy" fh
                INNER JOIN ancestors a ON fh.child_id = a.parent_id
            )
            SELECT DISTINCT fh.id, fh.parent_id, fh.child_id
            FROM "FunctionHierarchy" fh
            JOIN ancestors a ON fh.id = a.id
            ORDER BY fh.parent_id;
        """

        # Queryset.raw()는 SQL Injection에 안전한 파라미터 바인딩을 제공합니다
        queryset = FunctionHierarchy.objects.raw(
            query, params={"root_id": root_function_id}
        )

        # parent_id 값들만 리스트로 변환하여 반환
        return list(set(obj.parent_id for obj in queryset))
