__all__ = ["get_registered_mods"]

import importlib
import os
from os.path import dirname, join

from typing import *
from ._base_defmod import BaseDefinitionMod

registered_mods: List[BaseDefinitionMod] = []

path, dirs, files = next(os.walk(join(dirname(__file__))))
module_files = [f for f in files if f.endswith('.py') and not f.startswith('_')]
for modname in [ f[:-3] for f in module_files ]:
    mod = importlib.import_module('.' + modname, __name__)
    #for c in dir(mod):
    #    registered_mods.append(getattr(mod, c))
    registered_mods.append(mod.DEFMOD)

def get_registered_mods():
    return registered_mods

# def load_definition(dlls, platform, ea64):
#     defs = {}
#     for mod in registered_mods:
#         if all(c in dlls for c in mod.__DLL__):
#             defs.update(mod.load_definition(dlls, platform, ea64))
#     return defs
