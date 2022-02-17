from datetime import date, datetime, timedelta

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accountapp.models import AppUser, Estimate
from dailypathapp.models import DailyPath
from dailypathapp.utils import get_distance
from diaryapp.models import Diary
from intervalapp.models import IntervalStay
from myapi.utils import make_response_content, check_daily_path_obj


def make_diary_content(start: datetime, end: datetime, category: str) -> str:
    hours, remainder = divmod((end - start).seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if minutes == 0:
        time_spent = f'{hours}시간'
    else:
        time_spent = f'{hours}시간 {minutes}분'

    if category == "집":
        return f'{start.hour}시 {start.minute}분부터 {time_spent}동안 {category}에 있었다.'
    elif category == "식사":
        return f'{start.hour}시 {start.minute}분에 {category}를 했다.'
    elif category in ["회사", "학교", "카페", "병원", "모임"]:
        return f'{start.hour}시 {start.minute}분에 {category}에 도착하여 {time_spent}동안 있었다.'
    elif category in ["운동", "쇼핑"]:
        return f'{start.hour}시 {start.minute}분에 {category}을 시작하여 {time_spent}동안 {category}을 했다.'
    else:
        return ''


@method_decorator(csrf_exempt, name='dispatch')
class DiaryRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        # daily path 찾기
        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        try:
            diary_obj = Diary.objects.get(user=user, date=request_date)
        except Diary.DoesNotExist:
            if date.today().strftime("%Y-%m-%d") > request_date:
                diary_obj = Diary.objects.create(user=user, date=request_date, content='')
            else:
                content = make_response_content("일기 data 없음", {})
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        no_content = "일기를 작성할 기록이 없습니다."
        if diary_obj.content == '' or diary_obj.content == no_content:
            try:
                daily_path_obj = DailyPath.objects.get(user=user, date=request_date)
                interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj).order_by('start_time')
                diary_content = [
                    make_diary_content(interval_stay_obj.start_time, interval_stay_obj.end_time,
                                       interval_stay_obj.category)
                    for interval_stay_obj in interval_stay_objs
                ]
                content = ' '.join(content for content in diary_content if content != '')
                diary_obj.content = content if content else no_content
            except:
                diary_obj.content = no_content

            diary_obj.save()

        data = {
            "id": diary_obj.id,
            "date": request_date,
            "content": diary_obj.content
        }
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        request_user = request.data['user']
        request_date = request.data['date']
        request_content = request.data['content']

        # daily path 찾기
        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        diary_obj, created = Diary.objects.get_or_create(user=user, date=request_date)
        diary_obj.content = request_content
        diary_obj.save()

        data = {
            "id": diary_obj.id,
            "date": request_date,
            "content": diary_obj.content
        }

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)



@method_decorator(csrf_exempt, name='dispatch')
class TopicRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


        base_date = datetime.strptime(request_date, "%Y-%m-%d")
        _, _, day_order = base_date.isocalendar()
        target_date = base_date - timedelta(days=day_order)
        year, week, _ = target_date.isocalendar()

        start_date = datetime.fromisocalendar(year, week, 1)
        end_date = datetime.fromisocalendar(year, week, 7)

        try:
            daily_path_obj = DailyPath.objects.get(user=user, date=base_date)
        except DailyPath.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj)
        estimate_objs = Estimate.objects.filter(user=user)

        data = {
            "topic": "추천 내용이 없습니다."
        }
        for interval_stay_obj in interval_stay_objs:
            for estimate_obj in estimate_objs:
                d = get_distance(
                    interval_stay_obj.latitude,
                    interval_stay_obj.longitude,
                    estimate_obj.latitude,
                    estimate_obj.longitude
                )
                # if d > 200:





        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)
