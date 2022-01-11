from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime


def make_dummy_piechart_info():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["id"] = 132

    # make interval1 info
    interval1 = dict()
    interval1["id"] = 2
    interval1["startTime"] = "2022-01-04 10:45:10"
    interval1["endTime"] = "2022-01-04 17:45:10"
    interval1["labels"] = ["회사"]
    # make interval2 info
    interval2 = dict()
    interval2["id"] = 3
    interval2["startTime"] = "2022-01-04 17:45:10"
    interval2["endTime"] = "2022-01-04 22:45:10"
    interval2["labels"] = ["?"]

    content["data"]["info"] = list()
    content["data"]["info"].append(interval1)
    content["data"]["info"].append(interval2)

    return content


def parse_time_sequence(time_sequence):
    datetimes = list()
    coordinates = list()
    for data in time_sequence:
        # time info
        datetime_str = data["time"]
        datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        datetimes.append(datetime_obj)

        # 좌표 info
        y, x = map(float, data["coordinate"])
        coordinates.append((y, x))
    return datetimes, coordinates


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
        content = make_dummy_piechart_info()
        return Response(content, status=status.HTTP_200_OK)

    # def post(self, request):
    #     # data parsing
    #     content = request.data
    #     uuid = content["uuid"]
    #     piechart_id = content["piechart_id"]
    #     time_sequence = content["time_sequence"]
    #     datetimes, coordinates = parse_time_sequence(time_sequence)
    #
    #     # make intervals
    #     intervals = make_intervals(datetimes, coordinates)
    #     save_intervals(uuid, piechart_id, intervals)
    #
    #     return Response("ok", status=status.HTTP_200_OK)
