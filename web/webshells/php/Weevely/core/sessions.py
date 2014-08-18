import os
import glob
import urlparse 
import yaml
from core.moduleexception import ModuleException

dirpath = '.weevely'
rcfilepath = 'weevely.rc'
cfgext = '.session'
cfgfilepath = 'sessions'
historyfilepath = 'history'

default_session = { 'global' : { 'url' : '' , 'username': '', 'password': '', 'hostname': '', 'rcfile': '' } }

WARN_NOT_FOUND = 'Session file not found'
WARN_BROKEN_SESS = 'Broken session file, missing fields'
WARN_LOAD_ERR = "Error loading session file"

class Sessions():

    def __init__(self, url = None, password = None, sessionfile=None):
        
        self.sessions = {}
        self.current_session_name = ''
        
        if not os.path.isdir(cfgfilepath):
            os.makedirs(cfgfilepath)
            
        self.load_session(url, password, sessionfile) 


    def load_session(self, url, password, sessionfile):
        
        if sessionfile:
            self._load_session_by_file(sessionfile)
        elif url and password:
            self._load_session_by_url(url, password)
        else:
            self._load_fake_session()
            
        if not self.current_session_name:
            raise ModuleException("session", WARN_LOAD_ERR)   


    def _load_fake_session(self):
        
        self.sessions['fake'] = default_session.copy()
        self.current_session_name = 'fake'
        

    def _validate_session_data(self, session_dict):
        
        for sect in default_session:
            if not sect in session_dict:
                raise ModuleException("session", "%s '%s'" % (WARN_BROKEN_SESS, sect))
            
            for subsect in default_session[sect]:
                if not subsect in session_dict[sect]:
                    raise ModuleException("session", "%s '%s'" % (WARN_BROKEN_SESS, sect))



    def _load_session_by_file(self, session_name, just_return = False):
        
        if not os.path.isfile(session_name):
            raise ModuleException('session', WARN_NOT_FOUND)

        try:
            session_data = yaml.load(open(session_name,'r').read())
        except Exception as e:
          raise ModuleException("session", WARN_BROKEN_SESS)
        
        self._validate_session_data(session_data)
        
        if not just_return:
            self.sessions[session_name] = session_data
            self.current_session_name = session_name
            
        else:
            return session_data          

      
    def _load_session_by_url(self, url, password):
        
        sessions_available = glob.glob(os.path.join(cfgfilepath,'*','*%s' % cfgext)) 
        
        for session in sessions_available:
            session_opts = self._load_session_by_file(session, just_return=True)
            if session_opts['global']['url'] == url and session_opts['global']['password'] == password:
                self._load_session_by_file(session)
                return
                

        self._init_new_session(url, password)
            
    
    def _guess_first_usable_session_name(self, hostfolder, bd_fixedname):      
        
        if not os.path.isdir(hostfolder):
            os.makedirs(hostfolder)
        
        bd_num = 0
        
        while True:
            bd_filename =  bd_fixedname + (str(bd_num) if bd_num else '') + cfgext
            session_name = os.path.join(hostfolder, bd_filename) 
                
            if not os.path.exists(session_name):
                return session_name
            else:
                bd_num +=1
        
        
    def _init_new_session(self, url, password, session_name = None):
        
        if not session_name:
            hostname = urlparse.urlparse(url).hostname
            hostfolder = os.path.join(cfgfilepath, hostname)
            bd_fixedname = os.path.splitext(os.path.basename(urlparse.urlsplit(url).path))[0]
            
            session_name = self._guess_first_usable_session_name(hostfolder, bd_fixedname)


        self.sessions[session_name] = default_session.copy()
        
        self.sessions[session_name]['global']['url'] = url
        self.sessions[session_name]['global']['password'] = password
        self.current_session_name = session_name
    
    def get_session(self, session_name = None):
        
        if not session_name:
            return self.sessions[self.current_session_name]
        else:
            return self.sessions[session_name]
            

    def dump_all_sessions(self, modules):
        
        # Update sessions with module stored arguments
        
        for modname, mod in modules.items():
            for arg, val in mod.stored_args_namespace:
                if not modname in self.sessions[self.current_session_name]:
                    self.sessions[self.current_session_name][modname] = {}
                    
                self.sessions[self.current_session_name][modname][arg] = val
                
        
        # Dump all sessions
        for session_name in self.sessions:
            if session_name != 'fake':
                self._dump_session(self.sessions[session_name], session_name)

    def _dump_session(self, session, session_name):
            
        try:
            yaml.dump(session,open(session_name,'w'), default_flow_style=False)
        except Exception as e:
            raise ModuleException("session", e)


    def format_sessions(self, level = 0):
        
        output = "Current session: '%s'%s" % (self.current_session_name, os.linesep)
        if level > 0:
            sessions_loaded = "', '".join(sorted(self.sessions.keys()))
            output += "Loaded: '%s'%s" % (sessions_loaded, os.linesep)
        if level > 1:
            sessions_available = "', '".join(glob.glob(os.path.join(cfgfilepath,'*','*%s' % cfgext)))
            output += "Available: '%s'%s" % (sessions_available, os.linesep)
            
        return output
            
        