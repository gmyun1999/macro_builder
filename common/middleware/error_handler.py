from django.utils.deprecation import MiddlewareMixin

from common.interface.response import error_response

# class CustomServerErrorMiddleware(MiddlewareMixin):
#     def process_exception(self, request, exception):
#         # 500 에러를 503 에러로 변경하여 클라이언트에 반환
#         code = "Service Unavailable"
#         message = "일시적인 서버 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

#         return error_response(code=code, message=message, status=503)
