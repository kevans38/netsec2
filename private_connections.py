import time
import re
import datetime


OFFER = 0
ACK = 1
#1 second time threshold
TIME_THRESH = 1


def write_to_file(round_num, dictionary, file_name):
    with open(file_name, "a") as file:
        file.write("-------- Round : " + str(round_num) + '\n')
        for k, v in dictionary.items():
            file.write("Message: " + str(k) + '\n')
            for row in v:
                file.write("User and time: " + str(row) + "\n")
        file.close()


def read_peers_file(filename):
    peer_ids = []
    with open(filename) as f:
        peers = f.readlines()
        for peer in peers:
            split_p = re.split('[@ : \n]', peer)
            split_p = split_p[:-1]
            peer_ids.append(split_p)
    return peer_ids


file_number = str(7)
#file_number = "chad"
file_name = "transcript_" + file_number + ".txt"

new_file_name = "private_eight_" + file_number + ".txt"
#this deletes the stuff in the csv file
open(new_file_name, 'w').close()

#just to initialize
user_id = ""
time_stamp = ""
msg_id = ""
msg_id_type = -1
new_round = 1

data_file_in = open(file_name, "r")
started_new_round = 0

# setup dictionary of all private peers messages
priv_msg_dict = {}
curr_time = 0
prev_epoch = 0.0
curr_msg_time = 0
curr_time_add_ten = 0
first = 0
round_start_time = 0
round_ct = 0

for row in data_file_in:
    dif = 0     # difference in time
    row_split = row.split()

    #the rows that have an ID do not have the [
    if row[0] != "[":
        user_id = row_split[0]
        round_number = int(row_split[2])

        # starting new round
        if round_number != new_round:
            print("-=======================NEW ROUND")
            write_to_file(round_number, priv_msg_dict, new_file_name)
            round_ct += 1

            started_new_round += 1
            new_round = round_number

            # NEW additions
            prev_time = 0
            prev_epoch = 0.0
            first = 0
            priv_msg_dict = {}  # collect new private messages each round..

    # this is the OFFER or ACK in that round
    else:
        # the [:-1] gets rid of the ']'
        time_stamp = row_split[1][:-8]
        full_time_stamp = row_split[0][1:] + " " + time_stamp
        epoch_time = time.mktime(time.strptime(full_time_stamp, "%Y-%m-%d %H:%M:%S"))
        miliseconds = float(row_split[1][-8:-1])
        full_epoch_time = epoch_time + miliseconds

        curr_msg_time = float(full_epoch_time)  # converted to float for better calculations

        # if it is the first of the round, keep track of to determine private nodes.
        if first == 0:
            round_start_time = curr_msg_time

        msg_id = row_split[2]
        if msg_id == "OFFER":
            msg_id_type = 0

        elif msg_id == "ACK":
            msg_id_type = 1

        else: #is the message id number
            # Look for OFFERS, then private messages
            if msg_id_type == OFFER:

                # if messsage from a private node, check time and put in dict
                if row_split[2][0] != "f":
                    msg_id_type = -1
                    msg = row_split[2]

                    temp = [user_id, curr_msg_time]

                    # if not in the dictionary, only add to list of 8 if...???
                    if msg not in priv_msg_dict:
                        time_dif = abs(curr_msg_time - round_start_time)

                        if time_dif < 5:
                            priv_msg_dict[msg] = []
                            priv_msg_dict[msg].append(temp)
                    else: # only put user in priv_msg_dict if fit in the right time
                        if msg in priv_msg_dict:
                            for k,v in priv_msg_dict.items():
                                dict_user_time = v[0][1]            #This should be the lowest time
                                time_dif = abs(curr_msg_time - dict_user_time)
                                # time_dif should only be 10

                                if time_dif < 5:
                                    #print("here")
                                    priv_msg_dict[msg].append(temp)
                                    break
                    first += 1
            msg_id_type = -1

    '''
    for k,v in priv_msg_dict.items():
        print("message: ", k)
        #print("node recvd message, time: ", v[0][1])    # this give the time of the 0th user
        print("node recev", v )
    '''
    prev_epoch = curr_msg_time      # not using anymore
data_file_in.close()
