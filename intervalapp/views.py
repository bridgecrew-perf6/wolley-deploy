from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accountapp.models import AppUser, Estimate
from dailypathapp.models import DailyPath
from dailypathapp.utils import coordinate2address, get_visited_place
from intervalapp.models import IntervalStay
from intervalapp.utils import search_location
from myapi.utils import make_response_content, make_interval_stay_to_data


@method_decorator(csrf_exempt, name='dispatch')
class IntervalRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_interval_id = request.headers['intervalId']

        try:
            interval_obj = IntervalStay.objects.get(id=request_interval_id)
        except IntervalStay.DoesNotExist:
            content = make_response_content("Interval 기록 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        data = make_interval_stay_to_data(interval_obj)
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        request_interval_id = request.data["intervalId"]

        try:
            interval_obj = IntervalStay.objects.get(id=request_interval_id)
        except IntervalStay.DoesNotExist:
            content = make_response_content("Interval 기록 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        app_user_obj = AppUser.objects.get(user=interval_obj.daily_path.user)

        Estimate.objects.create(
            user=app_user_obj,
            category=request.data["category"],
            location=request.data["location"],
            location_id=request.data["locationId"],
            latitude=request.data["coordinates"]["latitude"],
            longitude=request.data["coordinates"]["longitude"]
        )
        print("estimate save")

        daily_path_objs = DailyPath.objects.filter(user=app_user_obj)
        for daily_path_obj in daily_path_objs:
            interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj)
            for interval_stay_obj in interval_stay_objs:
                if interval_stay_obj.category == "?":
                    interval_stay_obj.category = get_visited_place(
                        interval_stay_obj.latitude,
                        interval_stay_obj.longitude,
                        app_user_obj
                    )
                    interval_stay_obj.save()

        interval_obj.category = request.data["category"]
        interval_obj.location = request.data["location"]
        interval_obj.location_id = request.data["locationId"]
        interval_obj.latitude = request.data["coordinates"]["latitude"]
        interval_obj.longitude = request.data["coordinates"]["longitude"]
        interval_obj.address = coordinate2address(
            request.data["coordinates"]["latitude"],
            request.data["coordinates"]["longitude"]
        )
        interval_obj.save()

        data = make_interval_stay_to_data(interval_obj)
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class LocationRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_interval_id = int(request.data['intervalId'])
        request_keyword = request.data['keyword']

        try:
            interval_stay_obj = IntervalStay.objects.get(id=request_interval_id)
        except IntervalStay.DoesNotExist:
            content = make_response_content("interval 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = search_location(request_keyword, interval_stay_obj.latitude, interval_stay_obj.longitude)
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)