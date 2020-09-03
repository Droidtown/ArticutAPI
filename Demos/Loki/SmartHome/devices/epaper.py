#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from waveshare_epd import epd2in7b
from time import time

class Epaper():
    
    epd = None

    def __init__(self):
        try:
            startTime = time()
            self.epd = epd2in7b.EPD()
            self.epd.init()
            print("Init: %f sec" % (time()-startTime))
        except:
            self.epd = None

    def setText(self, textLIST):
        if self.epd is None:
            return False

        startTime = time()
        self.epd.Clear()
        print("Clear: %f sec" % (time()-startTime))

        startTime = time()
        font = ImageFont.truetype('Font.ttc', 50)
        HBlackimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 298*126
        #HRedimage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 298*126    
        HRedimage = Image.new('1', (0, 0), 255)  # 0*0    
    
        drawblack = ImageDraw.Draw(HBlackimage)
        drawred = ImageDraw.Draw(HRedimage)

        for text in textLIST:
            #print(text)
            #if text["color"] == "black":
            drawblack.text((text["x"], text["y"]), text["text"], font=font, fill=0)
            #if text["color"] == "red":
                #drawred.text((text["x"], text["y"]), text["text"], font=font, fill=0)
        
        self.epd.display(self.epd.getbuffer(HBlackimage), self.epd.getbuffer(HRedimage))
        print("execute: %f sec" % (time()-startTime))
        #self.epd.sleep()

        return True

if __name__ == "__main__":
    epaper = Epaper()
    epaper.setText([
        {
            "color": "black",
            "text": "頻道：",
            "x": 20,
            "y": 20
        },
        {
            "color": "red",
            "text": "62",
            "x": 170,
            "y": 20
        },
        {
            "color": "black",
            "text": "音量：",
            "x": 20,
            "y": 90
        },
        {
            "color": "red",
            "text": "12",
            "x": 170,
            "y": 90
        }
    ])
