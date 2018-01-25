from decimal import Decimal
import sqlite3
import re
import codecs


# setup sqlite
conn = sqlite3.connect('hour.db')
c = conn.cursor()
c.execute('select * from Servers')
r0 = c.fetchall()
stm = r0[0][1].decode('utf-8')
ots = r0[1][1].decode('utf-8')
psp = r0[2][1].decode('utf-8')
shift0 = ['David', 'Jordan B.', 'Matthew']


def parse(server):
    # remove double lines
    out0 = server.replace('\n\n', '\n')
    # split out by \n
    out1 = out0.split('\n')
    # remove spaces in elements
    out2a = [l.replace(' ', '') for l in out1]
    out2b = [l.replace('s|S', '5') for l in out2a]
    out2 = [l.replace('o|O', '0') for l in out2b]
    # remove 1st element
    out2.pop(0)
    #  print(out2)
    # get stMailDI memor
    if server == stm:
        out3 = re.findall(r'(\d\d)%', out2[0])
        out4 = Decimal(12 * (float(out3[-1]) / 100))
        return str(round(out4, 1))
    else:
        read = out2[2][0:2]
        write = Decimal(str(100 - float(read)))
        out4 = [out2[0], out2[1], read, round(write, 0)]
        return out4


# string together hourly
stm0 = 'ST-MAIL-DI:\n{} / 12 GB Total Memory Usage' \
    .format(parse(stm))
ots0 = 'OTS10SAN1\nAverage IOPS (past 1HR) - {} / {}' \
    .format(parse(ots)[1], parse(ots)[0])
ots1 = 'Read/Write% - {}% / {}% '.format(parse(ots)[2], parse(ots)[3])
ots2 = '{}\n{}'.format(ots0, ots1)
psp0 = 'PSP10SAN1\nAverage IOPS (past 1HR) - {} / {}' \
    .format(parse(psp)[1], parse(psp)[0])
psp1 = 'Read/Write% - {}% / {}% '.format(parse(psp)[2], parse(psp)[3])
psp2 = '{}\n{}'.format(psp0, psp1)
none = '\n------------------------------\n- None'
ongoing = 'Ongoing Incidents:{}'.format(none)
resolved = 'Recently Resolved Incidents:{}'.format(none)
tasks = 'Tasks{}'.format(
    none.replace('None', 'Monitoring SiteMonster and Nagios')
)
shift1 = ['- {}'.format(i) for i in shift0]
shift2 = 'On shift:\n' + '\n'.join(shift1)
#  shift0 = 'On shift:\n'.join(here)
txt = [stm0, ots2, psp2, ongoing, resolved, tasks, shift2]
print('\n\n'.join(txt))
file = codecs.open("hour", "w", "utf-8")
file.write(u'\n\n'.join(txt))
file.close()
