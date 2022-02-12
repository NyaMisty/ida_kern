import ctypes
import _ctypes

class CtypesDllStub():
    def __init__(self, dll):
        self.dll = dll
    def __getattr__(self, func):
        parentFun = getattr(self.dll, func, None)
        if not parentFun:
            return ctypes.CFUNCTYPE(None)(0)
        return parentFun

def load_definition(dll, platform, ea64):
    if platform == 'win32':
        from ._sdkhdr import idasdk_win
        idasdk_win._libraries['FIXME_STUB'] = CtypesDllStub(dll)
        defs = idasdk_win.ctypeslib_define()
        newdefs = {}
        for k, v in defs.items():
            incl = True
            if isinstance(v, _ctypes.CFuncPtr):
                if not v:
                    incl = False
            if incl:
                newdefs[k] = v
        return newdefs

    return {}