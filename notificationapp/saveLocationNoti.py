from notificationapp.FCM import *

import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from accountapp.models import AppUser

"""
thread_id="saveLocation"
목적 : 로컬 디바이스에 GPSLog 데이터를 한번 생성하기 위함
방법 : silent push
noti 시각 : 매일 30분에 한 번씩
메세지 내용 : 없음
"""


def get_nearest_half_hour():
    now_minute = datetime.datetime.now().minute
    delta = (30 - now_minute) % 30
    return datetime.datetime.now() + datetime.timedelta(minutes=delta)


def func_to_schedule(appuser_tokens, is_silent, msg_type, msg_title, msg_body):
    send_to_firebase_cloud_group_messaging(appuser_tokens, is_silent, msg_type, msg_title, msg_body)


def start_save_location_noti():
    app_users = AppUser.objects.filter(FCM_token__isnull=False)
    appuser_tokens = [app_user.FCM_token for app_user in app_users]

    scheduler = BlockingScheduler(timezone="Asia/Seoul", job_defaults={"max_instance": 1})
    scheduler.add_job(func_to_schedule, 'interval', minutes=30,
                      args=[appuser_tokens, True, "saveLocation", "saveLocation 통신", "saveLocation 통신"])

    # 가장 가까운 30분 단위의 시간으로 조정 - ex) 현재 시각이 22:42 라면, 23:00으로 조정
    scheduler.get_jobs()[0].modify(next_run_time=get_nearest_half_hour())
    scheduler.start()
