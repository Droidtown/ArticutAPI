#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests

class Articut:
    def __init__(self, username="", apikey="", version="latest", level="lv2"):
        self.username = username
        self.apikey = apikey
        self.version = version
        self.level = level

        self.url = "https://api.droidtown.co"

    def __str__(self):
        return "Articut API"

    def parse(self, inputSTR, level=""):
        if level=="":
            level = self.level
        else:
            pass
        url = "{}/Articut/API/".format(self.url)
        payload = {"input_str": inputSTR,
                   "username": self.username,
                   "api_key": self.apikey,
                   "version": self.version,
                   "level": level}
        result = requests.post(url, data=payload)
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

