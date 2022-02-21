from django.urls import path
from .views import IntervalRequestView, LocationRequestView

app_name = "Intervalhapp"

urlpatterns = [
    path('interval/', IntervalRequestView.as_view(), name="interval_request"),
    path('location/', LocationRequestView.as_view(), name="search_location_request"),
]
