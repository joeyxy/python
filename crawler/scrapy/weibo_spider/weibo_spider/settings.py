# -*- coding: utf-8 -*-

# Scrapy settings for weibo_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'weibo_spider'

SPIDER_MODULES = ['weibo_spider.spiders']
NEWSPIDER_MODULE = 'weibo_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'weibo_spider (+http://www.yourdomain.com)'
