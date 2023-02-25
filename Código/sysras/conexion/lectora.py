import socket
import sys
from datetime import date, datetime


class Lectora:
    
    def __init__(self):
        self.PORT = 10001
        self.HOST = "192.168.0.100"
        self.server_address = (self.HOST,self.PORT)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def getConexion(self):
        try:
            conn = self.sock.connect(self.server_address)
            print("conexion exitosa al socket")
            
        except Exception as e:
            print("Error de conexion", e)
        
        return conn
    
    def mensajeServer(self):
        mensaje = self.sock.recv(1024)
        #print(mensaje)
        return mensaje
    
    def getDesconexion(self):
        try:
            diss = self.sock.close()
            print("desconexion exitosa")
        
        except: 
            print("No se ha desconectado")
        
        return diss
