import requests
import json
from math import radians, cos, sin, asin, sqrt

from accountapp.models import Estimate, AppUser
from myapi.settings.__init__ import *
# from myapi.settings.deploy import *


def coordinate2address(latitude: float, longitude: float) -> str:
    """
    위도, 경도를 입력받아 해당 좌표의 주소를 반환하는 함수

    Args:
        latitude (float): 위도 입력 값
        longitude (float): 경도 입력 값

    Returns:
        return_address (str): 입력 받은 위도, 경도 값의 주소
    """
    base_url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?y={latitude}&x={longitude}&input_coord=WGS84"
    rest_api_key = MY_REST_API_KEY
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}
    api_request = requests.get(base_url, headers=headers)
    json_data = json.loads(api_request.text)
    return_address = json_data["documents"][0]["address_name"]
    return return_address


def get_distance(y1: float, x1: float, y2: float, x2: float) -> int:
    """
    입력된 좌표의 거리를 계산하는 함수

    Args:
        y1 (float): 입력 값
        x1 (float): 입력 값
        y2 (float): 입력 값
        x2 (float): 입력 값

    Returns:
        m (integer): 계산된 거리 값
    """
    lat1, lon1, lat2, lon2 = list(map(radians, [y1, x1, y2, x2]))
    diff_lon = lon2 - lon1
    diff_lat = lat2 - lat1
    a = sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2
    c = 2 * asin(sqrt(a))
    m = 6371000 * c
    return m


def get_visited_place(latitude: float, longitude: float, app_user_obj: AppUser, DIST_THR: int = 200) -> str:
    """
    입력된 좌표가 이전에 사용자가 방문한 동선과 겹치는 부분이 있는지 확인하는 함수

    Args:
        latitude (float): 위도 입력 값
        longitude (float): 경도 입력 값
        app_user_obj (AppUser): 사용자 object
        DIST_THR (int): 거리 차이 기준

    Returns:
        category (str): 기존의 동선과 겹치면 해당 category 값을 아닐 경우 "?"
    """
    estimate_objs = Estimate.objects.filter(user=app_user_obj)
    for estimate_obj in estimate_objs:
        dist = get_distance(
            latitude,
            longitude,
            estimate_obj.latitude,
            estimate_obj.longitude
        )
        if dist < DIST_THR:
            return estimate_obj.category
    return "?"
