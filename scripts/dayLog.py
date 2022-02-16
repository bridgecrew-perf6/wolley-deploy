from myapi.settings.__init__ import *
import datetime
from dailypathapp.models import GPSLog
import django

os.environ.setdefault("DJANGO_SETTING_MODULE", "myapi.settings")
django.setup()


# python manage.py runscript -v2 gpsPrinter --script-args F1 2022-02-16
def run(username, date):
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    gpslogs = GPSLog.objects.filter(
        daily_path__user__user__username__icontains=username,
        timestamp__year=date.year,
        timestamp__month=date.month,
        timestamp__day=date.day,
    )

    data_to_print = dict()
    if len(gpslogs) != 0:
        gpslog_obj = gpslogs[0]
        username = gpslog_obj.daily_path.user.user.username
        data_to_print["user"] = username

    data_to_print["timeSequence"] = list()
    for gpslog in gpslogs:
        timestamp = dict()
        timestamp["time"] = gpslog.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        timestamp["coordinates"] = dict()
        timestamp["coordinates"]["latitude"] = gpslog.latitude
        timestamp["coordinates"]["longitude"] = gpslog.longitude
        data_to_print["timeSequence"].append(timestamp)
    print(data_to_print)
