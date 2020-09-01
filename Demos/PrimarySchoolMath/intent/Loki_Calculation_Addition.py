#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Calculation_Addition

    Input:
        pattern       str,
        utterance     str,
        args          str[],
        questionDICT    dict

    Output:
        questionDICT    dict
"""

from intentFunction import *

DEBUG_Calculation_Addition = True
userDefinedDICT = {'小強': ['小剛', '小正', '小紅', '小明', '明明', '小方', '樂樂', '冬冬', '小優']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Calculation_Addition:
        print("[Calculation_Addition]")
        print("{} ===> {}\n".format(utterance, args))
        #print("Pattern:", pattern)

def getResult(pattern, utterance, args, inputUtterance, questionDICT):
    debugInfo(pattern, utterance, args)
    if "比"+args[0] in inputUtterance:
        return questionDICT

    if utterance == "借給[小強][4本][後]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "吃了[5顆]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit ,questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "得到[20元]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, amount, unit)])

    if utterance == "挑走了[17個][作品]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[1], -amount, unit)])

    if utterance == "摘採[6個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "放入[2個][籃球]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "游來[2條][熱帶魚]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "現做[30個][甜甜圈]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "用去[38張]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "用了[8元]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "移走[5個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "給[虎客][8塊]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "謝了[4朵]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit,questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "賣掉[1個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "購進[小提琴][52把]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[0], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[0], amount, unit)])

    if utterance == "運進[21個][作品]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "離開[8個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "借出[40本]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "壞掉[6個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "吃了[9顆][巧克力]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[1], -amount, unit)])

    if utterance == "[小娟]做了[3個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[維尼]做了[7個][蝴蝶]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[維尼]做了[7個][蝴蝶][結]":
        numberSTR, amount = amountSTRconvert(args[1])
        entity = args[2]+args[3]
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[國王]做了[4][下]仰臥起坐":
        numberSTR, amount = amountSTRconvert(args[1])
        subject, entity, questionDICT = transitive(args[0], "", amount, args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[0], amount, args[2])])

    if utterance == "[奶奶]包了[13個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[奶奶]包了[13個][粽子]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[小剛]吃了[3個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[小正]吃了[9顆][巧克力]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[2], -amount, unit)])

    if utterance == "[棕熊]堆疊了[28個][魚罐頭]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[哥哥]幫[弟弟]買[糖果]花掉[100元]":
        numberSTR, amount = amountSTRconvert(args[3])
        unit = args[3].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[0], -amount, unit)])

    if utterance == "[小福]得[42分]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[0], amount, unit)])

    if utterance == "[小俊]拍球拍了[5][下]":
        subject, entity, questionDICT = transitive(args[0], "", int(args[1]), args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[0], args[1], args[2])])

    if utterance == "[弟弟]踢了[6][下]":
        numberSTR, amount = amountSTRconvert(args[1])
        questionDICT = existential(args[0], "", amount, args[2], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, args[2])])

    if utterance == "[妹妹]拿走了[5個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[小傑]換了[7隻][熊寶貝]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[船長]準備了[12片][牛肉]和[4片][豬肉]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], args[2], amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[3])
        unit = args[3].replace(numberSTR, "")
        questionDICT = existential(args[0], args[4], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{0}_{1}+{2}; {0}_{3}+{4}".format(args[0], args[2], args[1], args[4], args[3])])

    if utterance == "[廚師]烤了[15塊][餅乾]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[自己]也花掉[20元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        if args[0] == "自己":
            subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        else:
            subject, entity, questionDICT = transitive(args[1], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[媽媽]買了[兩枝]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}+{}{}".format(args[0], entity, amount, unit)])

    if utterance == "[媽媽]購買了[12個][月餅]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[養殖場]養了[93隻][雞]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[小明]第[一天]讀了[47頁]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("第"+args[1], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[老師]又放上了[4本]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[爸爸]又給[他][15元]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[1], "", amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[叔叔]又買[9隻]放進來":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[叔叔]又送給[我們][5顆]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[1], "", amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[小木偶]再放進[6元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(subject, amount, unit)])

    if utterance == "[姊姊]再給[他][4張]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[1], "", amount, unit, questionDICT)
        subject, entity, questionDICT = transitive(args[0], entity, -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[小兔]摘了[136個][果子]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[大毛]摺了[14架][紙飛機]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[小宏]買給[小華][4顆][蘋果]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[1], args[3], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}; ".format(args[1], amount, unit)])

    if utterance == "[花園][裡]開了[11朵][白花]和[8朵][紅花]":
        subject = args[0]+args[1]
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, args[3], amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[4])
        unit = args[4].replace(numberSTR, "")
        questionDICT = existential(subject, args[5], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{0}_{1}+{2}; {0}_{3}+{4}".format(subject, args[3], args[2], args[5], args[4])])

    if utterance == "[花園][裡]的[玉蘭花]開了[12朵]":
        numberSTR, amount = amountSTRconvert(args[3])
        subject = args[0]+args[1]
        unit = args[3].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(subject, args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[小優][上午]吃了[9顆][巧克力]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[3], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[3], amount, unit)])

    if utterance == "[鞋店][昨天]賣出[6雙][鞋子]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(args[0], args[3], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(args[3], -amount, unit)])

    if utterance == "[4個]下台[後]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[6個]壞掉[後]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "有[8]人下車":
        numberSTR, amount = amountSTRconvert(args[0])
        subject, entity, questionDICT = transitive("", "", -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(amount)])

    if utterance == "[8片][光碟]放回[CD][盒][裡]":
        numberSTR, amount = amountSTRconvert(args[0])
        subject = args[2]+args[3]+args[4]
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive(subject, args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "[2]班借走了[14個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        subject = args[0]+"班"
        subject, entity, questionDICT = transitive(subject, entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "[1]班還回來[9個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[一]班用了[15張][紙]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject = args[0] + "班"
        subject, entity, questionDICT = transitive(subject, args[2], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}-{}{}".format(subject, amount, unit)])

    if utterance == "第[二天]讀了[53頁]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("第"+args[0], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "又來了[10]人":
        numberSTR, amount = amountSTRconvert(args[0])
        subject, entity, questionDICT = transitive("", "", amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "+{}人".format(amount)])

    if utterance == "又游來[2條][魟魚]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "又移走[3個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(entity, -amount, unit)])

    if utterance == "又跑來[6隻]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "又給[弟弟][10元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject1, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        subject2, entity, questionDICT = transitive(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{0}+{1}{2}; {3}-{1}{2}".format(args[0], amount, unit, subject1)])

    if utterance == "又購買了[4條]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "又跑來了[2隻][綠][頭鴨]":
        numberSTR, amount = amountSTRconvert(args[0])
        entity = args[1]+args[2]
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "又運進[21個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "又開來[13輛]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "其他的是[鴨蛋]":
        ent, amount, unit, questionDICT = intransitive(args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "其他的是[草莓][派]":
        ent, amount, unit, questionDICT = intransitive(args[0]+args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "其他的是[綠][蘋果]":
        ent, amount, unit, questionDICT = intransitive(args[0]+args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "其餘的是[小雞]":
        ent, amount, unit, questionDICT = intransitive(args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "其餘的全部是[蘋果][樹]":
        ent, amount, unit, questionDICT = intransitive(args[0]+args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "其餘的是[紅][蘋果]":
        ent, amount, unit, questionDICT = intransitive(args[0]+args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "剩餘的是[柳樹]":
        ent, amount, unit, questionDICT = intransitive(args[0], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "剩餘的是[蘋果][樹]":
        ent, amount, unit, questionDICT = intransitive(args[0]+args[1], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}{}".format(ent, -amount, unit)])

    if utterance == "再堆疊[10個]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "再放入[8個][排球]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[1], amount, unit)])

    if utterance == "再游來[1條]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(entity, amount, unit)])

    if utterance == "[昨天]賣出[6雙][鞋子]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[0].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}+{}{}".format(args[2], amount, unit)])

    if utterance == "[上午]來了[遊客][583]人":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, entity, questionDICT = transitive("", args[1], amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "+{}人".format(amount)])

    if utterance == "[中午]走了[107]人":
        numberSTR, amount = amountSTRconvert(args[1])
        subject, entity, questionDICT = transitive("", "", -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(-amount)])

    if utterance == "[中午]有[215]人離去":
        numberSTR, amount = amountSTRconvert(args[1])
        subject, entity, questionDICT = transitive("", "", -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}人".format(-amount)])

    if utterance == "[中午]離去[186]人":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject, entity, questionDICT = transitive("", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}".format(-amount, unit)])

    ###############################################################################################
    # 未實做

    if utterance == "[商店]運來[蘋果][38公斤]":
        # write your code here
        pass

    if utterance == "已經參觀過[博物館]的有[398]人":
        # write your code here
        pass

    if utterance == "已經捉住了[4個]":
        # write your code here
        pass

    if utterance == "已經捉住了[4]人":
        # write your code here
        pass

    if utterance == "已經捉到了其中的[3個][人]":
        # write your code here
        pass

    if utterance == "已經生產了[653塊]":
        # write your code here
        pass

    if utterance == "先運走[45.2噸]":
        # write your code here
        pass

    if utterance == "已經量了[身高]的有[396]人":
        # write your code here
        pass

    if utterance == "上來了[9]人":
        # write your code here
        pass

    if utterance == "上車[19]人":
        # write your code here
        pass

    if utterance == "下車[12]人":
        # write your code here
        pass

    if utterance == "付給[售貨員][15元]":
        # write your code here
        pass

    if utterance == "做[數學][作業]用去[0.15小時]":
        # write your code here
        pass

    if utterance == "做了[3個]":
        # write your code here
        pass

    if utterance == "參加[美術][小組]的有[12]人":
        # write your code here
        pass

    if utterance == "參加了[3個][興趣][小組]":
        # write your code here
        pass

    if utterance == "找回了[13.37元]":
        # write your code here
        pass

    if utterance == "投進了[6]球":
        # write your code here
        pass

    if utterance == "拿到[4個]":
        # write your code here
        pass

    if utterance == "有[2個][小朋友]請假":
        # write your code here
        pass

    if utterance == "有[四]人下台":
        # write your code here
        pass

    if utterance == "洗米需要[1分鐘]":
        # write your code here
        pass

    if utterance == "炒菜需要[10分鐘]":
        # write your code here
        pass

    if utterance == "煮飯需要[15分鐘]":
        # write your code here
        pass

    if utterance == "生產[4500雙][涼鞋]":
        # write your code here
        pass

    if utterance == "用去[1.6公尺]":
        # write your code here
        pass

    if utterance == "用去[0.15小時]":
        # write your code here
        pass

    if utterance == "訂《[少年報]》的有[40]人":
        # write your code here
        pass

    if utterance == "訂《[小主][人報]》的有[25]人":
        # write your code here
        pass

    if utterance == "買[鋼筆]用去[3.2元]":
        # write your code here
        pass

    if utterance == "買了[水壺][後]還剩[57元]":
        # write your code here
        pass

    if utterance == "買了[四個][蛋糕]":
        # write your code here
        pass

    if utterance == "買了[48.2元]的[零食]和[18.43元]的[文具]":
        # write your code here
        pass

    if utterance == "賣出[42公斤]":
        # write your code here
        pass

    if utterance == "運來[57公斤][水果]":
        # write your code here
        pass

    if utterance == "運進[21個]":
        # write your code here
        pass

    if utterance == "[小紅]拿了[60元]":
        # write your code here
        pass

    if utterance == "[他]付出[50元]":
        # write your code here
        pass

    if utterance == "[小明]做[數學][作業]用去[0.15小時]":
        # write your code here
        pass

    if utterance == "[媽媽]帶[100元]":
        # write your code here
        pass

    if utterance == "[學校]挑走了[17個][作品]":
        # write your code here
        pass

    if utterance == "[小豬]摘的[個數]和[小兔]同樣多":
        # write your code here
        pass

    if utterance == "[他]獲得[29枚][金牌]":
        # write your code here
        pass

    if utterance == "[小明]已經看了[100頁]":
        # write your code here
        pass

    if utterance == "[老師]說要[11枝][鉛筆]":
        # write your code here
        pass

    if utterance == "[樂樂]買[書]用去[8.55元]":
        # write your code here
        pass

    if utterance == "[阿姨]打[一份][1000個][字]":
        # write your code here
        pass

    if utterance == "[哥哥]自己也花掉[20元]":
        # write your code here
        pass

    if utterance == "[叔叔]又買[7隻][鴨子]放進來":
        # write your code here
        pass

    if utterance == "[小欣][昨天]摺了[4隻][紙鶴]":
        # write your code here
        pass

    if utterance == "公園[裡]新種[359棵]樹":
        # write your code here
        pass

    if utterance == "[3隻][貓]上車[後]":
        # write your code here
        pass

    if utterance == "[4個][人]下台[後]":
        # write your code here
        pass

    if utterance == "[8片][光碟]放回[盒子][裡]":
        # write your code here
        pass

    if utterance == "[108]人上船":
        # write your code here
        pass

    if utterance == "[4]人下台[後]":
        # write your code here
        pass

    if utterance == "第[一天]看了[24頁]":
        # write your code here
        pass

    if utterance == "第[二天]看的與第[一天]同樣多":
        # write your code here
        pass

    if utterance == "又還回[285本]":
        # write your code here
        pass

    if utterance == "又拿到[4個]":
        # write your code here
        pass

    if utterance == "又買[9隻]放進來":
        # write your code here
        pass

    if utterance == "又買[9隻][鴨子]放進來":
        # write your code here
        pass

    if utterance == "[英國]獲得[29枚][金牌]":
        # write your code here
        pass

    if utterance == "[後面]還有[7]人":
        # write your code here
        pass

    if utterance == "[上午]做了[38朵]":
        # write your code here
        pass

    if utterance == "[今天]摺了[46隻]":
        # write your code here
        pass

    if utterance == "[上午]收[雞蛋][85公斤]":
        # write your code here
        pass

    if utterance == "[今天]有[2個][小朋友]請假":
        # write your code here
        pass

    if utterance == "[上午]賣出[132公斤]":
        # write your code here
        pass

    if utterance == "[下午]購進[145公斤]":
        # write your code here
        pass


    return questionDICT