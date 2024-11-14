from django.db import transaction

from macro_sheet.domain.Function.block_function import BlockFunction
from macro_sheet.infra.repo.block_function_repo import BlockFunctionRepo
from macro_sheet.infra.repo.function_closure_repo import FunctionClosureRepo
from macro_sheet.service.i_repo.i_block_function_repo import IBlockFunctionRepo
from macro_sheet.service.i_repo.i_function_closure_repo import IFunctionClosureRepo


class BlockFunctionService:
    def __init__(self) -> None:
        self.blk_func_repo: IBlockFunctionRepo = BlockFunctionRepo()
        self.func_closure_repo: IFunctionClosureRepo = FunctionClosureRepo()

    def update_block_function_with_closure_function(
        self,
        block_function_obj: BlockFunction,
        new_parent_function_ids: list[str],
    ) -> BlockFunction:
        """
        블록 함수와 그에 따른 클로저 관계를 업데이트합니다.

        - 함수 레코드를 업데이트합니다.
        - 기존에 이 함수가 하위인 클로저 관계를 일괄 삭제합니다.
        - 새로운 부모 함수 ID가 있는 경우 클로저 관계를 일괄 생성합니다.
        """
        try:
            with transaction.atomic():
                # 함수 업데이트
                updated_block_function = self.blk_func_repo.update_function(
                    block_function_obj
                )

                # 기존 클로저 관계 삭제 (일괄 처리)
                closure_filter = IFunctionClosureRepo.Filter(
                    child_id=updated_block_function.id
                )
                existing_closures = self.func_closure_repo.fetch(closure_filter)
                closures_to_delete = existing_closures
                if closures_to_delete:
                    self.func_closure_repo.bulk_delete(closures_to_delete)

                # 새로운 클로저 관계 생성 (일괄 처리)
                if new_parent_function_ids:
                    closures_to_create = [
                        IFunctionClosureRepo.Closure(
                            parent_id=parent_id, child_id=updated_block_function.id
                        )
                        for parent_id in new_parent_function_ids
                    ]
                    self.func_closure_repo.bulk_save(closures_to_create)

                return updated_block_function

        except Exception as e:
            raise ValueError(f"블록 함수 및 클로저 관계 업데이트 중 오류가 발생했습니다: {str(e)}")

    def create_block_function_with_closure_function(
        self,
        block_function_obj: BlockFunction,
        parent_function_ids: list[str] | None = None,
    ) -> BlockFunction:
        """
        새로운 블록 함수를 생성하고, 지정된 상위 함수들과 클로저 관계를 설정합니다.
        """
        try:
            with transaction.atomic():
                created_block_function = self.blk_func_repo.create_function(
                    block_function_obj
                )

                # 클로저 관계 생성 (일괄 처리)
                if parent_function_ids:
                    closures_to_create = [
                        IFunctionClosureRepo.Closure(
                            parent_id=parent_id, child_id=created_block_function.id
                        )
                        for parent_id in parent_function_ids
                    ]
                    self.func_closure_repo.bulk_save(closures_to_create)

                return created_block_function
        except Exception as e:
            raise ValueError(f"블록 함수 및 클로저 관계 생성 중 오류가 발생했습니다: {str(e)}")

    def delete_block_function_with_closure_function(self, function_id: str) -> bool:
        """
        블록 함수를 삭제하고, 관련된 모든 클로저 관계를 제거합니다.

        - 함수 레코드를 삭제합니다.
        - 이 함수가 상위 또는 하위인 모든 클로저 관계를 일괄 삭제합니다.
        """
        try:
            with transaction.atomic():
                # 이 함수가 상위인 클로저 관계 삭제
                ancestor_filter = IFunctionClosureRepo.Filter(parent_id=function_id)
                ancestor_closures = self.func_closure_repo.fetch(ancestor_filter)
                closures_to_delete = ancestor_closures

                # 이 함수가 하위인 클로저 관계 삭제
                descendant_filter = IFunctionClosureRepo.Filter(child_id=function_id)
                descendant_closures = self.func_closure_repo.fetch(descendant_filter)
                closures_to_delete += descendant_closures  # 합쳐서 일괄 삭제

                if closures_to_delete:
                    self.func_closure_repo.bulk_delete(closures_to_delete)

                # 함수 삭제
                result = self.blk_func_repo.delete_function(function_id)
                return result
        except Exception as e:
            raise ValueError(f"블록 함수 및 클로저 관계 삭제 중 오류가 발생했습니다: {str(e)}")

    def fetch_function_by_id(self, function_id: str) -> BlockFunction | None:
        result = self.blk_func_repo.fetch_function(
            filter=self.blk_func_repo.Filter(id=function_id)
        )
        if not result:
            return None

        return result[0]

    def fetch_function_by_owner_id(self, owner_id: str) -> list[BlockFunction]:
        return self.blk_func_repo.fetch_function(
            filter=self.blk_func_repo.Filter(owner_id=owner_id)
        )

    def get_ancestors_ids(self, function_id: str) -> list[str]:
        """
        주어진 함수의 모든 부모 함수 ID를 조회합니다.
        """
        try:
            ancestors = self.func_closure_repo.get_all_ancestors(function_id)
            return ancestors

        except Exception as e:
            raise ValueError(f"부모 함수 조회 중 오류가 발생했습니다: {str(e)}")

    def get_child_function_ids(self, function_id: str):
        """
        주어진 function_id의 자식 function들의 ids 를 반환한다. 없으면 None
        """
        closure_relation = self.func_closure_repo.fetch(
            self.func_closure_repo.Filter(parent_id=function_id)
        )
        if closure_relation:
            return [child.child_id for child in closure_relation]

        return None

    def check_circular(
        self, target_function_id: str, related_function_ids: list[str]
    ) -> bool:
        """
        function 끼리의 순환참조를 체크한다.
        related_function_ids의 조상들중에서
        function_id가 존재하는지 확인하면됨.
        """
        ancestors = set()
        for related_func in related_function_ids:
            related_ancestors = self.get_ancestors_ids(function_id=related_func)
            ancestors.update(related_ancestors)

            if target_function_id in ancestors:
                return True  # 순환 참조 발견

        return False  # 순환 참조 없음

    def check_recursion(
        self, function_id: str, related_function_ids: list[str]
    ) -> bool:
        """
        재귀인지를 확인한다
        """
        return function_id in related_function_ids

    def check_is_exist_id(self, function_id: str) -> bool:
        """
        function_id가 존재하는지를 확인한다.
        """
        result = self.fetch_function_by_id(function_id=function_id)
        if result is None:
            return False

        return True
