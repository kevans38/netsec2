import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
	print("Error %s" %(err))

s.connect(("160.36.57.98", 10843))
while True:
	print(s.recv(1024))
