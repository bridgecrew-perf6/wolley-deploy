import json
from datetime import date, timedelta
from typing import Dict

import requests
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from dailypathapp.models import DailyPath
from diaryapp.models import Diary
from intervalapp.models import Interval
from accountapp.models import AppUser


def make_dummy_diary_info():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["id"] = 1
    content["data"]["date"] = "2022-01-04 18:50:10"
    content["data"]["content"] = "10시에 출근하고 12시에 퇴근하는 직장에 다니는 평범한 직장인이었다. " \
                                 "회사에서는 업무가 많아 야근을 밥먹듯이 하는 사람이었고 집에 와서는 TV와 스마트폰을 끼고 살았다. " \
                                 "주말이 되면 잠만 자는 사람이었다. 그런데 어느 날부터인가 갑자기 허리가 아프기 시작했다. " \
                                 "허리를 굽히거나 펼 때, 앉았다가 일어날 때, 심지어 기침을 할 때에도 허리가 아팠다. " \
                                 "처음에는 그냥 좀 아픈 정도였는데 시간이 갈수록 통증이 심해졌다."
    return content


def make_response_content(response_msg: str, data: Dict = None) -> Dict:
    content = dict()
    content['responseMsg'] = response_msg

    if data:
        content['data'] = data

    return content


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        check_date = date.today() - timedelta(1)

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            daily_path = DailyPath.objects.get(user=user, date=check_date)
        except DailyPath.DoesNotExist:
            content = make_response_content("daily path 없음")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            diary = Diary.objects.get(daily_path=daily_path.id)
            data = {
                "id": diary.id,
                "date": check_date,
                "content": diary.content
            }
            content = make_response_content("성공", data)
            return Response(content, status=status.HTTP_200_OK)
        except Diary.DoesNotExist:
            intervals = Interval.objects.filter(daily_path=daily_path.id)
            request_data = json.dumps({"data": list(intervals.values())}, cls=DjangoJSONEncoder)

            # 일기 생성 요청
            res = requests.post("http://34.97.149.180/diary/", data=request_data)

            # 일기 객체 생성
            diary_content = res.json()['content']
            new_diary = Diary(daily_path=daily_path, content=diary_content)
            new_diary.save()

            # 일기 객체 전달
            data = {
                "id": new_diary.id,
                "date": check_date,
                "content": new_diary.content
            }
            content = make_response_content("일기 생성 성공", data)
            return Response(content, status=status.HTTP_201_CREATED)

        content = make_response_content("잘못된 접근")
        return Response(content, status=status.HTTP_404_NOT_FOUND)