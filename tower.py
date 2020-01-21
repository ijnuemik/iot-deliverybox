import Tkinter
import tkMessageBox
import tkSimpleDialog
from datetime import datetime
from influxdb import InfluxDBClient
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.7',1113))


while True:
	server_socket.listen(0)
	client_socket, addr = server_socket.accept()
	data = client_socket.recv(65535)
	print("receive data from pi: " +data)
	application_window = Tkinter.Tk()
	result = tkMessageBox.askyesno("POSTBOX","Delivery has arrived.\n Do you confirm?\n You can watch CCTV at 192.168.1.12/zm \n", parent = application_window)
	if result is True:
		answer = 'Open'
		send_data = 'True'
	else:
		answer = 'refused'
		send_data = 'False'
	current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
	json_body = [ { "measurement" :"Delivery", "time" : current_time, "fields":{ "Status" : answer } } ]
	client = InfluxDBClient('192.168.0.11',8086)
	client.switch_database('POSTBOX')
	client.write_points(json_body)
	print("Complete DB write status")

	client_socket.send(send_data)

	if result is True:
		answer = tkSimpleDialog.askstring("POSTBOX", "Is there any information about the delivery?", parent=application_window)
		json_body = [ { "measurement" :"Delivery", "time" : current_time, "fields":{ "Status" : '', "information" : answer } } ]
		client.write_points(json_body)
		result2 = client.query('select information from Delivery;')
		print("Complete DB write information")

	application_window.destroy()
