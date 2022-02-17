from rest_framework.test import APITestCase
from dailypathapp.models import GPSLog

import os
import datetime

"""
- shell 명령
export TestDate=2020-02-06;
export TestUser=F123;
python manage.py test dailypathapp.tests.test_print_GPSDayLog;
"""


class MyDayLogClass(APITestCase):
    username = ""
    date = ""

    @classmethod
    def setUpTestData(cls):
        cls.username = os.environ["TestUser"]
        cls.date = os.environ["TestDate"]
        print("\n***** YOUR input DATA *****")
        print(f"user: {cls.username}")
        print(f"date: {cls.date}")
        print("***** YOUR input DATA *****\n")
        pass

    def test_print_GPSDayLog(self):
        date = datetime.datetime.strptime(self.date, '%Y-%m-%d')
        gpslogs = GPSLog.objects.filter(
            daily_path__user__user__username__icontains=self.username,
            timestamp__year=date.year,
            timestamp__month=date.month,
            timestamp__day=date.day,
        )

        data_to_print = dict()
        if len(gpslogs) != 0:
            gpslog_obj = gpslogs[0]
            username = gpslog_obj.daily_path.user.user.username
            data_to_print["user"] = username
            print("입력한 user에 해당하는 GPSLog 없음")
            return

        data_to_print["timeSequence"] = list()
        for gpslog in gpslogs:
            timestamp = dict()
            timestamp["time"] = gpslog.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            timestamp["coordinates"] = dict()
            timestamp["coordinates"]["latitude"] = gpslog.latitude
            timestamp["coordinates"]["longitude"] = gpslog.longitude
            data_to_print["timeSequence"].append(timestamp)

        print("***** GPS Day Log *****")
        print(data_to_print)
        print("***** GPS Day Log *****")
