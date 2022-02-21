from django.urls import path
from .views import IntervalRequestView

app_name = "Intervalhapp"

urlpatterns = [
    path('interval/', IntervalRequestView.as_view(), name="interval_request"),
]
