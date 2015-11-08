import re

"""Returns Hit Count for Firefox"""

def grep(lines,pattern="Firefox"):
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line): yield line

def increment(lines):
    num = 0
    for line in lines:
        num += 1
    return num

wwwlog = open("/home/noahgift/logs/noahgift.com-combined-log")
column = (line.rsplit(None,1)[1] for line in wwwlog)
match  = grep(column)
count = increment(match)
print "Total Number of Firefox Hits: %s" % count
