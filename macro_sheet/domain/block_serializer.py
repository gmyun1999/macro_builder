from dataclasses import asdict, fields, is_dataclass
from enum import Enum
from typing import Any, Type, Union, get_args, get_origin

from macro_sheet.domain.block.block import Block
from macro_sheet.domain.registry import BLOCK_TYPE_REGISTRY


class GenericSerializer:
    def __init__(self, data: dict[str, Any]):
        self.data = data
        self.validated_data: dict[str, Any] = {}
        self.errors: dict[str, str] = {}
        self.domain_class: Type[Block] = self.get_domain_class()

    def get_domain_class(self) -> Type[Block]:
        block_type_value = self.data.get("block_type")
        if not block_type_value:
            raise ValueError("Missing 'block_type' in data.")

        domain_class = BLOCK_TYPE_REGISTRY.get(block_type_value)
        if not domain_class:
            raise ValueError(f"Unsupported block_type: {block_type_value}")

        return domain_class

    def validate_field(self, field_type: Any, value: Any, field_name: str) -> Any:
        origin = get_origin(field_type)
        args = get_args(field_type)

        # Handle Optional types (e.g., Type | None)
        if origin is Union and type(None) in args:
            non_none_args = [arg for arg in args if arg is not type(None)]
            if not non_none_args:
                raise ValueError(f"{field_name} has an unsupported type.")
            field_type = non_none_args[0]
            if value is None:
                return None

        # Handle Enums
        if isinstance(field_type, type) and issubclass(field_type, Enum):
            try:
                return field_type(value)
            except ValueError:
                raise ValueError(f"{field_name} must be a valid {field_type.__name__}.")

        # Handle list types (e.g., list[Block])
        if origin is list:
            item_type = args[0]
            if not isinstance(value, list):
                raise ValueError(f"{field_name} must be a list.")
            validated_list = []
            for index, item in enumerate(value):
                try:
                    validated_item = self.validate_field(
                        item_type, item, f"{field_name}[{index}]"
                    )
                    validated_list.append(validated_item)
                except ValueError as ve:
                    self.errors[f"{field_name}[{index}]"] = str(ve)
            return validated_list

        # Handle dict types (e.g., dict[str, Any])
        if origin is dict:
            key_type, val_type = args
            if not isinstance(value, dict):
                raise ValueError(f"{field_name} must be a dict.")
            validated_dict = {}
            for key, val in value.items():
                try:
                    validated_key = self.validate_field(
                        key_type, key, f"{field_name} key"
                    )
                    validated_val = self.validate_field(
                        val_type, val, f"{field_name}[{key}]"
                    )
                    validated_dict[validated_key] = validated_val
                except ValueError as ve:
                    self.errors[f"{field_name}[{key}]"] = str(ve)
            return validated_dict

        # Handle nested dataclasses (Blocks)
        if is_dataclass(field_type) and issubclass(field_type, Block):
            if not isinstance(value, dict):
                raise ValueError(
                    f"{field_name} must be a dict representing {field_type.__name__}."
                )
            nested_serializer = GenericSerializer(value)
            if nested_serializer.is_valid():
                return nested_serializer.to_domain_object()
            else:
                self.errors[field_name] = str(nested_serializer.errors)
                return None

        # Handle basic types
        if not isinstance(value, field_type):
            raise ValueError(f"{field_name} must be of type {field_type.__name__}.")
        return value

    def validate(self) -> dict[str, Any]:
        validated_data: dict[str, Any] = {}
        for field_info in fields(self.domain_class):
            field_name = field_info.name
            field_type = field_info.type

            # Handle missing fields
            if field_name not in self.data:
                # Check if the field has a default or is Optional
                if field_info.default is not field_info.default_factory or (
                    get_origin(field_type) is Union
                    and type(None) in get_args(field_type)
                ):
                    if field_info.default is not field_info.default_factory:
                        validated_data[field_name] = field_info.default
                    else:
                        validated_data[field_name] = None
                    continue
                else:
                    self.errors[field_name] = f"{field_name} is required."
                    continue

            value = self.data[field_name]

            # Handle Optional fields
            if get_origin(field_type) is Union and type(None) in get_args(field_type):
                if value is None:
                    validated_data[field_name] = None
                    continue

            try:
                validated_value = self.validate_field(field_type, value, field_name)
                validated_data[field_name] = validated_value
            except ValueError as ve:
                self.errors[field_name] = str(ve)

        if self.errors:
            raise ValueError("Validation failed.")

        self.validated_data = validated_data
        return validated_data

    def to_domain_object(self) -> Block:
        if not self.validated_data:
            self.validate()
        return self.domain_class(**self.validated_data)

    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except ValueError:
            return False
