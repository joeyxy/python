from core.module import Module
from core.moduleexception import ProbeException, ProbeSucceed
from core.argparse import ArgumentParser

from tempfile import mkdtemp
from os import path
from subprocess import call
from shutil import copy
from core.utils import md5sum

WARN_DOWNLOAD_FAILED = 'Edit failed, check path and reading permission of'
WARN_BACKUP_FAILED = 'Backup version copy failed'
WARN_UPLOAD_FAILED = 'Edit failed, check path and writing permission of'
WARN_EDIT_FAILED = 'Edit failed, temporary file not found'
WARN_KEEP_FAILED = 'Fail keeping original timestamp'

class Edit(Module):
    '''Edit remote file'''


    def _set_vectors(self):
        self.support_vectors.add_vector('download', 'file.download', [ "$rpath", "$lpath" ])
        self.support_vectors.add_vector('upload', 'file.upload', [ "$lpath", "$rpath", "-force" ])
        self.support_vectors.add_vector('md5', 'file.check', [ "$rpath", "md5" ])
        self.support_vectors.add_vector('exists', 'file.check', [ "$rpath", "exists" ])
        self.support_vectors.add_vector('get_time', 'file.check', [ "$rpath", "time_epoch" ])
        self.support_vectors.add_vector('set_time', 'file.touch', [ "$rpath", "-epoch", "$epoch" ])


    def _set_args(self):
        self.argparser.add_argument('rpath', help='Remote path')
        self.argparser.add_argument('-editor', help='Choose editor. default: vim',  default = 'vim')
        self.argparser.add_argument('-keep-ts', help='Keep original timestamp',  action='store_true')
        

    def _probe(self):
        
        self._result = False
        
        rpathfolder, rfilename = path.split(self.args['rpath'])
        
        lpath = path.join(mkdtemp(),rfilename)
        lpath_orig = lpath + '.orig'
        
        rpath_existant = self.support_vectors.get('exists').execute({ 'rpath' : self.args['rpath'] })
        
        if rpath_existant:
            if not self.support_vectors.get('download').execute({ 'rpath' : self.args['rpath'], 'lpath' : lpath }):
                raise ProbeException(self.name, '%s \'%s\'' % (WARN_DOWNLOAD_FAILED, self.args['rpath']))
            
            if self.args['keep_ts']:
                self.args['epoch'] = self.support_vectors.get('get_time').execute({'rpath' : self.args['rpath']})
                
            try:
                copy(lpath, lpath_orig)
            except Exception, e:
                raise ProbeException(self.name, '\'%s\' %s %s' % (lpath_orig, WARN_BACKUP_FAILED, str(e)))
            
            call("%s %s" % (self.args['editor'], lpath), shell=True)
            
            md5_lpath_orig = md5sum(lpath_orig)
            if md5sum(lpath) == md5_lpath_orig:
                self._result = True
                raise ProbeSucceed(self.name, "File unmodified, no upload needed")
            
        else:
            call("%s %s" % (self.args['editor'], lpath), shell=True)
            
        if not path.exists(lpath):
            raise ProbeException(self.name, '%s \'%s\'' % (WARN_EDIT_FAILED, lpath))

            
        if not self.support_vectors.get('upload').execute({ 'rpath' : self.args['rpath'], 'lpath' : lpath }):
            
            recover_msg = ''
            
            if rpath_existant:
                if self.support_vectors.get('md5').execute({ 'rpath' : self.args['rpath'] }) != md5_lpath_orig:
                    recover_msg += 'Upload fail but remote file result modified. Recover backup copy from \'%s\'' % lpath_orig
        
            raise ProbeException(self.name, '%s \'%s\' %s' % (WARN_UPLOAD_FAILED, self.args['rpath'], recover_msg))
        
        if self.args['keep_ts'] and self.args.get('epoch', None):
            new_ts_output, new_ts = self.support_vectors.get('set_time').execute(self.args, return_out_res = True)

            if new_ts_output:
                self.mprint(new_ts_output)
            else:
                raise ProbeException(self.name, WARN_KEEP_FAILED)
                
        self._result = True
        
    def _stringify_result(self):
        pass