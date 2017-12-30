import subprocess
from time import localtime, strftime
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

# define vars
Keywords = ['dot', 'sys', 'vim', 'pull', 'exit']
time = strftime("%Y-%m-%d %H:%M:%S", localtime())
cmd = 'git commit -m "' + time + '"'
pathdot = '~/m/dotfiles'
pathsys = '~/m/sys'
pathvim = '~/m/vim'

# array for rsync
arrdot = [
    '~/.xonshrc',
    '~/.ptpython/config.py',
    '~/.tmux.conf.local',
    '~/.vimrc',
    '~/.config/xonsh/config.json',
    '~/.config/alacritty/alacritty.yml',
    '~/.bashrc',
    '~/.config/nvim/init.vim',
    '~/.config/fish/config.fish',
]

# array for github
arrgit = [
    'git add -A',
    cmd,
    'git push'
]


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

    if user_input == 'dot':
        # chain bash commands for dotfiles
        listBash = ['rsync -avz {} {}'.format(x, pathdot)
                    for x in arrdot]
        listBash.append('cd ' + pathdot)
        listBash.extend(arrgit)
        chain = '; '.join(listBash)
        execBash()
    elif user_input == 'sys':
        listBash = ['cd ' + pathsys]
        listBash.extend(arrgit)
        chain = '; '.join(listBash)
        execBash()
    elif user_input == 'vim':
        listBash = ['cd ' + pathvim]
        listBash.extend(arrgit)
        chain = '; '.join(listBash)
        execBash()
    elif user_input == 'pull':
        chainBash = ['cd {}'.format(pathdot)]
        chainBash.extend(arrgit)
        chain = '; '.join(chainBash)
        print(chain)
        execBash(chain)
        chainBash = ['cd {}'.format(pathsys)]
        chainBash.extend(arrgit)
        chain = '; '.join(chainBash)
        print(chain)
        execBash(chain)
        chainBash = ['cd {}'.format(pathvim)]
        chainBash.extend(arrgit)
        chain = '; '.join(chainBash)
        print(chain)
        execBash(chain)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
