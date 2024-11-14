from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import OuterRef, Q, Subquery
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
        """ """
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
