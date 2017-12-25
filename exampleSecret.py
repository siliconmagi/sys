# example secret object


class ssh:
    def __init__(self, user, pwd, ip):
        self.user = user
        self.pwd = pwd
        self.ip = ip


amo9 = ssh('root', 'password', '127.0.0.1')
