from core.moduleexception import ModuleException
from string import Template
from types import ListType, StringTypes, DictType
import thread
import collections

class VectorsDict(collections.OrderedDict):
    
    def __init__(self, modhandler, *args):
        self.modhandler = modhandler
        collections.OrderedDict.__init__(self, args)

    def add_vector(self, name, interpreter, payloads):
        self[name] = Vector(self.modhandler, name, interpreter, payloads)
    
    def get(self, name):
        return self[name]


class Vector:
    
    
    def __init__(self, modhandler, name, interpreter, payloads):
        
        self.modhandler = modhandler
        self.name = name
        self.interpreter = interpreter
        
        # Payloads and Formats are lists
        self.payloads = []
        
        if payloads and isinstance(payloads, ListType):
            self.payloads = payloads
        elif payloads and isinstance (payloads, StringTypes):
            self.payloads.append(payloads)
        
    def execute(self, format_list = {}, return_out_res = False):

        # Check type dict
        if not isinstance(format_list, DictType):
            raise Exception("[!][%s] Error, format vector type is not dict: '%s'" % (self.name, format_list))



        formatted_list = []
        format_template_list = format_list.keys()
        for payload in self.payloads:
            
            # Search format keys present in current payload part 
            list_of_key_formats_in_payload = [s for s in format_template_list if '$%s' % s in payload]
            
            # Extract from format dict just the ones for current payload part
            dict_of_formats_in_payload = {}
            for k, v in format_list.iteritems():
                if k in list_of_key_formats_in_payload:
                    dict_of_formats_in_payload[k]=v
            
            if dict_of_formats_in_payload:
                formatted_list.append(Template(payload).safe_substitute(**dict_of_formats_in_payload))
            else:
                formatted_list.append(payload)

        res, out = self.modhandler.load(self.interpreter).run(formatted_list)
        
        if return_out_res:
            return out, res
        else:
            return res


    def execute_background(self, format_list = {}):
        thread.start_new_thread(self.execute, (format_list,))
        
