 #v3.1

from time import sleep
import sys
import subprocess, shlex
sys.path.append("home/pi/sysras/WS")
from Audio import Audio
from GPS import GPSClient
from Botonera import Botonera
import serial
import threading
import time
import logging
from threading import Thread
##port=serial.Serial("/dev/rfcomm0", baudrate=9600)
audios = Audio()
gps = GPSClient()
botonera = Botonera()
connected=True

import paho.mqtt.client as mqtt



global estado
estado=True
placa="PT2097"
username="PT"
contraseña=""
class MqttCliente:
    

    def __init__(self):
        self.numCentinela=placa
        self.client = mqtt.Client(self.numCentinela)
        

##        self.client = self.client.connect("caciv.ddns.net", 1883, 60)

    def on_connect(self,client, userdata, flags, rc):
        if rc==0:
            print("Conectado")
            global connected
            connected=True
        else:
            print("Desconectado")
            
        print(f"Connected with result code {rc}")
        # subscribe, which need to put into on_connect
        # if reconnect after losing the connection with the broker, it will continue to subscribe to the raspberry/topic topic
        self.client.subscribe("/notCent")
        
        self.enviarMensaje("Patrulla conectada")

    # the callback function, it will be triggered when receiving messages
    def on_message(self,client, userdata, msg):
        print(str(userdata))
        #print(repr(msg))
        print("Mensaje---------")
        print(str(msg.payload))
        mensaje=str(msg.payload)
        print(mensaje.find('FOLIO'))
        if mensaje.find('FOLIO') >1:
            botonera.folio(str(msg.payload))
        audios.procesarMensaje(str(msg.payload.decode("utf-8")))

    def on_disconnect(self,client, userdata, rc):
##        self.main()
        print("Desconectado")

    def enviarMensaje(self,mensaje):
        self.client.publish('/notCent',mensaje, qos=0, retain=False)
        
    def enviarPosicion(self,latitud, longitud):
        try:
            if (str(latitud) != "0.00"):
                print("Enviando....")
                self.client.publish('/pos',payload="7~" + placa + "~" + str(latitud) + "~-"+str(longitud) , qos=1, retain=False)
                
        except Exception as e:
##            self.main()
            print("Falla de publicación")

    def posicionamiento(self):
        while True:
            try:
                gps.main()
            except Exception as e: 
                print("Error en ciclo GPS")
                print(e)

    def botones(self):
        while True:
            global estado
            if estado==True:
                try:
                    print("Entrando a botonera")
                    botonera.main()
                    estado=True
                except Exception as e:
                    print("Error en ciclo Botonera")
                    print(e)
                    estado=False
            else:
                comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
                args=shlex.split(comando1)
                subprocess.call(args)
                
        
                


        
        
            

    def main(self):
        self.client = mqtt.Client(self.numCentinela)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(username, contraseña)
        self.client.on_disconnect = self.on_disconnect
        # set the will message, when the Raspberry Pi is powered off, or the network is interrupted abnormally, it will send the will message to other clients
        self.client.will_set('raspberry/status', b'{"status": "Off"}')

        # create connection, the three parameters are broker address, broker port number, and keep-alive time respectively
        self.client.connect("caciv.ddns.net", 1883, keepalive=30)

        hilo = Thread(target=self.posicionamiento, args=())
        hilo.start()

        hilo2 = Thread(target=self.botones, args=())
        hilo2.start()
        
        while True:
            #print(ser)
            try:
##                gps.main()
                sleep(1)
                mensaje=botonera.variable()
                if mensaje != "":
                    self.client.publish('/mqtt',payload=mensaje , qos=0, retain=False)
                    botonera.resetV()
                self.enviarPosicion(gps.latitudGbl, gps.longitudGbl)
                self.client.loop_start()
            except Exception as e: 
                print("Error en ciclo")
                print(e)
                
            
        self.client.loop_start()
        

mqttcl = MqttCliente()
mqttcl.main()




