#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Light
    
    Input:
        pattern       str,
        utterance     str,
        args          str[],
        resultDICT    dict
    
    Output:
        resultDICT    dict
"""

import os

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki/SmartHome/intent", "")
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""

lightDICT = {"entity": ["發光二極體", "LED", "房間燈", "電燈", "燈光", "亮度", "光線", "房間", "客房", "書房", "臥房", "臥室", "客廳", "廁所", "餐廳", "廚房", "陽台", "燈"],
             "brighten": ["亮", "高"],
             "darken":["暗", "黑", "低"]}

DEBUG_Light = True
userDefinedDICT = {'發光二極體': [''], '伸手不見五指': ['']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Light:
        print("[Light] {} ===> {}\n{}\n".format(utterance, args, pattern))

def optionInterpreter(inputSTR):
    '''
    詮釋究竟要如何調整燈光：
    + : 調亮一度
    ++: 全亮
    - : 調暗一度
    --: 全暗
    '''
    if set(inputSTR).intersection(lightDICT["brighten"]):
        if "全" in inputSTR:
            result = "++"
        else:
            result = "+"
    elif set(inputSTR).intersection(lightDICT["darken"]):
        if "全" in inputSTR:
            result = "--"
        else:
            result = "-"
    else:
        result = ""
    return result

def getResult(pattern, utterance, args, resultDICT, input_str):
    debugInfo(pattern, utterance, args)
    if utterance in ["調[亮][一點]", "調[亮][一些]"]:
        if args[1] in ["一點", "一些"]:
            action = optionInterpreter(args[0])
            if action:
                resultDICT["action"] = action

    if utterance == "開燈":
        resultDICT["action"] = "++"

    if utterance == "關燈":
        resultDICT["action"] = "--"

    if utterance in ["把[燈]調[亮][一點]", "把[燈]調[亮][一些]"]:
        if args[0] in lightDICT["entity"]:
            action = optionInterpreter(args[1])
            if action:
                resultDICT["action"] = action

    if utterance == "[燈]打開":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "++"

    if utterance == "[我]看不見":
        if args[0] in lightDICT["entity"] or args[0] in "你我他":
            resultDICT["action"] = "++"

    if utterance in ["[燈光]調[暗][一點]", "[燈光]調[暗][一些]"]:
        if args[0] in lightDICT["entity"]:
            action = optionInterpreter(args[1])
            if action:
                resultDICT["action"] = action

    if utterance in ["[亮度]調高[一點]" , "[亮度]調高[一些]"]:
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "+"

    if utterance in ["[燈]開[亮][一點]", "[燈]開[亮][一些]"]:
        if args[0] in lightDICT["entity"]:
            action = optionInterpreter(args[1])
            if action:
                resultDICT["action"] = action

    if utterance == "[燈]關掉":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "--"

    if utterance == "[亮度][不夠]":
        if args[0] in lightDICT["entity"] and args[1] in ["不足", "不夠"]:
            resultDICT["action"] = "+"

    if utterance == "[燈光][不夠][亮]":
        if args[0] in lightDICT["entity"]:
            action = optionInterpreter(args[2])
            if action:
                resultDICT["action"] = action

    if utterance == "[燈][全]開":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "++"

    if utterance == "[燈][全]關":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "--"

    if utterance == "伸手不見五指":
        resultDICT["action"] = "++"

    if utterance == "好刺眼":
        resultDICT["action"] = "-"

    if utterance == "[太]刺眼":
        resultDICT["action"] = "-"

    if utterance in ["[再亮][一點]", "[再亮][一些]"]:
        action = optionInterpreter(args[0])
        if action:
            resultDICT["action"] = action

    if utterance == "[全][亮]":
        action = optionInterpreter(args[0]+args[1])
        if action:
            resultDICT["action"] = action

    if utterance in ["有[點][亮]", "有[些][亮]"]:
        if args[1] in lightDICT["brighten"]:
            resultDICT["action"] = "-"
        if args[1] in lightDICT["darken"]:
            resultDICT["action"] = "+"

    if utterance == "[太亮]了":
        if "非常" in args[0]:
            if "亮" in args[0]:
                resultDICT["action"] = "--"
            if "暗" in args[0]:
                resultDICT["action"] = "++"
        else:
            if "亮" in args[0]:
                resultDICT["action"] = "-"
            if "暗" in args[0]:
                resultDICT["action"] = "+"

    if utterance == "[房間燈]好像沒關":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "--"

    if utterance == "沒關[房間燈]":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "--"

    if utterance == "[房間燈]沒關":
        if args[0] in lightDICT["entity"]:
            if "沒" in input_str:
                resultDICT["action"] = "--"
            elif [True for x in ["別", "不"] if x in input_str]:
                resultDICT["action"] = "++"

    if utterance == "[房間燈]別開":
        if args[0] in lightDICT["entity"]:
            if "沒" in input_str:
                resultDICT["action"] = "++"
            elif [True for x in ["別", "不"] if x in input_str]:
                resultDICT["action"] = "--"

    if utterance == "[我]看不到":
        resultDICT["action"] = "++"

    if utterance == "不要關燈":
        resultDICT["action"] = "++"

    if utterance == "不要開燈":
        resultDICT["action"] = "--"

    if utterance == "開[電燈]":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "++"

    if utterance == "關[電燈]":
        if args[0] in lightDICT["entity"]:
            resultDICT["action"] = "--"

    if utterance == "[我]想要看[書]":
        if "書" in args[1]:
            resultDICT["action"] = "++"

    return resultDICT