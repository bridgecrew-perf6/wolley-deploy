from django.urls import path
from .views import PathDailyRequestView, MonthlyRequestView, PieChartRequestView, MapRequestView

app_name = "dailypathapp"

urlpatterns = [
    path('path/daily/', PathDailyRequestView.as_view(), name="pathdaily_request"),
    path('monthly/', MonthlyRequestView.as_view(), name="monthly_request"),
    path('piechart/', PieChartRequestView.as_view(),name="piechart_request"),
    path('map/', MapRequestView.as_view(), name="map_request"),
]