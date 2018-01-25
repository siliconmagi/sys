import sqlite3
import csv
import re
import subprocess
from pexpect import pxssh
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

# setup sqlite
conn = sqlite3.connect('neo.db')
c = conn.cursor()
c.execute('drop table if exists Emails')
c.execute('CREATE TABLE {tn} (\
          {c1} {t1} PRIMARY KEY,\
          {c2} {t2})'.format(
    tn='Emails',
    c1='email',
    t1='TEXT',
    c2='count',
    t2='INTEGER',
)
)


# global vars
mailq = "mailq | grep Jan | awk '{print $7}' | sort | uniq -c | sort -n"

#  mailq | grep Jan | grep 'ex@alpha-enterprise.co.jp' | awk '{print $1}'

#  mailq | grep Jan | grep 'h-takahashi@adrs-s.co.jp' | awk '{print $1}'


def mqFind(findX):
    return "mailq | grep Jan | grep '{}' | awk '{{print $1}}'".format(findX)


def ipFind(findX):
    return "cat /var/spool/mqueue/{}".format(findX)

#  | awk -F '*' '{print $1}' | postsuper -d -
#  mailq | grep Jan | awk '{print $7}' | sort | uniq -c | sort -n
# rdesktop options


# create list of connection dictionaries from csv
try:
    ipList = []
    with open('secret.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ipList.append(
                {
                    'name': row[0],
                    'ip': row[1],
                    'user': row[2],
                    'pwd': row[3]
                })
except ImportError:
    print('secret.csv not found')

# gen keywords from ipList
keywords = [x['name'] for x in ipList]
keywords.extend(['exit'])


def execBash(bashChain):
    process = subprocess.Popen(
        '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(bashChain.encode('utf-8'))
    print(out.decode('utf-8'))


def login(in0):
    # extract connection info from secret
    ip = [x['ip'] for x in ipList if x['name'] == in0][0]
    user = [x['user'] for x in ipList if x['name'] == in0][0]
    pwd = [x['pwd'] for x in ipList if x['name'] == in0][0]
    #  before = s.before.decode('unicode_escape')
    s = pxssh.pxssh()
    s.SSH_OPTS = "-o 'RSAAuthentication=no' -o 'PubKeyAuthentication=no'"
    s.login(ip, user, pwd)
    # send mailq command
    s.sendline(mailq)
    # match prompt
    s.prompt()
    # decode bytes object for split
    mqOut = s.before.decode()
    mqList = mqOut.split('\n')
    # strip whitespace
    s0 = [i.strip() for i in mqList]
    # remove first and last element from list
    s1 = s0[1:-1]
    # list element must contain key and value
    regex = re.compile(r'^\d <.*\w.*>')
    f0 = [m.group(0) for l in s1 for m in [regex.search(l)] if m]
    # remove brackets in email
    f1 = [re.sub('<|>', '', l) for l in f0]
    # split name
    z1 = [i.split(' ')[0] for i in f1]
    # split instances
    z2 = [i.split(' ')[1] for i in f1]
    # zip names as list of tuples
    t0 = zip(z2, z1)
    # descending order by value
    t1 = sorted(list(t0), key=lambda x: x[1])
    # remove all rows from table Emails
    c.execute('delete from Emails')
    # save list of tuples to sqlite table
    c.executemany('insert into Emails (email, count) values (?,?)', t1)
    c.execute('select * from Emails')
    r0 = c.fetchall()
    [print(row) for row in r0]
    c.execute('select * from Emails where count>1')
    r1 = c.fetchall()
    # iterate rows for message ID
    for row in r1:
        s.sendline(mqFind(row[0]))
        s.prompt()
        find0 = s.before.decode('ISO-8859-1')
        # extract str starting with 'w08' until \w
        print(find0)
        find1 = re.findall(r'(w0.*\w)', find0)
        #  print(find1)
        #  get first msgID
        find2 = 'qf{}'.format(find1[0])
        print(find2)
        s.sendline(ipFind(find2))
        s.prompt()
        # necessary encoding for message
        ip0 = s.before.decode('ISO-8859-1')
        #  print(ip0)
        # get ip using msgID
        ip1 = re.findall(r'Received:.*\[(.*)\]', ip0)[-1]
        print(ip1)

    # test cat
    s.sendline('uname')
    s.prompt()
    catOut = s.before
    print(catOut)
    #  curl ipinfo.io/210.189.28.2
    conn.commit()
    s.logout()


class iceCompleter(Completer):
    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        matches = fuzzyfinder(word_before_cursor, keywords)
        for m in matches:
            yield Completion(m, start_position=-len(word_before_cursor))


while 1:
    # create prompt
    user_input = prompt(u'mail>',
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=iceCompleter(),
                        vi_mode=True,
                        )

    # check input
    if user_input in [x['name'] for x in ipList]:
        login(user_input)
    elif user_input == 'exit':
        conn.close()
        exit()
    else:
        print('Unable to handle input')
