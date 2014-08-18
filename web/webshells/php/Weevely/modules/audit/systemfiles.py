from core.module import Module
from core.moduleexception import ProbeException
from core.argparse import ArgumentParser
from ast import literal_eval
from core.utils import join_abs_paths
from re import compile
import os


class Systemfiles(Module):
    '''Find wrong system files permissions'''

    def _set_vectors(self):
        self.support_vectors.add_vector('find', 'find.perms', ["$path", "$mode"])
        self.support_vectors.add_vector('findfiles', 'find.perms', ["$path", "$mode", "-type", "f"])
        self.support_vectors.add_vector('findnorecurs', 'find.perms', ["$path", "$mode", "-no-recursion"])
        self.support_vectors.add_vector('findfilesnorecurs', 'find.perms', ["$path", "$mode", "-no-recursion", "-type", "f"])
        self.support_vectors.add_vector('users', 'audit.etcpasswd', ["-real"])
        self.support_vectors.add_vector('check', 'file.check', ["$path", "$attr"])
    
    def _set_args(self):
        
        self.audits = ( 'etc_readable', 'etc_writable', 'crons', 'homes', 'logs', 'binslibs', 'root')
        self.argparser.add_argument('audit', default='all', choices=self.audits + ('all',), nargs='?')

    def __etc_writable(self):
        result = self.support_vectors.get('find').execute({'path' : '/etc/', 'mode' : '-writable' })   
        self.mprint('Writable files in \'/etc/\' and subfolders ..')
        if result: 
            self.mprint('\n'.join(result), module_name='')   
            return {'etc_writable' : result }
        else:
            return {}

    def __etc_readable(self):
        
        sensibles = [ 'shadow', 'ap-secrets', 'NetworkManager.*connections', 'mysql/debian.cnf', 'sa_key$', 'keys' '\.gpg', 'sudoers' ]
        sensibles_re = compile('.*%s.*' % '.*|.*'.join(sensibles))
        
        allresults = self.support_vectors.get('findfiles').execute({'path' : '/etc/', 'mode' : '-readable' })   
        
        result = [ r for r in allresults if sensibles_re.match(r) ]
        
        self.mprint('Readable sensible files in \'/etc/\' and subfolders ..')
        
        if result: 
            self.mprint('\n'.join(result), module_name='')   
            return {'etc_writable' : result }
        else:
            return {}
        
    def __crons(self):
        result = self.support_vectors.get('find').execute({'path' : '/var/spool/cron/', 'mode' : '-writable' })   
        self.mprint('Writable files in \'/var/spool/cron\' and subfolders ..')
        if result: 
            self.mprint('\n'.join(result), module_name='')   
            return { 'cron_writable' : result }
        else:
            return {}
        
    def __homes(self):
        dict_result = {}
        
        result = self.support_vectors.get('findnorecurs').execute({'path' : '/home/', 'mode' : '-writable'})  
        result += ['/root'] if self.support_vectors.get('check').execute({'path' : '/root', 'attr' : 'write' }) else []
        self.mprint('Writable folders in \'/home/*\', \'/root/\' ..')
        if result: 
            self.mprint('\n'.join(result), module_name='')  
            dict_result.update({'home_writable': result })
            
        result = self.support_vectors.get('findnorecurs').execute({'path' : '/home/', 'mode' : '-executable' })  
        result += ['/root'] if self.support_vectors.get('check').execute({'path' : '/root', 'attr' : 'exec' }) else [] 
        self.mprint('Browsable folders \'/home/*\', \'/root/\' ..')
        if result: 
            self.mprint('\n'.join(result), module_name='')  
            dict_result.update({'home_executable': result })

        
        
        return dict_result
        
    def __logs(self):
        
        commons = [ 'lastlog', 'dpkg', 'Xorg', 'wtmp', 'pm', 'alternatives', 'udev', 'boot' ]
        commons_re = compile('.*%s.*' % '.*|.*'.join(commons))
        
        allresults = self.support_vectors.get('findfilesnorecurs').execute({'path' : '/var/log/', 'mode' : '-readable' }) 
        
        result = [ r for r in allresults if not commons_re.match(r) ]
          
        self.mprint('Readable files in \'/var/log/\' and subfolders ..')

        if result: 
            self.mprint('\n'.join(result), module_name='')  
            return { 'log_writable' : result }
        else:
            return {}

    def __binslibs(self):
        
        dict_result = {}
        paths = ['/bin/', '/usr/bin/', '/usr/sbin', '/sbin', '/usr/local/bin', '/usr/local/sbin']
        paths += ['/lib/', '/usr/lib/', '/usr/local/lib' ]
        
        for path in paths:
            result = self.support_vectors.get('find').execute({'path' : path, 'mode' : '-writable' })   
            self.mprint('Writable files in \'%s\' and subfolders ..' % path)
            if result: 
                self.mprint('\n'.join(result), module_name='')  
                dict_result.update({ '%s_writable' % path : result })
                
        return dict_result
        
    def __root(self):
        
        result = self.support_vectors.get('findnorecurs').execute({'path' : '/', 'mode' : '-writable' })  
        self.mprint('Writable folders in \'/\' ..')
        if result: 
            self.mprint('\n'.join(result), module_name='')  
            return { 'root_writable' : result }
        else:
            return {}
            
    def _probe(self):
        
        self._result = {}
        
        for audit in self.audits:
            if self.args['audit'] in (audit, 'all'):
                funct = getattr(self,'_Systemfiles__%s' % audit)
                self._result.update(funct())
                         
       
    def _stringify_result(self):
       pass
                        