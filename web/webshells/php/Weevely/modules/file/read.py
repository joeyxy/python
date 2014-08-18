from modules.file.download import Download
from tempfile import NamedTemporaryFile
from core.argparse import ArgumentParser
from core.moduleguess import ModuleGuess

class Read(Download):
    '''Read remote file'''


    def _set_args(self):
        self.argparser.add_argument('rpath')
        self.argparser.add_argument('-vector', choices = self.vectors.keys())

    def _verify_vector_execution(self):

        file = NamedTemporaryFile()
        file.close()

        self.args['lpath'] = file.name
        
        return Download._verify_vector_execution(self)
    
    def _stringify_result(self):
        self._result = self._content
        return ModuleGuess._stringify_result(self)
