import os

path = ["./data", "./data/final", "./data/gen", "./data/original", "./data/tmp"]

for i in range(len(path)):
    os.makdir(path[i])
