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
    info1["intervalCategory"] = "회사"
    info1["intervalLocation"] = "카카오브레인"
    info1["time"] = {"start": "10:45:10", "end": "12:00:00"}
    info1["coordinate"] = {"latitude": 33.450901, "longitude": 126.570667}
    info1["labels"] = ["?"]
    info1["percent"] = 0.3
    info1["emotion"] = "긍정"

    # 2번째 info 정보
    info2 = dict()
    info2["id"] = 2
    info2["intervalCategory"] = "식사"
    info2["intervalLocation"] = "청년다방"
    info2["time"] = {"start": "12:10:00", "end": "13:00:00"}
    info2["coordinate"] = {"latitude": 33.450901, "longitude": 126.570667}
    info2["labels"] = ["음식점"]
    info2["percent"] = 0.1
    info2["emotion"] = "긍정"

    # 3번째 info 정보
    info3 = dict()
    info3["id"] = 1
    info3["intervalCategory"] = "회사"
    info3["intervalLocation"] = "카카오브레인"
    info3["time"] = {"start": "13:00:11", "end": "17:00:00"}
    info3["coordinate"] = {"latitude": 33.450901, "longitude": 126.570667}
    info3["labels"] = ["?"]
    info3["percent"] = 0.6
    info3["emotion"] = "긍정"

    content["data"]["info"] = [info1, info2, info3]

    return content


def save_raw_in_test_table(request):
    """
    FE의 request 내용을 raw하게 Test 테이블의 textfield에 있는 그대로 저장
    """
    content = request.data
    TestTable.objects.create(textfield=content)