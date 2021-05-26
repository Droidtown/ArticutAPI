#!/usr/bin/env python3
# -*- coding:utf-8 -*-


try:
    #Installed via pip install
    try:
        from .ArticutAPI import Articut
    except:
        from ArticutAPI import Articut
except:
    #Installed via git clone
    import sys
    sys.path.append("../..")

from pprint import pprint
from ArticutAPI import Articut

if __name__ == "__main__":
    articut = Articut()
    demoSTR = """美食商圈內高人氣四川牛肉麵專賣店選用大量的台灣洋蔥、
義大利番茄熬煮的自然酸甜牛肉湯底。加入大塊又有咬勁的牛肉塊，
特選訂製的Q彈拉麵條。日式拉麵完全吸附湯汁的精華，加入德國酸菜、牛油、辣油後更加美味""".replace("\n", "")
    resultDICT = articut.parse(demoSTR)

    #只取出 [食物名稱]
    foodLIST = articut.NER.getFood(resultDICT, indexWithPOS=False)
    pprint(foodLIST)

    #取出 [地方風格]+[食物名稱]
    locFoodLIST = articut.NER.getFood(resultDICT, withLocation=True , indexWithPOS=False)
    pprint(locFoodLIST)