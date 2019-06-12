#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import requests

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        '''
        username = ""    # 你註冊時的 email。若留空，則會使用每日 1 萬字的公用帳號。
        apikey = ""      # 您完成付費後取得的 apikey 值。若留空，則會使用每日 10 萬字的公用帳號。
        '''

        self.url = "https://api.droidtown.co"
        self.username = username
        self.apikey = apikey
        self.version = version
        self.level = level

        self.userDefinedDictFILE = None
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

        self.verbPPat = re.compile("(?<=<VerbP>)[^<]*?(?=.</VerbP>)")

        self.verbPat = re.compile("(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)")
        self.nounPat = re.compile("(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)")
        self.modifierPat = re.compile("(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)")
        self.funcPat = re.compile("(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)")
        self.personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)|(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")
        self.locationPat = re.compile("(?<=<LOCATION>)[^<]*?(?=</LOCATION>)")
        self.timePat = re.compile("(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)")

    def __str__(self):
        return "Articut API"

    def parse(self, inputSTR, level="", userDefinedDictFILE=None):
        if level=="":
            level = self.level

        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,
                   "username": self.username,
                   "api_key": self.apikey,
                   "version": self.version,
                   "level": level}

        if userDefinedDictFILE:
            try:
                if os.path.getsize(userDefinedDictFILE) <= self.fileSizeLimit:
                    userDefinedFile = json.load(open(userDefinedDictFILE, "r", encoding="utf8"))
                    if type(userDefinedFile) == dict:
                        payload["file"] = userDefinedFile
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
        取出斷詞結果中的 content word。
        每個句子內的 content word 為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        contentWordLIST = []
        contentPat = re.compile("|".join([self.verbPat.pattern, self.nounPat.pattern, self.modifierPat.pattern, self.verbPPat.pattern]))
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                contentWordLIST.append([(c.start(), c.end(), c.group(0)) for c in reversed(list(contentPat.finditer(p)))])
        return contentWordLIST

    def getVerbStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的 verb。此處指的是 ACTION_verb 標記的動詞詞彙。
        每個句子內的 verb word 為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        verbLIST = []

        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                if "VerbP" in p:
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(self.verbPPat.finditer(p)))])
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(self.verbPat.finditer(p)))])
                else:
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(self.verbPat.finditer(p)))])
        verbLIST = [v for v in verbLIST if v]
        return verbLIST

    def getNounStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的 noun。此處指的是 ENTITY_noun、ENTITY_nouny、ENTITY_nounHead 或 ENTITY_oov 標記的名詞詞彙。
        每個句子內的 noun word 為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        nounLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                nounLIST.append([(n.start(), n.end(), n.group(0)) for n in reversed(list(self.nounPat.finditer(p)))])
        nounLIST = [n for n in nounLIST if n]
        return nounLIST

    def getLocationStemLIST(self, parseResultDICT):
        '''
        取出斷詞結果中的 LOCATION。此處指的是 LOCATION 標記的地名詞彙，可能是實體地方名稱或在句子中表示地方的詞彙。
        每個句子內的 location word 為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        locationLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                locationLIST.append([(l.start(), l.end(), l.group(0)) for l in reversed(list(self.locationPat.finditer(p)))])
        locationLIST = [l for l in locationLIST if l]
        return locationLIST

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

    #inputSTR = "我的計劃是讓你計劃人類補完計劃。"
    inputSTR = "你計劃過地球人類補完計劃"
    articut = Articut()

    #取得斷詞結果
    result = articut.parse(inputSTR, level="lv2")
    pprint(result)

    #列出所有的 content word.
    contentWordLIST = articut.getContentWordLIST(result)
    pprint(contentWordLIST)

    #列出所有的 verb word. (動詞)
    verbStemLIST = articut.getVerbStemLIST(result)
    pprint(verbStemLIST)

    #列出所有的 noun word. (名詞)
    nounStemLIST = articut.getNounStemLIST(result)
    pprint(nounStemLIST)

    #列出所有的 location word. (地方名稱)
    locationStemLIST = articut.getLocationStemLIST(result)
    pprint(locationStemLIST)

    #列出目前可使用的 Articut 版本選擇。通常版本號愈大，完成度愈高。
    versions = articut.versions()
    pprint(versions)