import socket
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import traceback
from waveshare_OLED import OLED_0in91
from PIL import Image,ImageDraw,ImageFont

try:
    disp = OLED_0in91.OLED_0in91()
    # Initialize library.
    disp.Init()
        
    # Clear display.
    disp.clear()

    # Create blank image for drawing.
    image1 = Image.new('1', (disp.width, disp.height), "WHITE")
    draw = ImageDraw.Draw(image1)
    font1 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12)
    font2 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    #Get IP
    host_name = socket.gethostname()
    ip = "IP: " + socket.gethostbyname(host_name + ".local")
    draw.text((20,0), ip, font = font1, fill = 0)

    image1=image1.rotate(0) 
    disp.ShowImage(disp.getbuffer(image1))

except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    OLED_0in91.config.module_exit()
    exit()
