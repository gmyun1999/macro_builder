from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, Type, Union, cast, get_args, get_origin

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from rest_framework import serializers


class PydanticToDjangoSerializer:
    """
    Pydantic 모델을 Django REST framework 시리얼라이저로 변환하는 유틸리티 클래스
    Python 3.9+ 호환
    """

    TYPE_MAPPING = {
        str: serializers.CharField,
        int: serializers.IntegerField,
        float: serializers.FloatField,
        bool: serializers.BooleanField,
        datetime: serializers.DateTimeField,
        date: serializers.DateField,
        Decimal: serializers.DecimalField,
        dict: serializers.JSONField,
        list: serializers.ListField,
    }

    @classmethod
    def convert(
        cls, pydantic_model: Type[BaseModel], serializer_name: str | None = None
    ) -> Type[serializers.Serializer]:
        """
        Pydantic 모델을 Django 시리얼라이저 클래스로 변환

        Args:
            pydantic_model: 변환할 Pydantic 모델 클래스
            serializer_name: 생성될 시리얼라이저의 이름 (기본값: {모델명}Serializer)

        Returns:
            Django REST framework Serializer 클래스
        """
        if not serializer_name:
            serializer_name = f"{pydantic_model.__name__}Serializer"

        fields = {}
        model_fields = pydantic_model.model_fields

        for field_name, model_field in model_fields.items():
            field_type = model_field.annotation
            django_field = cls._convert_field(field_type, model_field)
            fields[field_name] = django_field

        return type(serializer_name, (serializers.Serializer,), fields)

    @classmethod
    def _convert_field(
        cls, field_type: Any, field_info: FieldInfo
    ) -> serializers.Field:
        """단일 필드를 Django 시리얼라이저 필드로 변환"""

        # Union 타입 처리 (예: Union[str, None])
        origin = get_origin(field_type)
        if origin is Union:
            args = get_args(field_type)
            # None이 포함된 경우 required=False로 설정
            if type(None) in args:
                remaining_types = [arg for arg in args if arg is not type(None)]
                if len(remaining_types) == 1:
                    return cls._create_field(
                        remaining_types[0], field_info, required=False
                    )

        # 기본 타입 변환
        return cls._create_field(field_type, field_info)

    @classmethod
    def _create_field(
        cls, field_type: Any, field_info: FieldInfo, required: bool | None = None
    ) -> serializers.Field:
        """
        필드 타입과 정보를 바탕으로 Django 시리얼라이저 필드 생성
        """
        # Enum 처리
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            choices = [(e.value, e.name) for e in field_type]
            return serializers.ChoiceField(choices=choices)

        # 중첩된 Pydantic 모델 처리
        if isinstance(field_type, type) and issubclass(field_type, BaseModel):
            nested_serializer = cls.convert(field_type)
            return nested_serializer()

        # 리스트 처리
        origin = get_origin(field_type)
        if origin is list:
            args = get_args(field_type)
            if args:
                child_type = args[0]
                if isinstance(child_type, type) and issubclass(child_type, BaseModel):
                    return serializers.ListSerializer(child=cls.convert(child_type)())
                else:
                    child_field = cls._create_field(child_type, field_info)
                    return serializers.ListField(child=child_field)

        # 기본 타입 매핑
        field_class = cls.TYPE_MAPPING.get(field_type, serializers.CharField)

        field_kwargs: Dict[str, Any] = {
            "required": required if required is not None else field_info.is_required()
        }

        # 추가 필드 옵션 설정
        if hasattr(field_info, "max_length"):
            field_kwargs["max_length"] = field_info.max_length

        if field_class is serializers.DecimalField:
            field_kwargs.update(
                {
                    "max_digits": 16,  # 기본값 설정
                    "decimal_places": 4,
                }
            )

        return field_class(**field_kwargs)
