#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut

text = "研究這個研究的研究已經被研究許多年了"


articut = Articut(username="", apikey="")
result = articut.parse(text)

#Articut 的 POS 標記斷詞結果在 "result_pos" 中。
print(result["result_pos"])



print("有幾個動詞的「研究」呢？")
verbLIST = articut.getVerbStemLIST(result, indexWithPOS=False)

verbCounter = 0
for sentence in verbLIST: #verbLIST 中，每「一個」句子是一個獨立的 list，故要先進入 sentence，再計算其中的 "研究"
    for v in sentence:
        if v[-1] == "研究":
            print("發現動詞「研究」 ，位於原句的 {}~{} 位置".format(v[0], v[1]))
            verbCounter = verbCounter + 1

print("共有 {} 個『研究』是動詞。".format(verbCounter))



print("有幾個名詞的「研究」呢？")
nounLIST = articut.getNounStemLIST(result, indexWithPOS=False)

nounCounter = 0
for sentence in nounLIST: #nounLIST 中，每「一個」句子是一個獨立的 list，故要先進入 sentence，再計算其中的 "研究"
    for n in sentence:
        if n[-1] == "研究":
            print("發現名詞「研究」 ，位於原句的 {}~{} 位置".format(n[0], n[1]))
            nounCounter = nounCounter + 1

print("共有 {} 個『研究』是名詞。".format(verbCounter))