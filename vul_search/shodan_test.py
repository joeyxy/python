#!/usr/bin/env python

import shodan

SHODAN_API_KEY = ""

api = shodan.Shodan(SHODAN_API_KEY)


try:
    results = api.search('apache')
    
    print "Results found:%s" % results['total']
    for result in results['matches']:
        print 'IP:%s' % result['ip_str']
        print result['data']
        print ''
except shodan.APIError,e:
    print 'Error:%s' % e
