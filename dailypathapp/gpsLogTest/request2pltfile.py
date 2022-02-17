import folium
import dummy_data as dum
import os, sys


def main():
    m = folium.Map(location=[37.566651, 126.978428], zoom_start=12)
    mapDots = folium.map.FeatureGroup()

    fp = open("buffer/dummyfile.plt", "w")

    fp.writelines("Geolife trajectory\n")
    fp.writelines("WGS 84\n")
    fp.writelines("altitude is in Feet\n")
    fp.writelines("Reserved 3\n")
    fp.writelines("0,2,255,My Track,0,0,2,12345678\n")
    fp.writelines("0\n")

    datas = dum.data
    for data in datas["timeSequence"]:
        # print(data)
        y = data["coordinate"]["latitude"]
        x = data["coordinate"]["longitude"]

        date, time = data["time"].split()

        fp.writelines(f"{y},{x},{date},{time}\n")

    print("plt 파일 생성 완료")
    fp.close()


if __name__ == '__main__':
    main()
