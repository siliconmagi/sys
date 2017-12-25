import pexpect
from secret import (
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
)

# connection constructor


class conn:
    def __init__(self, user, pwd, ip):
        self.user = user
        self.pwd = pwd
        self.ip = ip

    # ssh with psp, login sudo
    def psp(self):
        ssh = 'ssh ' + self.user + '@' + self.ip
        child = pexpect.spawn(ssh)
        child.expect('assword.*: ')
        child.sendline(self.pwd)
        child.expect('psp.*')
        child.sendline('sudo su -')
        child.expect('assword.*: ')
        child.sendline(self.pwd)
        child.expect('root.*')
        child.sendline('uname -a')
        print(child.before.decode('unicode_escape'))
        return child.interact()

    # ssh as root
    def root(self):
        ssh = 'ssh ' + self.user + '@' + self.ip
        child = pexpect.spawn(ssh)
        child.expect('assword.*: ')
        child.sendline(self.pwd)
        child.expect('root.*')
        child.sendline('uname -a')
        print(child.before.decode('unicode_escape'))
        return child.interact()


# init servers
amo5 = conn(amo5.user, amo5.pwd, amo5.ip)
amo7 = conn(amo7.user, amo7.pwd, amo7.ip)
amo8 = conn(amo8.user, amo8.pwd, amo8.ip)
amo9 = conn(amo9.user, amo9.pwd, amo9.ip)
amo10 = conn(amo10.user, amo10.pwd, amo10.ip)

amp1 = conn(amp1.user, amp1.pwd, amp1.ip)
amp2 = conn(amp2.user, amp2.pwd, amp2.ip)

lts1 = conn(lts1.user, lts1.pwd, lts1.ip)
lts2 = conn(lts2.user, lts2.pwd, lts2.ip)

smtp2 = conn(smtp2.user, smtp2.pwd, smtp2.ip)
ns1 = conn(ns1.user, ns1.pwd, ns1.ip)
