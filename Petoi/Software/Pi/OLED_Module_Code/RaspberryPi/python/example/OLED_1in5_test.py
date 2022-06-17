#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging    
import time
import traceback
from waveshare_OLED import OLED_1in5
from PIL import Image,ImageDraw,ImageFont
logging.basicConfig(level=logging.DEBUG)

try:
    disp = OLED_1in5.OLED_1in5()

    logging.info("\r 1.5inch OLED ")
    # Initialize library.
    disp.Init()
    # Clear display.
    logging.info("clear display")
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new('L', (disp.width, disp.height), 0)
    draw = ImageDraw.Draw(image1)
    font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    logging.info ("***draw line")
    draw.line([(0,0),(127,0)], fill = 15)
    draw.line([(0,0),(0,127)], fill = 15)
    draw.line([(0,127),(127,127)], fill = 15)
    draw.line([(127,0),(127,127)], fill = 15)
    logging.info ("***draw text")
    draw.text((20,0), 'Waveshare ', font = font1, fill = 15)
    draw.text((20,24), u'微雪电子 ', font = font2, fill = 11)
    draw.text((20,64), 'Waveshare ', font = font1, fill = 7)
    draw.text((20,92), u'微雪电子 ', font = font2, fill = 3)
    image1 = image1.rotate(0)
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(3)
 
    logging.info ("***draw rectangle")
    image1 = Image.new('L', (disp.width, disp.height), 0)
    draw = ImageDraw.Draw(image1)
    for i in range(0, 16):
        draw.rectangle([(0, 8*i), (128, 8*(i+1))], fill = i)
    disp.ShowImage(disp.getbuffer(image1))
    time.sleep(3)

    logging.info ("***draw image")
    Himage2 = Image.new('L', (disp.width, disp.height), 0)  # 0: clear the frame
    bmp = Image.open(os.path.join(picdir, '1in5.bmp'))
    Himage2.paste(bmp, (0,0))
    Himage2=Himage2.rotate(0) 	
    disp.ShowImage(disp.getbuffer(Himage2)) 
    time.sleep(3)    
    disp.clear()

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    OLED_1in5.config.module_exit()
    exit()