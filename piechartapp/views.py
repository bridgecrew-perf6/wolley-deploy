from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

import dummy_communication as dum


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
        """
        FE와 dummy data 통신
        """
        dum.save_raw_in_test_table(request)
        content = dum.make_dummy_piechart_info()
        return Response(content, status=status.HTTP_200_OK)

    # def post(self, request):
    #     # data parsing
    #     content = request.data
    #
    #     uuid = content["uuid"]
    #     piechart_id = content["piechart_id"]
    #     time_sequence = content["time_sequence"]
    #     datetimes, coordinates = parse_time_sequence(time_sequence)
    #
    #     ## make intervals
    #     intervals = make_intervals(datetimes, coordinates)
    #     save_intervals(uuid, piechart_id, intervals)
    #
    #     return Response("ok", status=status.HTTP_200_OK)
