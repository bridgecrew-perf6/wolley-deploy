from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from datetime import date
from datetime import datetime
from datetime import timedelta
import time

import dailypathapp.dummy.dummyCommunication as dum
import dailypathapp.stayPointDetectionDensity as sp
from dailypathapp.utils import coordinate2address, get_visited_place

from accountapp.models import AppUser

from dailypathapp.models import DailyPath, GPSLog
from intervalapp.models import IntervalStay, IntervalMove

from myapi.utils import make_response_content, check_interval_objs, check_daily_path_objs

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def generate_points_from_DB(uuid):
    today = date.today()
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
    for data in request_dict["timeSequence"]:  # 추후 request.data로 고치면 됨
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
        # 해당 uuid의 사용자가 있는지 찾고, 없으면, DB에 등록
        uuid = request.data["uuid"]
        if not AppUser.objects.filter(user__username=uuid).exists():
            AppUser.objects.create(user__username=uuid)

        time_sequence = request.data["timeSequence"]
        for time_info_requested in time_sequence:
            # 해당 날짜와 관련된 DailyPath 객체 우선 생성
            time_obj = time.strptime(time_info_requested["time"], TIME_FORMAT)
            datetime_obj = datetime.strptime(time_info_requested["time"], TIME_FORMAT)
            date_obj = date.fromtimestamp(time.mktime(time_obj))
            if not DailyPath.objects.filter(user__user__username=uuid,
                                            date=date_obj).exists():  # 해당 날짜의 dailypath 객체 없다면 -> 만들어 줌
                DailyPath.objects.create(user__user__username=uuid, date=date_obj)

            # DailyPath 객체가 가지고 있는 날짜에 대응하는 GPSLogs 객체 생성
            dailypath_obj = DailyPath.objects.filter(date=date_obj)[0]
            y = time_info_requested["coordinate"]["latitude"]
            x = time_info_requested["coordinate"]["longitude"]
            # 후에 서비스할 때, 아래 조건문은 삭제 가능 - 여러번 실험해보는 환경에서 DB에 중복된 값이 쌓이는 현상을 방지하고자 추가하게 되었음
            if not GPSLog.objects.filter(daily_path__user__user_username=uuid, daily_path=dailypath_obj, latitude=y,
                                         longitude=x, timestamp=datetime_obj).exists():
                GPSLog.objects.create(daily_path__user__user_username=uuid, daily_path=dailypath_obj, latitude=y,
                                      longitude=x, timestamp=datetime_obj)

        if len(time_sequence) != 0:
            oldest_date = date.fromtimestamp(time.mktime(time.strptime(time_sequence[0]["time"], TIME_FORMAT)))
            target_date = oldest_date
            while target_date <= date.today():
                # GPSLogs를 이용해서 stayPointCenter 알아냄
                GPSlog_objs = GPSLog.objects.filter(daily_path__user__user_username=uuid, daily_path__date=target_date)
                time_sequence = []
                for GPSlog_obj in GPSlog_objs:
                    y = GPSlog_obj.latitude
                    x = GPSlog_obj.longitude
                    datetime_str = GPSlog_obj.timestamp.strftime(TIME_FORMAT)
                    time_sequence.append((y, x, datetime_str))

                points = sp.generatePoints(time_sequence)
                stay_point_centers, stay_points = sp.stayPointExtraction(points)

                print(stay_point_centers)

                # 기존의 GPSLogs로 만든 IntervalStays IntervalMove 삭제
                dailypath_obj = DailyPath.objects.filter(user__user__username=uuid, date=target_date)[0]
                intervalstay_objs = dailypath_obj.intervalstays.all()
                for intervalstay_obj in intervalstay_objs:
                    intervalstay_obj.delete()
                intervalmove_objs = dailypath_obj.intervalmoves.all()
                for intervalmove_obj in intervalmove_objs:
                    intervalmove_obj.delete()

                # stayPointCenter 이용해서 IntervalStay 객체 생성
                

                # 먼저 00시 ~ 아침 출발까지 -> 집
                IntervalStay.start_time = datetime.combine(target_date, time())  # 해당 날짜, 00시 00분
                gpslog_obj = GPSLog.objects.filter(daily_path__user__user_username=uuid, daily_path__date=target_date)[0]
                IntervalStay.end_time = gpslog_obj.timestamp
                IntervalStay.address = coordinate2address(point.latitude, point.longitude)

                IntervalStay.category = "집"
                IntervalStay.location = "?"
                IntervalStay.save()

                # 머문장소들
                for point in stay_point_centers:
                    IntervalStay.start_time = datetime.strftime(TIME_FORMAT, datetime.localtime(point.arriveTime))
                    IntervalStay.end_time = datetime.strftime(TIME_FORMAT, datetime.localtime(point.leaveTime))
                    IntervalStay.address = coordinate2address(point.latitude, point.longitude)

                    appuser_obj = AppUser.objects.filter(user__username=uuid)[0]
                    IntervalStay.category = get_visited_place(point.latitude, point.longitude, appuser_obj)
                    IntervalStay.location = "?"
                    IntervalStay.save()

                # stayPointCenter 이용해서 IntervalMove 객체 생성


                # stay_point_centers 이용해서 Interval 객체 생성
                # if stay

                target_date += timedelta(days=1)

        return Response("ok", status=status.HTTP_200_OK)

        # points = generate_points_from_DB(request.data["uuid"])
        # points += generate_points_from_request_new_ver(request.data)
        # stayPointCenter, stayPoint = sp.stayPointExtraction(points, distThres=200, timeThres=30 * 60)
        #
        # import time
        # content = dict()
        # asc = 65
        # time_format = '%Y-%m-%d %H:%M:%S'
        # for obj in stayPointCenter:
        #     name = f"{chr(asc)}장소"
        #     content[name] = f"{time.strftime(time_format, time.localtime(obj.arriveTime))} ~ {time.strftime(time_format, time.localtime(obj.leaveTime))}"
        #     asc += 1
        # print(stayPointCenter)
        # print(content, "!!!!!!!!!!!!!!!!!!")
        # return Response(content, status=status.HTTP_200_OK)


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
