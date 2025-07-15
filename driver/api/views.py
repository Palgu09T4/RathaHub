# driver/api_views.py


from rest_framework.response import Response
from rest_framework import status
from driver.models import Driver
from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView

class DeleteDriverByIdAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]  # uses Django login sessions

    def delete(self, request, id):
        driver = get_object_or_404(Driver, id=id)

        if driver.user:
            driver.user.delete()

        driver.delete()
        return Response({"message": "Driver deleted successfully."}, status=status.HTTP_200_OK)
