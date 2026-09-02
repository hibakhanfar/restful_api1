from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ('author', 'title','content')
        extra_kwargs = {'author': {'read_only': True}}
