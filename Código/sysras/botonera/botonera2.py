
import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database

import mysql.connector
import time


##from pynput import keyboard as kb
from pynput import keyboard

from gtts import gTTS
from playsound import playsound
import pygame
import paho.mqtt.client as mqtt


db = Database()
conexion = db.getConexion()

fecha = str(time.strftime("%d%m%y"))

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

def pulsa(tecla):
    print("Vuelta...")
    print(tecla)

    if str(tecla)== '"s"': #Confirmar última notificación
        print("letra s")
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
            
        if idNotificacion !=0:
            print(usuario)
            if(vehiculo != None):
                query="SELECT idVe,placaVe FROM vehiculo WHERE idVe = "+str(vehiculo)
                cursor.execute(query)
                for base in cursor:
                    #print(str(base))
                    datos="7CON~"+str(base[1] + "~" + placa)
                    client.publish('/pp',payload=datos , qos=0, retain=False)
                    
                query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                cursor.execute(query)
            if(usuario != None):
                query="SELECT idUsr,identificadorUsr FROM usuario WHERE idUsr = "+str(usuario)
                cursor.execute(query)
                for base in cursor:
                    datos="7CON~"+str(base[1] + "~" + placa)
                    client.publish('/pp',payload=datos , qos=0, retain=False)
                    
                query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                cursor.execute(query)
            conexion.commit()
            print("1")
            habla("Notificacion confirmada" + mensaje)             
        else:
            cursor.execute("SELECT idNot, mensajeNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
            for base in cursor:
                #print(str(base))
                idNotificacion = base[0]
                mensaje = base[1]
                habla("Ya fue notificada " + mensaje)

    if str(tecla)== "'d'":  #Ultima notificación
        print("letra d")
        cursor=conexion.cursor()
        cursor.execute("SELECT idNot, mensajeNot FROM notificacion ORDER BY fCreacionNot DESC LIMIT 1 ;")
        Notificacion =""
        print(cursor)
        for base in cursor:
            print(str(base))
            Notificacion = base[1]
            habla(Notificacion)
        

        conexion.commit()

    if str(tecla)== "f": ##Notificaciones de las últimas 24 horas
        
        cursorx=conexion.cursor()
        cursorx.execute("SELECT idNot, mensajeNot FROM notificacion WHERE fCreacionNot between DATE_SUB(now(),INTERVAL 24 HOUR) and now()")
        Notificacion =""
        FechaHora = ""
        for base in cursorx:
            print(str(base))
            Notificacion = base[1]
            print(Notificacion)
            habla(Notificacion)

        conexion.commit()


    time.sleep(2)

##kb.Listener(pulsa).run()

def on_press(key):
    try:
        print('alphanumeric key {0} '.format(
            key.char))
        pulsa(key.char)
    except AttributeError:
        print('special key {0} pressed'.format(
            key))

def on_release(key):
    print('{0} released'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

listener.start()
