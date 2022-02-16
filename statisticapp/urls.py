from django.urls import path
from .views import BadgeRequestView

app_name = "statisticapp"

urlpatterns = [
    path('badge/', BadgeRequestView.as_view(), name="badge_request"),
]
