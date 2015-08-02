#!/usr/bin/env python

from datetime import datetime
import feedparser
BBC_FEED_URL = 'http://feeds.bbc.co.uk/news/%s/rss.xml'


def read_news(feed_url):
	try:
		data = feedparser.parse(feed_url)
	except Exception,e:
		print "Got error:%s" % str(e)

	for entry in data.entries:
		print(entry.title)
		print(entry.link)
		print(entry.description)
		print("\n")


if __name__ == '__main__':
	print "====Reading technology news feed from bbc.co.uk (%s)====" % datetime.today()
	print "Entery the type of news feed: "
	print "Available options are:world,uk,health,sci-tech,business,technology"
	type = raw_input("News feed type:")
	read_news(BBC_FEED_URL %type)
	print "==== End of BBC news feed ===="