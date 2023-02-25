# Sixfab - Reading GPS data with Python
# 2020
#Centinela v2.0


from time import sleep
import serial
import os
import sys


class GPSClient:

    def __init__(self):
        self.portwrite = "/dev/ttyUSB2"
        self.port = "/dev/ttyUSB1"
        self.latitudGbl = "0.00"
        self.longitudGbl = "0.00"
##        print("Connecting Port..")
        try:
            self.serw = serial.Serial(self.portwrite, baudrate = 115200, timeout = 2.5,rtscts=True, dsrdtr=True)
            self.serw.write('AT+QGPS=1\r'.encode())
            self.serw.close()
            sleep(1)
        except Exception as e: 
##            print("Serial port connection failed.")
            print(e)

##        print("Receiving GPS data\n")
        self.ser = serial.Serial(self.port, baudrate = 115200, timeout = 2,rtscts=True, dsrdtr=True)



    def parseGPS(self, data):
##        print(data, end='') #prints raw data
        if data[0:6] == "$GPRMC":
            sdata = data.split(",")
            if sdata[2] == 'V':
##                print("\nNo satellite data available.\n")
                self.latitudGbl = "0.00"
                self.longitudGbl = "0.00"                
                return
            print("-----Parsing GPRMC-----")
            time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
            lat = self.decode(sdata[3]) #latitude
            dirLat = sdata[4]      #latitude direction N/S
            lon = self.decode(sdata[5]) #longitute
            dirLon = sdata[6]      #longitude direction E/W
            speed = sdata[7]       #Speed in knots
            trCourse = sdata[8]    #True course
            date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6] #date
            variation = sdata[10]  #variation
            degreeChecksum = sdata[13]
            #print(degreeChecksum)
            dc = degreeChecksum.split("*")
            try:
                #print ("Escribele algo")
                degree = dc[0]        #degree
                checksum = dc[1]      #checksum

                latitud = lat.split() # parsing latitude
                longitud = lon.split() # parsing lo5ngitute

                #print (str(int(latitud[0]) + (float(latitud[2])/60)) + "~-"+str(int(longitud[0]) + (float(longitud[2])/60)))
                #guardaPosicion(lapostitud, longitud)
                #envioPosicion(latitud, longitud)
                # client.publish('/pos',payload="7~PT120~" + str(int(latitud[0]) + (float(latitud[2])/60)) + "~-"+str(int(longitud[0]) + (float(longitud[2])/60)) , qos=0, retain=False)
                # mqttcl.enviarPosicion(str(int(latitud[0]) + (float(latitud[2])/60)), str(int(longitud[0]) + (float(longitud[2])/60)))
                
                self.latitudGbl = str(int(latitud[0]) + (float(latitud[2])/60))
                self.longitudGbl =str(int(longitud[0]) + (float(longitud[2])/60))
                print(self.latitudGbl)
                print(self.longitudGbl)
                #time.seelp(2)
            except Exception as e:
                print(e)
                print("Fallo al procesar los datos enviados del GPS")

            
    
    def decode(self, coord):
    ##    Converts DDDMM.MMMMM -> DD deg MM.MMMMM min
        x = coord.split(".")
        head = x[0]
        tail = x[1]
        deg = head[0:-2]
        min = head[-2:]
        return deg + " deg " + min + "." + tail + " min"


    def main(self):
        
        try:
            data = self.ser.readline().decode('utf-8')
            self.parseGPS(data)
                    
        except Exception as e:
            print("Error en datos gps")
            print(e)
            
            
            
    


