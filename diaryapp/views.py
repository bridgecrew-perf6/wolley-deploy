import json

import requests
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


def make_dummy_diary_info():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["diaryInfo"] = dict()
    content["data"]["diaryInfo"]["id"] = 1
    content["data"]["diaryInfo"]["date"] = "2022-01-04 18:50:10"
    content["data"]["diaryInfo"]["content"] = "10시에 출근하고 12시에 퇴근하는 직장에 다니는 평범한 직장인이었다. " \
                                              "회사에서는 업무가 많아 야근을 밥먹듯이 하는 사람이었고 집에 와서는 TV와 스마트폰을 끼고 살았다. " \
                                              "주말이 되면 잠만 자는 사람이었다. 그런데 어느 날부터인가 갑자기 허리가 아프기 시작했다. " \
                                              "허리를 굽히거나 펼 때, 앉았다가 일어날 때, 심지어 기침을 할 때에도 허리가 아팠다. " \
                                              "처음에는 그냥 좀 아픈 정도였는데 시간이 갈수록 통증이 심해졌다."
    return content


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        content = make_dummy_diary_info()
        return Response(content, status=status.HTTP_200_OK)


# API Test Code
def make_dummy_diary_info_api():
    r = requests.get(
        'http://brain-cluster-gpu9.dakao.io:27151/diary/?uuid=1&pieChartId=1&diaryId=1',
    )

    response = json.loads(r.content)
    return response


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        content = make_dummy_diary_info_api()
        print(content)
        return Response(content, status=status.HTTP_200_OK)
