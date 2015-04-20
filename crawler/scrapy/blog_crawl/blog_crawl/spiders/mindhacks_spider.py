from scrapy.spider import BaseSpider

class MindhacksSpider(BaseSpider):
	domain_name = "mindhacks.cn"
	start_urls = ["http://mindhacks.cn/"]

	def parse(self,response):
		return []


SPIDER = MindhacksSpider()
