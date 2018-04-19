import socket
from threading import Thread, Lock
import threading
import sys
import re
from datetime import datetime
import time

mutex = Lock()

def thread_work(s, user_id):
	
	print("Thread for user: " + user_id)
	current_round = []
	last_message = ''
	ackd = 0
	this_round = 0
	while True:
		try:
			received = s.recv(10024)
		except socket.error as err:
			print("Error %s" %(err))
			break
		timestamp = "[" + str(datetime.now()) + "] "
		split = re.split('[\n]', received)
		
		if last_message != '':
			current_round.append(old_timestamp + last_message + split[0])
			del split[0]

		for element in split[:-1]:
			if element == "ACK":
				ackd += 1
			current_round.append(timestamp + str(element))
		
		if split[-1] == '':
			last_message = ''
		else:
			last_message = split[-1]
			old_timestamp = timestamp
		
		if ackd == 32:
			mutex.acquire()
			print(user_id + " writing to file")
			with open ("transcript.txt", "a") as f:
				f.write(user_id + " Round: " + str(this_round) + '\n')
				for item in current_round:
					f.write(item + '\n')
			mutex.release()
			ackd = 0	
			current_round = []
			this_round += 1

def read_target_file(filename):
        target_ids = []
        with open(filename) as f:
                targets = f.readlines()
                for target in targets:
                        split_targ = re.split('[@ : \n]', target)
                        split_targ = split_targ[:-1]
                        target_ids.append(split_targ)
        return target_ids

peers = read_target_file("publicpeers.txt")

priv = 0
pub = 0
for peer in peers:
	
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as err:
		print("Error %s" %(err))

	try:
		s.connect((peer[1], int(peer[2])))
	except socket.error as err:
		print("Error %s" % (err))
		continue

	t1 = Thread(target=thread_work, args=(s, peer[0]))
	t1.daemon = True
	t1.start()

while threading.active_count() > 0:
	time.sleep(0.1)
	
