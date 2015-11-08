#!/usr/bin/env python
#A simple python script we will package
#Distutils Example.  Version 0.1

class DistutilsClass(object):
    """This class prints out a statement about itself."""
    def __init__(self):
        print "Hello, I am a distutils distributed script." \
            "All I do is print this message."

if __name__ == '__main__':
    DistutilsClass()
