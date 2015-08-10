#!/usr/bin/env python

import argparse
import urllib
import re
from datetime import datetime

SEARCH_URL = 'http://finance.google.com/finance?q='

def get_quote(symbol):
	content = urllib.urlopen(SEARCH_URL+symbol).read()
	m = re.search('id="ref_694653_1".*?>(.*?)<',content)
	if m :
		quote = m.group(1)
	else:
		quote = 'No quote available for: '+ symbol
	return quote


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="stock quote search")
	parser.add_argument('--symbol',action="store",dest="symbol",required=True)
	given_args= parser.parse_args()
	print "Searching stock quote for symbol '%s'" % given_args.symbol
	print "Stock quote for %s at %s:%s" % (given_args.symbol,datetime.today(),get_quote(given_args.symbol))