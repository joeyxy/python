#!/usr/bin/env python

import getopt
import sys
import time

def dosomething(*args):
    """ do something useful """
    print "I am running"

def main():

  daemon = False
  sleep = 1
  quiet = False

  short_args = "qds:h"
  long_args = ["quiet",
               "daemon",
               "sleep=None",
               "help",
               ]
  try:
      opts, args = getopt.getopt(sys.argv[1:], short_args, long_args)
  except getopt.GetoptError:
      print __doc__
      sys.exit(1)

  for option, value in opts:

      if option in ("-h", "--help"):
          print __doc__
          sys.exit(2)

      if option in ("-q", "--quiet"):
          quiet = True

      if option in ("-d", "--daemon"):
          daemon = True

      if option in ("-s", "--sleep"):
          sleep = int(value)

  if sleep is not None and not daemon:
      print 'Sleep is not meaningful unless running in daemon mode.'
      sys.exit(1)

  while True:
      dosomething(quiet)
      if daemon:
          time.sleep(sleep)
      else:
          break

if __name__ == '__main__':
  main()
