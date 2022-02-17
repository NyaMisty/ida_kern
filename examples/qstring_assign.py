import ida_kern
k = ida_kern.IDAKern()
k.init()

# IDA's qstring::assign is inline function, so we have to manually implement it in ctypes
def qstr_assign(qstr, s):
    arr_var = qstr.body.get_cfield('array')
    buflen = len(s) + 1
    if buflen > qstr.body.alloc:
        arr_var.value = k.qvector_reserve(byref(qstr.body), arr_var, buflen, 1)
    qstr.body.n = buflen
    ctypes.memmove(arr_var, s + b'\x00', len(s) + 1)


ret = qstring()
qstr_assign(ret, b'test!!!')

print("qstring struct: <qstring n=%d alloc=%d content=%s>" % (ret.body.n, ret.body.alloc, ret.body.array))