
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
Placa="PT2098"

class Botonera:

        def __init__(self):
                self.datosc = ""
                print("Iniciando botonera")

        def habla(self,texto):
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

                    
        def main(self):   
                for event in A.read_loop():
                    if event.type == ecodes.EV_KEY:
                        if event.value==EV_VAL_PRESSED:
                            if event.code == BTN_LEFT:
                                print('---')
                                print('Presionado L')
                                print(event)
                                cursor=conexion.cursor()
                                cursor.execute("SELECT idNot, mensajeNot, idVeNot, idUsrNot FROM notificacion where confirmaLocalNot = False order by fCreacionNot limit 1 ")
                                idNotificacion =0
                                mensaje = ""
                                vehiculo = ""
                                usuario = ""
                                for base in cursor:
                                    #print(str(base))
                                    idNotificacion = base[0]
                                    mensaje = base[1]
                                    vehiculo=base[2]
                                    usuario = base[3]
                                    #print(idNotificacion)
                                    
                                if idNotificacion  > 0:
                                    print(usuario)
                                    if(vehiculo != None):
                                        query="SELECT idVe,placaVe FROM vehiculo WHERE idVe = "+str(vehiculo)
                                        cursor.execute(query)
                                        for base in cursor:
                                            #print(str(base))
                                                print ("AQUI se envia")
                                                self.datosc="5C~"+ Placa + "~" + str(base[1])
##                                            client.publish('/pp',payload=datos , qos=0, retain=False)
                                            
                                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                                        cursor.execute(query)
                                    if(usuario != None):
                                        query="SELECT idUsr,identificadorUsr FROM usuario WHERE idUsr = "+str(usuario)
                                        cursor.execute(query)
                                        for base in cursor:
                                                print ("AQUI se envia")
                                                self.datosc="5C~"+ Placa + "~" + str(base[0])
##                                            client.publish('/pp',payload=datos , qos=0, retain=False)
                                            
                                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                                        cursor.execute(query)
                                    conexion.commit()
                                    print("1")
                                    self.habla("Notificación recibida y confirmada  " + mensaje)             
                                else:
                                    cursor.execute("SELECT idNot, mensajeNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
                                    for base in cursor:
                                        #print(str(base))
                                        idNotificacion = base[0]
                                        mensaje = base[1]
                                        self.habla("La notificación ya fue confirmada " + mensaje)
                                             
                            elif event.code == BTN_RIGHT:
                                print('---')
                                print('Presionado R')
                                print(event)
                                cursor=conexion.cursor()
                                cursor.execute("SELECT idNot, mensajeNot FROM notificacion ORDER BY fCreacionNot DESC LIMIT 1 ;")
                                Notificacion =""
                                print(cursor)
                                for base in cursor:
                                    print(str(base))
                                    Notificacion = base[1]
                                    self.habla(Notificacion)
                                

                                conexion.commit()

                            elif event.code == BTN_MIDDLE:
                                print('---')
                                print('Presionado M')
                                print(event)
                                cursorx=conexion.cursor()
                                cursorx.execute("SELECT idNot, mensajeNot FROM notificacion WHERE fCreacionNot between DATE_SUB(now(),INTERVAL 24 HOUR) and now()")
                                Notificacion =""
                                FechaHora = ""
                                for base in cursorx:
                                    print(str(base))
                                    Notificacion = base[1]
                                    print(Notificacion)
                                    self.habla(Notificacion)

                                conexion.commit()
        def variable(self):
                return self.datosc
        
        def resetV(self):
                self.datosc = ""
                        


