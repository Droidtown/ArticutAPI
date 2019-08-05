#!/usr/bin/env python
# -*- coding:utf-8 -*-



class QuoiphQL(object):
    def __init__(self, inputSTR, langModel=None):
        self.inputSTR = inputSTR
        self.langModel = langModel
        if self.langModel in ("TW", "CN"):
            pass
        else:
            self.langModel = "TW"

        #self.functions=self.__dir__()
        return None

    def method01(self):
        return self.inputSTR


if __name__ == "__main__":
    doc = QuoiphQL("中文測試")
    print(doc.method01)

