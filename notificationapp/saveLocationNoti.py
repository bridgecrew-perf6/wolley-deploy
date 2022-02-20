from notificationapp.FCM import *

import datetime

# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from accountapp.models import AppUser

"""
thread_id="saveLocation"
목적 : 로컬 디바이스에 GPSLog 데이터를 한번 생성하기 위함
방법 : silent push
noti 시각 : 매일 30분에 한 번씩
메세지 내용 : 없음
"""


def start_save_location_noti():
    app_users = AppUser.objects.filter(fcmToken="abc")
    appuser_tokens = [app_user.fcmToken for app_user in app_users]

    scheduler = BackgroundScheduler(timezone="Asia/Seoul", job_defaults={"max_instance": 1})
    scheduler.add_job(func_to_schedule, 'cron', minute='0, 30',
                      args=[appuser_tokens, False, "saveLocation", "saveLocation 통신", "saveLocation 통신"])

    scheduler.start()
    from testapp.models import TestTable
    TestTable.objects.create(textfield="start_save_location_noti 성공~!!!!!!!")
    print("start_save_location_noti 성공!!!!!!!!!!!!!!!!!!")
