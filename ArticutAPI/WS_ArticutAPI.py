#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import time

try:
    import rapidjson as json
except:
    import json

try:
    import requests
except Exception as e:
    import platform
    if "windows" in platform.system().lower():
        print("""
        Module, \"requests\" is not installed.
        If you don't know how to install "requests" under Windows,
        please use our request_installer.py in "Windows_Module_Installer" folder.
        """)
    else:
        print(e)

from pprint import pprint
from websocket import enableTrace, create_connection

try:
    from Toolkit.analyse import AnalyseManager
    from Toolkit.localRE import TaiwanAddressAnalizer
    from Toolkit.toolkits import *
except: #供外部載入時使用。
    from .Toolkit.analyse import AnalyseManager
    from .Toolkit.localRE import TaiwanAddressAnalizer
    from .Toolkit.toolkits import *


class WS_Articut:
    def __init__(self, url="ws://127.0.0.1", port="8964", bulkSize=20, userDefinedDictFILE=None):
        self.port = port
        if "ws" in url:
            self.ws_url = "{}:{}/Articut/WebSocket".format(url, port)
            self.url = "{}:{}".format(url.replace("ws", "http"), port)
        elif "http" in url:
            self.ws_url = "{}:{}/Articut/WebSocket".format(url.replace("http", "ws"), port)
            self.url = "{}:{}".format(url, port)
        else:
            self.ws_url = "ws://{}:{}/Articut/WebSocket".format(url, port)
            self.url = "http://{}:{}".format(url, port)
        #enableTrace(True)
        self.ws = create_connection("{}/API/".format(self.ws_url))
        self.ws_bulk = create_connection("{}/BulkAPI/".format(self.ws_url))

        self.bulkSize = bulkSize

        self.userDefinedDictFILE = None
        self.openDataPlaceAccessBOOL=False
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB
        self.userDefinedDICT = {}

        if userDefinedDictFILE:
            try:
                if os.path.getsize(userDefinedDictFILE) <= self.fileSizeLimit:
                    userDefinedFile = json.load(open(userDefinedDictFILE, "r", encoding="utf8"))
                    if type(userDefinedFile) == dict:
                        self.userDefinedDICT = userDefinedFile
                    else:
                        print("User Defined File must be dict type.")
                        return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}
                else:
                    print("Maximum file size limit is 10 MB.")
            except Exception as e:
                print("User Defined File Loading Error.")
                print(str(e))
                return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}

        # Toolkit
        self.analyse = AnalyseManager()
        self.localRE = TaiwanAddressAnalizer(locale="TW")

    def __str__(self):
        return "Articut WebSocket API"

    def _wsCreateConnection(self):
        if not self.ws.connected:
            try:
                print("Reconnecting WebSocket...")
                self.ws = create_connection("{}/API/".format(self.ws_url))
            except Exception as e:
                print("WebSocket Connection Failed.", e)
        if not self.ws_bulk.connected:
            try:
                print("Reconnecting WebSocket[Bulk]...")
                self.ws_bulk = create_connection("{}/BulkAPI/".format(self.ws_url))
            except Exception as e:
                print("WebSocket[Bulk] Connection Failed.", e)
        return self.ws.connected

    def parse(self, inputSTR, level="lv2", userDefinedDICT={}, chemicalBOOL=True, openDataPlaceBOOL=False, wikiDataBOOL=False, indexWithPOS=False, timeRef=None, pinyin="BOPOMOFO"):
        if self._wsCreateConnection():
            payload = {"input_str": inputSTR,
                       "level": level,
                       "chemical": chemicalBOOL,
                       "opendata_place": openDataPlaceBOOL,
                       "wikidata": wikiDataBOOL,
                       "index_with_pos": indexWithPOS,
                       "pinyin": pinyin}
            if userDefinedDICT:
                payload["user_defined_dict_file"] = userDefinedDICT
            else:
                payload["user_defined_dict_file"] = self.userDefinedDICT

            if timeRef:
                payload["time_ref"] = str(timeRef)

            try:
                self.ws.send(json.dumps(payload))
                result = json.loads(self.ws.recv())
                return result
            except Exception as e:
                print("Exception", e, "\nInputSTR", inputSTR)
                return None

    def bulk_parse(self, inputLIST, level="lv2", userDefinedDICT={}, chemicalBOOL=True, openDataPlaceBOOL=False, wikiDataBOOL=False, indexWithPOS=False, timeRef=None, pinyin="BOPOMOFO"):
        resultLIST = []
        if self._wsCreateConnection():
            resultAppend = resultLIST.append
            inputLen = len(inputLIST)
            payload = {"level": level,
                       "chemical": chemicalBOOL,
                       "opendata_place": openDataPlaceBOOL,
                       "wikidata": wikiDataBOOL,
                       "index_with_pos": indexWithPOS,
                       "pinyin": pinyin}
            if userDefinedDICT:
                payload["user_defined_dict_file"] = userDefinedDICT
            else:
                payload["user_defined_dict_file"] = self.userDefinedDICT

            if timeRef:
                payload["time_ref"] = str(timeRef)

            for i in range(0, inputLen, self.bulkSize):
                if i+self.bulkSize > inputLen:
                    payload["input_list"] = inputLIST[i:]
                else:
                    payload["input_list"] = inputLIST[i:i+self.bulkSize]

                try:
                    self.ws_bulk.send(json.dumps(payload))
                    resultAppend(json.loads(self.ws_bulk.recv()))
                except Exception as e:
                    print("Exception", e, "\nInputLIST", payload["input_list"])
                    return None
        return resultLIST

    def mergeBulkResult(self, inputLIST):
        resultLIST = []
        resultExtend = resultLIST.extend
        for x in filter(None, inputLIST):
            try:
                if x["status"]:    # 只取成功的結果
                    resultExtend(x["result_list"])
            except:
                pass
        return resultLIST

    def version(self):
        url = "{}/Articut/Version/".format(self.url)
        result = requests.get(url)
        if result.status_code == 200:
            result = result.json()
        return result

    ##############################################################################
    #                                 Toolkits                                   #
    ##############################################################################
    def getPersonLIST(self, parseResultDICT, includePronounBOOL=True, indexWithPOS=True):
        '''
        取出斷詞結果中的人名 (Person)
        若 includePronounBOOL 為 True，則連代名詞 (Pronoun) 一併回傳；若為 False，則只回傳人名。
        回傳結果為一個 list。
        '''
        return getPersonLIST(parseResultDICT, includePronounBOOL, indexWithPOS)

    def getContentWordLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的實詞 (content word)。
        每個句子內的實詞為一個 list。
        '''
        return getContentWordLIST(parseResultDICT, indexWithPOS)

    def getChemicalLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的化學類詞 (KNOWLEDGE_chemical)。
        每個句子內的化學類詞為一個 list。
        '''
        return getChemicalLIST(parseResultDICT, indexWithPOS)

    def getVerbStemLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的動詞 (verb)。此處指的是 ACTION_verb 標記的動詞詞彙。
        每個句子內的動詞為一個 list。
        '''
        return getVerbStemLIST(parseResultDICT, indexWithPOS)

    def getNounStemLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的名詞 (noun)。此處指的是 ENTITY_noun、ENTITY_nouny、ENTITY_nounHead 或 ENTITY_oov 標記的名詞詞彙。
        每個句子內的名詞為一個 list。
        '''
        return getNounStemLIST(parseResultDICT, indexWithPOS)

    def getTimeLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的時間 (time)。
        每個句子內的「時間」詞列為一個 list。
        '''
        return getTimeLIST(parseResultDICT, indexWithPOS)

    def getLocationStemLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的地理位置 (location)。此處指的是地理位置標記的行政區地名詞彙，例如「台北」、「桃園」、「墨西哥」。
        每個句子內的地理位置列為一個 list。
        '''
        return getLocationStemLIST(parseResultDICT, indexWithPOS)

    def getOpenDataPlaceLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的景點 (KNOWLEDGE_place) 標籤的字串。此處指的是景點 (KNOWLEDGE_place)標記的非行政地點名稱詞彙，例如「鹿港老街」、「宜蘭運動公園」。
        每個句子內的景點為一個 list.
        '''
        return getOpenDataPlaceLIST(parseResultDICT, indexWithPOS)

    def getQuestionLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (CLAUSE_Q) 標籤的句子。
        此處指的是
            <CLAUSE_AnotAQ>: A-not-A 問句
            <CLAUSE_YesNoQ>: 是非問句
            <CLAUSE_WhoQ">: 「誰」問句
            <CLAUSE_WhatQ>: 「物」問句
            <CLAUSE_WhereQ>: 「何地」問句
            <CLAUSE_WhenQ>: 「何時」問句
            <CLAUSE_HowQ>: 「程度/過程」問句
            <CLAUSE_WhyQ>: 「原因」問句
        每個句子內若有 <CLAUSE_Q> 標籤，整個句子將會存進 list。
        '''
        return getQuestionLIST(parseResultDICT, indexWithPOS)

    def getAddTWLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (KNOWLEDGE_addTW) 標籤的字串。
        該字串為一台灣地址。
        '''
        return getAddTWLIST(parseResultDICT, indexWithPOS)

    def getCurrencyLIST(self, parseResultDICT, indexWithPOS=True, greedyBOOL=False):
        '''
        取出斷詞結果中的貨幣金額 (KNOWLEDGE_currency) 標籤的字串。
        每個句子內的「貨幣金額」，將列為一個 list。
        若 greedy = True，則以下格式會加到回傳 list
            貨幣名稱 + 數字 (包含「'」與「,」符號)
            新台幣 100
            美金9.99
            歐元 1,999'99
        '''
        return getCurrencyLIST(parseResultDICT, indexWithPOS, greedyBOOL)

    def getWikiDataLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的 WikiData 標記文字。此處指的是 KNOWLEDGE_wikiData 標記的條目名稱。
        每個句子內的條目名稱為一個 list。
        '''
        return getWikiDataLIST(parseResultDICT, indexWithPOS)

    def bulk_getPersonLIST(self, parseResultLIST, includePronounBOOL=True, indexWithPOS=True):
        '''
        取出斷詞結果中的人名 (Person)
        若 includePronounBOOL 為 True，則連代名詞 (Pronoun) 一併回傳；若為 False，則只回傳人名。
        回傳結果為一個 list。
        '''
        resultLIST = [getPersonLIST(x, includePronounBOOL, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getContentWordLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的實詞 (content word)。
        每個句子內的實詞為一個 list。
        '''
        resultLIST = [getContentWordLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getChemicalLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的化學類詞 (KNOWLEDGE_chemical)。
        每個句子內的化學類詞為一個 list。
        '''
        resultLIST = [getChemicalLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getVerbStemLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的動詞 (verb)。此處指的是 ACTION_verb 標記的動詞詞彙。
        每個句子內的動詞為一個 list。
        '''
        resultLIST = [getVerbStemLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getNounStemLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的名詞 (noun)。此處指的是 ENTITY_noun、ENTITY_nouny、ENTITY_nounHead 或 ENTITY_oov 標記的名詞詞彙。
        每個句子內的名詞為一個 list。
        '''
        resultLIST = [getNounStemLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getTimeLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的時間 (time)。
        每個句子內的「時間」詞列為一個 list。
        '''
        resultLIST = [getTimeLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getLocationStemLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的地理位置 (location)。此處指的是地理位置標記的行政區地名詞彙，例如「台北」、「桃園」、「墨西哥」。
        每個句子內的地理位置列為一個 list。
        '''
        resultLIST = [getLocationStemLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getOpenDataPlaceLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的景點 (KNOWLEDGE_place) 標籤的字串。此處指的是景點 (KNOWLEDGE_place)標記的非行政地點名稱詞彙，例如「鹿港老街」、「宜蘭運動公園」。
        每個句子內的景點為一個 list.
        '''
        resultLIST = [getOpenDataPlaceLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getQuestionLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (CLAUSE_Q) 標籤的句子。
        此處指的是
            <CLAUSE_AnotAQ>: A-not-A 問句
            <CLAUSE_YesNoQ>: 是非問句
            <CLAUSE_WhoQ">: 「誰」問句
            <CLAUSE_WhatQ>: 「物」問句
            <CLAUSE_WhereQ>: 「何地」問句
            <CLAUSE_WhenQ>: 「何時」問句
            <CLAUSE_HowQ>: 「程度/過程」問句
            <CLAUSE_WhyQ>: 「原因」問句
        每個句子內若有 <CLAUSE_Q> 標籤，整個句子將會存進 list。
        '''
        resultLIST = [getQuestionLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getAddTWLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (KNOWLEDGE_addTW) 標籤的字串。
        該字串為一台灣地址。
        '''
        resultLIST = [getAddTWLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST

    def bulk_getCurrencyLIST(self, parseResultLIST, indexWithPOS=True, greedyBOOL=False):
        '''
        取出斷詞結果中的貨幣金額 (KNOWLEDGE_currency) 標籤的字串。
        每個句子內的「貨幣金額」，將列為一個 list。
        若 greedy = True，則以下格式會加到回傳 list
            貨幣名稱 + 數字 (包含「'」與「,」符號)
            新台幣 100
            美金9.99
            歐元 1,999'99
        '''
        resultLIST = [getCurrencyLIST(x, indexWithPOS, greedyBOOL) for x in parseResultLIST]
        return resultLIST

    def bulk_getWikiDataLIST(self, parseResultLIST, indexWithPOS=True):
        '''
        取出斷詞結果中的 WikiData 標記文字。此處指的是 KNOWLEDGE_wikiData 標記的條目名稱。
        每個句子內的條目名稱為一個 list。
        '''
        resultLIST = [getWikiDataLIST(x, indexWithPOS) for x in parseResultLIST]
        return resultLIST


if __name__ == "__main__":
    PORT = 8964
    URL = "127.0.0.1"
    BulkSize = 20
    enableTrace(False)

    userDefinedDICT = {"地球人類補完計劃":["人類補完計劃", "人類再生計劃", "補完計劃"]}
    inputLIST = open("{}/as_test_1k.utf8".format(os.path.dirname(os.path.abspath(__file__))), "r", encoding="UTF-8").read().split("\n")[:20]

    articut = WS_Articut(url=URL, port=PORT, bulkSize=BulkSize)

    startTime = time.time()
    # 一次一句 N=1
    for inputSTR in inputLIST:
        result = articut.parse(inputSTR, "lv2")
        pprint(result)
    pprint(articut.getContentWordLIST(result))

    # 一次多句 (BulkSize=N)
    result = articut.bulk_parse(inputLIST, "lv2")
    #pprint(result)
    resultLIST = articut.mergeBulkResult(result)
    #pprint(resultLIST)
    pprint(articut.bulk_getContentWordLIST(resultLIST))
    print("Execution Time:", round(time.time() - startTime, 4))
