#!/usr/bin/env python3
# -*- coding:utf-8 -*-

__author__ = ["jacksugood@gmail.com", "60621032L@gapps.ntnu.edu.tw"]

import os
pythonLIST = [p for p in os.popen("where python").read().split("\n") if p !=""]
    
print("請選擇要安裝 request 模組的版本")
for i in range(0, len(pythonLIST)):
    print("{}). {}".format(i+1, pythonLIST[i]))
    
pythonSelection = int(input("您選擇(輸入數字)："))
if pythonSelection in range(1, len(pythonLIST)+1):
    try:
        os.system("{} -m pip install requests".format(pythonLIST[pythonSelection-1])) 
        #以後如果要裝別的就直接在這一行改就可以了喔 把requests換成你的packages的名字
        print("裝…好啦！")
    except:
        print("呃…好像出了什麼錯，總之是沒裝成功。請把這個畫面擷圖傳給 info@droidtown.co ，我們會再做調整。") 
else:
    print("看不懂你在選什麼，請重新執行一次。")