import subprocess
import time
import os

while 1:
	try:
		subprocess.check_output(["networkctl", "status", "ppp0"])
		print("BAM Conectada")
	except:
		print("BAM No Conectada")
		os.system("sudo python3 /home/pi/sysras/bam/connect_bam.py")
	time.sleep(1)

