from django.urls import path
from .views import PiechartRequestView

app_name = "dailypathapp"

urlpatterns = [
    path('path/daily/', PiechartRequestView.as_view(), name="pathdaily_request"),
]
