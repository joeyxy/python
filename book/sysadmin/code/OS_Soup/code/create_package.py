#!/usr/bin/env python
from fingerprint import fingerprint
from subprocess import call

os = fingerprint()

#Gets epm keyword correct
epm_keyword = {"ubuntu":"dpkg", "redhat":"rpm", "SunOS":"pkg", "osx":"osx"}

if epm_keyword.has_key(os):
        platform_cmd = epm_keyword[os]

subprocess.call("epm -f %s helloEPM hello_epm.list" % platform_cmd, shell=True)

