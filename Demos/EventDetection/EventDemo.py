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
    from ArticutAPi import Articut

import json

#實體化 Articut()
atc = Articut()

#載入 Demo 用的文字
with open("./PengHu.txt", encoding="utf-8") as f:
    contentLIST = [l.replace("\n", "") for l in f.readlines()]

resultLIST = []
for c in contentLIST:
    print("Processing:{}/{} >> {}".format(contentLIST.index(c)+1, len(contentLIST), c))
    resultDICT = atc.parse(c, openDataPlaceAccessBOOL=True)

    tmpLIST = []
    timeLIST = atc.getTimeLIST(resultDICT)
    if timeLIST!=None:
        tmpLIST.append("".join([t[-1] for t in timeLIST]))
    else:
        pass
    actionLIST = atc.getVerbStemLIST(resultDICT)
    if actionLIST!=None:
        tmpLIST.append("".join([a[-1] for a in actionLIST]))
    else:
        pass
    locationLIST = atc.getLocationStemLIST(resultDICT)
    if locationLIST!=None:
        tmpLIST.append("".join([l[-1] for l in locationLIST]))
    else:
        pass

    placeLIST = atc.getOpenDataPlaceLIST(resultDICT)
    if placeLIST!=None:
        tmpLIST.append("".join([p[-1] for p in placeLIST]))
    else:
        pass

    for t in tmpLIST:
        if len(t)>=2: #在「時間」、「地點」和「活動」中，至少佔了兩個。
            resultLIST.extend(t)

with open("./LocationDetectionResultLIST.json", "w", encoding="utf-8") as f:
    json.dump(resultLIST, f, ensure_ascii=False)