
def make_time_spent(total_time):
    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}시간 {minutes}분"


def make_date(obj_date):
    return f'{obj_date.month}월 {obj_date.day}일'