from apscheduler.schedulers.background import BackgroundScheduler
from .views import update_something


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_something, 'interval', minutes=10)
    scheduler.start()