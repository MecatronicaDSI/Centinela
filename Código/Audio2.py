import threading
import time
import logging
from threading import Thread

from gtts import gTTS
import os
from playsound import playsound
import pygame


import mysql.connector


NombreArchivo = "sonido_Generado.mp3"

class Audio:
    def __init__(self):  #Se ejecuta cada vez que se ejecuta la clase
        self.fileNoti = "Notificacion.mp3" 
        self.fileRep = "Repeticion.mp3" 
        self.arrayMensaje = []
        print ("Mi clase")

   

    def procesarMensaje(self,mensaje):
        print(mensaje)
        arrayMensaje = mensaje.split("~")

        if arrayMensaje[0]=="1CENT":

            conexionz=mysql.connector.connect(host="localhost", user="sysras", passwd="sysras2020",db="sysras_cent")
            #conexionz=mysql.connector.connect(host="localhost", user="root", passwd="root",db="sysras_cent")
            cursorz=conexionz.cursor()
        

            tipoRegistroVe = 0
            notificacion = ""
            if arrayMensaje[1] == "Uber":
                notificacion = "Se Reporta una "+arrayMensaje[2]+" en un vehículo  privado Uber " + arrayMensaje[4] + " " + arrayMensaje[5] + " Color " + arrayMensaje[7] + " con placas " + arrayMensaje[3]
                query = "SELECT idVe FROM vehiculo WHERE placaVe = '" + str(arrayMensaje[3]) + "'"
                tipoRegistroVe = 2
            elif arrayMensaje[1]== "UberRobo":
                notificacion = "Se Reporta un posible robo en un vehículo privado Uber " + arrayMensaje[4] + " " + arrayMensaje[5] + " Color " + arrayMensaje[7] + " con placas " + arrayMensaje[3]
                query = "SELECT idVe FROM vehiculo WHERE placaVe = '" + str(arrayMensaje[3]) + "'"
                tipoRegistroVe = 2
            elif arrayMensaje[1] == "UberGenero":
                notificacion = "Se Reporta un posible robo/violencia de género en un vehículo privado Uber  " + arrayMensaje[4] + " " + arrayMensaje[5] + " Color " + arrayMensaje[7] + " con placas " + arrayMensaje[3]
                query = "SELECT idVe FROM vehiculo WHERE placaVe = '" + str(arrayMensaje[3]) + "'"
                tipoRegistroVe = 2
            elif arrayMensaje[1]== "AppRobo":
                notificacion = "Se Reporta un posible robo a ciudadano, activación de alerta desde Aplicación"
                query = "SELECT idUsr FROM usuario WHERE identificadorUsr = '" + str(arrayMensaje[3]) + "'"
            elif arrayMensaje[1] == "AppGenero":
                notificacion = "Se Reporta un posible robo ó violencia de género, activación de alerta desde Aplicación"
                query = "SELECT idUsr FROM usuario WHERE identificadorUsr = '" + str(arrayMensaje[3]) + "'"
            else:
                notificacion = "Se Reporta un "+arrayMensaje[2]+" en un vehículo " + arrayMensaje[4] + " " + arrayMensaje[5] + " Color " + arrayMensaje[7] + " con placas " + arrayMensaje[3]
                query = "SELECT idVe FROM vehiculo WHERE placaVe = '" + str(arrayMensaje[3]) + "'"
                tipoRegistroVe = 1
                
                
                ## Caso si es desde App
            if arrayMensaje[1]== "AppRobo" or arrayMensaje[1] == "AppGenero":
                cursorz.execute(query)

                registro1 = cursorz.fetchall()
                    
                idUsr = 0
                if registro1: #Si ya hay un registro de esa placa evita el duplicado, esto porque desde los navegadores se envian los socket 1y se duplicaba el mismo caso
                    print(registro1)
                    for baseVe in registro1:
                        idUsr = baseVe[0]
                else:
                    print("Nuevo Usuario....")
                    query2="INSERT INTO usuario (identificadorUsr) VALUES ("+ arrayMensaje[3] +")"
                    cursorz.execute(query2)

                    cursorz.execute("SELECT idUsr FROM usuario WHERE identificadorUsr = " + arrayMensaje[3])
                    for baseVe in cursorz:
                        idUsr = baseVe[0]
                    
                print(idUsr)

                cursorz.execute("SELECT * FROM notificacion WHERE fCreacionNot > DATE_SUB(now(), INTERVAL 1 HOUR) AND idUsrNot = " + str(idUsr))  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                registro = cursorz.fetchall()
                if registro: #Si ya hay un registro de esa placa evita el duplicado, esto porque desde los navegadores se envian los socket 1y se duplicaba el mismo caso
                    print("Ya hay registro")
                else:
                    print("Registrando..")
                    query="INSERT INTO notificacion (mensajeNot, fCreacionNot,idUsrNot) VALUES (%s,now(), %s)"
                    values = (notificacion, idUsr)
                    cursorz.execute(query, values)
                    hilo = Thread(target=self.hablaV, args=(notificacion,))
                    hilo.start()
                    #self.hablaV(notificacion)

            else:
                cursorz.execute(query)

                registro1 = cursorz.fetchall()
                    
                idVe = 0
                if registro1: #Si ya hay un registro de esa placa evita el duplicado, esto porque desde los navegadores se envian los socket 1y se duplicaba el mismo caso
                    print(registro1)
                    for baseVe in registro1:
                        idVe = baseVe[0]
                else:
                    print("Nuevo Vehiculo....")
                    query2="INSERT INTO vehiculo (placaVe,estadoVe,estatusVe,tipoVe,marcaVe,modeloVe,anioVe,colorVe,tipoRegistroVe) VALUES (%s, %s, 1, %s, %s, %s, %s, %s, %s)"
                    val2=(arrayMensaje[3],arrayMensaje[9],arrayMensaje[8],arrayMensaje[4],arrayMensaje[5],arrayMensaje[6],arrayMensaje[7],tipoRegistroVe)
                    cursorz.execute(query2,val2)
                    
                    query3 = "SELECT idVe FROM vehiculo WHERE placaVe = '" + arrayMensaje[3] + "'"
                    print(query3)
                    cursorz.execute(query3)
                    print(cursorz)
                    for baseVe in cursorz:
                        idVe = baseVe[0]


                print(idVe)
                cursorz.execute("SELECT * FROM notificacion WHERE fCreacionNot > DATE_SUB(now(), INTERVAL 1 HOUR) AND idVeNot = " + str(idVe))  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                registro = cursorz.fetchall()
                print ("registro")
                print (registro)
                if registro: #Si ya hay un registro de esa placa evita el duplicado, esto porque desde los navegadores se envian los socket 1y se duplicaba el mismo caso
                    print("Ya hay registro")
                else:
                    print("Registrando..")
                    query="INSERT INTO notificacion (mensajeNot, fCreacionNot,idVeNot) VALUES ('" + notificacion + "',now(), " + str(idVe) + ")"
                    cursorz.execute(query)
                    hilo = Thread(target=self.hablaV, args=(notificacion,))
                    hilo.start()
                    #self.hablaV(notificacion)
            

            conexionz.commit()
            cursorz.close()
            conexionz.close()
            
        if arrayMensaje[0]=="1UB":
            conexionx=mysql.connector.connect(host="localhost", user="sysras", passwd="sysras2020",db="sysras_cent")
            #conexionx=mysql.connector.connect(host="localhost", user="root", passwd="root",db="sysras_cent")
            cursorx=conexionx.cursor()
            cursory=conexionx.cursor()
            notificacion = ""
            
            if arrayMensaje[2] == "BPP":
                notificacion = "Vehículo con placas " + arrayMensaje[4] + " reportado en " + arrayMensaje[1]
                cursorx.execute("SELECT Max(idNot) FROM notificacion as n join vehiculo as v on n.idVeNot = v.idVe where v.placaVe = '" + arrayMensaje[4] + "'")
            elif arrayMensaje[2] == "TPLUBER":
                notificacion = "Vehículo con placas " + arrayMensaje[4] + " reportado en " + arrayMensaje[1]
                cursorx.execute("SELECT Max(idNot) FROM notificacion as n join vehiculo as v on n.idVeNot = v.idVe where v.placaVe = '" + arrayMensaje[4] + "'")
            elif arrayMensaje[2]== "APPSEGURIDAD":
                notificacion = "Ciudadano ha reportado posible acto delictivo en " + arrayMensaje[1]
                cursorx.execute("SELECT Max(idNot) FROM notificacion as n join usuario as u on n.idUsrNot = u.idUsr where u.identificadorUsr = '" + arrayMensaje[4] + "'")
            else:
                notificacion = "Vehículo con placas " + arrayMensaje[4] + " reportado en " + arrayMensaje[1]
                cursorx.execute("SELECT Max(idNot) FROM notificacion as n join vehiculo as v on n.idVeNot = v.idVe where v.placaVe = '" + arrayMensaje[4] + "'")
                
            idNot = 0
            for base in cursorx:
                idNot = base[0]
            
            cursorx.execute("SELECT * FROM notificaciondireccion WHERE fCreacionDir > DATE_SUB(now(), INTERVAL 1 HOUR) AND idNotDir = " + str(idNot))  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
            registro = cursorx.fetchall()
            if registro: #Si ya hay un registro de esa placa evita el duplicado, esto porque desde los navegadores se envian los socket 1y se duplicaba el mismo caso
                print("Ya hay registro")
            else:
                print("Registrando..")
                query2="INSERT INTO notificaciondireccion (mensajeDir,fCreacionDir,idNotDir) VALUES ('" + notificacion + "',now()," + str(idNot) + ")"
                cursorx.execute(query2)
                time.sleep(3.5)
                hilo = Thread(target=self.hablaDir, args=(notificacion,))
                hilo.start()
                #self.hablaDir(notificacion)

            conexionx.commit()
            cursorx.close()
            conexionx.close()

        if arrayMensaje[0]=="5LC":
            numeroPlaca = arrayMensaje[1]
            conexionx=mysql.connector.connect(host="localhost", user="sysras", passwd="sysras2020",db="sysras_cent")
            cursorx=conexionx.cursor()
            cursory=conexionx.cursor()
            
            if arrayMensaje[2] == "0":
                idVe = 0
                idNot = 0
                cursorx.execute("SELECT idVe FROM vehiculo WHERE placaVe = '" + numeroPlaca + "'")  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                for base in cursorx:
                    idVe = base[0]
                
                cursorx.execute("SELECT idNot FROM notificacion WHERE fCreacionNot > DATE_SUB(now(), INTERVAL 1 HOUR) AND idVeNot= " + str(idVe))  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                for base in cursorx:
                    idNot = base[0]
                    
                cursory.execute("DELETE FROM notificaciondireccion WHERE idNotDir = "  + str(idNot))
                cursory.execute("DELETE FROM notificacion WHERE idNot = "  + str(idNot))

            elif arrayMensaje[2] == "1":
                idVe = 0
                idNot = 0
                cursorx.execute("SELECT idUsr FROM usuario WHERE identificadorUsr = '" + numeroPlaca + "'")  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                for base in cursorx:
                    idVe = base[0]
                
                cursorx.execute("SELECT idNot FROM notificacion WHERE fCreacionNot > DATE_SUB(now(), INTERVAL 1 HOUR) AND idUsrNot= " + str(idVe))  #Busqueda de placa para saber si ya paso un socket "1" y lo registro
                for base in cursorx:
                    idNot = base[0]

                print(idVe)
                    
                cursory.execute("DELETE FROM notificaciondireccion WHERE idNotDir = "  + str(idNot))
                cursory.execute("DELETE FROM notificacion WHERE idNot = "  + str(idNot))
            conexionx.commit()
            cursorx.close()
            cursory.close()
            conexionx.close()


    def hablaV(self,texto):
            tts= gTTS(texto,lang='es')
            tts.save("/home/pi/sysras/WS/Audios/Notificacion.mp3")
            pygame.mixer.init(26000)
            pygame.mixer.music.load("/home/pi/sysras/WS/Audios/Notificacion.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

    def hablaDir(self,texto):
            tts= gTTS(texto,lang='es')
            tts.save("/home/pi/sysras/WS/Audios/Direccion.mp3")
            pygame.mixer.init(26000)
            pygame.mixer.music.load("/home/pi/sysras/WS/Audios/Direccion.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue
