from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from apps.accounts.models import User
from rest_framework.views import APIView


class RegisterView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
      serializer = RegisterSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
          serializer.save()
          return Response(
              {
                  "message": "User registered successfully",
                  "data": serializer.data
              },
              status=status.HTTP_201_CREATED
          )
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
