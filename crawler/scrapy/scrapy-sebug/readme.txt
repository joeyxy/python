# scrapy-sebug

使用scrapy框架爬取sebug漏洞库内容，并存入mysql数据库。

不太了解scrapy的童鞋看这里：http://doc.scrapy.org/en/0.24/intro/overview.html

==========================

（1）简单定义sebug的漏洞详情页的item数据结构：

class SebugItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ssv = Field()
    appdir = Field()
    title = Field()
    content = Field()
    publishdate = Field()
    
（2）mysql数据库创建相应的表结构

（3）为防止爬虫被ban,设置setting.py

DOWNLOAD_DELAY = 2
RANDOMIZE_DOWNLOAD_DELAY = True
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'

（4）开始运行爬虫

scrapy crawl sebugvul