from pynput import keyboard as kb


def pulsa(tecla):
	print('Se ha pulsado la tecla ' + str(tecla))

def suelta(tecla):
	print('Se ha soltado la tecla ' + str(tecla))
	# if tecla == kb.KeyCode.from_char('q'):
	# 	return False

escuchador = kb.Listener(pulsa, suelta)
escuchador.start()

while escuchador.is_alive():
	pass
