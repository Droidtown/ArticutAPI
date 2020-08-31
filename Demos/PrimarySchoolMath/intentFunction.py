#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import re
import requests

try:
    infoPath = "{}/account.info".format(os.path.dirname(os.path.abspath(__file__)))
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
    LOKI_KEY = infoDICT["loki_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""
    LOKI_KEY = ""

nubmerPat = re.compile("[\d０１２３４５６７８９〇一二三四五六七八九十零壹貳參肆伍陸柒捌玖拾廿卅貮兩百佰千仟万萬亿億兆點.]+")

def amountSTRconvert(amountSTR):
    '''把 amountSTR 的數字字串，透過 Articut 的 lv3 轉為數值類型並回傳。
    如此一來，就能把「兩個」變成數字 2 以便後續計算使用。'''
    numberSTR = nubmerPat.match(amountSTR).group()
    response = requests.post("https://api.droidtown.co/Articut/API/",
                              json={"username": USERNAME,
                                    "api_key": API_KEY,
                                    "input_str": numberSTR,
                                    "version": "latest",
                                    "level": "lv3",
                                    }).json()
    return numberSTR, response["number"][numberSTR]

def comparative(subject1, entity1, subject2, entity2, unit, questionDICT):
    '''
    計算「X 比 Y 多幾個」或是「X 比 Y 少幾個」的比較句。
    '''
    questionDICT["Question"].append([unit, entity1, subject1, entity2, subject2])
    entityAmount = 0
    subj1, ent1, ent1Amount, questionDICT = inTotal(subject1, entity1, unit, questionDICT)
    questionDICT["Question"].pop()
    subj2, ent2, ent2Amount, questionDICT = inTotal(subject2, entity2, unit, questionDICT)
    questionDICT["Question"].pop()

    entityAmount = abs(ent1Amount - ent2Amount)

    questionDICT["Answer"] = {"": [unit, entityAmount]}

    return entityAmount, questionDICT

def difference(subject, entity, unit, questionDICT):
    '''
    處理減法的計算。
    '''
    if entity == "":
        if unit in questionDICT["Entity"]:
            if len(questionDICT["Entity"][unit]) == 1:
                entity = questionDICT["Entity"][unit][0]
    else:
        entityLIST = list(set(list(questionDICT["Definition"].keys())+list(questionDICT["Calculation"].keys())+list(questionDICT["Memory"].keys())))
        if entity not in entityLIST:
            for ent in questionDICT["Definition"].keys():
                if entity in questionDICT["Definition"][ent]:
                    subject = entity
                    entity = ent
                    break
            for ent in questionDICT["Memory"].keys():
                if entity in questionDICT["Memory"][ent]:
                    subject = entity
                    entity = ent
                    break

    if subject == "":
        if questionDICT["Definition"]:
            if entity in questionDICT["Definition"]:
                subject = list(questionDICT["Definition"][entity].keys())[0]
        elif questionDICT["Calculation"]:
            if entity in questionDICT["Calculation"]:
                subject = list(questionDICT["Calculation"][entity].keys())[0]

    questionDICT["Question"].append([unit, entity, subject])
    entityAmount = 0
    if len(questionDICT["Memory"]) == 0:
        if entity not in questionDICT["Definition"] and entity not in questionDICT["Calculation"]:
            for ent in questionDICT["Definition"]:
                for subj in questionDICT["Definition"][ent].values():
                    if unit in subj:
                        entityAmount += subj[unit]
            for ent in questionDICT["Calculation"]:
                for subj in questionDICT["Calculation"][ent].values():
                    for v in subj:
                        if unit in v:
                            entityAmount += v[unit]
        else:
            if entity in questionDICT["Definition"]:
                if subject in questionDICT["Definition"][entity]:
                    entityAmount = questionDICT["Definition"][entity][subject][unit]
                else:
                    for subj in questionDICT["Definition"][entity].values():
                        entityAmount += subj[unit]

            if entity in questionDICT["Calculation"]:
                if subject in questionDICT["Calculation"][entity] and subject != "":
                    for subj in questionDICT["Calculation"][entity][subject]:
                        entityAmount += subj[unit]
                else:
                    for subj in questionDICT["Calculation"][entity].values():
                        for v in subj:
                            if unit in v:
                                entityAmount += v[unit]
    else:
        if entity not in questionDICT["Definition"] and entity not in questionDICT["Memory"] and entity not in questionDICT["Calculation"]:
            for ent in questionDICT["Definition"]:
                for subj in questionDICT["Definition"][ent].values():
                    if unit in subj:
                        entityAmount += subj[unit]
            for ent in questionDICT["Memory"]:
                for subj in questionDICT["Memory"][ent].values():
                    for v in subj:
                        if unit == v:
                            entityAmount += subj[unit]
            for ent in questionDICT["Calculation"]:
                for subj in questionDICT["Calculation"][ent].values():
                    for v in subj:
                        if unit in v and "ref" not in v:
                            entityAmount += v[unit]
        else:
            if entity in questionDICT["Definition"]:
                if subject in questionDICT["Definition"][entity]:
                    entityAmount = questionDICT["Definition"][entity][subject][unit]
                else:
                    for subj in questionDICT["Definition"][entity].values():
                        entityAmount += subj[unit]
            if entity in questionDICT["Memory"]:
                if subject in questionDICT["Memory"][entity]:
                    entityAmount = questionDICT["Memory"][entity][subject][unit]
                else:
                    for subj in questionDICT["Memory"][entity].values():
                        for v in subj:
                            if unit == v:
                                entityAmount += subj[unit]
            if entity in questionDICT["Calculation"]:
                if subject in questionDICT["Calculation"][entity]:
                    for subj in questionDICT["Calculation"][entity][subject]:
                        if "ref" not in subj:
                            entityAmount += subj[unit]
                else:
                    for subj in questionDICT["Calculation"][entity].values():
                        for v in subj:
                            if unit in v and "ref" not in v:
                                entityAmount += v[unit]

    if entity == "":
        questionDICT["Answer"] = {subject: {unit: abs(entityAmount)}}
    else:
        questionDICT["Answer"] = {entity: {unit: abs(entityAmount)}}
    return subject, entity, abs(entityAmount), questionDICT

def inTotal(subject, entity, unit, questionDICT):
    '''
    處理加法的計算。
    '''
    if entity == "":
        if unit in questionDICT["Entity"]:
            if len(questionDICT["Entity"][unit]) == 1:
                entity = questionDICT["Entity"][unit][0]
    else:
        entityLIST = list(set(list(questionDICT["Definition"].keys())+list(questionDICT["Calculation"].keys())+list(questionDICT["Memory"].keys())))
        if entity not in entityLIST:
            for ent in questionDICT["Definition"].keys():
                if entity in questionDICT["Definition"][ent]:
                    subject = entity
                    entity = ent
                    break
            for ent in questionDICT["Memory"].keys():
                if entity in questionDICT["Memory"][ent]:
                    subject = entity
                    entity = ent
                    break

    if subject == "":
        if questionDICT["Definition"]:
            if entity in questionDICT["Definition"] and "" in questionDICT["Definition"]:
                subject = list(questionDICT["Definition"][entity].keys())[0]
        elif questionDICT["Calculation"]:
            if entity in questionDICT["Calculation"] and "" in questionDICT["Calculation"]:
                subject = list(questionDICT["Calculation"][entity].keys())[0]

    questionDICT["Question"].append([unit, entity, subject])
    entityAmount = 0
    if len(questionDICT["Memory"]) == 0:
        if entity not in questionDICT["Definition"] and entity not in questionDICT["Calculation"]:
            for ent in questionDICT["Definition"]:
                for subj in questionDICT["Definition"][ent].values():
                    if unit in subj:
                        entityAmount += subj[unit]
            for ent in questionDICT["Calculation"]:
                for subj in questionDICT["Calculation"][ent].values():
                    for v in subj:
                        if unit in v:
                            entityAmount += v[unit]
        else:
            if entity in questionDICT["Definition"]:
                if subject in questionDICT["Definition"][entity]:
                    entityAmount = questionDICT["Definition"][entity][subject][unit]
                else:
                    for subj in questionDICT["Definition"][entity].values():
                        entityAmount += subj[unit]

            if entity in questionDICT["Calculation"]:
                if subject in questionDICT["Calculation"][entity] and subject != "":
                    for subj in questionDICT["Calculation"][entity][subject]:
                        entityAmount += subj[unit]
                else:
                    for subj in questionDICT["Calculation"][entity].values():
                        for v in subj:
                            if unit in v:
                                entityAmount += v[unit]
    else:
        if entity not in questionDICT["Definition"] and entity not in questionDICT["Memory"] and entity not in questionDICT["Calculation"]:
            for ent in questionDICT["Definition"]:
                for subj in questionDICT["Definition"][ent].values():
                    if unit in subj:
                        entityAmount += subj[unit]
            for ent in questionDICT["Memory"]:
                for subj in questionDICT["Memory"][ent].values():
                    for v in subj:
                        if unit == v:
                            entityAmount += subj[unit]
            for ent in questionDICT["Calculation"]:
                for subj in questionDICT["Calculation"][ent].values():
                    for v in subj:
                        if unit in v and "ref" not in v:
                            entityAmount += v[unit]
        else:
            if entity in questionDICT["Definition"]:
                if subject in questionDICT["Definition"][entity]:
                    entityAmount = questionDICT["Definition"][entity][subject][unit]
                else:
                    for subj in questionDICT["Definition"][entity].values():
                        entityAmount += subj[unit]
            if entity in questionDICT["Memory"]:
                if subject in questionDICT["Memory"][entity]:
                    entityAmount = questionDICT["Memory"][entity][subject][unit]
                else:
                    for subj in questionDICT["Memory"][entity].values():
                        for v in subj:
                            if unit == v:
                                entityAmount += subj[unit]
            if entity in questionDICT["Calculation"]:
                if subject in questionDICT["Calculation"][entity]:
                    for subj in questionDICT["Calculation"][entity][subject]:
                        if "ref" not in subj:
                            entityAmount += subj[unit]
                else:
                    for subj in questionDICT["Calculation"][entity].values():
                        for v in subj:
                            if unit in v and "ref" not in v:
                                entityAmount += v[unit]

    if entity == "":
        questionDICT["Answer"] = {subject: {unit: abs(entityAmount)}}
    else:
        questionDICT["Answer"] = {entity: {unit: abs(entityAmount)}}
    return subject, entity, abs(entityAmount), questionDICT

def existential(subject, entity, amount, unit, questionDICT):
    '''
    處理存現動詞， 也就是意思上表示「存在著」的那些動詞。
    例如「桌上有兩顆蘋果」裡的 "有"。以「桌子」做為「物體存在的地點」。

    同時兼容動詞的「擁有」或「持有」的動詞。
    例如「妹妹有三個杯子蛋糕」裡的 "有"。以「妹妹」做為「物體存在的地點」。
    '''
    if entity == "":
        entityLIST = list(questionDICT["Definition"].keys())
        if len(entityLIST) > 0:
            entity = entityLIST[0]

    if unit in questionDICT["Entity"]:
        if entity not in questionDICT["Entity"][unit]:
            questionDICT["Entity"][unit].append(entity)
    else:
        questionDICT["Entity"][unit] = [entity]

    if entity in questionDICT["Definition"]:
        if subject in questionDICT["Definition"][entity]:
            questionDICT["Definition"][entity][subject][unit] = amount
        else:
            questionDICT["Definition"][entity][subject] = {unit: amount}
    else:
        questionDICT["Definition"][entity] = {subject: {unit: amount}}
    return questionDICT

def bitransitive(subject1, subject2, entity1, entity2, amount, unit, questionDICT):
    '''
    處理 A 比 B 多或少的題型
    subject1 比 subject2 多 amount unit
    entity1 比 entity2 多 amount unit
    '''
    entityLIST = list(set(list(questionDICT["Definition"].keys())+list(questionDICT["Calculation"])+list(questionDICT["Memory"])))
    subjectLIST = []
    for k in ["Memory", "Definition", "Calculation"]:
        for ent in entityLIST:
            if ent in questionDICT[k]:
                subjectLIST.extend(list(questionDICT[k][ent].keys()))
    subjectLIST = list(set(subjectLIST))

    if entity2 != "":
        if entity1 in subjectLIST or entity2 in subjectLIST or entity2 in ["他", "她"]:
            tmpEnt1 = subject1
            tmpEnt2 = subject2
            subject1 = entity1
            subject2 = entity2
            entity1 = tmpEnt1
            entity2 = tmpEnt2

    if subject2 != "":
        if subject1 in entityLIST or subject2 in entityLIST:
            tmpSubj1 = entity1
            tmpSubj2 = entity2
            entity1 = subject1
            entity2 = subject2
            subject1 = tmpSubj1
            subject2 = tmpSubj2

    # 把已存在的 entity1 / subject1 放入 entity2 / subject2
    if entity1 in entityLIST and entity2 != "":
        tmpEnt = entity1
        entity1 = entity2
        entity2 = tmpEnt
        amount = -amount

    if subject1 in subjectLIST and subject2 != "":
        tmpSubj = subject1
        subject1 = subject2
        subject2 = tmpSubj
        amount = -amount

    # entity1 / subject1 空白時試著補上存在的 entity / subject
    if entity1 == "":
        if unit in questionDICT["Entity"]:
            if len(questionDICT["Entity"][unit]) == 1:
                entity1 = questionDICT["Entity"][unit][0]

    if subject1 == "":
        for k in ["Definition", "Memory", "Calculation"]:
            if entity1 != "" and entity2 != "":
                tmpEnt = entity2
            else:
                tmpEnt = entity1
            if tmpEnt in questionDICT[k]:
                subject1 = list(questionDICT[k][tmpEnt].keys())[0]
                subject2 = subject1
                break

    # 決定 ref 是 entity 或 subject
    if entity1 != "" and entity2 != "":
        entity = entity2
        subject = subject1
        refOBJ = entity2
    else:
        entity = entity1
        subject = subject2
        refOBJ = subject2

    if subject in ["", "他", "她"]:
        for k in ["Definition", "Memory", "Calculation"]:
            if entity in questionDICT[k]:
                subjectLIST = list(questionDICT[k][entity].keys())
                if len(subjectLIST) == 1 and subjectLIST[0] != "":
                    subject = subjectLIST[0]
                    refOBJ = subject
                    break

    # 取得 ref 的 amount
    refAmount = 0
    for k in ["Memory", "Definition", "Calculation"]:
        if entity in questionDICT[k]:
            if subject in questionDICT[k][entity]:
                if k == "Calculation":
                    refAmount = questionDICT[k][entity][subject][-1][unit]
                else:
                    refAmount = questionDICT[k][entity][subject][unit]
                break

    # 算式存入 Calculation
    if entity1 in questionDICT["Calculation"]:
        if subject1 in questionDICT["Calculation"][entity1]:
            questionDICT["Calculation"][entity1][subject1].append({unit: amount, "ref": refOBJ})
        else:
            questionDICT["Calculation"][entity1][subject1] = [{unit: amount, "ref": refOBJ}]
    else:
        questionDICT["Calculation"][entity1] = {subject1: [{unit: amount, "ref": refOBJ}]}

    # 結果存入 Memory
    if entity1 in questionDICT["Memory"]:
        questionDICT["Memory"][entity1][subject1] = {unit: refAmount + amount}
    else:
        questionDICT["Memory"][entity1] = {subject1: {unit: refAmount + amount}}

    if unit in questionDICT["Entity"]:
        if entity1 not in questionDICT["Entity"][unit]:
            questionDICT["Entity"][unit].append(entity1)
    else:
        questionDICT["Entity"] = {unit: [entity1]}

    if refOBJ == subject:
        return subject1, refOBJ, questionDICT
    else:
        return entity1, refOBJ, questionDICT

def transitive(subject, entity, amount, unit, questionDICT):
    '''
    處理及物動詞， 也就是「有受詞」的那些動作。
    '''
    if entity == "":
        if unit in questionDICT["Entity"]:
            if len(questionDICT["Entity"][unit]) == 1:
                entity = questionDICT["Entity"][unit][0]
                if subject in ["", "他", "她", "我", "他們", "她們", "我們"]:
                    if questionDICT["Definition"]:
                        if subject not in questionDICT["Definition"][entity]:
                            subject = list(questionDICT["Definition"][entity].keys())[0]
                    elif questionDICT["Calculation"]:
                        if subject not in questionDICT["Calculation"][entity]:
                            subject = list(questionDICT["Calculation"][entity].keys())[0]
    else:
        if subject in ["", "他", "她", "我", "他們", "她們", "我們"]:
            if entity in questionDICT["Definition"]:
                subject = list(questionDICT["Definition"][entity].keys())[0]
            elif entity in questionDICT["Calculation"]:
                subject = list(questionDICT["Calculation"][entity].keys())[0]

    if entity in questionDICT["Calculation"]:
        if subject in questionDICT["Calculation"][entity]:
            questionDICT["Calculation"][entity][subject].append({unit: amount})
        else:
            questionDICT["Calculation"][entity][subject] = [{unit: amount}]
    else:
        if unit in questionDICT["Entity"]:
            if entity not in questionDICT["Entity"][unit]:
                questionDICT["Entity"][unit].append(entity)
        else:
            questionDICT["Entity"][unit] = [entity]
        questionDICT["Calculation"][entity] = {subject: [{unit: amount}]}

    return subject, entity, questionDICT

def intransitive(entity, questionDICT):
    '''
    處理不及物動詞， 也就是「沒有受詞」的那些動作。
    '''
    #pprint(questionDICT)
    if entity not in questionDICT["Definition"] and entity not in questionDICT["Calculation"]:
        primaryEnt = None
        primaryAmount = None
        primaryUnit = None
        primarySubject = None
        entAmount = 0
        resultAmount = 0
        for ent in questionDICT["Definition"]:
            for subj in questionDICT["Definition"][ent]:
                for unit in questionDICT["Definition"][ent][subj]:
                    if unit != "元":
                        if primaryEnt == None:
                            primarySubject = subj
                            primaryEnt = ent
                            primaryAmount = questionDICT["Definition"][ent][subj][unit]
                            primaryUnit = unit
                            entAmount += questionDICT["Definition"][ent][subj][unit]
                        elif unit == primaryUnit:
                            if primaryAmount < questionDICT["Definition"][ent][subj][unit]:
                                primarySubject = subj
                                primaryEnt = ent
                                primaryAmount = questionDICT["Definition"][ent][subj][unit]
                                primaryUnit = unit
                            entAmount += questionDICT["Definition"][ent][subj][unit]

        for ent in questionDICT["Calculation"]:
            for subj in questionDICT["Calculation"][ent]:
                for v in questionDICT["Calculation"][ent][subj]:
                    for unit in v:
                        if unit != "元":
                            if primaryEnt == None:
                                primarySubject = subj
                                primaryEnt = ent
                                primaryAmount = v[unit]
                                primaryUnit = unit
                                entAmount += v[unit]
                            elif unit == primaryUnit:
                                if primaryAmount < v[unit]:
                                    primarySubject = subj
                                    primaryEnt = ent
                                    primaryAmount = v[unit]
                                    primaryUnit = unit
                                entAmount += v[unit]
        resultAmount = primaryAmount - (entAmount - primaryAmount)
    questionDICT["Calculation"][entity] = {primarySubject: [{primaryUnit: resultAmount}]}
    return primaryEnt, (entAmount - primaryAmount), primaryUnit, questionDICT

