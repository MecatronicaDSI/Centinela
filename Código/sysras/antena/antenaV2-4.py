
import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database
from lectora import Lectora
import serial, time
from datetime import datetime, timedelta
import os
import socket
import mysql.connector

VERBOSE = True

lec = Lectora();
lec.getConexion();
db = Database();

contadorPasada = 1
contador = 0;
fecha = str(time.strftime("%d%m%y"))

def cuenta():
    cuenta.numero += 1
    return cuenta.numero

cuenta.numero = 0
conexion = db.getConexion()

def imprimirValor(x):
    if(len(x) > 8):
        tagH1=x[8]
        tagH1s=tagH1[1:3]
        tagH2=x[9]
        tagH2s=tagH2[1:3]
        res=int(tagH1s+tagH2s,16)
        cadena = str(res)
        if(len(cadena)!= 4):
            tagH1=x[9]
            tagH1s=tagH1[1:3]
            tagH2=x[10]
            tagH2s=tagH2[1:3]
            res=int(tagH1s+tagH2s,16)
            guardarSenso(res)
        

def guardarSenso(res):
    ArregloVR=[]
    contador = cuenta()
    hora = str(datetime.now().strftime("%H:%M:%S"))
    print(str(res)+" leido a las "+hora)
    cursor1=conexion.cursor()
    
    cursor1.execute("select * from tag where numeroTag = " + str(res))
    
    for base in cursor1:
        print("1")
        tag = base[0]
        enviado = 0
        
        if (base[3] == 1):
            print("3")
            query3 = "SELECT idTagRep FROM sensoreportado WHERE fCreacionRep > DATE_SUB(NOW(), INTERVAL 5 SECOND) AND idTagRep = " + str(tag)
            #Falta validar cuando es un botón de pánico estándar no activado se active
            cursor1.execute(query3)
            filas = cursor1.fetchall()
            print("3")
            if len(filas) == 0:
                query2="INSERT INTO sensoreportado (idTagRep,enviadoRep,fLecturaRep,fCreacionRep) VALUES (%s,%s,now(),now())"
                val2=(tag,enviado)
                cursor1.execute(query2,val2)
            
    conexion.commit()

try:
    while True:
        
        data = lec.mensajeServer();
        cadenaCompleta = str(data).split('\\')
        
        if(len(cadenaCompleta) > 1):
            primerValor = cadenaCompleta[1]
            finalValor = str(data)[-2]
            if(primerValor[0:3] == "xaa" and len(cadenaCompleta) > 2):
                if(cadenaCompleta[2][0:3] == "x0f"):    
                    if(primerValor[0:3] == "xaa" and finalValor == "D"):
                        x = str(data).split('\\',12)
                        imprimirValor(x)
                    else:
                        if(contadorPasada == 1):
                            contadorPasada = 2
                            data1 = data
            elif(primerValor[0:3] == "xaa"):
                if(contadorPasada == 1):
                    contadorPasada = 2
                    data1 = data
            elif(contadorPasada == 2):
                data2 = data
                data3 = str(data1) + str(data2)
                x = str(data3).split('\\',12)
                if(x[2][0:3] == "x0f"):
                    imprimirValor(x)
                contadorPasada = 1
        elif(cadenaCompleta[0] == "b'"):
            print(str(data) + "  - otro")
            if(contadorPasada == 1):
                contadorPasada = 2
                data1 = data
            else:
                data2 = data
                data3 = str(data1) + str(data2)
                x = str(data3).split('\\',12)
                print(str(x) + " - el 3")
                if(x[2][0:3] == "x0f"):
                    imprimirValor(x)
                contadorPasada = 1   

    contador = cuenta()
    n = 0
     
except:
    contador = cuenta()
    n = 0
    pass


    

    
