from django.urls import path
from .views import StatRequestView

app_name = "statisticapp"

urlpatterns = [
    path('stat/', StatRequestView.as_view(), name="stat_request"),
]
