import socket  
import time
import json

BUFFSIZE=1024

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
s.bind(("0.0.0.0",22223))  
s.listen(5)

while True:
	conn, addr = s.accept()
	print("connected by ", addr)
	data = conn.recv(BUFFSIZE).decode()
	recvjson = json.loads(data)
	print(recvjson)
	conn.sendall(json.dumps({'cmd_ans': True, 'log_ans': True, 'equip': 'dht11v2.0'}).encode())
s.close()  