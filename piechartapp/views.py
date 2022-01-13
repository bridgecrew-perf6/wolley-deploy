from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime

def make_dummy_interval_info(interval_id: int, start_time: str, end_time: str, label: str):
    interval = dict()
    interval["id"] = interval_id
    interval["startTime"] = start_time
    interval["endTime"] = end_time
    interval["labels"] = [label]
    return interval


def make_dummy_piechart_info():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["id"] = 132

    content["data"]["info"] = list()

    content["data"]["info"].append(
        make_dummy_interval_info(1, "2022-01-12 00:00:00", "2022-01-12 09:00:00", "A장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(2, "2022-01-12 09:00:00", "2022-01-12 09:52:00", "이동(차)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(3, "2022-01-12 09:52:00", "2022-01-12 11:58:00", "B장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(4, "2022-01-12 11:58:00", "2022-01-12 12:08:00", "이동(도보)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(5, "2022-01-12 12:08:00", "2022-01-12 12:43:00", "C장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(6, "2022-01-12 12:43:00", "2022-01-12 12:52:00", "이동(도보)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(7, "2022-01-12 12:52:00", "2022-01-12 13:34:00", "B장소")
    )

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
