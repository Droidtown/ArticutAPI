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
        self.TWaddPatDICT = {"countyPat"      : "[^\s][^市]縣",
                             "cityPat"        : "[^是在於及、，\s]{1,2}市",
                             "districtPat"    : "那瑪夏區|[^市及、，\s]+?.社?區|[東西南北中]區",
                             "townshipPat"    : "(阿里山|三地門|太麻里)鄉|..鄉|[^縣].里(?!區)",
                             "townPat"        : "[^\s][^\s]鎮",
                             "villagePat"     : "[^\s][^\s]新?村(?!路)",
                             "neighborhoodPat": "(\s?[零一二三四五六七八九十廿卅０-９\d]+?\s?鄰)",
                             "roadPat"        : "市府路|市[政場]([北南中]|[1-7一二三四五六七]){0,2}路|市港[^\s]路|美村路|[新環村盛果]市[^\s]?[路街]|市民大道|市宅街|[埔菜美元西]市[路街]|(?<=[縣市區鄉鎮里村鄰])[^市區鄉鎮村路及鄰、，]{1,4}([路街](?!里)|大道)",
                             "sectionPat"     : "\s?[零一二三四五六七八九十廿卅百０-９\d]*?\s?段",
                             "alleyPat"       : "(國中|市場|新市.|([^縣市區鄉鎮里村路街段]{1,2}|鐵路)[零一二三四五六七八九十廿卅百０-９\d]*?|\s?[零一二三四五六七八九十廿卅百０-９\d]*?)\s?巷([零一二三四五六七八九十廿卅百０-９\d]*?\s?弄)?",
                             "numberPat"      : "(\s?[零一二三四五六七八九十廿卅百０-９\d]*?\s?[之\-]\s?)?\s?[零一二三四五六七八九十廿卅百０-９\d]*?\s?號([之\-]\s?[零一二三四五六七八九十廿卅百０-９\d]+?)?",
                             "floorPat"       : "\s?[零一二三四五六七八九十廿卅百０-９\d]*?\s?[fF樓]",
                             "roomPat"        : "\s?([a-zA-Z零一二三四五六七八九十廿卅百\d０-９]+?)\s?(室?$)"}
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
                    resultLIST[-1].extend([[c.start()+start, c.end()+start, c.group(0)] for c in list(addPat.finditer(tmp))])
            else:
                resultLIST.append([])
                continue
        return resultLIST

    def mergeBulkResult(self, inputLIST):
        resultLIST = []
        resultExtend = resultLIST.extend
        for x in filter(None, inputLIST):
            try:
                if x["status"]:    # 只取成功的結果
                    resultExtend(x["result_list"])
            except:
                pass
        return resultLIST

    def getAddressCounty(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["countyPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["countyPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressCity(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["cityPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["cityPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressDistrict(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["districtPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["districtPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTownship(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["townshipPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["townshipPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressTown(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["townPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["townPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressVillage(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["villagePat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["villagePat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNeighborhood(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["neighborhoodPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["neighborhoodPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoad(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["roadPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["roadPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressSection(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["sectionPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["sectionPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressAlley(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["alleyPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["alleyPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressNumber(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["numberPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["numberPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressFloor(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["floorPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["floorPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST

    def getAddressRoom(self, ArticutResultDICT, indexWithPOS=True):
        resultLIST = []
        resultAppend = resultLIST.append
        if type(ArticutResultDICT) is list:
            ArticutResultLIST = self.mergeBulkResult(ArticutResultDICT)
            for i, x in enumerate(ArticutResultLIST):
                resultAppend(self._getAddLIST(x, self.TWaddPatDICT["roomPat"]))
                if not indexWithPOS and resultLIST:
                    resultLIST[i] = self._addIndexConverter(x, resultLIST)
        else:
            resultLIST = self._getAddLIST(ArticutResultDICT, self.TWaddPatDICT["roomPat"])
            if not indexWithPOS and resultLIST:
                resultLIST = self._addIndexConverter(ArticutResultDICT, resultLIST)
        return resultLIST
