from collections import namedtuple
import csv
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder


Keywords = ['mntSt1', 'umntSt1', 'check', 'exit']
listIP = []
listDelete = []
SECRET = 'secret.csv'
DELETE = 'deleteList.csv'
fields = ('name', 'ip', 'user', 'pwd')
dataRecord = namedtuple('dataRecord', fields)
mntOpt = 'sudo mount -t cifs --ro'
#  mntOpt = 'sudo mount -t cifs --rw'
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'

# directories to check
dir1 = '/mnt/stmail/Inetpub/scripts/dreamersi/CheckAccount'
dir2 = '/mnt/stmail/Inetpub/scripts/dreamersi/Vendors'
dir3 = '/mnt/stmail/Inetpub/wwwroot/dreamersi/vendors'
dir4 = '/mnt/stmail/Inetpub/mailroot/Mailbox'
dir5 = '/mnt/stmail/Inetpub/mailroot/UserInf'
dir6 = '/mnt/stmail/Inetpub/mailroot/UserExtra'
dir7 = '/mnt/stmail/Inetpub/mailroot/SpamBox'
dir8 = '/mnt/stmail/Inetpub/mailroot/mailinglist'
dir9 = '/mnt/stmail/Inetpub/mailroot/FullList'


def mnt1(st1IP, st1User, st1Pwd):
    '''Mount String'''
    mntStr = "{} //{}/f$ -o username='{}',password='{}' {}".format(
        mntOpt,
        st1IP,
        st1User,
        st1Pwd,
        mntLoc1
    )
    return mntStr


def readData(path):
    try:
        with open(path, newline='') as data:
            data.readline()
            reader = csv.reader(data)
            for row in map(dataRecord._make, reader):
                yield row
    except ImportError:
        print('secret.csv not found')


def listifyIP():
    for row in readData(SECRET):
        listIP.append(row)


def listifyDelete():
    for row in readData(DELETE):
        listDelete.append(row)


def execBash(chain):
    process = subprocess.Popen(
        '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(chain.encode('utf-8'))
    print(out.decode('utf-8'))


class cli(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, Keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


# prompt options
while 1:
    user_input = prompt(u'mailREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli()
                        )
    if user_input == 'mntSt1':
        #  REFERENCE
        #  chain = mntSt1
        #  chainBash.extend('ls')
        #  chain = '; '.join(chainBash)
        listifyIP()
        st1IP = [x.ip for x in listIP if x[0] == 'stMailDI'][0]
        st1User = [x.user for x in listIP if x[0] == 'stMailDI'][0]
        st1Pwd = [x.pwd for x in listIP if x[0] == 'stMailDI'][0]
        chain = mnt1(st1IP, st1User, st1Pwd)
        print(chain)
        execBash(chain)
    elif user_input == 'umntSt1':
        chain = 'sudo umount {}' .format(mntLoc1)
        print(chain)
        execBash(chain)
    elif user_input == 'check':
        listifyIP()
        print(listIP)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
