#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for TV
    
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

tvDICT = {"entity": ["電視", "TV", "音量", "聲音"],
          "modifier": ["大聲", "小聲", "靜音", "(?<!不)大", "(?<!不)小"],
          "filter": ["上", "下", "前", "後", "第", "台", "臺"]}

modifierPat = re.compile("({}|不夠|不足)$".format("|".join(tvDICT["modifier"])))
filterPat = re.compile("[{}]".format("".join(tvDICT["filter"])))

DEBUG_TV = True
userDefinedDICT = {}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_TV:
        print("[TV] {} ===> {}\n{}\n".format(utterance, args, pattern))

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

def getVolume(inputSTR, resultDICT):
    """從字串轉成音量值"""
    m = [x.group() for x in modifierPat.finditer(inputSTR)]
    volume = 0
    if m:
        if "大" in m[0]:
            volume = 2
        elif "小" in m[0]:
            volume = -2
        if [True for x in ["太", "很", "好"] if x in inputSTR]:
            volume *= -3
        resultDICT["set_volume"] = volume
    return resultDICT

def getChannel(inputSTR, resultDICT):
    """從字串轉成頻道"""
    numberSTR = filterPat.sub("", inputSTR)
    number = getNumberFromLv3(numberSTR)
    determiner = inputSTR[:inputSTR.find(numberSTR)]
    if number:
        if determiner in ["下", "後"]:
            resultDICT["set_channel"] = number
        elif determiner in ["上", "前"]:
            resultDICT["set_channel"] = -number
        elif determiner == "第" or determiner == "":
            resultDICT["channel"] = number
    return resultDICT

def getResult(pattern, utterance, args, resultDICT, input_str):
    debugInfo(pattern, utterance, args)
    if utterance == "回[上一台]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance in ["有[點]吵", "有[些]吵"]:
        resultDICT["set_volume"] = -2

    if utterance == "調[大聲]":
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance in ["調[大聲][一點]", "調[大聲][一些]"]:
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance == "轉[大聲]":
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance in ["轉[大聲][一點]", "轉[大聲][一些]"]:
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance == "轉到[第50台]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "轉到[50台]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "開聲音":
        resultDICT["volume"] = 10

    if utterance == "開電視":
        resultDICT["tv"] = True

    if utterance == "開[大聲]":
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance == ["開[大聲][一點]", "開[大聲][一些]"]:
        if args[0] in tvDICT["modifier"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance == "關聲音":
        resultDICT["volume"] = 0

    if utterance == "關電視":
        resultDICT["tv"] = False

    if utterance == "關[小聲]":
        if "小" in args[0]:
            resultDICT["set_volume"] = -2

    if utterance in ["關[小聲][一點]", "關[小聲][一些]"]:
        if "小" in args[0]:
            resultDICT["set_volume"] = -2

    if utterance == "把[電視]打開":
        if args[0] in tvDICT["entity"]:
            if "音" in args[0]:
                resultDICT["volume"] = 10
            else:
                resultDICT["tv"] = True

    if utterance == "把[電視]關掉":
        if args[0] in tvDICT["entity"]:
            if "音" in args[0]:
                resultDICT["volume"] = 0
            else:
                resultDICT["tv"] = False

    if utterance == "[第50台]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "[音量]調[30]":
        if args[0] in tvDICT["entity"]:
            if "音" in args[0]:
                resultDICT["volume"] = getNumberFromLv3(args[1])

    if utterance == "[電視]調[大聲]":
        if args[0] in tvDICT["entity"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[電視]轉[大聲]":
        if args[0] in tvDICT["entity"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[電視]開[大聲]":
        if args[0] in tvDICT["entity"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[電視]關[小聲]":
        if args[0] in tvDICT["entity"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[電視][太大聲]":
        if args[0] in tvDICT["entity"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[電視]好吵":
        resultDICT["volume"] = 0

    if utterance == "[聲音][不夠][大聲]":
        if args[0] in ["聲音", "音量"]:
            if args[1] == "不夠":
                resultDICT = getVolume(args[2], resultDICT)

    if utterance == "頻道[50]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "[上一台]":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "不想看[第50台]":
        resultDICT["set_channel"] = 1

    if utterance == "不想看這一台":
        resultDICT["set_channel"] = 1

    if utterance == "[靜音]":
        if args[0] in ["靜音"]:
            resultDICT["volume"] = 0
        elif args[0] in ["大聲", "小聲"]:
            resultDICT = getVolume(args[0], resultDICT)

    if utterance == "[第50]頻道":
        resultDICT = getChannel(args[0], resultDICT)

    if utterance == "不要開[電視]":
        if args[0] in ["電視", "電視機", "TV"]:
            resultDICT["tv"] = False
        if args[0] in ["音量", "聲音"]:
            resultDICT["volume"] = 0

    if utterance == "不要關[電視]":
        if args[0] in ["電視", "電視機", "TV"]:
            resultDICT["tv"] = True
        if args[0] in ["音量", "聲音"]:
            resultDICT["volume"] = 10

    if utterance in ["[音量][小聲][一點]", "[音量][小聲][一些]"]:
        if args[0] in t["音量", "聲音"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance in ["[音量]調[小][一些]", "[音量]調[小][一點]"]:
        if args[0] in ["音量", "聲音"]:
            resultDICT = getVolume(args[1], resultDICT)

    if utterance == "[我]想要看[電視]":
        if args[1] in ["電視", "電視機", "TV"]:
            resultDICT["tv"] = True

    if utterance == "[電視]打開":
        if args[0] in ["電視", "電視機", "TV"]:
            resultDICT["tv"] = True

    if utterance == "[電視]關掉":
        if args[0] in ["電視", "電視機", "TV"]:
            resultDICT["tv"] = False

    if utterance in ["[我]聽不見", "[我]聽不到"]:
        resultDICT["set_volume"] = 2

    if utterance == "[我]聽不[清楚]":
        if args[1] in ["清楚"]:
            resultDICT["set_volume"] = 2

    if utterance == "轉台":
        resultDICT["set_channel"] = 1

    if utterance == "不要[靜音]":
        if args[0] in ["靜音"]:
            resultDICT["volume"] = 10

    if utterance == "不要[太大聲]":
        resultDICT = getVolume(args[0], resultDICT)

    return resultDICT