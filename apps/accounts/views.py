from rest_framework import status, permissions
from rest_framework.response import Response
from .serializers import ProfileSerializer
from apps.accounts.models import Profile
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
       profile, created = Profile.objects.get_or_create(user=request.user)
       serializer = ProfileSerializer(profile)
       return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request):
       profile, created = Profile.objects.get_or_create(user=request.user)
       serializer = ProfileSerializer(profile, data=request.data, partial=True)
       if serializer.is_valid(raise_exception=True):
           serializer.save()
       return Response({
           "message": "Profile updated successfully",
           "data": serializer.data
       }, status=status.HTTP_200_OK)
