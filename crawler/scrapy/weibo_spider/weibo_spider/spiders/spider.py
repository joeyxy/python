from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from weibo_spider.items import WeiboSpiderItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import re

class weibo_spider(CrawlSpider):

	name='weibo_spider'
	allowed_domains=['weibo.com']
	start_urls=['http://huodong.weibo.com/hongbao/']
	rules=(
			Rule(SgmlLinkExtractor(allow = (r'http://huodong.weibo.com/hongbao/special_.+?'))),
			Rule(SgmlLinkExtractor(allow = (r'http://huodong.weibo.com/hongbao/top_.+?'))),
			Rule(SgmlLinkExtractor(allow = (r'http://huodong.weibo.com/hongbao/cate?type=.+?'))),
			Rule(SgmlLinkExtractor(allow = (r'http://huodong.weibo.com/hongbao/theme'))),
			Rule(SgmlLinkExtractor(allow=(r'http://huodong.weibo.com/hongbao/\d+?')), callback="parse_page",follow=True),
		)

	def parse_page(self,response):
		#ids=[]
		sel=Selector(response)
		item=WeiboSpiderItem()
		try:
			id=re.findall('hongbao/(\d+)',response.url)[0]
			item['hongbao_id']=id
			item['url']=response.url
		except Exception,e:
			print 'the id is wrong!!'
		return item
