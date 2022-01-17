from django.urls import path
from .views import RecommendationRequestView

app_name = "diaryapp"

urlpatterns = [
    path('recommendation/', RecommendationRequestView.as_view(), name="recommendation_request"),
]