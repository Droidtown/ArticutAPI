#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#from nltk.corpus import stopwords
#EngStopWords = set(stopwords.words('english'))#這裡設定稍後取用 English 的停用詞語料庫
#text = "There is an apple on the table."
#for word in text.split():
    #if word in EngStopWords:
        #pass #如果詞彙是個英文的停用詞的話，就略過不處理。
    #else:
        #print(word) #如果詞彙不是英文的停用詞的話，呈現在畫面上。


from ArticutAPI import Articut

text = "餐桌上面有一顆蘋果"

articut = Articut(username="", apikey="")
result = articut.parse(text)

contentWordLIST = articut.getContentWordLIST(result)
for sentence in contentWordLIST:
    for word in sentence:
        print(word[-1])