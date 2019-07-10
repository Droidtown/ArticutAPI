import json
import unicodedata

from math import log10

class KeywordExtraction(object):
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

    def extractKeyword(self, inputSTR):
        # get word list
        # get tfDICT
        # get wct of the inputSTR
        wLIST = inputSTR.split("/")            # wLIST = ["沒有", "人", ...]
        tfDICT, wct = self.getTfList(wLIST)    # tfDICT = {"沒有":1, "命運":2, ...}

        # get tfidf dict
        evalDICT = self.eval(wct, tfDICT, self.docCount, self.idfDICT)    # evalDict = {w:tfidf, ...}

        # sort by tfidf
        rst = self.sortByTfidf(evalDICT)

        # filter by threshold
        kwLIST = []
        for k in rst:
            if k[1] < self.thd:
                break
            kwLIST.append(k[0])

        # return key word list
        return kwLIST

    def extractTags(self, parseResultDICT):
        if "result_segmentation" in parseResultDICT:
            pass
        else:
            return None
        try:
            result = self.extractKeyword(parseResultDICT["result_segmentation"])
            return result
        except Exception as e:
            print(str(e))
            return None

    def extract_tags(self, parseResultDICT):
        # Alias of extractTags()
        return self.extractTags(parseResultDICT)