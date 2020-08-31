#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Weather

    Input:
        pattern       str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

import datetime
import glob
import os
import rapidjson as json
import requests


BASEPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CityDICT = glob.glob("{}/datastore/*.json".format(BASEPATH))

datetimeFMT = "%Y-%m-%d %H:%M:%S"
defualtDatetime = datetime.datetime.now()

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki/WeatherMan/intent", "")
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""


def getCityForecastDict(city):
    forecastDICT = {}
    for c in CityDICT:
        if city in c:
            forecastDICT = json.load(open(c, "r", encoding="UTF-8"))
            break
    return forecastDICT

def getDatetime(inputSTR, timeRef=None):
    '''把 inputSTR 的時間字串轉換成時間類型並回傳'''
    if inputSTR:
        response = requests.post("https://api.droidtown.co/Articut/API/",
                                 json={"username": USERNAME,
                                       "api_key": API_KEY,
                                       "input_str": inputSTR,
                                       "version": "latest",
                                       "time_ref": timeRef,    # "2020-08-07 06:00:00"
                                       "level": "lv3",
                                      }).json()
        return response["time"][0]
    else:
        return []

def convertDatetime2ForecastFMT(datetimeSTR):
    try:
        resultDatetime = datetime.datetime.strptime(getDatetime(datetimeSTR)[0]["datetime"], datetimeFMT)
        if datetimeSTR in ["今天", "今日"]:
            resultDatetime = resultDatetime.replace(hour=12)
        return resultDatetime.strftime(datetimeFMT)
    except:
        return ""


DEBUG_Weather = True
# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Weather:
        print("[Weather]\n{} ===> {}\n".format(utterance, args))
        #print("Pattern: ", pattern)

def getResult(pattern, utterance, args, resultDICT):
    debugInfo(pattern, utterance, args)

    if utterance == "[今天][台北]熱不[熱]":
        forecastDICT = getCityForecastDict(args[1])
        queryDatetime = convertDatetime2ForecastFMT(args[0])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "Td":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        if "熱" in args[2] or "冷" in args[2]:
                            pass
                        else:
                            break
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 31:
                                resultDICT["answer"] += "平均露點溫度為攝氏 {} 度，氣溫非常悶熱，容易中暑，請盡量補充水份。\n".format(value)
                                if "熱" in args[2]:
                                    resultDICT["answer"] = "非常熱。\n" + resultDICT["answer"]
                                elif "冷" in args[2]:
                                    resultDICT["answer"] = "不會冷，但非常熱。\n" + resultDICT["answer"]
                            elif value >= 27:
                                resultDICT["answer"] += "平均露點溫度為攝氏 {} 度，氣溫較為悶熱。\n".format(value)
                            elif value >= 20:
                                resultDICT["answer"] += "平均露點溫度為攝氏 {} 度，氣溫較為舒適。\n".format(value)
                            else:
                                resultDICT["answer"] += "平均露點溫度為攝氏 {} 度，氣溫稍有寒意。\n".format(value)
                                if "熱" in args[2]:
                                    resultDICT["answer"] = "不會熱。\n" + resultDICT["answer"]
                                elif "冷" in args[2]:
                                    resultDICT["answer"] = "會冷，若要外出建議穿著外套。\n" + resultDICT["answer"]
                        except:
                            pass
                        break

    if utterance == "[今天][台北]會下雨嗎":
        forecastDICT = getCityForecastDict(args[1])
        queryDatetime = convertDatetime2ForecastFMT(args[0])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "PoP12h":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 70:
                                resultDICT["answer"] += "有 {}% 機率降雨，不建議進行戶外活動。\n".format(value)
                            else:
                                resultDICT["answer"] += "有 {}% 機率降雨，可以外出活動。\n".format(value)
                        except:
                            pass
                        break

    if utterance == "[台北][今天]可以不用帶傘嗎":
        forecastDICT = getCityForecastDict(args[0])
        queryDatetime = convertDatetime2ForecastFMT(args[1])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "PoP12h":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 50:
                                resultDICT["answer"] += "有 {}% 機率降雨，建議攜帶雨具。\n".format(value)
                            else:
                                resultDICT["answer"] += "有 {}% 機率降雨，若短時間外出可以不帶傘。\n".format(value)
                        except:
                            pass
                        break

    if utterance == "[今天][台北]可以不用帶傘嗎":
        forecastDICT = getCityForecastDict(args[1])
        queryDatetime = convertDatetime2ForecastFMT(args[0])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "PoP12h":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 50:
                                resultDICT["answer"] += "有 {}% 機率降雨，建議攜帶雨具。\n".format(value)
                            else:
                                resultDICT["answer"] += "有 {}% 機率降雨，若短時間外出可以不帶傘。\n".format(value)
                        except:
                            pass
                        break

    if utterance == "[今天][台北]需不[需]要帶傘":
        forecastDICT = getCityForecastDict(args[1])
        queryDatetime = convertDatetime2ForecastFMT(args[0])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "PoP12h":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 50:
                                resultDICT["answer"] += "有 {}% 機率降雨，建議攜帶雨具。\n".format(value)
                            else:
                                resultDICT["answer"] += "有 {}% 機率降雨，若短時間外出可以不帶傘。\n".format(value)
                        except:
                            pass
                        break

    if utterance == "[今天][台北]需不[需]要帶[陽傘]":
        # write your code here
        pass

    if utterance == "[今天][台北][中午]過[後]天氣如何":
        forecastDICT = getCityForecastDict(args[1])
        queryDatetime = convertDatetime2ForecastFMT(args[0]+args[2])
        for weatherElement in forecastDICT["weatherElement"]:
            if weatherElement["elementName"] == "WeatherDescription":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        resultDICT["answer"] = "WeatherDescription"
                        break

    if utterance == "[後天][晚上][台北]適合慢跑嗎":
        forecastDICT = getCityForecastDict(args[2])
        queryDatetime = convertDatetime2ForecastFMT(args[0]+args[1])
        for weatherElement in forecastDICT["weatherElement"]:
            #if weatherElement["elementName"] == "WeatherDescription":
                #for elementTime in weatherElement["time"]:
                    #if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        #resultDICT["WeatherDescription"] = elementTime["elementValue"][0]["value"]
                        #break
            if weatherElement["elementName"] == "UVI":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 7:
                                resultDICT["answer"] += "紫外線指數 {}，{} 曝曬級數，若要外出請注意防曬及補充水分。\n".format(value, elementTime["elementValue"][1]["value"])
                            elif value >= 5:
                                resultDICT["answer"] += "紫外線指數 {}，{} 曝曬級數，請穿戴衣帽以保護皮膚並在中午陽光強烈時尋找遮蔽處。\n".format(value, elementTime["elementValue"][1]["value"])
                            else:
                                resultDICT["answer"] += "紫外線指數 {}，{} 曝曬級數，屬弱紫外線輻射天氣，無需特別防護。若長期在戶外，建議塗擦SPF在8-12之間的防曬護膚品。\n".format(value, elementTime["elementValue"][1]["value"])
                        except:
                            pass
                        break
            if weatherElement["elementName"] == "PoP12h":
                for elementTime in weatherElement["time"]:
                    if queryDatetime >= elementTime["startTime"] and queryDatetime <= elementTime["endTime"]:
                        try:
                            value = int(elementTime["elementValue"][0]["value"])
                            if value >= 70:
                                resultDICT["answer"] += "有 {}% 機率降雨，不建議進行戶外活動。\n".format(value)
                            else:
                                resultDICT["answer"] += "有 {}% 機率降雨，可以外出活動。\n".format(value)
                        except:
                            pass
                        break

    return resultDICT