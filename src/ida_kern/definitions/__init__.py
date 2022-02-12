import importlib
import os
from os.path import dirname, basename, isfile, join
import glob

registered_mods = []

path, dirs, files = next(os.walk(join(dirname(__file__))))
module_files = [f for f in files if f.endswith('.py') and not f.startswith('_')]
for modname in [ f[:-3] for f in module_files ]:
    mod = importlib.import_module('.' + modname, __name__)
    #for c in dir(mod):
    #    registered_mods.append(getattr(mod, c))
    registered_mods.append(mod)

def get_registered_mods():
    return registered_mods

def load_definition(dll, platform, ea64):
    defs = {}
    for mod in registered_mods:
        defs.update(mod.load_definition(dll, platform, ea64))
    return defs
        