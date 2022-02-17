import ida_kern
k = ida_kern.IDAKern()
k.init()

# Find a plugin by its name, using Hex-Rays as example
def find_hexrays():
    plugs = k.get_plugins()
    while plugs:
        plug = plugs[0]
        if b'Hex-Rays Decompiler' == plug.name:
            return {
                "path": plug.path,
                "name": plug.name,
                "comment": plug.comment,
                "flags": plug.flags,
            }
        plugs = plugs[0].next

hx = find_hexrays()