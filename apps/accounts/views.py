from rest_framework import status, permissions
from rest_framework.response import Response
#from .serializers
from apps.accounts.models import User
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import datetime
import jwt


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        pass
