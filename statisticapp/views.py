from datetime import datetime, timedelta

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
from statisticapp.models import WeekInfo, WeekCategoryInfo, Badge


def make_time_spent(total_time):
    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분"


def make_date(obj_date):
    return f'{obj_date.month}월 {obj_date.day}일'


@method_decorator(csrf_exempt, name='dispatch')
class BadgeRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.today()
        _, _, day_order = today.isocalendar()

        target_date = today - timedelta(days=day_order)
        year, week_order, _ = target_date.isocalendar()
        month_order = target_date.month
        try:
            user_week_info_obj = WeekInfo.objects.get(user=user, year=year, month_order=month_order,
                                                      week_order=week_order)
        except WeekInfo.DoesNotExist:
            content = make_response_content("week info 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user_week_category_info_objs = WeekCategoryInfo.objects.filter(week_info=user_week_info_obj).exclude(
            percent=0).order_by('rank')
        sector_sort = [
            user_week_category_info_obj.name for user_week_category_info_obj in user_week_category_info_objs
        ]

        badge_data = {
            "topBadge": {},
            "badges": []
        }

        start_date = datetime.fromisocalendar(year, week_order, 1)
        end_date = datetime.fromisocalendar(year, week_order, 7)
        detail_data = []
        if not sector_sort:
            try:
                badge_obj = user_week_info_obj.badges.get(sector='무')
                badge_data['topBadge'] = {
                    "title": badge_obj.title,
                    "description": badge_obj.description,
                    "sector": badge_obj.sector
                }
            except Badge.DoesNotExist:
                badge_data['topBadge'] = {
                    "title": "균형의 수호자",
                    "description": "균형을 지킨 당신을 위한 특별한 히든 뱃지",
                    "sector": "무"
                }

            daily_path_objs = DailyPath.objects.filter(user=user, date__range=[start_date, end_date])
            for daily_path_obj in daily_path_objs:
                interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj)
                for interval_stay_obj in interval_stay_objs:
                    total_time = interval_stay_obj.end_time - interval_stay_obj.start_time
                    detail_data.append({
                        "id": interval_stay_obj.id,
                        "date": make_date(daily_path_obj.date),
                        "location": interval_stay_obj.location,
                        "timeSpent": make_time_spent(total_time),
                        "sortKey": total_time
                    })
            badge_data['topBadge']['detail'] = [
                {
                    "id": detail['id'],
                    "date": detail['date'],
                    "location": detail['location'],
                    "timeSpent": detail['timeSpent'],
                } for detail in sorted(detail_data, key=lambda x: -x['sortKey'])[:3]
            ]
        else:
            for idx, sector in enumerate(sector_sort):
                try:
                    badge_obj = user_week_info_obj.badges.get(sector=sector)
                except Badge.DoesNotExist:
                    continue

                if idx == 0:
                    # topBadge
                    badge_data['topBadge'] = {
                        "title": badge_obj.title,
                        "description": badge_obj.description,
                        "sector": badge_obj.sector,
                    }
                    daily_path_objs = DailyPath.objects.filter(user=user, date__range=[start_date, end_date])
                    for daily_path_obj in daily_path_objs:
                        interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj,
                                                                         category=badge_obj.sector)
                        for interval_stay_obj in interval_stay_objs:
                            total_time = interval_stay_obj.end_time - interval_stay_obj.start_time
                            detail_data.append({
                                "id": interval_stay_obj.id,
                                "date": make_date(daily_path_obj.date),
                                "location": interval_stay_obj.location,
                                "timeSpent": make_time_spent(total_time),
                                "sortKey": total_time
                            })
                    badge_data['topBadge']['detail'] = [
                        {
                            "id": detail['id'],
                            "date": detail['date'],
                            "location": detail['location'],
                            "timeSpent": detail['timeSpent'],
                        } for detail in sorted(detail_data, key=lambda x: -x['sortKey'])[:3]
                    ]
                else:
                    badge_data['badges'].append({
                        "title": badge_obj.title,
                        "description": badge_obj.description,
                        "sector": badge_obj.sector
                    })

        content = make_response_content("성공", badge_data)
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class DummyBadgeRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        dummy_data = {
            "topBadge": {
                "title": "이 주의 농노!",
                "description": "혹시 판교에서 커피와 사탕수수를 재배하시나요?! 플랜테이션에 이바지하는 당신!",
                "sector": "회사",
                "detail": [
                    {
                        "id": 1,
                        "date": "02월 16일",
                        "location": "서울대 집무실",
                        "timeSpent": "20시간 7분"
                    },
                    {
                        "id": 2,
                        "date": "02월 15일",
                        "location": "목동 집무실",
                        "timeSpent": "13시간 8분"
                    },
                    {
                        "id": 3,
                        "date": "02월 14일",
                        "location": "왕십리 집무실",
                        "timeSpent": "9시간 2분"
                    }
                ]
            },
            "badges": []
        }
        badge_objs = Badge.objects.all()
        dummy_data["badges"] = [
            {
                "title": badge_obj.title,
                "description": badge_obj.description,
                "sector": badge_obj.sector
            } for badge_obj in badge_objs
        ]

        content = make_response_content("성공", dummy_data)
        return Response(content, status=status.HTTP_200_OK)
