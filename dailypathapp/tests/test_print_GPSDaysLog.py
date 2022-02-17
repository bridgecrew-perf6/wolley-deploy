from rest_framework.test import APITestCase
from dailypathapp.models import GPSLog

import os
import datetime

"""
- shell 명령
export TestStartDate=2020-02-06;
export TestEndDate=2020-02-07; 
export TestUser=F123; 
python manage.py test dailypathapp.tests.test_print_GPSDaysLog;
"""


class MyDaysLogClass(APITestCase):
    username = ""
    start_date = ""
    end_date = ""

    @classmethod
    def setUpTestData(cls):
        cls.username = os.environ["TestUser"]
        cls.start_date = os.environ["TestStartDate"]
        cls.end_date = os.environ["TestEndDate"]
        print("\n***** YOUR input DATA *****")
        print(f"user: {cls.username}")
        print(f"start_date: {cls.start_date}, end_date: {cls.end_date}")
        print("***** YOUR input DATA *****\n")
        pass

    def test_print_GPSDaysLog(self):
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

        gpslogs = GPSLog.objects.filter(daily_path__user__user__username__icontains=self.username,
                                        timestamp__gte=start_date,
                                        timestamp__lte=end_date,
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

        print("***** GPS Days Log *****")
        print(data_to_print)
        print("***** GPS Days Log *****")
