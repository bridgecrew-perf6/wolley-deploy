from django.urls import path
from .views import DiaryRequestView, TopicRequestView

app_name = "diaryapp"

urlpatterns = [
    path('diary/', DiaryRequestView.as_view(), name="diary_request"),
    path('topic/', TopicRequestView.as_view(), name="topic_request"),
]