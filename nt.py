import csv
from collections import namedtuple

SECRET = 'secret.csv'
fields = ('name', 'ip', 'user', 'pwd')
dataRecord = namedtuple('dataRecord', fields)


def readData(path):
    with open(path, newline='') as data:
        data.readline()            # Skip the header
        reader = csv.reader(data)  # Create a regular tuple reader
        for row in map(dataRecord._make, reader):
            yield row


if __name__ == "__main__":
    for row in readData(SECRET):
        print(row)
