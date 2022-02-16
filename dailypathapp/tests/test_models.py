from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

import os

"""
shell 명령
export TestDate=2020-02-06; export TestUser=F123; python manage.py test dailypathapp
"""
class MyTestClass(APITestCase):
    @classmethod
    def setUpTestData(cls):
        date = os.environ["TestDate"]
        user = os.environ["TestUser"]
        print(date, user)
        pass

    def setUp(self) -> None:
        print("setUp : !!!!!!!!!!!!")

    def test_그냥한번(self):
        print("test 그냥한번")
