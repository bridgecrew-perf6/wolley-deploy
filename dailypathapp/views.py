from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

import dailypathapp.dummy_communication as dum
import dailypathapp.stayPointDetectection as sp
from dailypathapp.models import DailyPath


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
class PiechartRequestView(APIView):
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
