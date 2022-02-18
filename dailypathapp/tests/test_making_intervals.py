from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from intervalapp.models import IntervalStay, IntervalMove

import json
import random

"""
3 시나리오

1. GPSLog 데이터를 뭉텅이로 넘기는 경우
2. GPSLog 데이터를 매번 POST 통신으로 넘기는 경우
3. 1과 2가 뒤섞인 경우
"""


def parse(coarse_list):
    latitude = float(coarse_list[-4][1:-1])
    longitude = float(coarse_list[-3][:-1])

    date_str = coarse_list[-2]
    time_str = coarse_list[-1]
    timestamp = f"{date_str} {time_str}"

    return latitude, longitude, timestamp


def mk_timeSequence_from_txt_file(fp):
    timeSequence = list()
    for line in fp.readlines():
        line_splited = line.rstrip().split()
        lat, long, timestamp = parse(line_splited)
        data = {"time": timestamp, "coordinates": {"latitude": lat, "longitude": long}}
        timeSequence.append(data)
    return timeSequence


"""
python manage.py test dailypathapp.tests.test_making_intervals;
"""


class TestClass(APITestCase):
    timeSequence = list()

    @classmethod
    def setUpTestData(cls):
        fp = open("./dailypathapp/tests/dummydata", 'r')
        cls.timeSequence = mk_timeSequence_from_txt_file(fp)
        cls.timeSequence.sort(key=lambda x: x["time"])
        # print(cls.timeSequence)
        fp.close()

    def test_모든_GPS로그가_POST_통신_한방에_뭉텅이로_오는_시나리오(self):
        data_to_send = {"user": "TESTBOY", "timeSequence": self.timeSequence}
        url = reverse(viewname="dailypathapp:pathdaily_request")
        json_data = json.dumps(data_to_send)
        response = self.client.post(
            path=url,
            data=json_data,
            content_type="application/json"
        )

        print("\n********** (뭉텅이) RESULT ************")
        print(f"IntervalStay: {len(IntervalStay.objects.all())} 개")
        print(f"IntervalMove: {len(IntervalMove.objects.all())} 개")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("******************************")

    def test_모든_GPS로그_각각이_POST_통신으로_쪼개져서_오는_시나리오(self):
        for timestamp in self.timeSequence:
            data_to_send = {"user": "TESTBOY", "timeSequence": [timestamp]}
            url = reverse(viewname="dailypathapp:pathdaily_request")
            json_data = json.dumps(data_to_send)
            response = self.client.post(
                path=url,
                data=json_data,
                content_type="application/json"
            )

        print("\n********** (모든로그가POST) RESULT ************")
        print(f"IntervalStay: {len(IntervalStay.objects.all())} 개")
        print(f"IntervalMove: {len(IntervalMove.objects.all())} 개")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("******************************")

    def test_GPS로그가_드문드문_POST통신으로_넘어오는_시나리오(self):
        chk = [False for _ in range(len(self.timeSequence))]
        for _ in range(10):
            chk[random.randint(1, len(self.timeSequence) - 1)] = True

        l = 0
        for r, timestamp in enumerate(self.timeSequence):
            if chk[r]:
                data_to_send = {"user": "TESTBOY", "timeSequence": self.timeSequence[l:r]}
                url = reverse(viewname="dailypathapp:pathdaily_request")
                json_data = json.dumps(data_to_send)
                response = self.client.post(
                    path=url,
                    data=json_data,
                    content_type="application/json"
                )
                l = r

        print("\n********** (이따금씩POST) RESULT ************")
        print(IntervalStay.objects.all())
        print(f"IntervalStay: {len(IntervalStay.objects.all())} 개")
        print(f"IntervalMove: {len(IntervalMove.objects.all())} 개")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("******************************")
