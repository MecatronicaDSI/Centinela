#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO
from gtts import gTTS
from playsound import playsound
import pygame
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.IN)
GPIO.setwarnings(False)

def readVoltage(bus):

     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = swapped * 1.25 /1000/16
     return voltage


def readCapacity(bus):

     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256
     if capacity > 100:
        capacity = 100
     return capacity

def apagarSoft(motivo):
     print (motivo)
     print ("Centinela se apagará en 5 segundos")
     time.sleep(5)
     GPIO.output(13, GPIO.HIGH)
     time.sleep(3)
     GPIO.output(13, GPIO.LOW)

def TextoVoz(mensaje):
     fileTexto= "texto.mp3"
     tts=gTTS(mensaje,lang='es', tld="us")
     tts.save("/home/pi/sysras/WS/Audios/texto.mp3")
     pygame.mixer.init(26000)
     pygame.mixer.music.load("/home/pi/sysras/WS/Audios/texto.mp3")
     pygame.mixer.music.play()
     while pygame.mixer.music.get_busy() == True:
          continue
bus = smbus.SMBus(1)

while True:
     print ("******************")
     print ("Voltaje:%5.2fV" % readVoltage(bus))
     print ("Bateria:%5i%%" % readCapacity(bus))
     if readCapacity(bus) >= 100:
          print ("Bateria LLENA")
     if readCapacity(bus) < 20:
          print ("Bateria BAJA")
     if readVoltage(bus) < 3.00:
          apagarSoft("SIN BATERÍA")
     if GPIO.input(6)== True:
          TextoVoz("Apagando centinela")
          apagarSoft("SIN ALIMENTACIÓN")
     time.sleep(2)
