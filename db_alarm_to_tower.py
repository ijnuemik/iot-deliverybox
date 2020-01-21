import socket
import time
from socket import error

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(('210.114.90.95',1112))
sock.connect(('103.22.222.216',1111))
output = 'Fire alarm!'
sock.sendall(output.encode('utf-8'))
data = sock.recv(65566)
print(data)
