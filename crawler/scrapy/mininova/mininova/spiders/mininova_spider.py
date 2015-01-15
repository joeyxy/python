from mininova.items import TorrentItem
from scrapy.contrib.spiders import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor

class MininovaSpider(CrawlSpider):
	name ='mininova'
	allowed_domains = ['mininova.org']
	start_urls = ['http://www.mininova.org/today']
	rules = [Rule(LinkExtractor(allow=['/tor/\d+']),'parse_torrent')]

	def parse_torrent(self,response):
		torrent = TorrentItem()
		torrent['url'] = response.url
		torrent['name'] = response.xpath("//h1/text()").extract()
		torrent['description'] = response.xpath("//div[@id='description']").extract()
		torrent['size'] = response.xpath("//div[@id='info-left']/p[2]/text()[2]").extract()
		return torrent
