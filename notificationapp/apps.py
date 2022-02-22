from django.apps import AppConfig
import firebase_admin
from firebase_admin import credentials
import os
from myapi.settings.base import BASE_DIR


def init_app():
    # firebase 관련
    cred_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)


class NotificationappConfig(AppConfig):
    name = 'notificationapp'

    def ready(self):
        from . import pathDailyNoti, saveLocationNoti
        init_app()

        from testapp.models import TestTable
        import datetime
        print(f"{datetime.datetime.now()}: ready가 정상 작동")
        TestTable.objects.create(textfield=f"{datetime.datetime.now()}, ready 가 정상 작동 in apps")
        # pathDailyNoti.start_path_daily_noti()
        saveLocationNoti.start_saveLocation()
