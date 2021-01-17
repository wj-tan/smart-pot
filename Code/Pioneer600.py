#!/usr/bin/python
# -*- coding:utf-8 -*-
# Cem KEYLAN
# 2018
# Version 1.1

import RPi.GPIO as GPIO
import smbus
import spidev as SPI
import SSD1306
import time
import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import add_module

import Sensors

arrData = [] #array to store sensors and machine learning data to be displayed later in the oled

#this method is to update the menu that is taking data from arrData[] hourly
def updateMenu():
    global arrData #calls the global variable
    arrData = Sensors.main() #calling the main function which take in all the sensors data as well as publish to Thingsboard
    threading.Timer(10, updateMenu).start() #setup a timer interrupt to call the updateMenu() every 3600 seconds
    
updateMenu()

KEY = 20
address = 0x20
main_menu = 1
submenus = 1


def beep_on():
    bus.write_byte(address,0x7F&bus.read_byte(address))
def beep_off():
    bus.write_byte(address,0x80|bus.read_byte(address))
def led_off():
    bus.write_byte(address,0x10|bus.read_byte(address))
def led_on():
    bus.write_byte(address,0xEF&bus.read_byte(address))


def oled(Line1, Line2, Line3=""):
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top), str(Line1), font=font1, fill=255)
        draw.text((x, top+20), str(Line2), font=font2, fill=255)
        draw.text((x, top+40), str(Line3), font=font2, fill=255)
        disp.image(image)
        disp.display()

def MyInterrupt(KEY):
    print("KEY PRESS")

def menu ():
    global values
    global submenus
    global main_menu
    
    if values == "up" :
        submenus = submenus - 1
    elif values == 'down' :
        submenus = submenus + 1
    elif values == "right" :
        main_menu = main_menu + 1
        submenus = 1
    elif values == "left" :
        main_menu = main_menu - 1
        submenus = 1

    if main_menu == 5:
        main_menu = 1
    if main_menu == 0:
        main_menu = 4

    # Main Information delivering up status
    if main_menu == 1 :
        strtime = time.strftime("%H : %M : %S")

        if submenus == 4:
            submenus = 1
        if submenus ==0:
            submenus =3

        if submenus == 1:
            oled(arrData[7], arrData[8], arrData[9])
        elif submenus == 3 :
            if len(os.popen("hostname -I").read()) == 1 :
                upstatus = "Down"
            else:
                upstatus = "UP"
            oled("Status = " + upstatus,os.popen("/sbin/ifconfig eth0 | grep 'inet ' | cut -d: -f2 | awk '{ print $2}'").read(), strtime)
        elif submenus == 2 :
            if len(os.popen("hostname -I").read()) is not 1:
                if "unreachable" in os.popen("nc 8.8.8.8 53 -zv").read():
                    oled("Connection", "could NOT be","established.")
                else:
                    oled("Connection","could be","established.")


    # Device Info
    elif main_menu == 2:
        
        if submenus == 5:
            submenus = 1
        if submenus ==0:
            submenus =4


        
        if submenus == 4 :
            if (isinstance(arrData[1], str) == True):
                oled("Readings","Moisture", arrData[1])
            else:
                oled("Readings","Moisture", str( round(arrData[1],2) ) + " %")
        elif submenus == 3 :
            if (isinstance(arrData[0], str) == True):
                oled("Readings","LDR", arrData[0])
            else:
                oled("Readings","LDR", str(arrData[0]) + " ohm")
        elif submenus == 2 :
            if (isinstance(arrData[3], str) == True):
                oled("Readings","Humidity", arrData[3])
            else:
                oled("Readings","Humidity", str( round(arrData[3],2) ) + " %")
        
        elif submenus == 1 :
            if (isinstance(arrData[2], str) == True):
                oled("Readings","Temperature", arrData[2])
            else:
                oled("Readings","Temperature", str( round(arrData[2],2) )+ " C")
            
    #aç kapa
    elif main_menu == 3 :

        if submenus == 4:
            submenus = 1
        if submenus == 0:
            submenus = 3

        elif submenus == 1 :
            oled("System","Close App","Press Button")
            if GPIO.input(KEY) == 0:
                if len(os.popen("hostname -I").read()) is not 1:
                    exit ()
                else:
                    oled("System","Close App","Must be connected")
                    time.sleep(2)
        elif submenus == 2 :
            oled("System","Reboot","Press Button")
            if GPIO.input(KEY) == 0:
                os.popen('sudo reboot')
        elif submenus == 3 :
            oled("System","Halt System","Press Button")
            if GPIO.input(KEY) == 0:
                os.popen('sudo halt')

    #interfaces
    elif main_menu == 4 :
        if submenus == 4:
            submenus = 1
        if submenus == 0:
            submenus = 3
            
        elif submenus == 2 :
            if (isinstance(arrData[4], str) == True):
                oled("Readings","Germination", arrData[4])
            else:
                oled("Readings","Germination", str(arrData[4])+ " Hrs")
        elif submenus == 1:
            res = isinstance(arrData[5], str) 
            if (res == True):
                oled("Readings","EPH", arrData[5])
            else:
                oled("Readings","EPH", str( round(arrData[5],2) )+ " Hrs")
        elif submenus == 3:
            oled("Readings","Plant Status", arrData[6])


    else :
        print ("Something went wrong")

    return (submenus)

# Raspberry Pi pin configuration:
RST = 19
# Note the following are only used with SPI:
DC = 16
bus = 0
device = 0

# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(RST, DC, SPI.SpiDev(bus,device))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = 1
top = padding
x = padding
# Load default font.
# font = ImageFont.load_default()
font_dir =  os.path.dirname(os.path.realpath(__file__)) +"/KeepCalm-Medium.ttf"
font1 = ImageFont.truetype(font_dir, 15)
font2 = ImageFont.truetype(font_dir, 14)

GPIO.setmode(GPIO.BCM)
GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP)
#GPIO.add_event_detect(KEY,GPIO.FALLING,MyInterrupt,200)

#bmp = BMP180()
bus = smbus.SMBus(1)

print("Starting...")
print("Version 1.1")

try:
    while True:
        bus.write_byte(address,0x0F|bus.read_byte(address))
        value = bus.read_byte(address) | 0xF0
        if value != 0xFF:
            led_on()
            if (value | 0xFE) != 0xFF:
                values= "left"
            elif (value | 0xFD) != 0xFF:
                values= "up"
            elif (value | 0xFB) != 0xFF:
                values= "down"
            else :
                values= "right"
            while value != 0xFF:
                bus.write_byte(address,0x0F|bus.read_byte(address))
                value = bus.read_byte(address) | 0xF0
                time.sleep(0.01)
            led_off()
            submenus=menu()

        time.sleep(0.1)
        values= "YOK"
        submenus=menu()

# for keyboard interrupt
except (KeyboardInterrupt, SystemExit):
    print ("Keyboard Interrupt")
    # Clear display.
    disp.clear()
    disp.display()

except:
    print ("ERROR")
    # Clear display.
    oled("There was an error","")
    time.sleep(2)
    disp.clear()
    disp.display()
