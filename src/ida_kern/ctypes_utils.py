import ctypes
from ctypes import CFUNCTYPE as ctypes_CFUNCTYPE

def CFUNCTYPE(*args, **kwargs):
    ret = ctypes_CFUNCTYPE(*args, **kwargs)
    def CFUNCTYPE_wrap(arg0, *args, **kwargs):
        if arg0 is None or arg0 == 0:
            return ret(0)
        else:
            return ret.__class__.from_param(ret, arg0, *args, **kwargs)
    ret.from_param = CFUNCTYPE_wrap
    #ret.from_param = lambda *args, **kwargs: ret(0) if not args[0:1] else ret.__class__.from_param(ret, *args, **kwargs)
    return ret

def hook_ctypes():
    ctypes.CFUNCTYPE = CFUNCTYPE

def unhook_ctypes():
    ctypes.CFUNCTYPE = ctypes_CFUNCTYPE