from myapi.settings.__init__ import *
import django
import pprint

os.environ.setdefault("DJANGO_SETTING_MODULE", "myapi.settings")
django.setup()


def parse(coarse_list):
    latitude = float(coarse_list[-4][1:-1])
    longitude = float(coarse_list[-3][:-1])

    date_str = coarse_list[-2]
    time_str = coarse_list[-1]
    timestamp = f"{date_str} {time_str}"

    return latitude, longitude, timestamp


def mk_timeSequence_from_txt_file(fp):
    timeSequence = list()
    for line in fp.readlines():
        line_splited = line.rstrip().split()
        lat, long, timestamp = parse(line_splited)
        data = {"time": timestamp, "coordinates": {"latitude": lat, "longitude": long}}
        timeSequence.append(data)
    return timeSequence


# python manage.py runscript -v2 mkDummyGPSLogs --script-args TESTBOY
def run(uuid):
    # mk timeSequence
    fp = open("scripts/dummyData.txt", 'r')
    timeSequence = mk_timeSequence_from_txt_file(fp)
    timeSequence.sort(key=lambda x: x["time"])
    fp.close()

    data_to_print = {"user": uuid, "timeSequence": timeSequence}

    print("********** Copy below & Beautify json : https://jsonformatter.curiousconcept.com/ ************")
    print(data_to_print)
