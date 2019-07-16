#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI.ArticutAPI import Articut
import json

denormalizedFILE = "facts_as_lines.txt"
userDefinedDICT = "UserDefinedDictFile.json"
try:
    with open("./account.info") as f:
        accountInfoDICT = json.loads(f.read())
    articut = Articut(username=accountInfoDICT["email"], apikey=accountInfoDICT["apikey"])
except:
    articut = Articut()


with open(denormalizedFILE, encoding="utf-8") as f:
    inputLIST = [d.replace("\n", "") for d in f.readlines()]

print(inputLIST)

resultLIST = []
for i in inputLIST:
    result = articut.parse(i, level="lv1", userDefinedDictFILE=userDefinedDICT)
    resultLIST.append([i, result["result_segmentation"], result["result_pos"]])

with open("domain_knowledge.json", "w", encoding="utf-8") as f:
    json.dump(resultLIST, f, ensure_ascii=False)
