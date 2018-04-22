# -*- coding: utf-8 -*-
import os
import time
import datetime

from sense_hat import SenseHat

if __name__ == "__main__":
    s = SenseHat()
    temp = min([s.get_temperature_from_humidity(), s.get_temperature_from_pressure()]) - 4.0 # correction
    hum = s.get_humidity()
    s.rotation = 180
    pres = s.get_pressure()/1000.0
    s.low_light = True 
    t = datetime.datetime.now().strftime("%b %d, %Y. %H:%M")
    
    for i in range(0, 29 - 8):
        p = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "img_{}.png".format(i))
        s.load_image(p)
        time.sleep(0.3)
    time.sleep(1)
    for i in reversed(range(0, 29 - 8)):
        p = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "img_{}.png".format(i))
        s.load_image(p)
        time.sleep(0.3)
    time.sleep(1)

    for i in range(2):
        s.show_message(t, scroll_speed=0.05, text_colour=[255,0,0])
        message = "T: {:1.1f} C".format(temp)
        s.show_message(message, scroll_speed=0.05, text_colour=[239, 83, 80])
        message = "H: {:1.1f}%".format(hum)
        s.show_message(message, scroll_speed=0.05, text_colour=[38, 166, 154])
        message = "P: {:1.2f}bar".format(pres)
        s.show_message(message, scroll_speed=0.05, text_colour=[128, 222, 234])
        time.sleep(1)
    
    s.low_light = False

    for i in range(0, 29 - 8):
        p = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "img_{}.png".format(i))
        s.load_image(p)
        time.sleep(0.3)
    time.sleep(1)
    for i in reversed(range(0, 29 - 8)):
        p = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "img_{}.png".format(i))
        s.load_image(p)
        time.sleep(0.3)
    time.sleep(1)

    s.rotation = 0
    s.low_light = False
