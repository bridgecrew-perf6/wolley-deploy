from datetime import datetime
from typing import Dict, Union, List

from django.db.models import QuerySet
from django.http import HttpRequest
from rest_framework import status

from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import IntervalStay, IntervalMove


def make_response_content(response_msg: str, data: Union[Dict, List]) -> Dict:
    content = dict()
    content['responseMsg'] = response_msg
    content['data'] = data
    return content


def check_interval_objs(request_user: str, request_date: str) -> (Dict, int, QuerySet):
    try:
        user = AppUser.objects.get(user__username=request_user)
        daily_path = DailyPath.objects.get(user=user, date=request_date)
        interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path.id)
        interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path.id)
        data = {
            "id": daily_path.id,
            "date": daily_path.date,
            "info": list()
        }
        content = make_response_content("성공", data)
        return content, status.HTTP_200_OK, interval_stay_objs, interval_move_objs
    except AppUser.DoesNotExist:
        content = make_response_content("User 없음", {})
    except DailyPath.DoesNotExist:
        content = make_response_content("Daily 기록 없음", {})
    except IntervalStay.DoesNotExist:
        content = make_response_content("Interval 기록 없음", {})
    return content, status.HTTP_400_BAD_REQUEST, None, None


## 요것도 분리하기
def check_daily_path_objs(request: HttpRequest) -> (Dict, int, QuerySet):
    request_user = request.headers['user']
    request_date = request.headers['date']
    year, month, _ = request_date.split('-')

    try:
        user = AppUser.objects.get(user__username=request_user)
        daily_path_objs = DailyPath.objects.filter(user=user, date__year=year, date__month=month)
        content = make_response_content("성공", [])
        return content, status.HTTP_200_OK, daily_path_objs
    except AppUser.DoesNotExist:
        content = make_response_content("user 없음", {})
    except DailyPath.DoesNotExist:
        content = make_response_content("Monthly 기록 없음", {})
    return content, status.HTTP_400_BAD_REQUEST, None


def check_daily_path_obj(request: HttpRequest) -> (Dict, int, DailyPath):
    request_user = request.headers['user']
    request_date = request.headers['date']
    try:
        user = AppUser.objects.get(user__username=request_user)
        daily_path_obj = DailyPath.objects.get(user=user, date=request_date)
        content = make_response_content("성공", {})
        return content, status.HTTP_200_OK, daily_path_obj
    except AppUser.DoesNotExist:
        content = make_response_content("user 없음", {})
    except DailyPath.DoesNotExist:
        content = make_response_content("daily path 없음", {})
    return content, status.HTTP_400_BAD_REQUEST, None


def make_interval_stay_to_data(interval_obj: IntervalStay) -> Dict:
    data = {
        "id": interval_obj.id,
        "category": interval_obj.category,
        "location": interval_obj.location,
        "address": interval_obj.address,
        "coordinates": {
            "latitude": interval_obj.latitude,
            "longitude": interval_obj.longitude
        },
        "time": {
            "start": interval_obj.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "end": interval_obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
        },
        "percent": interval_obj.percent
    }
    return data


def update_before_interval_end_time(daily_path: DailyPath, start_time: datetime, start: str) -> None:
    pass


def update_after_interval_start_time(daily_path: DailyPath, end_time: datetime, end: str) -> None:
    pass