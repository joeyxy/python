from core.moduleguess import ModuleGuess
from core.moduleexception import ProbeException, ProbeSucceed, ModuleException
import time
import datetime
import os


class Touch(ModuleGuess):
    '''Change file timestamps'''

    def _set_vectors(self):
        
        self.vectors.add_vector(name='touch_php', interpreter='shell.php', payloads = [ "touch('$rpath', '$epoch_time');" ])
        self.vectors.add_vector(name='touch', interpreter='shell.sh', payloads = [ 'touch -d @$epoch_time "$rpath" ' ])

        self.support_vectors.add_vector(name="exists", interpreter='file.check', payloads = ['$rpath', 'exists'])
        self.support_vectors.add_vector(name='get_epoch', interpreter='file.check', payloads = ['$rpath', 'time_epoch'])
        self.support_vectors.add_vector(name='ls', interpreter='file.ls', payloads = ['$rpath'])
        
        
    def _set_args(self):
        self.argparser.add_argument('rpath')
        self.argparser.add_argument('-time', help='Use timestamp like \'2004-02-29 16:21:42\' or \'16:21\'')
        self.argparser.add_argument('-epoch', help='Use epoch timestamp')
        self.argparser.add_argument('-ref', help='Use other file\'s time')
        self.argparser.add_argument('-oldest', action='store_true', help='Use time of the oldest file in same folder')        
    
        
    def _prepare(self):
        global dateutil
        try:
            import dateutil.parser
        except ImportError, e:
            raise ModuleException(self.name, str(e) + ', install \'dateutil\' python module')
        
    def __get_epoch_ts(self, rpath):

        ref_epoch = 0
        if self.support_vectors.get('exists').execute({ 'rpath' : rpath }):
            ref_epoch = self.support_vectors.get('get_epoch').execute({ 'rpath' : rpath })
        
        if not ref_epoch:
            raise ProbeException(self.name, 'can\'t get timestamp from \'%s\'' % ref_epoch)
        
        return ref_epoch
    
    def __get_oldest_ts(self, rpath, limit=5):
      
      rfolder, rfile = os.path.split(rpath)
      if not rfolder:
          rfolder = '.'
      
      file_ls_all = self.support_vectors.get('ls').execute({ 'rpath' : rfolder})
      
      if len(file_ls_all) >= limit:
          file_ls = file_ls_all[:limit]
      else:
          file_ls = file_ls_all
      
      file_ts = []
      for file in [ rfolder.rstrip('/') + '/' + filepath for filepath in file_ls ]:
          ts = self.__get_epoch_ts(file)
          if ts: 
              file_ts.append(ts)
          
      if file_ts:
          return min(file_ts)
      else:
          return 0
    
    def _prepare_vector(self):
        
        self.formatted_args['rpath'] = self.args['rpath']
        if self.args['oldest'] == True:
            # get oldest timestamp
            self.formatted_args['epoch_time'] = self.__get_oldest_ts(self.args['rpath'])
            
        elif self.args['epoch']:
            self.formatted_args['epoch_time'] = float(self.args['epoch'])
            
        elif self.args['ref']:
            self.formatted_args['epoch_time'] = self.__get_epoch_ts(self.args['ref'])
            
        elif self.args['time']:
            self.formatted_args['epoch_time'] = int(time.mktime(dateutil.parser.parse(self.args['time'], yearfirst=True).timetuple()))

        else:
            raise ModuleException(self.name, 'Too few arguments, specify -time or -ref or -oldest')
            
    def _verify_vector_execution(self):
        current_epoch = self.__get_epoch_ts(self.args['rpath'])
        if current_epoch == self.formatted_args['epoch_time']:
            self._result = current_epoch
            raise ProbeSucceed(self.name, "Correct timestamp")
            
    def _verify(self):
        if not self._result:
            raise ProbeException(self.name, "Unable to change timestamp, check permission")
            
    def _stringify_result(self):
        if self._result:
            self._output = 'Changed timestamp: %s' % datetime.datetime.fromtimestamp(self._result).strftime('%Y-%m-%d %H:%M:%S')
       
