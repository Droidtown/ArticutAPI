#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Question

    Input:
        pattern       str,
        utterance     str,
        args          str[],
        questionDICT    dict

    Output:
        questionDICT    dict
"""

from intentFunction import *

DEBUG_Question = True
userDefinedDICT = {'小強': ['小剛', '小正', '小紅', '小明', '明明', '小方', '樂樂', '冬冬', '小優'], '時速': [''], '獵豹': [''], '畫片': [''], '植物園': [''], '黃阿姨': ['']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Question:
        print("[Question]")
        print("{} ===> {}\n".format(utterance, args))
        #print("Pattern:", pattern)

def getResult(pattern, utterance, args, inputUtterance, questionDICT):
    debugInfo(pattern, utterance, args)

    if utterance == "共賣出幾[雙][鞋子]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "一共做了多少[個][作品]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "一共吃了幾[顆][巧克力]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "總共有幾人":
        subject, entity, entityAmount, questionDICT = inTotal("", "", "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(entityAmount)])

    if utterance == "總共有幾[條][小魚]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "共包了幾[個][粽子]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "一共有[氣球]多少[個]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[0], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], entityAmount, args[1])])

    if utterance == "一共做了多少[個][蝴蝶][結]":
        entity = args[1]+args[2]
        subject, entity, entityAmount, questionDICT = inTotal("", entity, args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[0])])

    if utterance == "剩下幾[個]":
        subject, entity, entityAmount, questionDICT = difference("", "", args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[0])])

    if utterance == "剩下幾[個][小魚]":
        subject, entity, entityAmount, questionDICT = difference("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "還有幾[條][小魚]":
        subject, entity, entityAmount, questionDICT = difference("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "還剩幾[條][小魚]":
        subject, entity, entityAmount, questionDICT = difference("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "還剩下多少[張]":
        subject, entity, entityAmount, questionDICT = difference("", "", args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[0])])

    if utterance == "[男生]有幾人":
        subject, entity, entityAmount, questionDICT = inTotal("", args[0], "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}人".format(args[0], entityAmount)])

    if utterance == "[植物園][裡]有多少人":
        subject, entity, entityAmount, questionDICT = inTotal(args[0]+args[1], "", "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, "人")])

    if utterance == "[小威]拍了幾[下]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], entityAmount, args[1])])

    if utterance == "[王子]做了幾[下]仰臥起坐":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_仰臥起坐={}{}".format(args[0], entityAmount, args[1])])

    if utterance == "[小華]剩下幾[顆][蘋果]":
        subject, entity, entityAmount, questionDICT = difference(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[小玉]吃了幾[顆][草莓]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[小梅]換了幾[隻][熊寶貝]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[小毛]摺了幾[架][紙飛機]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[小萱]寫了幾[行][國字]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[1]+args[2])])

    if utterance == "[家民]買了幾[枝][自動鉛筆]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])

    if utterance == "[他們]總共有幾元":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", "元", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}元".format(entityAmount)])

    if utterance == "[蘋果]總共有幾[顆]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[0], args[1], questionDICT)
        if subject == "":
            questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])
        else:
            questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, entity, entityAmount, args[1])])

    if utterance == "[冰箱][裡]總共有幾[顆]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0]+args[1], "", args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, entity, entityAmount, args[2])])

    if utterance == "[皇后]有幾[顆][寶石]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[公主]有幾[顆][紅][寶石]":
        entity = args[2]+args[3]
        subject, entity, entityAmount, questionDICT = inTotal(args[0], entity, args[1], questionDICT)
        if subject == "":
            questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])
        else:
            questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, entity, entityAmount, args[1])])

    if utterance == "[豬肉]比[牛肉]多幾[片]":
        entityAmount, questionDICT = comparative("", args[0], "", args[1], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[2])])

    if utterance == "[豬肉]比[牛肉]少幾[片]":
        entityAmount, questionDICT = comparative("", args[0], "", args[1], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[2])])

    if utterance == "[棒虎]比[小福][多]得幾分":
        entityAmount, questionDICT = comparative(args[0], "", args[1], "", "分", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}分".format(entityAmount)])

    if utterance == "[自己]還有幾元":
        if args[0] == "自己":
            subject, entity, entityAmount, questionDICT = inTotal("", "", "元", questionDICT)
        else:
            subject, entity, entityAmount, questionDICT = inTotal(args[0], "", "元", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}元".format(entityAmount)])

    if utterance == "[哥哥]總共用多少元":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", "元", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}元".format(entityAmount)])

    if utterance == "[姊姊]踢了幾[下]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], entityAmount, args[1])])

    if utterance == "[乙數]是多少":
        subject, entity, entityAmount, questionDICT = inTotal("", args[0], "", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}".format(args[0], entityAmount)])

    if utterance == "有多少[個][梨]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[1], args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[0])])

    if utterance == "[老師]還有幾[條][緞帶]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], entityAmount, args[1])])

    if utterance == "[快餐店]還有[漢堡]多少[個]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[1], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], entityAmount, args[2])])

    if utterance == "[球場][上]共有幾人":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, "", "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_人={}人".format(subject, entityAmount)])

    if utterance == "[撲滿][裡]共有幾元":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, "", "元", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}元".format(subject, entityAmount)])

    if utterance == "[海盜船][上]還剩下幾[個][海盜]":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, args[3], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[2])])

    if utterance == "[舞台][上]有幾[個][演員]":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, args[3], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[3], entityAmount, args[2])])

    if utterance == "[花瓶][裡]有幾[朵][白][玫瑰]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0]+args[1], args[3]+args[4], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[2])])

    if utterance == "[海盜船][上]還有幾[個][海盜]":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, args[3], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[2])])

    if utterance == "[魚缸][裡][現在]有幾[條][熱帶魚]":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, args[4], args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[4])])

    if utterance == "[公車][上][現在]還有幾人":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal(subject, "", "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_人={}人".format(subject, entityAmount)])

    if utterance == "[架][上][現在]還有幾[本][故事書]":
        subject = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = difference(subject, args[4], args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[4], entityAmount, args[3])])

    if utterance == "[小美][現在]有幾[張]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[2])])

    if utterance == "[二]班用了多少[張][紙]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0]+"班", args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}班={}{}".format(args[0], entityAmount, args[1])])

    if utterance == "[兩個]班一共用了多少[張]":
        subject, entity, entityAmount, questionDICT = inTotal("", "", args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])

    if utterance == "[黑][珠子]有幾[顆]":
        entity = args[0]+args[1]
        subject, entity, entityAmount, questionDICT = inTotal("", entity, args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[2])])

    if utterance == "[兩天]共賣出幾[雙][鞋子]":
        subject, entity, entityAmount, questionDICT = inTotal("", args[2], args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])

    if utterance == "[現在]總共有幾[顆]":
        subject, entity, entityAmount, questionDICT = inTotal("", "", args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[1])])

    if utterance == "[哥哥]總共花掉多少元":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], "", "元")
        questionDICT["Process"].append([inputUtterance, "{}元".format(entityAmount)])

    if utterance == "[楊阿姨]已經打了多少[個][字]":
        subject, entity, entityAmount, questionDICT = inTotal(args[0], args[2], args[1])
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[1]+args[2])])

    if utterance == "[現在][瑋瑋]有幾元":
        subject, entity, entityAmount, questionDICT = inTotal(args[1], "", "元", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}元".format(args[1], entityAmount)])

    if utterance == "[現在][球場][上]共有幾人":
        subject = args[1]+args[2]
        subject, entity, entityAmount, questionDICT = inTotal(subject, "", "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_人={}人".format(subject, entityAmount)])

    if utterance == "[現在][舞台][上]有幾[個][演員]":
        subject = args[1]+args[2]
        subject, entity, entityAmount, questionDICT = inTotal(subject, args[4], args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[4], entityAmount, args[3])])

    if utterance == "[小湘]比[小強]多幾[張][紙]":
        entityAmount, questionDICT = comparative(args[0], args[3], args[1], args[3], args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[2])])

    if utterance == "[媽媽]比[黃阿姨][多]買幾[個][月餅]":
        entityAmount, questionDICT = comparative(args[0], args[4], args[1], args[4], args[3])
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, args[3])])

    if utterance == "[姊姊]比[哥哥][少]買幾[枝]":
        subject, entity, entityAmount, questionDICT = inTotal("", "", args[3])
        entityAmount, questionDICT = comparative(args[0], entity, args[1], entity, args[3])
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, entityAmount, args[3])])

    if utterance == "[紅][風車]比[藍][風車]多幾[枝]":
        entityAmount, questionDICT = comparative("", args[0]+args[1], "", args[2]+args[3], unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, unit)])

    if utterance == "[紅][風車]比[藍][風車]少幾[枝]":
        entityAmount, questionDICT = comparative("", args[0]+args[1], "", args[2]+args[3], unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(entityAmount, unit)])

    if utterance == "[昨天]比[今天][少]摺了幾[隻][紙鶴]":
        entityAmount, questionDICT = comparative(args[0], args[4], args[1], args[4], args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[4], entityAmount, args[3])])

    if utterance == "[二]年級[三]班比[二]年級[一]班多幾人":
        subject1 = args[1]+"班"
        subject2 = args[3]+"班"
        entity = args[0] + "年級"
        entityAmount, questionDICT = comparative(subject1, entity, subject2, entity, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(entityAmount)])

    if utterance == "[二]年級[三]班比[二]年級[一]班少幾人":
        subject1 = args[1]+"班"
        subject2 = args[3]+"班"
        entity = args[0] + "年級"
        entityAmount, questionDICT = comparative(subject1, entity, subject2, entity, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(entityAmount)])

    if utterance == "[二]年級[一]班和[二]年級[二]班共有多少人":
        entity = args[0]+"年級"
        entityAmount = inTotal(args[1]+"班", entity, "人")[2] + inTotal(args[3]+"班", entity, "人",  questionDICT)[2]
        questionDICT["Process"].append([inputUtterance, "{}人".format(entityAmount)])

    ###############################################################################################
    # 未實做

    if utterance == "還剩多少[噸]":
        # write your code here
        pass

    if utterance == "比原計畫增產多少[打]":
        # write your code here
        pass

    if utterance == "[媽媽]帶了多少[錢]":
        # write your code here
        pass

    if utterance == "[梨]有多少[公斤]":
        # write your code here
        pass

    if utterance == "[商店]有[蘋果]多少[公斤]":
        # write your code here
        pass

    if utterance == "有幾[球]沒投進":
        # write your code here
        pass

    if utterance == "還需要多少人":
        # write your code here
        pass

    if utterance == "應找回多少[元]":
        # write your code here
        pass

    if utterance == "上車的[人][中]有多少人站著":
        # write your code here
        pass

    if utterance == "共有幾人在排隊":
        # write your code here
        pass

    if utterance == "[水果]多少[公斤]":
        # write your code here
        pass

    if utterance == "[收入]多少[萬元]":
        # write your code here
        pass

    if utterance == "[獵豹]最快時速比[馬]最快時速快多少":
        # write your code here
        pass

    if utterance == "[蘋果]和[梨]一共有多少[公斤]":
        # write your code here
        pass

    if utterance == "[商店]還有[水果]多少[公斤]":
        # write your code here
        pass

    if utterance == "[洋娃娃]和[猴子]各[一個]一共需要多少元":
        # write your code here
        pass

    if utterance == "還有多少人沒捉住":
        # write your code here
        pass

    if utterance == "還有多少[個]沒捉住":
        # write your code here
        pass

    if utterance == "[三盒]總共有幾[個][罐頭]":
        # write your code here
        pass

    if utterance == "[兩桶][油]共重多少[公斤]":
        # write your code here
        pass

    return questionDICT