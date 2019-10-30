#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#from nltk.tokenize import sent_tokenize, word_tokenize

#text = "I know all work and no play can make Jack a dull boy. I didn't know all play and no work would make Jack a drama queen."

#sentences = sent_tokenize(text)
#print("句子的 Token:{}".format(sentences))
#words = word_tokenize(text)
#print("字彙的 Token:{}".format(words))



#text = "I didn't do it."
#print("用 .split():", text.split())
#print("用 .word_tokenization():", word_tokenize(text))



from ArticutAPI import Articut
import re

text = "整天工作不玩耍，型男也會變傻瓜。"


articut = Articut(username="", apikey="")
result = articut.parse(text)

# 利用 ArticutAPI 做中文「句子」的 tokenization
sentenceTokenLIST = []
for s in result["result_pos"]: #在 result_pos 裡，標點符號不會被加上 POS 標記，因此字串長度為 1。
    if len(s) != 1:
        sentenceTokenLIST.append(re.sub("</?[^>]*?>", "", s))

print("句子 token 的結果為：{}".format(sentenceTokenLIST))


# 利用 ArticutAPI 做中文「詞彙」的 tokenization
sentenceSpliter = []
for s in result["result_pos"]: #在 result_pos 裡，標點符號不會被加上 POS 標記，因此字串長度為 1。
    if len(s) == 1:
        sentenceSpliter.append(s)

wordTokenLIST = result["result_segmentation"].split("/")
for i in wordTokenLIST:
    if i in sentenceSpliter:
        wordTokenLIST.remove(i)

print("詞彙 Token 的結果為：{}".format(wordTokenLIST))