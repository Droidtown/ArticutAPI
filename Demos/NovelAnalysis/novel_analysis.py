#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re

try:
    # Installed via pip install
    try:
        from .ArticutAPI import Articut
    except:
        from ArticutAPI import Articut
except:
    # Installed via git clone
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut


#username 和 apikey 留空的話，就只有每小時 2000 字的公用額度可以玩囉。
username = ""
apikey = ""
articut = Articut(username=username, apikey=apikey)

userDefinedDictFILE = "./KNOWLEDGE_三國人物.json"
if os.path.exists(userDefinedDictFILE):
    pass
else:
    raise IOError("請到 https://github.com/Droidtown/ArticutAPI/blob/master/Public_UserDefinedDict/ 下載 KNOWLEDGE_三國人物.json 字典檔配合使用。")

#取出所有依字典被標為人名的字串
UserDefinedPat = re.compile("<UserDefined>[^<]*?</UserDefined>")
#取出所有只有「一個字符」，可能是人名的字串
possibleAliasPosTUPL = ("ENTITY_nounHead", "ENTITY_nouny", "ENTITY_noun", "ENTITY_oov", "ACTION_verb", "MODIFIER")

def main(inputSTR):
    articutResultDICT = articut.parse(inputSTR, userDefinedDictFILE="./KNOWLEDGE_三國人物.json")
    print(articutResultDICT)
    resultDICT = {}
    #取出這段文字裡所有被列在「三國人物.json」裡的人名，並加到 resultDICT 裡做為 key
    possibleAliasDICT = {}
    for posSentenceDICT in articutResultDICT["result_obj"]:
        if posSentenceDICT[0]["pos"] == "PUNCTUATION":
            pass
        else:
            for ud in posSentenceDICT:
                if ud["pos"] == "UserDefined":
                    resultDICT[ud["text"]] = []
                    possibleAliasDICT[ud["text"][-1]] = ud["text"]
                if ud["pos"] in possibleAliasPosTUPL and len(ud["text"]) == 1 and ud["text"] in possibleAliasDICT.keys():
                    ud["pos"] = "UserDefined"
                    ud["text"] = possibleAliasDICT[ud["text"]] #這行示範把「雲」取代成「趙雲」

                #若要把「夫人」或是「妾」取代成「糜夫人」，可仿照前述的方式，在這裡處理。

    #真正開始抽取資訊的段落
    for i in range(len(articutResultDICT["result_obj"])):
        if articutResultDICT["result_obj"][i][0]["pos"] == "PUNCTUATION":
            pass
        else:
            for ud in articutResultDICT["result_obj"][i]:
                if ud["pos"] == "UserDefined":
                    focusPerson = ud["text"]
                if ud["pos"] in ("ACTION_verb", "ACTION_quantifiedVerb", "VerbP"):
                    if focusPerson != None:
                        resultDICT[focusPerson].append(ud["text"])
                    else:
                        pass
                elif "ENTITY" in ud["pos"]:
                    focusPerson = None
                else:
                    pass


    return resultDICT  #回傳結果範例 {"趙雲": ["伏地", "拍馬"], "糜夫人": ["投井"]}


if __name__== "__main__":

    inputSTR = """趙雲聽了，連忙追尋。只見一個人家，被火燒壞土牆，糜夫人抱著阿斗，坐於牆下枯井之傍啼哭。
    雲急下馬伏地而拜。夫人曰：「妾得見將軍，阿斗有命矣。望將軍可憐他父親飄蕩半世，只有這點骨血。
    將軍可護持此子，教他得見父面，妾死無恨！」"""

    resultDICT = main(inputSTR)
    print(resultDICT)


