#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

class TaiwanAddressAnalizer:
    def __init__(self, locale=None):
        if locale in ("TW", "CN"):
            pass
        else:
            locale="TW"
        self.addTWPat = re.compile("(?<=<KNOWLEDGE_addTW>)[^<]*?(?=</KNOWLEDGE_addTW>)")
        self.TWaddPatDICT = {"countyPat"      : ".[^市區]縣",
                             "cityPat"        : "[^是在於及、，]{1,2}市",
                             "districtPat"    : "那瑪夏區|[^市及、，]?.社?區",
                             "townshipPat"    : "(阿里山|三地門|太麻里)鄉|..[鄉里]",
                             "townPat"        : "..鎮",
                             "villagePat"     : "..村",
                             "neighborhoodPat": "(\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?鄰)",
                             "roadPat"        : "(?<=[縣市區鄉鎮里村])[^市區鄉鎮村路及、，]{1,4}([路街]|大道)",
                             "sectionPat"     : "\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?段",
                             "alleyPat"       : "(國中|([^縣市區鄉鎮里村路段]{1,2}|鐵路)[\d零一二三四五六七八九十百千１２３４５６７８９０]*?|\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?)\s?巷([\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?弄)?",
                             "numberPat"      : "(\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?[之\-]\s?)?\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?號([之\-]\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]+?)?",
                             "floorPat"       : "\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?\s?[fF樓]\s?([之\-]\s?[\d零一二三四五六七八九十百千１２３４５６７８９０]*?)?",
                             "roomPat"        : "\s?[a-zA-Z]*?\d*?([a-zA-Z]*?)?(\d*?)?\s?室",
                             "0-3":"{0,2}",
                             "1-3":"{1,3}",
                             "1-4":"{1,4}",
                             }
        self.stripPat = re.compile("(?<=>).*?(?=<)")

    def _addIndexConverter(self, ArticutResultDICT, addIndexLIST):
        '''
        Convert posIndex to segIndex
        Return list
        '''
        if type(addIndexLIST) is list:
            pass
        else:
            return None
        segIndexLIST = []
        try:
            tagLen = len("<KNOWLEDGE_addTW>")
            for i, posLIST in enumerate(addIndexLIST):
                if posLIST:
                    tmpLIST = []
                    for start, end, seg in posLIST:
                        posEndSTR = ArticutResultDICT["result_pos"][i][:start]
                        endSTR = posEndSTR[posEndSTR.rfind("<KNOWLEDGE_addTW>")+tagLen:]
                        segEndSTR = "".join([x.group() for x in self.stripPat.finditer(posEndSTR)])
                        tmpLIST.append((len(segEndSTR+endSTR), len(segEndSTR+endSTR)+len(seg), seg))
                    segIndexLIST.append(tmpLIST)
                else:
                    segIndexLIST.append(posLIST)
        except Exception as e:
            print("Invalid posIndexLIST format")
            return None
        return segIndexLIST

    def _getAddLIST(self, ArticutResultDICT, addPatSTR):
        if "result_pos" in ArticutResultDICT:
            pass
        else:
            return None
        resultLIST = []
        addPat = re.compile(addPatSTR)
        for r in ArticutResultDICT["result_pos"]:
            if "<KNOWLEDGE_addTW>" in r:
                tmpLIST = [(c.start(), c.end(), c.group(0)) for c in list(self.addTWPat.finditer(r))]
                resultLIST.append([])
                for start, end, tmp in tmpLIST:
                    resultLIST[-1].extend([(c.start()+start, c.end()+start, c.group(0)) for c in list(addPat.finditer(tmp))])
            else:
                resultLIST.append([])
                continue
        return resultLIST

    def getAddressCounty(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["countyPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressCity(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["cityPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressDistrict(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["districtPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTownship(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["townshipPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTown(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["townPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressVillage(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["villagePat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNeighborhood(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["neighborhoodPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoad(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["roadPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressSection(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["sectionPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressAlley(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["alleyPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNumber(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["numberPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressFloor(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["floorPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoom(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["roomPat"])
        if not indexWithPOS and resultLIST:
            resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST
