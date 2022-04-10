__all__ = ['DEFMOD']

import importlib

from ._base_defmod import BaseDefinitionMod
from ..exceptions import *

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


class IDASDKHeaderDef(BaseDefinitionMod):
    def dll_needed(self):
        return ["kernel"]

    def load_definition(self, dlls, idainfo):
        dll = dlls['kernel']
        PLATFORM_MAP = {
            'win': 'win',
            'linux': 'linux',
            'mac': 'mac',
            'armmac': 'armmac',
        }
        platType = PLATFORM_MAP.get(idainfo.platform)
        if platType is None:
            raise UnknownArchitecture('Unsupported platform %s' % idainfo.platform)
        VERSION_MAP = [
            (770, '77'),
        ]
        verName = None
        for v, vname in VERSION_MAP:
            if idainfo.idaver >= v:
                verName = vname
        if platType is None:
            raise UnknownArchitecture('Unsupported IDA version %s' % idainfo.idaver)

        hdr_prefix = f'ida{platType}{verName}_'

        get_sdkhdr = lambda x: importlib.import_module('._sdkhdr.' + hdr_prefix + x, package=__package__)

        retDef = {}

        for modType in ['sdk', 'libtypes', 'hexrays']:
            mod = get_sdkhdr(modType)
            try:
                mod._libraries['FIXME_STUB'] = CtypesDllStub(dll)
            except AttributeError:
                pass
            defs = mod.ctypeslib_define()

            newdefs = {}
            for k, v in defs.items():
                incl = True
                if isinstance(v, _ctypes.CFuncPtr):
                    if not v:
                        incl = False
                if incl:
                    newdefs[k] = v
            retDef.update(newdefs)

        return retDef

DEFMOD = IDASDKHeaderDef()