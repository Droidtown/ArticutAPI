#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki Template For Python3

    Request:
        {
            "username": "your_username",
            "input_str": "your_sentence",
            "loki_key": "your_loki_key"
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v193",
            "word_count_balance": 2000,
            "results": [
                {
                    "intent": "intentName",
                    "pattern": "matchPattern",
                    "utterance": "matchUtterance",
                    "argument": ["arg1", "arg2", ... "argN"]
                },
                ...
            ]
        }
"""

import json
import os
import requests
from intent import Loki_Exchange

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki", "")
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
    LOKI_KEY = infoDICT["loki_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""
    LOKI_KEY = ""


class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = None

    def __init__(self, input_str):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = None

        try:
            result = requests.post("https://api.droidtown.co/Loki/API/", json={
                "username": USERNAME,
                "input_str": input_str,
                "loki_key": LOKI_KEY
            })

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["results"]
            else:
                self.message = "Connect Error."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLen(self):
        rst = 0
        if self.lokiResultLIST is not None:
            rst = len(self.lokiResultLIST)

        return rst

    def getLokiResult(self, index):
        lokiResultDICT = None
        if self.lokiResultLIST is not None:
            if index < self.getLen():
                lokiResultDICT = self.lokiResultLIST[index]

        return lokiResultDICT

    def getIntent(self, index):
        rst = ""
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["intent"]

        return rst

    def getPattern(self, index):
        rst = ""
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["pattern"]

        return rst

    def getUtterance(self, index):
        rst = ""
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["utterance"]

        return rst

    def getArgs(self, index):
        rst = []
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["argument"]

        return rst

#建立貨幣名稱代碼轉換字典
currencyCodeDICT = {"美金":"USD", "美元":"USD", "日幣":"JPY", "日圓":"JPY", "日元":"JPY",
                    "台幣":"TWD", "臺幣":"TWD", "新台幣":"TWD", "新臺幣":"TWD", "歐元":"EUR"}

#建立貨幣匯率字典
currencyExRateDICT = {}

def getCurrencyExRate():
    '''取得最新匯率，並儲存到 currencyExRateDICT'''
    global currencyExRateDICT
    currencyExRateDICT = requests.get("https://tw.rter.info/capi.php").json()

def getSrc2TgtCurrencyExRate(sourceCurrencySTR, targetCurrencySTR):
    '''依 currencyExRateDICT 的內容，將 sourceCurrencySTR 和 targetCurrencySTR 兩種貨幣之間的匯率取出並回傳'''
    if sourceCurrencySTR == None:
        sourceCurrencyCode = "TWD"
    else:
        sourceCurrencyCode = currencyCodeDICT[sourceCurrencySTR]

    if targetCurrencySTR == None:
        targetCurrencyCode = "TWD"
    else:
        targetCurrencyCode = currencyCodeDICT[targetCurrencySTR]
    #print(sourceCurrencyCode, targetCurrencyCode)
    exRate = (1 / currencyExRateDICT["USD{}".format(sourceCurrencyCode)]["Exrate"]) * (currencyExRateDICT["USD{}".format(targetCurrencyCode)]["Exrate"])
    return exRate

def amountSTRconvert(amountSTR):
    '''把 amountSTR 的金額數字字串轉為數值類型並回傳'''
    if amountSTR:
        response = requests.post("https://api.droidtown.co/Articut/API/",
                                  json={"username": USERNAME,
                                        "api_key": API_KEY,
                                        "input_str": amountSTR,
                                        "version": "latest",
                                        "level": "lv3",
                                        }).json()
        return response["number"][amountSTR]
    else:
        return 1

def runLoki(input_str):
    resultDICT = {}
    lokiRst = LokiResult(input_str)
    if lokiRst.getStatus():
        for i in range(0, lokiRst.getLen()):
            # Exchange
            if lokiRst.getIntent(i) == "Exchange":
                resultDICT = Loki_Exchange.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), resultDICT)
        getCurrencyExRate()
        # 兌換數字 * 貨幣轉換匯率
        resultDICT["answer"] = amountSTRconvert(resultDICT["amount"]) * getSrc2TgtCurrencyExRate(resultDICT["source"], resultDICT["target"])
    else:
        resultDICT = {"msg": lokiRst.getMessage()}

    return resultDICT

if __name__ == "__main__":
    input_str = "100台幣換美金"
    resultDICT = runLoki(input_str)
    print(resultDICT)
    print("需要 {} 元".format(resultDICT["answer"]))