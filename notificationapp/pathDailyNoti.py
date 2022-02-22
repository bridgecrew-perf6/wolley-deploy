from notificationapp.FCM import *

# from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler

from accountapp.models import AppUser

"""
thread_id="pathDaily"
목적 : 사용자에게 일주일 동안의 기록 확인을 유도 + path/daily 통신을 하기 위함
방법 : remote push
noti 시각 : 일->월 넘어가는 00:10:00
메세지 내용 : 일주일 동안의 기록을 확인해보세요!
"""


def start_path_daily_noti():
    app_users = AppUser.objects.exclude(fcmToken="abc").exclude(fcmToken="")
    appuser_tokens = [app_user.fcmToken for app_user in app_users]

    scheduler = BackgroundScheduler(timezone="Asia/Seoul", job_defaults={"max_instance": 1})
    scheduler.add_job(func_to_schedule, 'cron', day_of_week='tue', hour=19, minute=30,
                      args=[appuser_tokens, False, "pathDaily", "From Wolley 🗓", "일주일 동안의 기록을 확인해보세요!"])

    scheduler.start()
