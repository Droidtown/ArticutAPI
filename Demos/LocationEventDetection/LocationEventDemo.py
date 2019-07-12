#!/usr/bin/env python
# -*- coding:utf-8 -*-
# FileName: LocationDemo.py
# Developer: Peter. w (peterwolf.wang@gmail.com)


#Sample Text "PengHu.txt" Source:
#https://bosstwo420.pixnet.net/blog/post/220559147-%E3%80%8E%E6%BE%8E%E6%B9%96%E8%87%AA%E7%94%B1%E8%A1%8C%E3%80%8F%E6%BE%8E%E6%B9%96%E6%99%AF%E9%BB%9E%E6%8E%A8%E8%96%A6%EF%BD%9E%E5%BF%85%E5%90%83%E7%BE%8E%E9%A3%9F%EF%BD%9E%E5%A4%A7

try:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut
except:
    from ArticutAPI import Articut

import json


############################ 定義及說明 ############################
# LocationEvent 定義為「某時 - 某地 - 發生某事」。
# 其中「某時」為可有可無。
# 本 Demo 利用 ArticutAPI 的斷詞結果，搭配
# getTimeLIST() 取出「某時」
# getLocationStemLIST() 和 getOpenDataPlaceLIST() 取出「某地」
# getEventLIST() 取出「發生某事」
# 再將以上三者結合成符合 LocationEvent 定義之「某時 - 某地 - 發生某事」
# 的結果，並另存之。
###################################################################


#實體化 Articut()
atc = Articut()

#載入 Demo 用的文字
contentLIST = []
with open("./PengHu.txt", encoding="utf-8") as f:
    contentLIST = [l.replace("\n", "") for l in f.readlines()]

resultLIST = []

for c in contentLIST:
    print("Processing:{}/{} >> {}".format(contentLIST.index(c)+1, len(contentLIST), c))
    resultDICT = atc.parse(c, openDataPlaceAccessBOOL=True)

    eventDICT = {"time":[],
                 "site":[],
                 "event":[]}

    tmpLIST = []
    timeLIST = atc.getTimeLIST(resultDICT)
    if timeLIST!=None:
        for tm in timeLIST:
            eventDICT["time"].append([t[-1] for t in tm])
    else:
        pass
    siteLIST = []
    locationLIST = atc.getLocationStemLIST(resultDICT)
    if locationLIST!=None:
        siteLIST.extend(locationLIST)
        for location in locationLIST:
            eventDICT["site"].append([l[-1] for l in location])
    else:
        pass
    placeLIST = atc.getOpenDataPlaceLIST(resultDICT)
    if placeLIST!=None:
        siteLIST.extend(placeLIST)
        for place in placeLIST:
            eventDICT["site"].append([p[-1] for p in place])
    else:
        pass
    eventLIST = atc.getEventLIST(resultDICT)
    eventLIST.sort()
    if eventLIST!=None:
        if len(siteLIST)>0:
            anchorIndex = min([l[0][0] for l in siteLIST])
            for event in eventLIST:
                if event[1]<anchorIndex:
                    pass
                else:
                    eventDICT["event"].append("".join(event[-1]))
    else:
        pass
    if eventDICT["site"]!=[] and eventDICT["event"]!=[]:
        resultLIST.append(eventDICT)

print("DetectionResult:\n", resultLIST)

with open("./LocationEventDetectionResultLIST.json", "w", encoding="utf-8") as f:
    json.dump(resultLIST, f, ensure_ascii=False)