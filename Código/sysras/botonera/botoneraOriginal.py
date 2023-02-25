
#import sys
#sys.path.append("/home/pi/sysras/conexion")

#from database import Database

#import mysql.connector
#import time
from evdev import InputDevice, categorize, ecodes
from gtts import gTTS
from playsound import playsound
import pygame

A = InputDevice('/dev/input/event0')


EV_VAL_PRESSED = 1
EV_VAL_RELEASED = 0
BTN_SHUTTER = 31
d = 32
f = 33

class Botonera:

        def habla(texto):
                print (texto)
                try:
                    tts= gTTS(texto,lang='es')
                    tts.save("../Confirmada.mp3")
                    print("Guardado")
                    # tts.save("C:/Users/Desarrollo/Documents/productoscaciv/centinela pro 2.4/sysras/Audio/Notificacion.mp3")
                    pygame.mixer.init(26000)
                    pygame.mixer.music.load("../Confirmada.mp3")
                    # pygame.mixer.music.load("C:/Users/Desarrollo/Documents/productoscaciv/centinela pro 2.4/sysras/Audio/Notificacion.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() == True:
                        continue
                except:
                    print("No existe el audio")

                    

        for event in A.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value==EV_VAL_PRESSED:
                    if event.code == BTN_SHUTTER:
                        print('---')
                        print('Presionado s')
                        print(event)
                        habla('Hola jelipon')
                        

                        
                    elif event.code == d:
                        print('---')
                        print('Presionado d')
                        print(event)

                    elif event.code == f:
                        print('---')
                        print('Presionado f')
                        print(event)
