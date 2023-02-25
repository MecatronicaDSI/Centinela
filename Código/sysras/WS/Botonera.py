#!/usr/bin/python
import sys
import subprocess, shlex
sys.path.append("/home/pi/sysras/conexion")
from database import Database
import serial
import mysql.connector
import time
from evdev import InputDevice, categorize, ecodes
from gtts import gTTS
from playsound import playsound
import pygame

import sys
import subprocess, shlex

#comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
#args=shlex.split(comando1)
#subprocess.call(args)

db = Database()
conexion = db.getConexion()
#port=serial.Serial("/dev/rfcomm0", baudrate=9600)
T_boton=1
Placa="PT2097"



    
class Botonera:
    def __init__(self):
        self.datosc=""
        print("iniciando botonera")
        self.habla("iniciando botonera")
    def folio(self, F_activo):
        print("Funcion .------. folio")
        print(F_activo)
        print("Funcion .------.")
        MenFolio=F_activo
        MenFolio2=MenFolio.split("~",2)
        MenFolio3=MenFolio2[1]
        print("SEPARADO.------.")
        print(MenFolio3)
        print("SEPARADO.------.")
        MenFolio4=str(MenFolio3[5:8])
        conexionNU=mysql.connector.connect(host="localhost", user="sysras", passwd="sysras2020",db="sysras_cent")
        cursorNU=conexionNU.cursor()
        cursorNU.execute("INSERT INTO Folios (IdFolio,Fcreac) VALUES ('"+ MenFolio4 +"', now())")
        conexionNU.commit()
    def habla(self,texto):
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
        try:
            port=serial.Serial("/dev/rfcomm0", baudrate=9600)
            while True:
                rcv = port.read(1)
                print(rcv)
                if rcv == b'1':
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
                        cursor.execute("SELECT idNot, mensajeNot, fCreacionNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
                        for base in cursor:
                            idNotificacion = base[0]
                            mensaje = base[1]
                        
                            self.habla("La notificación ya fue confirmada " + mensaje)
                    self.habla("Fin de notificación")
                elif rcv == b'2':
                    self.habla("Notificaciones de lasúltimas 24 horas")
                    cursorx=conexion.cursor()
                    cursorx.execute("SELECT idNot, mensajeNot FROM notificacion WHERE fCreacionNot between DATE_SUB(now(),INTERVAL 24 HOUR) and now()")
                    Notificacion=""
                    FechaHora=""
                    for base in cursorx:
                        #print(str(base))
                        Notificacion= base[1]
                        #print(Notificacion)
                        self.habla(Notificacion)
                    self.habla("Fin de notificaciones")
                    conexion.commit()
                elif rcv == b'3':
                    self.habla("Última notificación")
                    cursorx=conexion.cursor()
                    cursorx.execute("SELECT idNot, mensajeNot FROM notificacion ORDER BY fCreacionNot DESC LIMIT 1;")
                    Notificacion =""
                    FechaHora = ""
                    for base in cursorx:
                        #print(str(base))
                        Notificacion = base[1]
                        #print(Notificacion)
                        self.habla(Notificacion)
                    self.habla("Fin de notificación")
                    conexion.commit()
                elif rcv == b'4':
                    print(".-.-.-.-.-.-.-.-.-.-.-")
                    cursorx=conexion.cursor()
                    cursorx.execute("SELECT IdFolio,Fcreac FROM Folios ORDER BY Fcreac DESC LIMIT 1;")
                    Notificacion =""
                    for base in cursorx:
                        #print(str(base))
                        Notificacion = base[0]
                        #print(Notificacion)
                        self.habla("El folio de la última persecución activa es:  " + Notificacion)
                    self.habla("Fin de notificación")
                    conexion.commit()
        except Exception as e:
            #comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
            #args=shlex.split(comando1)
            #subprocess.call(args)
            self.habla("Error en botonera")
            
    
    def variable(self):
        return self.datosc
    def resetV(self):
        self.datosc=""

