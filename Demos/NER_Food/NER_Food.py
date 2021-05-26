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
    username = "" #這裡填入您在 https://api.droidtown.co 使用的帳號 email。若使用空字串，則預設使用每小時 2000 字的公用額度。
    apikey   = "" #這裡填入您在 https://api.droidtown.co 登入後取得的 api Key。若使用空字串，則預設使用每小時 2000 字的公用額度。
    articut = Articut(username, apikey)
    demoSTR = """美食商圈內高人氣四川牛肉麵專賣店選用大量的台灣洋蔥、
義大利番茄熬煮的自然酸甜牛肉湯底。加入大塊又有咬勁的牛肉塊，
特選訂製的Q彈拉麵條。日式拉麵完全吸附湯汁的精華，加入德國酸菜、牛油、辣油後更加美味
法式焗烤龍蝦和蕃茄牛肉炒飯還有法式起司火鍋以及五味章魚很夠味，章魚也不硬，搭配的小黃瓜很甜很好吃。魚蛋沙拉偶爾會點""".replace("\n", "")
    resultDICT = articut.parse(demoSTR)

    #只取出 [食物名稱]
    foodLIST = articut.NER.getFood(resultDICT, indexWithPOS=False)
    pprint(foodLIST)

    #取出 [地方風格]+[食物名稱]
    locFoodLIST = articut.NER.getFood(resultDICT, withLocation=True , indexWithPOS=False)
    pprint(locFoodLIST)