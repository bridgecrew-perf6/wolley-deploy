

from dailypathapp.dummy.dummyData import data
import dailypathapp.stayPointDetectectionBasic as sp


def make_dummy_timestamps():
    # make dummy data
    request = dict()

    uuid = "90A0A65E-67EF-4063-B47E-06D6BCC12BAD"
    request["uuid"] = uuid
    request["timeSequence"] = []

    # file open

    ##############
    # import os.path
    #
    # folder = os.getcwd()
    # print('current directory :%s, !!!!!!!!!!!!!!!!!!!!!!!!!!!' % folder)
    #
    # for filename in os.listdir(folder):
    #     print(filename)
    ###################

    fp = open("gps_logs2.plt", 'r')

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


def generate_points_from_request(request_dict):
    time_seq = []
    for data in request_dict["timeSequence"]: # 추후 request.data로 고치면 됨
        latitude = data["coordinate"]["latitude"]
        longitude = data["coordinate"]["longitude"]
        dateTime = data["time"]
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)
    return points

def generate_points_from_dummy_data(request_dict):
    time_seq = []
    for data in request_dict["time_sequence"]:
        latitude = data["coordinate"][0]
        longitude = data["coordinate"][1]
        dateTime = data["time"]
        time_seq.append((latitude, longitude, dateTime))
    points = sp.generatePoints(time_seq)

    return points


def testtest():
    # 1. from request
    # request = make_dummy_timestamps()
    # points = generate_points_from_request(request)

    # 2. from data
    points = generate_points_from_dummy_data(data)

    stayPointCenter, stayPoint = sp.stayPointExtraction(points, distThres=200, timeThres=30 * 60)

    import time
    content = dict()
    asc = 65
    time_format = '%Y-%m-%d %H:%M:%S'
    for obj in stayPointCenter:
        name = f"{chr(asc)}장소"
        content[name] = f"{time.strftime(time_format, time.localtime(obj.arriveTime))} ~ {time.strftime(time_format, time.localtime(obj.leaveTime))}"
        asc += 1

    return content


print(testtest())
