from functools import wraps

from django.http import JsonResponse
from rest_framework import status

from common.interface.response import error_response
from common.response_msg import MESSAGE
from common.service.token.i_token_parser import ITokenParser
from user.domain.user_role import UserRoles
from user.domain.user_token import UserTokenType
from user.infra.token.user_token_parser import UserTokenParser


def validate_token(
    roles: list = UserRoles.USER_ROLES,
    validate_type: str = UserTokenType.ACCESS,
):
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            request = args[1]
            headers = request.headers

            # TODO: DI 적용
            token_parser: ITokenParser = UserTokenParser()
            token = token_parser.get_token(http_header=headers)
            token_payload_vo, result_message = token_parser.check_token(
                token=token,
                allowed_roles=roles,
                validate_type=validate_type,
            )

            if token_payload_vo is None:
                return error_response(
                    code="VALIDATE_TOKEN_ERROR", message=result_message, status=403
                )

            return f(*args, **kwargs, token_payload=token_payload_vo)

        return wrapper

    return decorated_func
