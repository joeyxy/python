#!/usr/bin/env python
#David Beazly
import threading
import urllib

class FetchUrlThread(threading.Thread):
    def __init__(self, url, filename):
        threading.Thread.__init__(self)
        self.url = url
        self.filename = filename
    def run(self):
        print self.getName(), 'Fetching ', self.url
        urllib.urlretrieve(self.url, self.filename)

urls = [ ('http://www.python.org', '/tmp/index.html'),
        ('http://noahgift.com', 'index.html'),
        ('http://blog.noahgift.com', 'index.html')]

for url,file in urls:
    t = FetchUrlThread(url, file)
    t.start()


