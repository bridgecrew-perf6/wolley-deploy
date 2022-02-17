from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from dailypathapp.models import GPSLog

import os
import datetime

"""
3 시나리오

1. GPSLog 데이터를 뭉텅이로 넘기는 경우
2. GPSLog 데이터를 매번 POST 통신으로 넘기는 경우
3. 1과 2가 뒤섞인 경우
"""


"""
- shell 명령
export TestStartDate=2020-02-06;
export TestEndDate=2020-02-07; 
export TestUser=F123; 
python manage.py test dailypathapp.tests.test_making_intervals;
"""


class MyIntervalTestClass(APITestCase):
    username = ""
    start_date = ""
    end_date = ""

    @classmethod
    def setUpTestData(cls):
        cls.username = os.environ["TestUser"]
        cls.start_date = os.environ["TestStartDate"]
        cls.end_date = os.environ["TestEndDate"]
        print("\n***** YOUR input DATA *****")
        print(f"user: {cls.username}, start_date: {cls.start_date}, end_date: {cls.end_date}")
        print("***** YOUR input DATA *****\n")
        pass

    def test_POST_chunk_data(self):
        start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

        gpslogs = GPSLog.objects.filter(daily_path__user__user__username__icontains=self.username,
                                        timestamp__gte=start_date,
                                        timestamp__lte=end_date,
                                        )

        url = reverse(viewname="dailypathapp:pathdaily_request")

        data_to_req = dict()
        if len(gpslogs) != 0:
            gpslog_obj = gpslogs[0]
            username = gpslog_obj.daily_path.user.user.username
            data_to_req["user"] = username
            print("입력 user에 해당하는 GPSLog 없음")
            return

        data_to_req["timeSequence"] = list()
        for gpslog in gpslogs:
            timestamp = dict()
            timestamp["time"] = gpslog.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            timestamp["coordinates"] = dict()
            timestamp["coordinates"]["latitude"] = gpslog.latitude
            timestamp["coordinates"]["longitude"] = gpslog.longitude
            data_to_req["timeSequence"].append(timestamp)

        print("***** GPS Days Log *****")
        print(data_to_req)
        print("***** GPS Days Log *****")

        response = self.client.post(path=url, data=data_to_req)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
