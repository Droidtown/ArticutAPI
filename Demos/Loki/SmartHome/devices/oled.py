#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306
from time import sleep

class Oled():

    oled = None

    def __init__(self):
        try:
            self.oled = Adafruit_SSD1306.SSD1306_128_32(rst=None)
            self.oled.begin()
            self.oled.clear()
            self.oled.display()
        except:
            self.oled = None

    def setText(self, text):
        if self.oled is None:
            return False
        
        font = ImageFont.truetype("Font.ttc", 30)
        image = Image.new('1', (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
        draw.text((0, 0), text, font=font, fill=255)
        self.oled.image(image)
        self.oled.display()

        return True

if __name__ == "__main__":
    oled = Oled()
    oled.setText("溫度30°C")
    sleep(10)
