import csv
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

keywords = [x['name'] for x in ipList]
print(keywords.append('exit'))


def login(ip, user, pwd):
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
        print(s.before.decode('unicode_escape'))
        s.interact()


class iceCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    user_input = prompt(u'iceREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=iceCompleter(),
                        vi_mode=True,
                        )
    if user_input in [x['name'] for x in ipList]:
        user = [x['user'] for x in ipList if x['name'] == user_input][0]
        ip = [x['ip'] for x in ipList if x['name'] == user_input][0]
        pwd = [x['pwd'] for x in ipList if x['name'] == user_input][0]
        login(ip, user, pwd)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
