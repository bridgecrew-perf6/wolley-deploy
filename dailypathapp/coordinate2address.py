import requests
import json
from myapi.settings.local import *
# from myapi.settings.deploy import *


def coordinate2address(latitude, longitude):
    base_url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?y={latitude}&x={longitude}&input_coord=WGS84"
    rest_api_key = MY_REST_API_KEY
    headers = {"Authorization": f"KakaoAK {rest_api_key}"}

    api_request = requests.get(base_url, headers=headers)
    json_data = json.loads(api_request.text)
    return_address = json_data["documents"][0]["address_name"]
    return return_address


if __name__ == "__main__":
    y = 37.49730343068551
    x = 126.95287244268468
    print(coordinate2address(y, x))
