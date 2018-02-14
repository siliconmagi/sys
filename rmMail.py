import os
import re
import csv
from collections import namedtuple
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder


# SETUP
# dictionary globals
dicM1 = {
    # .txt, .cnt
    'dir1': '/mnt/stmail/Inetpub/scripts/dreamersi/CheckAccount',
    # folders
    'dir2': '/mnt/stmail/Inetpub/scripts/dreamersi/Vendors',
    # folders
    'dir3': '/mnt/stmail/Inetpub/wwwroot/dreamersi/vendors',
    # folders
    'dir4': '/mnt/stmail/Inetpub/mailroot/Mailbox',
    # folders
    'dir5': '/mnt/stmail/Inetpub/mailroot/UserInf',
    # youthchallenge010001, yoshidarivervi010001 (14 char)
    # files
    'dir6': '/mnt/stmail/Inetpub/mailroot/UserExtra',
    # folders
    'dir7': '/mnt/stmail/Inetpub/mailroot/SpamBox',
    # .txt
    'dir8': '/mnt/stmail/Inetpub/mailroot/mailinglist'
}
dicM2 = {
    # .txt, .cnt
    'dir1': '/mnt/stmail02/Inetpub/scripts/dreamersi/CheckAccount',
    # folders
    'dir2': '/mnt/stmail02/Inetpub/scripts/dreamersi/Vendors',
    # folders
    'dir3': '/mnt/stmail02/Inetpub/wwwroot/dreamersi/vendors',
    # folders
    'dir4': '/mnt/stmail02/Inetpub/mailroot/Mailbox',
    # folders
    'dir5': '/mnt/stmail02/Inetpub/mailroot/UserInf',
    # youthchallenge010001, yoshidarivervi010001 (14 char)
    # files
    'dir6': '/mnt/stmail02/Inetpub/mailroot/UserExtra',
    # folders
    'dir7': '/mnt/stmail02/Inetpub/mailroot/SpamBox',
    # .txt
    'dir8': '/mnt/stmail02/Inetpub/mailroot/mailinglist'
}
Keywords = ['mntStMailDI', 'umntStMailDI', 'exit']
Keywords.extend([x for x in dicM1])
print(Keywords)
ipList = []
deleteList = []
nestedList = []
fileList = ['dir1', 'dir6', 'dir8']
folderList = ['dir2', 'dir3', 'dir4', 'dir5', 'dir7']
mntOpt = 'sudo mount -t cifs --ro'
#  mntOpt = 'sudo mount -t cifs --rw'
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'

# read deleteList.csv into list
try:
    with open("deleteList.csv", newline="") as infile:
        reader = csv.reader(infile)
        deleteList = [line.strip() for line in infile]
except ImportError:
    print('deleteList.csv not found')

# read secret.csv into list of namedtuples
try:
    with open("secret.csv", newline="") as infile:
        reader = csv.reader(infile)
        Data = namedtuple("Data", next(reader))
        for data2 in map(Data._make, reader):
            ipList.append(data2)
except ImportError:
    print('secret.csv not found')

# extract stMailDI login
mailIP = [x.ip for x in ipList if x[0] == 'stMailDI'][0]
mailUser = [x.user for x in ipList if x[0] == 'stMailDI'][0]
mailPwd = [x.pwd for x in ipList if x[0] == 'stMailDI'][0]


def dirN(nameX, dirX):
    '''
    Dynamic regex searches each item in deleteList to dirList
    Returns successful search instances as a list
    '''
    outList = []
    dirList = os.listdir(dirX)
    for x in deleteList:
        regex = re.compile(x)
        # dynamic regex search each item in deleteList against dirList
        s = [l for l in dirList for m in [regex.search(l)] if m]
        outList.append(s)
    # write list of result instances
    with open('{}.csv'.format(nameX), 'w') as file_handler:
        for item in outList:
            file_handler.write("{}\n".format(item))
    # create flatList of shell commands from outList
    flatList = [l for sublist in outList for l in sublist]
    # check file type
    if nameX in fileList:
        c = ['rm {}/{}'.format(dicM1[nameX], i)
             for i in flatList]
    elif nameX in folderList:
        c = ['rm -rf {}/{}'.format(dicM1[nameX], i)
             for i in flatList]
    else:
        print('nameX not recognized')
    print(c)
    # write flatList
    with open('{}cmd.csv'.format(nameX), 'w') as file_handler:
        for item in c:
            file_handler.write("{}\n".format(item))


def mnt1():
    '''Mount String Gen'''
    mntStr = "{} //{}/f$ -o username='{}',password='{}' {}".format(
        mntOpt,
        mailIP,
        mailUser,
        mailPwd,
        mntLoc1
    )
    return mntStr


def execBash(chain):
    '''bash chain handler'''
    process = subprocess.Popen(
        '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(chain.encode('utf-8'))
    print(out.decode('utf-8'))


class cli(Completer):
    '''setup REPL'''
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, Keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    '''create REPL prompt'''
    user_input = prompt(u'mailREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli()
                        )
    if user_input == 'mntStMailDI':
        chain = mnt1()
        print(chain)
        execBash(chain)
    elif user_input == 'umntStMailDI':
        chain = 'sudo umount {}' .format(mntLoc1)
        print(chain)
        execBash(chain)
    # match input from dicM1 keys and autofill dirN()
    elif user_input in [x for x in dicM1]:
        nameX = user_input
        dirX = dicM1[nameX]
        dirN(nameX, dirX)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Unrecognized Input')
