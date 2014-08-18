


class ModuleException(Exception):
    def __init__(self, module, value):
        self.module = module
        self.error = value
    def __str__(self):
        return '%s %s' % (self.module, self.error)

class ProbeException(ModuleException):
    pass

class ProbeSucceed(ModuleException):
    pass

class ExecutionException(ModuleException):
    pass

class InitException(ModuleException):
    pass