__all__ = ['idadll', 'idatypes', 'find_dbctx']
from consolidate.utils.ctypeswrap import *

from ._ida64_win._ida64_dll import ida64 as idadll
from ._ida64_win import _ida64 as idatypes


# using get_ash would be easier

def find_dbctx():
    # get_dbctx_qty find
    dbctx_qty_funptr = get_pointer_address(idadll.get_dbctx_qty)
    print(f"Got dbctx_qty_funptr: {hex(dbctx_qty_funptr)}")
    funchead = bytes(cast(dbctx_qty_funptr, POINTER(c_char))[:0x40])

    pos = funchead.find(b'\xE8') + 5

    assert funchead[pos:pos + 3] == b'\x48\x8b\x3d'

    # patchfinder dbctx_ptr on x86
    dbctx_qty_varptr = int.from_bytes(funchead[pos + 3:pos + 7], 'little') + pos + dbctx_qty_funptr + 7
    dbctx_qty_listptr = dbctx_qty_varptr - 8

    dbctx_arr_ptr = cast(dbctx_qty_listptr, POINTER(c_void_p)).contents
    dbctx_ptr = cast(dbctx_arr_ptr, POINTER(c_void_p)).contents

    print(f"Got dbctx: {hex(dbctx_ptr.value)}")

    dbctx = cast(dbctx_ptr, POINTER(idatypes.struct_dbctx_t))
    return dbctx