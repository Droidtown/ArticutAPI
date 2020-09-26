#!/usr/bin/env python3
# -*- coding:utf-8 -*-

caseLIST = [
    "吳金順於108年8月21日下午6時18分許起，接到詐欺集團成員佯裝為其友人之電話向其借款云云，致其陷於錯誤，因而先後於108年8月22日中午12時37分許、同日下午2時50分許，在桃園市桃園區中山東路32之20號之5陽信商業銀行桃園分行，臨櫃匯款15萬元、25萬元至右列帳戶。",
    "林凌強於108年8月22日晚間7時30分許，接到詐欺集團成員佯裝為廠商人員，佯稱須依其指示操作始得取消重複訂單云云，致其陷於錯誤，因而於同日晚間8時17分許、8時26分許，在新北市淡水區民族路56號全家便利商店淡水竹勝店，轉帳2萬9,989元2筆至右列帳戶。",
    "陳純於108年7月25日下午3時13分許，接到詐欺集團成員佯裝為姪子陳英傑之電話向其借款云云，致其陷於錯誤，因而於108年7月26日上午11時44分許，在臺北市松山區南京東路5段184號1樓臺灣銀行中崙分行，臨櫃匯款15萬元至右列帳戶。",
    "沈末葉於108年7月31日下午3時17分許起，接到詐欺集團成員佯裝為其同學陳雪瑩之電話向其借款云云，致其陷於錯誤，因而於108年8月1日下午3時44分許，在臺中市北屯區文心路4段281號玉山商業銀行文心分行，臨櫃匯款29萬8,000元至右列帳戶。",
    "陳翁淑娟於108年7月30日晚間8時許起，接到詐欺集團成員佯裝為姚姓廠商朋友之電話向其借款云云，致其陷於錯誤，因而於108年8月1日下午3時13分許，由其媳婦范馨尹在高雄市三民區鼎力路142號陽信銀行鼎力分行，臨櫃匯款3萬元至右列帳戶。,"
]

entityReLIST = ["(<ENTITY_pronoun>[^<]*?</ENTITY_pronoun>)",
                "(<ENTITY_noun>[^<]*?</ENTITY_noun>)",
                "(<ENTITY_nounHead>[^<]*?</ENTITY_nounHead>)",
                "(<ENTITY_nouny>[^<]*?</ENTITY_nouny>)",
                "(<ENTITY_oov>[^<]*?</ENTITY_oov>)",
                "(<UserDefined>)[^<]*?(</UserDefined>)"]
entityReSTR = "(<ENTITY_possessive>[^<]*?</ENTITY_possessive>)?"+"|".join(entityReLIST)

from ArticutAPI.ArticutAPI import Articut

import json
import re

def graphExtractor_verb(posSTR, verbSTR):
    ''''
    從輸入的字串中，抓出以 verbSTR 為核心的，前後實體 (Entity) 關係。
    '''

    pat = re.compile("({})+(?:(?!<ACTION_verb>.).)*?<ACTION_verb>{}</ACTION_verb>(?:(?!<ACTION_verb>.).)*?({})+".format(entityReSTR, verbSTR, entityReSTR))
    resultLIST = [re.sub("<AUX>[^<]*</AUX>", "", p.group(0)) for p in pat.finditer(posSTR)]
    return resultLIST

def graphSubjectExtractor(posSTR, verbSTR):
    '''
    取出動詞 verbSTR 之前的實體，做為主詞 subject
    '''
    pat = re.compile("({})+(?:(?!<ACTION_verb>.).)*?(?=<ACTION_verb>{})".format(entityReSTR, verbSTR))
    resultLIST = [p.group(0) for p in re.finditer(pat, posSTR)]
    return resultLIST

def graphObjectExtractor(posSTR, verbSTR):
    '''
    取出動詞 verbSTR 之後的實體，做為受詞 object
    '''
    pat = re.compile("(?<={}</ACTION_verb>)(?:(?!<ACTION_verb>.).)*?({})+".format(verbSTR, entityReSTR))
    resultLIST = [p.group(0) for p in re.finditer(pat, posSTR)]
    return resultLIST

def posTagPurger(posSTR):
    '''
    移除 POS 的標記，並把所有的詞彙結合成單一字串
    '''
    pat = re.compile("</?[a-zA-Z]+(_[a-zA-Z]+)?>")
    resultSTR = re.sub(pat, "", posSTR)
    return resultSTR

if __name__ == "__main__":

    with open("../../account.info", encoding="utf-8") as f:
        accountINFO = json.loads(f.read())
    myDICT = "./myDICT.json"

    articut = Articut(username=accountINFO["userName"], apikey=accountINFO["apiKey"])
    articutResult = articut.parse(caseLIST[-1], userDefinedDictFILE=myDICT)

    verbSTR = "佯裝"
    targetSentenceLIST = []
    for a in articutResult["result_pos"]:
        if verbSTR in a:
            targetSentenceLIST.append(graphExtractor_verb(a, "佯裝"))

    subjectLIST = []
    for t in targetSentenceLIST:
        for sentence in t:
            subjectLIST.append(posTagPurger(graphSubjectExtractor(sentence, verbSTR)[0]))

    objectLIST = []
    for t in targetSentenceLIST:
        for sentence in t:
            objectLIST.append(posTagPurger(graphObjectExtractor(sentence, verbSTR)[0]))


    print(subjectLIST)
    print(verbSTR)
    print(objectLIST)


