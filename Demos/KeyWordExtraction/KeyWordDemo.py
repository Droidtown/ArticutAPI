#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# FileName: KeyWordDemo.py
# Developer: Trueming (trueming@gmail.com)


#Sample Text "InputString.txt"

try:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut
except:
    from ArticutAPI import Articut


# 載入 Demo 用的文字
text = open("./InputString.txt", "r").read()
sentLIST = text.split("\n")

# 實體化 Articut
atc = Articut()

print("ArticutAPI Term Extraction Demo")
for sentence in sentLIST:
    if "" == sentence.strip():
        continue

    result = atc.parse(sentence)
    if result["status"]:
        print("{}\nInput: {}".format('#'*20 , sentence))

        # TextRank 抽取句子關鍵詞並排序
        wordLIST = atc.analyse.textrank(result)
        print("TextRank:", wordLIST)
        # TFIDF 抽取句子關鍵詞
        wordLIST = atc.analyse.extract_tags(result)
        print("TFIDF:", wordLIST)
