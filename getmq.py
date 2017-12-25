from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder
#  from pexpect import pxssh
from ifpex import (
    amo5,
    amo7,
    amo8,
    amo9,
    amo10,
    amp1,
    amp2,
    lts1,
    lts2,
    smtp2,
    ns1,
    ns2,
    blog,
    kvm,
)
#  from pygments.lexers.sql import SqlLexer

spamKeywords = ['amo5', 'amo7', 'amo8', 'amo9', 'amo10', 'amp1', 'amp2',
                'lts1', 'lts2', 'smtp2', 'ns1', 'ns2', 'blog', 'exit', 'kvm']


class spamCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, spamKeywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    user_input = prompt(u'spamREPL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=spamCompleter(),
                        vi_mode=True,
                        )

    if user_input == 'amo5':
        amo5.root()
    elif user_input == 'amo7':
        amo7.root()
    elif user_input == 'amo8':
        amo8.root()
    elif user_input == 'amo9':
        amo9.root()
    elif user_input == 'amo10':
        amo10.root()
    elif user_input == 'amp1':
        amp1.root()
    elif user_input == 'amp2':
        amp2.root()
    elif user_input == 'lts1':
        lts1.root()
    elif user_input == 'lts2':
        lts2.root()
    elif user_input == 'smtp2':
        smtp2.root()
    elif user_input == 'ns1':
        ns1.root()
    elif user_input == 'ns2':
        ns2.root()
    elif user_input == 'blog':
        blog.root()
    elif user_input == 'kvm':
        kvm.root()
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Invalid Entry')
