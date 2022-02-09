from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import pushFCMNotification


def schedule_func():
    num = 1
    print(num)
    num += 1

    print(datetime.today())
    tokens = [pushFCMNotification.token_ella, pushFCMNotification.token_alpha]
    for tok in tokens:
        pushFCMNotification.send_to_firebase_cloud_messaging(tok)


if __name__ == "__main__":
    pushFCMNotification.init_app()

    scheduler = BlockingScheduler(timezone='Asia/Seoul', job_defaults={'max_instances': 1})
    scheduler.add_job(schedule_func, 'interval', minutes=1)

    # starting now
    for j in scheduler.get_jobs():
        j.modify(next_run_time=datetime.now())

    scheduler.start()
