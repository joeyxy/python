
from core.module import Module
from core.moduleexception import ModuleException, ProbeException
from core.argparse import ArgumentParser
from external.ipaddr import IPNetwork
import re

WARN_NO_OUTPUT = 'No execution output'
WARN_NO_IFACES = 'No interfaces address found'

class Ifaces(Module):
    '''Print interfaces addresses'''
    
    
    def _set_vectors(self):
        self.support_vectors.add_vector('enum',  'file.enum',  ["asd", "-pathlist", "$pathlist"])
        self.support_vectors.add_vector(  "ifconfig" , 'shell.sh', "$ifconfig_path")
    
    
    def _probe(self):
        
        self._result = {}
        
        enum_pathlist = str([ x + 'ifconfig' for x in ['/sbin/', '/bin/', '/usr/bin/', '/usr/sbin/', '/usr/local/bin/', '/usr/local/sbin/'] ])

        ifconfig_pathlist = self.support_vectors.get('enum').execute({'pathlist' : enum_pathlist })
        
        for path in ifconfig_pathlist:
            if ifconfig_pathlist[path] != ['','','','']:
                result = self.support_vectors.get('ifconfig').execute({'ifconfig_path' : path })
                
                if result:
                    ifaces = re.findall(r'^(\S+).*?inet addr:(\S+).*?Mask:(\S+)', result, re.S | re.M)

                    if ifaces:
                        
                        for iface in ifaces:
                            ipnet = IPNetwork('%s/%s' % (iface[1], iface[2]))
                            self._result[iface[0]] = ipnet
                else:
                    raise ProbeException(self.name, '\'%s\' %s' % (path, WARN_NO_OUTPUT))      
                
                
    def _verify(self):
        if not self._result:
            raise ProbeException(self.name, WARN_NO_IFACES)    
                
                     