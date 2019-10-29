#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from ArticutAPI import Articut

text = "處理自然語言文字"


articut = Articut(username="", apikey="")
result = articut.parse(text)
print(result["result_segmentation"].split("/")[3])