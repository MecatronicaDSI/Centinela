import os
import time

cmd_connect = "sudo ./home/pi/sysras/bam/sakis3g connect --sudo --console USBINTERFACE='0' OTHER='USBMODEM' USBMODEM='12d1:14ac' SIM_PIN='1234' APN='CUSTOM_APN' CUSTOM_APN='internet.itelcel.com' APN_USER='webgprs' APN_PASS='webgprs2002'"
print("conectando...")
os.system(cmd_connect)
