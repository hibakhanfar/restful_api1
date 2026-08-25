from django.urls import path
from .views import  AnnouncementView

urlpatterns = [
    path('announcement/', AnnouncementView.as_view(), name='announcement'),
]
