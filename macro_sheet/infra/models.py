import uuid

from django.db import models
from django_cte import CTEManager

from user.infra.models.user import User


class Function(models.Model):
    """
    Function 모델은 블록에서 참조되는 기능을 나타냅니다.
    """

    id = models.CharField(primary_key=True, max_length=36)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="functions", db_constraint=False
    )
    name = models.CharField(max_length=255)
    blocks = models.JSONField(default=list)
    raw_blocks = models.JSONField(default=list)

    class Meta:
        db_table = "Function"


class Worksheet(models.Model):
    """
    Worksheet 모델은 사용자 작업 공간을 나타내며, 블록들을 JSON 형식으로 저장합니다.
    """

    id = models.CharField(primary_key=True, max_length=36)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="worksheets",
        db_constraint=False,
    )
    main_block = models.JSONField(default=None)
    blocks = models.JSONField(default=list)
    raw_main_block = models.JSONField(default=list)
    raw_blocks = models.JSONField(default=list)

    class Meta:
        db_table = "Worksheet"


class WorksheetFunction(models.Model):
    """
    WorksheetFunction 모델은 Worksheet와 Function 간의 다대다 관계를 관리합니다.
    """

    worksheet = models.ForeignKey(
        Worksheet, on_delete=models.CASCADE, db_constraint=False
    )
    function = models.ForeignKey(
        Function, on_delete=models.CASCADE, db_constraint=False
    )

    class Meta:
        db_table = "WorksheetFunction"
        unique_together = ("worksheet", "function")
        indexes = [
            models.Index(fields=["worksheet"]),
            models.Index(fields=["function"]),
        ]


class FunctionHierarchy(models.Model):
    """
    FunctionHierarchy 모델은 Function 간의 모든 상위-하위 관계를 관리합니다.
    """

    parent = models.ForeignKey(
        Function, related_name="parent", on_delete=models.CASCADE, db_constraint=False
    )
    child = models.ForeignKey(
        Function, related_name="child", on_delete=models.CASCADE, db_constraint=False
    )

    objects = CTEManager()

    class Meta:
        db_table = "FunctionHierarchy"
        unique_together = ("parent", "child")
        indexes = [
            models.Index(fields=["parent"]),
            models.Index(fields=["child"]),
        ]


class Gui(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500)

    class Meta:
        db_table = "Gui"


class Script(models.Model):
    """
    gui 만들때 같이 만들어지는 스크립트
    동일한 스크립트가 있는지 확인할때 hash 값으로 비교한다.
    """

    id = models.CharField(max_length=255, primary_key=True)
    script_code = models.TextField()
    script_hash = models.CharField(max_length=64, unique=True)
    gui = models.ForeignKey(
        Gui, related_name="script_gui", on_delete=models.CASCADE, db_constraint=False
    )

    class Meta:
        db_table = "Script"
