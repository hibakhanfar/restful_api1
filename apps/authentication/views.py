from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from apps.accounts.models import User
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import datetime
import jwt


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
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload ={
            'id': user.id,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }

        token=jwt.encode(payload, settings.JWT_SECRET_KEY,algorithm='HS256')

        return Response( {
            'jwt':token
        })
