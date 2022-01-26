from datetime import datetime
import time
from typing import List, Dict, Tuple

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from dailypathapp.stayPointDetectionDensity import generatePoints, stayPointExtraction
from dailypathapp.utils import coordinate2address, get_visited_place, get_distance

from accountapp.models import AppUser

from dailypathapp.models import DailyPath, GPSLog
from intervalapp.models import IntervalStay, IntervalMove
from myapi.utils import make_response_content, check_interval_objs, check_daily_path_objs, check_daily_path_obj


def make_date_sequence(time_sequence: List[Dict]) -> (List[List], List[str]):
    date_sequence = []
    date_list = []
    flag = 0
    for idx in range(len(time_sequence) - 1):
        if time_sequence[idx]['time'][:10] != time_sequence[idx + 1]['time'][:10]:
            if flag != 0:
                data = [{
                    "time": time_sequence[flag]['time'][:10] + " 00:00:00",
                    "coordinates": {
                        "longitude": time_sequence[flag]['coordinates']['longitude'],
                        "latitude": time_sequence[flag]['coordinates']['latitude']
                    }
                }]
            else:
                data = []
            data.extend(time_sequence[flag:idx + 1])
            data.append(
                {
                    "time": time_sequence[idx]['time'][:10] + " 23:59:59",
                    "coordinates": {
                        "longitude": time_sequence[idx]['coordinates']['longitude'],
                        "latitude": time_sequence[idx]['coordinates']['latitude']
                    }
                }
            )
            date_sequence.append(data)
            date_list.append(time_sequence[idx]['time'][:10])
            flag = idx + 1

    if flag != len(time_sequence):
        data = [{
            "time": time_sequence[flag]['time'][:10] + " 00:00:00",
            "coordinates": {
                "longitude": time_sequence[flag]['coordinates']['longitude'],
                "latitude": time_sequence[flag]['coordinates']['latitude']
            }
        }]
        data.extend(time_sequence[flag:idx + 1])
        data.append(
            {
                "time": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                "coordinates": {
                    "longitude": time_sequence[idx]['coordinates']['longitude'],
                    "latitude": time_sequence[idx]['coordinates']['latitude']
                }
            }
        )
        date_sequence.append(data)
        date_list.append(time_sequence[flag]['time'][:10])
    return date_sequence, date_list


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


def make_interval(app_user: AppUser, daily_path: DailyPath, stay_point_centers: List[Tuple]) -> None:
    print("Interval Stay")
    for point in stay_point_centers:
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point.arriveTime))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point.leaveTime))
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

    # Interval Move
    print("Interval Move")
    for idx in range(len(stay_point_centers) - 1):
        before_point = stay_point_centers[idx]
        after_point = stay_point_centers[idx + 1]

        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(before_point.leaveTime))
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(after_point.arriveTime))
        percent = make_percent(start_time, end_time)
        IntervalMove.objects.create(
            daily_path=daily_path,
            start_time=start_time,
            end_time=end_time,
            transport="?",
            percent=percent
        )


@method_decorator(csrf_exempt, name='dispatch')
class PathDailyRequestView(APIView):
    permission_classes = [AllowAny]

    # for real 통신
    def post(self, request):
        # user 확인
        request_user = request.data['user']
        user, created = User.objects.get_or_create(username=request_user)
        if created:
            user.set_password('123')
            user.save()

        app_user, _ = AppUser.objects.get_or_create(user=user)

        # time stamp 분리
        time_sequence = request.data['timeSequence']
        date_sequence, date_list = make_date_sequence(time_sequence)

        for i in range(len(date_list)):
            daily_path, created = DailyPath.objects.get_or_create(user=app_user, date=date_list[i])

            for date in date_sequence[i]:
                GPSLog.objects.create(
                    daily_path=daily_path,
                    timestamp=datetime.strptime(date['time'], '%Y-%m-%d %H:%M:%S'),
                    latitude=date['coordinates']['latitude'],
                    longitude=date['coordinates']['longitude']
                )

            gps_logs = make_gps_logs(date_sequence[i])
            points = generatePoints(gps_logs)
            stay_point_centers, stay_points = stayPointExtraction(points)
            if created:
                make_interval(app_user, daily_path, stay_point_centers)
            else:
                point = stay_point_centers[0]
                interval_stay_obj = IntervalStay.objects.filter(daily_path=daily_path).order_by('start_time').last()
                interval_move_obj = IntervalMove.objects.filter(daily_path=daily_path).order_by('start_time').last()

                if interval_move_obj.start_time > interval_stay_obj.start_time:
                    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point.arriveTime))
                    interval_move_obj.end_time = start_time
                    interval_move_obj.percent = make_percent(
                        interval_move_obj.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                        interval_move_obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
                    )
                    interval_move_obj.save()
                    make_interval(app_user, daily_path, stay_point_centers)

                else:
                    d = get_distance(
                        interval_stay_obj.latitude,
                        interval_stay_obj.longitude,
                        point.latitude,
                        point.longitude
                    )
                    if d < 200:
                        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point.leaveTime))
                        interval_stay_obj.end_time = end_time
                        interval_stay_obj.save()
                        if len(stay_point_centers) >= 2:
                            start_time = interval_stay_obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
                            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stay_point_centers[1].arriveTime))
                            percent = make_percent(start_time, end_time)
                            IntervalMove.objects.create(
                                daily_path=daily_path,
                                start_time=start_time,
                                end_time=end_time,
                                transport="?",
                                percent=percent
                            )
                            make_interval(app_user, daily_path, stay_point_centers[1:])
                    else:
                        start_time = interval_stay_obj.end_time.strftime('%Y-%m-%d %H:%M:%S')
                        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(point.arriveTime))
                        percent = make_percent(start_time, end_time)
                        IntervalMove.objects.create(
                            daily_path=daily_path,
                            start_time=start_time,
                            end_time=end_time,
                            transport="?",
                            percent=percent
                        )
                        make_interval(app_user, daily_path, stay_point_centers)

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
