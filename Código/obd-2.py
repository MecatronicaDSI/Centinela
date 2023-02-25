import obd


obd.logger.setLevel(obd.logging.DEBUG)

connection = obd.OBD("/dev/rfcomm0")
print("Connection status: ")
print(connection.status())


connection.close()