#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    from ArticutAPI import Articut
except:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut

from pprint import pprint

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

    #Demo 用的文字：載入政府機構名稱前。
    inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
    resultDICT = atc.parse(inputSTR)
    print("1. 政府機構名稱直接「斷詞」處理：")
    pprint(resultDICT["result_pos"])
    print("=====================")

    inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
    resultDICT = atc.parse(inputSTR, userDefinedDictFILE="../../Public_UserDefinedDict/KNOWLEDGE_govTW.json")
    print("2. 政府機構名稱用「自定字典」處理：")
    pprint(resultDICT["result_pos"])
    print("=====================")

    inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
    resultDICT = atc.parse(inputSTR, userDefinedDictFILE="../../Public_UserDefinedDict/KNOWLEDGE_govTW.json")
    print("3. 政府機構名稱用「自定字典」處理，再依字典名稱調整「標記」。")
    tagName = "../../Public_UserDefinedDict/KNOWLEDGE_govTW.json".split("/")[-1].split(".")[0] #取得 KNOWLEDGE_gov
    pprint([result.replace("UserDefined", tagName) for result in resultDICT["result_pos"]])
    print("=====================")