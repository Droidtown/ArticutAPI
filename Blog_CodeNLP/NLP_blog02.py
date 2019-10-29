#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut

text = "研究這個研究的研究已經被研究許多年了"


articut = Articut(username="", apikey="")
result = articut.parse(text)
print(result["result_pos"])