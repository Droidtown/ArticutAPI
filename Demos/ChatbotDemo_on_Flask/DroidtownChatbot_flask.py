#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: CS_chatbot_flask.py
# Development starting date: 2019.07.13
# Developer: Peter. w (peter.w@droidtown.co), Wilbert (wilbert.phen@gmail.com)

import json
import re

from ArticutAPI.ArticutAPI import Articut


with open("config.json") as f:
    configDICT = json.loads(f.read())


from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("chatbotDemo.html")
    #return render_template('index.html')

@app.route("/ask", methods=["POST"])
def bot():
    inputSTR = request.values["inputSTR"]
    if inputSTR.startswith("ECHO_TEST"):
        responseSTR = "ECHO:{}".format(request.values["inputSTR"])
    else:
        pass
    responseSTR = ""
    articut = Articut()
    inputDICT = articut.parse(inputSTR, level="lv1", userDefinedDictFILE=configDICT["userDefinedDICT"])

    #<預檢查:程式邏輯>
    if "_verb" in "".join(inputDICT["result_pos"]):
        pass
    elif "AUX" in "".join(inputDICT["result_pos"]):
        pass
    else:
        return "你給的資訊太少了，我不明白你問的「{}」是什麼意思。".format(inputSTR)
    #</預檢查:程式邏輯>

    #<後檢查:程式邏輯>
    ansCandidateLIST = segTokenMatchListFinder(inputDICT["result_pos"], articut)
    if len(ansCandidateLIST)>0:
        responseSTR = "\n".join([a[0] for a in ansCandidateLIST])
        #responseSTR = "您可以考慮掛 "+"".join([a[0].split("負責")[0] for a in ansCandidateLIST])
    else:
        responseSTR = "嗯，還有別的症狀嗎？"
    #</後檢查:程式邏輯>
    return responseSTR

def segTokenMatchListFinder(inputSegTokenSTR, articut):
    inputSegTokenSTR = ''.join(inputSegTokenSTR)
    #<透過 UserDefinedLIST 中的 alias LIST 把使用者的輸入正規化>
    with open(configDICT["userDefinedDICT"], encoding="utf8") as f:
        userDefinedDICT = json.loads(f.read())

    inputLIST = re.finditer("<.*?>(.*?)</.*?>", inputSegTokenSTR)
    if inputLIST is None:
        return []

    formalizedSTR = []
    for wordSegment in inputLIST:
        current_word = wordSegment.group(0)
        for keys in userDefinedDICT:
            if wordSegment.group(1) in userDefinedDICT[keys]:
                current_word = re.sub(wordSegment.group(1), keys, current_word)
        formalizedSTR.append(current_word)
    formalizedSTR = ''.join(formalizedSTR)
    print("###formalizedSTR: ", formalizedSTR)
    #</透過 UserDefinedLIST 中的 alias LIST 把使用者的輸入正規化>

    #透過 LanguageKnowledge 取出可能的回答。
    with open(configDICT["domainKnowledge"], encoding="utf8") as f:
        knowledgeLIST = json.loads(f.read())

    UserDefindPat = re.compile("<UserDefined>[^<]*?</UserDefined>")
    UserDefinedFoundLIST = [u.group(0) for u in UserDefindPat.finditer(formalizedSTR)]
    #ActionPat = "<ACTION_verb>[^<]*?</ACTION_verb>"
    #ActionFoundLIST = [a.group(0) for a in re.finditer(ActionPat, inputSegTokenSTR["result_pos"][0])]
    #EntityPat = "<ENTITY_[^>]*?>[^<]*?</ENTITY_[^>]*?>"
    #EntityFoundLIST = [e.group(0) for e in re.finditer(EntityPat, inputSegTokenSTR["result_pos"][0])]


    candidateLIST = []
    for k in knowledgeLIST:
        if len(set([u.group(0) for u in UserDefindPat.finditer("".join(k[2]))]).intersection(set(UserDefinedFoundLIST)))>=len(UserDefinedFoundLIST)>=1:
            candidateLIST.append(k)
        #elif len([(a.start(), a.end(), a.group(0)) for a in re.finditer(ActionPat, k[2][0])]) > 2:
            #candidateLIST.append(k)
        #elif len([(e.start(), e.end(), e.group(0)) for e in re.finditer(EntityPat, k[2][0])])> 0:
            #candidateLIST.append(k)
        else:
            pass
    return candidateLIST


if __name__ == "__main__":
    app.debug = True
    app.run()