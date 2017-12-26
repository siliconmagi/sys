import csv
import subprocess
from pexpect import pxssh
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder


# create list of dicts from csv
ipList = []
with open('secret.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        ipList.append({'name': row[0], 'ip': row[1],
                       'user': row[2], 'pwd': row[3]})

# gen keywords from ipList
keywords = [x['name'] for x in ipList]
keywords.append('exit')


def login(ip, user, pwd):
    if user == 'administrator' or user == 'sysop':
        option = 'rdesktop -g 1280x960'
        bashChain = "{} -u {} -p '{}' {}".format(option, user, pwd, ip)
        print(bashChain)
        # subprocess for cmds
        process = subprocess.Popen(
            '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out, err = process.communicate(bashChain.encode('utf-8'))
        print(out.decode('utf-8'))
    else:
        s = pxssh.pxssh()
        s.SSH_OPTS = "-o 'RSAAuthentication=no' -o 'PubKeyAuthentication=no'"
        s.login(ip, user, pwd)
        s.sendline('whoami;uname -a')
        before = s.before.decode('unicode_escape')
        if 'psp' in before:
            s.sendline('sudo su -')
            s.expect('assword.*: ')
            s.sendline(pwd)
            s.expect('root.*')
            s.sendline('whoami')
            print(before)
            s.interact()
        elif 'root' in before:
            print(before)
            s.interact()
        else:
            print('Unknown Login')
            print(before)
            s.interact()


class iceCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    # create prompt
    user_input = prompt(u'iceREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=iceCompleter(),
                        vi_mode=True,
                        )
    # check input against name in ipList
    if user_input in [x['name'] for x in ipList]:
        ip = [x['ip'] for x in ipList if x['name'] == user_input][0]
        user = [x['user'] for x in ipList if x['name'] == user_input][0]
        pwd = [x['pwd'] for x in ipList if x['name'] == user_input][0]
        login(ip, user, pwd)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
