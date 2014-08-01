# coding=utf-8

__author__ = 'DM_'

import requests
import sys
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'
}


class search(object):
    def __init__(self, word, pages, searchdict):
        self.searchurl = searchdict['searchurl']
        self.urlPattern = searchdict['urlPattern']
        self.contentPattern = searchdict['contentPattern']
        self.nextPattern = searchdict['nextPattern']
        self.timeout = searchdict['timeout']
        self.proxies = searchdict['proxies']
        self.maxPages = searchdict['maxPages']
        self.headers = headers
        self.word = word
        self.pages = pages
        self.urls = []
        self.contents = []
        self.req = requests.session()
        self.login()


    def searchWithPages(self):
        for page in xrange(1, self.pages + 1):
            try:
                searchurl = self.searchurl(self.word, page)
                resp = self.req.get(searchurl, timeout=self.timeout, headers=headers)

                percent = int((1.0 * page / self.pages) * 100)
                sys.stdout.write("[+]Now is loading page %d, complete percent:%s. \r" % (page, str(percent) + '%'))
                sys.stdout.flush()
                html = resp.content

                self.urls.extend(re.findall(self.urlPattern, html))
                self.contents.extend(re.findall(self.contentPattern, html))

            except Exception, e:
                print "[!]%s \r" % e,
                break
        print

    def searchall(self):

        isNext = True
        searchpage = 0

        while isNext is not None:
            try:
                searchurl = self.searchurl(self.word, searchpage)
                resp = self.req.get(searchurl, timeout=self.timeout, headers=headers)

                html = resp.content

                self.urls.extend(re.findall(self.urlPattern, html))
                self.contents.extend(re.findall(self.contentPattern, html))

                sys.stdout.write("[+]now is loading page %d ..\r" % (searchpage + 1))
                sys.stdout.flush()

                isNext = re.search(self.nextPattern, html)
                searchpage += 1
            except requests.HTTPError, e:
                print u"[!]%s \r" % e,
                break

        print
        print '[+]searched %d pages.\n' % searchpage

    def search(self):
        if self.maxPages:
            if not self.pages is None and self.pages > self.maxPages:
                self.pages = self.maxPages
        else:
            if self.nextPattern is None:
                sys.exit("[!]error, not nextPattern so give a page for search.")

        if self.pages is None:
            self.searchall()
        else:
            self.searchWithPages()
        self.urls = list(set(self.urls))
        self.handle(self.contents)

    def login(self):
        pass

    def handle(self):
        pass


bingsearchDict = {
    'searchurl': lambda word, page: 'http://cn.bing.com/search?q=' + word + '&first=' + str(page - 1) + '1&FORM=PERE',
    'urlPattern': r'<li class="b_algo"><h2><a href="([\s\S]+?)"[\s\S]+?</li>',
    'contentPattern': '(?:<li class="b_algo">)(?:.+?)<p>([\s\S]+?)</p>(?:.+?)</li>',
    'nextPattern': r'下一页',
    "maxPages": None,
    'timeout': 5,
}

googlesearchDict = {
    'searchurl': lambda word, page: 'http://208.117.227.16/search?q=' + word + '&start=' + str(page) + '00&num=100',
    'urlPattern': r'<li class="g">[\s\S]+?<a href="([\s\S]+?)"[\s\S]+?</li>',
    'contentPattern': r'(?:<li class="g">)(?:.+?)<span class="st">(?:<span class="f">[\s\S]+?</span>)?([\s\S]+?)</span>(?:.+?)</li>',
    'nextPattern': r'下一页',
    "maxPages": None,
    'timeout': 5,
}

so360searchDict = {
    'searchurl': lambda word, page: 'http://www.so.com/s?ie=utf-8&q=' + word + '&pn=' + str(page),
    'urlPattern': r'<h3 class="res-title ">[\s]+?<a href="([\s\S]+?)"',
    'contentPattern': r'<p class="res-desc">([\s\S]+?)</p>',
    'nextPattern': r'id="snext"',
    "maxPages": None,
    'timeout': 5,
}

sogousearchDict = {
    'searchurl': lambda word, page: 'http://www.sogou.com/web?query=' + word + '&page=' + str(page) + '&num=100',
    'urlPattern': r'id="uigs_d0_\d{1,2}" href="([\s\S]+?)"',
    'contentPattern': r'<div class="ft" id="cacheresult_summary_\d+">  <!--summary_beg-->([\s\S]+?)<!--summary_end--></div>',
    'nextPattern': 'sogou_next',
    "maxPages": None,
    'timeout': 5,
}

zoomeyesearchDict = {
    'searchurl': lambda word, page: 'http://www.zoomeye.org/search?q=' + word + '&p=' + str(page),
    'urlPattern': r'<h4><a href="(?:search\?q=)?([\s\S]+?)"',
    'contentPattern': r' <div class="span7">([\s\S]+?)</div>',
    'nextPattern': None,
    "maxPages": 10,
    'timeout': 5,
}


class simplesearch(search):
    def __init__(self, word, pages, searchdict):
        super(simplesearch, self).__init__(word, pages, searchdict)


if __name__ == "__main__":
    s = simplesearch("site:x0day.me", None , googlesearchDict)
    s.search()
    print s.urls
