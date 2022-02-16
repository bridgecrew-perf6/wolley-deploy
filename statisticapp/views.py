from datetime import datetime

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accountapp.models import AppUser
from myapi.utils import make_response_content
from statisticapp.models import WeekInfo, WeekCategoryInfo


@method_decorator(csrf_exempt, name='dispatch')
class StatRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']
        year,month,_ = map(int,request_date.split('-'))
        week = datetime(year, month, 1).isocalendar().week

        user = AppUser.objects.get(user__username=request_user)
        week_info = WeekInfo.objects.get(user=user, year=year, month_order=month, week_order=week)
        week_category_info = WeekCategoryInfo.objects.filter(week_info=week_info, name="이동")

        data = {
            "labels": [
                {
                    "title": "워커홀릭",
                    "desc": "회사에서 보낸 시간이 상위 10%",
                    "part": "work"
                }
            ]
        }
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)
