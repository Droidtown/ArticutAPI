#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI
import os

from time import sleep

FAN_MIN = 1
FAN_MAX = 4
FAN_DEFAULT = 1
FAN_LIST = ["▄", "▅", "▆", "▇"]
TEMP_MIN = 16
TEMP_MAX = 30
TEMP_DEFAULT = 26
TIMING_MIN = 0
TIMING_MAX = 12
TIMING_DEFAULT = 0

class Ac():
    
    tft = None
    status = False
    fan = 0
    temp = 0
    timing = 0

    def __init__(self, dc=25, rst=24):
        try:
            self.tft = TFT.ILI9341(dc, rst=rst, spi=SPI.SpiDev(0, 0))
            self.tft.begin()
            self.status = False
            self.fan = FAN_DEFAULT
            self.temp = TEMP_DEFAULT
            self.timing = TIMING_DEFAULT
            self.tft.clear()
            self.tft.display()
        except:
            self.tft = None
    
    def getStatus(self):
        return self.status
    
    def getFan(self):
        return self.fan

    def getTemp(self):
        return self.temp

    def getTiming(self):
        return self.timing

    def setText(self):
        if self.tft is None:
            return False
        
        self.tft.clear()
        fontPath = os.getcwd()
        if "devices" not in fontPath:
            fontPath = "{}/devices".format(fontPath)
        font = ImageFont.truetype('{}/Font.ttc'.format(fontPath), 60)
        textImage = Image.new("RGBA", (320, 240), (0, 0, 0, 0))
        textDraw = ImageDraw.Draw(textImage)
        textDraw.text((0, 10), "風速", font=font, fill=(255, 255, 255))
        for i in range(0, self.fan):
            textDraw.text((140 + i * 40, 0), FAN_LIST[i], font=font, fill=(255, 255, 255))
        textDraw.text((0, 85), "溫度", font=font, fill=(255, 255, 255))
        textDraw.text((170, 85), "{:02d}°C".format(self.temp), font=font, fill=(255, 255, 255))
        textDraw.text((0, 160), "定時", font=font, fill=(255, 255, 255))
        textDraw.text((170, 160), "{:02d}hr".format(self.timing), font=font, fill=(255, 255, 255))
        rotated = textImage.rotate(-90, expand=1)
        self.tft.buffer.paste(rotated, (0, 15), rotated)

        self.tft.display()

        return True

    def switch(self, status):
        if self.tft is None:
            return False

        self.status = status
        if status:
            return self.setText()
        else:
            self.tft.clear()
            self.tft.display()
            return True

    def remote(self, mode, num):
        if self.tft is None:
            return False

        if self.status:
            if mode == "fan":
                if num >= FAN_MIN and num <= FAN_MAX:
                    self.fan = num
                    return self.setText()
                else:
                    return False
            if mode == "temp":
                if num >= TEMP_MIN and num <= TEMP_MAX:
                    self.temp = num
                    return self.setText()
                else:
                    return False
            if mode == "timing":
                if num >= TIMING_MIN and num <= TIMING_MAX:
                    self.timing = num
                    return self.setText()
                else:
                    return False
        
        return False

    def remoteNext(self, mode, num=1):
        if self.tft is None:
            return False
        
        if self.status:
            if mode == "fan":
                return self.remote("fan", (self.fan + num))
            if mode == "temp":
                return self.remote("temp", (self.temp + num))
            if mode == "timing":
                return self.remote("timing", (self.timing + num))

        return False

    def remoteLast(self, mode, num=1):
        if self.tft is None:
            return False

        if self.status:
            if mode == "fan":
                return self.remote("fan", (self.fan - num))
            if mode == "temp":
                return self.remote("temp", (self.temp - num))
            if mode == "timing":
                return self.remote("timing", (self.timing - num))

        return False


if __name__ == "__main__":
    ac = Ac()
    ac.switch(True)
    sleep(1)
    print(ac.remote("temp", 22))
    sleep(1.5)
    print(ac.remoteLast("temp", num=2))
    sleep(1.5)
    print(ac.remoteNext("fan", num=3))
    sleep(1.5)
    print(ac.remote("timing", 6))
    sleep(1.5)
    ac.switch(False)