import subprocess, shlex
import serial
import time
comando1='sudo rfcomm connect hci 94:E6:86:DA:EA:6A'
args=shlex.split(comando1)
subprocess.call(args)
msj="Recbido"
port=serial.Serial("/dev/rfcomm0")
#while port.name== "/dev/rfcomm0":
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
