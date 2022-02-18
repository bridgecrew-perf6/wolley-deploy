from django.urls import path
from .views import BadgeRequestView, DummyBadgeRequestView

app_name = "statisticapp"

urlpatterns = [
    path('badge/', BadgeRequestView.as_view(), name="badge_request"),
    path('badge/dummy/', DummyBadgeRequestView.as_view(), name="dummy_badge_request"),

]
