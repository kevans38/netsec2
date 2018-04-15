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

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket created")
	except socket.error as err:
		print ("Error %s" %(err))
		targets.remove(target)
		continue
	s.connect((target[1], int(target[2])))

	these_peers = []
	while True:
		s.send("PEERS\n")
		received = s.recv(1024)
		received2 = s.recv(1024)
		split_rec = re.split('[\n]', received2)
		split_rec = split_rec[:-1]
		split_rec.append(received[:-1])
		print("hm")

		if '@' not in split_rec[0]:
			continue
		print(split_rec)
		no_new = True
		threshold = 0
		for element in split_rec:
			found_peer = False
			for peer in these_peers:
				if element == peer:
					found_peer = True
					threshold = 0
					break
			if not found_peer:
				these_peers.append(element)
				no_new = False
				threshold += 1
				print(len(these_peers))
		if no_new == True and threshold > 4:
			break
							

	for peer in these_peers:
		split_peer = re.split('[@ :]', peer)
		found_peer = False
		for target2 in targets:
			if split_peer[0] == target2[0]:
				found_peer = True
				break
		if not found_peer:
			targets.append(split_peer)
	print("*********************************")
	print(len(targets))
	for ele in targets:
		print(ele)
	print("***********************************")


	s.close()

with open ("trash.txt") as trash:
	for target in targets:
		trash.write(target[0] + "@" + target[1] +":" + target[2])
