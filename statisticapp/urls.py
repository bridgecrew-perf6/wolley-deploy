from django.urls import path
from .views import BadgeRequestView, DummyBadgeRequestView, BadgeListRequestView

app_name = "statisticapp"

urlpatterns = [
    path('badge/', BadgeRequestView.as_view(), name="badge_request"),
    path('badge/list/', BadgeListRequestView.as_view(), name="badge_request"),
    path('badge/dummy/', DummyBadgeRequestView.as_view(), name="dummy_badge_request"),

]
