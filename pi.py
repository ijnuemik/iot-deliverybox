from datetime import datetime
from influxdb import InfluxDBClient
import socket
import RPi.GPIO as GPIO
import time


def GPIO_set():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT)
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.output(21,False)

def wait_button():
    if GPIO.input(23) == 0:
        print("Button pressed")
        status_request()

def status_request():
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [ { "measurement" :"Delivery", "time" : current_time, "fields":{ "Status" : "request" } } ]
        client = InfluxDBClient('192.168.0.11',8086)
        client.switch_database('POSTBOX')
        client.write_points(json_body)
        print("complete DB write request")
        TCP();


def status_closed():
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        json_body = [ { "measurement" :"Delivery", "time" : current_time, "fields":{ "Status" : "closed" } } ]
        client = InfluxDBClient('192.168.0.11',8086)
        client.switch_database('POSTBOX')
        client.write_points(json_body)
        result2 = client.query('select Status from Delivery;')
        print("Result: {0}".format(result2))

def TCP():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('192.168.0.7',1113))
        output = 'Delivery has arrived'
        sock.sendall(output.encode('utf-8'))
        data = sock.recv(65566)
        print(data)
        if data:
           print('request agreed')
           status_open()
           #switch on (5 sec)
        else:
           print('request refused')
           #switch off

def status_open():
        GPIO.output(21, True)
        while True:
            if GPIO.input(23) == 0:
                print('Button pressed(closed)')
                GPIO.output(21, False)
                status_closed()
                break
            time.sleep(1)

if __name__ == '__main__':
        GPIO_set()
        status_request()
        GPIO.cleanup()
