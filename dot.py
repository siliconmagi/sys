"""Greeter.

Usage:
basic.py hello <name>
basic.py goodbye <name>
basic.py (-h | --help)

Options:
-h --help     Show this screen.

"""
import csv
import sqlite3
from pexpect import pxssh
from docopt import docopt

# setup sqlite
conn = sqlite3.connect('dot.db')
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


def hello(name):
    ip = [x['ip'] for x in ipList if x['name'] == name][0]
    user = [x['user'] for x in ipList if x['name'] == name][0]
    pwd = [x['pwd'] for x in ipList if x['name'] == name][0]
    s = pxssh.pxssh()
    s.SSH_OPTS = "-o 'RSAAuthentication=no' -o 'PubKeyAuthentication=no'"
    s.login(ip, user, pwd)
    # send mailq command
    s.sendline('uname -a')
    # match prompt
    s.prompt()
    # decode bytes object for split
    mqOut = s.before.decode()
    print(mqOut)


def goodbye(name):
    print('Goodbye, {0}'.format(name))


if __name__ == '__main__':
    arguments = docopt(__doc__)

    # if an argument called hello was passed, execute the hello logic.
    if arguments['hello']:
        hello(arguments['<name>'])
    elif arguments['goodbye']:
        goodbye(arguments['<name>'])
