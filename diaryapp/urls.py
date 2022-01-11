from django.urls import path
from .views import DiaryRequestView, DiaryRequestApiView

app_name = "diaryapp"

urlpatterns = [
    path('diary/', DiaryRequestView.as_view(), name="diary_request"),
    path('diaryApi/', DiaryRequestApiView.as_view(), name="diary_request"),
]