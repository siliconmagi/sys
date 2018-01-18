from PIL import Image
import csv
import subprocess
import time
import os
import cv2
import pyscreenshot as ImageGrab

# rdesktop options
option = 'rdesktop -g 1920x1000'

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
    print(out.decode('utf-8'))


def login(nameX):
    """input: nameX, output: rdesktop connection string"""
    # extract connection info
    ip = [x['ip'] for x in ipList if x['name'] == nameX][0]
    user = [x['user'] for x in ipList if x['name'] == nameX][0]
    pwd = [x['pwd'] for x in ipList if x['name'] == nameX][0]
    bashChain = "{} -u {} -p '{}' {}".format(option, user, pwd, ip)
    execBash(bashChain)


def screen():
    time.sleep(3)
    img = ImageGrab.grab()
    select = img.crop((1960, 352, 2050, 420))
    # og size: 90x68
    size = select.resize((180, 136), Image.ANTIALIAS)
    size.save("ots.png")
    img2 = cv2.imread('ots.png')
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('ots.png', gray)
    os.system('pkill rdesktop')
    exit()


# fork process
try:
    pid = os.fork()
except OSError:
    exit("Could not create a child process")

# child process
if pid == 0:
    time.sleep(3)
    img = ImageGrab.grab()
    select = img.crop((1960, 352, 2050, 420))
    # og size: 90x68
    size = select.resize((180, 136), Image.ANTIALIAS)
    size.save("ots.png")
    img2 = cv2.imread('ots.png')
    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('ots.png', gray)
    os.system('pkill rdesktop')
    exit()

# parent process
login('ots')
print('ots.png complete')
