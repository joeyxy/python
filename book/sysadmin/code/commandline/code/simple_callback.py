#!/usr/bin/env python
import optparse


def main():
    p = optparse.OptionParser()

    def my_little_callback(option, opt_str, value, parser):
        print "ran"
        #setattr(p.values, option.dest, 1)
    p.add_option('--foo', action="callback", callback=my_little_callback, dest="foo")
    options, arguments = p.parse_args()
    if options.foo:
        print options.foo
if __name__ == '__main__':
    main()
