from testapp.models import TestTable


def make_dummy_interval_info(interval_id: int, start_time: str, end_time: str, label: str):
    interval = dict()
    interval["id"] = interval_id
    interval["startTime"] = start_time
    interval["endTime"] = end_time
    interval["labels"] = [label]
    return interval


def make_dummy_piechart_info():
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


def save_raw_in_test_table(request):
    """
    FE의 request 내용을 raw하게 Test 테이블의 textfield에 있는 그대로 저장
    """
    content = request.data
    Test.objects.create(textfield=content)