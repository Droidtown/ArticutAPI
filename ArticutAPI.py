#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
import requests

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        self.url = "https://api.droidtown.co"
        self.username = username
        self.apikey = apikey
        self.version = version
        self.level = level

        self.userDefinedDictFILE = None
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

    def __str__(self):
        return "Articut API"

    def parse(self, inputSTR, level="", userDefinedDictFILE=None):
        if level=="":
            level = self.level

        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,
                   "username": self.username,
                   "api_key": self.apikey,
                   "version": self.version,
                   "level": level}

        if userDefinedDictFILE:
            try:
                if os.path.getsize(userDefinedDictFILE) <= self.fileSizeLimit:
                    userDefinedFile = json.load(open(userDefinedDictFILE, "r", encoding="utf8"))
                    if type(userDefinedFile) == dict:
                        payload["file"] = userDefinedFile
                    else:
                        print("User Defined File must be dict type.")
                        return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}
                else:
                    print("Maximum file size limit is 10 MB.")
            except Exception as e:
                print("User Defined File Loading Error.")
                print(str(e))
                return {"status": False, "msg": "UserDefinedDICT Parsing ERROR. Please check your the format and encoding."}

        result = requests.post(url, json=payload)
        if result.status_code == 200:
            result = result.json()
            result["product"] = "{}/product/".format(self.url)
            result["document"] = "{}/document/".format(self.url)
        return result

    def versions(self):
        url = "{}/Articut/Versions/".format(self.url)
        payload = {"username":  self.username,
                   "api_key":   self.apikey}
        result = requests.post(url, data=payload)
        if result.status_code == 200:
            result = result.json()
            result["product"] = "{}/product/".format(self.url)
            result["document"] = "{}/document/".format(self.url)
        return result

if __name__ == "__main__":
    from pprint import pprint

    inputSTR = "我要重修計概"
    articut = Articut()

    result = articut.parse(inputSTR, "./UserDefinedFile.json")
    pprint(result)

    result = articut.versions()
    pprint(result)
