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

#實體化 Articut()
atc = Articut()

#載入 Demo 用的文字
with open("./PengHu.txt", encoding="utf-8") as f:
    contentLIST = [l.replace("\n", "") for l in f.readlines()]
#contentLIST=["這張地圖是不死兔這次到澎湖玩耍所記錄的景點與美食喔!"]

resultLIST = []

for c in contentLIST:
    print("Processing:{}/{} >> {}".format(contentLIST.index(c)+1, len(contentLIST), c))
    resultDICT = atc.parse(c, openDataPlaceAccessBOOL=True)

    eventDICT = {"time":[],
                 "site":[],
                 "event":[]
    }

    tmpLIST = []
    timeLIST = atc.getTimeLIST(resultDICT)
    timeLIST.sort()
    if timeLIST!=None:
        for tm in timeLIST:
            eventDICT["time"].append("".join([t[-1] for t in tm]))
    else:
        pass

    siteLIST = []
    locationLIST = atc.getLocationStemLIST(resultDICT)
    locationLIST.sort()
    if locationLIST!=None:
        siteLIST.extend(locationLIST)
        for location in locationLIST:
            eventDICT["site"].append("".join([l[-1] for l in location]))
    else:
        pass

    placeLIST = atc.getOpenDataPlaceLIST(resultDICT)
    placeLIST.sort()
    if placeLIST!=None:
        siteLIST.extend(placeLIST)
        for place in placeLIST:
            eventDICT["site"].append("".join([p[-1] for p in place]))
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

with open("./EventDetectionResultLIST.json", "w", encoding="utf-8") as f:
    json.dump(resultLIST, f, ensure_ascii=False)