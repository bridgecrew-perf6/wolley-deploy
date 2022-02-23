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
