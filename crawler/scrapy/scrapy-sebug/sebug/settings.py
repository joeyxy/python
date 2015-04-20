# -*- coding: utf-8 -*-

# Scrapy settings for sebug project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sebug'

SPIDER_MODULES = ['sebug.spiders']
NEWSPIDER_MODULE = 'sebug.spiders'

ITEM_PIPELINES = ['sebug.pipelines.SebugPipeline']

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
COOKIES_ENABLED = False
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sebug (+http://www.yourdomain.com)'
