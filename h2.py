import csv
from PIL import Image
import subprocess
import time
import os
import cv2
import pyscreenshot as ImageGrab
import pytesseract
import sqlite3

# rdesktop options
option = 'rdesktop -g 1920x1000 -x 0x81'
# setup sqlite
conn = sqlite3.connect('hour.db')
c = conn.cursor()
c.execute('drop table if exists Servers')
c.execute('CREATE TABLE {tn} (\
          {c1} {t1} PRIMARY KEY,\
          {c2} {t2})'.format(
    tn='Servers',
    c1='name',
    t1='text',
    c2='out',
    t2='text',
)
)

# read csv
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


def execBash(bashChain):
    '''execute bash chain'''
    process = subprocess.Popen(
        '/bin/bash',
        stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        # necessary?
        close_fds=True
    )
    out, err = process.communicate(bashChain.encode('utf-8'))


def login(nameX):
    """input: nameX, output: rdesktop connection string"""
    # extract connection info
    print(nameX)
    ip = [x['ip'] for x in ipList if x['name'] == nameX][0]
    user = [x['user'] for x in ipList if x['name'] == nameX][0]
    pwd = [x['pwd'] for x in ipList if x['name'] == nameX][0]
    bashChain = "{} -u {} -p '{}' {}".format(option, user, pwd, ip)
    execBash(bashChain)


# fork process


def grab(server):
    try:
        pid = os.fork()
    except OSError:
        exit("Could not create a child process")
    # child process
    if pid == 0:
        time.sleep(3)
        # comp right
        #  img = ImageGrab.grab(bbox=(605, 350, 685, 420))
        # comp left
        img = ImageGrab.grab(bbox=(1940, 350, 2050, 420))
        #  img2 = img.resize((80, 70), Image.ANTIALIAS)
        img2 = img.resize((195, 140), Image.ANTIALIAS)
        #  img = ImageGrab.grab()
        img2.save("ots.png")
        img2 = cv2.imread('ots.png')
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('ots.png', gray)
        os.system('pkill rdesktop')
        text = pytesseract.image_to_string(
            Image.open(os.path.abspath('ots.png')))
        # remove all rows from table Emails
        #  c.execute('delete from Servers')
        # save list of tuples to sqlite table
        t0 = (server, text.encode('utf-8'))
        sql = 'insert into Servers (name, out) values (?,?)'
        c.execute(sql, t0)
        conn.commit()
        # regex extract text before 'trac'
        #  print(text.encode('utf-8'))
        exit()
    # parent process
    login(server)
    #  login('psp10san')
    #  print('ots.png complete')
    #  print('psp10san.png complete')


grab('ots10san1')
grab('psp10san')
sql = 'select {cn} from {tn} where {ct}="ots10san1"'.format(
    cn='out',
    tn='Servers',
    ct='name')
c.execute(sql)
sRows = c.fetchone()
print(type(sRows))
print(sRows)
print(sRows[1])

conn.close()
