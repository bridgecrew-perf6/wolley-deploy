from datetime import datetime, timedelta, date
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

from accountapp.models import AppUser
from dailypathapp.models import DailyPath
from intervalapp.models import IntervalStay, IntervalMove
from statisticapp.models import WeekInfo, WeekCategoryInfo, Badge
from testapp.models import TestTable

BADGE_POINT = 0.1
CATEGORY_SORT = ["집", "회사", "학교", "식사", "카페", "쇼핑", "병원", "운동", "모임", "이동", "기타", "?"]


def weekly_batch():
    # 배치 시작과 동시에 날짜 기준 정리
    batch_day = date.today() - timedelta(days=1)
    year, week_order, _ = batch_day.isocalendar()
    month_order = batch_day.month

    test_text_1 = make_week_info(year, month_order, week_order, batch_day)
    test_text_2 = make_category_rank(year, month_order, week_order)
    week_info = WeekInfo.objects.all()
    week_category_info = WeekCategoryInfo.objects.all()
    TestTable.objects.create(
        textfield=f'{test_text_1}\n{test_text_2}\n{week_info}:{len(week_info)}, {week_category_info}:{len(week_category_info)}'
    )


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


def make_time_spent(time_spent):
    total_seconds = int(time_spent.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def make_week_info(year, month_order, week_order, batch_day):
    start_date = datetime.fromisocalendar(year, week_order, 1)
    end_date = datetime.fromisocalendar(year, week_order, 7)

    user_objs = AppUser.objects.all()
    for user_obj in user_objs:
        # week info 생성
        week_info = WeekInfo.objects.create(
            user=user_obj,
            year=year,
            month_order=month_order,
            week_order=week_order
        )

        daily_path_objs = DailyPath.objects.filter(user=user_obj, date__range=[start_date, end_date])

        stat_data = make_stat_data()
        total = timedelta(0)
        for daily_path_obj in daily_path_objs:
            interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj.id)
            interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_obj.id)

            for interval_stay_obj in interval_stay_objs:
                idx = get_category_idx(interval_stay_obj.category)
                stat_data[idx]['time_spent'] += interval_stay_obj.end_time - interval_stay_obj.start_time
                total += interval_stay_obj.end_time - interval_stay_obj.start_time

            for interval_move_obj in interval_move_objs:
                idx = get_category_idx('이동')
                stat_data[idx]['time_spent'] += interval_move_obj.end_time - interval_move_obj.start_time
                total += interval_move_obj.end_time - interval_move_obj.start_time

        for stat in stat_data:
            if total != timedelta(0):
                stat["percent"] = stat["time_spent"] / total
            else:
                stat["percent"] = 0.0

            WeekCategoryInfo.objects.create(
                week_info=week_info,
                name=stat['category'],
                time_spent=stat['time_spent'],
                percent=stat['percent'],
                date=batch_day
            )

    return f'{year}-{month_order}-{week_order} Testing {start_date}~{end_date}'


def make_category_rank(year, month_order, week_order):
    return_text = ''
    for category in CATEGORY_SORT:
        week_category_info_objs = WeekCategoryInfo.objects.filter(
            name=category,
            week_info__year=year,
            week_info__month_order=month_order,
            week_info__week_order=week_order
        ).order_by('-time_spent', '-percent')
        total_num = len(week_category_info_objs)
        for row_num, week_category_info_obj in enumerate(week_category_info_objs):
            week_category_info_obj.rank = (row_num+1)/total_num
            week_category_info_obj.save()
            if week_category_info_obj.rank <= BADGE_POINT:
                try:
                    badge_obj = Badge.objects.get(sector=week_category_info_obj.name)
                    badge_obj.week_info.add(week_category_info_obj.week_info)
                except Badge.DoesNotExist:
                    pass

                return_text += f'{badge_obj.id}: {badge_obj.week_info.all()}'
    return return_text


def start():
    pass
    # scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    # scheduler.add_job(weekly_batch, 'cron', day_of_week='wed', hour=10, minute=00)
    # scheduler.add_job(weekly_batch, 'interval', minutes=1)
    # scheduler.start()
