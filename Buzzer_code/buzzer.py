#!/usr/bin/python
# -*- coding:utf-8 -*-
#Based on https://www.waveshare.com/wiki/File:Pioneer600-Code.tar.gz Libaries
import RPi.GPIO as GPIO #import RPI.GPIO module
import smbus # smbus Library
import time # Time Library
import socket #socket Library
import spidev as SPI #Library for interfacing with SPI device
import SSD1306 #SDD1306 Driver
import threading
from threading import Thread
from PIL import Image  #Python Imaging Library
from PIL import ImageDraw #Python Imaging Library
from PIL import ImageFont #Python Imaging Library
UDP_IP="192.168.43.252" #IP address for this raspberry pi
UDP_PORT=5000 #Port number used for UDP
sock= socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #Specify that IPV4 and UDP is used
sock.bind((UDP_IP, UDP_PORT))   #socket.bind
address = 0x20 #i2c address

def beep_on(): #function to turn the buzzer on
	bus.write_byte(address,0x7F&bus.read_byte(address)) 
def beep_off(): #function to turn buzzer off
	bus.write_byte(address,0x80|bus.read_byte(address))
	disp.clear() 
	disp.display()
def display_help():
	draw.text((x, top),    'Help',  font=font, fill=500)  #Draw text on image
	draw.text((x, top+20), 'User Falling', font=font, fill=500) #Draw text on image
#Display image
	disp.image(image) 
	disp.display()
	#print("test")
def alert_user():
	beep_on() # write register to beep
	display_help() # display help message
	threading.Timer(2.5,beep_off).start() #threaded timer to off beep and clear display
	print("Reseted")
# Raspberry Pi pin configuration:
RST = 19
DC = 16
device = 0 
bus = smbus.SMBus(1)
#print("PCF8574 Test Program !!!")
# 128x64 display with hardware SPI:
disp = SSD1306.SSD1306(RST, DC, SPI.SpiDev(0, device))
#print("PCF8574 Test Program !!!")
disp.begin()
# Clear display.
disp.clear()
disp.display()
#Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
#print("draw Image")
# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)
# Draw some shapes.
padding = 2
shape_width = 20
top = padding
bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
x = padding
    # Load default font.
font = ImageFont.load_default() #Load font
fall = False #set default flag for
while True:
    #beep_off()
    #print("Fall")
    data, addr = sock.recvfrom(1026) #recv message from client,buffersize is 1026
    position = data.decode('ascii') #decode using ascii
    print("Fall")
    if position == "FALL": #check if is FALL
        fall = True  #set fall to True
    if fall == True:  #if condition to check if fall is true
        alert_user()
        fall = False
    


