from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from macro_be.settings import ENV


class HealthChecker(APIView):
    def get(self, request):
        return JsonResponse(
            data={"status": "success", "ENV": ENV},
            status=status.HTTP_200_OK,
        )
