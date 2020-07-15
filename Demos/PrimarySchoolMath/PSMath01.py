"""
    Loki Template For Python3

    Request:
        {
            "username": "your_username",
            "api_key": "your_articut_key",
            "input_str": "your_sentence",
            "version": "latest", # Articut Version
            "loki_key": "your_loki_key"
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v193",
            "word_count_balance": 2000,
            "results": [
                {
                    "intent": "intentName",
                    "pattern": "matchPattern",
                    "argument": ["arg1", "arg2", ... "argN"]
                },
                ...
            ]
        }
"""

import json
import os
import re
import requests

from pprint import pprint

try:
    infoPath = "{}/account.json".format(os.path.dirname(os.path.abspath(__file__)))
    infoDICT = json.load(open(infoPath, "r"))
    USERNAME = infoDICT["username"]
    API_KEY = infoDICT["api_key"]
    LOKI_KEY = infoDICT["loki_key"]
except:
    # HINT: 在這裡填入您在 https://api.droidtown.co 的帳號、Articut 的 API_Key 以及 Loki 專案的 Loki_Key
    USERNAME = ""
    API_KEY = ""
    LOKI_KEY = ""


# HINT: 基本上 LokiResult() 與你無關，這是用來和 Loki API 伺服器溝通用的 class.
class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = None

    def __init__(self, input_str):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = None

        try:
            result = requests.post("https://api.droidtown.co/Loki/API/", json={
                "username": USERNAME,
                "api_key": API_KEY,
                "input_str": input_str,
                "version": "latest",
                "loki_key": LOKI_KEY
            })

            if result.status_code == requests.codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["results"]
            else:
                self.message = "Connect Error."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLen(self):
        rst = 0
        if self.lokiResultLIST is not None:
            rst = len(self.lokiResultLIST)

        return rst

    def getLokiResult(self, index):
        lokiResultDICT = None
        if self.lokiResultLIST is not None:
            if index < self.getLen():
                lokiResultDICT = self.lokiResultLIST[i]

        return lokiResultDICT

    def getIntent(self, index):
        rst = ""
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["intent"]

        return rst

    def getPattern(self, index):
        rst = ""
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["pattern"]

        return rst

    def getArgs(self, index):
        rst = []
        lokiResultDICT = self.getLokiResult(index)
        if lokiResultDICT is not None:
            rst = lokiResultDICT["argument"]

        return rst


###############################################################################################
punctuationPat = re.compile("[，。；,;？]")
nubmerPat = re.compile("[\d０１２３４５６７８９〇一二三四五六七八九十零壹貳參肆伍陸柒捌玖拾廿卅貮兩百佰千仟万萬亿億兆點.]+")

questionDICT = {"Definition": {},
                "Calculation": {},
                "Entity": {},
                "Memory": {},
                "Process": [],
                "Question": []}

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

def doSomethingAbout(args, intent):
    '''將符合句型的參數列表印出。這是 debug 或是開發用的。'''
    print(args, "===>", intent)

def comparative(subject1, entity1, subject2, entity2, unit):
    '''
    計算「X 比 Y 多幾個」或是「X 比 Y 少幾個」的比較句。
    '''
    questionDICT["Question"].append([unit, entity1, subject1, entity2, subject2])
    entityAmount = 0
    subj1, ent1, ent1Amount = inTotal(subject1, entity1, unit)
    questionDICT["Question"].pop()
    subj2, ent2, ent2Amount = inTotal(subject2, entity2, unit)
    questionDICT["Question"].pop()

    entityAmount = abs(ent1Amount - ent2Amount)

    questionDICT["Answer"] = {"": [unit, entityAmount]}

    return entityAmount

def transitive(subject, entity, amount, unit):
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

    return subject, entity

def intransitive(entity):
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
    return primaryEnt, (entAmount - primaryAmount), primaryUnit

def bitransitive(subject1, subject2, entity1, entity2, amount, unit):
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
        return subject1, refOBJ
    else:
        return entity1, refOBJ

def existential(subject, entity, amount, unit):
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
    return None

def difference(subject, entity, unit):
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
    return subject, entity, abs(entityAmount)

def inTotal(subject, entity, unit):
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
    return subject, entity, abs(entityAmount)

if __name__ == "__main__":
    # HINT: 測試段落。
    inputSTR = "桌上有三顆蘋果，小明吃掉一顆，還剩下幾顆蘋果"
    inputLIST = list(filter(None, punctuationPat.sub("\n", inputSTR).split("\n")))
    print(inputLIST)

    for s in inputLIST:
        lokiRst = LokiResult(s)
        # HINT: 以下這些 lokiRst.getPattern(i) 都是在 Loki 的網頁中自動幫你生成的。
        # 所以後面那些看起來很複雜的正規表示式 (regular expression) 你不需要讀懂沒關係。
        # 每個 lokiRst.getPattern(i) 的上方還會出現一行「註解起來」的中文句子。那是用來
        # 表示那段正規表示式是在描述哪一種句型。比如說『剩下幾[個]』這段，就在表示其後的正規
        # 表示式是用來抓「剩下幾個」中的「個」。

        for i in range(0, lokiRst.getLen()):
            # <Question>
            if lokiRst.getIntent(i) == "Question":
                # 剩下幾[個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩下][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩下][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "剩下幾[個]")
                    subject, entity, entityAmount = difference("", "", lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[0])])

                # [乙數]是多少
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                    doSomethingAbout(lokiRst.getArgs(i), "[乙數]是多少")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], "")
                    questionDICT["Process"].append([s, "{}={}".format(lokiRst.getArgs(i)[0], entityAmount)])

                # [男生]有幾人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[男生]有幾人")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], "人")
                    questionDICT["Process"].append([s, "{}={}人".format(lokiRst.getArgs(i)[0], entityAmount)])

                # 總共有幾人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "總共有幾人")
                    subject, entity, entityAmount = inTotal("", "", "人")
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])

                # 剩下幾[個][小魚]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩下][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩下][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "剩下幾[個][小魚]")
                    subject, entity, entityAmount = difference("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # 還有多少[個]沒捉住
                if lokiRst.getPattern(i) == "<FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><FUNC_negation>[^<]*?</FUNC_negation>((<ACTION_verb>[^<不]*?[捉住][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉住][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "還有多少[個]沒捉住")
                    subject, entity, entityAmount = difference("", "", lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[0])])

                # [姊姊][今年]幾歲
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_year>[^<]*?</TIME_year><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊][今年]幾歲")
                # [姊姊]踢了幾[下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[踢][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[踢][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]踢了幾[下]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[1])])

                # [小威]拍了幾[下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[拍][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拍][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小威]拍了幾[下]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[1])])

                # [應]找回多少元
                if lokiRst.getPattern(i) == "(<MODAL>[^<]*?</MODAL>)?((<ACTION_verb>[^<不]*?[找回][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[找回][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[應]找回多少元")
                # 有幾[球]沒投進
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_negation>[^<]*?</FUNC_negation>((<ACTION_verb>[^<不]*?[投][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[投][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[進][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "有幾[球]沒投進")
                # [自己]還有幾元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[自己]還有幾元")
                    if lokiRst.getArgs(i)[0] == "自己":
                        subject, entity, entityAmount = inTotal("", "", "元")
                    else:
                        subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", "元")
                    questionDICT["Process"].append([s, "{}元".format(entityAmount)])

                # 還剩幾[條][小魚]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "還剩幾[條][小魚]")
                    subject, entity, entityAmount = difference("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # 還有幾[條][小魚]
                if lokiRst.getPattern(i) == "<FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "還有幾[條][小魚]")
                    subject, entity, entityAmount = difference("", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[0])])

                # [黑][珠子]有幾[顆]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[黑][珠子]有幾[顆]")
                    entity = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal("", entity, lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[2])])

                # [他們]總共有幾元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[他們]總共有幾元")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", "元")
                    questionDICT["Process"].append([s, "{}元".format(entityAmount)])

                # 共包了幾[個][粽子]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[包][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[包][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "共包了幾[個][粽子]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # 共有幾[人]在排隊
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[排隊][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[排隊][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "共有幾[人]在排隊")
                # 共賣出幾[雙][鞋子]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "共賣出幾[雙][鞋子]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[0])])

                # [撲滿][裡]共有幾元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[撲滿][裡]共有幾元")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, "", "元")
                    questionDICT["Process"].append([s, "{}={}元".format(subject, entityAmount)])

                # [現在][爸爸]在幾樓
                if lokiRst.getPattern(i) == "<TIME_justtime>[^<]*?</TIME_justtime><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>樓</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[現在][爸爸]在幾樓")
                # [現在][瑋瑋]有幾元
                if lokiRst.getPattern(i) == "<TIME_justtime>[^<]*?</TIME_justtime><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[現在][瑋瑋]有幾元")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[1], "", "元")
                    questionDICT["Process"].append([s, "{}={}元".format(lokiRst.getArgs(i)[1], entityAmount)])

                # [現在]總共有幾[顆]
                if lokiRst.getPattern(i) == "<TIME_justtime>[^<]*?</TIME_justtime>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[現在]總共有幾[顆]")
                    subject, entity, entityAmount = inTotal("", "", lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])

                # [球場][上]共有幾人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[球場][上]共有幾人")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, "", "人")
                    questionDICT["Process"].append([s, "{}_人={}人".format(subject, entityAmount)])

                # [皇后]有幾[顆][寶石]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[皇后]有幾[顆][寶石]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # 總共有幾[條][小魚]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "總共有幾[條][小魚]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # [蘋果]總共有幾[顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[蘋果]總共有幾[顆]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1])
                    if subject == "":
                        questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])
                    else:
                        questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, entity, entityAmount, lokiRst.getArgs(i)[1])])

                # 一共有[氣球]多少[個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "一共有[氣球]多少[個]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[1])])

                # [二]班用了多少[張][紙]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班用了多少[張][紙]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0]+"班", lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}班={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[1])])

                # [公主]有幾[顆][紅][寶石]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[公主]有幾[顆][紅][寶石]")
                    entity = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], entity, lokiRst.getArgs(i)[1])
                    if subject == "":
                        questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])
                    else:
                        questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, entity, entityAmount, lokiRst.getArgs(i)[1])])

                # [哥哥]總共用多少元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]總共用多少元")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", "元")
                    questionDICT["Process"].append([s, "{}元".format(entityAmount)])

                # [小玉]吃了幾[顆][草莓]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小玉]吃了幾[顆][草莓]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # [小華]剩下幾[顆][蘋果]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[剩下][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩下][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小華]剩下幾[顆][蘋果]")
                    subject, entity, entityAmount = difference(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # [老師]還有幾[條][緞帶]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[老師]還有幾[條][緞帶]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # [舞台][上]有幾[個][演員]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[舞台][上]有幾[個][演員]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[3], entityAmount, lokiRst.getArgs(i)[2])])

                # [豬肉]比[牛肉]多幾[片]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[豬肉]比[牛肉]多幾[片]")
                    entityAmount = comparative("", lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1], unit)
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, unit)])

                # [豬肉]比[牛肉]少幾[片]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[豬肉]比[牛肉]少幾[片]")
                    entityAmount = comparative("", lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1], unit)
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, unit)])

                # 再過幾[年][我]就[18]歲了
                if lokiRst.getPattern(i) == "<MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[過][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[過][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><TIME_year>[^<]*?</TIME_year><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "再過幾[年][我]就[18]歲了")

                # 一共做了多少[個][作品]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "一共做了多少[個][作品]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # 一共吃了幾[顆][巧克力]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "一共吃了幾[顆][巧克力]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[0])])

                # [三盒]總共有幾[個][罐頭]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[三盒]總共有幾[個][罐頭]")
                # [兩天]共賣出幾[雙][鞋子]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[兩天]共賣出幾[雙][鞋子]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])

                # [兩桶][油]共重多少[公斤]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[兩桶][油]共重多少[公斤]")
                # [公車][上][現在]還有幾人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><TIME_justtime>[^<]*?</TIME_justtime><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[公車][上][現在]還有幾人")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, "", "人")
                    questionDICT["Process"].append([s, "{}_人={}人".format(subject, entityAmount)])

                # [哥哥]總共花掉多少元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[花掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[花掉][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]總共花掉多少元")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", "元")
                    questionDICT["Process"].append([s, "{}元".format(entityAmount)])

                # [姊姊]比[哥哥]少買幾[枝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[哥哥]少買幾[枝]")
                    subject, entity, entityAmount = inTotal("", "", lokiRst.getArgs(i)[2])
                    entityAmount = comparative(lokiRst.getArgs(i)[0], entity, lokiRst.getArgs(i)[1], entity, lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[2])])

                # [小梅]換了幾[隻][熊寶貝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[換][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小梅]換了幾[隻][熊寶貝]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # [小毛]摺了幾[架][紙飛機]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小毛]摺了幾[架][紙飛機]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], entityAmount, lokiRst.getArgs(i)[1])])

                # [棒虎]比[小福]多得幾分
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[得][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>分</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[棒虎]比[小福]多得幾分")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1], "", "分")
                    questionDICT["Process"].append([s, "{}分".format(entityAmount)])

                # [棒虎]比[小福]少得幾分
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[得][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>分</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[棒虎]比[小福]少得幾分")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1], "", "分")
                    questionDICT["Process"].append([s, "{}分".format(entityAmount)])

                # [現在][球場][上]共有幾人
                if lokiRst.getPattern(i) == "<TIME_justtime>[^<]*?</TIME_justtime><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[現在][球場][上]共有幾人")
                    subject = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    subject, entity, entityAmount = inTotal(subject, "", "人")
                    questionDICT["Process"].append([s, "{}_人={}人".format(subject, entityAmount)])

                # 一共做了多少[個][蝴蝶][結]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "一共做了多少[個][蝴蝶][結]")
                    entity = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    subject, entity, entityAmount = inTotal("", entity, lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[0])])

                # [兩個]班一共用了多少[張]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[兩個]班一共用了多少[張]")
                    subject, entity, entityAmount = inTotal("", "", lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])

                # [家民]買了幾[枝][自動鉛筆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[家民]買了幾[枝][自動鉛筆]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[1])])

                # [快餐店]還有[漢堡]多少[個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><LOCATION>[^<]*?</LOCATION><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[快餐店]還有[漢堡]多少[個]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], entityAmount, lokiRst.getArgs(i)[2])])

                # [海盜船][上]還有幾[個][海盜]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[海盜船][上]還有幾[個][海盜]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[2])])

                # [魚缸][裡][現在]有幾[條][熱帶魚]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><TIME_justtime>[^<]*?</TIME_justtime>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[魚缸][裡][現在]有幾[條][熱帶魚]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[4])])

                # [王子]做了幾[下]仰臥起坐
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>((<ACTION_verb>[^<不]*?[仰臥起坐][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[仰臥起坐][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[王子]做了幾[下]仰臥起坐")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}_仰臥起坐={}{}".format(lokiRst.getArgs(i)[0], entityAmount, lokiRst.getArgs(i)[1])])

                # [現在][舞台][上]有幾[個][演員]
                if lokiRst.getPattern(i) == "<TIME_justtime>[^<]*?</TIME_justtime><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[現在][舞台][上]有幾[個][演員]")
                    subject = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    subject, entity, entityAmount = inTotal(subject, lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[4], entityAmount, lokiRst.getArgs(i)[3])])

                # [紅][風車]比[藍][風車]多幾[枝]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[紅][風車]比[藍][風車]多幾[枝]")
                    entityAmount = comparative("", lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], "", lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3], unit)
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, unit)])

                # [紅][風車]比[藍][風車]少幾[枝]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[紅][風車]比[藍][風車]少幾[枝]")
                    entityAmount = comparative("", lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], "", lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3], unit)
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, unit)])

                # [架][上][現在]還有幾[本][故事書]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><TIME_justtime>[^<]*?</TIME_justtime><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[架][上][現在]還有幾[本][故事書]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = difference(subject, lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[4], entityAmount, lokiRst.getArgs(i)[3])])

                # [海盜船][上]還剩下幾[個][海盜]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[剩下][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩下][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[海盜船][上]還剩下幾[個][海盜]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    subject, entity, entityAmount = inTotal(subject, lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, entityAmount, lokiRst.getArgs(i)[2])])

                # [昨天]比[今天]少摺了幾[隻][紙鶴]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<TIME_day>[^<]*?</TIME_day><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[昨天]比[今天]少摺了幾[隻][紙鶴]")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[3], entityAmount, lokiRst.getArgs(i)[2])])

                # [書][架][上][現在]還有幾[本][故事書]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><TIME_justtime>[^<]*?</TIME_justtime><FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[書][架][上][現在]還有幾[本][故事書]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    subject, entity, entityAmount = difference(subject, lokiRst.getArgs(i)[5], lokiRst.getArgs(i)[4])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[5], entityAmount, lokiRst.getArgs(i)[4])])

                # [二]年級[三]班比[二]年級[一]班多幾人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]年級[三]班比[二]年級[一]班多幾人")
                    subject1 = lokiRst.getArgs(i)[1]+"班"
                    subject2 = lokiRst.getArgs(i)[3]+"班"
                    entity = lokiRst.getArgs(i)[0] + "年級"
                    entityAmount = comparative(subject1, entity, subject2, entity, "人")
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])

                # [二]年級[三]班比[二]年級[一]班少幾人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]年級[三]班比[二]年級[一]班少幾人")
                    subject1 = lokiRst.getArgs(i)[1]+"班"
                    subject2 = lokiRst.getArgs(i)[3]+"班"
                    entity = lokiRst.getArgs(i)[0] + "年級"
                    entityAmount = comparative(subject1, entity, subject2, entity, "人")
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])

                # [二]年級[一]班和[二]年級[二]班共有多少人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]年級[一]班和[二]年級[二]班共有多少人")
                    entity = lokiRst.getArgs(i)[0]+"年級"
                    entityAmount = inTotal(lokiRst.getArgs(i)[1]+"班", entity, "人")[2] + inTotal(lokiRst.getArgs(i)[3]+"班", entity, "人")[2]
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])

                # [洋娃娃]和[猴子]各[一個]一共需要多少元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><QUANTIFIER>各</QUANTIFIER><ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>元</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[洋娃娃]和[猴子]各[一個]一共需要多少元")

                # 還有多少人沒捉住
                if lokiRst.getPattern(i) == "<FUNC_conjunction>[^<]*?</FUNC_conjunction><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined><FUNC_negation>[^<]*?</FUNC_negation>((<ACTION_verb>[^<不]*?[捉住][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉住][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "還有多少人沒捉住")
                    subject, entity, entityAmount = difference("","", "人")
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])

                # 上車的[人][中]有多少[人]站著
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[上車][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上車][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[站著][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[站著][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "上車的[人][中]有多少[人]站著")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}人".format(entityAmount)])


                # 沒有捉到的[小朋友]有多少[個]
                if lokiRst.getPattern(i) == "<FUNC_negation>[^<]*?</FUNC_negation>((<ACTION_verb>[^<不]*?[捉到][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉到][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "沒有捉到的[小朋友]有多少[個]")
                    subject, entity, entityAmount = difference("", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[1])])

                # [收入]多少萬元
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><KNOWLEDGE_currency>萬元</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[收入]多少萬元")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], "萬元")
                    questionDICT["Process"].append([s, "{}萬元".format(entityAmount)])

                # [水果]多少[公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[水果]多少[公斤]")
                    subject, entity, entityAmount = inTotal("", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[1])])

                # [商店]還有[水果]多少[公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[商店]還有[水果]多少[公斤]")
                    subject, entity, entityAmount = difference(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])


                # 還需要多少人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "還需要多少[人]")
                    subject, entity, entityAmount = difference("", "", "人")
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, "人")])

                # [植物園][裡]有多少人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[植物園][裡]有多少人")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], "", "人")
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, "人")])

                # 比原計畫增產多少[打]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[計畫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[計畫][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[增產][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[增產][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "比原計畫增產多少[打]")
                    subject, entity, entityAmount = inTotal("", "", lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[0])])

                # [商店]有[蘋果]多少[公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[商店]有[蘋果]多少[公斤]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])

                # [媽媽]帶了多少[錢]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[帶][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[帶][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]帶了多少[錢]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], "", "元")
                    questionDICT["Process"].append([s, "{}元".format(entityAmount)])

                # [楊阿姨]已經打了多少[個][字]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ACTION_lightVerb>[^<]*?</ACTION_lightVerb><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[楊阿姨]已經打了多少[個][字]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2])])

                # [獵豹]最快時速比[馬]最快時速快多少
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><DegreeP>最快</DegreeP><ENTITY_UserDefined>時速</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><DegreeP>最快</DegreeP><ENTITY_UserDefined>時速</ENTITY_UserDefined><MODIFIER>快</MODIFIER><CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ>":
                    doSomethingAbout(lokiRst.getArgs(i), "[獵豹]最快時速比[馬]最快時速快多少")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], "", lokiRst.getArgs(i)[1], "", "公里")
                    questionDICT["Process"].append([s, "{}公里".format(entityAmount)])

                # [小萱]寫了幾[行][國字]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[寫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[寫][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小萱]寫了幾[行][國字]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2])])

                # [蘋果]和[梨]一共有多少[公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[蘋果]和[梨]一共有多少[公斤]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])

                # [媽媽]比[黃阿姨]多買幾[個][月餅]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]比[黃阿姨]多買幾[個][月餅]")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])

                # [花瓶][裡]有幾[朵][白][玫瑰]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[花瓶][裡]有幾[朵][白][玫瑰]")
                    subject, entity, entityAmount = inTotal(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])

                # [小湘]比[小強]多幾[張][貼紙]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小湘]比[小強]多幾[張][貼紙]")
                    entityAmount = comparative(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}{}".format(entityAmount, lokiRst.getArgs(i)[2])])
            # </Question>

            # <Definition>
            if lokiRst.getIntent(i) == "Definition":
                # [羊][3隻]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    if len(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]) == len(s):
                        doSomethingAbout(lokiRst.getArgs(i), "[羊][3隻]")
                        numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                        unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                        existential("", lokiRst.getArgs(i)[0], amount, unit)
                        questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [女生][16]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[女生][16]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    existential("", lokiRst.getArgs(i)[0], amount, "人")
                    questionDICT["Process"].append([s, "{}={}人".format(lokiRst.getArgs(i)[0], amount)])

                # 有[12米][布]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[12米][布]")
                # [甲數]是[20]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><ENTITY_num>[^<]*?</ENTITY_num>":
                    doSomethingAbout(lokiRst.getArgs(i), "[甲數]是[20]")
                    existential("", lokiRst.getArgs(i)[0], int(lokiRst.getArgs(i)[1]), "")
                    questionDICT["Process"].append([s, "{}={}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1])])

                # [葡萄][18元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    if lokiRst.getArgs(i)[0] not in ["我", "他", "她"] and len(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]) == len(s):    # to be improved
                        doSomethingAbout(lokiRst.getArgs(i), "[葡萄][18元]")
                        numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                        unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                        existential("", lokiRst.getArgs(i)[0], amount, unit)
                        questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [小雨]有[7元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小雨]有[7元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [一]班有[42]人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[一]班有[42]人")
                    subject = lokiRst.getArgs(i)[0]+"班"
                    existential(subject, "", int(lokiRst.getArgs(i)[1]), "人")
                    questionDICT["Process"].append([s, "{}={}人".format(subject, lokiRst.getArgs(i)[1])])

                # 有[38個][罐頭]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[38個][罐頭]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 有[公雞][44隻]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[公雞][44隻]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [男生]有[35]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[男生]有[35]人")
                    if "其中" not in s:
                        numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                        existential("", lokiRst.getArgs(i)[0], amount, "人")
                        questionDICT["Process"].append([s, "{}={}人".format(lokiRst.getArgs(i)[0], amount)])

                # [約翰]有[10元]
                if lokiRst.getPattern(i) == "<ENTITY_person>[^<]*?</ENTITY_person>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[約翰]有[10元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [小軒][今年][7]歲
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_year>[^<]*?</TIME_year><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小軒][今年][7]歲")
                # [弟弟]踢了[6][下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[踢][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[踢][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[弟弟]踢了[6][下]")
                    existential(lokiRst.getArgs(i)[0], "", int(lokiRst.getArgs(i)[1]), lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # 有[5個]是[雞蛋]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[5個]是[雞蛋]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [白][珠子]有[2顆]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[白][珠子]有[2顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    entity = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, amount, unit)])

                # [蘋果派]有[9個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[蘋果派]有[9個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [一本][85頁]的[書]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[一本][85頁]的[書]")
                # [二]班[27名][男生]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班[27名][男生]")
                # [二]班[男生][27名]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班[男生][27名]")
                # [國旗杆]高[12米]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>高</MODIFIER><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[國旗杆]高[12米]")
                # [撲滿][裡]有[22元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[撲滿][裡]有[22元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    existential(subject, "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(subject, amount, unit)])

                # [瑋瑋]原有[13元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[瑋瑋]原有[13元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 其中[男生]有[9個]
                if lokiRst.getPattern(i) == "<FUNC_inner>其中</FUNC_inner><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "其中[男生]有[9個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], -amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # 其中[女生]有[7]人
                if lokiRst.getPattern(i) == "<FUNC_inner>其中</FUNC_inner><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其中[女生]有[7]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    existential("", lokiRst.getArgs(i)[0], -amount, "人")
                    questionDICT["Process"].append([s, "{}={}人".format(lokiRst.getArgs(i)[0], -amount)])

                # [小娟]有[7張][貼紙]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小娟]有[7張][貼紙]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    subject = lokiRst.getArgs(i)[0]
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [車][上]原有[6隻][貓]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[車][上]原有[6隻][貓]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[3], amount, unit)])

                # [二]班[圖書]有[67本]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班[圖書]有[67本]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject = lokiRst.getArgs(i)[0]+"班"
                    existential(subject, lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[1], amount, unit)])

                # [二]班有[27名][男生]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班有[27名][男生]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject = lokiRst.getArgs(i)[0]+"班"
                    existential(subject, lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[2], amount, unit)])

                # [二]班有[男生][27名]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班有[男生][27名]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject = lokiRst.getArgs(i)[0]+"班"
                    existential(subject, lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[1], amount, unit)])

                # [池][裡]有[30條][小魚]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[池][裡]有[30條][小魚]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[3], amount, unit)])

                # [球場][上]原有[33]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[球場][上]原有[33]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    existential(subject, "", amount, "人")
                    questionDICT["Process"].append([s, "{}_人={}人".format(subject, amount)])

                # [CD][盒][裡]有[12片][光碟]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[CD][盒][裡]有[12片][光碟]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[4], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, lokiRst.getArgs(i)[4], amount, unit)])

                # [小玲]寫了[4行][國字]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[寫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[寫][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小玲]寫了[4行][國字]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)])

                # [二]年級[一]班有[42]人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>年級</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]年級[一]班有[42]人")
                    subject = lokiRst.getArgs(i)[1]+"班"
                    entity = lokiRst.getArgs(i)[0]+"年級"
                    existential(subject, entity, int(lokiRst.getArgs(i)[2]), "人")
                    questionDICT["Process"].append([s, "{}_{}={}人".format(entity, subject, lokiRst.getArgs(i)[1])])

                # [兔屋外]有[10隻][兔子]
                if lokiRst.getPattern(i) == "<LOCATION>[^<]*?</LOCATION>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[兔屋外]有[10隻][兔子]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [養雞場]有[公雞][44隻]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[養雞場]有[公雞][44隻]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [游泳池][裡]有[男生][6]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[游泳池][裡]有[男生][6]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    existential(subject, lokiRst.getArgs(i)[2], amount, "人")
                    questionDICT["Process"].append([s, "{}_{}={}人".format(subject, lokiRst.getArgs(i)[2], amount)])

                # 有[7枝][藍筆]和[5枝][紅筆]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[7枝][藍筆]和[5枝][紅筆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[3], amount, unit)

                    questionDICT["Process"].append([s, "{}={}; {}={}".format(lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])])

                # [班級][裡]有[22張][臘光][紙]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[班級][裡]有[22張][臘光][紙]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    entity = lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, entity, amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, entity, amount, unit)])

                # [弟弟]有[3塊][蕾神][巧克力]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[弟弟]有[3塊][蕾神][巧克力]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    entity = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], entity, amount, unit)])

                # [海底]有[6個][紅色][寶特瓶]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[海底]有[6個][紅色][寶特瓶]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    entity = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], entity, amount, unit)])

                # [農場][裡]有[36隻][牛]和[40隻][羊]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[農場][裡]有[36隻][牛]和[40隻][羊]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[3], amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[4])
                    unit = lokiRst.getArgs(i)[4].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[5], amount, unit)
                    questionDICT["Process"].append([s, "{0}_{1}+{2}; {0}_{3}+{4}".format(subject, lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[5], lokiRst.getArgs(i)[4])])

                # 有[10條][紅][緞帶]和[6條][藍][緞帶]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[10條][紅][緞帶]和[6條][藍][緞帶]")

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2], amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[4]+lokiRst.getArgs(i)[5], amount, unit)

                    questionDICT["Process"].append([s, "{}{}={}; {}{}={}".format(lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[5], lokiRst.getArgs(i)[3])])

                # [草地][上]有[14枝][紅][風車]和[9枝][藍][風車]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[草地][上]有[14枝][紅][風車]和[9枝][藍][風車]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    entity = lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4]
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, entity, amount, unit)
                    processSTR = "{}_{}={}{}".format(subject, entity, amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[5])
                    entity = lokiRst.getArgs(i)[6]+lokiRst.getArgs(i)[7]
                    unit = lokiRst.getArgs(i)[5].replace(numberSTR, "")
                    existential(subject, entity, amount, unit)

                    questionDICT["Process"].append([s, "{0}_{1}={2}; {0}_{3}={4}".format(subject, lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[2], entity, lokiRst.getArgs(i)[5])])

                # 某班共有[46]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[共有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[共有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "某班共有[46]人")
                    if "共" in s:
                        numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                        existential("", "", amount, "人")
                        questionDICT["Process"].append([s, "{}人".format(amount)])

                # [水果店]有[水果][670公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[水果店]有[水果][670公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [批發站]原有[140筐][水果]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[批發站]原有[140筐][水果]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)])

                # [15個][小朋友]捉迷藏
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[捉迷藏][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉迷藏][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[15個][小朋友]捉迷藏")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [13個][小朋友]在玩捉迷藏
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[玩][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[玩][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[捉迷藏][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉迷藏][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[13個][小朋友]在玩捉迷藏")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [5年][1]班有[46]人
                if lokiRst.getPattern(i) == "<TIME_year>[^<]*?</TIME_year><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[5年][1]班有[46]人")
                    subject = lokiRst.getArgs(i)[0]
                    entity = lokiRst.getArgs(i)[1]+"班"
                    existential(subject, entity, int(lokiRst.getArgs(i)[2]), "人")
                    questionDICT["Process"].append([s, "{}_{}={}人".format(entity, subject, lokiRst.getArgs(i)[1])])

                # [舞蹈隊]需要[80]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[舞蹈隊]需要[80]人")
                    subject = lokiRst.getArgs(i)[0]
                    existential(subject, "", int(lokiRst.getArgs(i)[1]), "人")
                    questionDICT["Process"].append([s, "{}={}人".format(subject, lokiRst.getArgs(i)[1])])

                # 原計畫[8月]生產[手帕][780打]
                if lokiRst.getPattern(i) == "<MODIFIER>原</MODIFIER>((<ACTION_verb>[^<不]*?[計畫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[計畫][^<不]*?</VerbP>))<TIME_month>[^<]*?</TIME_month>((<ACTION_verb>[^<不]*?[生產][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[生產][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "原計畫[8月]生產[手帕][780打]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    entity = lokiRst.getArgs(i)[1]
                    existential("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, amount, unit)])

                # 還剩[485打]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "還剩[485打]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format("", amount, unit)])

                # 還剩餘[15.80元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩餘][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩餘][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "還剩餘[15.80元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format("", amount, unit)])

                # [獵豹]最快時速是每[小時][113公里]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><DegreeP>最快</DegreeP><ENTITY_UserDefined>時速</ENTITY_UserDefined><AUX>[^<]*?</AUX><QUANTIFIER>每</QUANTIFIER><TIME_justtime>[^<]*?</TIME_justtime><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[獵豹]最快時速是每[小時][113公里]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [小明][寒假]看[一本][126頁]的[科普書]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_season>[^<]*?</TIME_season>((<ACTION_verb>[^<不]*?[看][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[看][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明][寒假]看[一本][126頁]的[科普書]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[4], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[4], amount, unit)])

                # [小明]看[一本][35頁]的[書]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[看][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[看][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]看[一本][35頁]的[書]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[3], amount, unit)])

                # [鋼材]長[18.4公尺]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>長</MODIFIER><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[鋼材]長[18.4公尺]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 有[一批][貨物][14.6噸]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[一批][貨物][14.6噸]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [電視機]原價是[5800元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>原價</ENTITY_UserDefined><AUX>[^<]*?</AUX><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[電視機]原價是[5800元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [倉儲][裡]有[水泥][88噸]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[倉儲][裡]有[水泥][88噸]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # 有[水泥][88噸]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "有[水泥][88噸]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [一根][繩子][4公尺]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[一根][繩子][4公尺]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 若某[次][數學]考試標準[成績]定為[85分]
                if lokiRst.getPattern(i) == "<ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[考試][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[考試][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[定為][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[定為][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "若某[次][數學]考試標準[成績]定為[85分]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [成績]定為[85分]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[定為][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[定為][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "[成績]定為[85分]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [一本][19.5元]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[一本][19.5元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format("", amount, unit)])

                # [珠穆朗瑪峰]的[海拔][高度]為[海平面]以上[8844m]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[珠穆朗瑪峰]的[海拔][高度]為[海平面]以上[8844m]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[4])
                    unit = lokiRst.getArgs(i)[4].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [高度]為[8844m]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[高度]為[8844m]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [吐魯番盆地]的[高度]為[海平面]以下[155公尺]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[吐魯番盆地]的[高度]為[海平面]以下[155公尺]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(lokiRst.getArgs(i)[3], amount, unit)])

                # [速度]是每[小時][13.5公里]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><AUX>[^<]*?</AUX><QUANTIFIER>每</QUANTIFIER><TIME_justtime>[^<]*?</TIME_justtime><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[速度]是每[小時][13.5公里]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}/小時".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 其中[1200雙]是[塑料][涼鞋]
                if lokiRst.getPattern(i) == "<FUNC_inner>其中</FUNC_inner><ENTITY_classifier>[^<]*?</ENTITY_classifier><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其中[1200雙]是[塑料][涼鞋]")
                    entity = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    existential("", entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}".format(entity, -amount, unit)])

                # [花瓶][裡]有[15朵][紅][玫瑰]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[花瓶][裡]有[15朵][紅][玫瑰]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    entity = lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, entity, amount, unit)
                    questionDICT["Process"].append([s, "{}_{}={}{}".format(subject, entity, amount, unit)])
            # </Definition>

            # <Calculation_Addition>
            if lokiRst.getIntent(i) == "Calculation_Addition":
                if "比" in s:
                    continue

                # 做了[3個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "做了[3個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 再過[5年]
                if lokiRst.getPattern(i) == "<MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[過][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[過][^<不]*?</VerbP>))<TIME_year>[^<]*?</TIME_year>":
                    doSomethingAbout(lokiRst.getArgs(i), "再過[5年]")
                # 吃了[5顆]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "吃了[5顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 壞掉[6個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[壞掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[壞掉][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "壞掉[6個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 移走[5個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[移走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[移走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "移走[5個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 拿到[4個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[拿到][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拿到][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "拿到[4個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又拿到[4個]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[拿到][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拿到][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又拿到[4個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 摘採[6個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[摘採][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摘採][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "摘採[6個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 用了[8元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "用了[8元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 謝了[4朵]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[謝][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[謝][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "謝了[4朵]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 買了[四個][蛋糕]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "買了[四個][蛋糕]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 賣掉[1個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[賣掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣掉][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "賣掉[1個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 離開[8個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[離開][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[離開][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "離開[8個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 得到[20元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[得到][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[得到][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "得到[20元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, amount, unit)])

                # 用去[38張]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "用去[38張]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 運進[21個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[運進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運進][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "運進[21個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [4]人下台[後]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[下台][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[下台][^<不]*?</VerbP>))<RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[4]人下台[後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # [4個]下台[後]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[下台][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[下台][^<不]*?</VerbP>))<RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[4個]下台[後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [6個]壞掉[後]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[壞掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[壞掉][^<不]*?</VerbP>))<RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[6個]壞掉[後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 再游來[1條]
                if lokiRst.getPattern(i) == "<MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[游來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[游來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "再游來[1條]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又移走[3個]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[移走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[移走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又移走[3個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 又跑來[6隻]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[跑來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[跑來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又跑來[6隻]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 投進了[6]球
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[投進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[投進][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>球</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "投進了[6]球")
                # 給[虎客][8塊]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "給[虎客][8塊]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 再堆疊[10個]
                if lokiRst.getPattern(i) == "<MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[堆疊][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[堆疊][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "再堆疊[10個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又來了[10]人
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[來][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "又來了[10]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", amount, "人")
                    questionDICT["Process"].append([s, "+{}人".format(amount)])

                # 又運進[21個]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[運進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運進][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又運進[21個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又開來[13輛]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[開來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[開來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又開來[13輛]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小福]得[42分]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[得][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小福]得[42分]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 有[四]人下台
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[下台][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[下台][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "有[四]人下台")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(amount)])

                # [3隻][貓]上車[後]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[上車][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上車][^<不]*?</VerbP>))<RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[3隻][貓]上車[後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [4個][人]下台[後]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[下台][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[下台][^<不]*?</VerbP>))<RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[4個][人]下台[後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[1], -amount, unit)])

                # 又購買了[4條]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[購買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[購買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又購買了[4條]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小娟]做了[3個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小娟]做了[3個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小華]吃了[4顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小華]吃了[4顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}_{}{}{}".format(lokiRst.getArgs(i)[0], entity, -amount, unit)])

                # [後面]還有[7]人
                if lokiRst.getPattern(i) == "<RANGE>[^<]*?</RANGE><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[後面]還有[7]人")
                # 放入[2個][籃球]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[放入][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放入][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "放入[2個][籃球]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [1]班還回來[9個]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[回來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[回來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[1]班還回來[9個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [上午]做了[38朵]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[上午]做了[38朵]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又給[弟弟][10元]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "又給[弟弟][10元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{0}+{1}{2}; {3}-{1}{2}".format(lokiRst.getArgs(i)[0], amount, unit, subject)])

                # [奶奶]包了[13個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[包][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[包][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[奶奶]包了[13個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小紅]拿了[60元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[拿][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拿][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小紅]拿了[60元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}_{}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # 運進[21個][作品]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[運進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運進][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "運進[21個][作品]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [2]班借走了[14個]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[借走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[借走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[2]班借走了[14個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    subject = lokiRst.getArgs(i)[0]+"班"
                    transitive(subject, entity, amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 其他的是[鴨蛋]
                if lokiRst.getPattern(i) == "<MODIFIER>其他</MODIFIER><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其他的是[鴨蛋]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 其餘的是[小雞]
                if lokiRst.getPattern(i) == "<MODIFIER>其餘</MODIFIER><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其餘的是[小雞]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 剩餘的是[柳樹]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩餘][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩餘][^<不]*?</VerbP>))<AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "剩餘的是[柳樹]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # [媽媽]買了[兩枝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]買了[兩枝]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}_{}+{}{}".format(lokiRst.getArgs(i)[0], entity, amount, unit)])

                # 借給[小強][4本][後]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[借給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[借給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier><RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "借給[小強][4本][後]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 再放入[8個][排球]
                if lokiRst.getPattern(i) == "<MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[放入][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放入][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "再放入[8個][排球]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 又游來[2條][魟魚]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[游來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[游來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "又游來[2條][魟魚]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 又買[9隻]放進來
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[放進來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放進來][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "又買[9隻]放進來")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 吃了[9顆][巧克力]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "吃了[9顆][巧克力]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[1], -amount, unit)])

                # [妹妹]拿走了[5個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[拿走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拿走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[妹妹]拿走了[5個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [姊姊]再給[他][4張]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]再給[他][4張]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[1], "", amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 游來[2條][熱帶魚]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[游來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[游來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "游來[2條][熱帶魚]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [一]班用了[15張][紙]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[一]班用了[15張][紙]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject = lokiRst.getArgs(i)[0] + "班"
                    transitive(subject, lokiRst.getArgs(i)[2], -amount, unit)
                    questionDICT["Process"].append([s, "{}-{}{}".format(subject, amount, unit)])

                # [他]獲得[29枚][金牌]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[獲得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[獲得][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[他]獲得[29枚][金牌]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # 往上升了[10層]樓
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[上升][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上升][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>樓</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "往上升了[10層]樓")
                # 挑走了[17個][作品]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[挑走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[挑走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "挑走了[17個][作品]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[1], -amount, unit)])

                # [爸爸]又給[他][15元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[爸爸]又給[他][15元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[1], "", amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 現做[30個][甜甜圈]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[現做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[現做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "現做[30個][甜甜圈]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [自己]也花掉[20元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[花掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[花掉][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[自己]也花掉[20元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    if lokiRst.getArgs(i)[0] == "自己":
                        subject, entity = transitive("", "", -amount, unit)
                    else:
                        subject, entity = transitive(lokiRst.getArgs(i)[1], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 購進[小提琴][52把]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[購進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[購進][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "購進[小提琴][52把]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[0], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 運來[57公斤][水果]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[運來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運來][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "運來[57公斤][水果]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 其他的是[綠][蘋果]
                if lokiRst.getPattern(i) == "<MODIFIER>其他</MODIFIER><AUX>[^<]*?</AUX><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其他的是[綠][蘋果]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 其他的是[草莓][派]
                if lokiRst.getPattern(i) == "<MODIFIER>其他</MODIFIER><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其他的是[草莓][派]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 其餘的是[紅][蘋果]
                if lokiRst.getPattern(i) == "<MODIFIER>其餘</MODIFIER><AUX>[^<]*?</AUX><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其餘的是[紅][蘋果]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 其餘的全部是[蘋果][樹]
                if lokiRst.getPattern(i) == "<MODIFIER>其餘</MODIFIER><AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "其餘的全部是[蘋果][樹]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # 剩餘的是[蘋果][樹]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[剩餘][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩餘][^<不]*?</VerbP>))<AUX>[^<]*?</AUX><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "剩餘的是[蘋果][樹]")
                    ent, amount, unit = intransitive(lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1])
                    questionDICT["Process"].append([s, "{}{}{}".format(ent, -amount, unit)])

                # [小俊]拍球拍了[5][下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[拍球][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拍球][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[拍][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拍][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小俊]拍球拍了[5][下]")
                    transitive(lokiRst.getArgs(i)[0], "", int(lokiRst.getArgs(i)[1]), lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # [小木偶]再放進[6元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>再</MODIFIER>((<ACTION_verb>[^<不]*?[放進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放進][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小木偶]再放進[6元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(subject, amount, unit)])

                # [昨天]賣出[6雙][鞋子]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[昨天]賣出[6雙][鞋子]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[2], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[2], -amount, unit)])

                # 有[2個][小朋友]請假
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[請假][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[請假][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "有[2個][小朋友]請假")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[1], -amount, unit)])

                # [維尼]做了[7個][蝴蝶]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[維尼]做了[7個][蝴蝶]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [老師]又放上了[4本]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[放上][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放上][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[老師]又放上了[4本]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [奶奶]包了[13個][粽子]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[包][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[包][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[奶奶]包了[13個][粽子]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [廚師]烤了[15塊][餅乾]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[烤][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[烤][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[廚師]烤了[15塊][餅乾]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [老師]說要[11枝][鉛筆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[說][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[說][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[要][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[老師]說要[11枝][鉛筆]")
                # [英國]獲得[29枚][金牌]
                if lokiRst.getPattern(i) == "<LOCATION>[^<]*?</LOCATION>((<ACTION_verb>[^<不]*?[獲得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[獲得][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[英國]獲得[29枚][金牌]")
                # [養殖場]養了[93隻][雞]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[養][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[養][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[養殖場]養了[93隻][雞]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])


                # [公園][裡]新種[359棵][樹]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><ACTION_verb>新種</ACTION_verb><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[公園][裡]新種[359棵][樹]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(subject, lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}+{}{}".format(subject, lokiRst.getArgs(i)[3], amount, unit)])

                # [8片][光碟]放回[CD][盒][裡]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[放回][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放回][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[8片][光碟]放回[CD][盒][裡]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]+lokiRst.getArgs(i)[4]
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive(subject, lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [8片][光碟]放回[盒子][裡]
                if lokiRst.getPattern(i) == "<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[放回][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放回][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>":
                    doSomethingAbout(lokiRst.getArgs(i), "[8片][光碟]放回[盒子][裡]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive(subject, lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 又買[9隻][鴨子]放進來
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[放進來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放進來][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "又買[9隻][鴨子]放進來")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # 又跑來了[2隻][綠][頭鴨]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[跑來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[跑來][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "又跑來了[2隻][綠][頭鴨]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    entity = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [叔叔]又買[9隻]放進來
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>((<ACTION_verb>[^<不]*?[放進來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放進來][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[叔叔]又買[9隻]放進來")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [叔叔]又送給[我們][5顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[送給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[送給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[叔叔]又送給[我們][5顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[1], "", amount, unit)
                    transitive(lokiRst.getArgs(i)[0], entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小傑]換了[7隻][熊寶貝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[換][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小傑]換了[7隻][熊寶貝]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [小正]吃了[9顆][巧克力]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小正]吃了[9顆][巧克力]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[2], -amount, unit)])

                # [維尼]做了[7個][蝴蝶][結]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[維尼]做了[7個][蝴蝶][結]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    entity = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [哥哥]自己也花掉[20元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>自己</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[花掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[花掉][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]自己也花掉[20元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # [商店]運來[蘋果][38公斤]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[運來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運來][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[商店]運來[蘋果][38公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [大毛]摺了[14架][紙飛機]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[大毛]摺了[14架][紙飛機]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [媽媽]購買了[12個][月餅]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[購買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[購買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]購買了[12個][月餅]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [學校]挑走了[17個][作品]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[挑走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[挑走][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[學校]挑走了[17個][作品]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[2], -amount, unit)])

                # [今天]有[2個][小朋友]請假
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[請假][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[請假][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[今天]有[2個][小朋友]請假")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[2], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[2], -amount, unit)])

                # [國王]做了[4][下]仰臥起坐
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>((<ACTION_verb>[^<不]*?[仰臥起坐][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[仰臥起坐][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[國王]做了[4][下]仰臥起坐")
                    transitive(lokiRst.getArgs(i)[0], "", int(lokiRst.getArgs(i)[1]), lokiRst.getArgs(i)[2])
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # [小宏]買給[小華][4顆][蘋果]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[買給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小宏]買給[小華][4顆][蘋果]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}; ".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [小欣][昨天]摺了[4隻][紙鶴]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小欣][昨天]摺了[4隻][紙鶴]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[3], amount, unit)])

                # [鞋店][昨天]賣出[6雙][鞋子]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[鞋店][昨天]賣出[6雙][鞋子]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[3], -amount, unit)])

                # [妮妮][中餐]吃了[12顆][水餃]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[妮妮][中餐]吃了[12顆][水餃]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], -amount, unit)
                    questionDICT["Process"].append([s, "{}-{}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # [叔叔]又買[7隻][鴨子]放進來
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[放進來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[放進來][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[叔叔]又買[7隻][鴨子]放進來")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [小正][上午]吃了[9顆][巧克力]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小正][上午]吃了[9顆][巧克力]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[3], -amount, unit)])

                # [大棕熊]堆疊了[28個][魚罐頭]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[堆疊][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[堆疊][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[大棕熊]堆疊了[28個][魚罐頭]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [花園][裡]的[玉蘭花]開了[12朵]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[開][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[開][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[花園][裡]的[玉蘭花]開了[12朵]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    transitive(subject, lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[2], amount, unit)])

                # [哥哥]幫[弟弟]買[糖果]花掉[100元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[幫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[幫][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[花掉][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[花掉][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]幫[弟弟]買[糖果]花掉[100元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # [船長]準備了[12片][牛肉]和[4片][豬肉]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[準備][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[準備][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[船長]準備了[12片][牛肉]和[4片][豬肉]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    existential(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[4], amount, unit)
                    questionDICT["Process"].append([s, "{0}_{1}+{2}; {0}_{3}+{4}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[4], lokiRst.getArgs(i)[3])])

                # [花園][裡]開了[11朵][白花]和[8朵][紅花]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[開][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[開][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[花園][裡]開了[11朵][白花]和[8朵][紅花]")
                    subject = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[3], amount, unit)

                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[4])
                    unit = lokiRst.getArgs(i)[4].replace(numberSTR, "")
                    existential(subject, lokiRst.getArgs(i)[5], amount, unit)
                    questionDICT["Process"].append([s, "{0}_{1}+{2}; {0}_{3}+{4}".format(subject, lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[5], lokiRst.getArgs(i)[4])])

                # 已經捉住了[4]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[捉住][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉住][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經捉住了[4]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", amount, "人")
                    questionDICT["Process"].append([s, "{}{}人".format(entity, -amount)])

                # 上來了[9]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[上來][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上來][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "上來了[9]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", amount, "人")
                    questionDICT["Process"].append([s, "+{}人".format(amount)])

                # 參加[美術][小組]的有[12]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[參加][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[參加][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "參加[美術][小組]的有[12]人")
                    entity = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    subject, entity = transitive("", entity, amount, "人")
                    questionDICT["Process"].append([s, "{}+{}人".format(entity, amount)])

                # 已經捉到了其中的[3個][人]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[捉到][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉到][^<不]*?</VerbP>))<FUNC_inner>其中</FUNC_inner><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經捉到了其中的[3個][人]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    if lokiRst.getArgs(i)[1] == "人":
                        subject, entity = transitive("", "", -amount, unit)
                        questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])
                    else:
                        transitive("", lokiRst.getArgs(i)[1], -amount, unit)
                        questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[1], -amount, unit)])

                # 已經生產了[653塊]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[生產][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[生產][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經生產了[653塊]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [中午]走了[107]人
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[走][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[中午]走了[107]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    subject, entity = transitive("", "", -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # [上午]賣出[132公斤]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[上午]賣出[132公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [下午]購進[145公斤]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[購進][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[購進][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[下午]購進[145公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小明]第[一天]讀了[47頁]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_determiner>[^<]*?</FUNC_determiner><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[讀][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[讀][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]第[一天]讀了[47頁]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive("第"+lokiRst.getArgs(i)[1], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 第[二天]讀了[53頁]
                if lokiRst.getPattern(i) == "<FUNC_determiner>[^<]*?</FUNC_determiner><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[讀][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[讀][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "第[二天]讀了[53頁]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("第"+lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [樂樂]買[書]用去[8.55元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[樂樂]買[書]用去[8.55元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # 買[鋼筆]用去[3.2元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "買[鋼筆]用去[3.2元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", lokiRst.getArgs(i)[0], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(subject, -amount, unit)])

                # 付給[售貨員][15元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[付給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[付給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "付給[售貨員][15元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(subject, -amount, unit)])

                # 已經量了[身高]的有[396]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[量][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[量][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經量了[身高]的有[396]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    subject, entity = transitive("", lokiRst.getArgs(i)[0], -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # 下車[12]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[下車][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[下車][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "下車[12]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # 上車[19]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[上車][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上車][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "上車[19]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", amount, "人")
                    questionDICT["Process"].append([s, "+{}人".format(amount)])

                # 第[一天]看了[24頁]
                if lokiRst.getPattern(i) == "<FUNC_determiner>[^<]*?</FUNC_determiner><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[看][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[看][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "第[一天]看了[24頁]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive("", "第"+lokiRst.getArgs(i)[0], -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 已經參觀過[博物館]的有[398]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[參觀過][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[參觀過][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經參觀過[博物館]的有[398]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    subject, entity = transitive("", lokiRst.getArgs(i)[0], -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # [108]人上船
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[上船][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[上船][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[108]人上船")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    subject, entity = transitive("", "", amount, "人")
                    questionDICT["Process"].append([s, "+{}人".format(amount)])

                # [中午]有[215]人離去
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[離去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[離去][^<不]*?</VerbP>))":
                    doSomethingAbout(lokiRst.getArgs(i), "[中午]有[215]人離去")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    subject, entity = transitive("", "", -amount, "人")
                    questionDICT["Process"].append([s, "{}人".format(-amount)])

                # 借出[40本]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[借出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[借出][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "借出[40本]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 又還回[285本]
                if lokiRst.getPattern(i) == "<FUNC_inner>又</FUNC_inner>((<ACTION_verb>[^<不]*?[回][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[回][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "又還回[285本]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, amount, unit)])

                # 參加了[3個][興趣][小組]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[參加][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[參加][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "參加了[3個][興趣][小組]")
                    entity = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 洗米需要[1分鐘]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[洗米][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[洗米][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "洗米需要[1分鐘]")
                    entity = s[:s.find("需要")]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 煮飯需要[15分鐘]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[煮飯][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[煮飯][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "煮飯需要[15分鐘]")
                    entity = s[:s.find("需要")]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # 炒菜需要[10分鐘]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[炒菜][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[炒菜][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[需要][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[需要][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "炒菜需要[10分鐘]")
                    entity = s[:s.find("需要")]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", entity, amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])

                # [小明]已經看了[100頁]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[看][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[看][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]已經看了[100頁]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 買了[48.2元]的[零食]和[18.43元]的[文具]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "買了[48.2元]的[零食]和[18.43元]的[文具]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}={}; {}={}".format(lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], lokiRst.getArgs(i)[2])])

                # 找回了[13.37元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[找回][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[找回][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "找回了[13.37元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", amount, unit)
                    questionDICT["Process"].append([s, "+{}{}".format(amount, unit)])

                # [小兔]摘了[136個][果子]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[摘][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摘][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小兔]摘了[136個][果子]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)])

                # 先運走[45.2噸]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[運走][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[運走][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "先運走[45.2噸]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [媽媽]帶[100元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[帶][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[帶][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]帶[100元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[0], amount, unit)])

                # 用去[1.6公尺]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "用去[1.6公尺]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [阿姨]打[一份][1000個][字]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ACTION_lightVerb>[^<]*?</ACTION_lightVerb><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[阿姨]打[一份][1000個][字]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[3], amount, unit)])

                # [小明]做[數學][作業]用去[0.15小時]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]做[數學][作業]用去[0.15小時]")
                    entity = lokiRst.getArgs(i)[1]+lokiRst.getArgs(i)[2]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}_{}{}{}".format(lokiRst.getArgs(i)[0], entity, -amount, unit)])

                # 用去[0.15小時]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "用去[0.15小時]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 做[數學][作業]用去[0.15小時]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))((<ACTION_verb>[^<不]*?[去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[去][^<不]*?</VerbP>))<TIME_justtime>[^<]*?</TIME_justtime>":
                    doSomethingAbout(lokiRst.getArgs(i), "做[數學][作業]用去[0.15小時]")
                    entity = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive("", entity, -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [上午]收[雞蛋][85公斤]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[收][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[收][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "[上午]收[雞蛋][85公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    transitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}_{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # 賣出[42公斤]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[賣出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[賣出][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "賣出[42公斤]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # [他]付出[50元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[付出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[付出][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[他]付出[50元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    if lokiRst.getArgs(i)[0] in ["他", "她"]:
                        subject, entity = transitive("", "", -amount, unit)
                        questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])
                    else:
                        subject, entity = transitive(lokiRst.getArgs(i)[0], "", -amount, unit)
                        questionDICT["Process"].append([s, "{}{}{}".format(lokiRst.getArgs(i)[0], -amount, unit)])

                # 生產[4500雙][涼鞋]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[生產][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[生產][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "生產[4500雙][涼鞋]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    transitive("", lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(lokiRst.getArgs(i)[1], amount, unit)])

                # [中午]離去[186]人
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[離去][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[離去][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[中午]離去[186]人")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}".format(-amount, unit)])

                # 已經捉住了[4個]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[捉住][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[捉住][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "已經捉住了[4個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[0])
                    unit = lokiRst.getArgs(i)[0].replace(numberSTR, "")
                    subject, entity = transitive("", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}{}{}".format(entity, -amount, unit)])

                # 買了[水壺][後]還剩[57元]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[剩][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[剩][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "買了[水壺][後]還剩[57元]")
                # [小豬]摘的[個數]和[小兔]同樣多
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[摘][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摘][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><FUNC_conjunction>[^<]*?</FUNC_conjunction><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小豬]摘的[個數]和[小兔]同樣多")
                # 第[二天]看的與第[一天]同樣多
                if lokiRst.getPattern(i) == "<FUNC_determiner>[^<]*?</FUNC_determiner><TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[看][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[看][^<不]*?</VerbP>))<FUNC_conjunction>[^<]*?</FUNC_conjunction><FUNC_determiner>[^<]*?</FUNC_determiner><TIME_day>[^<]*?</TIME_day><MODIFIER>多</MODIFIER>":
                    doSomethingAbout(lokiRst.getArgs(i), "第[二天]看的與第[一天]同樣多")
                # 訂《[少年報]》的有[40]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[訂][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[訂][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "訂《[少年報]》的有[40]人")
                # 訂《[小主][人報]》的有[25]人
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[訂][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[訂][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[有][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[有][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "訂《[小主][人報]》的有[25]人")

                # [今天]摺了[46隻]
                if lokiRst.getPattern(i) == "<TIME_day>[^<]*?</TIME_day>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[今天]摺了[46隻]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[1])
                    unit = lokiRst.getArgs(i)[1].replace(numberSTR, "")
                    subject, entity = transitive(lokiRst.getArgs(i)[0], "", amount, unit)
                    questionDICT["Process"].append([s, "{}+{}{}".format(entity, amount, unit)])
            # </Calculation_Addition>

            # <Calculation_Comparison>
            if lokiRst.getIntent(i) == "Calculation_Comparison":
                # 比[梨]少[25公斤]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER><ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "比[梨]少[25公斤]")

                # [2]班比[3]班少[7]人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[2]班比[3]班少[7]人")
                # [3]班比[1]班多[3]人
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[3]班比[1]班多[3]人")

                # [乙數]比[甲數]多[5]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num>":
                    doSomethingAbout(lokiRst.getArgs(i), "[乙數]比[甲數]多[5]")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", int(lokiRst.getArgs(i)[2]), "")
                    questionDICT["Process"].append([s, "{}={}+{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # [乙數]比[甲數]少[5]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num>":
                    doSomethingAbout(lokiRst.getArgs(i), "[乙數]比[甲數]少[5]")
                # 比[房子]高出[3米]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[高出][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[高出][^<不]*?</VerbP>))<ENTITY_measurement>[^<]*?</ENTITY_measurement>":
                    doSomethingAbout(lokiRst.getArgs(i), "比[房子]高出[3米]")
                # [哥哥]比[弟弟]多[5元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]比[弟弟]多[5元]")
                # [哥哥]比[弟弟]少[5元]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<KNOWLEDGE_currency>[^<]*?</KNOWLEDGE_currency>":
                    doSomethingAbout(lokiRst.getArgs(i), "[哥哥]比[弟弟]少[5元]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [妹妹]比[姊姊]少[5張]
                if lokiRst.getPattern(i) == "":
                    doSomethingAbout(lokiRst.getArgs(i), "[妹妹]比[姊姊]少[5張]")
                # [姊姊]比[心慈]多[6]歲
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[心慈]多[6]歲")
                # [姊姊]比[心慈]大[6]歲
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[心慈]大[6]歲")
                # [姊姊]比[心慈]少[6]歲
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>歲</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[心慈]少[6]歲")
                # [家民]比[她]多買[3枝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[家民]比[她]多買[3枝]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(subject1, subject2, amount, unit)])

                # [小梅]比[他]多換[5隻]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[換][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[換][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小梅]比[他]多換[5隻]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], subject2, amount, unit)])

                # 比[二]班多用了[8張]
                if lokiRst.getPattern(i) == "((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "比[二]班多用了[8張]")
                # [男生]比[女生]多[2]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[男生]比[女生]多[2]人")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", int(lokiRst.getArgs(i)[2]), "人")
                    questionDICT["Process"].append([s, "{}={}+{}人".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # [男生]比[女生]少[2]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[男生]比[女生]少[2]人")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", -int(lokiRst.getArgs(i)[2]), "人")
                    questionDICT["Process"].append([s, "{}={}-{}人".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2])])

                # [皇后]比[公主]多[8顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[皇后]比[公主]多[8顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [黃花]比[紅花]少[9朵]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[黃花]比[紅花]少[9朵]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive("", "", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], -amount, unit)
                    questionDICT["Process"].append([s, "{}={}{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], -amount, unit)])

                # [豬肉]比[牛肉]少幾[片]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[豬肉]比[牛肉]少幾[片]")
                # [姊姊]比[弟弟]多踢[9][下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[踢][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[踢][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[弟弟]多踢[9][下]")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", int(lokiRst.getArgs(i)[2]), lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[3])])

                # [小明]比[小東]多跳[3]下
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[跳][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[跳][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]比[小東]多跳[3]下")
                # [小明]比[小東]少跳[3]下
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[跳][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[跳][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]比[小東]少跳[3]下")
                # [小玉]比[小美]少吃[3顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小玉]比[小美]少吃[3顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(subject1, subject2, amount, unit)])

                # [小萱]比[小玲]多寫[9行]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[寫][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[寫][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小萱]比[小玲]多寫[9行]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [王子]比[國王]多做[9][下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[做][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[做][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[王子]比[國王]多做[9][下]")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", int(lokiRst.getArgs(i)[2]), lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[3])])

                # [小威]比[小俊]多拍[19][下]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[拍][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[拍][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ACTION_eventQuantifier>[^<]*?</ACTION_eventQuantifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小威]比[小俊]多拍[19][下]")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", int(lokiRst.getArgs(i)[2]), lokiRst.getArgs(i)[3])
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(subject1, subject2, lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[3])])

                # [姊姊]比[哥哥]少買幾[枝]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[買][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[買][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[姊姊]比[哥哥]少買幾[枝]")
                # [小明]比[小優]多吃了[7顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]比[小優]多吃了[7顆]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [小毛]比[大毛]多摺了[8架]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小毛]比[大毛]多摺了[8架]")
                # [小毛]比[大毛]少摺了[8架]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小毛]比[大毛]少摺了[8架]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], "", "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [白][玫瑰]比[紅][玫瑰]少[9朵]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[白][玫瑰]比[紅][玫瑰]少[9朵]")
                    entity1 = lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1]
                    entity2 = lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3]
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[4])
                    unit = lokiRst.getArgs(i)[4].replace(numberSTR, "")
                    bitransitive("", "", entity1, entity2, -amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(entity1, entity2, amount, unit)])

                # [紅][氣球]比[藍][氣球]多[5個]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[紅][氣球]比[藍][氣球]多[5個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[4])
                    unit = lokiRst.getArgs(i)[4].replace(numberSTR, "")
                    bitransitive("", "", lokiRst.getArgs(i)[0]+lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2]+lokiRst.getArgs(i)[3], amount, unit)
                    questionDICT["Process"].append([s, "{}{}={}{}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[3], amount, unit)])

                # 甜[冰棒]比鹹[冰棒]多幾[隻]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比鹹][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比鹹][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "甜[冰棒]比鹹[冰棒]多幾[隻]")
                # [紅][風車]比[藍][風車]多幾[枝]
                if lokiRst.getPattern(i) == "<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<MODIFIER_color>[^<]*?</MODIFIER_color><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<CLAUSE_HowQ>[^<]*?</CLAUSE_HowQ><ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[紅][風車]比[藍][風車]多幾[枝]")
                # [二]班比[一]班多用了[6張][紙]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班比[一]班多用了[6張][紙]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0]+"班", lokiRst.getArgs(i)[1]+"班", lokiRst.getArgs(i)[3], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(subject1, subject2, amount, unit)])

                # [二]班比[一]班少用了[6張][紙]
                if lokiRst.getPattern(i) == "<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>班</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[用][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[用][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[二]班比[一]班少用了[6張][紙]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive(lokiRst.getArgs(i)[0]+"班", lokiRst.getArgs(i)[1]+"班", lokiRst.getArgs(i)[3], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(subject1, subject2, amount, unit)])

                # [足球]的個數比[排球]多[15個]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>個數</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[足球]的個數比[排球]多[15個]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    subject1, subject2 = bitransitive("", "", lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(subject1, subject2, amount, unit)])

                # [大目]比[阿草]多吃了[5塊][小披薩]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[吃][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[吃][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[大目]比[阿草]多吃了[5塊][小披薩]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [媽媽]給[小明]的[糖]比[爸爸]少[2顆]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[給][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[給][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[媽媽]給[小明]的[糖]比[爸爸]少[2顆]")
                # [小毛]比[大毛]多摺了[8架][紙飛機]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小毛]比[大毛]多摺了[8架][紙飛機]")
                # [小毛]比[大毛]少摺了[8架][紙飛機]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>少</MODIFIER>((<ACTION_verb>[^<不]*?[摺][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[摺][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小毛]比[大毛]少摺了[8架][紙飛機]")
                # [小車][上]的人比[大車][上]的多[9]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[多][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[多][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小車][上]的人比[大車][上]的多[9]人")
                # [小車][上]的人比[大車][上]的少[9]人
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE><ENTITY_UserDefined>人</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><RANGE>[^<]*?</RANGE>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_num>[^<]*?</ENTITY_num><ENTITY_UserDefined>人</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小車][上]的人比[大車][上]的少[9]人")
                # [小明]比[小紅]多得了[17個][小星星]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><MODIFIER>多</MODIFIER>((<ACTION_verb>[^<不]*?[得][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[得][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小明]比[小紅]多得了[17個][小星星]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[2])
                    unit = lokiRst.getArgs(i)[2].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], lokiRst.getArgs(i)[3], "", amount, unit)
                    questionDICT["Process"].append([s, "{}={}+{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[1], amount, unit)])

                # [小白兔]的[蘿蔔]比[小灰兔]少[12根]
                if lokiRst.getPattern(i) == "<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined><ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[比][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[比][^<不]*?</VerbP>))<ENTITY_UserDefined>[^<]*?</ENTITY_UserDefined>((<ACTION_verb>[^<不]*?[少][^<不]*?</ACTION_verb>)|(<VerbP>[^<不]*?[少][^<不]*?</VerbP>))<ENTITY_classifier>[^<]*?</ENTITY_classifier>":
                    doSomethingAbout(lokiRst.getArgs(i), "[小白兔]的[蘿蔔]比[小灰兔]少[12根]")
                    numberSTR, amount = amountSTRconvert(lokiRst.getArgs(i)[3])
                    unit = lokiRst.getArgs(i)[3].replace(numberSTR, "")
                    bitransitive(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], lokiRst.getArgs(i)[1], "", -amount, unit)
                    questionDICT["Process"].append([s, "{}={}-{}{}".format(lokiRst.getArgs(i)[0], lokiRst.getArgs(i)[2], amount, unit)])
            # </Calculation_Comparison>

    pprint(questionDICT)