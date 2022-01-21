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


def make_response_content(response_msg: str, data: Dict = {}) -> Dict:
    content = dict()
    content['responseMsg'] = response_msg
    content['data'] = data

    return content


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = date.today() - timedelta(1)

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            daily_path = DailyPath.objects.get(user=user, date=request_date)
        except DailyPath.DoesNotExist:
            content = make_response_content("daily path 없음")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        print(daily_path.id)
        try:
            diary = Diary.objects.get(daily_path=daily_path.id)
            print(diary)
            data = {
                "id": diary.id,
                "date": request_date,
                "content": diary.content
            }
            content = make_response_content("성공", data)
            return Response(content, status=status.HTTP_200_OK)
        except Diary.DoesNotExist:
            intervals = Interval.objects.filter(daily_path=daily_path.id).order_by('start_time')
            print(intervals)
            request_data = json.dumps({"data": list(intervals.values())}, cls=DjangoJSONEncoder)
            print(request_data)
            # 일기 생성 요청
            # res = requests.post("http://34.97.149.180/diary/", data=request_data)
            res = requests.post("http://127.0.0.1:8080/diary/", data=request_data)
            # 일기 객체 생성
            print(res)
            diary_content = res.json()['content']
            new_diary = Diary(daily_path=daily_path, content=diary_content)
            new_diary.save()

            # 일기 객체 전달
            data = {
                "id": new_diary.id,
                "date": request_date,
                "content": new_diary.content
            }
            content = make_response_content("일기 생성 성공", data)
            return Response(content, status=status.HTTP_201_CREATED)

        content = make_response_content("잘못된 접근")
        return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        diary_id = int(request.data['id'])
        update_content = request.data['content']
        try:
            diary_obj = Diary.objects.get(id=diary_id)
        except Diary.DoesNotExist:
            content = make_response_content("diary 없음")
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        diary_obj.content = update_content
        diary_obj.save()

        content = make_response_content("성공")
        return Response(content, status=status.HTTP_200_OK)