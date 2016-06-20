# -*- coding: utf-8 -*-
import csv, os, requests, json, sys, codecs
#import warning, time
#from pygeocoder import Geocoder, GeocoderResult
PYTHONIOENCODING='utf-8'


def filter(file):   # csvファイルから地名リストを作る
    reader = csv.reader(file)
    list = []
    for row in reader:
        list.append(row[0])
    return list

def YOLP_search(placelist, infolist):   # YOLPコンテンツジオコーダAPIを利用して住所を取得
    # Web Services by Yahoo! JAPAN
    url = "http://contents.search.olp.yahooapis.jp/OpenLocalPlatform/V1/contentsGeoCoder?"
    payload = {
        "appid" : os.environ.get("YAHOO_dev_ID"),   # 環境変数
        "output" : "json"
        }
    count = 0
    for place in placelist:
        placename = place.decode('utf-8')
        payload["query"] = placename
        r = requests.get(url, params=payload)
        res = r.json()
        if res["ResultInfo"]["Count"] != 0:
#            print placename
            p = {
                "placename" : placename,
                "coordinates" : res["Feature"][0]["Geometry"]["Coordinates"],
                "address" : res["Feature"][0]["Property"]["Address"]
                }
            infolist.append(p)
            count += 1
        if count >= 15000:  # 必要なデータの数を取り終えたら終了
            break
    return infolist

def search(list):   # 地名リストからメタ情報のリストをつくる
    info = []
#    GoogleMapsGeocodingAPI 使用回数制限：一日2500アクセスまで
#    geocoder = Geocoder()
#    for place in list:
#        placename = place.decode('utf-8')
#        with warnings.catch_warnings():
#            warnings.simplefilter("ignore")
#            result = geocoder.geocode(placename)
#        p = {"placename" : placename, "info" : result.coordinates}
#        info.append(p)
#        time.sleep(0.2)
    YOLP_search(list, info)
    return info

def export(file, list):     # 地名、緯度経度、大体の住所を出力
    for p in list:
        file.write("%s\t%s\t%s\n" % (p["placename"], p["coordinates"], p["address"]))



if __name__ == "__main__":

    datafile = open("~/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20160616/Noun.place.csv", "r")
    exportfile = open("metainfo.txt", "w")
    exportfile = codecs.lookup('utf_8')[-1](exportfile)

    placelist = filter(datafile)
    metainfolist = search(placelist)
    export(exportfile, metainfolist)
    print "datasize = %d" % len(placelist)
    print "resultsize = %d" % len(metainfolist)