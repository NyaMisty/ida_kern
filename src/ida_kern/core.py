from .platform_helper import *
from .definitions import load_definition

class IDAKern():
    def __init__(self):
        pass
    
    def init(self):
        self.kdll = get_ida_kernel()
        self.defs = load_definition(self.kdll, get_platform_type(), is_ea64())

    def __dir__(self):
        return list(self.__dict__) + list(self.defs)

    def __getattr__(self, attr):
        if attr in self.defs:
            return self.defs[attr]
        return super().__getattribute__(attr)

__all__ = ['IDAKern']