from myapi.settings.__init__ import *
import datetime
from dailypathapp.models import GPSLog
import django

# os.environ.setdefault("DJANGO_SETTING_MODULE", "myapi.settings")
# django.setup()


# python manage.py runscript -v2 daysLog --script-args F1 2022-02-16 2022-02-18
def run(username, start_date, end_date):
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

    gpslogs = GPSLog.objects.filter(daily_path__user__user__username__icontains=username,
                                    timestamp__gte=start_date,
                                    timestamp__lte=end_date,
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
