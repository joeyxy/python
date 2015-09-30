#!/usr/bin/env python

import shodan
import sys


api_key = ""


FACETS = [
  'org',
  'domain',
  'port',
  'asn',
  ('country',5)
]

FACET_TITLES = {
    'org' : 'Top 10 Organization',
    'domain' : 'Top 10 Domains',
    'port' : 'Top 10 Ports',
    'asn' : 'Top 10 Autonomous Systems',
    'country' : 'Top 5 Countries',
}

if len(sys.argv) == 1:
    print "Usage: %s <search query> " % sys.argv[0]

try:
    api = shodan.Shodan(api_key)
    
    query = ' '.join(sys.argv[1:])
    
    result = api.count(query,facets=FACETS)
    
    print 'Shodan Summary Information'
    print 'Query: %s' % query
    print 'Total Results:%s\n' % result['total']
    
    for facet in result['facets']:
        print FACET_TITLES[facet]
        
        for term in result['facets'][facet]:
            print '%s: %s' % (term['value'],term['count'])
            
        print ''
        
except Exception,e:
    print 'Error: %s' % e
    sys.exit(1)