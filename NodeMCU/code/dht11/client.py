import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.226", 8085))
while True:	
	s.sendall(input().encode())
	print(s.recv(1024).decode())
s.close()