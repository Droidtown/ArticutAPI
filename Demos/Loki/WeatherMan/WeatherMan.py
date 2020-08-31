#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki Template For Python3

    Request:
        {
            "username": "your_username",
            "input_str": "your_input",
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

import rapidjson as json
import os
import requests
from intent import Loki_Weather

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__))).replace("/Demos/Loki/WeatherMan", "")
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    LOKI_KEY = infoDICT["weather_loki_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
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

def runLoki(input_str):
    resultDICT = {}

    #視需要做些正規化的操作 (例如「台/臺」或是 "11:30" 變為「十一點三十」)
    lokiRst = LokiResult(input_str.replace("台", "臺"))
    if lokiRst.getStatus():
        resultDICT = {"answer": ""}
        for i in range(0, lokiRst.getLen()):
            # Weather
            if lokiRst.getIntent(i) == "Weather":
                resultDICT = Loki_Weather.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), resultDICT)
    else:
        resultDICT = {"msg": lokiRst.getMessage()}

    return resultDICT

if __name__ == "__main__":
    #input_str = "後天早上台北適合慢跑嗎"
    input_str = "明天台北可以不用帶傘嗎"
    print("Input:", input_str)
    resultDICT = runLoki(input_str)
    if "answer" in resultDICT:
        print("Output:", resultDICT["answer"])
    else:
        print("Error:", resultDICT["msg"])
