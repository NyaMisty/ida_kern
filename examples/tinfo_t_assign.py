import ida_kern
k = ida_kern.IDAKern()
k.init()

# This function assign IDAPython's SWIG tinfo_t wrapper into CPP SDK's raw "tinfo_t*"
# tinfo_t is only a simple wrapper around raw typid, like netnode, so we can copy them simply
# But be careful to use the typid as it's having reference count in the IDA kernel internally.
def tinfo_t_assign(c_tif, swig_tif):
    t = swig_tif.copy()
    c_newtif = cast(c_void_p(int(t.this)), POINTER(k.struct_tinfo_t))
    temp = c_tif[0].typid
    c_tif[0].typid = c_newtif[0].typid
    c_newtif[0].typid = temp

swig_t = idaapi.tinfo_t()
assert idaapi.parse_decl(swig_t, None, "void **test;", 0) is not None
c_t = k.struct_tinfo_t()

print('before: [tinfo-c]: %s' % k.dstr_tinfo(byref(c_t)))
print('before: [tinfo-swig]: %s' % swig_t.dstr())

tinfo_t_assign(pointer(c_t), swig_t)


print('after: [tinfo-c]: %s' % k.dstr_tinfo(byref(c_t)))
print('after: [tinfo-swig]: %s' % swig_t.dstr())