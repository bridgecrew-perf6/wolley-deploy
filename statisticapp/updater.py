from datetime import datetime, timedelta
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import IntervalStay, IntervalMove
from statisticapp.models import WeekInfo, WeekCategoryInfo
from testapp.models import TestTable

CATEGORY_SORT = ["집", "회사", "학교", "식사", "카페", "쇼핑", "병원", "운동", "모임", "이동", "기타", "?"]


def update_something():
    week_info = make_week_info()
    TestTable.objects.create(
        textfield=week_info
    )
    # print(f"this function runs every 10 seconds {datetime.datetime.today()}")


def get_category_idx(category: str) -> int:
    return CATEGORY_SORT.index(category)


def make_stat_data() -> List:
    stat_data = [
        {
            "category": category,
            "time_spent": timedelta(0)
        } for category in CATEGORY_SORT
    ]
    return stat_data


def make_week_info():
    today = datetime.today()
    year, week_order, _ = today.isocalendar()
    month_order = today.month

    start_date = datetime.fromisocalendar(year, week_order, 1)
    end_date = datetime.fromisocalendar(year, week_order, 7)

    return f'{year}-{month_order}-{week_order} Testing {start_date}~{end_date}'

    # user_objs = AppUser.objects.all()
    # for user_obj in user_objs:
    #     daily_path_objs = DailyPath.objects.filter(user=user_obj, date__range=[start_date, end_date])
    #     # if len(daily_path_objs) != 7:
    #     #     pass
    #
    #     week_info = WeekInfo.objects.create(
    #         user=user_obj,
    #         year=year,
    #         month_order=month_order,
    #         week_order=week_order
    #     )
    #
    #     stat_data = make_stat_data()
    #     total = timedelta(0)
    #     for daily_path_obj in daily_path_objs:
    #         interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj.id)
    #         interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_obj.id)
    #
    #         for interval_stay_obj in interval_stay_objs:
    #             idx = get_category_idx(interval_stay_obj.category)
    #             stat_data[idx]['time_spent'] += interval_stay_obj.end_time - interval_stay_obj.start_time
    #             total += interval_stay_obj.end_time - interval_stay_obj.start_time
    #
    #         for interval_move_obj in interval_move_objs:
    #             idx = get_category_idx('이동')
    #             stat_data[idx]['time_spent'] += interval_move_obj.end_time - interval_move_obj.start_time
    #             total += interval_move_obj.end_time - interval_move_obj.start_time
    #
    #     for stat in stat_data:
    #         if total != timedelta(0):
    #             stat["percent"] = stat["time_spent"] / total
    #         else:
    #             stat["percent"] = 0.0
    #
    #         total_seconds = int(stat["time_spent"].total_seconds())
    #         hours, remainder = divmod(total_seconds, 3600)
    #         minutes, seconds = divmod(remainder, 60)
    #         stat['time_spent'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    #         WeekCategoryInfo.objects.create(
    #             week_info=week_info,
    #             name=stat['category'],
    #             time_spent=stat['time_spent'],
    #             percent=stat['percent']
    #         )


def start():
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.add_job(update_something, 'cron', day_of_week=3, hour=9)
    scheduler.start()
