import csv
from collections import namedtuple


ipList = []

with open("deleteList.txt", newline="") as infile:
    reader = csv.reader(infile)
    Data = namedtuple("Data", next(reader))  # get names from column headers
    for data in map(Data._make, reader):
        print(data.domains)

with open("secret.csv", newline="") as infile:
    reader = csv.reader(infile)
    Data = namedtuple("Data", next(reader))  # get names from column headers
    for data2 in map(Data._make, reader):
        ipList.append(data2)
