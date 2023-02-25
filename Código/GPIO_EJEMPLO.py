import RPi.GPIO as GPIO
import time
B_izquierda=21
B_derecha=16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(B_izquierda, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(B_derecha, GPIO.IN,pull_up_down=GPIO.PUD_UP)
Cont_iz=0
Cont_der=0
inicio=0
fin=0
try:
    while True:
        B_iz=GPIO.input(B_izquierda)
        B_der=GPIO.input(B_derecha)
        time.sleep(0.2)
        if B_der==0:
            inicio=time.time()
            Cont_der+=1
            print(inicio)
            print("btn der")
            while fin - inicio <2:
                fin=time.time()
                print(fin-inicio)
                B_der=GPIO.input(B_derecha)
                
                time.sleep(0.2)
                if B_der==0:
                    Cont_der+=1
            print("Tiempo")
            if Cont_der == 1:
                print("Acción 1---DERECHA")
                inicio=0
                fin=0
                Cont_der=0
            if Cont_der == 2:
                print("Acción 2---DERECHA")
                inicio=0
                fin=0
                Cont_der=0
        if  B_iz==0:
            inicio=time.time()
            Cont_iz+=1
            print(inicio)
            print("btn izq")
            while  fin - inicio <1 :
                fin=time.time()
                print(fin-inicio)
                B_iz=GPIO.input(B_izquierda)
                time.sleep(0.2)
                if B_iz == 0:
                    Cont_iz+=1
            print("Tiempo")
            if Cont_iz==1:
                print("Acción 1---IZQUIERDA")
                inicio=0
                fin=0
                Cont_iz=0
            if Cont_iz==2:
                print("Acción 2---IZQUIERDA")
                inicio=0
                fin=0
                Cont_iz=0
                
except KeyboardInterrupt:
    print("TT")    
finally:
    GPIO.cleanup()
    print("Pines limpios")
    
