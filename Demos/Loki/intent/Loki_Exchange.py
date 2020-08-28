#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Exchange

    Input:
        pattern       str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Exchange = True

#建立貨幣名稱代碼轉換字典
currencyCodeDICT = {"美金":"USD", "美元":"USD", "日幣":"JPY", "日圓":"JPY", "日元":"JPY",
                    "台幣":"TWD", "臺幣":"TWD", "新台幣":"TWD", "新臺幣":"TWD", "歐元":"EUR"}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Exchange:
        print("[Exchange]\n{} ===> {}\n{}\n".format(utterance, args, pattern))

def getResult(pattern, utterance, args, resultDICT):
    debugInfo(pattern, utterance, args)

    if utterance == "[我]想要[美金][100元]":
        resultDICT["source"] = args[1]
        resultDICT["target"] = None
        resultDICT["amount"] = args[2]

    if utterance == "[我]想要[100元][美金]":
        resultDICT["source"] = args[2]
        resultDICT["target"] = None
        resultDICT["amount"] = args[1]

    if utterance == "[我]想買[美金][100元]":
        resultDICT["source"] = args[1]
        resultDICT["target"] = None
        resultDICT["amount"] = args[2]

    if utterance == "[我]想買[100元][美金]":
        resultDICT["source"] = args[2]
        resultDICT["target"] = None
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100]要多少[台幣]":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100]要[台幣]多少":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100元]要多少[台幣]":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100元]要[台幣]多少":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100元]可以兌換多少[台幣]":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[美金][100元]可以兌換[台幣]多少":
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    if utterance == "[100美金]要多少[台幣]":
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    if utterance == "[100美金]要[台幣]多少":
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    if utterance == "[100美金]能換多少[台幣]":
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    if utterance == "[100元][美金]要多少[台幣]":
        debugInfo("[100元][美金]要多少[台幣]", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    if utterance == "[100元][美金]要[台幣]多少":
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    if utterance == "[100元][美金]可以兌換多少[台幣]":
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    if utterance == "[100元][美金]可以兌換[台幣]多少":
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    if utterance == "[100台幣]換[美金]":
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    if utterance == "[今天][美金]兌換[台幣]是多少":
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = None

    if utterance == "[上星期三][美金]兌換[台幣]是多少":
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = None

    return resultDICT