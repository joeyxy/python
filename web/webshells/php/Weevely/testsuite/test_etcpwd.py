from baseclasses import SimpleTestCase
from unittest import skipIf
from test import conf


class AuditEtcPwd(SimpleTestCase):
    
    def test_etcpwd(self):
        
        self.assertRegexpMatches(self._outp(":audit.etcpasswd"), 'mail:x:8:8:mail:/var/mail:/bin/sh')    
        self.assertRegexpMatches(self._outp(":audit.etcpasswd -real"), 'root:x:0:0:root:/root:/bin/bash')   
        self.assertNotRegexpMatches(self._outp(":audit.etcpasswd -real"), 'mail:x:8:8:mail:/var/mail:/bin/sh')  
        self.assertRegexpMatches(self._outp(":audit.etcpasswd -real -vector posix_getpwuid"), 'root:x:0:0:root:/root:/bin/bash')            
        self.assertRegexpMatches(self._outp(":audit.etcpasswd -real -vector read"), 'root:x:0:0:root:/root:/bin/bash')         
        
        
    @skipIf(not conf['shell_sh'], "Skipping shell.sh dependent tests")
    def test_etcpwd_cat(self):
        self.assertRegexpMatches(self._outp(":audit.etcpasswd -real -vector cat"), 'root:x:0:0:root:/root:/bin/bash')    