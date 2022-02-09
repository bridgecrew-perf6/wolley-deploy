from datetime import datetime, timedelta
import time
from typing import List, Dict, Tuple

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from dailypathapp.stayPointDetectionDensity import generatePoints, stayPointExtraction, Point
from dailypathapp.utils import coordinate2address, get_visited_place, get_distance

from accountapp.models import AppUser

from dailypathapp.models import DailyPath, GPSLog
from intervalapp.models import IntervalStay, IntervalMove
from myapi.utils import make_response_content, check_interval_objs, check_daily_path_objs, check_daily_path_obj


def make_date_range(start: str, end: str) -> List:
    date_range = []
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    delta = end_date - start_date
    for i in range(delta.days+1):
        now = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        date_range.append(now)
    return date_range


def make_date_data(date: str, longitude: float, latitude: float) -> Dict:
    date_data = {
        "time": date,
        "coordinates": {
            "longitude": longitude,
            "latitude": latitude
        }
    }
    return date_data


def make_date_sequence(time_sequence: List[Dict], user: AppUser) -> Dict:
    if not time_sequence:
        return {}

    start_date = time_sequence[0]['time'][:10]
    end_date = time_sequence[-1]['time'][:10]
    date_range = make_date_range(start_date, end_date)
    date_sequence = {d: [] for d in date_range}

    for time_seq in time_sequence:
        date_sequence[time_seq['time'][:10]].append(time_seq)

    end_flag = len(date_sequence) - 1
    for idx, date_key in enumerate(date_sequence.keys()):
        if not date_sequence[date_key]:
            continue

        try:
            daily_path = DailyPath.objects.get(user=user, date=date_key)
            gps_log = GPSLog.objects.filter(daily_path=daily_path).order_by('timestamp').last()
            start_data = make_date_data(
                gps_log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                gps_log.longitude,
                gps_log.latitude
            )
            date_sequence[date_key].insert(0, start_data)
        except:
            start_data = make_date_data(
                date_key + " 00:00:00",
                date_sequence[date_key][0]['coordinates']['longitude'],
                date_sequence[date_key][0]['coordinates']['latitude']
            )
            date_sequence[date_key].insert(0, start_data)


        if idx != end_flag:
            end_data = make_date_data(
                date_key + " 23:59:59",
                date_sequence[date_key][-1]['coordinates']['longitude'],
                date_sequence[date_key][-1]['coordinates']['latitude']
            )
            date_sequence[date_key].append(end_data)
    return date_sequence


def make_gps_logs(date_sequence: List[Dict]) -> List[Tuple]:
    gps_logs = [
        (
            date['coordinates']['latitude'],
            date['coordinates']['longitude'],
            date['time']
        ) for date in date_sequence
    ]
    return gps_logs


def make_percent(start: str, end: str) -> float:
    _, start_time = start.split()
    _, end_time = end.split()

    start_hour, start_min, start_sec = map(int, start_time.split(':'))
    end_hour, end_min, end_sec = map(int, end_time.split(':'))

    start_total = start_hour * 3600 + start_min * 60 + start_sec
    end_total = end_hour * 3600 + end_min * 60 + end_sec

    return round((end_total - start_total) / 86400, 2)


def make_stay_interval(app_user: AppUser, daily_path: DailyPath, stay_point_centers: List[Tuple]) -> None:
    print("Interval Stay")
    for point in stay_point_centers:
        start_time = point.arriveTime
        end_time = point.leaveTime
        percent = make_percent(start_time, end_time)
        latitude = point.latitude
        longitude = point.longitude
        address = coordinate2address(point.latitude, point.longitude)
        IntervalStay.objects.create(
            daily_path=daily_path,
            start_time=start_time,
            end_time=end_time,
            address=address,
            category=get_visited_place(latitude, longitude, app_user),
            location="?",
            latitude=latitude,
            longitude=longitude,
            percent=percent
        )


def make_move_interval(app_user: AppUser, daily_path: DailyPath, move_points: List[Tuple]) -> None:
    print("Interval Move")
    for start_time, end_time in move_points:
        percent = make_percent(start_time, end_time)
        IntervalMove.objects.create(
            daily_path=daily_path,
            start_time=start_time,
            end_time=end_time,
            transport="?",
            percent=percent
        )


def check_last_interval(interval_stay_obj: IntervalStay, interval_move_obj: IntervalMove) -> str:
    if not interval_stay_obj and not interval_move_obj:
        return "none"
    elif not interval_stay_obj and interval_move_obj:
        return "move"
    elif interval_stay_obj and not interval_move_obj:
        return "stay"
    else:
        if interval_stay_obj.start_time > interval_move_obj.start_time:
            return "stay"
        else:
            return "move"


# 나중에 함수 분리하기
def make_move_point(points: Point, stay_point_centers: List[Point]) -> List:
    move_range = []
    flag = "stay"

    if not stay_point_centers:
        move_range.append((points[0].dateTime, points[-1].dateTime))
        flag = "move"
        return move_range, flag

    if points[0].dateTime != stay_point_centers[0].arriveTime:
        move_range.append((points[0].dateTime, stay_point_centers[0].arriveTime))
        flag = "move"

    for i in range(len(stay_point_centers)-1):
        move_range.append((stay_point_centers[i].leaveTime, stay_point_centers[i+1].arriveTime))

    if points[-1].dateTime != stay_point_centers[-1].leaveTime:
        move_range.append((stay_point_centers[-1].leaveTime, points[-1].dateTime))

    return move_range, flag


@method_decorator(csrf_exempt, name='dispatch')
class PathDailyRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):

        request_user = request.data['user']
        user, created = User.objects.get_or_create(username=request_user)
        if created:
            user.set_password('123')
            user.save()

        app_user, _ = AppUser.objects.get_or_create(user=user)
        request_time_sequence = request.data['timeSequence']
        date_sequence = make_date_sequence(request_time_sequence, app_user)
        print(date_sequence)
        # for date_key, date_value in date_sequence.items():
        #     daily_path, created = DailyPath.objects.get_or_create(user=app_user, date=date_key)
        #
        #     if not date_value:
        #         continue
        #
        #     # GPS log 저장
        #     for date in date_value:
        #         GPSLog.objects.create(
        #             daily_path=daily_path,
        #             timestamp=datetime.strptime(date['time'], '%Y-%m-%d %H:%M:%S'),
        #             latitude=date['coordinates']['latitude'],
        #             longitude=date['coordinates']['longitude']
        #         )
        #     gps_logs = make_gps_logs(date_value)
        #     points = generatePoints(gps_logs)
        #     stay_point_centers, stay_points = stayPointExtraction(points)
        #     move_points, add_flag = make_move_point(points, stay_point_centers)
        #
        #     interval_stay_obj = IntervalStay.objects.filter(daily_path=daily_path).order_by('start_time').last()
        #     interval_move_obj = IntervalMove.objects.filter(daily_path=daily_path).order_by('start_time').last()
        #     interval_flag = check_last_interval(interval_stay_obj, interval_move_obj)
        #
        #     print(interval_flag, add_flag)
        #     if interval_flag == "move" and add_flag == "move":
        #         _, end_time = move_points.pop(0)
        #         interval_move_obj.end_time = end_time
        #         interval_move_obj.percent = make_percent(
        #             interval_move_obj.start_time.strftime('%Y-%m-%d %H:%M:%S'),
        #             end_time
        #         )
        #         interval_move_obj.save()
        #     elif interval_flag == "stay" and add_flag == "stay":
        #         point = stay_point_centers.pop(0)
        #         d = get_distance(
        #             interval_stay_obj.latitude,
        #             interval_stay_obj.longitude,
        #             point.latitude,
        #             point.longitude
        #         )
        #         if d < 200:
        #             interval_stay_obj.end_time = point.leaveTime
        #             interval_stay_obj.save()
        #         else:
        #             stay_point_centers.insert(0, point)
        #
        #     make_stay_interval(app_user, daily_path, stay_point_centers)
        #     make_move_interval(app_user, daily_path, move_points)
        #     print("daily path 하나 성공")

        content = make_response_content("성공", {})
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class MonthlyRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content, status_code, daily_path_objs = check_daily_path_objs(request)
        if status_code == status.HTTP_200_OK:
            for daily_path_obj in daily_path_objs:
                interval_stay_objs = IntervalStay.objects.filter(daily_path_id=daily_path_obj.id)
                interval_move_objs = IntervalMove.objects.filter(daily_path_id=daily_path_obj.id)
                info_data = list()
                info_data.extend([
                    {
                        "id": interval_obj.id,
                        "category": interval_obj.category,
                        "percent": interval_obj.percent,
                        "start": interval_obj.start_time
                    } for interval_obj in interval_stay_objs
                ])
                info_data.extend([
                    {
                        "id": interval_obj.id,
                        "category": "이동",
                        "percent": interval_obj.percent,
                        "start": interval_obj.start_time
                    } for interval_obj in interval_move_objs
                ])
                info_data = sorted(info_data, key=lambda info: info['start'])

                daily_path_data = {
                    "id": daily_path_obj.id,
                    "date": daily_path_obj.date,
                    "info": info_data
                }
                content['data'].append(daily_path_data)
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class PieChartRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content, status_code, interval_stay_objs, interval_move_objs = check_interval_objs(request)
        if status_code == status.HTTP_200_OK:
            info_data = list()
            info_data.extend([
                {
                    "id": interval_obj.id,
                    "category": interval_obj.category,
                    "detail": interval_obj.location,
                    "percent": interval_obj.percent,
                    "start": interval_obj.start_time
                } for interval_obj in interval_stay_objs
            ])
            info_data.extend([
                {
                    "id": interval_obj.id,
                    "category": "이동",
                    "detail": interval_obj.transport,
                    "percent": interval_obj.percent,
                    "start": interval_obj.start_time
                } for interval_obj in interval_move_objs
            ])
            info_data = sorted(info_data, key=lambda info: info['start'])
            content['data']['info'] = info_data
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class MapRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content, status_code, interval_stay_objs, _ = check_interval_objs(request)
        if status_code == status.HTTP_200_OK:
            info_data = [
                {
                    "id": interval_obj.id,
                    "category": interval_obj.category,
                    "address": interval_obj.address,
                    "coordinates": {
                        "latitude": interval_obj.latitude,
                        "longitude": interval_obj.longitude
                    }
                } for interval_obj in interval_stay_objs
            ]
            content['data']['info'] = info_data
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class MapLogRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content, status_code, daily_path_obj = check_daily_path_obj(request)
        if status_code == status.HTTP_200_OK:
            map_log_objs = GPSLog.objects.filter(daily_path=daily_path_obj)
            content['data']['info'] = [
                {
                    "coordinates": {
                        "latitude": map_log_obj.latitude,
                        "longitude": map_log_obj.longitude
                    }
                } for map_log_obj in map_log_objs
            ]
        return Response(content, status=status_code)
