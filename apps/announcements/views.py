from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from apps.announcements.models import Announcement
from apps.announcements.serializers import AnnouncementSerializer


class AnnouncementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)

        return Response({
            'message': 'Announcement successfully created',
            'data': serializer.data
        }, status=status.HTTP_200_OK
     )

    def get(self, request):
        announcements = Announcement.objects.all()
        serializer = AnnouncementSerializer(announcements,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
