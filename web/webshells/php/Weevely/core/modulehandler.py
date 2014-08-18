import os,sys
from moduleexception import ModuleException
from core.sessions import Sessions, dirpath, rcfilepath
from helper import Helper


class ModHandler:


    def __init__(self, url = None, password = None, sessionfile=None):

        self.sessions = Sessions(url, password, sessionfile)

        self.set_url_pwd()

        self.interpreter = None
        self.modules_names_by_group = {}
        self.modules_classes = {}
        self.modules = {}

        self._guess_modules_path()
        self._load_modules_tree()

        self.verbosity=[ 3 ]
        
        self._last_warns = ''
        
    def set_url_pwd(self):
        self.url = self.sessions.get_session()['global']['url']
        self.password = self.sessions.get_session()['global']['password']        

    def _guess_modules_path(self):
    
    	try:
    		current_path = os.path.realpath( __file__ )
    		root_path = os.sep.join(current_path.split(os.sep)[:-2]) + os.sep
    		self.modules_path = root_path + 'modules'
    	except Exception, e :
    		raise Exception('Error finding module path: %s' % str(e))
    
        if not os.path.exists(self.modules_path):
            raise Exception( "No module directory %s found." % self.modules_path )
    


    def _load_modules_tree(self, startpath = None, recursive = True):

        if not startpath:
            startpath = self.modules_path

        for file_name in os.listdir(startpath):

            file_path = startpath + os.sep + file_name

            if os.path.isdir(file_path) and recursive:
                self._load_modules_tree(file_path, False)
            
            if os.path.isfile(file_path) and file_path.endswith('.py') and file_name != '__init__.py':
                
                module_name = '.'.join(file_path[:-3].split(os.sep)[-2:])
                mod = __import__('modules.' + module_name, fromlist = ["*"])
                classname = module_name.split('.')[-1].capitalize()
                
                if hasattr(mod, classname):
                    modclass = getattr(mod, classname)
                    self.modules_classes[module_name] = modclass
                
                    module_g, module_n = module_name.split('.')
                    if module_g not in self.modules_names_by_group:
                        self.modules_names_by_group[module_g] = []
                    self.modules_names_by_group[module_g].append(module_name)

        self.ordered_groups = self.modules_names_by_group.keys()
        self.ordered_groups.sort()


    def load(self, module_name):

        if module_name not in self.modules_classes.keys():
            raise ModuleException(module_name, "Module '%s' not found in path '%s'." % (module_name, self.modules_path) )  
        elif not module_name:
            module_name = self.interpreter
        elif not module_name in self.modules:
            self.modules[module_name]=self.modules_classes[module_name](self)

        
        return self.modules[module_name]


    def set_verbosity(self, v = None):

        if not v:
            if self.verbosity:
                self.verbosity.pop()
            else:
                self.verbosity = [ 3 ]
        else:
            self.verbosity.append(v)

