#!/usr/bin/env python3
# -*- coding:utf-8 -*-

try:
    import rapidjson as json
except:
    import json

import os
import re

# Regex Pattern
verbPPat = re.compile("(?<=<VerbP>)[^<]*?(?=.</VerbP>)")
verbPat = re.compile("(?<=<ACTION_verb>)[^<]*?(?=</ACTION_verb>)")
nounPat = re.compile("(?<=<ENTITY_nounHead>)[^<]*?(?=</ENTITY_nounHead>)|(?<=<ENTITY_nouny>)[^<]*?(?=</ENTITY_nouny>)|(?<=<ENTITY_noun>)[^<]*?(?=</ENTITY_noun>)|(?<=<ENTITY_oov>)[^<]*?(?=</ENTITY_oov>)")
modifierPat = re.compile("(?<=<MODIFIER>)[^<]*?(?=</MODIFIER>)")
modifierPPat = re.compile("(?<=<DegreeP>)[^<]*?(?=</DegreeP>)|(?<=<ModifierP>)[^<]*?(?=</ModifierP>)")
funcPat = re.compile("(?<=<AUX>)[^<]*?(?=</AUX>)|(?<=<FUNC_in[nt]er>)[^<]*?(?=</FUNC_in[nt]er>)|(?<=<RANGE_locality>)[^<]*?(?=</RANGE_locality>)|(?<=<RANGE_period>)[^<]*?(?=</RANGE_period>)")
personPat = re.compile("(?<=<ENTITY_person>)[^<]*?(?=</ENTITY_person>)")
pronounPat = re.compile("(?<=<ENTITY_pronoun>)[^<]*?(?=</ENTITY_pronoun>)")
locationPat = re.compile("(?<=<LOCATION>)[^<]*?(?=</LOCATION>)|(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)|(?<=<KNOWLEDGE_routeTW>)[^<]*?(?=</KNOWLEDGE_routeTW>)")
userDefinedPat = re.compile("(?<=<UserDefined>)[^<]*?(?=</UserDefined>)")
placePat = re.compile("(?<=<KNOWLEDGE_place>)[^<]*?(?=</KNOWLEDGE_place>)")
timePat = re.compile("(?<=<TIME_decade>)[^<]*?(?=</TIME_decade>)|(?<=<TIME_year>)[^<]*?(?=</TIME_year>)|(?<=<TIME_season>)[^<]*?(?=</TIME_season>)|(?<=<TIME_month>)[^<]*?(?=</TIME_month>)|(?<=<TIME_week>)[^<]*?(?=</TIME_week>)|(?<=<TIME_day>)[^<]*?(?=</TIME_day>)|(?<=<TIME_justtime>)[^<]*?(?=</TIME_justtime>)")
addTWPat = re.compile("(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)")
currencyPat = re.compile("(?<=<KNOWLEDGE_currency>)[^<]*?(?=</KNOWLEDGE_currency>)")
currencyGreedyPat = re.compile("(?<=[元金幣圜圓比布索鎊盾銖令朗郎]</ENTITY_noun><ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
currencyGreedyGapPat = re.compile("(?<=^<ENTITY_num>)[^<]*?(?=</ENTITY_num>)")
chemicalPat = re.compile("(?<=<KNOWLEDGE_chemical>)[^<]*?(?=</KNOWLEDGE_chemical>)")
wikiDataPat = re.compile("(?<=<KNOWLEDGE_wikiData>)[^<]*?(?=</KNOWLEDGE_wikiData>)")
stripPat = re.compile("(?<=>).*?(?=<)")
clausePat = re.compile("\<CLAUSE_.*?Q\>")
contentPat = re.compile("|".join([verbPPat.pattern, verbPat.pattern, nounPat.pattern, modifierPat.pattern, modifierPPat.pattern, userDefinedPat.pattern]))


def _segIndexConverter(parseResultDICT, posIndexLIST):
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
                    segEndSTR = "".join([x.group() for x in stripPat.finditer(posEndSTR)])
                    tmpLIST.append((len(segEndSTR), len(segEndSTR)+len(seg), seg))
                segIndexLIST.append(tmpLIST)
            else:
                segIndexLIST.append(posLIST)
    except Exception:
        print("Invalid posIndexLIST format")
        return None
    return segIndexLIST

def getPersonLIST(parseResultDICT, includePronounBOOL=True, indexWithPOS=True):
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
            personLIST = [(pn.start(), pn.end(), pn.group(0)) for pn in list(personPat.finditer(p))]
            person_pronounLIST.append(personLIST)
        else:
            person_pronounLIST.append([])
    if includePronounBOOL == True:
        for p in parseResultDICT["result_pos"]:
            if len(p)==1:
                pass
            else:
                person_pronounLIST[parseResultDICT["result_pos"].index(p)].extend([(pn.start(), pn.end(), pn.group(0)) for pn in list(pronounPat.finditer(p))])
    if not indexWithPOS:
        person_pronounLIST = _segIndexConverter(parseResultDICT, person_pronounLIST)
    return person_pronounLIST

def getContentWordLIST(parseResultDICT, indexWithPOS=True):
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
            contentWordLIST.append([(c.start(), c.end(), c.group(0)) for c in list(contentPat.finditer(p))])
        else:
            contentWordLIST.append([])
    if not indexWithPOS:
        contentWordLIST = _segIndexConverter(parseResultDICT, contentWordLIST)
    return contentWordLIST

def getChemicalLIST(parseResultDICT, indexWithPOS=True):
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
            chemicalLIST.append([(c.start(), c.end(), c.group(0)) for c in list(chemicalPat.finditer(p))])
        else:
            chemicalLIST.append([])
    if not indexWithPOS:
        chemicalLIST = _segIndexConverter(parseResultDICT, chemicalLIST)
    return chemicalLIST

def getVerbStemLIST(parseResultDICT, indexWithPOS=True):
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
                verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(verbPPat.finditer(p))])
            else:
                verbLIST.append([(v.start(), v.end(), v.group(0)) for v in list(verbPat.finditer(p))])
        else:
            verbLIST.append([])
    if not indexWithPOS:
        verbLIST = _segIndexConverter(parseResultDICT, verbLIST)
    return verbLIST

def getNounStemLIST(parseResultDICT, indexWithPOS=True):
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
            nounLIST.append([(n.start(), n.end(), n.group(0)) for n in list(nounPat.finditer(p))])
        else:
            nounLIST.append([])
    if not indexWithPOS:
        nounLIST = _segIndexConverter(parseResultDICT, nounLIST)
    return nounLIST

def getTimeLIST(parseResultDICT, indexWithPOS=True):
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
            timeLIST.append([(l.start(), l.end(), l.group(0)) for l in list(timePat.finditer(p))])
        else:
            timeLIST.append([])
    if not indexWithPOS:
        timeLIST = _segIndexConverter(parseResultDICT, timeLIST)
    return timeLIST

def getLocationStemLIST(parseResultDICT, indexWithPOS=True):
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
            locationLIST.append([(l.start(), l.end(), l.group(0)) for l in list(locationPat.finditer(p))])
        else:
            locationLIST.append([])
    if not indexWithPOS:
        locationLIST = _segIndexConverter(parseResultDICT, locationLIST)
    return locationLIST

def getOpenDataPlaceLIST(parseResultDICT, indexWithPOS=True):
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
            placeLIST.append([(l.start(), l.end(), l.group(0)) for l in list(placePat.finditer(p))])
        else:
            placeLIST.append([])
    if not indexWithPOS:
        placeLIST = _segIndexConverter(parseResultDICT, placeLIST)
    return placeLIST

def getQuestionLIST(parseResultDICT, indexWithPOS=True):
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
            tmpLIST = [q for q in list(clausePat.finditer(p))]
            if tmpLIST:
                for q in tmpLIST:
                    questionLIST.append([(q.group(0), "".join([x.group(0) for x in stripPat.finditer(p)])) for q in list(clausePat.finditer(p))])
            else:
                questionLIST.append([])
        else:
            questionLIST.append([])
    if not indexWithPOS:
        questionLIST = _segIndexConverter(parseResultDICT, questionLIST)
    return questionLIST

def getAddTWLIST(parseResultDICT, indexWithPOS=True):
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
            addTWLIST.append([(a.start(), a.end(), a.group(0)) for a in list(addTWPat.finditer(p))])
        else:
            addTWLIST.append([])
    if not indexWithPOS:
        addTWLIST = _segIndexConverter(parseResultDICT, addTWLIST)
    return addTWLIST

def getCurrencyLIST(parseResultDICT, indexWithPOS=True, greedyBOOL=False):
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
            currencyLIST.append([(c.start(), c.end(), c.group(0)) for c in list(currencyPat.finditer(p))])
            if greedyBOOL:
                greedyLIST = []
                try:
                    if parseResultDICT["result_pos"][i-1][-14:] == "</ENTITY_noun>" and parseResultDICT["result_pos"][i-1][-15] in "元金幣圜圓比布索鎊盾銖令朗郎":
                        greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(currencyGreedyGapPat.finditer(p))]
                except:
                    pass
                if greedyLIST:
                    greedyLIST.extend([(c.start(), c.end(), c.group(0)) for c in list(currencyGreedyPat.finditer(p))])
                else:
                    greedyLIST = [(c.start(), c.end(), c.group(0)) for c in list(currencyGreedyPat.finditer(p))]
                if greedyLIST:
                    currencyLIST[-1].extend(greedyLIST)
        else:
            currencyLIST.append([])
    if not indexWithPOS:
        currencyLIST = _segIndexConverter(parseResultDICT, currencyLIST)
    return currencyLIST

def getWikiDataLIST(parseResultDICT, indexWithPOS=True):
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
            wikiDataLIST.append([(n.start(), n.end(), n.group(0)) for n in list(wikiDataPat.finditer(p))])
        else:
            wikiDataLIST.append([])
    if not indexWithPOS:
        wikiDataLIST = _segIndexConverter(parseResultDICT, wikiDataLIST)
    return wikiDataLIST


class LawsToolkit:
    def __init__(self, articutResult):
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
        articleLIST = list(set([self.tagPurger(a.group(0)) for a in re.finditer(self.articlePat, "".join(self.articutResult["result_pos"]))]))
        return articleLIST

    def getCrime(self, parseResultDICT={}):
        '''
        取得罪名
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT
        crimePosLIST = set([c.group(0) for c in re.finditer(self.crimePat, "".join(self.articutResult["result_pos"]))])
        crimeTextLIST = [self.tagPurger(c) for c in crimePosLIST]
        return crimeTextLIST

    def getCriminalResponsibility(self, parseResultDICT={}):
        '''
        取得刑責
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT
        try:
            crPosLIST = set([c.group(0) for c in re.finditer(self.criminalResponsibilityPat, "".join(self.articutResult["result_pos"]))])
            crTextLIST = [self.tagPurger(c) for c in crPosLIST]
            return crTextLIST
        except KeyError:
            return []

    def getEventRef(self, parseResultDICT={}):
        '''
        取得「所受(之)XX」的列表
        '''
        if parseResultDICT:
            self.articutResult = parseResultDICT
        erPosLIST = set([e.group(0) for e in re.finditer(self.eventRefPat, "".join(self.articutResult["result_pos"]))])
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

