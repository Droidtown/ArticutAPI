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

import requests
from intent import Loki_GetVenueAddress

#USERNAME 為你的 Droidtown 帳號 email；LOKI_KEY 為此 Loki 專案的 KEY (需登入 Loki 管理頁面才看得到)
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
    lokiRst = LokiResult(input_str)
    if lokiRst.getStatus():
        for i in range(0, lokiRst.getLen()):
            # GetVenueAddress
            if lokiRst.getIntent(i) == "GetVenueAddress":
                resultDICT = Loki_GetVenueAddress.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}

    return resultDICT

if __name__ == "__main__":
    input_str = "Sprint辦在哪裡"
    resultDICT = runLoki(input_str)
    print("Result => {}".format(resultDICT))