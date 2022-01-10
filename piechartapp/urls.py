from django.urls import path
from .views import PiechartRequestView

app_name = "piechartapp"

urlpatterns = [
    path('piechart/', PiechartRequestView.as_view(), name="piechart_request"),
]