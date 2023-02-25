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
                    print("Acción 1---DERECHA")
                    inicio=0
                    fin=0
                    Cont_der=0
                if Cont_der == 2:
                    BTN=2
                    print("Acción 2---DERECHA")
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
                    print("Acción 1---IZQUIERDA")
                    inicio=0
                    fin=0
                    Cont_iz=0
                if Cont_iz==2:
                    BTN=4
                    print("Acción 2---IZQUIERDA")
                    inicio=0
                    fin=0
                    Cont_iz=0
                
 ##--------------------------------------------------
            if BTN==1:
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
            elif BTN==2:
                self.datosc="BPP90~APP~HTR4854~PERSECUCION~"+Placa+"~8~"

                conexion.commit()
            elif BTN==3:
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
            elif BTN==4:
                self.habla("Dirección de última notificación")
                cursorx=conexion.cursor()
                cursorx.execute("SELECT idNotDir, mensajeDir FROM notificaciondireccion ORDER BY fCreacionDir DESC LIMIT 1;")
                Notificacion=""
                FechaHora = ""
                for base in cursorx:
                    #print(str(base))
                    Notificacion= base[1]
                    self.habla(Notificacion)
                conexion.commit()
                self.habla("Fin de notificación")
            
    
    def variable(self):
        return self.datosc
    def resetV(self):
        self.datosc=""

