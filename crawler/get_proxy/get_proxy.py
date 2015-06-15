from bs4 import BeautifulSoup
import urllib2
import sys
 
 
of = open('proxy.txt' , 'w')
 
for page in range(1, 160):
    print "start at [+]page %s" % page
    try:
        html_doc = urllib2.urlopen('http://www.xici.net.co/nn/' + str(page),timeout=15).read()
        soup = BeautifulSoup(html_doc)
        trs = soup.find('table', id='ip_list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[2].text.strip()
            port = tds[3].text.strip()
            protocol = tds[6].text.strip()
            if protocol == 'HTTP' or protocol == 'HTTPS':
                of.write('%s=%s:%s\n' % (protocol, ip, port) )
                print '%s=%s:%s' % (protocol, ip, port)
    except urllib2.URLError,e:
        print "Failed to reach the server"
        print "The reason:",e.reason
        sys.exit(1)
 
of.close()
