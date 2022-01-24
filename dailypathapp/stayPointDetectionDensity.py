"""
-*- coding: utf-8 -*-
@Author  : zhang35
@Time    : 2020/09/16 18:00
@Function: extract stay points from a GPS log file (implementation of algorithm in [2])

References:
[1] Q. Li, Y. Zheng, X. Xie, Y. Chen, W. Liu, and W.-Y. Ma, "Mining user similarity based on location history", in Proceedings of the 16th ACM SIGSPATIAL international conference on Advances in geographic information systems, New York, NY, USA, 2008, pp. 34:1--34:10.
[2] Jing Yuan, Yu Zheng, Liuhang Zhang, XIng Xie, and Guangzhong Sun. 2011. Where to find my next passenger. In Proceedings of the 13th international conference on Ubiquitous computing (UbiComp '11). Association for Computing Machinery, New York, NY, USA, 109–118.

test data could be downloaded from: https://www.microsoft.com/en-us/download/confirmation.aspx?id=52367
"""
import time
from math import radians, cos, sin, asin, sqrt

time_format = '%Y-%m-%d %H:%M:%S'


# structure of point
class Point:
    def __init__(self, latitude, longitude, dateTime, arriveTime, leaveTime):
        self.latitude = latitude
        self.longitude = longitude
        self.dateTime = dateTime
        self.arriveTime = arriveTime
        self.leaveTime = leaveTime

    def __repr__(self):
        # return f"({self.latitude}, {self.longitude}) " \
        #        f"{time.strftime(time_format, time.localtime(self.arriveTime))} ~ {time.strftime(time_format, time.localtime(self.leaveTime))}"
        return f"{self.dateTime}"


# calculate distance between two points from their coordinate
def getDistanceOfPoints(pi, pj):
    lat1, lon1, lat2, lon2 = list(map(radians, [float(pi.latitude), float(pi.longitude),
                                                float(pj.latitude), float(pj.longitude)]))
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    m = 6371000 * c
    return m


# calculate time interval between two points
def getTimeIntervalOfPoints(pi, pj):
    t_i = time.mktime(time.strptime(pi.dateTime, time_format))
    t_j = time.mktime(time.strptime(pj.dateTime, time_format))
    return t_j - t_i


# compute mean coordinates of a group of points
def computMeanCoord(gpsPoints):
    lat = 0.0
    lon = 0.0
    for point in gpsPoints:
        lat += float(point.latitude)
        lon += float(point.longitude)
    return (lat / len(gpsPoints), lon / len(gpsPoints))


def stayPointExtraction(points, distThres=200, timeThres=30 * 60):
    """
    extract stay points from a GPS log file
    input:
           points: point 객체들
           distThres: distance threshold
           timeThres: time span threshold
    default values of distThres and timeThres are 200 m and 30 min respectively, according to [1]
    """
    stayPointCenterList = []
    stayPointList = []
    pointNum = len(points)
    i = 0
    while i < pointNum - 1:
        # j: index of the last point within distTres
        j = i + 1
        flag = False
        while j < pointNum:
            if getDistanceOfPoints(points[i], points[j]) < distThres:
                j += 1
            else:
                break

        j -= 1
        # at least one point found within distThres
        if j > i:
            # candidate cluster found
            if getTimeIntervalOfPoints(points[i], points[j]) > timeThres:
                nexti = i + 1
                j += 1
                while j < pointNum:
                    if getDistanceOfPoints(points[nexti], points[j]) < distThres and \
                            getTimeIntervalOfPoints(points[nexti], points[j]) > timeThres:
                        nexti += 1
                        j += 1
                    else:
                        break
                j -= 1
                latitude, longitude = computMeanCoord(points[i: j + 1])
                arriveTime = time.mktime(time.strptime(points[i].dateTime, time_format))
                leaveTime = time.mktime(time.strptime(points[j].dateTime, time_format))
                dateTime = time.strftime(time_format, time.localtime(arriveTime)), time.strftime(time_format,
                                                                                                 time.localtime(
                                                                                                     leaveTime))
                stayPointCenterList.append(Point(latitude, longitude, dateTime, arriveTime, leaveTime))
                stayPointList.extend(points[i: j + 1])
        i = j + 1
    return stayPointCenterList, stayPointList


# parse lines into points
def generatePoints(time_sequence):
    points = []
    for latitude, longitude, dateTime in time_sequence:
        points.append(Point(latitude, longitude, dateTime, 0, 0))
    return points


def main():
    time_sequence = []

    # file open
    fp = open("./dummy/gps_logs.plt", 'r')

    lines = fp.readlines()[6:]
    for line in lines:
        split_obj = line.rstrip().split(',')
        latitude = float(split_obj[0])
        longitude = float(split_obj[1])
        dateTime = f"{split_obj[-2]} {split_obj[-1]}"

        time_sequence.append((latitude, longitude, dateTime))
    # file close
    fp.close()

    points = generatePoints(time_sequence)
    stayPointCenter, stayPoint = stayPointExtraction(points)

    for ele in stayPointCenter:
        print(ele)


if __name__ == '__main__':
    main()
