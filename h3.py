import sqlite3
import re

# setup sqlite
conn = sqlite3.connect('hour.db')
c = conn.cursor()
c.execute('select * from Servers')
r0 = c.fetchall()
print(r0)
ots = r0[0][1].decode('utf-8')
psp = r0[1][1].decode('utf-8')


def iops(server):
    out0 = re.findall(r'(\d{1,2},\d\d\d\.\d\d|\d\d\d\.\d\d)', server)
    out1 = [out0[0], out0[-1]]
    return out1


def rw(server):
    out0 = re.findall(r'\/(\d\d\.\d)%', server)
    out1 = out0[0].replace(' ', '')
    out2 = [str(100 - float(out1[0])), out1[0]]
    return out2


def parse(server):
    # remove double lines
    out0 = server.replace('\n\n', '\n')
    # split out by \n
    out1 = out0.split('\n')
    # remove spaces in elements
    out2 = [l.replace(' ', '') for l in out1]
    # remove 1st element
    out2.pop(0)
    # gen rw
    out3 = re.findall(r'(\d\d\.\d)', out2[2])
    # select last match instance
    #  print(out3[-1])
    out4 = [out2[0], out2[1], str(100 - float(out3[-1]))[0:4], out3[-1]]
    return out4


print(parse(ots))
print(parse(psp))

#  str0 = 'ST-MAIL-DI:\n '
