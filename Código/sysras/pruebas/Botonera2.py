import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database
import serial
import mysql.connector
import time
from evdev import InputDevice, categorize, ecodes
from gtts import gTTS
from playsound import playsound
import pygame
db = Database()
conexion = db.getConexion()
port=serial.Serial("/dev/rfcomm0", baudrate=9600)

Placa="PT2097"

class Botonera:
    def __init__(self):
        self.datosc=""
        print("iniciando botonera")
    def habla(self,texto):
        print(texto)
        try:
            tts=gTTS(texto,lang='es')
            tts.save("../Confirmada.mp3")
            print("guardado")
            pygame.mixer.init(26000)
            pygame.mixer.music.load("../Confirmada.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
        except:
            print("No existe audio")
    
    def main(self):
        while True:
            rcv = port.read(10)
            if rcv == b'1111111111':
                print('---')
                print('Botón 1 presionado')
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
                            print ("AQUI se envia")
                            self.datosc="5C~"+ Placa + "~" + str(base[1])
                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                        cursor.execute(query)
                    if(usuario != None):
                        query="SELECT idUsr,identificadorUsr FROM usuario WHERE idUsr = "+str(usuario)
                        cursor.execute(query)
                        for base in cursor:
                            print ("AQUI se envia")
                            self.datosc="5C~"+ Placa + "~" + str(base[0])
                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                        cursor.execute(query)
                    conexion.commit()
                    print("1")
                    self.habla("Notificación recibida y confirmada  " + mensaje)  
                else:
                    cursor.execute("SELECT idNot, mensajeNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
                    for base in cursor:
                        idNotificacion = base[0]
                        mensaje = base[1]
                        self.habla("La notificación ya fue confirmada " + mensaje)           
            elif rcv == b'2222222222':
                print("Boton 2 presionado")
                cursorx=conexion.cursor()
                cursorx.execute("SELECT idNot, mensajeNot FROM notificacion WHERE fCreacionNot between DATE_SUB(now(),INTERVAL 24 HOUR) and now()")
                Notificacion=""
                FechaHora=""
                for base in cursorx:
                    print(str(base))
                    Notificacion= base[1]
                    print(Notificacion)
                    self.habla(Notificacion)
                conexion.commit()
            elif rcv == b'3333333333':
                print("Boton 3 presionado")
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
        self.datosc=""
