import subprocess
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

# define vars
Keywords = ['mntMail', 'exit']
mntLoc1 = '/mnt/stmail'
mntLoc2 = '/mnt/stmail02'


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
    user_input = prompt(u'gitgud>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=cli(),
                        vi_mode=True,
                        )
    if user_input == 'check':
        chainBash = ['cd {}'.format(mntLoc1)]
        chainBash.extend('ls')
        chain = '; '.join(chainBash)
        print(chain)
        execBash(chain)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
