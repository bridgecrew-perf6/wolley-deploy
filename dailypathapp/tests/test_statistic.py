from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from intervalapp.models import IntervalStay, IntervalMove

import json
import random
from dailypathapp.tests.utils import *


"""
python manage.py test dailypathapp.tests.test_statistic;
"""


class TestClass(APITestCase):
    timeSequence = list()
    data_to_send = dict()
    url = ""


    @classmethod
    def setUpTestData(cls):
        fp = open("./dailypathapp/tests/dummydata", 'r')
        cls.timeSequence = mk_timeSequence_from_txt_file(fp)
        cls.timeSequence.sort(key=lambda x: x["time"])
        # print(cls.timeSequence)
        fp.close()

        data_to_send = {"user": "TESTBOY", "timeSequence": cls.timeSequence, "fcmToken": ""}
        url = reverse(viewname="dailypathapp:pathdaily_request")
        json_data = json.dumps(data_to_send)

    def setUp(self) -> None:
        self.client.post(
            path=self.url,
            data=json.dumps(self.data_to_send),
            fcmToken="",
            content_type="application/json"
        )

    def test_weekly(self):
        url = reverse(viewname="dailypathapp:weekly_request")
        header = {
            "HTTP_user": "TESTBOY",
            "HTTP_date": "2022-02-18"
        }
        response = self.client.get(path=url, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_monthly(self):
        url = reverse(viewname="dailypathapp:monthly_request")
        header = {
            "HTTP_user": "TESTBOY",
            "HTTP_date": "2022-02-28"
        }
        response = self.client.get(path=url, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_yearly(self):
        url = reverse(viewname="dailypathapp:yearly_request")
        header = {
            "HTTP_user": "TESTBOY",
            "HTTP_date": "2022-02-28"
        }
        response = self.client.get(path=url, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
