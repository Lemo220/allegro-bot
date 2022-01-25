import os
auction_id_servers = {}

arr = os.listdir("./AuctionIDServers")

for file in arr:
    with open("./AuctionIDServers/"+file) as fp:
        item = []
        lines = fp.readlines()
        for line in lines:
            item.append(str(line.strip()))
        auction_id_servers.__setitem__(str(file.replace(".txt", "")), item)

