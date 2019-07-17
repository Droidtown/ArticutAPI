#!/usr/bin/env python
# -*- coding:utf-8 -*-

try:
    from ArticutAPI import Articut
except:
    import sys
    sys.path.append("../..")
    from ArticutAPI import Articut

#實體化 Articut()
atc = Articut()

#Demo 用的文字：載入政府機構名稱前。
inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
resultSTR = atc.parse(inputSTR)
print("1. 政府機構名稱直接「斷詞」處理：")
print(resultSTR["result_pos"])
print("=====================")

inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
resultSTR = atc.parse(inputSTR, userDefinedDictFILE="../../Public_UserDefinedDict/KNOWLEDGE_gov.json")
print("2. 政府機構名稱用「自定字典」處理：")
print(resultSTR["result_pos"])
print("=====================")

inputSTR = "國軍退除役官兵輔導委員會簡稱退輔會。 "
resultSTR = atc.parse(inputSTR, userDefinedDictFILE="../../Public_UserDefinedDict/KNOWLEDGE_gov.json")
print("3. 政府機構名稱用「自定字典」處理，再依字典名稱調整「標記」。")
tagName = "../../Public_UserDefinedDict/KNOWLEDGE_gov.json".split("/")[-1].split(".")[0] #取得 KNOWLEDGE_gov
print([result.replace("UserDefined", tagName) for result in resultSTR["result_pos"]])
print("=====================")
