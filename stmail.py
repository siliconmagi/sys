from collections import namedtuple
import csv
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder


SECRET = 'secret.csv'
fields = ('name', 'ip', 'user', 'pwd')
dataRecord = namedtuple('dataRecord', fields)


def readData(path):
    try:
        with open(path, newline='') as data:
            data.readline()            # Skip the header
            reader = csv.reader(data)  # Create a regular tuple reader
            for row in map(dataRecord._make, reader):
                yield row
    except ImportError:
        print('secret.csv not found')

def listData():
    for row in readData(SECRET):
        print(row)


# define vars
Keywords = ['mntSt1', 'exit']
mntOpt = 'sudo mount -t cifs --rw'
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'
st1IP = [x['ip'] for x in ipList if x['name'] == 'stmailDI'][0]
st1USER = [x['user'] for x in ipList if x['name'] == 'stmailDI'][0]
st1PWD = [x['pwd'] for x in ipList if x['name'] == 'stmailDI'][0]

# mount commands
#  [x['name'] for x in ipList if x['name'] == user_input][0]
#  mntSt1 = '{} //{}/f$ -o username={},password={} {}'.format(
#  mntOpt,
#  st1IP,
#  st1USER,
#  st1PWD,
#  mntLoc1
#  )


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
    user_input = prompt(u'popREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli(),
                        vi_mode=True,
                        )
    if user_input == 'mntSt1':
        #  chain = mntSt1
        #  chainBash.extend('ls')
        #  chain = '; '.join(chainBash)
        #  print(deleteList)
        print(ipList)
        #  execBash(chain)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
