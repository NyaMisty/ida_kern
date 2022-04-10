import os
import sys
import ctypes
from ..exceptions import *

def is_ea64():
    import idaapi
    ea64 = False
    if idaapi.BADADDR == 2**64 - 1:
        ea64 = True
    return ea64

def get_platform_type():
    if sys.platform == 'win32':
        return 'win'
    elif sys.platform == 'linux':
        return 'linux'
    elif sys.platform == 'darwin':
        if os.uname().machine == 'arm64':
            return 'armmac'
        else:
            return 'mac'
    else:
        raise UnknownArchitecture('unsupported os: %s' % sys.platform)

def get_idaver():
    import idaapi
    return idaapi.IDA_SDK_VERSION

class IDAInfo():
    def __init__(self, platform=None, ea64=None, idaver=None):
        self.platform = platform
        self.ea64 = ea64
        self.idaver = idaver
        if self.platform is None:
            self.platform = get_platform_type()
        if self.ea64 is None:
            self.ea64 = is_ea64()
        if self.idaver is None:
            self.idaver = get_idaver()

def get_ida_kerndll():
    ea64 = is_ea64()
    if sys.platform == 'win32':
        dll = ctypes.WinDLL
    else:
        dll = ctypes.CDLL
    if sys.platform == 'win32':
        dllname = ['ida64.dll', 'ida.dll']
    elif sys.platform == 'linux':
        dllname = ['libida64.so', 'libida.so']
    elif sys.platform == 'darwin':
        dllname = ['libida64.dylib', 'libida.dylib']
    else:
        raise UnknownArchitecture('unsupported os: %s' % sys.platform)

    return dll(dllname[0] if ea64 else dllname[1])

__all__ = ['IDAInfo', 'get_ida_kerndll']