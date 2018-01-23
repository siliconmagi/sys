import csv
import subprocess
#  import pexpect
from pexpect import pxssh
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from fuzzyfinder import fuzzyfinder

# rdesktop options
option = 'rdesktop -g 1280x960'

# create list of connection dictionaries from csv

try:
    ipList = []
    with open('secret.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            ipList.append(
                {'name': row[0],
                    'ip': row[1],
                    'user': row[2],
                    'pwd': row[3]})
except ImportError:
    print('secret.csv not found')

# create list of banned ips
try:
    banList = []
    with open('ban.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            banList.append(row[0])
except ImportError:
    print('ban.csv not found')

# gen keywords from ipList
keywords = [x['name'] for x in ipList]
keywords.extend(['exit', 'banIP'])


def execBash(bashChain):
    process = subprocess.Popen(
        '/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(bashChain.encode('utf-8'))
    print(out.decode('utf-8'))


def loginSSH():
    s = pxssh.pxssh()
    s.SSH_OPTS = "-o 'RSAAuthentication=no' -o 'PubKeyAuthentication=no'"
    s.login(ip, user, pwd)
    #  s.sendline('whoami;uname -a')
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


def banIP(banList):
    """handles banning on firewall"""
    try:
        def cycle():
            for x in banList:
                log.append('cycle start')
                cmd = 'network-object host {}'.format(x)
                print(cmd)
                s.sendline(cmd)
                log.append(s.before)
                s.expect('config.*')
        ip = [x['ip'] for x in ipList if x['name'] == 'firewall'][0]
        user = [x['user'] for x in ipList if x['name'] == 'firewall'][0]
        pwd = [x['pwd'] for x in ipList if x['name'] == 'firewall'][0]
        ip2 = [x['ip'] for x in ipList if x['name'] == 'firewall2'][0]
        user2 = [x['user'] for x in ipList if x['name'] == 'firewall2'][0]
        pwd2 = [x['pwd'] for x in ipList if x['name'] == 'firewall2'][0]
        log = []
        s = pxssh.pxssh()
        s.login(ip, user, pwd)
        s.sendline('whoami')
        s.prompt()
        log.append(s.before.decode('unicode_escape'))
        s.sendline('ssh {}@{}'.format(user2, ip2))
        s.expect('assword.*: ')
        s.sendline(pwd2)
        log.append(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('en')
        s.expect('assword.*: ')
        s.sendline('')
        log.append(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('conf t')
        log.append(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('object-group network blocklist')
        log.append(s.before.decode('unicode_escape'))
        s.expect('config.*')
        cycle()
        s.sendline('exit')
        s.expect('PDCC.*A')
        s.sendline('exit')
        s.expect('PDCC.*A')
        s.sendline('exit')
        s.expect('PDCC.*A')
        #  print(log)
        #  s.interact()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


def loginFirewall():
    """handles login to firewall from login function"""
    try:
        ip2 = [x['ip'] for x in ipList if x['name'] == 'firewall2'][0]
        user2 = [x['user'] for x in ipList if x['name'] == 'firewall2'][0]
        pwd2 = [x['pwd'] for x in ipList if x['name'] == 'firewall2'][0]
        s = pxssh.pxssh()
        s.login(ip, user, pwd)
        s.sendline('whoami')
        s.prompt()
        print(s.before.decode('unicode_escape'))
        s.sendline('ssh {}@{}'.format(user2, ip2))
        s.expect('assword.*: ')
        s.sendline(pwd2)
        print(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('en')
        s.expect('assword.*: ')
        s.sendline('')
        print(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('conf t')
        print(s.before.decode('unicode_escape'))
        s.expect('PDCC.*A')
        s.sendline('object-group network blocklist')
        print(s.before.decode('unicode_escape'))
        s.interact()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)


def login(name, ip, user, pwd):
    """handles login"""
    # login rdesktop
    if user == 'administrator' or user == 'sysop':
        bashChain = "{} -u {} -p '{}' {}".format(option, user, pwd, ip)
        execBash(bashChain)
    # login firewall
    elif name == 'firewall':
        loginFirewall()
    elif name == 'ltpop01':
        print('ltpop')
    # login ssh where ipList has no password
    # todo: ambk10 interact or run script
    elif pwd == 'none':
        bashChain = "ssh {}@{}".format(user, ip)
        execBash(bashChain)
    # else ssh: user, pass
    else:
        loginSSH()


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

    # check input
    if user_input in [x['name'] for x in ipList]:
        # parse and store user input
        name = [x['name'] for x in ipList if x['name'] == user_input][0]
        ip = [x['ip'] for x in ipList if x['name'] == user_input][0]
        user = [x['user'] for x in ipList if x['name'] == user_input][0]
        pwd = [x['pwd'] for x in ipList if x['name'] == user_input][0]
        login(name, ip, user, pwd)
    elif user_input == 'banIP':
        banIP(banList)
    elif user_input == 'exit':
        print('exit')
        exit()
    else:
        print('Input not handled')
