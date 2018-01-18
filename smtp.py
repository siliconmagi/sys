import smtplib

smtp = ''
port = 465
myEmail = 'siliconmagi@yandex.com'
pwd = ''
emailTo = ''
msg = 'hi'
smtpObj = smtplib.SMTP(smtp, port)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(myEmail, pwd)
smtpObj.sendmail(myEmail, emailTo, msg)
