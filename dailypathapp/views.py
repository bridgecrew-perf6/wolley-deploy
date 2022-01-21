from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

import dailypathapp.dummy_communication as dum
import dailypathapp.stayPointDetectection as sp
from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import Interval


def generate_points_from_DB(uuid):
    today = datetime.date.today()
    dailypath_obj = DailyPath.objects.filter(user__user__username=uuid, date__year=today.year, date__month=today.month, date__day=today.day)
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


def generate_points_from_request(request_dict):
    time_seq = []
    for data in request_dict["timeSequence"]: # 추후 request.data로 고치면 됨
        latitude = data["coordinate"]["latitude"]
        longitude = data["coordinate"]["longitude"]
        dateTime = data["time"]
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)

    return points


def make_intervals(datetimes, coordinates):
    # make intervals and save intervals
    pass
    # return intervals


def save_intervals(uuid, piechart_id, intervals):
    pass


@method_decorator(csrf_exempt, name='dispatch')
class PathDailyRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        FE와 dummy data 통신
        """
        dum.save_raw_in_test_table(request)
        content = dum.make_dummy_piechart_info_ver2()
        return Response(content, status=status.HTTP_200_OK)

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
    # def post(self, request):
    #     points = generate_points_from_DB(request.data["uuid"])
    #     points += generate_points_from_request(request)
    #     stayPointCenter, stayPoint = sp.stayPointExtraction(points, distThres=200, timeThres=30 * 60)
    #     return Response(stayPointCenter, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class MonthlyRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']
        year, month, _ = request_date.split('-')

        content = dict()

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content['responseMsg'] = "User 없음"
            content['data'] = list()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            daily_path_list = DailyPath.objects.filter(user=user, date__year=year, date__month=month)
        except DailyPath.DoesNotExist :
            content['responseMsg'] = "Monthly 기록 없음"
            content['data'] = list()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content['responseMsg'] = "성공"
        content['data'] = list()

        for daily_path in daily_path_list:
            print(daily_path)
            interval_list = Interval.objects.filter(daily_path_id=daily_path.id).order_by('start_time')
            daily_path_data = dict()
            daily_path_data['id'] = daily_path.id
            daily_path_data['date'] = daily_path.date
            daily_path_data['info'] = list()
            for interval in interval_list:
                interval_data = dict()
                interval_data['id'] = interval.id
                interval_data['category'] = interval.category
                interval_data['percent'] = interval.percent
                daily_path_data['info'].append(interval_data)

            content['data'].append(daily_path_data)

        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PieChartRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']
        content = dict()

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content['responseMsg'] = "User 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            daily_path = DailyPath.objects.get(user=user, date=request_date)
        except DailyPath.DoesNotExist:
            content['responseMsg'] = "daily 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            interval_list = Interval.objects.filter(daily_path=daily_path.id).order_by('start_time')
        except Interval.DoesNotExist:
            content['responseMsg'] = "Interval 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content['responseMsg'] = "성공"
        content['data'] = dict()
        content['data']['id'] = daily_path.id
        content['data']['date'] = daily_path.date
        content['data']['info'] = list()

        for interval in interval_list:
            interval_data = dict()
            interval_data['id'] = interval.id
            interval_data['category'] = interval.category
            interval_data['location'] = interval.location
            interval_data['percent'] = interval.percent
            content['data']['info'].append(interval_data)

        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class MapRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']
        content = dict()

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content['responseMsg'] = "User 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            daily_path = DailyPath.objects.get(user=user, date=request_date)
        except DailyPath.DoesNotExist:
            content['responseMsg'] = "daily 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            interval_list = Interval.objects.filter(daily_path=daily_path.id).order_by('start_time')
        except Interval.DoesNotExist:
            content['responseMsg'] = "Interval 기록 없음"
            content['data'] = dict()
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content['responseMsg'] = "성공"
        content['data'] = dict()
        content['data']['id'] = daily_path.id
        content['data']['date'] = daily_path.date
        content['data']['info'] = list()

        for interval in interval_list:
            interval_data = dict()
            interval_data['id'] = interval.id
            interval_data['address'] = interval.address
            interval_data['coordinate'] = dict()
            interval_data['coordinate']['latitude'] = interval.latitude
            interval_data['coordinate']['longitude'] = interval.longitude
            content['data']['info'].append(interval_data)

        return Response(content, status=status.HTTP_200_OK)