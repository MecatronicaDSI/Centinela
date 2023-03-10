import sys
sys.path.append("/home/pi/sysras/conexion")
import RPi.GPIO as GPIO
from database import Database
import serial
import mysql.connector
import time
from gtts import gTTS
from playsound import playsound
import pygame
db = Database()
conexion = db.getConexion()
B_izquierda=21
B_derecha=16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(B_izquierda, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(B_derecha, GPIO.IN,pull_up_down=GPIO.PUD_UP)
T_boton=1
Placa="PT2097"

    
class Botonera:
    def __init__(self):
        self.datosc=""
        print("iniciando botonera")
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
        while True:
            Cont_iz=0
            Cont_der=0
            inicio=0
            fin=0
            BTN=0
            B_iz=GPIO.input(B_izquierda)
            B_der=GPIO.input(B_derecha)
            time.sleep(0.2)
            if B_der==0:
                inicio=time.time()
                Cont_der+=1
                print(inicio)
                print("btn der")  
                while fin - inicio <T_boton:
                    fin=time.time()
                    print(fin-inicio)
                    B_der=GPIO.input(B_derecha)
                    time.sleep(0.2)
                    if B_der==0:
                        Cont_der+=1
                print("Tiempo")
                if Cont_der == 1:
                    BTN=1
                    print("Acci??n 1---DERECHA")
                    inicio=0
                    fin=0
                    Cont_der=0
                if Cont_der == 2:
                    BTN=2
                    print("Acci??n 2---DERECHA")
                    inicio=0
                    fin=0
                    Cont_der=0
            if  B_iz==0:
                inicio=time.time()
                Cont_iz+=1
                print(inicio)
                print("btn izq")
                while  fin - inicio <T_boton :
                    fin=time.time()
                    print(fin-inicio)
                    B_iz=GPIO.input(B_izquierda)
                    time.sleep(0.2)
                    if B_iz == 0:
                        Cont_iz+=1
                print("Tiempo")
                if Cont_iz==1:
                    BTN=3
                    print("Acci??n 1---IZQUIERDA")
                    inicio=0
                    fin=0
                    Cont_iz=0
                if Cont_iz==2:
                    BTN=4
                    print("Acci??n 2---IZQUIERDA")
                    inicio=0
                    fin=0
                    Cont_iz=0
                
 ##--------------------------------------------------
            if BTN==1:
                print('---')
                print('Bot??n 1 presionado')
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
                    self.habla("Notificaci??n recibida y confirmada  " + mensaje)  
                else:
                    cursor.execute("SELECT idNot, mensajeNot, fCreacionNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
                    for base in cursor:
                        idNotificacion = base[0]
                        mensaje = base[1]
                        
                        self.habla("La notificaci??n ya fue confirmada " + mensaje)
                self.habla("Fin de notificaci??n")
            elif BTN==2:
                self.habla("Notificaciones de las??ltimas 24 horas")
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
            elif BTN==3:
                self.habla("??ltima notificaci??n")
                cursorx=conexion.cursor()
                cursorx.execute("SELECT idNot, mensajeNot FROM notificacion ORDER BY fCreacionNot DESC LIMIT 1;")
                Notificacion =""
                FechaHora = ""
                for base in cursorx:
                    #print(str(base))
                    Notificacion = base[1]
                    #print(Notificacion)
                    self.habla(Notificacion)
                self.habla("Fin de notificaci??n")
                conexion.commit()
            elif BTN==4:
                print(".-.-.-.-.-.-.-.-.-.-.-")
                cursorx=conexion.cursor()
                cursorx.execute("SELECT IdFolio,Fcreac FROM Folios ORDER BY Fcreac DESC LIMIT 1;")
                Notificacion =""
                for base in cursorx:
                    #print(str(base))
                    Notificacion = base[0]
                    #print(Notificacion)
                    self.habla("El folio de la ??ltima persecuci??n activa es:  " + Notificacion)
                self.habla("Fin de notificaci??n")
                conexion.commit()
            
    
    def variable(self):
        return self.datosc
    def resetV(self):
        self.datosc=""

