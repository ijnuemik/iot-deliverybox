import socket
import time
import os
import threading

def infiniteloop3():
    print('=============get json from influx')
    os.system('python db_json_influx.py')

def infiniteloop1():
    print('==============combine json start')
    temp1 = ''
    temp2 = ''
    temp3 = ''
    temp4 = ''
    temp5 = ''
    while(1):
        with open('pi4', 'w') as outfile:
            outfile.write('[')
	    with open('pi1.json') as infile:
                a = infile.read()
                if a == '':
                    if temp1 != '':
                        outfile.write(temp1)
                else:
                    outfile.write(a)
                    temp1 = a
                infile.closed
            outfile.write(',')
	    with open('pi2.json') as infile:
                a = infile.read()
                if a == '':
                    if temp2 != '':
                        outfile.write(temp2)
                else:
                    outfile.write(a)
                    temp2 = a
                infile.closed
            outfile.write(',')
	    with open('pi3.json') as infile:
                a = infile.read()
                if a == '':
                    if temp3 != '':
                        outfile.write(temp3)
                else:
                    outfile.write(a)
                    temp3 = a
                infile.closed
            outfile.write(',')
	    with open('pi4.json') as infile:
                a = infile.read()
                if a == '':
                    if temp4 != '':
                        outfile.write(temp4)
                else:
                    outfile.write(a)
                    temp4 = a
                infile.closed
            outfile.write(',')
	    with open('pi5.json') as infile:
                a = infile.read()
                if a == '':
                    if temp5 != '':
                        outfile.write(temp5)
                else:
                    outfile.write(a)
                    temp5 = a
                infile.closed
            outfile.write(']')
    	outfile.closed
    	print('completely saved json file')
        time.sleep(1)

def infiniteloop2():
    os.system('python db_json_to_tower.py')

thread3 = threading.Thread(target = infiniteloop3)
thread3.start()
thread1 = threading.Thread(target = infiniteloop1)
thread1.start()
thread2 = threading.Thread(target = infiniteloop2)
thread2.start()
