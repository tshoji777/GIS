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
import pandas
import datetime as dt
import codecs
import folium

#import convert_coordinate as coord
#import data_master as master

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#from selenium import webdriver

_today = dt.date.today()
#------------------------------------------------------------------
# Main
#
#------------------------------------------------------------------
def main():
    try:
        map1 = folium.Map(location=[35.879207,139.520363], zoom_start=10)
        """
        folium.CircleMarker([35.879207,139.520363],
                            popup='ふじみ野市',
                            color='#3186cc',
                            fill_color='#3186cc',
                            ).add_to(map1)
        """


        folium.Marker([35.632896,139.880394], popup='東京ディズニーランド' ).add_to(map1)
        folium.Marker([35.654971,139.753319], popup='ミライズ' ).add_to(map1)
        map1.save('./map1.html')
    except:
        print(traceback.format_exc())

if __name__ == "__main__":
    main()


