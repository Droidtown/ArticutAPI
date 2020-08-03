#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Exchange

    Input:
        pattern       str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_Exchange = True

#建立貨幣名稱代碼轉換字典
currencyCodeDICT = {"美金":"USD", "美元":"USD", "日幣":"JPY", "日圓":"JPY", "日元":"JPY",
                    "台幣":"TWD", "臺幣":"TWD", "新台幣":"TWD", "新臺幣":"TWD", "歐元":"EUR"}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(intent, args):
    if DEBUG_Exchange:
        print(intent, "===>", args)

def getResult(pattern, args, resultDICT):
    # [我]想要[美金][100元]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[想要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
        debugInfo("[我]想要[美金][100元]", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = None
        resultDICT["amount"] = args[2]

    # [我]想要[100元][美金]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[想要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想要][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[我]想要[100元][美金]", args)
        resultDICT["source"] = args[2]
        resultDICT["target"] = None
        resultDICT["amount"] = args[1]

    # [我]想買[美金][100元]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[想買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
        debugInfo("[我]想買[美金][100元]", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = None
        resultDICT["amount"] = args[2]

    # [我]想買[100元][美金]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[想買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[想買][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[我]想買[100元][美金]", args)
        resultDICT["source"] = args[2]
        resultDICT["target"] = None
        resultDICT["amount"] = args[1]

    # [美金][100]要多少[台幣]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[美金][100]要多少[台幣]", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [美金][100]要[台幣]多少
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[美金][100]要[台幣]多少", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [美金][100元]要多少[台幣]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[美金][100元]要多少[台幣]", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [美金][100元]要[台幣]多少
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[美金][100元]要[台幣]多少", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [美金][100元]可以兌換多少[台幣]
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[美金][100元]可以兌換多少[台幣]", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [美金][100元]可以兌換[台幣]多少
    if pattern == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[美金][100元]可以兌換[台幣]多少", args)
        resultDICT["source"] = args[0]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[1]

    # [100美金]要多少[台幣]
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[100美金]要多少[台幣]", args)
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    # [100美金]要[台幣]多少
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[100美金]要[台幣]多少", args)
        resultDICT["source"] = [x for x in currencyCodeDICT if x in args[0]][0]
        resultDICT["target"] = args[1]
        resultDICT["amount"] = args[0]

    # [100元][美金]要多少[台幣]
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[100元][美金]要多少[台幣]", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    # [100元][美金]要[台幣]多少
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[100元][美金]要[台幣]多少", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    # [100元][美金]可以兌換多少[台幣]
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
        debugInfo("[100元][美金]可以兌換多少[台幣]", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    # [100元][美金]可以兌換[台幣]多少
    if pattern == "<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[100元][美金]可以兌換[台幣]多少", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = args[0]

    # [今天][美金]兌換[台幣]是多少
    if pattern == "<TIME_day>[^<]*?</TIME_day><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[今天][美金]兌換[台幣]是多少", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = None

    # [上星期三][美金]兌換[台幣]是多少
    if pattern == "<TIME_week>[^<]*?</TIME_week><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[兌換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[兌換][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
        debugInfo("[上星期三][美金]兌換[台幣]是多少", args)
        resultDICT["source"] = args[1]
        resultDICT["target"] = args[2]
        resultDICT["amount"] = None

    return resultDICT