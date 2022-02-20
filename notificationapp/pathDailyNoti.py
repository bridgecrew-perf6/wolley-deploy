from notificationapp.FCM import *

from apscheduler.schedulers.blocking import BlockingScheduler

from accountapp.models import AppUser

"""
thread_id="pathDaily"
목적 : 사용자에게 일주일 동안의 기록 확인을 유도 + path/daily 통신을 하기 위함
방법 : remote push
noti 시각 : 일->월 넘어가는 00:10:00
메세지 내용 : 일주일 동안의 기록을 확인해보세요!
"""


def func_to_schedule(appuser_tokens, is_silent, msg_type, msg_title, msg_body):
    send_to_firebase_cloud_group_messaging(appuser_tokens, is_silent, msg_type, msg_title, msg_body)


def start_path_daily_noti():
    app_users = AppUser.objects.filter(FCM_token__isnull=False)
    appuser_tokens = [app_user.FCM_token for app_user in app_users]

    scheduler = BlockingScheduler(timezone="Asia/Seoul", job_defaults={"max_instance": 1})
    scheduler.add_job(func_to_schedule, 'cron', day_of_week='mon', hour=0, minute=10,
                      args=[appuser_tokens, False, "pathDaily", "From Wolley 🗓", "일주일 동안의 기록을 확인해보세요!"])

    scheduler.start()
