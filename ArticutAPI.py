#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import requests

try:
    from Toolkit.analyse import KeywordExtraction
except: #供外部載入時使用。
    from .Toolkit.analyse import KeywordExtraction

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        '''
        username = ""    # 你註冊時的 email。若留空，則會使用每日 1 萬字的公用帳號。
        apikey = ""      # 您完成付費後取得的 apikey 值。若留空，則會使用每日 1 萬字的公用帳號。
        '''

        self.url = "https://api.droidtown.co"
        self.username = username
        self.apikey = apikey
        self.version = version
        self.level = level

        self.userDefinedDictFILE = None
        self.openDataPlaceAccessBOOL=False
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

        self.verbPPat = re.compile("(?<=<VerbP>)[^<]*?(?=.</VerbP>)")

        self.verbPat = re.compile("(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)")
        self.nounPat = re.compile("(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)")
        self.modifierPat = re.compile("(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)")
        self.funcPat = re.compile("(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)")
        self.personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)|(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")
        self.locationPat = re.compile("(?<=<LOCATION>)[^<]*?(?=</LOCATION>)")
        self.placePat = re.compile("(?<=<KNOWLEDGE_place>)[^<]*?(?=</KNOWLEDGE_place>)")
        self.timePat = re.compile("(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)")
        self.eventPat = re.compile("<ACTION_verb>[^<]{1,2}</ACTION_verb>(?!<ACTION)(?!<LOCATION)(?!<KNOWLEDGE)(?!<ENTITY_classifier)(<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>)?")
        self.stripPat = re.compile("(?<=>).*?(?=<)")
        self.clausePat = re.compile("\<CLAUSE_.*?Q\>")
        self.contentPat = re.compile("|".join([self.verbPat.pattern, self.nounPat.pattern, self.modifierPat.pattern, self.verbPPat.pattern]))

        # Toolkit
        self.analyse = KeywordExtraction()

    def __str__(self):
        return "Articut API"

    def parse(self, inputSTR, level="", userDefinedDictFILE=None, openDataPlaceAccessBOOL=False):
        if level=="":
            level = self.level
        self.openDataPlaceAccessBOOL=openDataPlaceAccessBOOL
        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,                         #String Type：要做斷詞處理的中文句子。
                   "username": self.username,                     #String Type：使用者帳號 email
                   "api_key": self.apikey,                        #String Type：使用者 api key。若未提供，預設使用每日公用一萬字的額度。
                   "version": self.version,                       #String Type：指定斷詞引擎版本號。預設為最新版 "latest"
                   "level": level,                                #String Type：指定為 lv1 極致斷詞 (斷得較細) 或 lv2 詞組斷詞 (斷得較粗)。
                   "opendata_place":self.openDataPlaceAccessBOOL} #Bool Type：為 True 或 False，表示是否允許 Articut 存取 OpenData 中的地點名稱。

        if userDefinedDictFILE:
            try:
                if os.path.getsize(userDefinedDictFILE) <= self.fileSizeLimit:
                    userDefinedFile = json.load(open(userDefinedDictFILE, "r", encoding="utf8"))
                    if type(userDefinedFile) == dict:
                        payload["user_defined_dict_file"] = userDefinedFile
                    else:
                        print("User Defined File must be dict type.")
                        return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}
                else:
                    print("Maximum file size limit is 10 MB.")
            except Exception as e:
                print("User Defined File Loading Error.")
                print(str(e))
                return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}

        result = requests.post(url, json=payload)
        if result.status_code == 200:
            result = result.json()
            result["product"] = "{}/product/".format(self.url)
            result["document"] = "{}/document/".format(self.url)
        return result

    def getContentWordLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的實詞 (content word)。
        每個句子內的實詞為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        contentWordLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                contentWordLIST.append([(c.start(), c.end(), c.group(0)) for c in list(self.contentPat.finditer(p))])
        return contentWordLIST

    def getVerbStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的動詞 (verb)。此處指的是 ACTION_verb 標記的動詞詞彙。
        每個句子內的動詞為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        verbLIST = []

        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                if "VerbP" in p:
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(self.verbPPat.finditer(p))])
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(self.verbPat.finditer(p))])
                else:
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(self.verbPat.finditer(p))])
        verbLIST = [v for v in verbLIST if v]
        return verbLIST

    def getNounStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的名詞 (noun)。此處指的是 ENTITY_noun、ENTITY_nouny、ENTITY_nounHead 或 ENTITY_oov 標記的名詞詞彙。
        每個句子內的名詞為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        nounLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                nounLIST.append([(n.start(), n.end(), n.group(0)) for n in list(self.nounPat.finditer(p))])
        nounLIST = [n for n in nounLIST if n]
        return nounLIST

    def getEventLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的事件 (event)。一個事件包含「一個動詞」以及受詞 (若有的話)。
        每個句子內事件列為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None

        eventLIST = []
        for e in parseResultDICT["result_pos"]:
            if len(e) > 1:
                tmpEvent = [(e.start(), e.end(), e.group(0)) for e in list(self.eventPat.finditer(e))]
                for t in tmpEvent:
                    eventLIST.append((t[0], t[1], [s.group(0) for s in list(self.stripPat.finditer(t[2])) if len(s.group(0))>0]))
        return eventLIST

    def getTimeLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的時間 (time)。
        每個句子內的「時間」詞列為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        timeLIST = []
        for t in parseResultDICT["result_pos"]:
            if len(t) > 1:
                timeLIST.append([(l.start(), l.end(), l.group(0)) for l in list(self.timePat.finditer(t))])
        timeLIST = [t for t in timeLIST if t]
        return timeLIST

    def getLocationStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的地理位置 (location)。此處指的是地理位置標記的行政區地名詞彙，例如「台北」、「桃園」、「墨西哥」。
        每個句子內的地理位置列為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        locationLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                locationLIST.append([(l.start(), l.end(), l.group(0)) for l in list(self.locationPat.finditer(p))])
        locationLIST = [l for l in locationLIST if l]
        return locationLIST

    def getOpenDataPlaceLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的景點 (KNOWLEDGE_place)。此處指的是景點 (KNOWLEDGE_place)標記的非行政地點名稱詞彙，例如「鹿港老街」、「宜蘭運動公園」。
        每個句子內的景點為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None

        if self.openDataPlaceAccessBOOL==True:
            pass
        else:
            return None

        placeLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                placeLIST.append([(l.start(), l.end(), l.group(0)) for l in list(self.placePat.finditer(p))])
        placeLIST = [l for l in placeLIST if l]
        return placeLIST

    def getQuestionLIST(self, parseResultDICT):
        '''
        取出斷詞結果中含有 <CLAUSE_Q> 標籤的句子。
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
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None

        questionLIST = []
        for i, p in enumerate(parseResultDICT["result_pos"]):
            if len(p) > 1:
                for q in list(self.clausePat.finditer(p)):
                    questionLIST.append([[q.group(0), "".join([x.group(0) for x in self.stripPat.finditer(p)])] for q in list(self.clausePat.finditer(p))])
        questionLIST = [q for q in questionLIST if q]
        return questionLIST

    def versions(self):
        url = "{}/Articut/Versions/".format(self.url)
        payload = {"username":  self.username,
                   "api_key":   self.apikey}
        result = requests.post(url, data=payload)
        if result.status_code == 200:
            result = result.json()
            result["product"] = "{}/product/".format(self.url)
            result["document"] = "{}/document/".format(self.url)
        return result


if __name__ == "__main__":
    from pprint import pprint

    #inputSTR = "你計劃過地球人類補完計劃"
    #inputSTR = "阿美族民俗中心, 以東海岸人數最眾的原住民族群阿美族為主題"
    inputSTR = "你是否知道傍晚可以到觀音亭去看夕陽喔!"
    articut = Articut()

    #取得斷詞結果
    result = articut.parse(inputSTR, level="lv2", openDataPlaceAccessBOOL=True)
    pprint(result)

    #列出目前可使用的 Articut 版本選擇。通常版本號愈大，完成度愈高。
    versions = articut.versions()
    print("\n##Avaliable Versions:")
    pprint(versions)

    #列出所有的 content word.
    contentWordLIST = articut.getContentWordLIST(result)
    print("\n##ContentWord:")
    pprint(contentWordLIST)

    #列出所有的 verb word. (動詞)
    verbStemLIST = articut.getVerbStemLIST(result)
    print("\n##Verb:")
    pprint(verbStemLIST)

    #列出所有的 noun word. (名詞)
    nounStemLIST = articut.getNounStemLIST(result)
    print("\n##Noun:")
    pprint(nounStemLIST)

    #列出所有的 location word. (地方名稱)
    locationStemLIST = articut.getLocationStemLIST(result)
    print("\n##Location:")
    pprint(locationStemLIST)

    #允許 Articut 調用字典，列出所有政府開放資料中列為觀光地點名稱的字串。(地點名稱)
    placeLIST = articut.getOpenDataPlaceLIST(result)
    print("\n##Place:")
    pprint(placeLIST)

    #列出所有的 CLAUSE 問句
    questionLIST = articut.getQuestionLIST(result)
    print("\n##Question:")
    pprint(questionLIST)

    # 使用 TF-IDF 演算法
    tfidfResult = articut.analyse.extract_tags(result)
    pprint(tfidfResult)