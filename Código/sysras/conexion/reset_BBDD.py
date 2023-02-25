import sys
sys.path.append("/home/pi/sysras/conexion")

from database import Database
from time import sleep

reset = False

sleep(10)

db = Database();
conexion = db.getConexion();

while reset == False:
    cursor1=conexion.cursor()
    cursor1.execute("TRUNCATE sensoreportado")
    
    cursor2=conexion.cursor()
    cursor2.execute("DELETE FROM notificaciondireccion where fcreacionDir < DATE_SUB(NOW(), INTERVAL 1 WEEK)")
    
    cursor3=conexion.cursor()
    cursor3.execute("DELETE FROM notificacion where fcreacionNot < DATE_SUB(NOW(), INTERVAL 1 WEEK)")

    conexion.commit()
    conexion.close()
    print("Reporte limpio")
    reset = True
    
