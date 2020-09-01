#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Definition

    Input:
        pattern       str,
        utterance     str,
        args          str[],
        questionDICT    dict

    Output:
        questionDICT    dict
"""

from intentFunction import *

DEBUG_Definition = True
userDefinedDICT = {'乘客': [''], '大米': [''], '小正': ['小強', '小紅', '小晴', '小優', '小明'], '時速': [''], '海拔': [''], '獵豹': [''], '貨物': [''], '周新新': [''], '批發站': [''], '海平面': [''], '科普書': [''], '吐魯番盆地': ['']}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_Definition:
        print("[Definition]")
        print("{} ===> {}\n".format(utterance, args))
        #print("Pattern:", pattern)

def getResult(pattern, utterance, args, inputUtterance, questionDICT):
    debugInfo(pattern, utterance, args)

    if utterance == "[甲數]是[20]":
        questionDICT = existential("", args[0], int(args[1]), "", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}".format(args[0], args[1])])

    if utterance == "有[公雞][44隻]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential("", args[0], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, unit)])

    if utterance == "有[5個]是[雞蛋]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        questionDICT = existential("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], amount, unit)])

    if utterance == "有[38個][罐頭]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        questionDICT = existential("", args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], amount, unit)])

    if utterance == "有[7枝][藍筆]和[5枝][紅筆]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        questionDICT = existential("", args[1], amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential("", args[3], amount, unit, questionDICT)

        questionDICT["Process"].append([inputUtterance, "{}={}; {}={}".format(args[1], args[0], args[3], args[2])])

    if utterance == "有[10條][紅][緞帶]和[6條][藍][緞帶]":
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        questionDICT = existential("", args[1]+args[2], amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[3])
        unit = args[3].replace(numberSTR, "")
        questionDICT = existential("", args[4]+args[5], amount, unit, questionDICT)

        questionDICT["Process"].append([inputUtterance, "{}{}={}; {}{}={}".format(args[1], args[2], args[0], args[4], args[5], args[3])])

    if utterance == "[蘋果派]有[9個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential("", args[0], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, unit)])

    if utterance == "[養雞場]有[公雞][44隻]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(args[0], args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[1], amount, unit)])

    if utterance == "[小卓]有[7張][色紙]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(args[0], args[2], amount, unit)])

    if utterance == "[弟弟]有[3塊][蕾神][巧克力]":
        numberSTR, amount = amountSTRconvert(args[1])
        entity = args[2]+args[3]
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(args[0], entity, amount, unit)])

    if utterance == "[海底]有[6個][紅色][寶特瓶]":
        numberSTR, amount = amountSTRconvert(args[1])
        entity = args[2]+args[3]
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(args[0], entity, amount, unit)])

    if utterance == "[CD][盒][裡]有[12片][光碟]":
        numberSTR, amount = amountSTRconvert(args[3])
        subject = args[0]+args[1]+args[2]
        unit = args[3].replace(numberSTR, "")
        questionDICT = existential(subject, args[4], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[4], amount, unit)])

    if utterance == "[池][裡]有[30條][小魚]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject = args[0]+args[1]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, args[3], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[3], amount, unit)])

    if utterance == "[班級][裡]有[22張][臘光][紙]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject = args[0]+args[1]
        entity = args[3]+args[4]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, entity, amount, unit)])

    if utterance == "[農場][裡]有[36隻][牛]和[40隻][羊]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject = args[0]+args[1]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, args[3], amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[4])
        unit = args[4].replace(numberSTR, "")
        questionDICT = existential(subject, args[5], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{0}_{1}+{2}; {0}_{3}+{4}".format(subject, args[3], args[2], args[5], args[4])])

    if utterance == "[花瓶][裡]有[15朵][紅][玫瑰]":
        subject = args[0]+args[1]
        entity = args[3]+args[4]
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, entity, amount, unit)])

    if utterance == "[草地][上]有[14枝][紅][風車]和[9枝][藍][風車]":
        subject = args[0]+args[1]

        numberSTR, amount = amountSTRconvert(args[2])
        entity = args[3]+args[4]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, entity, amount, unit, questionDICT)

        numberSTR, amount = amountSTRconvert(args[5])
        entity = args[6]+args[7]
        unit = args[5].replace(numberSTR, "")
        questionDICT = existential(subject, entity, amount, unit, questionDICT)

        questionDICT["Process"].append([inputUtterance, "{0}_{1}={2}; {0}_{3}={4}".format(subject, args[3]+args[4], args[2], entity, args[5])])

    if utterance == "[車][上]原有[6隻][貓]":
        numberSTR, amount = amountSTRconvert(args[2])
        subject = args[0]+args[1]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential(subject, args[3], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[3], amount, unit)])

    if utterance == "[兔屋外]有[10隻][兔子]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], amount, unit)])

    if utterance == "[弟弟]有[3塊][巧克力]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[2], amount, unit)])

    if utterance == "[白][珠子]有[2顆]":
        numberSTR, amount = amountSTRconvert(args[2])
        entity = args[0]+args[1]
        unit = args[2].replace(numberSTR, "")
        questionDICT = existential("", entity, amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, amount, unit)])

    if utterance == "[小玲]寫了[4行][國字]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(args[0], args[2], amount, unit)])

    if utterance == "[二]班有[男生][27名]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject = args[0]+"班"
        questionDICT = existential(subject, args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[1], amount, unit)])

    if utterance == "[二]班有[27名][男生]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject = args[0]+"班"
        questionDICT = existential(subject, args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[2], amount, unit)])

    if utterance == "[二]班[男生][27名]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject = args[0]+"班"
        questionDICT = existential(subject, args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[1], amount, unit)])

    if utterance == "[二]班[27名][男生]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        subject = args[0]+"班"
        questionDICT = existential(subject, args[2], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[2], amount, unit)])

    if utterance == "[二]班[圖書]有[67本]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject = args[0]+"班"
        questionDICT = existential(subject, args[1], amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}{}".format(subject, args[1], amount, unit)])

    if utterance == "[一]班有[42]人":
        subject = args[1]+"班"
        entity = args[0]+"年級"
        questionDICT = existential(subject, entity, int(args[2]), "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}人".format(entity, subject, args[1])])

    if utterance == "[5年][1]班有[46]人":
        subject = args[0]
        entity = args[1]+"班"
        questionDICT = existential(subject, entity, int(args[2]), "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}人".format(entity, subject, args[1])])

    if utterance == "[二]年級[一]班有[42]人":
        subject = args[1]+"班"
        entity = args[0]+"年級"
        questionDICT = existential(subject, entity, int(args[2]), "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}人".format(entity, subject, args[1])])

    if utterance == "[車][上]有[乘客][45]人":
        numberSTR, amount = amountSTRconvert(args[3])
        subject = args[0]+args[1]
        questionDICT = existential(subject, args[2], amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_{}={}人".format(subject, args[3], amount)])

    if utterance == "[球場][上]原有[33]人":
        numberSTR, amount = amountSTRconvert(args[2])
        subject = args[0]+args[1]
        questionDICT = existential(subject, "", amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}_人={}人".format(subject, amount)])

    if utterance == "[女生][16]人":
        numberSTR, amount = amountSTRconvert(args[1])
        questionDICT = existential("", args[0], amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}人".format(args[0], amount)])

    if utterance == "[男生]有[35]人":
        if "其中" not in inputUtterance:
            numberSTR, amount = amountSTRconvert(args[1])
            questionDICT = existential("", args[0], amount, "人", questionDICT)
            questionDICT["Process"].append([inputUtterance, "{}={}人".format(args[0], amount)])

    if utterance == "[小雨]有[7元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, unit)])

    if utterance == "[瑋瑋]原有[13元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, unit)])

    if utterance == "[撲滿][裡]有[22元]":
        numberSTR, amount = amountSTRconvert(args[2])
        unit = args[2].replace(numberSTR, "")
        subject = args[0]+args[1]
        questionDICT = existential(subject, "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(subject, amount, unit)])

    if utterance == "[約翰]有[10元]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential(args[0], "", amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], amount, unit)])

    if utterance == "其中[1200雙]是[塑料][涼鞋]":
        entity = args[1]+args[2]
        numberSTR, amount = amountSTRconvert(args[0])
        unit = args[0].replace(numberSTR, "")
        questionDICT = existential("", entity, -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(entity, -amount, unit)])

    if utterance == "其中[男生]有[9個]":
        numberSTR, amount = amountSTRconvert(args[1])
        unit = args[1].replace(numberSTR, "")
        questionDICT = existential("", args[0], -amount, unit, questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}{}".format(args[0], -amount, unit)])

    if utterance == "其中[女生]有[7]人":
        numberSTR, amount = amountSTRconvert(args[1])
        questionDICT = existential("", args[0], -amount, "人", questionDICT)
        questionDICT["Process"].append([inputUtterance, "{}={}人".format(args[0], -amount)])

    ###############################################################################################
    # 未實做

    if utterance == "有[水泥][88噸]":
        # write your code here
        pass

    if utterance == "有[12米][布]":
        # write your code here
        pass

    if utterance == "[水果店]有[水果][670公斤]":
        # write your code here
        pass

    if utterance == "[小明]看[一本][35頁]的[書]":
        # write your code here
        pass

    if utterance == "[舞蹈隊]需要[80]人":
        # write your code here
        pass

    if utterance == "[高度]為[8844m]":
        # write your code here
        pass

    if utterance == "[速度]是每[小時][13.5公里]":
        # write your code here
        pass

    if utterance == "[獵豹]最快時速是每[小時][113公里]":
        # write your code here
        pass

    if utterance == "[吐魯番盆地]的[高度]為[海平面]以下[155公尺]":
        # write your code here
        pass

    if utterance == "[珠穆朗瑪峰]的[海拔][高度]為[海平面]以上[8844m]":
        # write your code here
        pass

    if utterance == "[電視機][原價]是[5800元]":
        # write your code here
        pass

    if utterance == "[羊][3隻]":
        # write your code here
        pass

    if utterance == "[葡萄][18元]":
        # write your code here
        pass

    if utterance == "[批發站]原有[140筐][水果]":
        # write your code here
        pass

    if utterance == "[鋼材]長[18.4公尺]":
        # write your code here
        pass

    if utterance == "[國旗杆]高[12米]":
        # write your code here
        pass

    if utterance == "[倉儲][裡]有[水泥][88噸]":
        # write your code here
        pass

    if utterance == "[小明][寒假]看[一本][126頁]的[科普書]":
        # write your code here
        pass

    if utterance == "[15個][小朋友]捉迷藏":
        # write your code here
        pass

    if utterance == "[13個][小朋友]在玩捉迷藏":
        # write your code here
        pass

    if utterance == "[一根][繩子][4公尺]":
        # write your code here
        pass

    if utterance == "[一本][85頁]的[書]":
        # write your code here
        pass

    if utterance == "[一本][19.5元]":
        # write your code here
        pass

    if utterance == "原計畫[8月]生產[手帕][780打]":
        # write your code here
        pass

    return questionDICT