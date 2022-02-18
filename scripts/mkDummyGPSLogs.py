from myapi.settings.__init__ import *
import datetime

from django.contrib.auth.models import User
from accountapp.models import AppUser
from dailypathapp.models import DailyPath

from dailypathapp.models import GPSLog
import django

os.environ.setdefault("DJANGO_SETTING_MODULE", "myapi.settings")
django.setup()


def mk_timestamp(coarse_list, app_user):
    latitude = float(coarse_list[-4][1:-1])
    longitude = float(coarse_list[-3][:-1])

    date_str = coarse_list[-2]
    time_str = coarse_list[-1]
    datetime_obj = datetime.datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M:%S')
    date_obj = datetime_obj.date()
    if len(DailyPath.objects.filter(user=app_user, date=date_obj)) == 0:
        DailyPath.objects.create(user=app_user, date=date_obj)
    daily_path = DailyPath.objects.get(user=app_user, date=date_obj)

    return latitude, longitude, datetime_obj, daily_path


# python manage.py runscript -v2 mkDummyGPSLogs --script-args 265EDE33-9FAE-45DE-B51D-879B487BA198
def run(uuid):
    # mk user
    if len(User.objects.filter(username=uuid)) == 0:
        auth_user = User.objects.create_user(username=uuid, password="1234")
        AppUser.objects.create(user=auth_user)
    auth_user = User.objects.get(username=uuid)
    app_user = AppUser.objects.get(user=auth_user)

    # mk GPSLog by .txt file
    fp = open("scripts/dummyData.txt", "r")
    lines = fp.readlines()
    to_sort = []
    for line in lines:
        coarse_list = line.rstrip().split()
        lat, long, datetime_obj, daily_path = mk_timestamp(coarse_list, app_user)
        to_sort.append([lat, long, datetime_obj, daily_path])

    to_sort.sort(key=lambda x: x[2])  # 시간순으로 정렬
    for obj in to_sort:
        GPSLog.objects.create(latitude=obj[0], longitude=obj[1], timestamp=obj[2], daily_path=obj[3])
    fp.close()
