from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class HealthCheckView(APIView):
    """
    Health check of service. Should return 200
    """
    def get(self, request):
        return Response({}, status=status.HTTP_200_OK)
