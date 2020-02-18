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
from pprint import pprint

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



if __name__ == "__main__":

    try:
        #使用自己的斷詞額度。
        with open("../../account.info", "r") as f:
            userDICT = json.loads(f.read())
        username = userDICT["email"]
        apikey = userDICT["apikey"]
        atclv2 = Articut(username=userDICT["email"], apikey=userDICT["apikey"])
        atclv3 = Articut(username=userDICT["email"], apikey=userDICT["apikey"], level="lv3")
    except:
        #使用免費的斷詞額度。
        #實體化 Articut()
        atclv2 = Articut()
        atclv3 = Articut(level="lv3")

    #載入 Demo 用的文字
    contentLIST = []
    with open("./PengHu.txt", encoding="utf-8") as f:
        contentLIST = [l.replace("\n", "") for l in f.readlines()]

    #呼叫 parse(), 並把 "openDataPlaceAccessBOOL" 參數值設為 True 以便擷取最多的地點/地名資訊。
    resultLIST = []
    for c in contentLIST:
        print("Processing:{}/{} >> {}".format(contentLIST.index(c)+1, len(contentLIST), c))
        resultDICT = atclv2.parse(c, openDataPlaceAccessBOOL=True)

        eventDICT = {"time":[],
                     "site":[],
                     "event":[]}

        #將結果傳給 getTimeLIST() 取出時間
        timeLIST = atclv2.getTimeLIST(resultDICT)
        if timeLIST!=None:
            for tm in timeLIST:
                eventDICT["time"].append([t[-1] for t in tm])
        else:
            pass

        #將結果傳給 getLocationStemLIST() 取出地名
        siteLIST = []
        locationLIST = atclv2.getLocationStemLIST(resultDICT)
        if locationLIST!=None:
            siteLIST.extend(locationLIST)
            for location in locationLIST:
                eventDICT["site"].append([l[-1] for l in location])
        else:
            pass

        #將結果傳給 getAddTWLIST() 取出台灣地址
        addressLIST = atclv2.getAddTWLIST(resultDICT)
        if addressLIST !=None:
            siteLIST.extend(addressLIST)
            for address in range(0, len(addressLIST)):
                if addressLIST[address] == []:
                    pass
                else:
                    eventDICT["site"][address].extend([a[-1] for a in addressLIST[address]])

        #將結果傳給 getOpenDataPlaceLIST() 取出開放資料平台中的景點
        placeLIST = atclv2.getOpenDataPlaceLIST(resultDICT)
        if placeLIST!=None:
            siteLIST.extend(placeLIST)
            for place in range(0, len(placeLIST)):
                eventDICT["site"][place].extend([p[-1] for p in placeLIST[place]])
        else:
            pass

        eventLIST = ["->".join(e) for e in atclv3.parse(c)["event"]]
        if eventLIST!=None:
            if len(siteLIST)>0:
                for event in range(0, len(eventLIST)):
                    #eventDICT["event"].append([])
                    eventDICT["event"].extend([e[-1] for e in eventLIST[event]])
            else:
                pass
        else:
            pass
        if eventDICT["site"]!=[] and eventDICT["event"]!=[]:
            resultLIST.append(eventDICT)

    #在畫面上顯示結果，並將結果存入 LocationEventDetectionResultLIST.json 檔中。
    print("DetectionResult:\n")
    pprint(resultLIST)

    with open("./LocationEventDetectionResultLIST.json", "w", encoding="utf-8") as f:
        json.dump(resultLIST, f, ensure_ascii=False)