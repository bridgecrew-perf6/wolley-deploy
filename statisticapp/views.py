from datetime import datetime, timedelta
from typing import Dict

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import IntervalStay
from myapi.utils import make_response_content
from statisticapp.models import WeekInfo, WeekCategoryInfo
from statisticapp.updater import weekly_batch


def make_time_spent(total_time):
    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분"

@method_decorator(csrf_exempt, name='dispatch')
class BadgeRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # update_something()

        request_user = request.headers['user']
        request_date = request.headers['date']
        user = AppUser.objects.get(user__username=request_user)

        year, week_order, _ = datetime.strptime(request_date, '%Y-%m-%d %H:%M:%S').isocalendar()
        month_order = datetime.strptime(request_date, '%Y-%m-%d %H:%M:%S').month

        user_week_info_obj = WeekInfo.objects.get(user=user, year=year, month_order=month_order, week_order=week_order)

        user_week_category_info_objs = WeekCategoryInfo.objects.filter(week_info=user_week_info_obj).exclude(percent=0).order_by('rank')
        sector_sort = [
            user_week_category_info_obj.name for user_week_category_info_obj in user_week_category_info_objs
        ]

        badge_data = {
            "topBadge": {},
            "badges": []
        }
        if not sector_sort:
            badge_data['topBadge'] = {
                "title": "균형의 수호자",
                "description": "작은 육각형 인재",
                "sector": "X"
            }
            detail_data = []
            for user_week_category_info_obj in user_week_category_info_objs:
                detail_data.append({
                    "date": user_week_category_info_obj.date,
                    "location": user_week_category_info_obj.name,
                    "timeSpent": make_time_spent(user_week_category_info_obj.time_spent)
                })
            badge_data['topBadge']['detail'] = sorted(detail_data, key=lambda x: -x['timeSpent'])[:3]
        else:
            for idx, sector in enumerate(sector_sort):
                badge_obj = user_week_info_obj.badges.get(sector=sector)
                if idx == 0:
                    # topBadge
                    badge_data['topBadge'] = {
                        "title": badge_obj.title,
                        "description": badge_obj.description,
                        "sector": badge_obj.sector,
                    }

                    start_date = datetime.fromisocalendar(year, week_order, 1)
                    end_date = datetime.fromisocalendar(year, week_order, 7)

                    detail_data = []
                    daily_path_objs = DailyPath.objects.filter(user=user, date__range=[start_date, end_date])
                    for daily_path_obj in daily_path_objs:
                        interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj, category=badge_obj.sector)
                        for interval_stay_obj in interval_stay_objs:
                            total_time = interval_stay_obj.end_time - interval_stay_obj.start_time
                            detail_data.append({
                                "id": interval_stay_obj.id,
                                "date": daily_path_obj.date,
                                "location": interval_stay_obj.location,
                                "timeSpent": make_time_spent(total_time)
                            })
                    badge_data['topBadge']['detail'] = sorted(detail_data, key=lambda x: -x['timeSpent'])[:3]
                else:
                    badge_data.append({
                        "title": badge_obj.title,
                        "description": badge_obj.description,
                        "sector": badge_obj.sector
                    })

        content = make_response_content("성공", badge_data)
        return Response(content, status=status.HTTP_200_OK)
