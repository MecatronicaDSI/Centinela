import pymysql

class Database:
    
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'sysras2020'
        self.db = 'sysras_cent'
    
    def getConexion(self):
        try:
            conn = pymysql.connect(host=self.host,
                                   user=self.user,
                                   passwd=self.password,
                                   db=self.db)
            print('Conexion exitosa a la base de datos')
            
        except Exception as e:
            print("Error de conexion", e)
            
        return conn
