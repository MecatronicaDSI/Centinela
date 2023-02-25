import subprocess, time
from gpiozero import OutputDevice
import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
Umbral_on=55
Umbral_off=50
T_actualizacion= 5

def get_temp():
    output = subprocess.run(['vcgencmd', 'measure_temp'], capture_output=True)
    temp_str = output.stdout.decode()
    try:
        return float(temp_str.split('=')[1].split('\'')[0])
    except (IndexError, ValueError):
        raise RuntimeError('Could not parse temperature output.')


while True:
    temp=get_temp()
    print("Temperatura CPU: " + str(temp))

    if temp >= Umbral_on:
        GPIO.output(16,True)
    if temp < Umbral_on:
        GPIO.output(16,False)
    time.sleep(T_actualizacion)
