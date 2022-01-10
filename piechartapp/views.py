from django.shortcuts import render
from piechartapp.models import PieChart

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def make_dummy_piechart_info():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["piechartInfo"] = dict()
    content["data"]["piechartInfo"]["id"] = 132

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

    content["data"]["piechartInfo"]["info"] = list()
    content["data"]["piechartInfo"]["info"].append(interval1)
    content["data"]["piechartInfo"]["info"].append(interval2)

    return content


@method_decorator(csrf_exempt, name='dispatch')
class PiechartRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        content = make_dummy_piechart_info()
        return Response(content, status=status.HTTP_200_OK)
