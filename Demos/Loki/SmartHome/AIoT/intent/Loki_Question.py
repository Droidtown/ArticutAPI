#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Question
    
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

DEBUG_Question = True
userDefinedDICT = {"TV": ["八點檔", "電視", "電影", "新聞", "卡通", "美劇", "韓劇", "日劇", "台劇", "偶像劇", "兒童台", "幼幼台"]}

entityDICT = {
    "action": "燈",
    "ac": ["冷氣", "冷氣機", "空調"],
    "tv": ["電視", "電視機", "TV"]
}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Question:
        print("[Question] {} ===> {}\n{}".format(utterance, args, pattern))

def getResult(pattern, utterance, args, resultDICT, input_str):
    debugInfo(pattern, utterance, args)
    if utterance == "忘記關[冷氣]":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "--"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance == "忘記關燈":
        resultDICT["question_action"] = "--"

    if utterance == "[燈]忘記開":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "++"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = True
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = True

    if utterance == "[燈]忘記關":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "--"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance == "[燈]忘記開":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "++"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = True
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = True

    if utterance == "沒關[冷氣]":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "--"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance == "[好像]忘記關燈":
        if args[0] in ["好像"]:
            resultDICT["question_action"] = "--"

    if utterance == "[好像]忘記開燈":
        if args[0] in ["好像"]:
            resultDICT["question_action"] = "++"

    if utterance == "[燈][好像]忘記關":
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "--"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance in ["[好像]忘記關[冷氣]", "[好像]沒關[冷氣]"]:
        if entityDICT["action"] in args[1]:
            resultDICT["question_action"] = "--"
        if args[1] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[1] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance in ["忘記開[冷氣]", "沒開[冷氣]", "[燈][好像]忘記開"]:
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "++"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = True
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = True

    if utterance in ["[好像]忘記開[冷氣]", "[好像]沒開[冷氣]"]:
        if entityDICT["action"] in args[1]:
            resultDICT["question_action"] = "++"
        if args[1] in entityDICT["ac"]:
            resultDICT["question_ac"] = True
        if args[1] in entityDICT["tv"]:
            resultDICT["question_tv"] = True

    if utterance in ["[燈][好像]忘記開", "[冷氣][好像]沒開"]:
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "++"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = True
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = True

    if utterance in ["[燈][好像]忘記關", "[冷氣][好像]沒關"]:
        if entityDICT["action"] in args[0]:
            resultDICT["question_action"] = "--"
        if args[0] in entityDICT["ac"]:
            resultDICT["question_ac"] = False
        if args[0] in entityDICT["tv"]:
            resultDICT["question_tv"] = False

    if utterance == "[我]想看[卡通]":
        if args[1] in userDefinedDICT["TV"]:
            resultDICT["question_tv"] = True

    if utterance in ["有[卡通]可以看嗎", "可以看[卡通]嗎", "有什麼[卡通]可以看嗎"]:
        if args[0] in userDefinedDICT["TV"]:
            resultDICT["question_tv"] = True

    return resultDICT