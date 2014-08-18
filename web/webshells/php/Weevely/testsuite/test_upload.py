from baseclasses import FolderFSTestCase
from test import conf
from core.utils import randstr
import os, sys
from string import ascii_lowercase
sys.path.append(os.path.abspath('..'))
import modules
from urlparse import urljoin


class FSUpload(FolderFSTestCase):
    
    
    def test_upload(self):
        
        filename_rand = randstr(4)
        filepath_rand = os.path.join(self.basedir, filename_rand)
        
        self.assertEqual(self._res(':file.upload /etc/protocols %s0'  % filepath_rand), True)
        self.assertRegexpMatches(self._warn(':file.upload /etc/protocolsA %s1'  % filepath_rand), modules.file.upload.WARN_NO_SUCH_FILE)
        self.assertRegexpMatches(self._warn(':file.upload /etc/protocols /notwritable' ), modules.file.upload.WARN_UPLOAD_FAIL)
        self.assertEqual(self._res(':file.upload /bin/true %s2'  % filepath_rand), True)
        self.assertEqual(self._res(':file.upload /bin/true %s3 -vector file_put_contents'  % filepath_rand), True)   
        self.assertEqual(self._res(':file.upload /bin/true %s4 -vector fwrite'  % filepath_rand), True)        
        self.assertEqual(self._res(':file.upload /bin/true %s5 -chunksize 2048'  % filepath_rand), True)       
        self.assertEqual(self._res(':file.upload /bin/true %s6 -content MYTEXT'  % filepath_rand), True)   
        self.assertEqual(self._outp(':file.read %s6'  % (filepath_rand)), 'MYTEXT')     
     
        # Check force
        self.assertRegexpMatches(self._warn(':file.upload /bin/true %s6 -content MYTEXT'  % filepath_rand), modules.file.upload.WARN_FILE_EXISTS)    
        self.assertEqual(self._res(':file.upload /bin/true %s6 -content MYTEXT -force'  % filepath_rand), True)


    def test_upload2web(self):
        
        filename_rand = randstr(4)
        filepath_rand = os.path.join(self.basedir, filename_rand)
        
        env_writable_base_url = urljoin(conf['env_base_web_url'], self.basedir.replace(conf['env_base_web_dir'],''))
        env_writable_url = urljoin(conf['env_base_web_url'], conf['env_base_writable_web_dir'].replace(conf['env_base_web_dir'],''))
        
        self._outp('cd %s' % self.basedir)
        self.assertEqual(self._res(':file.upload2web /etc/protocols' ), ['%s/protocols' % self.basedir, '%s/protocols' % env_writable_base_url])
        self.assertEqual(self._res(':file.upload2web /etc/protocols %s/protocols' % os.path.join(self.basedir, self.dirs[0]) ), ['%s/protocols' % os.path.join(self.basedir, self.dirs[0]), '%s/protocols' % os.path.join(env_writable_base_url, self.dirs[0])])

        # Out of web root
        
        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols /asp' ), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)

        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols /tmp/protocols' ), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols -startpath /tmp/' ), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        
        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols ../../../protocols' ), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols -startpath ../../../' ), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        
        # In webroot but not writable
        self.assertRegexpMatches(self._warn(':file.upload2web /etc/protocols %s/protocols' % conf['env_base_notwritable_web_dir'] ), modules.file.upload.WARN_UPLOAD_FAIL)
        
        self.assertEqual(self._res(':file.upload2web /etc/protocols -startpath ../ -force' ), ['%s/protocols' % conf['env_base_writable_web_dir'].rstrip('/'), '%s/protocols' % env_writable_url.rstrip('/')])
        self.__class__._env_rm('%s/protocols' % conf['env_base_writable_web_dir'])
        
        self.assertEqual(self._res(':file.upload2web /bin/true -force'), ['%s/true' % self.basedir, '%s/true' % env_writable_base_url])
        self.assertEqual(self._res(':file.upload2web /bin/true -vector file_put_contents -force'), ['%s/true' % self.basedir, '%s/true' % env_writable_base_url])   
        self.assertEqual(self._res(':file.upload2web /bin/true -vector fwrite -force' ), ['%s/true' % self.basedir, '%s/true' % env_writable_base_url])        
        self.assertEqual(self._res(':file.upload2web /bin/true -chunksize 2048 -force' ), ['%s/true' % self.basedir, '%s/true' % env_writable_base_url])       
        self.assertEqual(self._res(':file.upload2web /bin/asd -content MYTEXT -force'), ['%s/asd' % self.basedir, '%s/asd' % env_writable_base_url])   
        self.assertEqual(self._outp(':file.read %s'  % ('%s/asd' % self.basedir)), 'MYTEXT')     


        self.assertEqual(self._res(':file.upload2web /etc/protocols %s' % filename_rand ), ['%s/%s' % (self.basedir,filename_rand), '%s/%s' % (env_writable_base_url,filename_rand)])
