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
    print(gpslogs)