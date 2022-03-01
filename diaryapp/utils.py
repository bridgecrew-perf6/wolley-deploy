from datetime import datetime


def make_diary_content(start: datetime, end: datetime, category: str) -> str:
    hours, remainder = divmod((end - start).total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    if minutes == 0:
        time_spent = f'{hours}시간'
    else:
        time_spent = f'{hours}시간 {minutes}분'

    if category == "집":
        return f'{start.hour}시 {start.minute}분부터 {time_spent}동안 {category}에 있었다.'
    elif category == "식사":
        return f'{start.hour}시 {start.minute}분에 {category}를 했다.'
    elif category in ["회사", "학교", "카페", "병원", "모임"]:
        return f'{start.hour}시 {start.minute}분에 {category}에 도착하여 {time_spent}동안 있었다.'
    elif category in ["운동", "쇼핑"]:
        return f'{start.hour}시 {start.minute}분에 {category}을 시작하여 {time_spent}동안 {category}을 했다.'
    else:
        return ''


def make_topic(start_time: datetime, category: str, location: str):
    if location == '?':
        return f"{start_time.hour}시 {start_time.minute}분의 {category}에 대해 써보세요"
    else:
        return f"{start_time.hour}시 {start_time.minute}분에 갔던 {location}에 대해 써보세요"
