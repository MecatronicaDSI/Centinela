from pynput import mouse

import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database


import mysql.connector
import time
from gtts import gTTS
from playsound import playsound
import pygame

db = Database()
conexion = db.getConexion()

def __init__(self):
    print("Iniciando botonera")

    
def habla(texto):
    print (texto)
    print("habla")
    try:
        tts= gTTS(texto,lang='es')
        tts.save("../Confirmada1.mp3")
        print("Guardado")
        # tts.save("C:/Users/Desarrollo/Documents/productoscaciv/centinela pro 2.4/sysras/Audio/Notificacion.mp3")
        pygame.mixer.init(26000)
        pygame.mixer.music.load("../Confirmada1.mp3")
        # pygame.mixer.music.load("C:/Users/Desarrollo/Documents/productoscaciv/centinela pro 2.4/sysras/Audio/Notificacion.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue
    except:
        print("No existe el audio")

#def main(self)
# The event listener will be running in this block
print("!")
with mouse.Events() as events:
    for event in events:
        try:
            if event.button == mouse.Button.right:
                print('Received event {}'.format(event))
                print('---')
                print('Presionado s')
                
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
                    #print(idNotificac





ion)
                    
                if idNotificacion  > 0:
                    print(usuario)
                    if(vehiculo != None):
                        query="SELECT idVe,placaVe FROM vehiculo WHERE idVe = "+str(vehiculo)
                        cursor.execute(query)
                        for base in cursor:
                            #print(str(base))
                                print ("AQUI se envia")
##                                            datos="7CON~"+str(base[1] + "~" + placa)
##                                            client.publish('/pp',payload=datos , qos=0, retain=False)
                            
                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                        cursor.execute(query)
                    if(usuario != None):
                        query="SELECT idUsr,identificadorUsr FROM usuario WHERE idUsr = "+str(usuario)
                        cursor.execute(query)
                        for base in cursor:
                                print ("AQUI se envia")
##                                            datos="7CON~"+str(base[1] + "~" + placa)
##                                            client.publish('/pp',payload=datos , qos=0, retain=False)
                            
                        query="update notificacion set confirmaLocalNot = True where idNot = "+str(idNotificacion)
                        cursor.execute(query)
                        conexion.commit()
                        print("1")
                        habla("Notificación recibida y confirmada  " + mensaje)             
                else:
                    cursor.execute("SELECT idNot, mensajeNot FROM notificacion where confirmaLocalNot = True order by fCreacionNot limit 1 ")
                    for base in cursor:
                        #print(str(base))
                        idNotificacion = base[0]
                        mensaje = base[1]
                        habla("La notificación ya fue confirmada " + mensaje)
                                     
                        
            else:
                print('Received event {}'.format(event))
        
        except Exception as e:
             print (e)
        
