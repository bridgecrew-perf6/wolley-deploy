from notificationapp.FCM import *

import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

from accountapp.models import AppUser

"""
thread_id="saveLocation"
목적 : 로컬 디바이스에 GPSLog 데이터를 한번 생성하기 위함
방법 : silent push
noti 시각 : 매일 30분에 한 번씩
메세지 내용 : 없음
"""


def start_saveLocation():
    app_users = AppUser.objects.exclude(fcmToken="abc").exclude(fcmToken="")
    appuser_tokens = [app_user.fcmToken for app_user in app_users]

    scheduler = BackgroundScheduler(timezone="Asia/Seoul", job_defaults={'max_instances': 1})

    scheduler.add_job(func_to_schedule, 'cron', minute='0, 30',
                      args=[appuser_tokens, False, "saveLocation", "saveLocation 통신", "saveLocation 통신"])

    from testapp.models import TestTable
    TestTable.objects.create(textfield=f"{datetime.datetime.now()}, start가 정상 작동")
    print(f"{datetime.datetime.now()}: start가 정상 작동")
    print(appuser_tokens)

    scheduler.start()
