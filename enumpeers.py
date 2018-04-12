import socket
import sys
import re

def read_target_file(filename):
	target_ids = []
	with open(filename) as f:
		targets = f.readlines()
		for target in targets:
			split_targ = re.split('[@ : \n]', target)
			split_targ = split_targ[:-1]
			target_ids.append(split_targ)
	return target_ids

targets = read_target_file("part2targets.txt")

x = 0	
for target in targets:

	if x == 0:
		x += 1
		continue	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket created")
	except socket.error as err:
		print ("Error %s" %(err))

	s.connect((target[1], int(target[2])))
	s.send("PEERS\n")
	received = s.recv(1024)
	print(received)
	received2 = s.recv(1024)
	print(received2)
	s.close()
