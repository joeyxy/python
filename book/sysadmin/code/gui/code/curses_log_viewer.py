#!/usr/bin/env python

"""
Curses based Apache log viewer

Usage:
    
    curses_log_viewer.py logfile

This will start an interactive, keyboard driven log viewing application.  Here
are what the various key presses do: 

    u/d   - scroll up/down
    t     - go to the top of the log file
    q     - quit
    b/h/s - sort by bytes/hostname/status
    r     - restore to initial sort order

"""

import curses
from apache_log_parser_regex import dictify_logline
import sys
import operator

class CursesLogViewer(object):
    def __init__(self, logfile=None):
        self.screen = curses.initscr()
        self.curr_topline = 0
        self.logfile = logfile
        self.loglines = []

    def page_up(self):
        self.curr_topline = self.curr_topline - (2 * curses.LINES)
        if self.curr_topline < 0:
            self.curr_topline = 0
        self.draw_loglines()

    def page_down(self):
        self.draw_loglines()

    def top(self):
        self.curr_topline = 0
        self.draw_loglines()

    def sortby(self, field):
        self.loglines.sort(key=operator.itemgetter(field))
        self.top()

    def set_logfile(self, logfile):
        self.logfile = logfile
        self.load_loglines()

    def load_loglines(self):
        self.loglines = []
        logfile = open(self.logfile, 'r')
        for i, line in enumerate(logfile):
            line_dict = dictify_logline(line)
            self.loglines.append((i + 1, line_dict['remote_host'], 
                line_dict['status'], int(line_dict['bytes_sent']), line.rstrip()))
        logfile.close()
        self.draw_loglines()

    def draw_loglines(self):
        self.screen.clear()
        status_col = 4
        bytes_col = 6
        remote_host_col = 16
        status_start = 0
        bytes_start = 4
        remote_host_start = 10
        line_start = 26
        logline_cols = curses.COLS - status_col - bytes_col - remote_host_col - 1
        for i in range(curses.LINES):
            c = self.curr_topline
            try:
                curr_line = self.loglines[c]
            except IndexError:
                break
            self.screen.addstr(i, status_start, str(curr_line[2]))
            self.screen.addstr(i, bytes_start, str(curr_line[3]))
            self.screen.addstr(i, remote_host_start, str(curr_line[1]))
            self.screen.addnstr(i, line_start, str(curr_line[4]), logline_cols)
            self.curr_topline += 1
        self.screen.refresh()

    def main_loop(self, stdscr):
        self.load_loglines()
        while True:
            c = self.screen.getch()
            try:
                c = chr(c)
            except ValueError:
                continue
            if c == 'd': 
                self.page_down()
            elif c == 'u': 
                self.page_up()
            elif c == 't': 
                self.top()
            elif c == 'b': 
                self.sortby(3)
            elif c == 'h': 
                self.sortby(1)
            elif c == 's': 
                self.sortby(2)
            elif c == 'r': 
                self.sortby(0)
            elif c == 'q': 
                break

if __name__ == '__main__':
    infile = sys.argv[1]
    c = CursesLogViewer(infile)
    curses.wrapper(c.main_loop)
