#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    import rapidjson as json
except:
    import json

import os
import re

def mergeBulkResult(inputLIST):
    resultLIST = []
    resultExtend = resultLIST.extend
    for x in filter(None, inputLIST):
        try:
            if x["status"]:    # 只取成功的結果
                resultExtend(x["result_list"])
        except:
            pass
    return resultLIST

class ArticutPOS:
    def __init__(self):
        # Regex Pattern
        self.verbPat = re.compile("(?<=<VerbP>)[^<]*?(?=.</VerbP>)|(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)")
        self.nounPat = re.compile("(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)")
        self.modifierPat = re.compile("(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)")
        self.modifierPPat = re.compile("(?<=<DegreeP>)[^<]*?(?=</DegreeP>)|(?<=<ModifierP>)[^<]*?(?=</ModifierP>)")
        self.funcPat = re.compile("(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)")
        self.personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)")
        self.pronounPat = re.compile("(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")
        self.locationPat = re.compile("(?<=<LOCATION>)[^<]*?(?=</LOCATION>)|(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)|(?<=<KNOWLEDGE_routeTW>)[^<]*?(?=</KNOWLEDGE_routeTW>)")
        self.userDefinedPat = re.compile("(?<=<UserDefined>)[^<]*?(?=</UserDefined>)")
        self.placePat = re.compile("(?<=<KNOWLEDGE_place>)[^<]*?(?=</KNOWLEDGE_place>)")
        self.timePat = re.compile("(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)")
        self.addTWPat = re.compile("(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)")
        self.colorPat = re.compile("(?<=<MODIFIER_color>)[^<]+?(?=</MODIFIER_color>)")
        self.currencyPat = re.compile("(?<=<KNOWLEDGE_currency>)[^<]*?(?=</KNOWLEDGE_currency>)")
        self.currencyGreedyPat = re.compile("(?<=[元金幣圜圓比布索鎊盾銖令朗郎]</ENTITY_noun><ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.currencyGreedyGapPat = re.compile("(?<=^<ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
        self.chemicalPat = re.compile("(?<=<KNOWLEDGE_chemical>)[^<]*?(?=</KNOWLEDGE_chemical>)")
        self.wikiDataPat = re.compile("(?<=<KNOWLEDGE_wikiData>)[^<]*?(?=</KNOWLEDGE_wikiData>)")
        self.stripPat = re.compile("(?<=>).*?(?=<)")
        self.clausePat = re.compile("\<CLAUSE_.*?Q\>")
        self.contentPat = re.compile("|".join([self.verbPat.pattern, self.nounPat.pattern, self.modifierPat.pattern, self.modifierPPat.pattern, self.userDefinedPat.pattern]))

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
        except Exception:
            print("Invalid posIndexLIST format")
            return None
        return segIndexLIST

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

    def getColorLIST(self, resultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中含有 (MODIFIER_color) 標籤的字串。
        該字串為一顏色表述字串
        '''
        if "result_pos" in resultDICT:
            pass
        else:
            return None
        colorLIST = []
        for p in resultDICT["result_pos"]:
            if len(p) > 1:
                colorLIST.append([(a.start(), a.end(), a.group(0)) for a in list(self.colorPat.finditer(p))])
            else:
                colorLIST.append([])
        if not indexWithPOS:
            colorLIST = self._segIndexConverter(resultDICT, colorLIST)
        return colorLIST

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

    def getChemicalLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的 KNOWLEDGE_chemical。
        每個句子內的 KNOWLEDGE_chemical 為一個 list.
        '''
        if "result_pos" in parseResultDICT:
            pass
        else:
            return None
        chemicalLIST = []
        for p in parseResultDICT["result_pos"]:
            if len(p) > 1:
                chemicalLIST.append([(c.start(), c.end(), c.group(0)) for c in list(self.chemicalPat.finditer(p))])
            else:
                chemicalLIST.append([])
        if not indexWithPOS:
            chemicalLIST = self._segIndexConverter(parseResultDICT, chemicalLIST)
        return chemicalLIST

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

    def getOpenDataPlaceLIST(self, parseResultDICT, indexWithPOS=True):
        '''
        取出斷詞結果中的景點 (KNOWLEDGE_place) 標籤的字串。此處指的是景點 (KNOWLEDGE_place)標記的非行政地點名稱詞彙，例如「鹿港老街」、「宜蘭運動公園」。
        每個句子內的景點為一個 list.
        '''
        if "result_pos" in parseResultDICT:
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
                verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(self.verbPat.finditer(p))])
            else:
                verbLIST.append([])
        if not indexWithPOS:
            verbLIST = self._segIndexConverter(parseResultDICT, verbLIST)
        return verbLIST

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

class LawsToolkit:
    def __init__(self, articutResult=None):
        self.articutResult = articutResult
        self.articlePat = re.compile("<KNOWLEDGE_lawTW>[^<]+?</KNOWLEDGE_lawTW>")
        self.crimePat = re.compile("(?<=[犯判決]</ACTION_verb>)[^犯罪]*?(>(?=<KNOWLEDGE_lawTW>第)|罪(?=<))")
        self.criminalResponsibilityPat = re.compile("(?<=<ACTION_verb>處</ACTION_verb>)[^處極重]*?[刑役](?=<)(<[^>]*?>)?(<TIME_year>[^<]+?</TIME_year>)?(<TIME_month>[^<]+?</TIME_month>)?")
        self.eventRefPat = re.compile("<FUNC_inner>所</FUNC_inner><ACTION_lightVerb>受</ACTION_lightVerb>(<FUNC_inner>之</FUNC_inner>)?(<QUANTIFIER>[^<]+?</QUANTIFIER>)?<ENTITY_nouny>..</ENTITY_nouny>")

    def tagPurger(self, posSTR):
        textSTR = re.sub("<[^<]*?>", "", posSTR)
        return textSTR

    def getLawArticle(self, parseResultDICT={}):
        '''
        取得法條編號
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT
        articleLIST = []
        if type(self.articutResult) is list:
            self.articutResult = mergeBulkResult(self.articutResult)
            articleAppend = articleLIST.append
            for x in self.articutResult:
                articleAppend(list(set([self.tagPurger(a.group(0)) for a in self.articlePat.finditer("".join(x["result_pos"]))])))
        else:
            articleLIST = list(set([self.tagPurger(a.group(0)) for a in self.articlePat.finditer("".join(self.articutResult["result_pos"]))]))
        return articleLIST

    def getCrime(self, parseResultDICT={}):
        '''
        取得罪名
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT

        crimeTextLIST = []
        if type(self.articutResult) is list:
            self.articutResult = mergeBulkResult(self.articutResult)
            crimeTextAppend = crimeTextLIST.append
            for x in self.articutResult:
                crimePosLIST = set([c.group(0) for c in self.crimePat.finditer("".join(x["result_pos"]))])
                crimeTextAppend([self.tagPurger(c) for c in crimePosLIST])
        else:
            crimePosLIST = set([c.group(0) for c in self.crimePat.finditer("".join(self.articutResult["result_pos"]))])
            crimeTextLIST = [self.tagPurger(c) for c in crimePosLIST]
        return crimeTextLIST

    def getCriminalResponsibility(self, parseResultDICT={}):
        '''
        取得刑責
        To be deprecated soon.
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT
        try:
            crTextLIST = []
            if type(self.articutResult) is list:
                self.articutResult = mergeBulkResult(self.articutResult)
                crTextAppend = crTextLIST.append
                for x in self.articutResult:
                    crPosLIST = set([c.group(0) for c in self.criminalResponsibilityPat.finditer("".join(x["result_pos"]))])
                    crTextAppend([self.tagPurger(c) for c in crPosLIST])
            else:
                crPosLIST = set([c.group(0) for c in self.criminalResponsibilityPat.finditer("".join(self.articutResult["result_pos"]))])
                crTextLIST = [self.tagPurger(c) for c in crPosLIST]
            print("getCriminalResponsibility() To be deprecated soon.")
            return crTextLIST
        except KeyError:
            return []

    def getPenalty(self, parseResultDICT={}):
        '''
        取得刑責。
        Dummy Function of getCriminalResponsibility()
        '''
        return self.getCriminalResponsibility(parseResultDICT)

    def getEventRef(self, parseResultDICT={}):
        '''
        取得「所受(之)XX」的列表
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT

        erTextLIST = []
        if type(self.articutResult) is list:
            self.articutResult = mergeBulkResult(self.articutResult)
            erTextAppend = erTextLIST.append
            for x in self.articutResult:
                erPosLIST = set([e.group(0) for e in self.eventRefPat.finditer("".join(x["result_pos"]))])
                erTextAppend([self.tagPurger(e) for e in erPosLIST])
        else:
            erPosLIST = set([e.group(0) for e in self.eventRefPat.finditer("".join(self.articutResult["result_pos"]))])
            erTextLIST = [self.tagPurger(e) for e in erPosLIST]

        return erTextLIST

class UserDefinedDictToolkit:
    def __init__(self):
        self.msg_AticutDictERROR = "\n".join(["請輸入 Articut.parse() 處理完的 dictionary 做為參數！", "Please specify dictionary returned by Articut.parse() as argument!"])
        self.msg_UserDefinedDictionaryDIRERROR = "\n".join(["", ""])

    def tagByDictName(self, ArticutDICT, UserDefinedDictionaryDIR):
        try:
            if isinstance(ArticutDICT, dict):
                if "result_pos" in ArticutDICT:
                    pass
                else:
                    return self.msg_AticutDictERROR
            else:
                return self.msg_AticutDictERROR
        except:
            return self.msg_AticutDictERROR

        dictLIST = [d for d in os.listdir(UserDefinedDictionaryDIR) if d.endswith(".json")]
        for D in dictLIST:
            try:
                dictName = D.split("/")[-1].split(".json")[0]
                with open(D) as f:
                    dDICT = json.load(f.read())
                    dLIST = []
                    for d in dDICT:
                        dLIST.append(d)
                        dLIST.extend(dDICT[d])
            except:
                return self.msg_UserDefinedDictionaryDIRERROR

            resultLIST = []
            for s in ArticutDICT["result_pos"]:
                for d in dLIST:
                    if "<UserDefined>{}</UserDefined>".format(d) in s:
                        resultLIST.append(s.replace("<UserDefined>{}</UserDefined>".format(d), "UD_{}".format(dictName)))
                    else:
                        resultLIST.append(s)
            ArticutDICT["result_pos"] = resultLIST
        return ArticutDICT

class Tokenizer:
    def __init__(self, articutResult):
        self.text = []
        self.tag_ = []
        self.idx = []
        self.pos_ = []
