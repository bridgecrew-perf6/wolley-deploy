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
from statisticapp.updater import update_something


@method_decorator(csrf_exempt, name='dispatch')
class StatRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']
        year, month, _ = map(int, request_date.split('-'))
        week = datetime(year, month, 1).isocalendar().week

        # user = AppUser.objects.get(user__username=request_user)
        # user_week_info_obj = WeekInfo.objects.get(user=user, year=year, month_order=month, week_order=week)
        # user_week_category_info_obj = WeekCategoryInfo.objects.filter(week_info=user_week_info_obj, name="이동")
        #
        # week_info_objs = WeekInfo.objects.filter(year=year, month_order=month, week_order=week)
        update_something()


        data = {
            "topBadge": {
                "title": "워커홀릭",
                "description": "회사에서 보낸 시간이 상위 10%",
                "sector": "work",
                "detail": [
                    {
                        "date": "2022-02-16",
                        "location": "집무실",
                        "timeSpent": "00:00:00"
                    },
                    {
                        "date": "2022-02-15",
                        "location": "집무실",
                        "timeSpent": "00:00:00"
                    },
                    {
                        "date": "2022-02-14",
                        "location": "집무실",
                        "timeSpent": "00:00:00"
                    }
                ]
            },
            "badges": [
                {
                    "title": "워커홀릭",
                    "description": "회사에서 보낸 시간이 상위 10%",
                    "sector": "work"
                },
                {
                    "title": "워커홀릭",
                    "description": "회사에서 보낸 시간이 상위 10%",
                    "sector": "work"
                },
                {
                    "title": "워커홀릭",
                    "description": "회사에서 보낸 시간이 상위 10%",
                    "sector": "work"
                }
            ]
        }
        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)
