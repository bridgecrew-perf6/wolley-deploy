from testapp.models import TestTable


def make_dummy_interval_info(interval_id: int, start_time: str, end_time: str, label: str):
    interval = dict()
    interval["id"] = interval_id
    interval["startTime"] = start_time
    interval["endTime"] = end_time
    interval["labels"] = [label]
    return interval


def make_dummy_piechart_info_ver1():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["id"] = 132

    content["data"]["info"] = list()

    content["data"]["info"].append(
        make_dummy_interval_info(1, "2022-01-12 00:00:00", "2022-01-12 09:00:00", "A장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(2, "2022-01-12 09:00:00", "2022-01-12 09:52:00", "이동(차)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(3, "2022-01-12 09:52:00", "2022-01-12 11:58:00", "B장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(4, "2022-01-12 11:58:00", "2022-01-12 12:08:00", "이동(도보)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(5, "2022-01-12 12:08:00", "2022-01-12 12:43:00", "C장소")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(6, "2022-01-12 12:43:00", "2022-01-12 12:52:00", "이동(도보)")
    )
    content["data"]["info"].append(
        make_dummy_interval_info(7, "2022-01-12 12:52:00", "2022-01-12 13:34:00", "B장소")
    )

    return content


def make_dummy_piechart_info_ver2():
    content = dict()
    content["responseMsg"] = "성공"

    content["data"] = dict()
    content["data"]["id"] = 132
    content["data"]["date"] = "2022-01-04"

    content["data"]["info"] = list()

    # 1번째 info 정보
    info1 = dict()
    info1["id"] = 1
    info1["intervalCategory"] = "집"
    info1["intervalLocation"] = "그린빌라"
    info1["time"] = {"start": "00:00:00", "end": "08:30:10"}
    info1["coordinate"] = {"latitude": 37.49711896196244, "longitude": 126.98005979012468}
    info1["address"] = "서울특별시 동작구 동작동 102-12 그린빌라"
    info1["percent"] = 0.65
    info1["emotion"] = "중립"

    # 2번째 info 정보
    info2 = dict()
    info2["id"] = 2
    info2["intervalCategory"] = "회사"
    info2["intervalLocation"] = "카카오브레인"
    info2["time"] = {"start": "09:10:00", "end": "10:15:10"}
    info2["coordinate"] = {"latitude": 37.40286996786888, "longitude": 127.1074258713285}
    info2["address"] = "경기도 성남시 분당구 삼평동 판교역로241번길 20 KR 미래에셋벤처타워 11층"
    info2["percent"] = 0.35
    info2["emotion"] = "긍정"

    content["data"]["info"] = [info1, info2]

    return content


def save_raw_in_test_table(request):
    """
    FE의 request 내용을 raw하게 Test 테이블의 textfield에 있는 그대로 저장
    """
    content = request.data
    TestTable.objects.create(textfield=content)


def make_dummy_timestamps():
    # make dummy data
    request = dict()

    uuid = "90A0A65E-67EF-4063-B47E-06D6BCC12BAD"
    request["uuid"] = uuid
    request["timeSequence"] = []

    # file open

    ##############
    import os.path

    folder = os.getcwd()
    print('current directory :%s, !!!!!!!!!!!!!!!!!!!!!!!!!!!' % folder)

    for filename in os.listdir(folder):
        print(filename)
    ###################

    fp = open("./dailypathapp/gps_logs.plt", 'r')

    lines = fp.readlines()[6:]
    for line in lines:
        obj = dict()

        split_obj = line.rstrip().split(',')
        latitude = float(split_obj[0])
        longitude = float(split_obj[1])
        obj["coordinate"] = dict()
        obj["coordinate"]["latitude"] = latitude
        obj["coordinate"]["longitude"] = longitude
        obj["time"] = f"{split_obj[-2]} {split_obj[-1]}"
        request["timeSequence"].append(obj)
    # file close
    fp.close()
    return request
