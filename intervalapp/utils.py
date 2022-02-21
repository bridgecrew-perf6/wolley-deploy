import math
import requests
import json

from myapi.settings.__init__ import *


def make_coordiantes_range(latitude: float, longitude: float, diff = 0.01):
    base_lat = round(latitude, 2)
    base_lon = round(longitude, 2)

    start_lat, end_lat = base_lat - diff, base_lat + diff
    start_lon, end_lon = base_lon - diff, base_lon + diff

    return start_lon, start_lat, end_lon, end_lat


def make_coordinates_distance(base_lon, base_lat, place_x, place_y):
    x = base_lon - place_x
    y = base_lat - place_y
    return math.sqrt((x**2)+(y**2))


def search_location(keyword: str, latitude: float, longitude: float):
    base_url = f"https://dapi.kakao.com/v2/local/search/keyword.json"

    start_lon, start_lat, end_lon, end_lat = make_coordiantes_range(latitude, longitude, diff=0.005)

    params = {'query': keyword, 'rect': f'{start_lon},{start_lat},{end_lon},{end_lat}'}
    rest_api_key = MY_REST_API_KEY
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}
    api_request = requests.get(base_url, params=params, headers=headers)
    json_data_list = json.loads(api_request.text)
    data = {
        "locations": []
    }

    for json_data in json_data_list['documents']:
        print(json_data)
        data['locations'].append({
            "id": json_data['id'],
            "place": json_data['place_name'],
            "coordinates": {
                "longitude": json_data['x'],
                "latitude": json_data['y']
            },
            "distance": make_coordinates_distance(longitude, latitude, float(json_data['x']), float(json_data['y']))
        })
    data['locations'] = sorted(data['locations'], key=lambda x: x['distance'])
    return data
