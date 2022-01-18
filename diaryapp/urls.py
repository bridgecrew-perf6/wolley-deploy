from django.urls import path
from .views import DiaryRequestView

app_name = "diaryapp"

urlpatterns = [
    path('diary/', DiaryRequestView.as_view(), name="diary_request"),
]