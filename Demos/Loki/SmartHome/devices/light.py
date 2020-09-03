#!/usr/bin/python
# -*- coding:utf-8 -*-
from gpiozero import LED
from time import sleep

class Light():
    ledLIST = None
    ledLen = 0
    ledCount = 0

    def __init__(self, ledPinLIST):
        try:
            self.ledLIST = []
            for ledPin in ledPinLIST:
                self.ledLIST.append(LED(ledPin))
            self.ledLen = len(self.ledLIST)
            self.ledCount = 0
        except:
            self.ledLIST = None
            self.ledlen = 0
            self.ledCount = 0

    def getLen(self):
        return self.ledLen

    def getCount(self):
        return self.ledCount

    def setLight(self):
        if self.ledLIST is None:
            return False

        for i in range(0, self.ledLen):
            if i < self.ledCount:
                self.ledLIST[i].on()
            else:
                self.ledLIST[i].off()
        
        return True

    def fullOff(self):
        if self.ledLen > 0:
            self.ledCount = 0
            return self.setLight()
        else:
            return False

    def fullOn(self):
        if self.ledLen > 0:
            self.ledCount = self.ledLen
            return self.setLight()
        else:
            return False
    
    def brighter(self, count=1):
        if (self.ledCount + count) <= self.ledLen:
            self.ledCount += count
            return self.setLight()
        else:
            return False

    def darker(self, count=1):
        if (self.ledCount - count) >= 0:
            self.ledCount -= count
            return self.setLight()
        else:
            return False

    def disco(self):
        if self.ledLen > 0:
            self.fullOff()
            sleep(0.2)
            for i in range(0, self.ledLen):
                self.brighter()
                sleep(0.3)
            for i in range(0, self.ledLen):
                self.darker()
                sleep(0.3)
            for i in range(0, 30):
                for j in range(0, self.ledLen):
                    if i % 2 == 0:
                        if j % 2 == 0:
                            self.ledLIST[j].on()
                        else:
                            self.ledLIST[j].off()
                    else:
                        if j % 2 == 0:
                            self.ledLIST[j].off()
                        else:
                            self.ledLIST[j].on()
                sleep(0.3)

            return True
        else:
            return False

if __name__ == "__main__":
    lightPinLIST = [16, 19, 20, 21, 26]
    light = Light(lightPinLIST)
    for i in range(0, len(lightPinLIST)):
        light.brighter()
        sleep(1.5)
    for i in range(0, len(lightPinLIST)):
        light.darker()
        sleep(1.5)

    light.fullOn()
    sleep(3)
    light.fullOff()
