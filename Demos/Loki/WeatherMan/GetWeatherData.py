#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests

from pprint import pprint

BASEPATH = os.path.dirname(os.path.abspath(__file__))
infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki/WeatherMan", "")
infoDICT = json.load(open(infoPath, "r"))
AuthorizationKEY = infoDICT["weather_api_key"]

weatherURL = "https://opendata.cwb.gov.tw/api/v1/rest/datastore"

DatastoreID = {
    # "城市" : ["未來 2 天", "未來 1 週"]
    "宜蘭縣": ["F-D0047-001", "F-D0047-003"],
    "桃園市": ["F-D0047-005", "F-D0047-007"],
    "新竹縣": ["F-D0047-009", "F-D0047-011"],
    "苗栗縣": ["F-D0047-013", "F-D0047-015"],
    "彰化縣": ["F-D0047-017", "F-D0047-019"],
    "南投縣": ["F-D0047-021", "F-D0047-023"],
    "雲林縣": ["F-D0047-025", "F-D0047-027"],
    "嘉義縣": ["F-D0047-029", "F-D0047-031"],
    "屏東縣": ["F-D0047-033", "F-D0047-035"],
    "臺東縣": ["F-D0047-037", "F-D0047-039"],
    "花蓮縣": ["F-D0047-041", "F-D0047-043"],
    "澎湖縣": ["F-D0047-045", "F-D0047-047"],
    "基隆市": ["F-D0047-049", "F-D0047-051"],
    "新竹市": ["F-D0047-053", "F-D0047-055"],
    "嘉義市": ["F-D0047-057", "F-D0047-059"],
    "臺北市": ["F-D0047-061", "F-D0047-063"],
    "高雄市": ["F-D0047-065", "F-D0047-067"],
    "新北市": ["F-D0047-069", "F-D0047-071"],
    "臺中市": ["F-D0047-073", "F-D0047-075"],
    "臺南市": ["F-D0047-077", "F-D0047-079"],
    "連江縣": ["F-D0047-081", "F-D0047-083"],
    "金門縣": ["F-D0047-085", "F-D0047-087"],
    "臺灣":   ["F-D0047-089", "F-D0047-091"]
}

ForecastFactor = {
    "溫度": "T",
    "露點溫度": "Td",
    "相對濕度": "RH",
    "風向": "WD",
    "風速": "WS",
    "體感溫度": "AT",
    "舒適度": "CI",    # 一週天氣預報無此選項
    #"最小舒適度指數": "MinCI",
    #"最大舒適度指數": "MaxCI",
    "天氣現象": "Wx",
    "降雨機率": "PoP12h",
    "6小時降雨機率": "PoP6h",    # 一週天氣預報無此選項
    "12小時降雨機率": "PoP12h",
    "最高溫度": "MaxT",
    "最低溫度": "MinT",
    "最高舒適度": "MaxCI",
    "最低舒適度": "MinCI",
    "最高體感溫度": "MaxAT",
    "最低體感溫度": "MinAT",
    "紫外線指數": "UVI",
    "天氣描述": "WeatherDescription"
}

for city in DatastoreID:
    if city == "臺灣":
        continue
    payload = {"Authorization": AuthorizationKEY,
               "format": "JSON",
               "locationName": [city],
               "elementName": ["T", "MaxAT", "MinAT", "MaxT", "MinT", "PoP12h", "Td", "RH", "Wx", "UVI", "WeatherDescription"],
               "sort": "startTime"}

    result = requests.get("{}/F-D0047-091".format(weatherURL), headers={"Content-Type": "application/json"}, params=payload)
    print(city, result)
    #pprint(result.json())

    with open("{}/datastore/{}.json".format(BASEPATH, city), "w", encoding="UTF-8") as nf:
        json.dump(result.json()["records"]["locations"][0]["location"][0], nf, ensure_ascii=False, indent=4)
    #break