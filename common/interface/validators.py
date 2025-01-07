import copy
from functools import wraps
from typing import Type

from django.http import JsonResponse
from pydantic import BaseModel, ValidationError
from rest_framework import status
from rest_framework.parsers import JSONParser

from common.interface.response import error_response


def validate_query_params(model: Type[BaseModel]):
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            params = request.GET.dict()
            try:
                validated_params = model.model_validate(params)
            except ValidationError as e:
                return error_response(
                    code="VALIDATE_QUERY_ERROR",
                    message="query params validation error",
                    detail={"details": e.errors()},
                )

            return f(*args, **kwargs, params=validated_params)

        return wrapper

    return decorated_func


def validate_body(model: Type[BaseModel]):
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            body = JSONParser().parse(request)
            try:
                validated_body = model.model_validate(body)
            except ValidationError as e:
                print(e.errors())
                return error_response(
                    code="VALIDATE_BODY_ERROR",
                    message="Body validation error",
                    detail={"details": e.errors()},
                )

            return f(*args, **kwargs, body=validated_body)

        return wrapper

    return decorated_func


def validate_form_data(model: Type[BaseModel]):
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]

            form_data = {}
            for key, value in copy.deepcopy(request.POST).items():
                form_data[key] = value
            for key, value in request.FILES.items():
                form_data[key] = value

            try:
                validated_form_data = model.model_validate(form_data)
            except ValidationError as e:
                return error_response(
                    code="VALIDATE_FORM_DATA_ERROR",
                    message="form validation error",
                    detail={"details": e.errors()},
                )

            return f(*args, **kwargs, form_data=validated_form_data)

        return wrapper

    return decorated_func
