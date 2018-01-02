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
# initialize vars
Keywords = ['mntStMailDI', 'umntStMailDI', 'check', 'exit']
ipList = []
deleteList = []
mntOpt = 'sudo mount -t cifs --ro'
#  mntOpt = 'sudo mount -t cifs --rw'
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'

# directories to check
# .txt, .cnt
dir1 = '/mnt/stmail/Inetpub/scripts/dreamersi/CheckAccount'
# folders
dir2 = '/mnt/stmail/Inetpub/scripts/dreamersi/Vendors'
# folders
dir3 = '/mnt/stmail/Inetpub/wwwroot/dreamersi/vendors'
# folders
dir4 = '/mnt/stmail/Inetpub/mailroot/Mailbox'
# folders
dir5 = '/mnt/stmail/Inetpub/mailroot/UserInf'
# youthchallenge010001, yoshidarivervi010001 (14 char)
dir6 = '/mnt/stmail/Inetpub/mailroot/UserExtra'
# folders
dir7 = '/mnt/stmail/Inetpub/mailroot/SpamBox'
# .txt
dir8 = '/mnt/stmail/Inetpub/mailroot/mailinglist'
# nothing:
dir9 = '/mnt/stmail/Inetpub/mailroot/FullList'

# read csv into list
try:
    with open("deleteList.csv", newline="") as infile:
        reader = csv.reader(infile)
        deleteList = [line.strip() for line in infile]
except ImportError:
    print('deleteList.csv not found')

# read csvs into list of namedtuples
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


while 1:
    user_input = prompt(u'mailREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli()
                        )
    if user_input == 'mntStMailDI':
        #  REFERENCE
        #  chain = mntSt1
        #  chainBash.extend('ls')
        #  chain = '; '.join(chainBash)
        chain = mnt1()
        print(chain)
        execBash(chain)
    elif user_input == 'umntStMailDI':
        chain = 'sudo umount {}' .format(mntLoc1)
        print(chain)
        execBash(chain)
    elif user_input == 'check':
        chain = 'cd {}; ls'.format(dir1)
        print(chain)
        execBash(chain)
    elif user_input == 'deleteList':
        print(deleteList)
    elif user_input == 'd1':
        addExt = [s + '.txt' for s in deleteList]
        sample = [x for x in os.listdir(dir1) if x in addExt]
        print(sample)
    elif user_input == 'd2':
        sample = [x for x in os.listdir(dir2) if x in deleteList]
        # write results to d2.txt
        with open('d2.txt', 'w') as file_handler:
            for item in sample:
                file_handler.write("{}\n".format(item))
                print(sample)
    elif user_input == 'd3':
        sample = [x for x in os.listdir(dir3) if x in deleteList]
        print(sample)
    elif user_input == 'd4':
        sample = [x for x in os.listdir(dir4) if x in deleteList]
        print(sample)
    elif user_input == 'd5':
        sample = [x for x in os.listdir(dir5) if x in deleteList]
        print(sample)
    elif user_input == 'd6':
        # WORKING:
        # return l from deleteList where matching charSlice
        charSlice = [x[0:14] for x in deleteList]
        t = []
        l2 = os.listdir(dir6)
        for x in charSlice:
            regex = re.compile(x)
            s = [l for l in l2 for m in [regex.search(l)] if m]
            #  t.append(s[0])
            print(s)
        #  print(t)
    elif user_input == 'd7':
        sample = [x for x in os.listdir(dir6) if x in deleteList]
        print(sample)
    elif user_input == 'test':
        charSlice = [x[0:14] for x in deleteList]
        regex = re.compile('youthchallenge')
        t = []
        for x in charSlice:
            s = [l for l in deleteList for m in [regex.search(x)] if m]
            t.append(s)
        print(t)
    elif user_input == 't2':
        charSlice = [x[0:14] for x in deleteList]
        t = []
        for a in charSlice:
            regex = re.compile(a)
            s = regex.search(a)
            #  s = [l for l in deleteList for m in [regex.search(a)] if m]
            print(s.group())
            #  t.append(s)
        print(t)
    elif user_input == 't3':
        charSlice = [x[0:14] for x in deleteList]
        regex = re.compile('^a')
        s = [l for l in deleteList for m in [regex.search(l)] if m]
        print(s)
    elif user_input == 'regex':
        charSlice = [x[0:14] for x in deleteList]
        regex = re.compile('youthchallenge')
        sample = [l for l in deleteList for m in [regex.search(l)] if m]
        print(sample)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
