import time
import re
import datetime

OFFER = 0
ACK = 1
#1 second time threshold
TIME_THRESH = 1

#msg_id is whether it is a OFFER or ACK


def WriteToCSVFile(send_or_recieve, dictionary, file_name):
    file = open(file_name, "a+")

    dict_length = len(dictionary)

    iteration = 0

    file_string = send_or_recieve + ":["
    for row in dictionary.values():
        iteration += 1
        user_id = row[1]
        check_for_public_nodes = row[2]

        #this means it is a public node
        if check_for_public_nodes == 1:
            #print("Public user: ", user_id)
            file_string += "'" + user_id

            file_string += "', "
        else: # IT IS A PRIVATE NODE
            #print("Private user: ", user_id)
            continue
    #TODO: Might cause problems? The ] in the csv file is in a different box
    file_string = file_string[:-2]
    file_string += "]\n"
    file.write(file_string)
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

csv_file_name = "transcript_" + file_number + ".csv"
#this deletes the stuff in the csv file
open(csv_file_name, 'w').close()

# open private peers file
#private_peers = read_peers_file("privatepeers.txt")

round_offer_dict = {}
round_ack_dict = {}

#just to initialize
user_id = ""
time_stamp = ""
msg_id = ""
msg_id_type = -1


#TODO: This will assume that the first round will start with 1
new_round = 1

data_file_in = open(file_name, "r")
started_new_round = 0

# setup dictionary of all private peers messages
priv_msg_dict = {}
curr_time = 0
prev_epoch = 0.0
ftime = 0

for row in data_file_in:
    dif = 0     # difference in time
    row_split = row.split()

    #the rows that have an ID do not have the [
    if row[0] != "[":
        user_id = row_split[0]
        round_number = int(row_split[2])

        first = 0

        # starting new round
        if round_number != new_round:
            started_new_round += 1
            WriteToCSVFile("S", round_offer_dict, csv_file_name)
            WriteToCSVFile("R", round_ack_dict, csv_file_name)
            round_offer_dict = {}
            round_ack_dict = {}
            new_round = round_number

            # NEW additions
            prev_time = 0
            prev_epoch = 0.0

            priv_msg_dict = {}  # collect new private messages each round..


    # this is the OFFER or ACK in that round
    else:
        # the [:-1] gets rid of the ']'
        time_stamp = row_split[1][:-8]
        full_time_stamp = row_split[0][1:] + " " + time_stamp
        epoch_time = time.mktime(time.strptime(full_time_stamp, "%Y-%m-%d %H:%M:%S"))
        miliseconds = float(row_split[1][-8:-1])
        full_epoch_time = epoch_time + miliseconds

        ftime = float(full_epoch_time)  # converted to float for better calculations


        #print("current epoch", type(ftime))
        #print("prev epoch ", type(prev_epoch))
        # DOESN't WORK here because want to compare the same msg time!!!
        '''
        if prev_epoch != 0:
            dif = ftime - prev_epoch)
            print("DIF", dif)

        if dif != 0:
            print("WHAT, YAY!!!!")
        '''

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
                    #print("++++++++++++++++user_id", user_id)
                    #print("row_split[2][0]: ", row_split[2])

                    msg = row_split[2]

                    temp = [user_id, ftime]

                    # only put user in priv_msg_dict  if really close time?
                    if msg not in priv_msg_dict:
                        priv_msg_dict[msg] = []

                    priv_msg_dict[msg].append(temp)

            msg_id_type = -1

    if started_new_round == 3:
        print("in")
        for k,v in priv_msg_dict.items():
            print("message: ", k)
            print("node recvd message, time: ", v)
        #exit()
    prev_epoch = ftime
    first += 1

data_file_in.close()
