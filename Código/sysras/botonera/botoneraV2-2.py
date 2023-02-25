
"""Simple gamepad/joystick test example."""

import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database

import inputs
import os

import threading

from datetime import datetime, timedelta

import pygame

import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time
import wave
from gtts import gTTS
from playsound import playsound

NombreArchivo = "sonido_Generado.mp3"

import pyttsx3

EVENT_ABB = (
    # PiHUT SNES style controller buttons
    ('Key-BTN_TRIGGER', 'N'),
    ('Key-BTN_THUMB', 'E'),
    ('Key-BTN_THUMB2', 'S'),
    ('Key-BTN_TOP', 'W')
)


# This is to reduce noise from the PlayStation controllers
# For the Xbox controller, you can set this to 0
MIN_ABS_DIFFERENCE = 5

db = Database();
conexion = db.getConexion();

class JSTest(object):
    """Simple joystick test class."""
    def __init__(self, gamepad=None, abbrevs=EVENT_ABB):
        self.btn_state = {}
        self.old_btn_state = {}
        self.abs_state = {}
        self.old_abs_state = {}
        self.abbrevs = dict(abbrevs)
        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.abs_state[value] = 0
                self.old_abs_state[value] = 0
            if key.startswith('Key'):
                self.btn_state[value] = 0
                self.old_btn_state[value] = 0
        self._other = 0
        self.gamepad = gamepad
        if not gamepad:
            self._get_gamepad()

    def _get_gamepad(self):
        """Get a gamepad object."""
        try:
            self.gamepad = inputs.devices.gamepads[0]
        except IndexError:
            raise inputs.UnpluggedError("No gamepad found.")

    def handle_unknown_event(self, event, key):
        """Deal with unknown events."""
        if event.ev_type == 'Key':
            new_abbv = 'B' + str(self._other)
            self.btn_state[new_abbv] = 0
            self.old_btn_state[new_abbv] = 0
        elif event.ev_type == 'Absolute':
            new_abbv = 'A' + str(self._other)
            self.abs_state[new_abbv] = 0
            self.old_abs_state[new_abbv] = 0
        else:
            return None

        self.abbrevs[key] = new_abbv
        self._other += 1

        return self.abbrevs[key]

    def process_event(self, event):
        """Process the event into a state."""
        if event.ev_type == 'Sync':
            return
        if event.ev_type == 'Misc':
            return
        key = event.ev_type + '-' + event.code
        try:
            abbv = self.abbrevs[key]
        except KeyError:
            abbv = self.handle_unknown_event(event, key)
            if not abbv:
                return
        BotonPresionado=""
        
        if event.ev_type == 'Key' and abbv == "N" and event.state == 1:
            print("N")
            cursor=conexion.cursor()
            cursor.execute("SELECT idNot FROM notificacion where confirmaLocalNot = False order by fCreacionNot limit 1 ")
            idNotificacion =0
            for base in cursor:
                #print(str(base))
                idNotificacion = base[0]

            if idNotificacion !=0:
                query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                
                cursor.execute(query)
                conexion.commit()
                self.habla(-1)             
            else:
                self.habla(0)
            
        if event.ev_type == 'Key' and abbv == "E" and event.state == 1:
            print("E")
            #cmd = 'espeak -ves+f5 -p0 -s0 "Repetir" --stdout | aplay'
            #os.system(cmd)

            cursor=conexion.cursor()
            cursor.execute("SELECT n.idNot, v.placaVe FROM notificacion as n join vehiculo as v on n.idVeNot = v.idVe order by n.fCreacionNot desc limit 1 ")
            Notificacion =""
            for base in cursor:
                print(str(base))
                Notificacion = base[0]
                plac=base[1]
                print(Notificacion)
            if Notificacion !="":
                self.habla(Notificacion)
                self.hablaDireccion(Notificacion)
                self.habla(plac)
            else: 
                self.habla(-2)

            conexion.commit()
 
            
        if event.ev_type == 'Key' and abbv == "S" and event.state == 1:
            print("S")
            cursor=conexion.cursor()
            cursor.execute("SELECT mensajeNot FROM notificacion where confirmaLocalNot = False order by fCreacionNot limit 1 ")
            Notificacion =""
            for base in cursor:
                print(str(base))
                Notificacion = base[0]
        
            BotonPresionado="Repetir notificaciones de las últimas 24 horas"
            self.habla(-24)
            cursorx=conexion.cursor()
            cursorx.execute("select n.fCreacionNot, n.idNot,v.placaVe from notificacion as n join vehiculo as v on n.idVeNot = v.idVe where n.fCreacionNot between DATE_SUB(now(),INTERVAL 24 HOUR) and now()")
            Notificacion =""
            FechaHora = ""
            for base in cursorx:
                print(str(base))
                Notificacion = base[1]
                print(Notificacion)
                self.habla(Notificacion)
                self.habla(base[2])
            conexion.commit()
            

    def process_events(self):
        """Process available events."""
        try:
            events = self.gamepad.read()
        except EOFError:
            events = []
        for event in events:
            self.process_event(event)
            

    def habla(self,texto):
        print (texto)
        try:
            pygame.mixer.init(26000)
            pygame.mixer.music.load("../Audio/Reportes/"+str(texto)+".mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        except:
            print("No existe el audio")
            

    def hablaDireccion(self,texto):
        print (texto)
        try:
            pygame.mixer.init(26000)
            pygame.mixer.music.load("../Audio/Direcciones/"+str(texto)+".mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        except:
            print("No existe el audio")
            
            
def main():
    """Process all events forever."""
    jstest = JSTest()
    while 1:
        jstest.process_events()


if __name__ == "__main__":
    main()
