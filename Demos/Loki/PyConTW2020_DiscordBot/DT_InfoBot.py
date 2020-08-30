#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#載入 runLoki() 以便稍後把 Discord 取得的句子交給 Loki 處理。
from PyConTW2020_InfoBot import runLoki

#讀入大會相關資訊
import json
with open("info.json", encoding="utf-8") as infoFILE:
    infoDICT = json.loads(infoFILE.read())

# DT_InfoBot.py
import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#啟動 Discord Bot
@client.event
async def on_ready():
    print(
        f'{client.user} is connected to the following guild:\n'
    )

#聆聽頻道內容
@client.event
async def on_message(message):
    #避免 bot 自問自答
    if message.author == client.user:
        return

    #處理 Bot 的回覆資訊
    response = "[DumpMode: On] I do not have information about this."
    #只有當 Bot 被指定回覆時 (e.g., @Bot) 才會處理。
    if "<@!{}> ".format(client.user.id) in message.content:
        msgSTR = message.content.replace("<@!{}> ".format(client.user.id), "")
        if msgSTR == "RADIO CHECK":
            response = "555, Loud & Clear!"
        else:
            NLUresultDICT = runLoki(msgSTR)
            if "destination" in NLUresultDICT:
                response = "\n".join(infoDICT[NLUresultDICT["destination"]])
        await message.channel.send(response)
    else: #如果沒有指定 Bot 回覆，直接略過。不做存檔處理，保障使用者隱私。
        return

client.run(TOKEN)
