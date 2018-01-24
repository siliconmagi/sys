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

# setup bounding box from screengrab
stX1 = 13
stY1 = 150
stX2 = 200
stY2 = 200
stXR = int((stX2 - stX1) * 2.5)
stYR = int((stY2 - stY1) * 1.5)

# setup bounding box from screengrab
sanX1 = 580
sanY1 = 350
sanX2 = 685
sanY2 = 420
sanXR = int((sanX2 - sanX1) * 2)
sanYR = int((sanY2 - sanY1) * 1.5)

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
        file0 = '{}.png'.format(server)
        time.sleep(5)
        if server == 'stMailDI':
            bbX1 = stX1
            bbY1 = stY1
            bbX2 = stX2
            bbY2 = stY2
            bbXR = stXR
            bbYR = stYR
        else:
            bbX1 = sanX1
            bbY1 = sanY1
            bbX2 = sanX2
            bbY2 = sanY2
            bbXR = sanXR
            bbYR = sanYR
        img = ImageGrab.grab(bbox=(bbX1, bbY1, bbX2, bbY2))
        img2 = img.resize((bbXR, bbYR), Image.ANTIALIAS)
        img2.save(file0)
        img2 = cv2.imread(file0)
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(file0, gray)
        os.system('pkill rdesktop')
        text = pytesseract.image_to_string(
            Image.open(os.path.abspath(file0)))
        # save list of tuples to sqlite table
        t0 = (server, text.encode('utf-8'))
        sql = 'insert into Servers (name, out) values (?,?)'
        c.execute(sql, t0)
        conn.commit()
        exit()
    # parent process
    login(server)


grab('stMailDI')
grab('ots10san1')
grab('psp10san')
conn.close()
