from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer
from apps.accounts.models import User
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed


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

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        return Response(
            {
                "message": "WELCOME",
                "id": user.id,
                "email": user.email,
            },
            status=status.HTTP_200_OK
        )
