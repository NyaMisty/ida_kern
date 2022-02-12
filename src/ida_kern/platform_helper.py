import sys
import ctypes
import idaapi
from .exceptions import *

def is_ea64():
    ea64 = False
    if idaapi.BADADDR == 2**64 - 1:
        ea64 = True
    return ea64

def get_ida_kernel():
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

def get_platform_type():
    if sys.platform == 'win32':
        return 'win32'
    elif sys.platform == 'linux':
        return 'linux'
    elif sys.platform == 'darwin':
        if os.uname().machine == 'arm64':
            return 'armmac'
        else:
            return 'mac'
    else:
        raise UnknownArchitecture('unsupported os: %s' % sys.platform)