import datetime


def crontab_job():
    print(datetime.datetime.today())
    return f"{datetime.datetime.today()}"


if __name__ == "__main__":
    crontab_job()
