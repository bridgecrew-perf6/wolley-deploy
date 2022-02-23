import calendar
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Any

from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from dailypathapp.stayPointDetectionDensity import generatePoints, stayPointExtraction, Point
from dailypathapp.utils import coordinate2address, get_visited_place, get_distance

from accountapp.models import AppUser
from dailypathapp.models import DailyPath, GPSLog
from intervalapp.models import IntervalStay, IntervalMove
from myapi.utils import make_response_content, check_interval_objs, check_daily_path_obj

DAY = 7
MONTH = 12
DAY_NAME = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CATEGORY_SORT = ["집", "회사", "학교", "식사", "카페", "쇼핑", "병원", "운동", "모임", "이동", "기타", "?"]
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def make_date_range(start: str, end: str) -> List:
    date_range = []
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")
    delta = end_date - start_date
    for i in range(delta.days + 1):
        now = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        date_range.append(now)
    return date_range


def make_date_data(date: str, longitude: float, latitude: float) -> Dict:
    date_data = {
        "time": date,
        "coordinates": {
            "longitude": longitude,
            "latitude": latitude
        }
    }
    return date_data


def make_date_sequence(time_sequence: List[Dict], user: AppUser) -> Dict:
    if not time_sequence:
        return {}

    start_date = time_sequence[0]['time'][:10]
    end_date = time_sequence[-1]['time'][:10]
    date_range = make_date_range(start_date, end_date)
    date_sequence = {d: [] for d in date_range}

    for time_seq in time_sequence:
        date_sequence[time_seq['time'][:10]].append(time_seq)

    end_flag = len(date_sequence) - 1
    for idx, date_key in enumerate(date_sequence.keys()):
        if not date_sequence[date_key]:
            continue

        try:
            daily_path = DailyPath.objects.get(user=user, date=date_key)
            gps_log = GPSLog.objects.filter(daily_path=daily_path).order_by('timestamp').last()
            start_data = make_date_data(
                gps_log.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                gps_log.longitude,
                gps_log.latitude
            )
            date_sequence[date_key].insert(0, start_data)
        except:
            start_data = make_date_data(
                date_key + " 00:00:00",
                date_sequence[date_key][0]['coordinates']['longitude'],
                date_sequence[date_key][0]['coordinates']['latitude']
            )
            date_sequence[date_key].insert(0, start_data)

        if idx != end_flag:
            end_data = make_date_data(
                date_key + " 23:59:59",
                date_sequence[date_key][-1]['coordinates']['longitude'],
                date_sequence[date_key][-1]['coordinates']['latitude']
            )
            date_sequence[date_key].append(end_data)
    return date_sequence


def make_gps_logs(date_sequence: List[Dict]) -> List[Tuple]:
    gps_logs = [
        (
            date['coordinates']['latitude'],
            date['coordinates']['longitude'],
            date['time']
        ) for date in date_sequence
    ]
    return gps_logs


def make_percent(start: datetime, end: datetime) -> float:
    total_time = end - start
    percent = total_time / timedelta(hours=23, minutes=59, seconds=59)
    return percent


def make_stay_interval(app_user: AppUser, daily_path: DailyPath, stay_point_centers: List) -> None:
    # print("Interval Stay")
    for point in stay_point_centers:
        start_time = datetime.strptime(point.arriveTime, DATETIME_FORMAT)
        end_time = datetime.strptime(point.leaveTime, DATETIME_FORMAT)
        percent = make_percent(start_time, end_time)
        latitude = point.latitude
        longitude = point.longitude
        address = coordinate2address(point.latitude, point.longitude)
        IntervalStay.objects.create(
            daily_path=daily_path,
            start_time=start_time,
            end_time=end_time,
            address=address,
            category=get_visited_place(latitude, longitude, app_user),
            location="?",
            latitude=latitude,
            longitude=longitude,
            percent=percent
        )


def make_move_interval(app_user: AppUser, daily_path: DailyPath, move_points: List[Tuple]) -> None:
    # print("Interval Move")
    for start_time, end_time in move_points:
        start = datetime.strptime(start_time, DATETIME_FORMAT)
        end = datetime.strptime(end_time, DATETIME_FORMAT)
        percent = make_percent(start, end)
        IntervalMove.objects.create(
            daily_path=daily_path,
            start_time=start,
            end_time=end,
            transport="?",
            percent=percent
        )


def check_last_interval(interval_stay_obj: IntervalStay, interval_move_obj: IntervalMove) -> str:
    if not interval_stay_obj and not interval_move_obj:
        return "none"
    elif not interval_stay_obj and interval_move_obj:
        return "move"
    elif interval_stay_obj and not interval_move_obj:
        return "stay"
    else:
        if interval_stay_obj.start_time > interval_move_obj.start_time:
            return "stay"
        else:
            return "move"


# 나중에 함수 분리하기
def make_move_point(points: Point, stay_point_centers: List[Point]) -> Tuple[List[Tuple[Any, Any]], str]:
    move_range = []
    flag = "stay"

    if not stay_point_centers:
        move_range.append((points[0].dateTime, points[-1].dateTime))
        flag = "move"
        return move_range, flag

    if points[0].dateTime != stay_point_centers[0].arriveTime:
        move_range.append((points[0].dateTime, stay_point_centers[0].arriveTime))
        flag = "move"

    for i in range(len(stay_point_centers) - 1):
        move_range.append((stay_point_centers[i].leaveTime, stay_point_centers[i + 1].arriveTime))

    if points[-1].dateTime != stay_point_centers[-1].leaveTime:
        move_range.append((stay_point_centers[-1].leaveTime, points[-1].dateTime))

    return move_range, flag


@method_decorator(csrf_exempt, name='dispatch')
class PathDailyRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_user = request.data['user']
        user, created = User.objects.get_or_create(username=request_user)
        if created:
            user.set_password('123')
            user.save()

        app_user, _ = AppUser.objects.get_or_create(user=user)
        app_user.fcmToken = request.data["fcmToken"]
        request_time_sequence = request.data['timeSequence']
        date_sequence = make_date_sequence(request_time_sequence, app_user)

        for date_key, date_value in date_sequence.items():
            daily_path, created = DailyPath.objects.get_or_create(user=app_user, date=date_key)

            if not date_value:
                continue

            # GPS log 저장
            for date in date_value:
                GPSLog.objects.create(
                    daily_path=daily_path,
                    timestamp=datetime.strptime(date['time'], '%Y-%m-%d %H:%M:%S'),
                    latitude=date['coordinates']['latitude'],
                    longitude=date['coordinates']['longitude']
                )
            gps_logs = make_gps_logs(date_value)
            points = generatePoints(gps_logs)
            stay_point_centers, stay_points = stayPointExtraction(points)
            move_points, add_flag = make_move_point(points, stay_point_centers)

            interval_stay_obj = IntervalStay.objects.filter(daily_path=daily_path).order_by('start_time').last()
            interval_move_obj = IntervalMove.objects.filter(daily_path=daily_path).order_by('start_time').last()
            interval_flag = check_last_interval(interval_stay_obj, interval_move_obj)

            # print(interval_flag, add_flag)
            if interval_flag == "move" and add_flag == "move":
                _, end_time = move_points.pop(0)
                end = datetime.strptime(end_time, DATETIME_FORMAT)
                interval_move_obj.end_time = end_time
                interval_move_obj.percent = make_percent(
                    interval_move_obj.start_time,
                    end
                )
                interval_move_obj.save()
            elif interval_flag == "stay" and add_flag == "stay":
                point = stay_point_centers.pop(0)
                d = get_distance(
                    interval_stay_obj.latitude,
                    interval_stay_obj.longitude,
                    point.latitude,
                    point.longitude
                )
                if d < 200:
                    interval_stay_obj.end_time = point.leaveTime
                    interval_stay_obj.save()
                else:
                    stay_point_centers.insert(0, point)

            make_stay_interval(app_user, daily_path, stay_point_centers)
            make_move_interval(app_user, daily_path, move_points)
            # print("daily path 하나 성공")

        content = make_response_content("성공", {})
        return Response(content, status=status.HTTP_200_OK)


def make_stay_point(data: Dict) -> Dict:
    stay_point = {
        "start_time": data["time"],
        "end_time": data["time"][:10] + " 23:59:59",
        "latitude": float(data["coordinates"]["latitude"]),
        "longitude": float(data["coordinates"]["longitude"])
    }
    return stay_point

@method_decorator(csrf_exempt, name='dispatch')
class PathPastRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        request_user = request.data['user']
        request_date = request.data['date']
        request_time_sequence = request.data['timeSequence']

        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        daily_path_obj, created = DailyPath.objects.get_or_create(
            user=user,
            date=request_date
        )

        if not created:
            content = make_response_content("이미 존재하는 daily path", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        daily_path_obj.path_type = "past"
        daily_path_obj.save()

        # print(daily_path_obj.date, daily_path_obj.path_type)
        if not request_time_sequence:
            content = make_response_content("time sequence 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        request_time_sequence = sorted(request_time_sequence, key=lambda x: x["time"])
        stay_points = []
        for idx, data in enumerate(request_time_sequence):
            if idx == 0:
                stay_point = make_stay_point(data)
                stay_points.append(stay_point)
            else:
                d = get_distance(
                    stay_points[-1]["latitude"],
                    stay_points[-1]["longitude"],
                    float(data["coordinates"]["latitude"]),
                    float(data["coordinates"]["longitude"])
                )
                stay_points[-1]["end_time"] = data["time"]
                if d > 200:
                    stay_point = make_stay_point(data)
                    stay_points.append(stay_point)

        for point in stay_points:
            start = datetime.strptime(point["start_time"], DATETIME_FORMAT)
            end = datetime.strptime(point["end_time"], DATETIME_FORMAT)
            percent = make_percent(start, end)
            latitude = point["latitude"]
            longitude = point["longitude"]
            IntervalStay.objects.create(
                daily_path=daily_path_obj,
                start_time=start,
                end_time=end,
                address="?",
                category="과거",
                location="?",
                latitude=latitude,
                longitude=longitude,
                percent=percent
            )
        content = make_response_content("성공", {})
        return Response(content, status=status.HTTP_200_OK)


def make_blank_percent(info_data: List) -> float:
    blank_percent = 1.0
    for data in info_data:
        blank_percent -= data['percent']

    if blank_percent < 0:
        return 0.0
    return blank_percent


def make_blank_interval(percent: float) -> Dict:
    blank_interval = {
        "id": 0,
        "category": "없음",
        "detail": "없음",
        "percent": percent,
        "start": datetime.today()
    }
    return blank_interval


@method_decorator(csrf_exempt, name='dispatch')
class PieChartRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        content, status_code, interval_stay_objs, interval_move_objs = check_interval_objs(request_user, request_date)
        if status_code == status.HTTP_200_OK:
            info_data = list()
            info_data.extend([
                {
                    "id": interval_obj.id,
                    "category": interval_obj.category,
                    "detail": interval_obj.location,
                    "percent": interval_obj.percent,
                    "start": interval_obj.start_time
                } for interval_obj in interval_stay_objs
            ])
            info_data.extend([
                {
                    "id": interval_obj.id,
                    "category": "이동",
                    "detail": interval_obj.transport,
                    "percent": interval_obj.percent,
                    "start": interval_obj.start_time
                } for interval_obj in interval_move_objs
            ])
            info_data = sorted(info_data, key=lambda info: info['start'])
            blank_percent = make_blank_percent(info_data)
            info_data.append(
                make_blank_interval(blank_percent)
            )
            content['data']['info'] = info_data
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class MapRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        content, status_code, interval_stay_objs, _ = check_interval_objs(request_user, request_date)
        if status_code == status.HTTP_200_OK:
            info_data = [
                {
                    "id": interval_obj.id,
                    "category": interval_obj.category,
                    "address": interval_obj.address,
                    "coordinates": {
                        "latitude": interval_obj.latitude,
                        "longitude": interval_obj.longitude
                    }
                } for interval_obj in interval_stay_objs
            ]
            content['data']['info'] = info_data
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class MapLogRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content, status_code, daily_path_obj = check_daily_path_obj(request)

        if status_code == status.HTTP_200_OK:
            content['data']['info'] = list()
            interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_obj.id)
            for interval_move_obj in interval_move_objs:
                map_log_objs = GPSLog.objects.filter(daily_path=daily_path_obj,
                                                     timestamp__range=[interval_move_obj.start_time,
                                                                       interval_move_obj.end_time])
                content['data']['info'].extend([
                    {
                        "coordinates": {
                            "latitude": map_log_obj.latitude,
                            "longitude": map_log_obj.longitude
                        }
                    } for map_log_obj in map_log_objs
                ])
        return Response(content, status=status_code)


@method_decorator(csrf_exempt, name='dispatch')
class WeeklyRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        iso_year, iso_week, _ = datetime.strptime(request_date, "%Y-%m-%d").isocalendar()

        data = {
            "tag": {
                "start": datetime.fromisocalendar(iso_year, iso_week, 1).strftime("%Y년 %m월 %d일"),
                "end": datetime.fromisocalendar(iso_year, iso_week, 7).strftime("%Y년 %m월 %d일")
            },
            "days": []
        }
        for i in range(DAY):
            check_date = datetime.fromisocalendar(iso_year, iso_week, i + 1)
            try:
                user = AppUser.objects.get(user__username=request_user)
                daily_path_objs = DailyPath.objects.get(user=user, date=check_date)
                interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_objs)
                interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_objs)
            except AppUser.DoesNotExist:
                content = make_response_content("user 없음", {})
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            except DailyPath.DoesNotExist:
                day_data = {
                    "id": None,
                    "day": DAY_NAME[i],
                    "date": check_date,
                    "info": []
                }
                data["days"].append(day_data)
                continue

            day_data = {
                "id": daily_path_objs.id,
                "day": DAY_NAME[i],
                "date": check_date,
                "info": []
            }
            day_data["info"].extend([
                {
                    "id": interval_obj.id,
                    "category": interval_obj.category,
                    "percent": interval_obj.percent,
                    "time": {
                        "start": interval_obj.start_time,
                        "end": interval_obj.end_time
                    }
                } for interval_obj in interval_stay_objs
            ])
            day_data["info"].extend([
                {
                    "id": interval_obj.id,
                    "category": "이동",
                    "percent": interval_obj.percent,
                    "time": {
                        "start": interval_obj.start_time,
                        "end": interval_obj.end_time
                    }
                } for interval_obj in interval_move_objs
            ])
            day_data["info"] = sorted(day_data["info"], key=lambda x: x['time']['start'])
            data["days"].append(day_data)

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)


def get_category_idx(category: str) -> int:
    return CATEGORY_SORT.index(category)


def make_stat_data() -> List:
    stat_data = [
        {
            "category": category,
            "time_spent": timedelta(0)
        } for category in CATEGORY_SORT
    ]
    return stat_data


@method_decorator(csrf_exempt, name='dispatch')
class MonthlyRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        today = datetime.today()
        request_year, request_month, _ = map(int, request_date.split('-'))
        _, end = calendar.monthrange(request_year, request_month)
        start_iso = datetime(request_year, request_month, 1).isocalendar()
        end_iso = datetime(request_year, request_month, end).isocalendar()

        start_date = datetime.fromisocalendar(start_iso.year, start_iso.week, 1)
        end_date = datetime.fromisocalendar(end_iso.year, end_iso.week, 7)

        diff = (end_date - start_date).days
        if request_year == today.year and request_month == today.month:
            print("이번달")
            content = make_response_content("month data 부족", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        user_obj = AppUser.objects.get(user__username=request_user)

        data = {
            "tag": f'{request_year}-{request_month:02d}',
            "weeks": []
        }
        cnt = (diff + 1) // DAY
        for i in range(cnt):
            s_date = start_date + timedelta(7 * i)
            e_date = start_date + timedelta(7 * i + 6)

            stat_data = make_stat_data()
            total = timedelta(0)
            daily_path_objs = DailyPath.objects.filter(user=user_obj, date__range=[s_date, e_date])
            for daily_path_obj in daily_path_objs:
                interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj.id)
                interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_obj.id)

                for interval_stay_obj in interval_stay_objs:
                    idx = get_category_idx(interval_stay_obj.category)
                    stat_data[idx]['time_spent'] += interval_stay_obj.end_time - interval_stay_obj.start_time
                    total += interval_stay_obj.end_time - interval_stay_obj.start_time

                for interval_move_obj in interval_move_objs:
                    idx = get_category_idx('이동')
                    stat_data[idx]['time_spent'] += interval_move_obj.end_time - interval_move_obj.start_time
                    total += interval_move_obj.end_time - interval_move_obj.start_time

            for stat in stat_data:
                if total != timedelta(0):
                    stat["percent"] = stat["time_spent"] / total
                else:
                    stat["percent"] = 0.0

                total_seconds = int(stat["time_spent"].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                stat['time_spent'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            week_data = {
                "order": i + 1,
                "info": stat_data
            }
            data["weeks"].append(week_data)

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class YearlyRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        request_date = request.headers['date']

        today = datetime.today()
        request_year, _, _ = map(int, request_date.split('-'))
        if request_year == today.year:
            print("이번 연도")
            content = make_response_content("year data 부족", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        data = {
            "tag": f'{request_year}',
            "months": []
        }
        user_obj = AppUser.objects.get(user__username=request_user)
        for i in range(MONTH):
            stat_data = make_stat_data()
            total = timedelta(0)
            daily_path_objs = DailyPath.objects.filter(user=user_obj, date__year=request_year, date__month=i)
            for daily_path_obj in daily_path_objs:
                interval_stay_objs = IntervalStay.objects.filter(daily_path=daily_path_obj.id)
                interval_move_objs = IntervalMove.objects.filter(daily_path=daily_path_obj.id)

                for interval_stay_obj in interval_stay_objs:
                    idx = get_category_idx(interval_stay_obj.category)
                    stat_data[idx]['time_spent'] += interval_stay_obj.end_time - interval_stay_obj.start_time
                    total += interval_stay_obj.end_time - interval_stay_obj.start_time

                for interval_move_obj in interval_move_objs:
                    idx = get_category_idx('이동')
                    stat_data[idx]['time_spent'] += interval_move_obj.end_time - interval_move_obj.start_time
                    total += interval_move_obj.end_time - interval_move_obj.start_time

            for stat in stat_data:
                if total != timedelta(0):
                    stat["percent"] = stat["time_spent"] / total
                else:
                    stat["percent"] = 0.0

                total_seconds = int(stat["time_spent"].total_seconds())
                hours, remainder = divmod(total_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                stat['time_spent'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

            month_data = {
                "order": i + 1,
                "info": stat_data
            }
            data["months"].append(month_data)

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PathListRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        request_user = request.headers['user']
        try:
            user = AppUser.objects.get(user__username=request_user)
        except AppUser.DoesNotExist:
            content = make_response_content("user 없음", {})
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


        try:
            request_date = request.headers['date']
            year, month = map(int, request_date.split('-'))
        except:
            year = datetime.today().year
            month = datetime.today().month

        data = {
            "dateList": []
        }

        daily_path_objs = DailyPath.objects.filter(user=user, date__year=year, date__month=month).order_by('date')
        for daily_path_obj in daily_path_objs:
            data["dateList"].append(daily_path_obj.date)

        content = make_response_content("성공", data)
        return Response(content, status=status.HTTP_200_OK)