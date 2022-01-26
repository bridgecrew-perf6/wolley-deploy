from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

import dailypathapp.dummy.dummyCommunication as dum
import dailypathapp.stayPointDetectionDensity as sp
from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import IntervalStay, IntervalMove
from myapi.utils import make_response_content, check_interval_objs, check_daily_path_objs


def generate_points_from_DB(uuid):
    today = datetime.date.today()
    dailypath_obj = DailyPath.objects.filter(user__user__username=uuid, date__year=today.year, date__month=today.month,
                                             date__day=today.day)
    if len(dailypath_obj) == 0:
        return []

    time_seq = []
    dailypath_obj = dailypath_obj[0]
    for gpslog in dailypath_obj.gpslogs.all():
        latitude = gpslog.latitude
        longitude = gpslog.longitude
        dateTime = str(gpslog.timestamp)
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)

    return points


def generate_points_from_reqeust_old_ver(request_dict):
    time_seq = []
    for data in request_dict["time_sequence"]:
        latitude = data["coordinate"][0]
        longitude = data["coordinate"][1]
        dateTime = data["time"]
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)
    return points


def generate_points_from_request_new_ver(request_dict):
    time_seq = []
    for data in request_dict["timeSequence"]: # 추후 request.data로 고치면 됨
        latitude = data["coordinate"]["latitude"]
        longitude = data["coordinate"]["longitude"]
        dateTime = data["time"]
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)
    return points


def gpslogs2intervals(date):
    """
    1. 특정 날짜의 gpslogs 객체들을 가져온다.
    2. 이 정보를 interval 객체로 환원한다.
    """
    # make intervals and save intervals
    pass
    # return intervals


def save_intervals(uuid, piechart_id, intervals):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class PathDailyRequestView(APIView):
    permission_classes = [AllowAny]

    # def post(self, request):
    #     """
    #     FE와 dummy data 통신
    #     """
    #     dum.save_raw_in_test_table(request)
    #     content = dum.make_dummy_piechart_info_ver2()
    #     return Response(content, status=status.HTTP_200_OK)

    # dummy gps data로 통신
    # def post(self, request):
    #     request = dum.make_dummy_timestamps()
    #     points = generate_points_from_DB(request["uuid"])
    #     points += generate_points_from_request(request)
    #     stayPointCenter, stayPoint = sp.stayPointExtraction(points, distThres=200, timeThres=30 * 60)
    #
    #     import time
    #     content = dict()
    #     asc = 65
    #     time_format = '%Y-%m-%d %H:%M:%S'
    #     for obj in stayPointCenter:
    #         name = f"{chr(asc)}장소"
    #         content[name] = f"{time.strftime(time_format, time.localtime(obj.arriveTime))} ~ {time.strftime(time_format, time.localtime(obj.leaveTime))}"
    #         asc += 1
    #
    #     return Response(content, status=status.HTTP_200_OK)

    # for real 통신
    def post(self, request):
        points = generate_points_from_DB(request.data["uuid"])
        points += generate_points_from_request_new_ver(request.data)
        stayPointCenter, stayPoint = sp.stayPointExtraction(points, distThres=200, timeThres=30 * 60)

        import time
        content = dict()
        asc = 65
        time_format = '%Y-%m-%d %H:%M:%S'
        for obj in stayPointCenter:
            name = f"{chr(asc)}장소"
            content[name] = f"{time.strftime(time_format, time.localtime(obj.arriveTime))} ~ {time.strftime(time_format, time.localtime(obj.leaveTime))}"
            asc += 1
        print(stayPointCenter)
        print(content, "!!!!!!!!!!!!!!!!!!")
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
            info_data = sorted(info_data, key=lambda info: info['start'])
            content['data']['info'] = info_data
        return Response(content, status=status_code)
