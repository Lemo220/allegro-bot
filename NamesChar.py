import os
names_char = {}

arr = os.listdir("./Names_char")

for file in arr:
    with open("./Names_char/Names_char.txt") as fp:
        item = []
        lines = fp.readlines()
        for line in lines:
            item.append(str(line.replace("\n", "")))
        names_char.__setitem__(str(file.replace(".txt", "")), item)
