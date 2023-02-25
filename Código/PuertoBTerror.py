import subprocess, shlex
import serial
import time
comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
args=shlex.split(comando1)
p=subprocess.run(args,capture_output=True, text=True)
print(p.stdout)
print(p.stderr)
print("dddd")
msj="Recbido"

try:
    port=serial.Serial("/dev/rfcomm0",timeout=1)
    estPuerto=port.isOpen()
    #while port.name== "/dev/rfcomm0":
    print ("Estado de puerto: " + str(port.isOpen()))
    while True:
        port.write(msj.encode())
        time.sleep(1)
        rcv = port.read(1)
        print(rcv)
        if rcv == b'1':
            print("Boton 1 presionado")
        elif rcv == b'2':
            print("Boton 2 presionado")
        elif rcv == b'3':
            print("Boton 3 presionado")
        elif rcv == b'4':
            print("Boton 4 presionado")        
    else:
        print("se ha desconectado botonera")
except Exception as e:
    print("Puerto COM no disponible")
