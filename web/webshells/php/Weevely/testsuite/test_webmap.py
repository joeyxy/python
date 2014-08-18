from baseclasses import SimpleTestCase, FolderFSTestCase
from test import conf
import os, sys
sys.path.append(os.path.abspath('..'))
import modules


class WebMap(SimpleTestCase):
    
    
    @classmethod
    def _setenv(cls):    
        FolderFSTestCase._setenv.im_func(cls)
        
        cls._env_newfile('web_page1.html', content=conf['web_page1_content'])
        cls._env_newfile('web_page2.html', content=conf['web_page2_content'])
        cls._env_newfile('web_page3.html', content=conf['web_page3_content'])

    def test_mapweb(self):
        
        web_page1_relative_path = os.path.join(self.basedir.replace(conf['env_base_web_dir'],''), 'web_page1.html')
        web_page1_url = '%s%s' %  (conf['env_base_web_url'], web_page1_relative_path)
        web_base_url = '%s%s' %  (conf['env_base_web_url'], self.basedir.replace(conf['env_base_web_dir'],''))
        
        webmap1 = { os.path.join(self.basedir, 'web_page1.html'): ['exists', 'readable', 'writable', ''] }
        webmap2 = { os.path.join(self.basedir, 'web_page2.html'): ['exists', 'readable', 'writable', ''] }
        webmap3 = { os.path.join(self.basedir, 'web_page3.html'): ['exists', 'readable', 'writable', ''] }
        
        webmap = webmap1.copy(); webmap.update(webmap2); webmap.update(webmap3)
        webmap_first_two = webmap1.copy(); webmap_first_two.update(webmap2);

        self.assertEqual(self._res(':audit.mapwebfiles %s %s %s' % (web_page1_url, web_base_url, self.basedir)), webmap)
        self.assertEqual(self._res(':audit.mapwebfiles %s %s %s -depth 0' % (web_page1_url, web_base_url, self.basedir)), webmap_first_two)

        
        self.assertRegexpMatches(self._warn(':audit.mapwebfiles %s_unexistant.html %s %s' % (web_page1_url, web_base_url, self.basedir)), modules.audit.mapwebfiles.WARN_CRAWLER_NO_URLS)

        web_page1_badurl = 'http://localhost:90/%s' %  (web_page1_relative_path)
        self.assertRegexpMatches(self._warn(':audit.mapwebfiles %s %s %s' % (web_page1_badurl, web_base_url, self.basedir)), modules.audit.mapwebfiles.WARN_CRAWLER_NO_URLS)

