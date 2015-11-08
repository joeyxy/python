#!/usr/bin/env python
import optparse
import os

def main():
    p = optparse.OptionParser(description="Python 'ls' command clone",
                                prog="pyls",
                                version="0.1a",
                                usage="%prog [directory]")
    p.add_option("--chatty", "-c", action="store", type="choice",
                    dest="chatty",
                    choices=["normal", "verbose", "quiet"],
                    default="normal")
    options, arguments = p.parse_args()
    print options
    if len(arguments) == 1:
        if options.chatty == "verbose":
            print "Verbose Mode Enabled"
        path = arguments[0]
        for filename in os.listdir(path):
            if options.chatty == "verbose":
                print "Filename: %s " % filename
            elif options.chatty == "quiet":
                pass
            else:
                print filename
    else:
        p.print_help()
if __name__ == '__main__':
    main()
