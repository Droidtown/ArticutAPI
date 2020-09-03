#!/usr/bin/python
# -*- coding:utf-8 -*-
from RPLCD.i2c import CharLCD
from time import sleep
import smbus2

CHANNEL_MIN = 1
CHANNEL_MAX = 300
CHANNEL_DEFAULT = 6
VOLUME_MIN = 0
VOLUME_MAX = 40
VOLUME_DEFAULT = 10

class Tv():

    lcd = None
    status = False
    channel = 0
    volume = 0

    def __init__(self, addr=0x27, port=1, backlight=True):
        try:
            self.lcd = CharLCD('PCF8574', address=addr, port=port, backlight_enabled=backlight)
            self.status = False
            self.channel = CHANNEL_DEFAULT
            self.volume = VOLUME_DEFAULT
        except:
            self.lcd = None
   
    def getStatus(self):
        return self.status

    def getChannel(self):
        return self.channel

    def getVolume(self):
        return self.volume

    def setText(self, textLIST):
        if self.lcd is None:
            return False

        for text in textLIST:
            self.lcd.cursor_pos = (text["y"], text["x"])
            self.lcd.write_string(text["text"])

        return True

    def switch(self, status):
        if self.lcd is None:
            return False

        self.lcd.clear()
        self.status = status
        if status:
            return self.setText([
                {"x":0,"y":0,"text":"Channel"},{"x":8,"y":0,"text":"--->"},{"x":13,"y":0,"text":f"{self.channel:03}"},
                {"x":0,"y":1,"text":"Volume"},{"x":8,"y":1,"text":"--->"},{"x":13,"y":1,"text":f"{self.volume:03}"}])
        else:
            return True

    def updateValue(self, mode):
        if self.lcd is None:
            return False

        if mode == "channel":
            return self.setText([{"x": 13, "y": 0, "text": f"{self.channel:03}"}])
        if mode == "volume":
            return self.setText([{"x": 13, "y": 1, "text": f"{self.volume:03}"}])

        return False

    def switchTo(self, mode, num):
        if self.lcd is None:
            return False

        if self.status:
            if mode == "channel":
                if num >= CHANNEL_MIN and num <= CHANNEL_MAX:
                    self.channel = num
                    return self.updateValue("channel")
                else:
                    if num < CHANNEL_MIN:
                        self.channel = CHANNEL_MAX
                        return self.updateValue("cahnnel")
                    if num > CHANNEL_MAX:
                        self.channel = CHANNEL_MIN
                        return self.updateValue("channel")
                    return False

            if mode == "volume":
                if num >= VOLUME_MIN and num <= VOLUME_MAX:
                    self.volume = num
                    return self.updateValue("volume")
                else:
                    return False

        return False

    def switchNext(self, mode, num=1):
        if self.lcd is None:
            return False

        if mode == "channel":
            return self.switchTo("channel", self.channel + num)
        if mode == "volume":
            return self.switchTo("volume", self.volume + num)

        return False

    def switchLast(self, mode, num=1):
        if self.lcd is None:
            return False

        if mode == "channel":
            return self.switchTo("channel", self.channel - num)
        if mode == "volume":
            return self.switchTo("volume", self.volume - num)

        return False


if __name__ == "__main__":
    tv = Tv()
    print(tv.switch(True))
    sleep(1.5)
    print(tv.switchTo("channel", 50))
    sleep(1.5)
    print(tv.switchLast("volume"))
    sleep(1.5)
    print(tv.switch(False))
