# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 22:20:12 2017

@author: tshoji
"""
import os
import sys
import jsm
from time import sleep
import datetime
from dateutil.relativedelta import relativedelta
import traceback
import pandas as pd
import re

place = {"エブリイ6条店":"香川県高松市下田井372-1"}
"""
place = {
        "東京ディズニーランド":"千葉県浦安市舞浜1-1",
        "東京ディズニーシー":"千葉県浦安市舞浜1-13",
        "銀座三越":"東京都中央区銀座4丁目6-16",
        "新宿伊勢丹":"東京都新宿区新宿3丁目14-14",
        "東京ドーム":"東京都文京区後楽1-3-61",
        "よみうりランド 神奈川":"神奈川県川崎市多摩区菅仙谷4-1",
        "よみうりランド 東京":"東京都稲城市矢野口4015-1",
        "日本ビューホテル 浅草":"東京都台東区西浅草3丁目17-1",
        "日本ビューホテル 成田":"千葉県成田市小菅700",
        "大井競馬場":"東京都品川区勝島2丁目1-2",
        "楽天本社":"東京都世田谷区玉川1-14-1",
        "ファーストリテイリング旗艦店":"東京都中央区銀座6丁目9-5",
        "ファーストリテイリング":"東京都新宿区新宿3丁目29-1",
        "大塚家具 有明":"東京都江東区有明3-6-11",
        "大塚家具 銀座":"東京都中央区銀座1-9-13",
        "大塚家具 新宿":"東京都新宿区新宿3-33-1",
        "ニトリ 渋谷区神南":"東京都渋谷区神南1-12-13",
        "ニトリ 渋谷区千駄ヶ谷":"東京都渋谷区千駄ヶ谷5-24-2",
        "ニトリ 銀座":"東京都中央区銀座3-2-1",
        "ニトリ 吉祥寺":"東京都武蔵野市吉祥寺本町2-3-1",
        "ニトリ 池袋":"東京都豊島区西池袋1-1-25",
        "ドン・キホーテ 銀座":"東京都中央区銀座8-10",
        "ドン・キホーテ 六本木":"東京都港区六本木3-14-10",
        "ドン・キホーテ 赤坂":"東京都港区赤坂3丁目11-14",
        "ドン・キホーテ 白金台":"東京都港区白金台3-15-5",
        "ロイヤルホテル藤田観光 銀座":"東京都中央区銀座7-10-1",
        "ロイヤルホテル藤田観光 文京区関口":"東京都文京区関口2丁目10-8",
        "ロイヤルホテル藤田観光 新宿":"東京都新宿区西新宿3丁目2-9",
        "ロイヤルホテル藤田観光 有明":"東京都江東区有明3丁目7-11",
        "共立メンテナンス 渋谷区神宮前":"東京都渋谷区神宮前6丁目24-4",
        "共立メンテナンス 千代田区神田":"東京都千代田区神田須田町1-16",
        "共立メンテナンス 台東区花川戸":"東京都台東区花川戸1丁目3-4",
        "共立メンテナンス 千代田区外神田":"東京都千代田区外神田4-12-5",
        "東武ストア 西池袋":"東京都豊島区西池袋3丁目17-3",
        "東武ストア 板橋区赤塚":"東京都板橋区赤塚2-8-7-101",
        "東武ストア 板橋区高島平":"東京都板橋区高島平2-33-1-107",
        "東武ストア 板橋区小豆沢":"東京都板橋区小豆沢2-4-8-101",
        "東武ストア 大宮区寿能町":"埼玉県さいたま市大宮区寿能町1-177-5",
        "東武ストア 大宮区土手町":"埼玉県さいたま市大宮区土手町3丁目-285",
        "東武ストア 大宮区堀の内町":"埼玉県さいたま市大宮区堀の内町3丁目158-1",
        "東武ストア 朝霞市本町":"埼玉県朝霞市本町2-3-23",
        "富士急ハイランド":"山梨県富士吉田市新西原5-6-1",
        "東京タワー":"東京都港区芝公園4丁目2-8",
        "東京スカイツリー":"東京都墨田区押上1丁目1-2",
        "上野動物園":"東京都台東区上野公園9-83",
        "サンシャインシティ":"東京都 豊島区東池袋3丁目1-1",
        "浅草寺":"東京都台東区浅草2丁目3−1",
        "ジブリ美術館":"東京都三鷹市下連雀1丁目1−83"
}
"""

import time
import requests
import xmltodict

f = open("./result.csv", 'w')
url = 'http://www.geocoding.jp/api/'
for key, item in place.items():
    full_adress = item
    payload = {'q': full_adress}
    result = requests.get(url, params=payload)
    time.sleep(5)
    resultdict = xmltodict.parse(result.text)

    #>>>print(resultdict["result"]["coordinate"]["lat"])         #緯度
    #>>>print(resultdict["result"]["coordinate"]["lng"])         #経度
    f.write(key+','+item+','+str(resultdict["result"]["coordinate"]["lat"])+','+str(resultdict["result"]["coordinate"]["lng"])+'\n')
f.close()
"""
#ロジック２
import geocoder
import mesh_lib as mesh

f = open("./result.csv", 'w')
f.write('建物名,住所,緯度,経度,1次メッシュ,2次メッシュ,3次メッシュ,1/2メッシュ,1/4メッシュ,1/8メッシュ\n')

for key, item in place.items():
    Localname = item
    #g = geocoder.google(Localname)
    g = geocoder.arcgis(Localname)
    if(g.latlng is None):
        print(key, item)
    else:
        time.sleep(1)
        first_mesh = mesh.latlong_to_meshcode(g.latlng[0],g.latlng[1],1)
        second_mesh= mesh.latlong_to_meshcode(g.latlng[0],g.latlng[1],2)
        thard_mesh= mesh.latlong_to_meshcode(g.latlng[0],g.latlng[1],3)
        detail_mesh = mesh.latlong_to_detail_meshcode(g.latlng[0],g.latlng[1])

        result_text = key+','+item+','+str(g.latlng[0])+','+str(g.latlng[1])+','+\
                str(first_mesh)+','+str(second_mesh)[0:4]+'-'+str(second_mesh)[4:]+','+str(thard_mesh)[0:4]+'-'+str(thard_mesh)[4:]+','+\
                detail_mesh[0]+','+detail_mesh[1]+','+detail_mesh[2]+'\n'
        f.write(result_text)
        #print("lat=", g.latlng[0])
        #print("log=",g.latlng[1])

f.close()
"""
