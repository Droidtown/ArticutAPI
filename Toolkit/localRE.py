#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re

class TaiwanAddressAnalizer:
    def __init__(self, locale=None):
        if locale in ("TW", "CN"):
            pass
        else:
            locale="TW"

        self.TWaddPatDICT = {"countyPat"      : ".[^市區]縣",
                             "cityPat"        : "[^是在於及、，]{1,2}市",
                             "districtPat"    : "那瑪夏區|[^市及、，]?.社?區",
                             "townshipPat"    : "(阿里山|三地門|太麻里)鄉|..[鄉里]",
                             "townPat"        : "..鎮",
                             "villagePat"     : "..村",
                             "neighborhoodPat": "(\s?[\d零一二三四五六七八九１２３４５６７８９０]*?\s?鄰)",
                             "roadPat"        : "(?<=[縣市區鄉鎮里村])[^市區鄉鎮村及、，]{1,4}([路街]|大道)",
                             "sectionPat"     : "\s?[\d零一二三四五六七八九１２３４５６７８９０]*?\s?段",
                             "alleyPat"       : "(國中|\s?[\d零一二三四五六七八九１２３４５６７８９０]*?)\s?巷([\d零一二三四五六七八九１２３４５６７８９０]*?\s?弄)?",
                             "numberPat"      : "(\s?[\d零一二三四五六七八九１２３４５６７８９０]*?\s?[之\-]\s?)?\s?[\d零一二三四五六七八九１２３４５６７８９０]*?\s?號([之\-]\s?[\d零一二三四五六七八九１２３４５６７８９０]+?)?",
                             "floorPat"       : "\s?[\d零一二三四五六七八九１２３４５６７８９０]*?\s?[fF樓]\s?([之\-]\s?[\d零一二三四五六七八九１２３４５６７８９０]*?)?",
                             "roomPat"        : "\s?[a-zA-Z]*?\d*?([a-zA-Z]*?)?(\d*?)?\s?室",
                             "0-3":"{0,2}",
                             "1-3":"{1,3}",
                             "1-4":"{1,4}",
                             }
        self.stripPat = re.compile("(?<=>).*?(?=<)")

    def _segIndexConverter(self, parseResultDICT, posIndexLIST):
        '''
        Convert posIndex to segIndex
        Return list
        '''
        if type(posIndexLIST) is list and "result_pos" in parseResultDICT:
            pass
        else:
            return None

        segIndexLIST = []
        try:
            for i, posLIST in enumerate(posIndexLIST):
                if posLIST:
                    tmpLIST = []
                    for start, end, seg in posLIST:
                        posEndSTR = parseResultDICT["result_pos"][i][:start]
                        segEndSTR = "".join([x.group() for x in self.stripPat.finditer(posEndSTR)])
                        tmpLIST.append((len(segEndSTR), len(segEndSTR)+len(seg), seg))
                    segIndexLIST.append(tmpLIST)
                else:
                    segIndexLIST.append(posLIST)
        except Exception as e:
            print("Invalid posIndexLIST format")
            return None
        return segIndexLIST


    def getAddressCounty(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["countyPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressCity(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["cityPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressDistrict(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["districtPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTownship(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["townshipPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTown(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["townPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressVillage(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["villagePat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNeighborhood(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["neighborhoodPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoad(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["roadPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressSection(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["sectionPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressAlley(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["alleyPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNumber(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["numberPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressFloor(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["floorPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoom(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        addPat = re.compile(self.TWaddPatDICT["roomPat"])
        for r in ArticutResultDICT["result_pos"]:
            resultLIST.append([(c.start(), c.end(), c.group(0)) for c in list(addPat.finditer(r))])

        if not indexWithPOS:
            resultLIST = self._segIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST