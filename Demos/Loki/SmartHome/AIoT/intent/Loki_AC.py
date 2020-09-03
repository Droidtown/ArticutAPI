#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for AC
    
    Input:
        pattern       str,
        utterance     str,
        args          str[],
        resultDICT    dict
    
    Output:
        resultDICT    dict
"""

import os
import re
from requests import post

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki/SmartHome/intent", "")
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""

acDICT = {"entity": ["冷氣", "溫度", "室溫", "空調", "風量", "風"],
          "modifier": ["冷", "熱", "強", "弱", "小", "大", "高", "低"],
          "unit": ["小時", "時", "度"]}

modifierPat = re.compile("((?<!不)[{}]|不夠|不足)$".format("".join(acDICT["modifier"])))
unitPat = re.compile("({})$".format("|".join(acDICT["unit"])))

DEBUG_AC = True
userDefinedDICT = {'舒眠': ['']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_AC:
        print("[AC] {} ===> {}\n{}\n".format(utterance, args, pattern))

def getNumberFromLv3(inputSTR):
    """將字串型態的數字轉換成數字型態"""
    url = "https://api.droidtown.co/Articut/API/"
    payload = {
        "username": USERNAME,
        "api_key": API_KEY,
        "input_str": inputSTR,
        "level": "lv3"
    }
    try:
        response = post(url, json=payload).json()
        if response["status"]:
            return response["number"][inputSTR]
    except:
        pass
    return None

def getNumber(inputSTR):
    """將數字的單位移除，並轉換成數字型態"""
    numberSTR = unitPat.sub("", inputSTR)
    number = getNumberFromLv3(numberSTR)
    return number

def getTime(inputSTR):
    """取得 x 小時的時間 (number/HR)，並轉成數字型態回傳"""
    number = getNumber(inputSTR)
    if "時" in inputSTR:
        return number
    elif "分" in inputSTR:
        return round(number / 60, 2)
    else:
        return 0

def getFanSpeed(inputSTR):
    """從字串轉成風速值"""
    m = [x.group() for x in modifierPat.finditer(inputSTR)]
    speed = 0
    if m:
        if m[0] in ["強", "大", "高"]:
            speed = 1
        elif m[0] in ["弱", "小", "低"]:
            speed = -1
        if [True for x in ["太", "很", "好"] if x in inputSTR]:
            speed *= -2
    return speed

def getTemperature(inputSTR):
    """從字串轉成溫度的調整值"""
    m = [x.group() for x in modifierPat.finditer(inputSTR)]
    temp = 0
    if m:
        if m[0] in ["冷", "強", "大", "低"]:
            temp = -1
        elif m[0] in ["熱", "弱", "小", "高"]:
            temp = 1
        if [True for x in ["太", "很", "好"] if x in inputSTR]:
            temp *= -2
    return temp


def getResult(pattern, utterance, args, resultDICT, input_str):
    debugInfo(pattern, utterance, args)
    if utterance == "升[一度]":
        resultDICT["set_temperature"] = getNumber(args[0])

    if utterance == "定時[1小時]":
        resultDICT["time"] = getTime(args[0])

    if utterance == "定時[1小時]關":
        resultDICT["time"] = getTime(args[0])

    if utterance == "定時[1小時][後]開":
        # write your code here
        pass

    if utterance == "定時[1小時][後]關":
        resultDICT["time"] = getTime(args[0])

    if utterance == "覺得有[點][冷]":
        temp = -getTemperature(args[1])
        if temp != 0:
            resultDICT["set_temperature"] = temp

    if utterance == "調高[一度]":
        resultDICT["set_temperature"] = getNumber(args[0])

    if utterance == "開冷氣":
        resultDICT["ac"] = True

    if utterance == "關冷氣":
        resultDICT["ac"] = False

    if utterance == "降[一度]":
        resultDICT["set_temperature"] = -getNumber(args[0])

    if utterance == "預約[1小時]":
        resultDICT["time"] = getTime(args[0])

    if utterance == "預約[1小時]關":
        resultDICT["time"] = getTime(args[0])

    if utterance == "預約[1小時][後]開":
        # write your code here
        pass

    if utterance == "預約[1小時][後]關":
        resultDICT["time"] = getTime(args[0])

    if utterance in ["[溫度]升高[一點]", "[溫度]升高[一些]"]:
        if "風" in args[0]:
            resultDICT["set_fan_speed"] = 1
        elif args[0] in acDICT["entity"]:
            resultDICT["set_temperature"] = 1

    if utterance == "[冷氣]調[太強]":
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[冷氣]調[強][一點]", "[冷氣]調[強][一些]"]:
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[溫度]調高[一點]", "[溫度]調高[一些]"]:
        if "風" in args[0]:
            resultDICT["set_fan_speed"] = 1
        elif args[0] in acDICT["entity"]:
            resultDICT["set_temperature"] = 1

    if utterance == "[冷氣]轉[太強]":
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[冷氣]轉[強][一點]", "[冷氣]轉[強][一些]"]:
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[溫度]轉高[一點]", "[溫度]轉高[一些]"]:
        if "風" in args[0]:
            resultDICT["set_fan_speed"] = 1
        elif args[0] in acDICT["entity"]:
            resultDICT["set_temperature"] = 1

    if utterance == "[冷氣]開[太強]":
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[冷氣]開[強][一點]", "[冷氣]開[強][一些]"]:
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[冷氣]關[小][一點]", "[冷氣]關[小][一些]"]:
        if args[1] == "小":
            if "風" in args[0]:
                resultDICT["set_fan_speed"] = 1
            elif args[0] in acDICT["entity"]:
                resultDICT["set_temperature"] = 1

    if utterance in ["[溫度]降低[一點]", "[溫度]降低[一些]"]:
        if "風" in args[0]:
            resultDICT["set_fan_speed"] = -1
        elif args[0] in acDICT["entity"]:
            resultDICT["set_temperature"] = -1

    if utterance == "[溫度][太高]":
        if "風" in args[0]:
            fan_speed = getFanSpeed(args[1])
            if fan_speed != 0:
                resultDICT["set_fan_speed"] = fan_speed
        elif args[0] in acDICT["entity"]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp
        else:
            if [True for x in ["冷", "熱"] if x in args[1]]:
                temp = getTemperature(args[1])
                if temp != 0:
                    resultDICT["set_temperature"] = temp

    if utterance == "[溫度][不夠][低]":
        if args[1] == "不夠":
            if "風" in args[0]:
                fan_speed = getFanSpeed(args[2])
                if fan_speed != 0:
                    resultDICT["set_fan_speed"] = fan_speed
            elif args[0] in acDICT["entity"]:
                temp = getTemperature(args[2])
                if temp != 0:
                    resultDICT["set_temperature"] = temp

    if utterance in ["我有[點][冷]", "我有[些][冷]"]:
        if [True for x in ["太", "很", "好"] if x in args[1]]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp
        else:
            temp = -getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance == "[溫度]調到[20度]":
        if args[0] in acDICT["entity"]:
            resultDICT["temperature"] = getNumber(args[1])

    if utterance == "溫度[20度]":
        resultDICT["temperature"] = getNumber(args[0])

    if utterance == "舒眠[1小時]":
        resultDICT["time"] = getTime(args[0])

    if utterance in ["好像有[一點][冷]", "好像有[一些][冷]"]:
        if [True for x in ["太", "很", "好"] if x in args[1]]:
            temp = getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp
        else:
            temp = -getTemperature(args[1])
            if temp != 0:
                resultDICT["set_temperature"] = temp

    if utterance in ["[我]想要吹[冷氣]", "[我]想要開[冷氣]"]:
        if args[1] in ["冷氣", "冷氣機", "空調"]:
            resultDICT["ac"] = True

    if utterance == "[冷氣]打開":
        if args[0] in ["冷氣", "冷氣機", "空調"]:
            resultDICT["tv"] = True

    if utterance == "[冷氣]關掉":
        if args[0] in ["冷氣", "冷氣機", "空調"]:
            resultDICT["tv"] = False

    if utterance == "[這裡][好冷]":
        if args[0] in ["這裡", "那裡"]:
            if [True for x in ["太", "很", "好"] if x in args[1]]:
                temp = getTemperature(args[1])
                if temp != 0:
                    resultDICT["set_temperature"] = temp
            else:
                temp = -getTemperature(args[1])
                if temp != 0:
                    resultDICT["set_temperature"] = temp

    return resultDICT