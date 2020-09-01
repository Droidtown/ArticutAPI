#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Calculation_Comparison

    Input:
        pattern       str,
        utterance     str,
        args          str[],
        questionDICT    dict

    Output:
        questionDICT    dict
"""

from intentFunction import *

DEBUG_Calculation_Comparison = True
userDefinedDICT = {'小優': ['小明', '小紅', '小強', '小晴', '小正'], '周新新': [''], '黃阿姨': ['']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Calculation_Comparison:
        print("[Calculation_Comparison]")
        print("{} ===> {}\n".format(utterance, args))
        #print("Pattern:", pattern)

def getResult(pattern, utterance, args, inputUtterance, questionDICT):
    debugInfo(pattern, utterance, args)

    if utterance == "[皇后]比[公主]多[8顆]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[妹妹]比[姊姊]少[5張]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}{}".format(args[0], args[1], -amount, unit)])

    if utterance == "[乙數]比[甲數]多[5]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, "", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}".format(args[0], args[1], args[2])])

    if utterance == "[乙數]比[甲數]少[5]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, "", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}".format(args[0], args[1], amount)])

    if utterance == "[男生]比[女生]多[2]人":
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", int(args[2]), "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}人".format(args[0], args[1], args[2])])

    if utterance == "[男生]比[女生]少[2]人":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}人".format(args[0], args[1], amount)])

    if utterance == "[3]班比[1]班多[3]人":
        numberSTR, amount = amountSTRconvert(args[2])
        subject1 = args[0] + "班"
        subject2 = args[1] + "班"
        subject, refOBJ, questionDICT = bitransitive(subject1, subject2, "", "", amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}人".format(args[0], args[1], amount)])

    if utterance == "[2]班比[3]班少[7]人":
        numberSTR, amount = amountSTRconvert(args[2])
        subject1 = args[0] + "班"
        subject2 = args[1] + "班"
        subject, refOBJ, questionDICT = bitransitive(subject1, subject2, "", "", -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}人".format(args[0], args[1], amount)])

    if utterance == "[哥哥]比[弟弟]多[5元]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[哥哥]比[弟弟]少[5元]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[王子]比[國王]多做[9][下]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, args[3])])

    if utterance == "[小明]比[小優]多吃了[7顆]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[大目]比[阿草]多吃了[5塊][小披薩]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], args[3], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[小萱]比[小玲]多寫[9行]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[小威]比[小俊]多拍[19][下]":
        subject1, subject2, questionDICT = bitransitive(args[0], args[1], "", "", int(args[2]), args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(subject1, subject2, args[2], args[3])])

    if utterance == "[小梅]比[他]多換[5隻]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], subject2, amount, unit)])

    if utterance == "[家民]比[她]多買[3枝]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(subject1, subject2, amount, unit)])

    if utterance == "[小毛]比[大毛]多摺了[8架]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[小毛]比[大毛]少摺了[8架]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(args[0], args[1], amount, unit)])

    if utterance == "[小毛]比[大毛]多摺了[8架][紙飛機]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], args[3], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}_{}+{}{}".format(args[0], args[1], args[3], amount, unit)])

    if utterance == "[小毛]比[大毛]少摺了[8架][紙飛機]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], args[3], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}_{}-{}{}".format(args[0], args[1], args[3], amount, unit)])

    if utterance == "[姊姊]比[弟弟]多踢[9][下]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject, refOBJ, questionDICT = bitransitive(args[0], args[1], "", "", amount, args[3], questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[1], amount, args[3])])

    if utterance == "[小玉]比[小美]少吃[3顆]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0], args[1], "", "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(subject1, subject2, amount, unit)])

    if utterance == "[二]班比[一]班多用了[6張][紙]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0]+"班", args[1]+"班", args[3], "", -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(subject1, subject2, amount, unit)])

    if utterance == "[二]班比[一]班少用了[6張][紙]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0]+"班", args[1]+"班", args[3], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(subject1, subject2, amount, unit)])

    if utterance == "[紅][氣球]比[藍][氣球]多[5個]":
        numberSTR, amount = amountSTRconvert(args[4])
        unit = args[4].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive("", "", args[0]+args[1], args[2]+args[3], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}{}={}{}+{}{}".format(args[0], args[1], args[2], args[3], amount, unit)])

    if utterance == "[白][玫瑰]比[紅][玫瑰]少[9朵]":
        entity1 = args[0]+args[1]
        entity2 = args[2]+args[3]
        numberSTR, amount = amountSTRconvert(args[4])
        unit = args[4].replace(numberSTR, "")
        subject, refOBJ, questionDICT = bitransitive("", "", entity1, entity2, -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(entity1, entity2, amount, unit)])

    if utterance == "[小白兔]的[蘿蔔]比[小灰兔]少[12根]":
        numberSTR, amount = amountSTRconvert(args[3])
        unit = args[3].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0], args[2], args[1], args[1], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}-{}{}".format(args[0], args[2], amount, unit)])

    if utterance == "[小白兔]的[蘿蔔]比[小灰兔]多[12根]":
        numberSTR, amount = amountSTRconvert(args[3])
        unit = args[3].replace(numberSTR, "")
        subject1, subject2, questionDICT = bitransitive(args[0], args[2], args[1], args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}+{}{}".format(args[0], args[2], amount, unit)])


    ###############################################################################################
    # 未實做

    if utterance == "比[房子]高出[3米]":
        # write your code here
        pass

    if utterance == "比[梨]少[25公斤]":
        # write your code here
        pass

    if utterance == "比[二]班多用了[8張]":
        # write your code here
        pass

    if utterance == "[小明]比[小東]多跳[3][下]":
        # write your code here
        pass

    if utterance == "[小明]比[小東]少跳[3][下]":
        # write your code here
        pass

    if utterance == "[媽媽]給[小明]的[糖]比[爸爸]少[2顆]":
        # write your code here
        pass

    if utterance == "[足球]的個數比[排球]多[15個]":
        # write your code here
        pass

    if utterance == "[小車][上]的人比[大車][上]的多[9]人":
        # write your code here
        pass

    if utterance == "[小車][上]的人比[大車][上]的少[9]人":
        # write your code here
        pass

    if utterance == "[小明]比[小紅]多得了[17個][小星星]":
        # write your code here
        pass

    return questionDICT