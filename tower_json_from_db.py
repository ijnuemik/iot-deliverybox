import socket                   # Import socket module
import time
from socket import error


while 1:
    try:
	s = socket.socket()             # Create a socket object
	print("a")
	s.connect(('103.22.222.214',1115))
    except socket.error as serr:
	print serr
        time.sleep(5)
	continue
    break

while 1:
    with open('pi4.json', 'wb') as f:
        print 'file opened'
        print('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        # write data to a file
        f.write(data)
    f.close()
    print('Successfully get the file')
    time.sleep(1)

s.close()
print('connection closed')
