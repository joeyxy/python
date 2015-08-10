#!/usr/bin/env python

import os
import argpparse
import smtplib
import zipfile
import tempfile
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def email_dir_zipped(sender,recipient):
	zf = tempfile.TemporaryFile(prefix='mail',suffix='.zip')
	zip = zipfile.ZipFile(zf,'w')
	print "Zipping current dir:%s"