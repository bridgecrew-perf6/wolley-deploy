import json
from datetime import date

import requests
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from diaryapp.models import Diary
from intervalapp.models import IntervalStay
from myapi.utils import make_response_content, check_daily_path_obj


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        content, status_code, daily_path_obj = check_daily_path_obj(request)

        try:
            diary_obj = Diary.objects.get(daily_path=daily_path_obj)
        except Diary.DoesNotExist:
            if date.today().strftime("%Y-%m-%d") > request_date:
                diary_obj = Diary.objects.create(daily_path=daily_path_obj)

                intervals = IntervalStay.objects.filter(daily_path=daily_path_obj).order_by('start_time')
                diary_obj.content = [
                    f'{interval.start_time} - {interval.end_time} {interval.category} {interval.location}'
                    for interval in intervals
                ]
                diary_obj.save()
            else:
                content = make_response_content("일기 data 없음", {})
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content['data'] = {
            "id": diary_obj.id,
            "date": request_date,
            "content": diary_obj.content
        }

        return Response(content, status=status_code)

    def post(self, request):
        request_user = request.data['user']
        request_date = request.data['date']
        request_content = request.data['content']

        # daily path 찾기
        try:
            user = AppUser.objects.get(user__username=request_user)
            daily_path_obj = DailyPath.objects.get(user=user, date=request_date)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except DailyPath.DoesNotExist:
            content = make_response_content("daily path 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        diary_obj, created = Diary.objects.get_or_create(daily_path=daily_path_obj)

        diary_obj.content = request_content
        diary_obj.save()

        data = {
            "id": diary_obj.id,
            "date": request_date,
            "content": diary_obj.content
        }

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)

