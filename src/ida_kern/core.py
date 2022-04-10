from .utils.ida_utils import find_hexrays
from .utils.platform_helper import *
from .definitions import get_registered_mods
from .utils.ctypes_utils import hook_ctypes, unhook_ctypes


class IDAKern():
    def __init__(self, idainfo=None):
        self.loaded_mods = []
        self.dlls = {}
        self.defs = {}
        if idainfo is None:
            self.idainfo = None
        else:
            self.idainfo = idainfo

    def add_dll(self, dllname, dll):
        self.dlls[dllname] = dll

    def _on_defmod_loaded(self):
        """
        callback for receiving definition module loading event, to support loading modules that depends on other mod
        :return: True if updated something, so a new round of loading is needed
        """
        try:
            if not 'hexrays' in self.dlls:
                self.dlls['hexrays'] = find_hexrays(self)
                return True
        except:
            pass
        return False

    def load_mods(self):
        """
        Load all modules with dependency in mind
        :return: None
        """
        hook_ctypes()
        try:
            while True:
                new_loaded = False
                for mod in get_registered_mods():
                    if mod in self.loaded_mods:
                        continue
                    if all(c in self.dlls for c in mod.dll_needed()):
                        newdef = mod.load_definition(self.dlls, self.idainfo)
                        self.defs.update(newdef)
                        self.__dict__.update(newdef)
                        self.loaded_mods.append(mod)
                        new_loaded = True

                if not self._on_defmod_loaded() and not new_loaded:
                    break
        finally:
            unhook_ctypes()

    def init(self):
        """
        Initialize IDA information & DLL info, then load modules
        :return:
        """
        if self.idainfo is None:
            self.idainfo = IDAInfo()
            self.add_dll('kernel', get_ida_kerndll())
        self.load_mods()

    #def __dir__(self):
    #    return list(self.__dict__) + list(self.defs)

    #def __getattr__(self, attr):
    #    if attr in self.defs:
    #        return self.defs[attr]
    #    return super().__getattribute__(attr)

__all__ = ['IDAKern', 'IDAInfo']