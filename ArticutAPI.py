#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import requests

try:
    from Toolkit.analyse import AnalyseManager
    from Toolkit.localRE import TaiwanAddressAnalizer
except: #供外部載入時使用。
    from .Toolkit.analyse import AnalyseManager
    from .Toolkit.localRE import TaiwanAddressAnalizer

try:
    from Toolkit.graphQL import GraphQL
except:
    print("No module named 'graphene'")
    print("Articut-graphQL requires 'graphene' module.")
    print("Please use pip/conda install graphene-python to install the module and reload ArticutAPI.")

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        '''
        username = ""    # 你註冊時的 email。若留空，則會使用每小時更新 2000 字的公用帳號。
        apikey = ""      # 您完成付費後取得的 apikey 值。若留空，則會使用每小時更新 2000 字的公用帳號。
        '''
        try:
            with open("./account.info", "r") as f:
                userDICT = json.loads(f.read())
            self.username = userDICT["email"]
            self.apikey = userDICT["apikey"]
        except:
            self.username = username
            self.apikey = apikey

        self.url = "https://api.droidtown.co"

        self.version = version
        self.level = level

        self.userDefinedDictFILE = None
        self.openDataPlaceAccessBOOL=False
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

        # Regex Pattern
        self.verbPPat = re.compile("(?<=<VerbP>)[^<]*?(?=.</VerbP>)")
        self.verbPat = re.compile("(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)")
        self.nounPat = re.compile("(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)")
        self.modifierPat = re.compile("(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)")
        self.funcPat = re.compile("(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)")
        self.personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)")
        self.pronounPat = re.compile("(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")
        self.locationPat = re.compile("(?<=<LOCATION>)[^<]*?(?=</LOCATION>)")
        self.placePat = re.compile("(?<=<KNOWLEDGE_place>)[^<]*?(?=</KNOWLEDGE_place>)")
        self.timePat = re.compile("(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)")
        self.eventPat = re.compile("<ACTION_lightVerb>[^<]</ACTION_lightVerb>((?<!</LOCATION>)<ENTITY_nouny>[^<]</ENTITY_nouny>)?((<ACTION_verb>[^<]*?</ACTION_verb>)|(<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>$))|<ACTION_verb>.?[有現到見道]</ACTION_verb>(<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>|<ENTITY_person>[^<]*?</ENTITY_person>)$|(?<=[有現到見道]</ACTION_verb>)((?<!</LOCATION>)<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>)?<ACTION_verb>[^<有現到見道]{1,2}</ACTION_verb>$|((?<!</LOCATION>)<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>)?<ACTION_verb>[^<有現到見道]{1,2}</ACTION_verb>(?!<ACTION)(?!<LOCATION)(?!<KNOWLEDGE)(?!<MODIFIER>)(?!<ENTITY_classifier)(?!<ENTITY_pronoun>)(<ENTITY_nouny?>[^<]*?</ENTITY_nouny?>|<ENTITY_person>[^<]*?</ENTITY_person>)?|<ACTION_lightVerb>.</ACTION_lightVerb><VerbP>[^<]*?</VerbP>|<ACTION_verb>[^<]*?</ACTION_verb>($|(?=<ACTION_verb>))")
        self.addTWPat = re.compile("(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)")
        self.currencyPat = re.compile("(?<=<KNOWLEDGE_currency>)[^<]*?(?=</KNOWLEDGE_currency>)")
        self.currencyGreedyPat = re.compile("(?<=[元金幣圜圓比布索鎊盾銖令朗郎]</ENTITY_noun><ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.currencyGreedyGapPat = re.compile("(?<=^<ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.wikiDataPat = re.compile("(?<=<KNOWLEDGE_wikiData>)[^<]*?(?=</KNOWLEDGE_wikiData>)")
        self.stripPat = re.compile("(?<=>).*?(?=<)")
        self.clausePat = re.compile("\<CLAUSE_.*?Q\>")
        self.contentPat = re.compile("|".join([self.verbPat.pattern, self.nounPat.pattern, self.modifierPat.pattern, self.verbPPat.pattern]))

        # Toolkit
        self.analyse = AnalyseManager()
        self.localRE = TaiwanAddressAnalizer(locale="TW")
        try:
            self.graphQL = GraphQL()
        except:
            pass

    def __str__(self):
        return "Articut API"

    def _segIndexConverter(self, parseResultDICT, posIndexLIST):
        '''
        Convert posIndex to segIndex
        Return list
        '''

        if type(posIndexLIST) is list and "result_pos" in parseResultDICT:
            pass
        else:
            return None

        segIndexLIST = []
        try:
            for i, posLIST in enumerate(posIndexLIST):
                if posLIST:
                    tmpLIST = []
                    for start, end, seg in posLIST:
                        posEndSTR = parseResultDICT["result_pos"][i][:start]
                        segEndSTR = "".join([x.group() for x in self.stripPat.finditer(posEndSTR)])
                        tmpLIST.append((len(segEndSTR), len(segEndSTR)+len(seg), seg))
                    segIndexLIST.append(tmpLIST)
                else:
                    segIndexLIST.append(posLIST)
        except Exception as e:
            print("Invalid posIndexLIST format")
            return None
        return segIndexLIST

    def parse(self, inputSTR, level="", userDefinedDictFILE=None, openDataPlaceAccessBOOL=False, wikiDataBOOL=False):
        if level=="":
            level = self.level
        self.openDataPlaceAccessBOOL=openDataPlaceAccessBOOL
        self.wikiDataBOOL=wikiDataBOOL
        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,                         #String Type：要做斷詞處理的中文句子。
                   "username": self.username,                     #String Type：使用者帳號 email
                   "api_key": self.apikey,                        #String Type：使用者 api key。若未提供，預設使用每小時更新 2000 字的公用額度。
                   "version": self.version,                       #String Type：指定斷詞引擎版本號。預設為最新版 "latest"
                   "level": level,                                #String Type：指定為 lv1 極致斷詞 (斷得較細) 或 lv2 詞組斷詞 (斷得較粗)。
                   "opendata_place":self.openDataPlaceAccessBOOL, #Bool Type：為 True 或 False，表示是否允許 Articut 讀取 OpenData 中的地點名稱。
                   "wikidata": self.wikiDataBOOL}                 #Bool Type：為 True 或 False，表示是否允許 Articut 讀取 WikiData 中的條目名稱。

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

    def getPersonLIST(self, parseResultDICT, includePronounBOOL=True, indexWithPOS=True):
        '''
        取出斷詞結果中的人名 (Person)
        若 includePronounBOOL 為 True，則連代名詞 (Pronoun) 一併回傳；若為 False，則只回傳人名。
        回傳結果為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        person_pronounLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p)>1:
                personLIST = [(pn.start(), pn.end(), pn.group(0)) for pn in list(self.personPat.finditer(p))]
                person_pronounLIST.append(personLIST)
            else:
                person_pronounLIST.append([])
        if includePronounBOOL == True:
            for p in parseResultDICT["result_pos"]:
                if len(p)==1:
                    pass
                else:
                    person_pronounLIST[parseResultDICT["result_pos"].index(p)].extend([(pn.start(), pn.end(), pn.group(0)) for pn in list(self.pronounPat.finditer(p))])
        if not indexWithPOS:
            person_pronounLIST = self._segIndexConverter(parseResultDICT, person_pronounLIST)
        return person_pronounLIST

    def getContentWordLIST(self, parseResultDICT, indexWithPOS=True):
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
            else:
                contentWordLIST.append([])
        if not indexWithPOS:
            contentWordLIST = self._segIndexConverter(parseResultDICT, contentWordLIST)
        return contentWordLIST

    def getVerbStemLIST(self, parseResultDICT, indexWithPOS=True):
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
                verbLIST.append([])
        if not indexWithPOS:
            verbLIST = self._segIndexConverter(parseResultDICT, verbLIST)
        return verbLIST

    def getNounStemLIST(self, parseResultDICT, indexWithPOS=True):
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
            else:
                nounLIST.append([])
        if not indexWithPOS:
            nounLIST = self._segIndexConverter(parseResultDICT, nounLIST)
        return nounLIST

    def getEventLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的事件 (event)。一個事件包含「一個動詞」以及受詞 (若有的話)。
        每個句子內事件列為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        eventLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                tmpE = re.sub("(?<=</ACTION_verb>)<((MODIFIER)|(ENTITY_nouny))>[^<]{1,4}</((MODIFIER)|(ENTITY_nouny))>(<FUNC_inner>的</FUNC_inner>)?(?=<ENTITY_nouny>)", "", p)
                tmpEvent = [(e.start(), e.end(), re.sub("<{1}/?.*?>{1}", "", e.group(0))) for e in list(self.eventPat.finditer(tmpE))]
                eventLIST.append(tmpEvent)
            else:
                eventLIST.append([])
        if not indexWithPOS:
            eventLIST = self._segIndexConverter(parseResultDICT, eventLIST)
        return eventLIST

    def getTimeLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的時間 (time)。
        每個句子內的「時間」詞列為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        timeLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                timeLIST.append([(l.start(), l.end(), l.group(0)) for l in list(self.timePat.finditer(p))])
            else:
                timeLIST.append([])
        if not indexWithPOS:
            timeLIST = self._segIndexConverter(parseResultDICT, timeLIST)
        return timeLIST

    def getLocationStemLIST(self, parseResultDICT, indexWithPOS=True):
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
            else:
                locationLIST.append([])
        if not indexWithPOS:
            locationLIST = self._segIndexConverter(parseResultDICT, locationLIST)
        return locationLIST

    def getOpenDataPlaceLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的景點 (KNOWLEDGE_place) 標籤的字串。此處指的是景點 (KNOWLEDGE_place)標記的非行政地點名稱詞彙，例如「鹿港老街」、「宜蘭運動公園」。
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
            else:
                placeLIST.append([])
        if not indexWithPOS:
            placeLIST = self._segIndexConverter(parseResultDICT, placeLIST)
        return placeLIST

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
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None

        questionLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                tmpLIST = [q for q in list(self.clausePat.finditer(p))]
                if tmpLIST:
                    for q in tmpLIST:
                        questionLIST.append([(q.group(0), "".join([x.group(0) for x in self.stripPat.finditer(p)])) for q in list(self.clausePat.finditer(p))])
                else:
                    questionLIST.append([])
            else:
                questionLIST.append([])
        if not indexWithPOS:
            questionLIST = self._segIndexConverter(parseResultDICT, questionLIST)
        return questionLIST

    def getAddTWLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (KNOWLEDGE_addTW) 標籤的字串。
        該字串為一台灣地址。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        addTWLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                addTWLIST.append([(a.start(), a.end(), a.group(0)) for a in list(self.addTWPat.finditer(p))])
            else:
                addTWLIST.append([])
        if not indexWithPOS:
            addTWLIST = self._segIndexConverter(parseResultDICT, addTWLIST)
        return addTWLIST

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
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        currencyLIST = []
        for i, p in enumerate(parseResultDICT["result_pos"]):
            if len(p) > 1:
                currencyLIST.append([(c.start(), c.end(), c.group(0)) for c in list(self.currencyPat.finditer(p))])
                if greedyBOOL:
                    greedyLIST = []
                    try:
                        if parseResultDICT["result_pos"][i-1][-14:] == "</ENTITY_noun>" and parseResultDICT["result_pos"][i-1][-15] in "元金幣圜圓比布索鎊盾銖令朗郎":
                            greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyGapPat.finditer(p))]
                    except:
                        pass
                    if greedyLIST:
                        greedyLIST.extend([(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyPat.finditer(p))])
                    else:
                        greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(self.currencyGreedyPat.finditer(p))]
                    if greedyLIST:
                        currencyLIST[-1].extend(greedyLIST)
            else:
                currencyLIST.append([])
        if not indexWithPOS:
            currencyLIST = self._segIndexConverter(parseResultDICT, currencyLIST)
        return currencyLIST

    def getWikiDataLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的 WikiData 標記文字。此處指的是 KNOWLEDGE_wikiData 標記的條目名稱。
        每個句子內的條目名稱為一個 list。
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        wikiDataLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                wikiDataLIST.append([(n.start(), n.end(), n.group(0)) for n in list(self.wikiDataPat.finditer(p))])
            else:
                wikiDataLIST.append([])
        if not indexWithPOS:
            wikiDataLIST = self._segIndexConverter(parseResultDICT, wikiDataLIST)
        return wikiDataLIST

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


class Tokenizer:
    def __init__(self, articutResult):
        self.text = []
        self.tag_ = []
        self.idx = []
        self.pos_ = []


if __name__ == "__main__":
    from pprint import pprint

    #inputSTR = "你計劃過地球人類補完計劃" #parse() Demo
    #inputSTR = "2018 年 7 月 26 日" #getTimeLIST() Demo
    #inputSTR = "台北信義區出現哥吉拉！"#getEventLIST() Demo
    #inputSTR = "蔡英文總統明日到台北市政府找柯文哲開會討論他的想法，請你安排一下！" #getPersonLIST() Demo
    #inputSTR = "地址：宜蘭縣宜蘭市縣政北七路六段55巷1號2樓" #localRE 工具包 Demo
    inputSTR = "劉克襄在本次活動當中，分享了台北中山北路一日遊路線。他表示當初自己領著柯文哲一同探索了雙連市場與中山捷運站的小吃與商圈，還有商圈內的文創商店與日系雜物店鋪，都令柯文哲留下深刻的印象。劉克襄也認為，雙連市場內的魯肉飯、圓仔湯與切仔麵，還有九條通的日式店家、居酒屋等特色，也能讓人感受到台北舊城區不一樣的魅力。" #Articut-GraphQL Demo

    articut = Articut()

    print("inputSTR:{}\n".format(inputSTR))

    #檢查儲存的結果是否已存在
    resultFilePath = "articutResult.json"
    resultExistBOOL = False
    try:
        with open(resultFilePath, "r", encoding="utf-8") as resultFile:
            result = json.loads(resultFile.read())
            # inputSTR 去除空白及斜線
            # result_segmentation 去除斜線
            if inputSTR.replace(' ', '').replace("/", "") == result["result_segmentation"].replace("/", ""):
                resultExistBOOL = True
    except:
        pass

    #取得斷詞結果
    if not resultExistBOOL:
        result = articut.parse(inputSTR, level="lv2", openDataPlaceAccessBOOL=True, wikiDataBOOL=True)

        #儲存斷詞結果
        try:
            with open(resultFilePath, "w", encoding="utf-8") as resultFile:
                json.dump(result, resultFile, ensure_ascii=False)
                print("斷詞結果儲存成功")
        except Exception as e:
            print("斷詞結果儲存失敗：{}".format(e))

    print("\n斷詞結果：")
    pprint(result["result_segmentation"])
    print("\n標記結果：")
    pprint(result["result_pos"])

    #列出目前可使用的 Articut 版本選擇。通常版本號愈大，完成度愈高。
    versions = articut.versions()
    print("\n##Avaliable Versions:")
    pprint(versions)

    #列出所有的 content word.
    contentWordLIST = articut.getContentWordLIST(result)
    print("\n##ContentWord:")
    pprint(contentWordLIST)

    #列出所有的人名 (不含代名詞).
    personLIST = articut.getPersonLIST(result, includePronounBOOL=False)
    print("\n##Person (Without Pronoun):")
    pprint(personLIST)
    personLIST = articut.getPersonLIST(result, includePronounBOOL=True)
    print("\n##Person (With Pronoun):")
    pprint(personLIST)

    #列出所有的 verb word. (動詞)
    verbStemLIST = articut.getVerbStemLIST(result)
    print("\n##Verb:")
    pprint(verbStemLIST)

    #列出所有的 noun word. (名詞)
    nounStemLIST = articut.getNounStemLIST(result)
    print("\n##Noun:")
    pprint(nounStemLIST)

    #列出所有的 event (事件)
    eventLIST = articut.getEventLIST(result)
    print("\n##Event:")
    pprint(eventLIST)

    #列出所有的 time (時間)
    timeLIST = articut.getTimeLIST(result)
    print("\n##Time:")
    pprint(timeLIST)

    #列出所有的 location word. (地方名稱)
    locationStemLIST = articut.getLocationStemLIST(result)
    print("\n##Location:")
    pprint(locationStemLIST)

    #允許 Articut 調用字典，列出所有政府開放資料中列為觀光地點名稱的字串。(地點名稱)
    placeLIST = articut.getOpenDataPlaceLIST(result)
    print("\n##Place:")
    pprint(placeLIST)

    #允許 Articut 調用 WikiData 字典，列出所有 WikiData 條目名稱的字串。
    wikiDataLIST = articut.getWikiDataLIST(result)
    print("\n##WikiData:")
    pprint(wikiDataLIST)

    #列出所有的 CLAUSE 問句
    questionLIST = articut.getQuestionLIST(result)
    print("\n##Question:")
    pprint(questionLIST)

    #列出所有的台灣地址
    addTWLIST = articut.getAddTWLIST(result)
    print("\n##Address:")
    pprint(addTWLIST)

    #使用 TF-IDF 演算法
    tfidfResult = articut.analyse.extract_tags(result)
    print("\n##TF-IDF:")
    pprint(tfidfResult)

    #使用 Textrank 演算法
    textrankResult = articut.analyse.textrank(result)
    print("\n##Textrank:")
    pprint(textrankResult)

    #使用 localRE 工具取得地址分段細節
    countyResult = articut.localRE.getAddressCounty(result)
    print("\n##localRE: 縣")
    pprint(countyResult)

    cityResult = articut.localRE.getAddressCity(result)
    print("\n##localRE: 市")
    pprint(cityResult)

    districtResult = articut.localRE.getAddressDistrict(result)
    print("\n##localRE: 區")
    pprint(districtResult)

    townshipResult = articut.localRE.getAddressTownship(result)
    print("\n##localRE: 鄉里")
    pprint(townshipResult)

    townResult = articut.localRE.getAddressTown(result)
    print("\n##localRE: 鎮")
    pprint(townResult)

    villageResult = articut.localRE.getAddressVillage(result)
    print("\n##localRE: 村")
    pprint(villageResult)

    neighborhoodResult = articut.localRE.getAddressNeighborhood(result)
    print("\n##localRE: 鄰")
    pprint(neighborhoodResult)

    roadResult = articut.localRE.getAddressRoad(result)
    print("\n##localRE: 路")
    pprint(roadResult)

    sectionResult = articut.localRE.getAddressSection(result)
    print("\n##localRE: 段")
    pprint(sectionResult)

    alleyResult = articut.localRE.getAddressAlley(result)
    print("\n##localRE: 巷、弄")
    pprint(alleyResult)

    numberResult = articut.localRE.getAddressNumber(result)
    print("\n##localRE: 號")
    pprint(numberResult)

    floorResult = articut.localRE.getAddressFloor(result)
    print("\n##localRE: 樓")
    pprint(floorResult)

    roomResult = articut.localRE.getAddressRoom(result)
    print("\n##localRE: 室")
    pprint(roomResult)

    #列出所有的貨幣金額
    currencyResult = articut.getCurrencyLIST(result)
    print("\n##currencyLIST:")
    pprint(currencyResult)

    #使用 Articut-GraphQL 查詢斷詞結果
    try:
        graphQLResult = articut.graphQL.query(
            filePath=resultFilePath,
            query="""
        {
          meta {
            lang
            description
          }
          doc {
            text
            tokens {
              text
              pos_
              tag_
              isStop
              isEntity
              isVerb
              isTime
              isClause
              isKnowledge
            }
            ents {
              persons {
                text
                pos_
                tag_
              }
              nouns {
                text
                pos_
                tag_
              }
              numbers {
                text
                pos_
                tag_
              }
              sites {
                text
                pos_
                tag_
              }
            }
          }
        }""")
        print("\n##Articut-GraphQL:")
        pprint(graphQLResult)
    except:
        print("No module named 'graphene'")
        print("Articut-graphQL requires 'graphene' module.")
        print("Please use pip/conda install graphene-python to install the module and reload ArticutAPI.")