#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import requests

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        '''
        username = "你註冊時的 email。若留空，則會使用每日 1 萬字的公用帳號。
        apikey = "您完成付費後取得的 apikey 值。若留空，則會使用每日 10 萬字的公用帳號。
        '''

        self.url = "https://api.droidtown.co"
        self.username = username
        self.apikey = apikey
        self.version = version
        self.level = level

        self.userDefinedDictFILE = None
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

        self.verbPPat = "(?<=<VerbP>)[^<]*?(?=.</VerbP>)"

        self.verbPat = "(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)"
        self.nounPat = "(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)"
        self.modifierPat = "(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)"
        self.funcPat = "(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)"
        self.personPat = "(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)|(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)"
        self.locationPat = "(?<=<LOCATION>)[^<]*?(?=</LOCATION>)"
        self.timePat = "(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)"

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
        contentPat = "|".join([self.verbPat, self.nounPat, self.modifierPat, self.verbPPat])
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                contentWordLIST.append([(c.start(), c.end(), c.group(0)) for c in reversed(list(re.finditer(contentPat, p)))])
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
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(re.finditer(self.verbPPat, p)))])
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(re.finditer(self.verbPat, p)))])
                else:
                    verbLIST.append([(v.start(), v.end(), v.group(0)) for v in reversed(list(re.finditer(self.verbPat, p)))])
        verbLIST = [v for v in verbLIST if v]
        return verbLIST

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
    inputSTR = "你計劃過人類補完計劃"
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


    #列出目前可使用的 Articut 版本選擇。通常版本號愈大，完成度愈高。
    versions = articut.versions()
    pprint(versions)