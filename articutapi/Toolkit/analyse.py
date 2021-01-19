#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import re
import unicodedata

from math import log10

class WordExtractionTFIDF(object):
    def __init__(self):
        self.thd = 0.06
        self.idfDICT, self.docCount = self._getIdfDict("idf.json")

    def __str__(self):
        return "Articut API KeywordExtraction"

    def _getIdfDict(self, fn):
        import os
        fn = "{}/data/{}".format(os.path.dirname(os.path.abspath(__file__)),fn)
        try:
            aidf = json.load(open(fn, "r", encoding=("UTF-8")))
            # idfDICT = {"":[fn id list], w:[ids, ids, ...], ...}
            return aidf, len(aidf[""])
        except Exception as e:
            print("idf dict import error.")
            print(str(e))
            return None

    def eval(self, wct, wlst, dct, idfd):
        # wlst = {w:ct, w:ct, ...}
        # idfd= {w:[ids, ids, ...], ...}
        d = {}
        for w in wlst:
            if "" == w:
                continue
            if w not in idfd:       # 未知詞彙 wct = 1
                sdt = 1
            else:
                sdt = len(idfd[w])  # 已知詞彙
            # tf, idf, tfidf 計算
            tf = wlst[w]/float(wct)
            idf = log10(float(dct)/sdt)
            tfidf = tf*idf
            # d[w] = (tf, idf, tfidf)
            d[w] = tfidf
        return d

    def getTfList(self, wLIST):
        d = {}
        wct = 0
        for k in wLIST:
            # Ignore ''
            if "" == k:
                continue
            # Ignore punctuation
            if 1 == len(k) and unicodedata.category(k).startswith("P"):
                continue
            if k not in d:
                d[k] = 1
                wct += 1
            else:
                d[k] += 1
                wct += 1
        return d, wct

    def sortByTfidf(self, evlDICT):
        # evldict = _evld = {w:(tf,idf,tfidf)}
        lst = list(evlDICT.items())
        # lst = [ (u"\u4e00", 0.02395209580838323), ... ]
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        return lst

    def extractKeyword(self, inputSTR, topK, withWeight, allowPOS):
        self.thd = topK/100.0

        # get word list
        wordLIST = inputSTR.split("/")            # wordLIST = ["沒有", "人", ...]

        # get tfDICT and get wct of the inputSTR
        tfDICT, wct = self.getTfList(wordLIST)    # tfDICT = {"沒有":1, "命運":        2, ...}

        # get tfidf dict
        evalDICT = self.eval(wct, tfDICT, self.docCount, self.idfDICT)    # evalDict = {w:tfidf, ...}

        # sort by tfidf
        rst = self.sortByTfidf(evalDICT)

        # filter by threshold
        keyWordLIST = rst[:round(self.thd*len(rst))]

        # return key word list
        if withWeight is False:
            newLIST = []
            for k in keyWordLIST:
                newLIST.append(k[0])
            return newLIST
        else:
            return keyWordLIST

class WordExtractionTextRank(object):
    def __init__(self):
        self.dWeight = 0.85
        self.initScoreINT = 1
        self.winSizeINT = 5
        self.stopWordTagsLIST = ["<QUANTIFIER>[^<]*?</QUANTIFIER>",
                                 "<MODAL>[^<]*?</MODAL>",
                                 "<AUX>[^<]*?</AUX>",
                                 "<ASPECT>[^<]*?</ASPECT>",
                                 "<FUNC_.*?>[^<]*?</FUNC_.*?>",
                                 "<CLAUSE_.*?>[^<]*?</CLAUSE_.*?>",
                                 "<RANGE_.*?>[^<]*?</RANGE_.*?>"]
        self.stopWordPat = re.compile("|".join(self.stopWordTagsLIST))
        self.stripPat = re.compile("(?<=>).*?(?=<)")

    def _getScore(self, scoreLIST, outLIST, linksLIST, refID):
        i = 0
        score = 0
        while i < len(scoreLIST):
            if i != refID:
                score += 1-self.dWeight + self.dWeight*(scoreLIST[i] * outLIST[i] / linksLIST[i])
            i += 1
        return score

    def itrRanking(self, wordRefLIST, matrixLIST, iterTimesINT):
        # wordRefLIST = ['命運', '自己', '手', '人', '決定', '你', '命運']
        # matrixLIST = [[0, 1, 1, 0, ...], [1, 0, 2, 2, ...], ... ]
        # iterTimesINT = 5
        linksLIST = []
        for outLIST in matrixLIST:
            ct = 0
            for i in outLIST:
                ct += i
            linksLIST.append(ct)

        scoreLIST = [self.initScoreINT]*len(wordRefLIST)
        t = 0
        while t < iterTimesINT:
            tmpLIST = []
            for i in range(len(matrixLIST)):
                score = self._getScore(scoreLIST, matrixLIST[i], linksLIST, i)
                tmpLIST.append(score)
            scoreLIST = tmpLIST[:]
            t += 1

        return scoreLIST

    def mappingWords(self, scoreLIST, wordRefLIST):
        # wordRefLIST = ['命運', '自己', '手', '人', '決定', '你', '命運']
        # scoreLIST = [1.1575125520833334, 2.438575, 1.9919230208333336, 1.4989894270833335, ...]
        sortLIST = []
        for i in range(len(scoreLIST)):
            sortLIST.append([wordRefLIST[i], scoreLIST[i]])
        sortLIST = sorted(sortLIST, key=lambda x: x[1])
        sortLIST.reverse()
        return sortLIST

    def rankWords(self, wordLIST, iterTimesINT):
        # wordLIST = ['命運', '自己', '手', '人', '決定', '你', '命運']
        wordRefLIST = []
        for w in wordLIST:
            if w not in wordRefLIST:
                wordRefLIST.append(w)
        # wordRefLIST = ['命運', '自己', '決定', '手', '你', '人']
        matrixLIST = [[0]*len(wordRefLIST) for item in range(len(wordRefLIST))]
        # matrixLIST = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0] ]
        # matrixLIST = [['命運', '自己', '決定', '手', '你', '人'],    for（命運）
        #               ['命運', '自己', '決定', '手', '你', '人'],    for（自己）
        #               ['命運', '自己', '決定', '手', '你', '人'],    for（決定）
        #               ['命運', '自己', '決定', '手', '你', '人'],    for（手）
        #                ...... ]

        for i in range(len(wordLIST)):
            startOffsetINT = i-self.winSizeINT
            endOffsetINT = i+self.winSizeINT+1
            if i-self.winSizeINT < 0:
                startOffsetINT = 0
            # print(wordLIST[startOffsetINT:i], wordLIST[i], wordLIST[i+1:endOffsetINT])

            for w in wordLIST[startOffsetINT:i] + wordLIST[i+1:endOffsetINT]:
                matrixLIST[wordRefLIST.index(wordLIST[i])][wordRefLIST.index(w)] += 1

        scoreLIST = self.itrRanking(wordRefLIST, matrixLIST, iterTimesINT)
        wordRankLIST = self.mappingWords(scoreLIST, wordRefLIST)
        return wordRankLIST

    def extractWords(self, resultLIST):
        resultSTR = "".join([x for x in resultLIST if len(x)>1])
        wordLIST = []
        stopwordLIST = [x.group() for x in self.stopWordPat.finditer(resultSTR)]
        for sw in stopwordLIST:
            resultSTR = resultSTR.replace(sw, "")
        wordLIST = [x.group() for x in self.stripPat.finditer(resultSTR) if len(x.group())>0]
        return wordLIST

    def extractKeyword(self, articutDICT, iterTimesINT=20, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')):
        resultLIST = articutDICT['result_pos']
        # resultLIST =
        # [ '<articut_tag>沒有人可以決定你的命運</articut_tag>',
        #   '，',
        #   '<articut_tag>命運在自己的手上</articut_tag>',
        #   '。' ]
        wordLIST = self.extractWords(resultLIST)
        # wordLIST = ['命運', '自己', '決定', '手', '你', '人']
        wordRankLIST = self.rankWords(wordLIST, iterTimesINT)
        # wordRankLIST = [['命運', 5.591625666787958],
        #                 ['自己', 3.4637188376903927],
        #                 ['你', 3.4637188376903927],
        #                 ['決定', 3.4637188376903927],
        #                 ['手', 2.959546855830475],
        #                 ['人', 2.9595468558304745]]
        if withWeight is False:
            tmpLIST = []
            for w in wordRankLIST:
                tmpLIST.append(w[0])
            return tmpLIST
        else:
            return wordRankLIST

class AnalyseManager(object):
    def __init__(self):
        self.tfidfOBJ = WordExtractionTFIDF()
        self.txtrankOBJ = WordExtractionTextRank()
        self.POSDICT = {'n':'', 'v':'', 'a':'', 'p':''}

    def convertPOS(self, POSTOUPLE):
        return POSTOUPLE

    def TFIDF(self, idf_path=None):
        if idf_path != None:
            self.tfidfOBJ._getIdfDict(idf_path)

    def extractTags(self, parseResultDICT, topK=50, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')):
        if "result_segmentation" in parseResultDICT:
            pass
        else:
            return None
        try:
            allowPOS = self.convertPOS(allowPOS)
            result = self.tfidfOBJ.extractKeyword(parseResultDICT["result_segmentation"], topK, withWeight, allowPOS)
            return result
        except Exception as e:
            print(str(e))
            return None

    def extract_tags(self, parseResultDICT):
        # Alias of extractTags()
        return self.extractTags(parseResultDICT)

    def textrank(self, parseResultDICT, topK=10, withWeight=False, allowPOS=('ns', 'n', 'vn', 'v')):
        # Key word extraction and rank by the TextRank algorithm
        # Alias of jieba textrank()
        # topK = iterative times
        if "result_segmentation" in parseResultDICT and "result_pos" in parseResultDICT:
            pass
        else:
            return None
        try:
            allowPOS = self.convertPOS(allowPOS)
            return self.txtrankOBJ.extractKeyword(parseResultDICT, topK, withWeight, allowPOS)
        except Exception as e:
            print(str(e))
            return None
