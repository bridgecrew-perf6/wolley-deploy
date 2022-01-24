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

from diaryapp.models import Diary
from intervalapp.models import Interval
from myapi.utils import make_response_content, check_daily_path_obj


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_date = request.headers['date']
        # 날짜가 오늘이면 400 전달
        if request_date == date.strftime(date.today(), "%Y-%m-%d"):
            content = make_response_content("일기 생성 전", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        content, status_code, daily_path_obj = check_daily_path_obj(request)
        if status_code == status.HTTP_200_OK:
            diary_obj, created = Diary.objects.get_or_create(daily_path=daily_path_obj.id)
            if created:
                intervals = Interval.objects.filter(daily_path=daily_path_obj.id).order_by('start_time')

                request_data = json.dumps({"data": list(intervals.values())}, cls=DjangoJSONEncoder)
                # res = requests.post("http://34.97.149.180/diary/", data=request_data)
                res = requests.post("http://127.0.0.1:8080/diary/", data=request_data)
                generated_diary_content = res.json()['content']

                diary_obj.content = generated_diary_content
                diary_obj.save()

            content['data'] = {
                "id": diary_obj.id,
                "date": request_date,
                "content": diary_obj.content
            }
        return Response(content, status=status_code)

    def post(self, request):
        request_diary_id = request.data['id']
        update_content = request.data['content']

        try:
            diary_obj = Diary.objects.get(id=request_diary_id)
        except Diary.DoesNotExist:
            content = make_response_content("diary 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        diary_obj.content = update_content
        diary_obj.save()

        content = make_response_content("성공", {})
        return Response(content, status=status.HTTP_200_OK)

