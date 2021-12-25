#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut
import re

articut = Articut()

def commaPreprocessor(inputSTR, refLIST):
    if "、" in inputSTR:
        pass
    else:
        return inputSTR

    ignoreVerbLIST = []
    for r in refLIST:
        rDICT = articut.parse(r)
        verbLIST = articut.getVerbStemLIST(rDICT)
        for v in verbLIST:
            if v == []: #標點符號，或是沒有動詞的句子
                pass
            else:       #有動詞的句子，動詞列表成 [(startIndex, endIndex, word)] 格式
                for i in v:
                    ignoreVerbLIST.append(i[2])

    resultDICT = articut.parse(inputSTR)
    #取出第一個「頓號」前一句 index。通常主要動詞在其中。
    refIndexLIST = []
    for i in range(1, len(resultDICT["result_pos"])):  #從 1 開始算，以免 inputSTR 是「、」開頭的字串片段。
        if resultDICT["result_pos"][i] == "、":
            refIndexLIST.append(i-1)
            break
    #依前述的 refIndex 取出主要動詞
    for refIndex in refIndexLIST:
        verb2DistSTR = ""
        verbPat = re.compile("(?<=<ACTION_verb>)[^<]{2,3}(?=</ACTION_verb>)") #取二字詞或三字詞，避免誤抓了「看、聽、說、講、想」…等一字詞的動詞。
        try: #有可能前一句就是沒有合適的動詞，那麼就不適用這個前處理方法。
            verb2DistSTR = [v for v in verbPat.findall(resultDICT["result_pos"][refIndex]) if v not in ignoreVerbLIST][0]
        except:
            break

    for i in range(1, len(resultDICT["result_pos"])): #把抓出的動詞補回去。但如果遇到斷句的「，。！？」時，就停止補動詞。
        if resultDICT["result_pos"][i] == "、":
            resultDICT["result_pos"][i] = resultDICT["result_pos"][i] + verb2DistSTR
        elif resultDICT["result_pos"][i] in "，。！？":
            break

    resultSTR = re.sub("</?[A-Z]+?(_[a-zA-Z]+)?>", "", "".join(resultDICT["result_pos"]))

    return resultSTR


if __name__ == "__main__":
    refLIST = ["網頁設計"]

    inputSTR = "應徵UX 網頁設計、網頁設計師、網站維護等職缺，熟悉HTML5、CSS3、Photoshop、Illustractor、JavaScript、JQuery。"
    #先用 re.split 把字串分切成「句子」。這裡不處理「、」的原因是 commaPreprocessor() 就是用來處理「、」的，所以我們把它留著。
    inputLIST = re.split("[，。！？]", inputSTR)

    #把前一步切開的字串，送入 commaPreprocessor() 裡處理。
    for i in inputLIST:
        resultSTR = commaPreprocessor(i, refLIST)
        print(resultSTR)