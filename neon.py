"""Neofifti CLI tool

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
from pexpect import pxssh
from docopt import docopt


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

# create list from neoList.csv
try:
    neoList = []
    with open('neoList.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            neoList.append(row[0])
except ImportError:
    print('neoList.csv not found')


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
        for x in neoList:
            s.sendline(bash(x))
            # match prompt
            s.prompt()
            # decode bytes object for split
            mqOut = s.before.decode()
            print(mqOut)
        s.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


def auto():
    while True:
        loopf('neo1')
        loopf('neo2')
        loopf('neo3')
        time.sleep(90)


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
