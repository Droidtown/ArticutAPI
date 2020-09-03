from flask import Flask
from flask import render_template
from flask import request
from AIoT.AIoT import runLoki
from devices import light
from devices import tv
from devices import ac

app = Flask(__name__)
BOT_NAME = "小三"
devLight = None
devTV = None
devAC = None
DEFAULT_MSG = "對不起，{}不太了懂您的意思 ...".format(BOT_NAME)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/msg", methods=["POST"])
def processMsg():
    try:
        inputSTR = request.form.get("msg")
        resultDICT = runLoki(inputSTR)
        print(resultDICT)
        resultLen = len(resultDICT)
        try:
            if resultLen == 0:
                return {"type": "msg", "msg": DEFAULT_MSG}

            elif resultLen == 1:
                return controlDevices(resultDICT)

            elif resultLen == 2:
                for x in ["ac", "tv", "action"]:
                    if x in resultDICT and "question_{}".format(x) in resultDICT:
                        del resultDICT[x]
                        return controlDevices(resultDICT)

                return {"type": "command", "command": askCommand(resultDICT), "msg": "請問要{}幫您做什麼呢？".format(BOT_NAME)}

            else:
                return {"type": "msg", "msg": DEFAULT_MSG}

        except Exception as e:
            print(str(e))
            return {"type": "msg", "msg": DEFAULT_MSG}
    except:
        return {"type": "msg", "msg": DEFAULT_MSG}


@app.route("/command", methods=["POST"])
def processCommand():
    try:
        command = request.form.get("command")
        value = request.form.get("value")
        if value == "true":
            value = True
        if value == "false":
            value = False
        return controlDevices({command: value})
    except Exception as e:
        print(str(e))
        return {"type": "msg", "msg": DEFAULT_MSG}


###################################################

def controlDevices(resultDICT):
    try:

        command = None

        # AC
        if "ac" in resultDICT:
            typeSTR = "msg"
            status = devAC.switch(resultDICT["ac"])
            if status:
                if resultDICT["ac"]:
                    msg = "{}幫您開啟冷氣了。".format(BOT_NAME)
                else:
                    msg = "{}幫您關閉冷氣了。".format(BOT_NAME)
            else:
                msg = DEFAULT_MSG

        if "question_ac" in resultDICT:
            typeSTR = "question"
            command = {"command": "ac", "value": resultDICT["question_ac"]}
            if resultDICT["question_ac"]:
                msg = "請問要{}幫您開冷氣嗎？".format(BOT_NAME)
            else:
                msg = "請問要{}幫您關冷氣嗎？".format(BOT_NAME)

        if "set_temperature" in resultDICT:
            typeSTR = "msg"
            status = devAC.remoteNext("temp", resultDICT["set_temperature"])
            if status:
                if resultDICT["set_temperature"] >= 0:
                    msg = "{}幫您把冷氣調高 {} °C。".format(BOT_NAME, resultDICT["set_temperature"])
                else:
                    msg = "{}幫您把冷氣調低 {} °C。".format(BOT_NAME, abs(resultDICT["set_temperature"]))
            else:
                if devAC.getStatus() is False:
                    msg = "您的冷氣未開機。"
                else:
                    if resultDICT["set_temperature"] >= 0:
                        msg = "冷氣溫度已經最低了。".format(ac.TEMP_MIN)
                    else:
                        msg = "冷氣溫度已經最高了。".format(ac.TEMP_MAX)

        if "temperature" in resultDICT:
            typeSTR = "msg"
            status = devAC.remote("temp", resultDICT["temperature"])
            if status:
                msg = "{}幫您把冷氣調至 {} °C。".format(BOT_NAME, resultDICT["temperature"])
            else:
                if devAC.getStatus() is False:
                    msg = "您的冷氣未開機。"
                else:
                    msg = "冷氣溫度只能設定 {} ~ {} °C。".format(ac.TEMP_MIN, ac.TEMP_MAX)

        if "set_fan_speed" in resultDICT:
            typeSTR = "msg"
            status = devAC.remoteNext("fan", resultDICT["set_fan_speed"])
            if status:
                if resultDICT["set_fan_speed"] >= 0:
                    msg = "{}幫您把冷氣風量調大 {} 檔。".format(BOT_NAME, resultDICT["set_fan_speed"])
                else:
                    msg = "{]幫您把冷氣風量調小 {} 檔。".format(BOT_NAME, abs(resultDICT["set_fan_speed"]))
            else:
                if devAC.getStatus() is False:
                    msg = "您的冷氣未開機。"
                else:
                    if resultDICT["set_fan_speed"] >= 0:
                        msg = "冷氣風速已經最高檔了。"
                    else:
                        msg = "冷氣風速已經最低檔了。"

        if "time" in resultDICT:
            typeSTR = "msg"
            status = devAC.remote("timing", resultDICT["time"])
            if status:
                msg = "{}幫您冷氣定時 {} 小時".format(BOT_NAME, resultDICT["time"])
            else:
                if devAC.getStatus() is False:
                    msg = "您的冷氣未開機。"
                else:
                    msg = "冷氣定時只能設定 {} ~ {} 小時".format(ac.TIMING_MIN, ac.TIMING_MAX)

        # TV
        if "tv" in resultDICT:
            typeSTR = "msg"
            status = devTV.switch(resultDICT["tv"])
            if status:
                if resultDICT["tv"]:
                    msg = "{}幫您開啟電視了。".format(BOT_NAME)
                else:
                    msg = "{}幫您關閉電視了。".format(BOT_NAME)
            else:
                msg = DEFAULT_MSG

        if "question_tv" in resultDICT:
            typeSTR = "question"
            command = {"command": "tv", "value": resultDICT["question_tv"]}
            if resultDICT["question_tv"]:
                msg = "請問要{}幫您開電視嗎？".format(BOT_NAME)
            else:
                msg = "請問要{}幫您關電視嗎？".format(BOT_NAME)

        if "set_channel" in resultDICT:
            typeSTR = "msg"
            status = devTV.switchNext("channel", resultDICT["set_channel"])
            if status:
                if resultDICT["set_channel"] >= 0:
                    msg = "{}幫您把電視往後 {} 台。".format(BOT_NAME, resultDICT["set_channel"])
                else:
                    msg = "{}幫您把電視往前 {} 台。".format(BOT_NAME, abs(resultDICT["set_channel"]))
            else:
                if devTV.getStatus() is False:
                    msg = "您的電視未開機。"
                else:
                    msg = "電視頻道只能設定 {} ~ {} 台".format(tv.CHANNEL_MIN, tv.CHANNEL_MAX)

        if "channel" in resultDICT:
            typeSTR = "msg"
            status = devTV.switchTo("channel", resultDICT["channel"])
            if status:
                msg = "{}幫您把電視調至 {} 台。".format(BOT_NAME, resultDICT["channel"])
            else:
                if devTV.getStatus() is False:
                    msg = "您的電視未開機。"
                else:
                    msg = "電視頻道只能設定 {} ~ {} 台".format(tv.CHANNEL_MIN, tv.CHANNEL_MAX)

        if "set_volume" in resultDICT:
            typeSTR = "msg"
            status = devTV.switchNext("volume", resultDICT["set_volume"])
            if status:
                if resultDICT["set_volume"] >= 0:
                    msg = "{}幫您把電視音量調大 {} 格。".format(BOT_NAME, resultDICT["set_volume"])
                else:
                    msg = "{}幫您把電視音量調小 {} 格。".format(BOT_NAME, abs(resultDICT["set_volume"]))
            else:
                if devTV.getStatus() is False:
                    msg = "您的電視未開機。"
                else:
                    if resultDICT["set_volume"] >= 0:
                        msg = "電視音量已經最大聲了。"
                    else:
                        msg = "電視音量已經最小聲了。"

        if "volume" in resultDICT:
            typeSTR = "msg"
            status = devTV.switchTo("volume", resultDICT["volume"])
            if status:
                msg = "{}幫您把電視音量調至 {} 格。".format(BOT_NAME, resultDICT["volume"])
            else:
                if devTV.getStatus() is False:
                    msg = "您的電視未開機。"
                else:
                    msg = "電視音量只能設定 {} ~ {} 台".format(tv.VOLUME_MIN, tv.VOLUME_MAX)

        # Light
        if "action" in resultDICT:
            typeSTR = "msg"
            if resultDICT["action"] == "++":
                status = devLight.fullOn()
                if status:
                    msg = "{}幫您把燈光全打開了。".format(BOT_NAME)
                else:
                    msg = "燈已經全亮了。"

            if resultDICT["action"] == "--":
                status = devLight.fullOff()
                if status:
                    msg = "{}幫您把燈光全關閉了。".format(BOT_NAME)
                else:
                    msg = "燈已經全關了。"

            if resultDICT["action"] == "+":
                status = devLight.brighter()
                if status:
                    msg = "{}幫您打開 1 盞燈。".format(BOT_NAME)
                else:
                    msg = "燈已經全亮了。"

            if resultDICT["action"] == "-":
                status = devLight.darker()
                if status:
                    msg = "{}幫您關閉 1 盞燈。".format(BOT_NAME)
                else:
                    msg = "燈已經全關了。"

        if "question_action" in resultDICT:
            typeSTR = "question"
            command = {"command": "action", "value": resultDICT["question_action"]}
            if resultDICT["question_action"] == "++":
                msg = "請問要{}幫您開燈嗎？".format(BOT_NAME)
            else:
                msg = "請問要{}幫您關燈嗎？".format(BOT_NAME)

        if command is None:
            return {"type": typeSTR, "msg": msg}
        else:
            return {"type": typeSTR, "command": command, "msg": msg}
    except Exception as e:
        print(str(e))
        msg = DEFAULT_MSG

    return {"type": "msg", "msg": msg}


def askCommand(resultDICT):
    commandLIST = []

    # AC
    if "ac" in resultDICT:
        commandDICT = {"command": "ac", "value": resultDICT["ac"]}
        if resultDICT["ac"]:
            commandDICT["text"] = "開冷氣"
        else:
            commandDICT["text"] = "關冷氣"
        commandLIST.append(commandDICT)

    if "set_temperature" in resultDICT:
        commandDICT = {"command": "set_temperature", "value": resultDICT["set_temperature"]}
        if resultDICT["set_temperature"] >= 0:
            commandDICT["text"] = "冷氣溫度調高 {} °C".format(resultDICT["set_temperature"])
        else:
            commandDICT["text"] = "冷氣溫度調低 {} °C".format(abs(resultDICT["set_temperature"]))
        commandLIST.append(commandDICT)

    if "temperature" in resultDICT:
        commandLIST.append({"command": "temperature", "value": resultDICT["temperature"], "text": "冷氣溫度設定 {} °C".format(resultDICT["temperature"])})

    if "set_fan_speed" in resultDICT:
        commandDICT = {"command": "set_fan_speed", "value": resultDICT["set_fan_speed"]}
        if resultDICT["set_fan_speed"] >= 0:
            commandDICT["text"] = "冷氣風速調高 {} 檔".format(resultDICT["set_fan_speed"])
        else:
            commandDICT["text"] = "冷氣風速調低 {} 檔".format(abs(resultDICT["set_fan_speed"]))
        commandLIST.append(commandDICT)

    if "time" in resultDICT:
        commandLIST.append({"command": "time", "value": resultDICT["time"], "text": "冷氣定時設定 {} 小時".format(resultDICT["time"])})

    # TV
    if "tv" in resultDICT:
        commandDICT = {"command": "tv", "value": resultDICT["tv"]}
        if resultDICT["tv"]:
            commandDICT["text"] = "開電視"
        else:
            commandDICT["text"] = "關電視"
        commandLIST.append(commandDICT)

    if "set_channel" in resultDICT:
        commandDICT = {"command": "set_channel", "value": resultDICT["set_channel"]}
        if resultDICT["set_channel"] >= 0:
            commandDICT["text"] = "電視頻道往後 {} 台".format(resultDICT["set_channel"])
        else:
            commandDICT["text"] = "電視頻道往前 {} 台".format(abs(resultDICT["set_channel"]))
        commandLIST.append(commandDICT)

    if "channel" in resultDICT:
        commandLIST.append({"command": "channel", "value": resultDICT["channel"], "text": "電視頻道設定 {} 台".format(resultDICT["set_channel"])})

    if "set_volume" in resultDICT:
        commandDICT = {"command": "set_volume", "value": resultDICT["set_volume"]}
        if resultDICT["set_volume"] >= 0:
            commandDICT["text"] = "電視音量調大 {} 格".format(resultDICT["set_volume"])
        else:
            commandDICT["text"] = "電視音量調小 {} 格".format(abs(resultDICT["set_volume"]))
        commandLIST.append(commandDICT)

    if "volume" in resultDICT:
        commandLIST.append({"command": "volume", "value": resultDICT["volume"], "text": "電視音量設定 {} 格".format(resultDICT["set_channel"])})

    # Light
    if "action" in resultDICT:
        commandDICT = {"command": "action", "value": resultDICT["action"]}
        if resultDICT["action"] == "++":
            commandDICT["text"] = "電燈全開"
        if resultDICT["action"] == "--":
            commandDICT["text"] = "電燈全關"
        if resultDICT["action"] == "+":
            commandDICT["text"] = "電燈調亮一格"
        if resultDICT["action"] == "-":
            commandDICT["text"] = "電燈調暗一格"
        commandLIST.append(commandDICT)

    return commandLIST


if __name__ == "__main__":
    devLight = light.Light([16, 19, 20, 21, 26])
    devTV = tv.Tv(addr=0x27, port=1, backlight=True)
    devAC = ac.Ac(25, rst=24)
    app.run(debug=True, host="0.0.0.0")