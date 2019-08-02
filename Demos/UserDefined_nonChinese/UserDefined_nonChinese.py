#!/usr/bin/env python
# -*- coding:utf-8 -*-


try:
    from ArticutAPI import Articut
except:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut

import json
import re

def translateWithDictionary(Articut_resultDICT, dictionaryFILE):
    '''
    依 dictionaryFILE 翻譯 Articut 回傳的 resultDICT
    '''
    #載入自定詞典
    try:
        with open(dictionaryFILE) as f:
            myEnglishDictionary = json.loads(f.read())
    except Exception as e:
        print("User Defined File Loading Error.")
        print(str(e))
        return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}
    stripPat = re.compile("(?<=>).*?(?=<)")
    Articut_resultDICT["translated_pos"] = []
    Articut_resultDICT["translated_seg"] = ""
    translatePat = re.compile("(?<=<UserDefined>).*?(?=</UserDefined>)")
    for p in resultDICT["result_pos"]:
        translateLIST = [(t.start(), t.end(), t.group(0)) for t in reversed(list(translatePat.finditer(p)))]
        if translateLIST == []:
            Articut_resultDICT["translated_pos"].append(p)
        else:
            for t in translateLIST:
                for k in myEnglishDictionary:
                    if t[2] in myEnglishDictionary[k]:
                        #目前是找到就停。如有其它的比對策略，例如最長優先…等，可在此區塊調整。
                        targetSTR = k
                        break
                    else:
                        targetSTR = t[2]

                p = "{}{}{}".format(p[:t[0]], targetSTR, p[t[1]:])
            Articut_resultDICT["translated_pos"].append(p)
    Articut_resultDICT["translated_seg"] = "".join([x.group() for x in stripPat.finditer("".join(Articut_resultDICT["translated_pos"]))])
    return Articut_resultDICT






if __name__ == "__main__":

    try:
        #使用自己的斷詞額度。
        with open("../../account.info", "r") as f:
            userDICT = json.loads(f.read())
        username = userDICT["email"]
        apikey = userDICT["apikey"]
        atc = Articut(username=userDICT["email"], apikey=userDICT["apikey"])
    except:
        #使用免費的斷詞額度。
        #實體化 Articut()
        atc = Articut()

    inputSTR = '''You know，我們company是一個比較global的corporation，所以進來的candidate都要有一定的English的communication的ability，才qualified可以這樣mix的speak的。如果你老是speak這個Chinese的話，就給人local的image，you know，這個first impression就low掉了，可以understand嗎'''

    resultDICT = atc.parse(inputSTR, userDefinedDictFILE="./myEnglishDICT.json")

    translateResult = translateWithDictionary(resultDICT, dictionaryFILE="./myEnglishDICT.json")


    print("轉譯前：\n{}\n".format(inputSTR))
    print("-字典中沒有 company 這個字！-\n")
    print("轉譯後：\n{}\n".format(translateResult["translated_seg"]))
