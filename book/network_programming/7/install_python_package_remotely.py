#!/usr/bin/env python

from getpass import getpass
from fabric.api import settings,run,env,prompt

def remote_server():
	env.hosts = ['192.168.10.11']
	env.user = prompt('Enter user name: ')
	env.password = getpass('Enter passowrd: ')

def install_package():
	run("yum list php*")