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

import json
import os
import re
import requests
from intent import Loki_Question
from intent import Loki_Calculation_Comparison
from intent import Loki_Calculation_Addition
from intent import Loki_Definition
from pprint import pprint

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__)))
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

###############################################################################################
punctuationPat = re.compile("[，。；,;？]")

def runLoki(inputSTR):
    questionDICT = {"Definition": {},
                    "Calculation": {},
                    "Entity": {},
                    "Memory": {},
                    "Process": [],
                    "Question": []}

    inputLIST = list(filter(None, punctuationPat.sub("\n", inputSTR).split("\n")))
    print("[Input_list]\n{}\n".format(inputLIST))

    for u in inputLIST:
        lokiRst = LokiResult(u)
        if lokiRst.getStatus():
            # HINT: 以下這些 lokiRst.getResult(i) 都是在 Loki 的網頁中自動幫你生成的。
            # 每個 lokiRst.getPattern(i) 的上方還會出現一行「註解起來」的中文句子。那是用來
            # 表示那段正規表示式是在描述哪一種句型。比如說『剩下幾[個]』這段，就在表示其後的正規
            # 表示式是用來抓「剩下幾個」中的「個」。
            for i in range(0, lokiRst.getLen()):
                # Question
                if lokiRst.getIntent(i) == "Question":
                    questionDICT = Loki_Question.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), u, questionDICT)

                # Calculation_Comparison
                if lokiRst.getIntent(i) == "Calculation_Comparison":
                    questionDICT = Loki_Calculation_Comparison.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), u, questionDICT)

                # Calculation_Addition
                if lokiRst.getIntent(i) == "Calculation_Addition":
                    questionDICT = Loki_Calculation_Addition.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), u, questionDICT)

                # Definition
                if lokiRst.getIntent(i) == "Definition":
                    questionDICT = Loki_Definition.getResult(lokiRst.getPattern(i), lokiRst.getUtterance(i), lokiRst.getArgs(i), u, questionDICT)

        else:
            pass
            #questionDICT = {"msg": lokiRst.getMessage()}

    return questionDICT

if __name__ == "__main__":
    # HINT: 測試段落。
    input_str = "小毛有10架紙飛機，小毛比大毛多摺7架紙飛機，總共有幾架紙飛機"
    resultDICT = runLoki(input_str)
    print("Result ===>")
    pprint(resultDICT)