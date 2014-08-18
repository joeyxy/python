

from moduleexception import ModuleException, ProbeException, ProbeSucceed, InitException
from core.argparse import ArgumentParser, Namespace
from types import ListType, StringTypes, DictType
from core.prettytable import PrettyTable
from core.vector import VectorsDict
from os import linesep
from core.modulebase import ModuleBase

class Module(ModuleBase):
    '''Generic Module class to inherit.

    The Module object is a dynamically loaded Weevely extension that executes
    automatic tasks on the remote target. The Vector objects contain the code to
    run on remote target.

    To create a new module, define a class that inherit Module (e.g. 'class
    Mymodule(Module)') in a python file located in a subdirectory of 'modules/',
    for example 'modules/mygroup/mymodule.py'. The class name must be the same
    as the python file but starting with a capital letter.

    The module can then be executed from the terminal with ':mygroup.mymodule'.

    Every time the module takes care of:

        1) prepare the environment (method _prepare(), optional)
        2) run vectors and save results (method _probe(), mandatory)
        3) verify the probe execution (method _verify(), optional)

    The first time the constructor performs the following preliminary tasks:

        1) Defines module arguments (method _set_args(), recommended)
        2) Defines module vectors (method _set_vectors(), recommended)

    Follows an example of a basic module that downloads files from the web into
    target:

    ============================== webdownload.py ==============================

    from core.module import Module
    from core.moduleexception import ProbeException, ProbeSucceed
    
    WARN_DOWNLOAD_FAIL = 'Downloaded failed'
    
    class Webdownload(Module):
        
        def _set_args(self):

            # Declare the parameters accepted by this module. They will be
            # stored in the self.args dictionary.

            self.argparser.add_argument('url')
            self.argparser.add_argument('rpath')
    
        def _set_vectors(self):

            # Declare the vectors to execute. The vector named 'wget' uses the
            # module 'shell.sh' that executes shell commands to run wget,
            # 'check_download' uses 'file.check' (included in Weevely) to verify
            # the downloaded file. The 'payloads' field will be replaced with
            # values from self.args.

            self.support_vectors.add_vector(name='wget', interpreter='shell.sh', payloads = [ 'wget $url -O $rpath' ])
            self.support_vectors.add_vector(name='check_download', interpreter='file.check', payloads = [ '$rpath', 'exists' ])
            
        def _probe(self):

           # Start the download by calling the 'wget' vector.
           self.support_vectors.get('wget').execute(self.args)
       
        def _verify(self):

           # Verify downloaded file. Save the vector return value in
           # self._result and eventually raise ProbeException to stop module
           # execution and print an error message.

           self._result = self.support_vectors.get('check_download').execute({ 'rpath' : self.args['rpath'] })
           if self._result == False:
               raise ProbeException(self.name, WARN_DOWNLOAD_FAIL)
           

    =======================================================================================

       
    '''

        
    def _set_vectors(self):
        """Inherit this method to add vectors in self.vectors and
        self.support_vectors lists. This method is called by the constructor.

        Example of vector declaration:
        
        > self.support_vectors.add_vector(name='vector_name', interpreter='module_name', payloads = [ 'module_param1', '$module_param2', .. ])
        
        Template fields like '$rpath' are replaced at vector execution.
        
        """
        
        pass
    
    def _set_args(self):
        """Inherit this method to set self.argparser arguments. This method is
        called by module constructor. Arguments passed at module execution are
        stored in the self.args dictionary. See the official python argparse
        documentation.
        """
        
        pass

    def _init_module(self):
        """Inherit this method to set additional variables. This method is
        called by the constructor.
        """
        pass

    def _prepare(self):
        """Inherit this method to prepare vectors and environment for the
        probe, using declared vectors.

        This method is called at every module execution. Throws ModuleException,
        ProbeException.
        """
        
        pass

    def _probe(self):
        """Inherit this method to execute the main task. Vector declared before
        are used to call other modules and execute shell and php
        statements. This method is mandatory.

        Example of vector selection and execution:
        
        > self.support_vectors.get('vector_name').execute({ '$module_param2' : self.args['arg2']})

        The vector is selected with VectorList.get(name=''), and launched with
        Vector.execute(templated_params={}), that replaces the template
        variables and run the vector.

        Probe results should be stored in self._result.  This method is called
        at every module execution.  Throws ModuleException, ProbeException,
        ProbeSucceed.

        """
        pass

    
    def _verify(self):
        """Inherit this method to check the probe result.

        The results should be stored in self._result. It is called at every
        module execution. Throws ModuleException, ProbeException, ProbeSucceed.
        """
        pass
