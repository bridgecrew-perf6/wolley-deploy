from django.urls import path
from .views import PiechartRequestView

app_name = "dailypathapp"

urlpatterns = [
    path('piechart/', PiechartRequestView.as_view(), name="piechart_request"),
]