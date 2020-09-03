#!/usr/bin/python
# -*- coding:utf-8 -*
from light import Light
from ac import Ac
from tv import Tv
from time import sleep

lightPinLIST = [16, 19, 20, 21, 26]


if __name__ == "__main__":
    light = Light(lightPinLIST)
    ac = Ac(25, rst=24)
    tv = Tv(addr=0x27)
    
    print("Init Done")
    #sleep(3)

    #light.fullOn()
    #print("Light => {}".format(light.getCount()))
    ac.remote("fan", 4)
    #print("AC Fan => {}".format(ac.getFan()))
    tv.switch(True)
    #print("TV Status => {}".format(tv.getStatus()))
    
    #sleep(10)

    light.disco()
