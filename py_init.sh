#!/usr/bin/env bash
#inital the python module install
 
yum -y install gcc gcc-*
sleep 1
 
yum -y install python-devel
sleep 1
 
yum -y install sqlite-devel
sleep1
 
wget http://peak.telecommunity.com/dist/ez_setup.py 
python ez_setup.py
sleep 1
easy_install pip
sleep 1
yum -y install python-devel
sleep 1
pip install termcolor
sleep 2
pip install processing
sleep 1
pip install pycrypto
sleep 2
pip install paramiko
 
#install django
pip install Django==1.5.1
sleep 1
pip install pysqlite
