# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from sebug.items import SebugItem
import re

class SebugvulSpider(CrawlSpider):
    name = "sebugvul"
    allowed_domains = ["sebug.net"]
    start_urls = (
        'http://sebug.net/vuldb/vulnerabilities?start=1',
    )
   
    rules = [
	Rule(SgmlLinkExtractor(allow=('/vuldb/ssvid-(\d{1,6})$',)),callback='parse_vul'),
	Rule(SgmlLinkExtractor(allow=('/vuldb/vulnerabilities\?start=(\d{1,5})$',)),follow=True)
]

    def parse_vul(self, response):
    	hxs = HtmlXPathSelector(response)
	item = SebugItem()
	item['title'] = hxs.select('//h2[@class="article_title"]/text()').extract()[0]
	item['ssv'] = hxs.select('//div[@class="vuln"]/a/text()').re('\d{1,6}')[0]
	appdirtemp = hxs.select('//div[@class="vuln"]/a/text()').re('.+\D$')
	if appdirtemp == []:
		item['appdir'] = ""
	else:
		item['appdir'] = appdirtemp[0]
	item['publishdate'] = hxs.select('//div[@class="vuln"]/text()').re('\d{4}-\d{1,2}-\d{1,2}')[0]
	item['content'] = hxs.select('//div[@class="article_exp"]/pre/text()').extract()[0]
#	print item['content'] 
	return item
