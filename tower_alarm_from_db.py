import socket
import time
import os
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('103.22.222.216',1114))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

data = client_socket.recv(65535)
print(data)
client_socket.send(data)

def json():
	os.system('python tower_json_from_db.py')
#thread1 = threading.Thread(target = json)
#thread1.start()
#thread2 = threading.Thread(target = popup)
#thread2.start()
