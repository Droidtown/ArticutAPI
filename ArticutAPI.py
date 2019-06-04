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

        self.file = None
        self.fileSizeLimit = 1024 * 1024 * 10    # 10 MB

    def __str__(self):
        return "Articut API"

    def parse(self, inputSTR, level="", file=None):
        if level=="":
            level = self.level

        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,
                   "username": self.username,
                   "api_key": self.apikey,
                   "version": self.version,
                   "level": level}

        if file:
            try:
                if os.path.getsize(file) <= self.fileSizeLimit:
                    userDefinedFile = json.load(open(file, "r", encoding="utf8"))
                    if type(userDefinedFile) == list:
                        payload["file"] = userDefinedFile
                else:
                    print("Maximum file size limit is 10 MB.")
            except Exception as e:
                print("User Defined List File Loading Error.")
                print(str(e))

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

    inputSTR = "努力才能成功"
    articut = Articut()

    result = articut.parse(inputSTR)
    pprint(result)

    result = articut.versions()
    pprint(result)
