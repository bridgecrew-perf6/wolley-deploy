import requests
import json
from math import radians, cos, sin, asin, sqrt

from accountapp.models import Estimate, AppUser
# from myapi.settings.local import *
from myapi.settings.deploy import *


def coordinate2address(latitude, longitude):
    base_url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?y={latitude}&x={longitude}&input_coord=WGS84"
    rest_api_key = MY_REST_API_KEY
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}

    api_request = requests.get(base_url, headers=headers)
    json_data = json.loads(api_request.text)
    return_address = json_data["documents"][0]["address_name"]
    return return_address


def get_distance(y1, x1, y2, x2):
    lat1, lon1, lat2, lon2 = list(map(radians, [y1, x1, y2, x2]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    m = 6371000 * c
    return m


def get_visited_place(latitude: float, longitude: float, app_user_obj: AppUser, DIST_THR: int = 200) -> str:
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


if __name__ == "__main__":
    y = 37.49730343068551
    x = 126.95287244268468
    print(coordinate2address(y, x))
