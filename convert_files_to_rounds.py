OFFER = 0
ACK = 1

def ChangeDictionary(msg_id, time_stamp, user_id, dictionary):
    if msg_id not in dictionary:
        dictionary[msg_id] = [time_stamp, user_id]
    else:  # it is in the dictionary
        check_time = dictionary[msg_id][0]
        if check_time > time_stamp:
            dictionary[msg_id] = [time_stamp, user_id]

def WriteToCSVFile(send_or_recieve, dictionary, file_name):
    file = open(file_name, "a+")

    dict_length = len(dictionary)

    iteration = 0

    file.write(send_or_recieve + ":[")
    for row in dictionary.values():
        iteration += 1
        user_id = row[1]
        file.write("'" + user_id)

        if iteration != dict_length:
            file.write("', ")
    #TODO: Might cause problems? The ] in the csv file is in a different box
    file.write("]\n")

    file.close()


file_number = str(99)
file_name = "transcript_" + file_number + ".txt"

csv_file_name = "transcript_" + file_number + ".csv"
#this deletes the stuff in the csv file
open(csv_file_name, 'w').close()

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

# goes through each line in the file
for row in data_file_in:
    row_split = row.split()

    #the rows that have an ID do not have the [
    if row[0] != "[":
        user_id = row_split[0]
        round_number = int(row_split[2])
        if round_number != new_round:
            WriteToCSVFile("S", round_offer_dict, csv_file_name)
            WriteToCSVFile("R", round_ack_dict, csv_file_name)
            round_offer_dict = {}
            round_ack_dict = {}
            new_round = round_number

    else:
        #the [:-1] gets rid of the ']'
        time_stamp = row_split[1][:-1]
        msg_id = row_split[2]

        if msg_id == "OFFER":
            msg_id_type = 0

        elif msg_id == "ACK":
            msg_id_type = 1

        else: #is the message id number
            if msg_id_type == OFFER:
                if msg_id[0] != "f":
                    msg_id_type = -1
                    continue
                ChangeDictionary(msg_id, time_stamp, user_id, round_offer_dict)
            elif msg_id_type == ACK:
                ChangeDictionary(msg_id, time_stamp, user_id, round_ack_dict)
            msg_id_type = -1

data_file_in.close()