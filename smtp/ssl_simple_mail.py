#!/usr/bin/env python

#coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sender = 'support@nearfor.me'
subject = 'python test mail'
smtpserver = 'email-smtp.us-west-2.amazonaws.com'
username = ''
password = ''

receiver = raw_input('input the receiver: ')

msg = MIMEText('hello','text')
msg['Subject'] = Header(subject,'utf-8')

smtp = smtplib.SMTP()
smtp.connect('email-smtp.us-west-2.amazonaws.com')
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender,receiver, msg.as_string())
smtp.quit()