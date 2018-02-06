"""Mail CLI tool

Usage:
neon.py loopf <name>
neon.py all
neon.py auto
neon.py (-h | --help)

Options:
-h --help     Show this screen.

"""
import csv
import time
#  import re
import sqlite3
from pexpect import pxssh
from docopt import docopt


def mailQ():
    s0 = [
        "mailq",
        "grep Feb",
        "awk '{{print $7}}'",
        "sort",
        "uniq -c",
        "sort -n",
        "less"
    ]
    cmd = ' | '.join(s0)
    return cmd


# setup sqlite
conn = sqlite3.connect('mn.db')
c = conn.cursor()
c.execute('drop table if exists Emails')
c.execute('CREATE TABLE {tn} (\
          {c1} {t1} PRIMARY KEY,\
          {c2} {t2})'.format(
    tn='Emails',
    c1='email',
    t1='TEXT',
    c2='count',
    t2='INTEGER',
)
)


def bash(xList):
    # double bracket as escape character
    s0 = [
        "mailq",
        "grep Feb",
        "grep '{}'",
        "awk '{{print $1}}'",
        "awk -F '*' '{{print $1}}'",
        "postsuper -d -"
    ]
    cmd = ' | '.join(s0)
    return cmd.format(xList)


# create list of connection dictionaries from csv
try:
    ipList = []
    with open('secret.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ipList.append(
                {
                    'name': row[0],
                    'ip': row[1],
                    'user': row[2],
                    'pwd': row[3]
                })
except ImportError:
    print('secret.csv not found')


def loopf(name):
    '''Loop each line in neoList into bash()'''
    try:
        ip = [x['ip'] for x in ipList if x['name'] == name][0]
        user = [x['user'] for x in ipList if x['name'] == name][0]
        pwd = [x['pwd'] for x in ipList if x['name'] == name][0]
        s = pxssh.pxssh()
        s.SSH_OPTS = "-o 'RSAAuthentication=no' -o 'PubKeyAuthentication=no'"
        s.login(ip, user, pwd)
        # send mailq command
        print(mailQ)
        s.sendline(mailQ)
        # match prompt
        s.prompt()
        # decode bytes object for split
        mqOut = s.before.decode()
        print(mqOut)
        #  mqList = mqOut.split('\n')
        #  # strip whitespace
        #  s0 = [i.strip() for i in mqList]
        #  # remove first and last element from list
        #  s1 = s0[1:-1]
        #  # list element must contain key and value
        #  regex = re.compile(r'^\d \w.*')
        #  f0 = [m.group(0) for l in s1 for m in [regex.search(l)] if m]
        #  # split name
        #  z1 = [i.split(' ')[0] for i in f0]
        #  # split instances
        #  z2 = [i.split(' ')[1] for i in f0]
        #  # zip names as list of tuples
        #  t0 = zip(z2, z1)
        #  # descending order by value
        #  t1 = sorted(list(t0), key=lambda x: x[1])
        #  # remove all rows from table Emails
        #  c.execute('delete from Emails')
        #  # save list of tuples to sqlite table
        #  c.executemany('insert into Emails (email, count) values (?,?)', t1)
        #  c.execute('select * from Emails')
        #  r0 = c.fetchall()
        #  [print(row) for row in r0]
        #  conn.commit()
        #  s.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


def auto():
    while True:
        loopf('neo1')
        loopf('neo2')
        loopf('neo3')
        time.sleep(160)


if __name__ == '__main__':
    arguments = docopt(__doc__)

    # if an argument called "file" was passed, execute the file logic.
    if arguments['loopf']:
        loopf(arguments['<name>'])
    elif arguments['all']:
        loopf('neo1')
        loopf('neo2')
        loopf('neo3')
    elif arguments['auto']:
        auto()
