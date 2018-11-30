# -*- coding: utf-8 -*-
"""
Created on Tue May  8 21:27:00 2018

SONY BANK 国土交通省地価公示

@author: MILIZE
"""
import sys
import os
import requests
import lxml.html
import traceback
import xlrd as xl
import re
import zenhan
import pandas as pd
import datetime as dt
import codecs
import folium
import numpy as np
#import convert_coordinate as coord
#import data_master as master

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#from selenium import webdriver
import csv
_today = dt.date.today()

def read_tokyo_data():
    #tokyoのShape用DBF（CSV変換後）を取得
    tokyo_csv = pd.read_csv('./data/tokyo.csv', encoding='shift-jis', engine='python')

    #東京都の人口データ取得
    with open("./data/tokyo_人口.csv", "r", encoding = "shift-jis") as f:      
        csv_data = csv.reader(f)
        tokyo_population = [row for row in csv_data]

    return tokyo_csv, tokyo_population

def set_result(pop, result):
    dictKey = [ "15～19歳:","20～24歳:","25～29歳:","30～34歳:",\
                "35～39歳:","40～44歳:","45～49歳:"]

    print(result)

    old = 0
    for i in range(len(dictKey)):
        old = int(result[dictKey[i]])
        if( pop[i+1] != '' ):
            try:
                b = int(pop[i+1])
                nvalue = old + int(pop[i+11])
                result.update({ dictKey[i]:nvalue })
            except:
                continue
    print(result)

def find_population(map_csv, pop, lat, lot, x):
    pd.options.display.precision = 4

    #1kmあたりの緯度経度の変化値
    #   0.010966404715491394
    lat_min = lat - (0.010966404715491394 * x )
    lat_max = lat + (0.010966404715491394 * x )

    lot_min = lot - (0.010966404715491394 * x )
    lot_max = lot + (0.010966404715491394 * x )

    print(lat_min)
    print(lat_max)
    print(lot_min)
    print(lot_max)

    #dfdf = (df[(df["データ日付"] == survey.replace('年','-').replace('月',''))])

    map_df = ( map_csv[( map_csv['Y_CODE'] >= float(lat_min) ) & \
                       ( map_csv['Y_CODE'] <= float(lat_max) ) & \
                       ( map_csv['X_CODE'] >= float(lot_min) ) & \
                       ( map_csv['X_CODE'] <= float(lot_max) ) ] )

    if( len(map_df) == 0 ):
        return 'not data'
    else:
        pop_info = {
            "15～19歳:":0, "20～24歳:": 0,
            "25～29歳:":0, "30～34歳:": 0,
            "35～39歳:":0, "40～44歳:": 0,
            "45～49歳:":0 
        }
        dictKey = [ "15～19歳:","20～24歳:","25～29歳:","30～34歳:",\
                    "35～39歳:","40～44歳:","45～49歳:"]

        pop_key = map_df['KEY_CODE']
        result = []
        for item in pop_key:
            if( len(str(item)) == 11 ):
                result.append(str(item))
        for key in pop:
            old = 0
            if( str(key[0]) in result ):
                print(key[2]+key[3])
                for i in range(len(dictKey)):
                    print(dictKey[i])
                    old = int(pop_info[dictKey[i]])
                    try:
                        b = int(key[i + 11])
                        nvalue = old + int(key[i+11])
                        pop_info.update({ dictKey[i]:nvalue })
                    except:
                        continue
                #T000849005	T000849006	T000849007	T000849008	T000849009	T000849010	T000849011
                #  15～19歳    20～24歳    25～29歳    30～34歳     35～39歳    40～44歳     45～49歳
                print("KEY     :", key[0])
                print("KEY     :", key[2]+key[3])
                print("15～19歳:", key[11])
                print("20～24歳:", key[12])
                print("25～29歳:", key[13])
                print("30～34歳:", key[14])
                print("35～39歳:", key[15])
                print("40～44歳:", key[16])
                print("45～49歳:", key[17])
        return pop_info 

#------------------------------------------------------------------
# Main
#
#------------------------------------------------------------------
def main():
    try:
        tokyo_csv, tokyo_population = read_tokyo_data()
        with open("./かつや.csv", "r", encoding = "utf_8_sig") as f:      
            csv_data = csv.reader(f)
            data = [row for row in csv_data]

        #map1 = folium.Map(location=[35.879207,139.520363], zoom_start=10)
        #中心点を東京駅に設定
        map1 = folium.Map(location=[35.681382, 139.76608399999998], zoom_start=12)

        #人口集計
        for i in range(1, len(data)):
            pop_info = find_population(tokyo_csv, tokyo_population, \
                                 float(data[i][2]), float(data[i][3]), 0.5)

            population = ''
            for key in pop_info.keys():
                population = population + '  ' + key + str(pop_info[key]) + '人<br>'

            folium.Marker([float(data[i][2]), float(data[i][3])],
                            popup = data[i][0] + '<br>' + data[i][1] + '<br>' + population,
                            ).add_to(map1)
            """
            folium.CircleMarker([float(data[i][2]), float(data[i][3])],
                            popup = data[i][0],
                            color = '#3186cc', 
                            fill = True, 
                            fill_color = '#3186cc',
                            ).add_to(map1)
            """
            folium.Circle([float(data[i][2]), float(data[i][3])],
                            color ='#3186cc', 
                            fill=True,
                            fill_color = '#3186cc',
                            radius=500).add_to(map1)

        """
        folium.CircleMarker([35.879207,139.520363],
                            popup='ふじみ野市',
                            color='#3186cc',
                            fill_color='#3186cc',
                            ).add_to(map1)
        folium.Marker([35.632896,139.880394], popup='東京ディズニーランド' ).add_to(map1)
        folium.Marker([35.654971,139.753319], popup='ミライズ' ).add_to(map1)
        """
        map1.save('./map1.html')
    except:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()


