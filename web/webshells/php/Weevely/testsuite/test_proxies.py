from baseclasses import FolderFSTestCase
from test import conf
import os, sys, time, urllib2, signal
sys.path.append(os.path.abspath('..'))
import modules
from random import randint

class Proxies(FolderFSTestCase):
    
    @classmethod
    def _setenv(cls):    
        FolderFSTestCase._setenv.im_func(cls)
        cls._env_newfile('web_page4.html', content=conf['web_page4_content'])
    
    def __check_urlopen(self, result=None, url=None):
        
        if not url:
            self.assertEqual(len(result),2)
            self.assertTrue(result[1])
            url = result[1] 
            
        web_page4_relative_path = os.path.join(self.basedir.replace(conf['env_base_web_dir'],''), 'web_page4.html')        
        web_page4_url = '%s%s' %  (conf['env_base_web_url'], web_page4_relative_path)

        url += '?u=%s' % web_page4_url
        page = str(urllib2.urlopen(url).read())
        self.assertTrue(page)
        self.assertRegexpMatches(page, conf['web_page4_content'])        
    
    def __check_proxyopen(self, url=None, proxyhost = '127.0.0.1', proxyport = 8081, delay=0.1):
        
        if not url:
            web_page4_relative_path = os.path.join(self.basedir.replace(conf['env_base_web_dir'],''), 'web_page4.html') 
            url = '%s%s' %  (conf['env_base_web_url'], web_page4_relative_path)
        
        proxy = urllib2.ProxyHandler({'http': '%s:%i' % (proxyhost, proxyport)})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        
        if delay:
            time.sleep(delay)
            
        page = str(urllib2.urlopen(url).read())
        
        self.assertTrue(page)
        self.assertRegexpMatches(page, conf['web_page4_content'])        
        

    def __killpid(self, pid):
        os.kill(pid, signal.SIGKILL)
        
    
    def test_phpproxy(self):
        
        
        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        
        self.__check_urlopen(self._res(":net.phpproxy"))
        self.__check_urlopen(self._res(":net.phpproxy -startpath %s/.././%s/./" % (self.dirs[0], self.dirs[0])))
        
        self.assertRegexpMatches(self._warn(":net.phpproxy -startpath unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        self.assertRegexpMatches(self._warn(":net.phpproxy -startpath /tmp/"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(":net.phpproxy -startpath /unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        
        
        web_base_url = '%s%s' %  (conf['env_base_web_url'], self.basedir.replace(conf['env_base_web_dir'],''))
        
        self.__check_urlopen(self._res(":net.phpproxy %s/.././%s/./inte.php" % (self.dirs[0], self.dirs[0])),'%s/%s/inte.php' % (web_base_url, self.dirs[0]))

        self.assertRegexpMatches(self._warn(":net.phpproxy unexistant/unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        self.assertRegexpMatches(self._warn(":net.phpproxy /tmp/unexistant.php"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(":net.phpproxy /unexistant.php"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
     
    def test_proxy(self):
        
        self.assertEqual(self._path('cd %s' % self.basedir), self.basedir)
        
        proxyportstart = randint(20000,25000)
        
        proxydata = self._res(":net.proxy")
        self.__check_proxyopen()
        self.__killpid(proxydata[2])
        
        proxydata = self._res(":net.proxy -startpath %s/.././%s/./ -lport %i" % (self.dirs[0], self.dirs[0], proxyportstart))
        self.__check_proxyopen(proxyport=proxyportstart)
        self.__killpid(proxydata[2])
        
        self.assertRegexpMatches(self._warn(":net.proxy -startpath unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        self.assertRegexpMatches(self._warn(":net.proxy -startpath /tmp/"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(":net.proxy -startpath /unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        
        web_base_url = '%s/%s' %  (conf['env_base_web_url'].rstrip('/'), self.basedir.replace(conf['env_base_web_dir'],'').lstrip('/'))
        proxydata = self._res(":net.proxy %s/.././%s/./inte3.php -lport %i -force " % (self.dirs[0], self.dirs[0], proxyportstart+1))
        self.assertEqual(proxydata[:2], [ '%s/%s/inte3.php' % (self.basedir.rstrip('/'), self.dirs[0].rstrip('/')), '%s/%s/inte3.php' % (web_base_url.rstrip('/'), self.dirs[0].rstrip('/')) ])
        self.__check_proxyopen(proxyport=proxyportstart+1)
        self.assertRaises(urllib2.URLError,self.__check_proxyopen,proxyport=proxyportstart-1)
        self.__killpid(proxydata[2])        

        proxydata = self._res(":net.proxy %s/.././%s/./inte3.php -lport %i -force -just-install" % (self.dirs[0], self.dirs[0], proxyportstart+2))
        self.assertEqual( proxydata[:2], [ '%s/%s/inte3.php' % (self.basedir.rstrip('/'), self.dirs[0].rstrip('/')), '%s/%s/inte3.php' % (web_base_url.rstrip('/'), self.dirs[0].rstrip('/')) ])
        self.assertRaises(urllib2.URLError,self.__check_proxyopen,proxyport=proxyportstart+2)
        self.__killpid(proxydata[2])  
        
        proxydata = self._res(":net.proxy -lport %i -force -just-run %s" % (proxyportstart+3, '%s/%s/inte3.php' % (web_base_url, self.dirs[0])))
        self.assertEqual( proxydata[:2], [ '', '%s/%s/inte3.php' % (web_base_url, self.dirs[0]) ])
        self.__check_proxyopen(proxyport=proxyportstart+3)
        self.__killpid(proxydata[2])  

        self.assertRegexpMatches(self._warn(":net.proxy unexistant/unexistant"), modules.file.upload2web.WARN_NOT_FOUND)
        self.assertRegexpMatches(self._warn(":net.proxy /tmp/unexistant.php"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(":net.proxy /unexistant.php"), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
     
        