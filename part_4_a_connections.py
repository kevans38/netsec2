

public_dict = {}
priv_dict = {}
current_public_id = -1

priv_nodes_file = open("privatepeers.txt", "r")


for element in priv_nodes_file:
    priv_node = element[:-20]
    priv_dict[priv_node] = []

priv_nodes_file.close()

transcript_name = "priv_transcript.txt"
data_file_in = open(transcript_name, "r")

for element in data_file_in:
    node_info = element.split()
    if node_info[0] == "!":
        #gets rid of newline
        node_info[-1] = node_info[-1].strip()
        current_public_id = str(node_info[1])
        #public_dict[current_public_id] = []
    else:
        current_public_nodes_node = node_info[0]
        if current_public_nodes_node in priv_dict:
            priv_dict[current_public_nodes_node].append(current_public_id)


        #public_dict[current_public_id].append(str(current_public_nodes_node))

data_file_in.close()

with open("pub_priv_connections.txt", "w") as file:
    for priv_node, public_nodes in priv_dict.items():
        file_string = (str(priv_node) + ", ")
        for ele in public_nodes:
            file_string += str(ele)
            file_string += ", "
        file_string = file_string[:-2]
        file_string += "\n"
        file.write(file_string)
