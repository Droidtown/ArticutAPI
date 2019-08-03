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


if __name__ == "__main__":

    try:
        #使用自己的斷詞額度。
        with open("../../account.info", "r") as f:
            userDICT = json.loads(f.read())
        username = userDICT["email"]
        apikey = userDICT["apikey"]
        atc = Articut(username=userDICT["email"], apikey=userDICT["apikey"])
    except:
        #使用免費的斷詞額度。
        #實體化 Articut()
        atc = Articut()

    # 載入 Demo 用的文字
    text = open("./InputString.txt", "r").read()
    sentLIST = text.split("\n")

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
            print("TF-IDF:", wordLIST)
