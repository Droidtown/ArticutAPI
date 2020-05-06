#!/usr/bin/env python3
# -*- coding:utf-8 -*-




"""
    Loki Template For Python3

    Request:
        {
            "username": "your_username",
            "api_key": "your_articut_key",
            "input_str": "your_sentence",
            "version": "latest", # Articut Version
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
                    "argument": ["arg1", "arg2", ... "argN"]
                },
                ...
            ]
        }
"""

import requests

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
                "username": "your_account@your_domain",
                "api_key": "your_articut_api_key",
                "input_str": input_str,
                "version": "latest",
                "loki_key": "your_loki_project_key"
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
                lokiResultDICT = self.lokiResultLIST[i]

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

    def getArgs(self, index):
        rst = []
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["argument"]

        return rst

def doSomethingAbout(args):
    '''將符合句型的參數列表印出'''
    print(args)

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
    print(sourceCurrencyCode, targetCurrencyCode)
    exRate = (1/currencyExRateDICT["USD{}".format(sourceCurrencyCode)]["Exrate"])*(currencyExRateDICT["USD{}".format(targetCurrencyCode)]["Exrate"])
    return exRate

def amountSTRconvert(amountSTR):
    '''把 amountSTR 的金額數字字串轉為數值類型並回傳'''
    response = requests.post("https://api.droidtown.co/Articut/API/",
                              json={"username": "your_email@your_domain",
                                    "api_key": "your_articut_api_key",
                                    "input_str": amountSTR,
                                    "version": "latest",
                                    "level": "lv3",
                                    }).json()
    return response["number"][amountSTR]

if __name__== "__main__":
    input_str = "我實在很想換真正的100元美金"
    lokiRst = LokiResult(input_str)

    for i in range(0, lokiRst.getLen()):
        # <換匯>
        if lokiRst.getIntent(i) == "換匯":
            # 我想要[100元][美金]
            if lokiRst.getPattern(i) == "(<ENTITY_pronoun>[^<]*?</ENTITY_pronoun>)?((<ACTION_verb>[^<不]*?[想要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想要][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = None
                amountSTR = lokiRst.getArgs(i)[0]
            # 我想要[美金][100元]
            if lokiRst.getPattern(i) == "(<ENTITY_pronoun>[^<]*?</ENTITY_pronoun>)?((<ACTION_verb>[^<不]*?[想要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = None
                amountSTR = lokiRst.getArgs(i)[1]
            # 我想買[100元][美金]
            if lokiRst.getPattern(i) == "(<ENTITY_pronoun>[^<]*?</ENTITY_pronoun>)?((<ACTION_verb>[^<不]*?[想買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想買][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = None
                amountSTR = lokiRst.getArgs(i)[0]
            # 我想買[美金][100元]
            if lokiRst.getPattern(i) == "(<ENTITY_pronoun>[^<]*?</ENTITY_pronoun>)?((<ACTION_verb>[^<不]*?[想買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = None
                amountSTR = lokiRst.getArgs(i)[1]
            # [100美金]要[台幣]多少
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = [code for code in currencyCodeDICT.keys() if code in lokiRst.getArgs(i)[1]][0]
                targetCurrencySTR = lokiRst.getArgs(i)[1]
                amountSTR = lokiRst.getArgs(i)[0]
            # [100美金]要多少[台幣]
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = [code for code in currencyCodeDICT.keys() if code in lokiRst.getArgs(i)[1]][0]
                targetCurrencySTR = lokiRst.getArgs(i)[1]
                amountSTR = lokiRst.getArgs(i)[0]
            # [美金][100]要[台幣]多少
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [美金][100]要多少[台幣]
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [100元][美金]要[台幣]多少
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[0]
            # [100元][美金]要多少[台幣]
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[0]
            # [美金][100元]要[台幣]多少
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [美金][100元]要多少[台幣]
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [今天][美金]兌換[台幣]是多少
            if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = "1元"
            # [100元][美金]可以兌換[台幣]多少
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[0]
            # [100元][美金]可以兌換多少[台幣]
            if lokiRst.getPattern(i) == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[1]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[0]
            # [美金][100元]可以兌換[台幣]多少
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [美金][100元]可以兌換多少[台幣]
            if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                doSomethingAbout(lokiRst.getArgs(i))
                sourceCurrencySTR = lokiRst.getArgs(i)[0]
                targetCurrencySTR = lokiRst.getArgs(i)[2]
                amountSTR = lokiRst.getArgs(i)[1]
            # [上星期三][美金]兌換[台幣]是多少
            if lokiRst.getPattern(i) == "<TIME_week>[^<]*?</TIME_week><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                doSomethingAbout(lokiRst.getArgs(i))
        # </換匯>
        getCurrencyExRate()
        #answer = 兌換數字 * 貨幣轉換匯率
        answer = amountSTRconvert(amountSTR) * getSrc2TgtCurrencyExRate(sourceCurrencySTR, targetCurrencySTR)
        print("需要{}元".format(answer))
