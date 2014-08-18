from core.module import Module
from core.moduleexception import ProbeException, ModuleException
from core.argparse import ArgumentParser
from external.crawler import Crawler
from ast import literal_eval
from core.prettytable import PrettyTable
import os
from core.utils import join_abs_paths, url_validator

WARN_CRAWLER_EXCEPT = 'Crawler exception'
WARN_CRAWLER_NO_URLS = "No sub URLs crawled. Check URL."
WARN_NOT_URL = 'Not a valid URL'


class Mapwebfiles(Module):
    '''Crawl and enumerate web folders files permissions'''


    def _set_vectors(self):
        self.support_vectors.add_vector('enum', 'file.enum', ["asd", "-pathlist", "$pathlist"])
    
    def _set_args(self):
        self.argparser.add_argument('url', help='HTTP URL where start crawling (es. http://host/path/page.html)')
        self.argparser.add_argument('baseurl', help='HTTP base url (es. http://host/path/)')
        self.argparser.add_argument('rpath', help='Remote web root corresponding to crawled path (es. /var/www/path)')
        self.argparser.add_argument('-depth', help='Crawl depth', type=int, default=3)


    def _prepare(self):
    
        if not url_validator.match(self.args['url']):
            raise ProbeException(self.name, '\'%s\': %s' % (self.args['url'], WARN_NOT_URL) )
        if not url_validator.match(self.args['baseurl']):
            raise ProbeException(self.name, '\'%s\': %s' % (self.args['baseurl'], WARN_NOT_URL) )
    
        url = self.args['url']    
        baseurl = self.args['baseurl']
        rpath = self.args['rpath']
        
        urls = []
    
        try:
            crawler = Crawler(url, self.args['depth'], '', '')
            crawler.crawl()
        except ModuleException, e:
            raise
        except Exception, e:
            raise ProbeException(self.name, "%s: %s" % (ERR_CRAWLER_EXCEPT, str(e)))
        else:
            urls = set(crawler.visited_links.union(crawler.urls_seen))
            
            # If no url, or the only one is the specified one
            
            if not urls or (urls and len(urls) == 1 and list(urls)[0] == url):
                raise ProbeException(self.name, WARN_CRAWLER_NO_URLS )
        
        
            self.args['paths'] = []
            for path in urls:
                self.args['paths'].append('/' + join_abs_paths([rpath, path[len(baseurl):]]))
                


    def _probe(self):

        self._result = self.support_vectors.get('enum').execute({'pathlist' : str(self.args['paths']) })