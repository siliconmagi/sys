import sqlite3
import re

# setup sqlite
conn = sqlite3.connect('hour.db')
c = conn.cursor()
c.execute('select * from Servers')
r0 = c.fetchall()
print(r0)
stm = r0[0][1].decode('utf-8')
ots = r0[1][1].decode('utf-8')
psp = r0[2][1].decode('utf-8')


def parse(server):
    # remove double lines
    out0 = server.replace('\n\n', '\n')
    # split out by \n
    out1 = out0.split('\n')
    # remove spaces in elements
    out2 = [l.replace(' ', '') for l in out1]
    # remove 1st element
    out2.pop(0)
    #  print(out2)
    # get stMailDI memory
    if server == stm:
        out3 = re.findall(r'(^\d{1,2}\.\d)', out2[0])
        print(out3)
    else:
        out3 = re.findall(r'(\d\d\.\d)', out2[-1])
        # select last match
        out4 = [out2[0], out2[1], str(100 - float(out3[-1]))[0:4], out3[-1]]
        print(out4)


parse(stm)
parse(ots)
parse(psp)

#  str0 = 'ST-MAIL-DI:\n '
