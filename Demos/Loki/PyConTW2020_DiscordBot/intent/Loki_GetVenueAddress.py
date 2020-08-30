#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for Traffic

    Input:
        pattern       str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_GetVenueAddress = True
userDefinedDICT = {'地址': ['地點', '位置', '位址'],
                   'PyConTW': ['pycontw', 'PYCON', 'Pycontw', 'PYCONTW', 'PyconTW', 'PyconTw', 'pycontw20', 'PYCON20', 'Pycontw20', 'PYCONTW20', 'PyconTW20', 'PyconTw20', 'pycontw2020', 'PYCONTW2020', 'Pycontw2020', 'PyconTW2020', 'PyconTw2020'],
                   '社群軌': ['Community Trac', 'community track', '社群track', '社群 track'],
                   '專業課程': ['專業課程與衝刺開發', '專業課程與衝刺', '衝刺開發', 'sprint', 'Sprint', 'SPRINT', 'sprints', 'Sprints', 'SPRINTS'],
                   '好想工作室': ['工作室', '好想工作']}

def destinationIdentifier(arg):
    '''
    依自建字典正規化要去的地址
    '''
    destDICT = {
    "main_venue": ['PyConTW', "會場", "會議廳", "成大國際會議廳", "國際會議廳", 'pycontw', 'PYCON', 'Pycontw', 'PYCONTW', 'PyconTW', 'PyconTw', 'pycontw20', 'PYCON20', 'Pycontw20', 'PYCONTW20', 'PyconTW20', 'PyconTw20', 'pycontw2020', 'PYCONTW2020', 'Pycontw2020', 'PyconTW2020', 'PyconTw2020'],
    "community" : ['社群軌', 'Community Trac', 'community track', '社群track', '社群 track'],
    "sprint"    : ['專業課程', "課程", '專業課程與衝刺開發', '專業課程與衝刺', '衝刺開發', 'sprint', 'Sprint', 'SPRINT', 'sprints', 'Sprints', 'SPRINTS'],
    "workshop"  : ['好想工作室', '工作室', '好想工作']
    }

    for dest in destDICT.keys():
        if arg in destDICT[dest]:
            return dest

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(pattern, utterance, args):
    if DEBUG_GetVenueAddress:
        print("[GetVenueAddress] {} ===> {}\n{}".format(utterance, args, pattern))

def getResult(pattern, utterance, args, resultDICT):
    debugInfo(pattern, utterance, args)
    if utterance == "哪裡有[專業課程與衝刺]":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "哪裡是[好想工作室]":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "哪裡是[好想工作室]的地址":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "哪裡是[PyConTW]會場":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "哪裡是[PyConTW]的會場地址":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]怎麼走去":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]在哪裡":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]的地址是什麼":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]地址怎麼走去":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]地址在哪裡":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[PyConTW]會場怎麼走去":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[PyConTW]會場在哪裡":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[PyConTW]會場地址是什麼":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[PyConTW]會場地址怎麼走去":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[PyConTW]會場地址在哪裡":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[Sprint]辦在哪裡":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]的地址":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    if utterance == "[好想工作室]的地址是":
        # write your code here
        resultDICT["destination"] = destinationIdentifier(args[0])

    return resultDICT