from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import F, IntegerField, Q, Value
from django.db.models.functions import Cast
from django_cte import With

from macro_sheet.infra.models import Function, FunctionHierarchy
from macro_sheet.service.i_repo.i_function_closure_repo import IFunctionClosureRepo


class FunctionClosureRepo(IFunctionClosureRepo):
    def save(self, closure: IFunctionClosureRepo.Closure) -> None:
        try:
            with transaction.atomic():
                FunctionHierarchy.objects.create(
                    parent_id=closure.parent_id, child_id=closure.child_id
                )
        except ObjectDoesNotExist:
            raise ValueError("상위 함수 또는 하위 함수가 존재하지 않습니다.")

    def delete(self, closure: IFunctionClosureRepo.Closure) -> None:
        deleted, _ = FunctionHierarchy.objects.filter(
            parent_id=closure.parent_id, child_id=closure.child_id
        ).delete()
        if deleted == 0:
            raise ValueError(
                f"FunctionClosure 관계가 존재하지 않습니다: Ancestor={closure.parent_id}, Descendant={closure.child_id}"
            )

    def fetch(
        self, filter: IFunctionClosureRepo.Filter
    ) -> list[IFunctionClosureRepo.Closure]:
        queryset = FunctionHierarchy.objects.all()
        if filter.parent_id is not None:
            queryset = queryset.filter(parent_id=filter.parent_id)
        if filter.child_id is not None:
            queryset = queryset.filter(child_id=filter.child_id)
        return [
            IFunctionClosureRepo.Closure(parent_id=parent_id, child_id=child_id)
            for parent_id, child_id in queryset.values_list("parent_id", "child_id")
        ]

    def bulk_save(self, closures: list[IFunctionClosureRepo.Closure]) -> None:
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
        with transaction.atomic():
            FunctionHierarchy.objects.bulk_create(objects)

    def bulk_delete(self, closures: list[IFunctionClosureRepo.Closure]) -> None:
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

    def get_all_ancestors(self, root_function_id: str) -> list[str | None]:
        """주어진 함수의 모든 상위 함수 ID를 조회합니다."""
        # 초기 CTE 정의 - root_function_id를 기준으로 직접 부모들 찾기
        ancestors_cte = With(
            FunctionHierarchy.objects.filter(child_id=root_function_id)
            .values("parent_id")
            .annotate(child_id=Cast(Value(root_function_id), IntegerField()))
        )

        # CTE를 사용하여 모든 상위 함수들을 재귀적으로 검색
        all_ancestors = (
            ancestors_cte.join(FunctionHierarchy, child_id=ancestors_cte.col.parent_id)
            .with_cte(ancestors_cte)
            .values_list("parent_id", flat=True)
            .distinct()  # 중복 제거
        )

        return list(all_ancestors)
