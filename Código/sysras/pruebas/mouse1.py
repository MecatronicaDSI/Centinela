
import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database

import mysql.connector
import time
from evdev import InputDevice, categorize, ecodes
from gtts import gTTS
from playsound import playsound
import pygame

db = Database()
conexion = db.getConexion()

A = InputDevice('/dev/input/event1')

EV_VAL_PRESSED = 1
EV_VAL_RELEASED = 0
BTN_LEFT=272
BTN_RIGHT=273
BTN_MIDDLE=274
c=0
d=0
e=0
f=0
g=0
                                    
def valores():
    global c
    global d
    global e
    global f
    global g
    
    if c == 2:
        print("2 L")
        print("")
        c = 0

    elif c == 1:
        print("1 L")
        print("")
        c = 0
        
    elif d == 2:
        print("R")
        print("")
        d = 0
        
    elif e == 2:
        print("M")
        print("")
        e = 0
        
    elif f == 2:
        print("S")
        print("")
        f = 0
        
    elif g == 2:
        print("E")
        print("")
        g = 0
        
def contador():
    for event in A.read_loop():
                        if event.type == ecodes.EV_KEY:
                            if event.value==EV_VAL_PRESSED:
                                if event.code == BTN_LEFT:
                                    print("BOTON DERECHO")
                                    print("")
                                    global c
                                    c = c + 1
                                    time.sleep(15)
                                    if event.code == BTN_LEFT:
                                        print("BOTON DERECHO")
                                        print("")
                                        c = c + 1
                                        
                                elif event.code == BTN_RIGHT:
                                    print('Presionado R')
                                    print("")
                                    global d
                                    d = d + 1
                                elif event.code == BTN_MIDDLE:
                                    print('Presionado M')
                                    print("")
                                    global e
                                    e = e + 1
                                elif event.code == BTN_SIDE:
                                    print('Presionado S')
                                    print("")
                                    global f
                                    f = f + 1
                                elif event.code == BTN_EXTRA:
                                    print('Presionado E')
                                    print("")
                                    global g
                                    g = g + 1
                                valores()
                                

        
while True:
    contador()
