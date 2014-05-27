#!/usr/bin/env bash

yum -y install python-devel python-setuptools
sleep 1;
easy_install BeautifulSoup
sleep 1;
wget https://github.com/joeyxy/python/blob/master/crawler/warrantycheck.py
chmod +x warrantycheck.py
