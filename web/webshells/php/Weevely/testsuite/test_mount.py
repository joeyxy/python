from baseclasses import FolderFSTestCase
from test import conf
from core.utils import randstr
from tempfile import mkdtemp
import os, sys
from string import ascii_lowercase
sys.path.append(os.path.abspath('..'))
import modules
import modules.file.mount
import modules.file.upload2web
import modules.file.upload

class Mount(FolderFSTestCase):


    def test_mount_expected_behaviour(self):
        
        temp_filename = randstr(4) + '.php'
        env_writable_url = os.path.join(conf['env_base_web_url'], conf['env_base_writable_web_dir'].replace(conf['env_base_web_dir'],''))
        env_writable_baseurl = os.path.join(env_writable_url, os.path.split(self.basedir)[-1])
        
        temp_dir = mkdtemp()
        
        self._outp('cd %s' % self.basedir)
        
        res = self._res(':file.mount')
        self.assertTrue(res and res[0].startswith(env_writable_baseurl) and res[0].endswith('.php') and res[1].startswith('/tmp/tmp') and res[2] == self.basedir)
        
        res = self._res(':file.mount -remote-mount /tmp/')
        self.assertTrue(res and res[0].startswith(env_writable_baseurl) and res[0].endswith('.php') and res[1].startswith('/tmp/tmp') and res[2] == '/tmp')

        res = self._res(':file.mount -local-mount %s' % temp_dir)
        self.assertTrue(res and res[0].startswith(env_writable_baseurl) and res[0].endswith('.php') and res[1] == temp_dir and res[2] == self.basedir)

        self.assertTrue(self._res(':file.mount -umount-all'))

        res = self._res(':file.mount -local-mount %s -rpath %s' % (temp_dir, temp_filename))
        self.assertTrue(res and res[0] == os.path.join(env_writable_baseurl, temp_filename) and res[1] == temp_dir and res[2] == self.basedir)
        
        res = self._res(':file.mount -rpath %s -force' % (temp_filename))
        self.assertTrue(res and res[0] == os.path.join(env_writable_baseurl, temp_filename) and res[1].startswith('/tmp/tmp') and res[2] == self.basedir)
        
        res = self._res(':file.mount -startpath %s' % (self.dirs[0]))
        self.assertTrue(res and res[0].startswith(os.path.join(env_writable_baseurl,self.dirs[0])) and res[0].endswith('.php') and res[1].startswith('/tmp/tmp') and res[2] == self.basedir)

        res = self._res(':file.mount -just-mount %s ' % os.path.join(env_writable_baseurl, temp_filename))
        self.assertTrue(res and res[0] == os.path.join(env_writable_baseurl, temp_filename) and res[1].startswith('/tmp/tmp') and res[2] == self.basedir)
        
        res = self._res(':file.mount -just-install')
        self.assertTrue(res and res[0].startswith(env_writable_baseurl) and res[0].endswith('.php') and res[1] == None and res[2] == self.basedir)


        self.assertTrue(self._res(':file.mount -umount-all'))
        self.assertRegexpMatches(self._warn(':file.mount -umount-all'), modules.file.mount.WARN_MOUNT_NOT_FOUND)

        
    def test_mount_errors(self):
        
        temp_filename = randstr(4) + '.php'
        env_writable_url = os.path.join(conf['env_base_web_url'], conf['env_base_writable_web_dir'].replace(conf['env_base_web_dir'],''))
        env_writable_baseurl = os.path.join(env_writable_url, os.path.split(self.basedir)[-1])
        
        temp_dir = mkdtemp()
        
        self._outp('cd %s' % self.basedir)

        self.assertRegexpMatches(self._warn(':file.mount -remote-mount /nonexistant/'),modules.file.mount.WARN_HTTPFS_MOUNTPOINT)
        self.assertRegexpMatches(self._warn(':file.mount -remote-mount /etc/protocols'),modules.file.mount.WARN_HTTPFS_OUTP)


        self.assertRegexpMatches(self._warn(':file.mount -local-mount /nonexistant/'),modules.file.mount.WARN_HTTPFS_OUTP)


        self.assertRegexpMatches(self._warn(':file.mount -rpath /notinwebroot'), modules.file.upload2web.WARN_NOT_WEBROOT_SUBFOLDER)
        self.assertRegexpMatches(self._warn(':file.mount -rpath ./unexistant/path'), modules.file.upload2web.WARN_NOT_FOUND)
        res = self._res(':file.mount -just-install -rpath %s' % (temp_filename))
        self.assertRegexpMatches(self._warn(':file.mount -just-install -rpath %s' % (temp_filename)), modules.file.upload.WARN_FILE_EXISTS)

        self.assertRegexpMatches(self._warn(':file.mount -startpath /notinwebroot'), modules.file.upload2web.WARN_NOT_FOUND)
        self.assertRegexpMatches(self._warn(':file.mount -startpath ./unexistant/path'), modules.file.upload2web.WARN_NOT_FOUND)

        self.assertRegexpMatches(self._warn(':file.mount -just-mount localhost:9909'),modules.file.mount.WARN_HTTPFS_OUTP)
        self.assertRegexpMatches(self._warn(':file.mount -just-mount %s/nonexistant' % env_writable_baseurl),modules.file.mount.WARN_HTTPFS_OUTP)

    
#        pathenv_splitted_orig = os.environ['PATH'].split(':')
#        pathenv_splitted_orig.remove('/usr/local/bin')
#        os.environ['PATH'] = ':'.join(pathenv_splitted_orig)
#        
#        self.assertRegexpMatches(self._warn(':file.mount -just-install'), modules.file.mount.WARN_ERR_RUN_HTTPFS)
