from typing import *
if False:
    # noqa
    from ida_kern import IDAKern

def find_hexrays(k: 'IDAKern') -> Optional[str]:
    plugs = k.get_plugins()
    while plugs:
        plug = plugs[0]
        if b'Hex-Rays Decompiler' == plug.name:
            return plug.path
        plugs = plugs[0].next

    return None
