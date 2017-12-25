import pexpect
import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder
from secret import stmail, stmail2

# define vars
Keywords = ['mntMail', 'exit']
cred1 = [stmail.user, stmail.pwd, stmail.ip]
cred1 = [stmail2.user, stmail2.pwd, stmail2.ip]
pathdot = '~/p/dotfiles'
pathsys = '~/p/sys'
pathvim = '~/p/vim'
mntOpt = 'sudo mount -t cifs --rw'
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'
mntSt1 = '{} //{}/f$ -o username={},password={} {}'.format(
    mntOpt,
    stmail.ip,
    stmail.user,
    stmail.pwd,
    mntLoc1)
mntSt2 = '{} //{}/f$ -o username={},password={} {}'.format(
    mntOpt,
    stmail.ip,
    stmail.user,
    stmail.pwd,
    mntLoc1)


# array setup for github
arr = [
]


def execBash():
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
    user_input = prompt(u'stmail>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli(),
                        vi_mode=True,
                        )

    if user_input == 'mntMail':
        chain = mntSt1
        execBash()
        child = pexpect.spawn(execBash)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
