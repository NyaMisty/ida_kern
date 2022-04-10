# -*- coding: utf-8 -*-

#

# TARGET arch is: []

# WORD_SIZE is: 4

# POINTER_SIZE is: 8

# LONGDOUBLE_SIZE is: 8

#

import ctypes



class AsDictMixin:

    @classmethod

    def as_dict(cls, self):

        result = {}

        if not isinstance(self, AsDictMixin):

            # not a structure, assume it's already a python object

            return self

        if not hasattr(cls, "_fields_"):

            return result

        # sys.version_info >= (3, 5)

        # for (field, *_) in cls._fields_:  # noqa

        for field_tuple in cls._fields_:  # noqa

            field = field_tuple[0]

            if field.startswith('PADDING_'):

                continue

            value = getattr(self, field)

            type_ = type(value)

            if hasattr(value, "_length_") and hasattr(value, "_type_"):

                # array

                if not hasattr(type_, "as_dict"):

                    value = [v for v in value]

                else:

                    type_ = type_._type_

                    value = [type_.as_dict(v) for v in value]

            elif hasattr(value, "contents") and hasattr(value, "_type_"):

                # pointer

                try:

                    if not hasattr(type_, "as_dict"):

                        value = value.contents

                    else:

                        type_ = type_._type_

                        value = type_.as_dict(value.contents)

                except ValueError:

                    # nullptr

                    value = None

            elif isinstance(value, AsDictMixin):

                # other structure

                value = type_.as_dict(value)

            result[field] = value

        return result





class Structure(ctypes.Structure, AsDictMixin):



    def __init__(self, *args, **kwds):

        # We don't want to use positional arguments fill PADDING_* fields



        args = dict(zip(self.__class__._field_names_(), args))

        args.update(kwds)

        super(Structure, self).__init__(**args)



    def get_cfield(self, field):

        fieldType = None

        for fn, ftype in self._fields_:

            if fn == field:

                fieldType = ftype

                break

        else:

            raise AttributeError('Field %s not found' % field)



        fieldAttr = getattr(self.__class__, field)

        return fieldType.from_buffer(self, fieldAttr.offset)



    @classmethod

    def _field_names_(cls):

        if hasattr(cls, '_fields_'):

            return (f[0] for f in cls._fields_ if not f[0].startswith('PADDING'))

        else:

            return ()



    @classmethod

    def get_type(cls, field):

        for f in cls._fields_:

            if f[0] == field:

                return f[1]

        return None



    @classmethod

    def bind(cls, bound_fields):

        fields = {}

        for name, type_ in cls._fields_:

            if hasattr(type_, "restype"):

                if name in bound_fields:

                    if bound_fields[name] is None:

                        fields[name] = type_()

                    else:

                        # use a closure to capture the callback from the loop scope

                        fields[name] = (

                            type_((lambda callback: lambda *args: callback(*args))(

                                bound_fields[name]))

                        )

                    del bound_fields[name]

                else:

                    # default callback implementation (does nothing)

                    try:

                        default_ = type_(0).restype().value

                    except TypeError:

                        default_ = None

                    fields[name] = type_((

                        lambda default_: lambda *args: default_)(default_))

            else:

                # not a callback function, use default initialization

                if name in bound_fields:

                    fields[name] = bound_fields[name]

                    del bound_fields[name]

                else:

                    fields[name] = type_()

        if len(bound_fields) != 0:

            raise ValueError(

                "Cannot bind the following unknown callback(s) {}.{}".format(

                    cls.__name__, bound_fields.keys()

            ))

        return cls(**fields)





class Union(ctypes.Union, AsDictMixin):

    pass



def ctypes_in_dll(typ, dll, name):

    try:

        return typ.in_dll(dll, name)

    except (ValueError, TypeError):

        return None






def string_cast(char_pointer, encoding='utf-8', errors='strict'):

    value = ctypes.cast(char_pointer, ctypes.c_char_p).value

    if value is not None and encoding is not None:

        value = value.decode(encoding, errors=errors)

    return value





def char_pointer_cast(string, encoding='utf-8'):

    if encoding is not None:

        try:

            string = string.encode(encoding)

        except AttributeError:

            # In Python3, bytes has no encode attribute

            pass

    string = ctypes.c_char_p(string)

    return ctypes.cast(string, ctypes.POINTER(ctypes.c_char))






c_int128 = ctypes.c_ubyte*16

c_uint128 = c_int128

void = None

if ctypes.sizeof(ctypes.c_longdouble) == 8:

    c_long_double_t = ctypes.c_longdouble

else:

    c_long_double_t = ctypes.c_ubyte*8


def ctypeslib_define():
    
    
    
    class struct_linput_t(Structure):
        pass
    
    
    # values for enumeration 'linput_type_t'
    linput_type_t__enumvalues = {
        0: 'LINPUT_NONE',
        1: 'LINPUT_LOCAL',
        2: 'LINPUT_RFILE',
        3: 'LINPUT_PROCMEM',
        4: 'LINPUT_GENERIC',
    }
    LINPUT_NONE = 0
    LINPUT_LOCAL = 1
    LINPUT_RFILE = 2
    LINPUT_PROCMEM = 3
    LINPUT_GENERIC = 4
    linput_type_t = ctypes.c_uint32 # enum
    class union__493D28877E64802C847645E3DAA9D4CA(Union):
        pass
    
    class struct_generic_linput_t(Structure):
        pass
    
    class struct__iobuf(Structure):
        pass
    
    union__493D28877E64802C847645E3DAA9D4CA._pack_ = 1 # source:False
    union__493D28877E64802C847645E3DAA9D4CA._fields_ = [
        ('fp', ctypes.POINTER(struct__iobuf)),
        ('gl', ctypes.POINTER(struct_generic_linput_t)),
    ]
    
    struct_linput_t._pack_ = 1 # source:False
    struct_linput_t._fields_ = [
        ('type', linput_type_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('___u1', union__493D28877E64802C847645E3DAA9D4CA),
        ('fsize', ctypes.c_int64),
        ('pos', ctypes.c_int64),
        ('bitmap', ctypes.POINTER(ctypes.c_ubyte)),
        ('cache', ctypes.POINTER(ctypes.c_ubyte)),
        ('cbsize', ctypes.c_uint64),
    ]
    
    class struct_dbctx_t(Structure):
        pass
    
    class struct_processor_t(Structure):
        pass
    
    class struct_encoding_vars_t(Structure):
        pass
    
    class struct_strlit_length_cache_t(Structure):
        pass
    
    class struct_gl_vars_t(Structure):
        pass
    
    class struct_asm_t(Structure):
        pass
    
    class struct_trusted_idb_vars_t(Structure):
        pass
    
    class struct_name_vars_t(Structure):
        pass
    
    class struct_custom_data_vars_t(Structure):
        pass
    
    class struct_seg_vars_t(Structure):
        pass
    
    class struct_netnode(Structure):
        pass
    
    class struct_fixup_vars_t(Structure):
        pass
    
    class struct_lines_vars_t(Structure):
        pass
    
    class struct_strlist_vars_t(Structure):
        pass
    
    class struct_group_vars_t(Structure):
        pass
    
    class struct_tryblks_vars_t(Structure):
        pass
    
    class struct_ncache_vars_t(Structure):
        pass
    
    class struct_demangler_vars_t(Structure):
        pass
    
    class struct_segregs_vars_t(Structure):
        pass
    
    class struct_ftable_vars_t(Structure):
        pass
    
    class struct_loader_vars_t(Structure):
        pass
    
    class struct_lex_vars_t(Structure):
        pass
    
    class struct_struct_vars_t(Structure):
        pass
    
    class struct_allprc_vars_t(Structure):
        pass
    
    class struct_idatil_vars_t(Structure):
        pass
    
    class struct_undo_vars_t(Structure):
        pass
    
    class struct_netnode_vars_t(Structure):
        pass
    
    class struct_dbg_vars_t(Structure):
        pass
    
    class struct_signs_vars_t(Structure):
        pass
    
    class struct_func_vars_t(Structure):
        pass
    
    class struct_lowtil_vars_t(Structure):
        pass
    
    class struct_tifcache_vars_t(Structure):
        pass
    
    class struct_auto_vars_t(Structure):
        pass
    
    class struct_debugger_t(Structure):
        pass
    
    class struct_ints_vars_t(Structure):
        pass
    
    class struct_vftable_vars_t(Structure):
        pass
    
    class struct_plugins_vars_t(Structure):
        pass
    
    class struct_dirtreeimpl_vars_t(Structure):
        pass
    
    class struct_snippets_vars_t(Structure):
        pass
    
    class struct_procmod_t(Structure):
        pass
    
    class struct_gdl_vars_t(Structure):
        pass
    
    class struct_module_vars_t(Structure):
        pass
    
    class struct_tinfo_vars_t(Structure):
        pass
    
    class struct_idainfo(Structure):
        pass
    
    class struct_baseinit_vars_t(Structure):
        pass
    
    class struct_kdata_t(Structure):
        pass
    
    class struct_problems_vars_t(Structure):
        pass
    
    class struct_qvector_void__P_(Structure):
        pass
    
    struct_qvector_void__P_._pack_ = 1 # source:False
    struct_qvector_void__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(None))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    
    # values for enumeration 'opening_state_t'
    opening_state_t__enumvalues = {
        0: 'NOT_OPENING_IDB',
        1: 'INITIALIZING_IDB',
        2: 'CREATING_NEW_IDB',
    }
    NOT_OPENING_IDB = 0
    INITIALIZING_IDB = 1
    CREATING_NEW_IDB = 2
    opening_state_t = ctypes.c_uint32 # enum
    class struct_range_t(Structure):
        pass
    
    struct_range_t._pack_ = 1 # source:False
    struct_range_t._fields_ = [
        ('start_ea', ctypes.c_uint64),
        ('end_ea', ctypes.c_uint64),
    ]
    
    class struct_compiler_info_t(Structure):
        pass
    
    struct_compiler_info_t._pack_ = 1 # source:False
    struct_compiler_info_t._fields_ = [
        ('id', ctypes.c_ubyte),
        ('cm', ctypes.c_ubyte),
        ('size_i', ctypes.c_ubyte),
        ('size_b', ctypes.c_ubyte),
        ('size_e', ctypes.c_ubyte),
        ('defalign', ctypes.c_ubyte),
        ('size_s', ctypes.c_ubyte),
        ('size_l', ctypes.c_ubyte),
        ('size_ll', ctypes.c_ubyte),
        ('size_ldbl', ctypes.c_ubyte),
    ]
    
    struct_idainfo._pack_ = 1 # source:False
    struct_idainfo._fields_ = [
        ('tag', ctypes.c_char * 3),
        ('zero', ctypes.c_char),
        ('version', ctypes.c_uint16),
        ('procname', ctypes.c_char * 16),
        ('s_genflags', ctypes.c_uint16),
        ('lflags', ctypes.c_uint32),
        ('database_change_count', ctypes.c_uint32),
        ('filetype', ctypes.c_uint16),
        ('ostype', ctypes.c_uint16),
        ('apptype', ctypes.c_uint16),
        ('asmtype', ctypes.c_ubyte),
        ('specsegs', ctypes.c_ubyte),
        ('af', ctypes.c_uint32),
        ('af2', ctypes.c_uint32),
        ('baseaddr', ctypes.c_uint64),
        ('start_ss', ctypes.c_uint64),
        ('start_cs', ctypes.c_uint64),
        ('start_ip', ctypes.c_uint64),
        ('start_ea', ctypes.c_uint64),
        ('start_sp', ctypes.c_uint64),
        ('main', ctypes.c_uint64),
        ('min_ea', ctypes.c_uint64),
        ('max_ea', ctypes.c_uint64),
        ('omin_ea', ctypes.c_uint64),
        ('omax_ea', ctypes.c_uint64),
        ('lowoff', ctypes.c_uint64),
        ('highoff', ctypes.c_uint64),
        ('maxref', ctypes.c_uint64),
        ('privrange', struct_range_t),
        ('netdelta', ctypes.c_int64),
        ('xrefnum', ctypes.c_ubyte),
        ('type_xrefnum', ctypes.c_ubyte),
        ('refcmtnum', ctypes.c_ubyte),
        ('s_xrefflag', ctypes.c_ubyte),
        ('max_autoname_len', ctypes.c_uint16),
        ('nametype', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte),
        ('short_demnames', ctypes.c_uint32),
        ('long_demnames', ctypes.c_uint32),
        ('demnames', ctypes.c_ubyte),
        ('listnames', ctypes.c_ubyte),
        ('indent', ctypes.c_ubyte),
        ('cmt_indent', ctypes.c_ubyte),
        ('margin', ctypes.c_uint16),
        ('lenxref', ctypes.c_uint16),
        ('outflags', ctypes.c_uint32),
        ('s_cmtflg', ctypes.c_ubyte),
        ('s_limiter', ctypes.c_ubyte),
        ('bin_prefix_size', ctypes.c_int16),
        ('s_prefflag', ctypes.c_ubyte),
        ('strlit_flags', ctypes.c_ubyte),
        ('strlit_break', ctypes.c_ubyte),
        ('strlit_zeroes', ctypes.c_char),
        ('strtype', ctypes.c_int32),
        ('strlit_pref', ctypes.c_char * 16),
        ('strlit_sernum', ctypes.c_uint64),
        ('datatypes', ctypes.c_uint64),
        ('cc', struct_compiler_info_t),
        ('PADDING_1', ctypes.c_ubyte * 2),
        ('abibits', ctypes.c_uint32),
        ('appcall_options', ctypes.c_uint32),
        ('padding', ctypes.c_uint32),
    ]
    
    class struct_qvector__qstring_char___(Structure):
        pass
    
    class struct__qstring_char_(Structure):
        pass
    
    struct_qvector__qstring_char___._pack_ = 1 # source:False
    struct_qvector__qstring_char___._fields_ = [
        ('array', ctypes.POINTER(struct__qstring_char_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__map__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64_____(Structure):
        pass
    
    struct_std__map__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64_____._pack_ = 1 # source:False
    struct_std__map__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_qvector_char_(Structure):
        pass
    
    struct_qvector_char_._pack_ = 1 # source:False
    struct_qvector_char_._fields_ = [
        ('array', ctypes.c_char_p),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct__qstring_char_._pack_ = 1 # source:False
    struct__qstring_char_._fields_ = [
        ('body', struct_qvector_char_),
    ]
    
    class struct_qvector_rangeset_t__P_(Structure):
        pass
    
    class struct_rangeset_t(Structure):
        pass
    
    struct_qvector_rangeset_t__P_._pack_ = 1 # source:False
    struct_qvector_rangeset_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_rangeset_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_rangevec_t(Structure):
        pass
    
    struct_rangevec_t._pack_ = 1 # source:False
    struct_rangevec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_rangeset_t._pack_ = 1 # source:False
    struct_rangeset_t._fields_ = [
        ('bag', struct_rangevec_t),
        ('cache', ctypes.POINTER(struct_range_t)),
        ('undo_code', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_config_t(Structure):
        pass
    
    class struct_text_options_t(Structure):
        pass
    
    class struct_cfgopt_set_vec_t(Structure):
        pass
    
    class struct_qvector_config_t__autorun_plugin_info_t_(Structure):
        pass
    
    class struct_config_t__autorun_plugin_info_t(Structure):
        pass
    
    struct_qvector_config_t__autorun_plugin_info_t_._pack_ = 1 # source:False
    struct_qvector_config_t__autorun_plugin_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_config_t__autorun_plugin_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_config_t__tagged_hash_t(Structure):
        pass
    
    class struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______(Structure):
        pass
    
    struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______._pack_ = 1 # source:False
    struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__map__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________(Structure):
        pass
    
    struct_std__map__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________._pack_ = 1 # source:False
    struct_std__map__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    struct_config_t__tagged_hash_t._pack_ = 1 # source:False
    struct_config_t__tagged_hash_t._fields_ = [
        ('defaults', struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______),
        ('hash', struct_std__map__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________),
    ]
    
    class struct_qvector_config_t__def_proc_t_(Structure):
        pass
    
    class struct_config_t__def_proc_t(Structure):
        pass
    
    struct_qvector_config_t__def_proc_t_._pack_ = 1 # source:False
    struct_qvector_config_t__def_proc_t_._fields_ = [
        ('array', ctypes.POINTER(struct_config_t__def_proc_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__map__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________(Structure):
        pass
    
    struct_std__map__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________._pack_ = 1 # source:False
    struct_std__map__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_rpc_connection_params_t(Structure):
        pass
    
    struct_rpc_connection_params_t._pack_ = 1 # source:False
    struct_rpc_connection_params_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('host', struct__qstring_char_),
        ('port', ctypes.c_uint16),
        ('tls', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 5),
    ]
    
    struct_config_t._pack_ = 1 # source:False
    struct_config_t._fields_ = [
        ('initial_privrange', struct_range_t),
        ('default_processor', struct_qvector_config_t__def_proc_t_),
        ('default_device', struct__qstring_char_),
        ('del_code_comments', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('lookback', ctypes.c_int32),
        ('cultures', struct_qvector__qstring_char___),
        ('encoding_1bpu', struct__qstring_char_),
        ('encoding_to_cultures', struct_std__map__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________),
        ('ida_database_memory', ctypes.c_uint32),
        ('ida_vpages', ctypes.c_uint16),
        ('ida_vpagesize', ctypes.c_uint16),
        ('ida_npagesize', ctypes.c_uint16),
        ('ida_npages', ctypes.c_uint16),
        ('pe_create_idata', ctypes.c_char),
        ('pe_load_resources', ctypes.c_char),
        ('pe_create_flat_group', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte),
        ('cc_vars', struct_config_t__tagged_hash_t),
        ('cpp_namespaces', struct_qvector__qstring_char___),
        ('fpnum_digits', ctypes.c_int32),
        ('fpnum_length', ctypes.c_int32),
        ('ida_workdir', struct__qstring_char_),
        ('ida_append_idb_ext', ctypes.c_char),
        ('PADDING_2', ctypes.c_ubyte * 3),
        ('default_graph_format', ctypes.c_int32),
        ('prolog_color', ctypes.c_uint32),
        ('epilog_color', ctypes.c_uint32),
        ('switch_color', ctypes.c_uint32),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('autorun_plugins', struct_qvector_config_t__autorun_plugin_info_t_),
        ('max_trusted_idb_count', ctypes.c_uint64),
        ('xref_cache_count', ctypes.c_uint64),
        ('elf_debug_file_directory', struct__qstring_char_),
        ('autohide_functail_referers_num', ctypes.c_uint64),
        ('dto', ctypes.POINTER(struct_text_options_t)),
        ('registered_cfgopts', ctypes.POINTER(struct_cfgopt_set_vec_t)),
        ('lumina_md', struct_rpc_connection_params_t),
        ('lumina_min_func_size', ctypes.c_int32),
        ('PADDING_4', ctypes.c_ubyte * 4),
        ('lumina_tlm', struct_rpc_connection_params_t),
        ('upgrade_cpstrings_silent', ctypes.c_char),
        ('PADDING_5', ctypes.c_ubyte * 7),
        ('upgrade_cpstrings_srcenc_oem', struct__qstring_char_),
        ('upgrade_cpstrings_srcenc_ansi', struct__qstring_char_),
        ('apply_name_regexps', ctypes.c_char),
        ('PADDING_6', ctypes.c_ubyte * 7),
    ]
    
    class struct_qvector_rangecb_t__P_(Structure):
        pass
    
    class struct_rangecb_t(Structure):
        pass
    
    struct_qvector_rangecb_t__P_._pack_ = 1 # source:False
    struct_qvector_rangecb_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_rangecb_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_dbctx_t._pack_ = 1 # source:False
    struct_dbctx_t._fields_ = [
        ('command_line_file', struct__qstring_char_),
        ('idb_path', struct__qstring_char_),
        ('id0_path', struct__qstring_char_),
        ('database_flags', ctypes.c_uint32),
        ('startup_time', ctypes.c_int32),
        ('elapsed', ctypes.c_int32),
        ('nopened', ctypes.c_int32),
        ('dbctx_id', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('hexdsp', ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.c_int32)),
        ('cfg', struct_config_t),
        ('config_directives', struct_qvector__qstring_char___),
        ('unhide_hint_text', struct__qstring_char_),
        ('opening_state', opening_state_t),
        ('seen_setproc_user', ctypes.c_char),
        ('seen_p_switch', ctypes.c_char),
        ('idb_loaded', ctypes.c_char),
        ('use_exported_globals', ctypes.c_char),
        ('ptrs', struct_qvector_void__P_),
        ('effective_culture_cps', struct_rangeset_t),
        ('rangecbs', struct_qvector_rangecb_t__P_),
        ('cultures_ranges', struct_qvector_rangeset_t__P_),
        ('cultures_lut', struct_std__map__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64_____),
        ('proc_saved', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 7),
        ('proc_saved_inf', struct_idainfo),
        ('dbg', ctypes.POINTER(struct_debugger_t)),
        ('procmod', ctypes.POINTER(struct_procmod_t)),
        ('inf', ctypes.POINTER(struct_idainfo)),
        ('ph', ctypes.POINTER(struct_processor_t)),
        ('ash', ctypes.POINTER(struct_asm_t)),
        ('root_node', ctypes.POINTER(struct_netnode)),
        ('allprc_vars', ctypes.POINTER(struct_allprc_vars_t)),
        ('auto_vars', ctypes.POINTER(struct_auto_vars_t)),
        ('baseinit_vars', ctypes.POINTER(struct_baseinit_vars_t)),
        ('custom_data_vars', ctypes.POINTER(struct_custom_data_vars_t)),
        ('demangler_vars', ctypes.POINTER(struct_demangler_vars_t)),
        ('dbg_vars', ctypes.POINTER(struct_dbg_vars_t)),
        ('dirtreeimpl_vars', ctypes.POINTER(struct_dirtreeimpl_vars_t)),
        ('encoding_vars', ctypes.POINTER(struct_encoding_vars_t)),
        ('fixup_vars', ctypes.POINTER(struct_fixup_vars_t)),
        ('ftable_vars', ctypes.POINTER(struct_ftable_vars_t)),
        ('func_vars', ctypes.POINTER(struct_func_vars_t)),
        ('gdl_vars', ctypes.POINTER(struct_gdl_vars_t)),
        ('gl_vars', ctypes.POINTER(struct_gl_vars_t)),
        ('group_vars', ctypes.POINTER(struct_group_vars_t)),
        ('idatil_vars', ctypes.POINTER(struct_idatil_vars_t)),
        ('ints_vars', ctypes.POINTER(struct_ints_vars_t)),
        ('kdata', ctypes.POINTER(struct_kdata_t)),
        ('lex_vars', ctypes.POINTER(struct_lex_vars_t)),
        ('lines_vars', ctypes.POINTER(struct_lines_vars_t)),
        ('loader_vars', ctypes.POINTER(struct_loader_vars_t)),
        ('lowtil_vars', ctypes.POINTER(struct_lowtil_vars_t)),
        ('module_vars', ctypes.POINTER(struct_module_vars_t)),
        ('name_vars', ctypes.POINTER(struct_name_vars_t)),
        ('ncache_vars', ctypes.POINTER(struct_ncache_vars_t)),
        ('netnode_vars', ctypes.POINTER(struct_netnode_vars_t)),
        ('plugins_vars', ctypes.POINTER(struct_plugins_vars_t)),
        ('problems_vars', ctypes.POINTER(struct_problems_vars_t)),
        ('seg_vars', ctypes.POINTER(struct_seg_vars_t)),
        ('segregs_vars', ctypes.POINTER(struct_segregs_vars_t)),
        ('signs_vars', ctypes.POINTER(struct_signs_vars_t)),
        ('snippets_vars', ctypes.POINTER(struct_snippets_vars_t)),
        ('strlit_length_cache', ctypes.POINTER(struct_strlit_length_cache_t)),
        ('strlist_vars', ctypes.POINTER(struct_strlist_vars_t)),
        ('struct_vars', ctypes.POINTER(struct_struct_vars_t)),
        ('tifcache_vars', ctypes.POINTER(struct_tifcache_vars_t)),
        ('tinfo_vars', ctypes.POINTER(struct_tinfo_vars_t)),
        ('trusted_idb_vars', ctypes.POINTER(struct_trusted_idb_vars_t)),
        ('tryblks_vars', ctypes.POINTER(struct_tryblks_vars_t)),
        ('undo_vars', ctypes.POINTER(struct_undo_vars_t)),
        ('vftable_vars', ctypes.POINTER(struct_vftable_vars_t)),
    ]
    
    class struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________(Structure):
        pass
    
    class struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________),
    ]
    
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1_),
    ]
    
    class struct_std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1__1_),
         ]
    
    class struct_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t__________std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t____________1_(Structure):
        pass
    
    class struct_std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________(Structure):
        pass
    
    class struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______(Structure):
        pass
    
    struct_std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________._pack_ = 1 # source:False
    struct_std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________._fields_ = [
        ('_Myfirst', ctypes.POINTER(struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______)),
        ('_Mylast', ctypes.POINTER(struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______)),
        ('_Myend', ctypes.POINTER(struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______)),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t__________std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t____________1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t__________std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t____________1_._fields_ = [
        ('_Myval2', struct_std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________),
    ]
    
    class struct_std___Compressed_pair_std__less_network_client_handler_t__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_____(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_____._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_____._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_____),
    ]
    
    struct_std___Compressed_pair_std__less_network_client_handler_t__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_network_client_handler_t__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1_),
    ]
    
    class struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_____(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_____._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_____._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_____),
    ]
    
    struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1_),
    ]
    
    class struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char_________(Structure):
        pass
    
    class struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char_________._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char_________._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char_________),
    ]
    
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1_),
    ]
    
    class struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_____(Structure):
        pass
    
    class struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_____._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_____._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_____),
    ]
    
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1_),
    ]
    
    class struct_std___Compressed_pair_qwstringi_less_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_______(Structure):
        pass
    
    class struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_______._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_______._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_______),
    ]
    
    struct_std___Compressed_pair_qwstringi_less_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_qwstringi_less_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1_),
    ]
    
    class struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char_______(Structure):
        pass
    
    class struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char_______._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char_______._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char_______),
    ]
    
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1_),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_____(Structure):
        pass
    
    class struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Range_eraser(Structure):
        pass
    
    class struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____(Structure):
        pass
    
    class struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_(Structure):
        pass
    
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Range_eraser._pack_ = 1 # source:False
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Range_eraser._fields_ = [
        ('_List', ctypes.POINTER(struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____)),
        ('_Predecessor', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('_Next', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
    ]
    
    class struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Clear_guard(Structure):
        pass
    
    class struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0___(Structure):
        pass
    
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Clear_guard._pack_ = 1 # source:False
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Clear_guard._fields_ = [
        ('_Target', ctypes.POINTER(struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0___)),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_____(Structure):
        pass
    
    class struct_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0_(Structure):
        pass
    
    struct_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0_._pack_ = 1 # source:False
    struct_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std___Compressed_pair_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P____std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______1_(Structure):
        pass
    
    class struct_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_____(Structure):
        pass
    
    struct_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_____._pack_ = 1 # source:False
    struct_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_____._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P____std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P____std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______1_._fields_ = [
        ('_Myval2', struct_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_____),
    ]
    
    struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____._pack_ = 1 # source:False
    struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____._fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P____std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______1_),
    ]
    
    class struct_std___Hash_vec_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t__________std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t____________1_),
         ]
    
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0___._pack_ = 1 # source:False
    struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0___._fields_ = [
        ('_Traitsobj', struct_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0_),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('_List', struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____),
        ('_Vec', struct_std___Hash_vec_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________),
        ('_Mask', ctypes.c_uint64),
        ('_Maxidx', ctypes.c_uint64),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________(Structure):
        pass
    
    class struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_char_const__P_const__P___(Structure):
        pass
    
    class struct_std___Tree_node_char_const__P_const__P_void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_char_const__P_const__P___._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_char_const__P_const__P___._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_char_const__P_const__P___),
    ]
    
    struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1_),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P___(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_network_client_handler_t__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1__1_),
         ]
    
    class struct_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_________(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('first', struct__qstring_char_),
        ('second', struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______),
         ]
    
    struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_________),
    ]
    
    class struct_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char___________(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1__1_),
         ]
    
    class struct_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0_(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1__1_),
         ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________(Structure):
        pass
    
    class struct_std__map_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____(Structure):
        pass
    
    struct_std__map_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____._pack_ = 1 # source:False
    struct_std__map_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__unordered_map_unsigned___int64_bytevec_t_std__hash_unsigned___int64__std__equal_to_unsigned___int64__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____(Structure):
        pass
    
    struct_std__unordered_map_unsigned___int64_bytevec_t_std__hash_unsigned___int64__std__equal_to_unsigned___int64__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____._pack_ = 1 # source:False
    struct_std__unordered_map_unsigned___int64_bytevec_t_std__hash_unsigned___int64__std__equal_to_unsigned___int64__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 64),
    ]
    
    class struct_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0_(Structure):
        pass
    
    class struct_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0_(Structure):
        pass
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1__1_),
         ]
    
    class struct_std__map_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____(Structure):
        pass
    
    struct_std__map_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____._pack_ = 1 # source:False
    struct_std__map_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
    ]
    
    class struct_std___Compressed_pair_std__less_int__std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_int___(Structure):
        pass
    
    class struct_std___Tree_node_int_void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_int___._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_int___._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_int___),
    ]
    
    struct_std___Compressed_pair_std__less_int__std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_int__std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1_),
    ]
    
    class struct_std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1__1_),
         ]
    
    class struct_std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_qwstringi_less_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1__1_),
         ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
    ]
    
    class struct_std___Uninitialized_backout_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________P_(Structure):
        pass
    
    struct_std___Uninitialized_backout_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________P_._pack_ = 1 # source:False
    struct_std___Uninitialized_backout_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________P_._fields_ = [
        ('_First', ctypes.POINTER(struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______)),
        ('_Last', ctypes.POINTER(struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______)),
    ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
    ]
    
    class struct_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0_(Structure):
        pass
    
    class struct_std___List_unchecked_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______std___Iterator_base0_(Structure):
        pass
    
    struct_std___List_unchecked_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___List_unchecked_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
    ]
    
    class struct_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0_(Structure):
        pass
    
    class struct_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0_(Structure):
        pass
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________bool_(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________bool_._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________(Structure):
        pass
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________bool_(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________bool_._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____(Structure):
        pass
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_____(Structure):
        pass
    
    class struct_std__map__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______(Structure):
        pass
    
    struct_std__map__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______._pack_ = 1 # source:False
    struct_std__map__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____(Structure):
        pass
    
    class struct_std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1__1_),
         ]
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
    ]
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____(Structure):
        pass
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_____(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_____(Structure):
        pass
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P____std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P____std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P____std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____(Structure):
        pass
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____(Structure):
        pass
    
    struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._pack_ = 1 # source:False
    struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___List_node_emplace_op2_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____(Structure):
        pass
    
    struct_std___List_node_emplace_op2_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____._pack_ = 1 # source:False
    struct_std___List_node_emplace_op2_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__hash_unsigned___int64__std___Compressed_pair_std__equal_to_unsigned___int64__float_1__1_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__equal_to_unsigned___int64__float_1_(Structure):
        pass
    
    struct_std___Compressed_pair_std__equal_to_unsigned___int64__float_1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__equal_to_unsigned___int64__float_1_._fields_ = [
        ('_Myval2', ctypes.c_float),
    ]
    
    struct_std___Compressed_pair_std__hash_unsigned___int64__std___Compressed_pair_std__equal_to_unsigned___int64__float_1__1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__hash_unsigned___int64__std___Compressed_pair_std__equal_to_unsigned___int64__float_1__1_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__equal_to_unsigned___int64__float_1_),
    ]
    
    class struct_std___List_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______(Structure):
        pass
    
    struct_std___List_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._pack_ = 1 # source:False
    struct_std___List_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____(Structure):
        pass
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
    ]
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Uhash_choose_transparency_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64__void_(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_____(Structure):
        pass
    
    class struct_std___Tree_find_result_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_(Structure):
        pass
    
    
    # values for enumeration 'std___Tree_child'
    std___Tree_child__enumvalues = {
        0: '_Right',
        1: '_Left',
        2: '_Unused',
    }
    _Right = 0
    _Left = 1
    _Unused = 2
    std___Tree_child = ctypes.c_uint32 # enum
    struct_std___Tree_id_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____(Structure):
        pass
    
    class struct_std___List_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______(Structure):
        pass
    
    struct_std___List_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._pack_ = 1 # source:False
    struct_std___List_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________(Structure):
        pass
    
    class struct_std___Tree_find_result_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
    ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P______bool_(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P_____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P_____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P______bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P______bool_._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P_____),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____(Structure):
        pass
    
    class struct_std___In_place_key_extract_map_char_const__P_const__P_std__pair_char_const__P_const__P_unsigned___int64___(Structure):
        pass
    
    class struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
    ]
    
    class struct_std__set_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P___(Structure):
        pass
    
    struct_std__set_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P___._pack_ = 1 # source:False
    struct_std__set_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______(Structure):
        pass
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int____std___Iterator_base0_(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int____std___Iterator_base0_._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int____std___Iterator_base0_._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
    ]
    
    class struct_std__pair_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Hash_find_last_result_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_(Structure):
        pass
    
    struct_std___Hash_find_last_result_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_._pack_ = 1 # source:False
    struct_std___Hash_find_last_result_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_._fields_ = [
        ('_Insert_before', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('_Duplicate', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
    ]
    
    class struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P___(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____(Structure):
        pass
    
    class struct_std__pair_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__unsigned___int64_____(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const___qstring_char_______(Structure):
        pass
    
    class struct_std___In_place_key_extract_map__qstring_wchar_t__std__pair__qstring_wchar_t___qstring_wchar_t_____(Structure):
        pass
    
    class struct_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__hash_unsigned___int64__std___Compressed_pair_std__equal_to_unsigned___int64__float_1__1_),
         ]
    
    class struct_std__pair_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Compressed_pair_std__allocator_char16_t__std___String_val_std___Simple_types_char16_t____1_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char16_t___(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char16_t______Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char16_t______Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char16_t______Bxty._fields_ = [
        ('_Alias', ctypes.c_char * 8),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std___String_val_std___Simple_types_char16_t___._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char16_t___._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char16_t______Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char16_t__std___String_val_std___Simple_types_char16_t____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char16_t__std___String_val_std___Simple_types_char16_t____1_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char16_t___),
    ]
    
    class struct_std___Compressed_pair_std__allocator_char32_t__std___String_val_std___Simple_types_char32_t____1_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char32_t___(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char32_t______Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char32_t______Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char32_t______Bxty._fields_ = [
        ('_Alias', ctypes.c_char * 4),
        ('PADDING_0', ctypes.c_ubyte * 12),
    ]
    
    struct_std___String_val_std___Simple_types_char32_t___._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char32_t___._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char32_t______Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char32_t__std___String_val_std___Simple_types_char32_t____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char32_t__std___String_val_std___Simple_types_char32_t____1_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char32_t___),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_wchar_t__std___String_val_std___Simple_types_wchar_t____1_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_wchar_t___(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_wchar_t______Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_wchar_t______Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_wchar_t______Bxty._fields_ = [
        ('_Buf', ctypes.c_wchar * 8),
        ('_Ptr', ctypes.POINTER(ctypes.c_wchar)),
        ('_Alias', ctypes.c_char * 8),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std___String_val_std___Simple_types_wchar_t___._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_wchar_t___._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_wchar_t______Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_wchar_t__std___String_val_std___Simple_types_wchar_t____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_wchar_t__std___String_val_std___Simple_types_wchar_t____1_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_wchar_t___),
    ]
    
    class struct_std__allocator_traits_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_std__pair_unsigned___int64_const__bytevec_t_____(Structure):
        pass
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__pair_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_char_const__P_const__P_void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_char_const__P_const__P_void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P___(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__unsigned___int64_____(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_char__std___String_val_std___Simple_types_char____1_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char___(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char______Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char______Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char______Bxty._fields_ = [
        ('_Buf', ctypes.c_char * 16),
        ('_Ptr', ctypes.c_char_p),
        ('_Alias', ctypes.c_char * 16),
    ]
    
    struct_std___String_val_std___Simple_types_char___._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char___._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char______Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char__std___String_val_std___Simple_types_char____1_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char__std___String_val_std___Simple_types_char____1_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char___),
    ]
    
    class struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const___qstring_char_______(Structure):
        pass
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______bool_(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______bool_._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____(Structure):
        pass
    
    class struct_std__pair_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__allocator_traits_std__allocator_std__pair_unsigned___int64_const__bytevec_t_____(Structure):
        pass
    
    class struct_std__pair_network_client_handler_t__P_const___qthread_t__P_(Structure):
        pass
    
    class struct_network_client_handler_t(Structure):
        pass
    
    class struct___qthread_t(Structure):
        pass
    
    struct_std__pair_network_client_handler_t__P_const___qthread_t__P_._pack_ = 1 # source:False
    struct_std__pair_network_client_handler_t__P_const___qthread_t__P_._fields_ = [
        ('first', ctypes.POINTER(struct_network_client_handler_t)),
        ('second', ctypes.POINTER(struct___qthread_t)),
    ]
    
    struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair_network_client_handler_t__P_const___qthread_t__P_),
    ]
    
    class struct_std__pair__qstring_char__const__qvector__qstring_char_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('first', struct__qstring_char_),
        ('second', struct_qvector__qstring_char___),
         ]
    
    struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair__qstring_char__const__qvector__qstring_char_____),
    ]
    
    class struct_std__pointer_traits_std__pair_network_client_handler_t__P_const___qthread_t__P___P_(Structure):
        pass
    
    class struct_std__pair_char_const__P_const__P_const_unsigned___int64_(Structure):
        pass
    
    struct_std__pair_char_const__P_const__P_const_unsigned___int64_._pack_ = 1 # source:False
    struct_std__pair_char_const__P_const__P_const_unsigned___int64_._fields_ = [
        ('first', ctypes.POINTER(ctypes.c_char_p)),
        ('second', ctypes.c_uint64),
    ]
    
    struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair_char_const__P_const__P_const_unsigned___int64_),
    ]
    
    class struct_std__basic_string_char16_t_std__char_traits_char16_t__std__allocator_char16_t___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char16_t__std___String_val_std___Simple_types_char16_t____1_),
         ]
    
    class struct_std__basic_string_char32_t_std__char_traits_char32_t__std__allocator_char32_t___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char32_t__std___String_val_std___Simple_types_char32_t____1_),
         ]
    
    class struct_std__initializer_list_std__pair_char_const__P_const__P_const_unsigned___int64___(Structure):
        pass
    
    struct_std__initializer_list_std__pair_char_const__P_const__P_const_unsigned___int64___._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_char_const__P_const__P_const_unsigned___int64___._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_char_const__P_const__P_const_unsigned___int64_)),
        ('_Last', ctypes.POINTER(struct_std__pair_char_const__P_const__P_const_unsigned___int64_)),
    ]
    
    class struct_std__pointer_traits_std__pair_char_const__P_const__P_const_unsigned___int64___P_(Structure):
        pass
    
    class struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___(Structure):
        pass
    
    class struct__qstring_wchar_t_(Structure):
        pass
    
    class struct_qvector_wchar_t_(Structure):
        pass
    
    struct_qvector_wchar_t_._pack_ = 1 # source:False
    struct_qvector_wchar_t_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_int16)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct__qstring_wchar_t_._pack_ = 1 # source:False
    struct__qstring_wchar_t_._fields_ = [
        ('body', struct_qvector_wchar_t_),
    ]
    
    struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___._pack_ = 1 # source:False
    struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___._fields_ = [
        ('first', struct__qstring_wchar_t_),
        ('second', struct__qstring_wchar_t_),
    ]
    
    struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___),
    ]
    
    class struct_std___Default_allocator_traits_std__allocator_std___Tree_node_int_void__P_____(Structure):
        pass
    
    class struct_std__initializer_list_std__pair__qstring_wchar_t__const___qstring_wchar_t_____(Structure):
        pass
    
    struct_std__initializer_list_std__pair__qstring_wchar_t__const___qstring_wchar_t_____._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair__qstring_wchar_t__const___qstring_wchar_t_____._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___)),
        ('_Last', ctypes.POINTER(struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___)),
    ]
    
    class struct_std__pointer_traits_std__pair__qstring_wchar_t__const___qstring_wchar_t_____P_(Structure):
        pass
    
    class struct_std___In_place_key_extract_set_char_const__P_const__P_char_const__P_const__P_(Structure):
        pass
    
    class struct_std__basic_string_wchar_t_std__char_traits_wchar_t__std__allocator_wchar_t___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_wchar_t__std___String_val_std___Simple_types_wchar_t____1_),
         ]
    
    class struct_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P___(Structure):
        pass
    
    class struct_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_______(Structure):
        pass
    
    class struct_std___Tree_find_result_std___Tree_node_char_const__P_const__P_void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_char_const__P_const__P_void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_char_const__P_const__P_void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_char_const__P_const__P_void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_char_const__P_const__P_void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_char_const__P_const__P_void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_char_const__P_const__P_void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
    ]
    
    class struct_std__pair__qstring_char__const__unsigned___int64_(Structure):
        pass
    
    struct_std__pair__qstring_char__const__unsigned___int64_._pack_ = 1 # source:False
    struct_std__pair__qstring_char__const__unsigned___int64_._fields_ = [
        ('first', struct__qstring_char_),
        ('second', ctypes.c_uint64),
    ]
    
    struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair__qstring_char__const__unsigned___int64_),
    ]
    
    class struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_int_void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_int_void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_int_void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_int_void__P_____(Structure):
        pass
    
    class struct_std__allocator_std___Tree_node_int_void__P___(Structure):
        pass
    
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_int_void__P_____._pack_ = 1 # source:False
    struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_int_void__P_____._fields_ = [
        ('_Al', ctypes.POINTER(struct_std__allocator_std___Tree_node_int_void__P___)),
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
    ]
    
    class struct_std__pair__qstring_char__const___qstring_char___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('first', struct__qstring_char_),
        ('second', struct__qstring_char_),
         ]
    
    struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', struct_std__pair__qstring_char__const___qstring_char___),
    ]
    
    class struct_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64___(Structure):
        pass
    
    class struct_std__pointer_traits_std__pair__qstring_char__const__unsigned___int64___P_(Structure):
        pass
    
    class struct_std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_int__std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1__1_),
         ]
    
    class struct_std___Default_allocator_traits_std__allocator_char_const__P_const__P___(Structure):
        pass
    
    class struct_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_____(Structure):
        pass
    
    class struct_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___(Structure):
        pass
    
    class struct_std__pair_unsigned___int64_const__bytevec_t_(Structure):
        pass
    
    class struct_bytevec_t(Structure):
        pass
    
    struct_bytevec_t._pack_ = 1 # source:False
    struct_bytevec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_std__pair_unsigned___int64_const__bytevec_t_._pack_ = 1 # source:False
    struct_std__pair_unsigned___int64_const__bytevec_t_._fields_ = [
        ('first', ctypes.c_uint64),
        ('second', struct_bytevec_t),
    ]
    
    struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_._pack_ = 1 # source:False
    struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_._fields_ = [
        ('_Next', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('_Prev', ctypes.POINTER(struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_)),
        ('_Myval', struct_std__pair_unsigned___int64_const__bytevec_t_),
    ]
    
    class struct_std__allocator_traits_std__allocator_std___Tree_node_int_void__P_____(Structure):
        pass
    
    class struct_std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P_____(Structure):
        pass
    
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P_____._pack_ = 1 # source:False
    struct_std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__basic_string_char_std__char_traits_char__std__allocator_char___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char__std___String_val_std___Simple_types_char____1_),
         ]
    
    class struct_std__initializer_list_std__pair_unsigned___int64_const__bytevec_t___(Structure):
        pass
    
    struct_std__initializer_list_std__pair_unsigned___int64_const__bytevec_t___._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_unsigned___int64_const__bytevec_t___._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_unsigned___int64_const__bytevec_t_)),
        ('_Last', ctypes.POINTER(struct_std__pair_unsigned___int64_const__bytevec_t_)),
    ]
    
    class struct_std__pointer_traits_std__pair_unsigned___int64_const__bytevec_t___P_(Structure):
        pass
    
    class struct_std__allocator_std__pair__qstring_char__const__unsigned___int64___(Structure):
        pass
    
    class struct_std__pair_std___Tree_node_char_const__P_const__P_void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_char_const__P_const__P_void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_char_const__P_const__P_void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Simple_types_std__pair_unsigned___int64_const__bytevec_t___(Structure):
        pass
    
    class struct_std__allocator_std__pair__qstring_char__const___qstring_char_____(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_char_const__P_const__P___(Structure):
        pass
    
    class struct_std__allocator_std__pair_unsigned___int64_const__bytevec_t___(Structure):
        pass
    
    class struct_std___Tset_traits_int_std__less_int__std__allocator_int__0_(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_char16_t___(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_char32_t___(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_wchar_t___(Structure):
        pass
    
    class struct_std___Tree_find_result_std___Tree_node_int_void__P___P_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_int_void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_int_void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_int_void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_std___Tree_find_result_std___Tree_node_int_void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_find_result_std___Tree_node_int_void__P___P_._fields_ = [
        ('_Location', struct_std___Tree_id_std___Tree_node_int_void__P___P_),
        ('_Bound', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
    ]
    
    class struct_create_bytearray_linput____l2__bytearray_linput_t_vtbl(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_char___(Structure):
        pass
    
    class struct_std___Tuple_val_network_client_handler_t__P_const__R_(Structure):
        pass
    
    struct_std___Tuple_val_network_client_handler_t__P_const__R_._pack_ = 1 # source:False
    struct_std___Tuple_val_network_client_handler_t__P_const__R_._fields_ = [
        ('_Val', ctypes.POINTER(ctypes.POINTER(struct_network_client_handler_t))),
    ]
    
    class struct_std___Conditionally_enabled_hash_unsigned___int64_1_(Structure):
        pass
    
    class struct_std___Default_allocator_traits_std__allocator_int___(Structure):
        pass
    
    class struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_b_(Structure):
        pass
    
    struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_b_._pack_ = 1 # source:False
    struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_b_._fields_ = [
        ('s_b1', ctypes.c_ubyte),
        ('s_b2', ctypes.c_ubyte),
        ('s_b3', ctypes.c_ubyte),
        ('s_b4', ctypes.c_ubyte),
    ]
    
    class struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_w_(Structure):
        pass
    
    struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_w_._pack_ = 1 # source:False
    struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_w_._fields_ = [
        ('s_w1', ctypes.c_uint16),
        ('s_w2', ctypes.c_uint16),
    ]
    
    class struct_op_t___unnamed_tag____unnamed_type_specval_shorts_(Structure):
        pass
    
    struct_op_t___unnamed_tag____unnamed_type_specval_shorts_._pack_ = 1 # source:False
    struct_op_t___unnamed_tag____unnamed_type_specval_shorts_._fields_ = [
        ('low', ctypes.c_uint16),
        ('high', ctypes.c_uint16),
    ]
    
    class struct_std__pair_char_const__P_const__P_unsigned___int64_(Structure):
        pass
    
    struct_std__pair_char_const__P_const__P_unsigned___int64_._pack_ = 1 # source:False
    struct_std__pair_char_const__P_const__P_unsigned___int64_._fields_ = [
        ('first', ctypes.POINTER(ctypes.c_char_p)),
        ('second', ctypes.c_uint64),
    ]
    
    class struct_create_bytearray_linput____l2__bytearray_linput_t(Structure):
        pass
    
    struct_create_bytearray_linput____l2__bytearray_linput_t._pack_ = 1 # source:False
    struct_create_bytearray_linput____l2__bytearray_linput_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('start', ctypes.POINTER(ctypes.c_ubyte)),
    ]
    
    class struct_std__set_int_std__less_int__std__allocator_int___(Structure):
        pass
    
    struct_std__set_int_std__less_int__std__allocator_int___._pack_ = 1 # source:False
    struct_std__set_int_std__less_int__std__allocator_int___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_op_t___unnamed_tag____unnamed_type_value_shorts_(Structure):
        pass
    
    struct_op_t___unnamed_tag____unnamed_type_value_shorts_._pack_ = 1 # source:False
    struct_op_t___unnamed_tag____unnamed_type_value_shorts_._fields_ = [
        ('low', ctypes.c_uint16),
        ('high', ctypes.c_uint16),
    ]
    
    class struct_std__allocator_traits_std__allocator_char16_t___(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_char32_t___(Structure):
        pass
    
    class struct_std__tuple_network_client_handler_t__P_const__R_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Myfirst', struct_std___Tuple_val_network_client_handler_t__P_const__R_),
         ]
    
    class struct_op_t___unnamed_tag____unnamed_type_addr_shorts_(Structure):
        pass
    
    struct_op_t___unnamed_tag____unnamed_type_addr_shorts_._pack_ = 1 # source:False
    struct_op_t___unnamed_tag____unnamed_type_addr_shorts_._fields_ = [
        ('low', ctypes.c_uint16),
        ('high', ctypes.c_uint16),
    ]
    
    struct_std___Tree_node_char_const__P_const__P_void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_char_const__P_const__P_void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_char_const__P_const__P_void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', ctypes.POINTER(ctypes.c_char_p)),
    ]
    
    class struct_std__allocator_traits_std__allocator_wchar_t___(Structure):
        pass
    
    class struct_std__pair__qstring_wchar_t___qstring_wchar_t___(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('first', struct__qstring_wchar_t_),
        ('second', struct__qstring_wchar_t_),
         ]
    
    class struct_std__pair_std___Tree_node_int_void__P___P_bool_(Structure):
        pass
    
    struct_std__pair_std___Tree_node_int_void__P___P_bool_._pack_ = 1 # source:False
    struct_std__pair_std___Tree_node_int_void__P___P_bool_._fields_ = [
        ('first', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('second', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_base_dispatcher_t__collect_cliopts____l2__ns_t(Structure):
        pass
    
    class struct_enumerate_sorted_files____l2__collector_t_vtbl(Structure):
        pass
    
    class struct_std__pair__qstring_char___P__qstring_char___P_(Structure):
        pass
    
    struct_std__pair__qstring_char___P__qstring_char___P_._pack_ = 1 # source:False
    struct_std__pair__qstring_char___P__qstring_char___P_._fields_ = [
        ('first', ctypes.POINTER(struct__qstring_char_)),
        ('second', ctypes.POINTER(struct__qstring_char_)),
    ]
    
    class struct_std__initializer_list_char_const__P_const__P_(Structure):
        pass
    
    struct_std__initializer_list_char_const__P_const__P_._pack_ = 1 # source:False
    struct_std__initializer_list_char_const__P_const__P_._fields_ = [
        ('_First', ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p))),
        ('_Last', ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p))),
    ]
    
    class struct_choose_ioport_device____l2__cb_parser_t_vtbl(Structure):
        pass
    
    class struct_enumerate_files____l2__old_enumerator_t_vtbl(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_char___(Structure):
        pass
    
    class struct_std__allocator_traits_std__allocator_int___(Structure):
        pass
    
    class struct_call_atexits____l10__call_exits_req_t_vtbl(Structure):
        pass
    
    class struct_std___Char_traits_char16_t_unsigned_short_(Structure):
        pass
    
    class struct_std___Tuple_val_unsigned___int64_const__R_(Structure):
        pass
    
    struct_std___Tuple_val_unsigned___int64_const__R_._pack_ = 1 # source:False
    struct_std___Tuple_val_unsigned___int64_const__R_._fields_ = [
        ('_Val', ctypes.POINTER(ctypes.c_uint64)),
    ]
    
    class struct_enumerate_sorted_files____l2__collector_t(Structure):
        pass
    
    struct_enumerate_sorted_files____l2__collector_t._pack_ = 1 # source:False
    struct_enumerate_sorted_files____l2__collector_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('files', struct_qvector__qstring_char___),
    ]
    
    class struct_qvector_rangeset_undo_record_t__action_t_(Structure):
        pass
    
    class struct_rangeset_undo_record_t__action_t(Structure):
        pass
    
    struct_qvector_rangeset_undo_record_t__action_t_._pack_ = 1 # source:False
    struct_qvector_rangeset_undo_record_t__action_t_._fields_ = [
        ('array', ctypes.POINTER(struct_rangeset_undo_record_t__action_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std___Char_traits_wchar_t_unsigned_short_(Structure):
        pass
    
    class struct_std__integer_sequence_unsigned___int64_0_(Structure):
        pass
    
    class struct_std___Char_traits_char32_t_unsigned_int_(Structure):
        pass
    
    class struct_std___Tuple_val__qstring_char__const__R_(Structure):
        pass
    
    struct_std___Tuple_val__qstring_char__const__R_._pack_ = 1 # source:False
    struct_std___Tuple_val__qstring_char__const__R_._fields_ = [
        ('_Val', ctypes.POINTER(struct__qstring_char_)),
    ]
    
    class struct_choose_ioport_device____l2__cb_parser_t(Structure):
        pass
    
    struct_choose_ioport_device____l2__cb_parser_t._pack_ = 1 # source:False
    struct_choose_ioport_device____l2__cb_parser_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('parse_params', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_), ctypes.c_char_p)),
    ]
    
    class struct_enumerate_files____l2__old_enumerator_t(Structure):
        pass
    
    struct_enumerate_files____l2__old_enumerator_t._pack_ = 1 # source:False
    struct_enumerate_files____l2__old_enumerator_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('func', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(None))),
        ('ud', ctypes.POINTER(None)),
    ]
    
    class struct_std___In_place_key_extract_set_int_int_(Structure):
        pass
    
    class struct_std__integer_sequence_unsigned___int64_(Structure):
        pass
    
    class struct_qvector_rangecb_undo_record_t__args_t_(Structure):
        pass
    
    class struct_rangecb_undo_record_t__args_t(Structure):
        pass
    
    struct_qvector_rangecb_undo_record_t__args_t_._pack_ = 1 # source:False
    struct_qvector_rangecb_undo_record_t__args_t_._fields_ = [
        ('array', ctypes.POINTER(struct_rangecb_undo_record_t__args_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_read_ioports____l2__cb_fallback_t_vtbl(Structure):
        pass
    
    class struct_std__allocator_char_const__P_const__P_(Structure):
        pass
    
    class struct_std__less_network_client_handler_t__P_(Structure):
        pass
    
    class struct_call_atexits____l10__call_exits_req_t(Structure):
        pass
    
    struct_call_atexits____l10__call_exits_req_t._pack_ = 1 # source:False
    struct_call_atexits____l10__call_exits_req_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('exitcode', ctypes.c_int32),
        ('noret', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
    ]
    
    class struct_std__numeric_limits_unsigned___int64_(Structure):
        pass
    
    class struct_std__tuple_unsigned___int64_const__R_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Myfirst', struct_std___Tuple_val_unsigned___int64_const__R_),
         ]
    
    class struct_idarpc_stream_t__progress_cb_info_t(Structure):
        pass
    
    
    # values for enumeration 'progress_loop_ctrl_t'
    progress_loop_ctrl_t__enumvalues = {
        0: 'plc_proceed',
        1: 'plc_skip_iter',
        2: 'plc_cancel',
    }
    plc_proceed = 0
    plc_skip_iter = 1
    plc_cancel = 2
    progress_loop_ctrl_t = ctypes.c_uint32 # enum
    struct_idarpc_stream_t__progress_cb_info_t._pack_ = 1 # source:False
    struct_idarpc_stream_t__progress_cb_info_t._fields_ = [
        ('cb', ctypes.CFUNCTYPE(progress_loop_ctrl_t, ctypes.c_char, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(None))),
        ('ud', ctypes.POINTER(None)),
        ('ms', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std__tuple__qstring_char__const__R_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Myfirst', struct_std___Tuple_val__qstring_char__const__R_),
         ]
    
    class struct_std___Narrow_char_traits_char_int_(Structure):
        pass
    
    class struct__0AE2711FE0E2D1D4B43BA550E29B8803(Structure):
        pass
    
    struct__0AE2711FE0E2D1D4B43BA550E29B8803._pack_ = 1 # source:False
    struct__0AE2711FE0E2D1D4B43BA550E29B8803._fields_ = [
        ('codepage', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
    ]
    
    class struct__77D3A2E2503DF0742434FD6F35F3BB5C(Structure):
        pass
    
    struct__77D3A2E2503DF0742434FD6F35F3BB5C._pack_ = 1 # source:False
    struct__77D3A2E2503DF0742434FD6F35F3BB5C._fields_ = [
        ('Offset', ctypes.c_uint32),
        ('OffsetHigh', ctypes.c_uint32),
    ]
    
    class struct__B950AFB169DC87688B328897744C612F(Structure):
        pass
    
    struct__B950AFB169DC87688B328897744C612F._pack_ = 1 # source:False
    struct__B950AFB169DC87688B328897744C612F._fields_ = [
        ('LowPart', ctypes.c_uint32),
        ('HighPart', ctypes.c_uint32),
    ]
    
    class struct__FAF74743FBE1C8632047CFB668F7028A(Structure):
        pass
    
    struct__FAF74743FBE1C8632047CFB668F7028A._pack_ = 1 # source:False
    struct__FAF74743FBE1C8632047CFB668F7028A._fields_ = [
        ('LowPart', ctypes.c_uint32),
        ('HighPart', ctypes.c_int32),
    ]
    
    class struct__ULARGE_INTEGER___unnamed_type_u_(Structure):
        pass
    
    struct__ULARGE_INTEGER___unnamed_type_u_._pack_ = 1 # source:False
    struct__ULARGE_INTEGER___unnamed_type_u_._fields_ = [
        ('LowPart', ctypes.c_uint32),
        ('HighPart', ctypes.c_uint32),
    ]
    
    class struct_read_ioports____l2__cb_fallback_t(Structure):
        pass
    
    class struct_qvector_ioport_t_(Structure):
        pass
    
    struct_read_ioports____l2__cb_fallback_t._pack_ = 1 # source:False
    struct_read_ioports____l2__cb_fallback_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('callback', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_qvector_ioport_t_), ctypes.c_char_p)),
    ]
    
    class struct_std__less_char_const__P_const__P_(Structure):
        pass
    
    class struct__LARGE_INTEGER___unnamed_type_u_(Structure):
        pass
    
    struct__LARGE_INTEGER___unnamed_type_u_._pack_ = 1 # source:False
    struct__LARGE_INTEGER___unnamed_type_u_._fields_ = [
        ('LowPart', ctypes.c_uint32),
        ('HighPart', ctypes.c_int32),
    ]
    
    class struct_qvector_qvector_char_const__P___(Structure):
        pass
    
    class struct_qvector_char_const__P_(Structure):
        pass
    
    struct_qvector_qvector_char_const__P___._pack_ = 1 # source:False
    struct_qvector_qvector_char_const__P___._fields_ = [
        ('array', ctypes.POINTER(struct_qvector_char_const__P_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_rangeset_undo_record_t__action_t._pack_ = 1 # source:False
    struct_rangeset_undo_record_t__action_t._fields_ = [
        ('range', struct_range_t),
        ('action', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    struct_config_t__autorun_plugin_info_t._pack_ = 1 # source:False
    struct_config_t__autorun_plugin_info_t._fields_ = [
        ('loader', struct__qstring_char_),
        ('plugin', struct__qstring_char_),
    ]
    
    class struct_qvector_rpc_packet_type_desc_t_(Structure):
        pass
    
    class struct_rpc_packet_type_desc_t(Structure):
        pass
    
    struct_qvector_rpc_packet_type_desc_t_._pack_ = 1 # source:False
    struct_qvector_rpc_packet_type_desc_t_._fields_ = [
        ('array', ctypes.POINTER(struct_rpc_packet_type_desc_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_void____cdecl_P__void__(Structure):
        pass
    
    struct_qvector_void____cdecl_P__void__._pack_ = 1 # source:False
    struct_qvector_void____cdecl_P__void__._fields_ = [
        ('array', ctypes.CFUNCTYPE(None)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__equal_to_unsigned___int64_(Structure):
        pass
    
    class struct__SecPkgCred_SupportedProtocols(Structure):
        pass
    
    struct__SecPkgCred_SupportedProtocols._pack_ = 1 # source:False
    struct__SecPkgCred_SupportedProtocols._fields_ = [
        ('grbitProtocol', ctypes.c_uint32),
    ]
    
    class struct_mt_client_handlers_list_t_vtbl(Structure):
        pass
    
    class struct_std__integral_constant_bool_0_(Structure):
        pass
    
    class struct_std__integral_constant_bool_1_(Structure):
        pass
    
    class struct_netnode__mapper_t__blobdesc_t(Structure):
        pass
    
    struct_netnode__mapper_t__blobdesc_t._pack_ = 1 # source:False
    struct_netnode__mapper_t__blobdesc_t._fields_ = [
        ('tag', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('from', ctypes.c_uint64),
        ('to', ctypes.c_uint64),
    ]
    
    class struct_network_client_handler_t_vtbl(Structure):
        pass
    
    struct_rangecb_undo_record_t__args_t._pack_ = 1 # source:False
    struct_rangecb_undo_record_t__args_t._fields_ = [
        ('act', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('before', struct_bytevec_t),
        ('after', struct_bytevec_t),
        ('n', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('new_ea', ctypes.c_uint64),
        ('was_ea', ctypes.c_uint64),
    ]
    
    class struct_std__less__qstring_wchar_t___(Structure):
        pass
    
    struct_std___Tree_node_int_void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_int_void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_int_void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('_Myval', ctypes.c_int32),
    ]
    
    class struct_std__numeric_limits___int64_(Structure):
        pass
    
    class struct__CRYPT_ALGORITHM_IDENTIFIER(Structure):
        pass
    
    class struct__CRYPTOAPI_BLOB(Structure):
        pass
    
    struct__CRYPTOAPI_BLOB._pack_ = 1 # source:False
    struct__CRYPTOAPI_BLOB._fields_ = [
        ('cbData', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pbData', ctypes.POINTER(ctypes.c_ubyte)),
    ]
    
    struct__CRYPT_ALGORITHM_IDENTIFIER._pack_ = 1 # source:False
    struct__CRYPT_ALGORITHM_IDENTIFIER._fields_ = [
        ('pszObjId', ctypes.c_char_p),
        ('Parameters', struct__CRYPTOAPI_BLOB),
    ]
    
    class struct__RTL_CRITICAL_SECTION_DEBUG(Structure):
        pass
    
    class struct__RTL_CRITICAL_SECTION(Structure):
        pass
    
    class struct__LIST_ENTRY(Structure):
        pass
    
    struct__LIST_ENTRY._pack_ = 1 # source:False
    struct__LIST_ENTRY._fields_ = [
        ('Flink', ctypes.POINTER(struct__LIST_ENTRY)),
        ('Blink', ctypes.POINTER(struct__LIST_ENTRY)),
    ]
    
    struct__RTL_CRITICAL_SECTION_DEBUG._pack_ = 1 # source:False
    struct__RTL_CRITICAL_SECTION_DEBUG._fields_ = [
        ('Type', ctypes.c_uint16),
        ('CreatorBackTraceIndex', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('CriticalSection', ctypes.POINTER(struct__RTL_CRITICAL_SECTION)),
        ('ProcessLocksList', struct__LIST_ENTRY),
        ('EntryCount', ctypes.c_uint32),
        ('ContentionCount', ctypes.c_uint32),
        ('Flags', ctypes.c_uint32),
        ('CreatorBackTraceIndexHigh', ctypes.c_uint16),
        ('SpareWORD', ctypes.c_uint16),
    ]
    
    class struct_client_handlers_list_t_vtbl(Structure):
        pass
    
    class struct_qvector_event_handler_t__P_(Structure):
        pass
    
    class struct_event_handler_t(Structure):
        pass
    
    struct_qvector_event_handler_t__P_._pack_ = 1 # source:False
    struct_qvector_event_handler_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_event_handler_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_recording_rpc_engine_t_vtbl(Structure):
        pass
    
    class struct_std___Char_traits_char_int_(Structure):
        pass
    
    class struct_std__hash_unsigned___int64_(Structure):
        pass
    
    class struct__SecPkgContext_StreamSizes(Structure):
        pass
    
    struct__SecPkgContext_StreamSizes._pack_ = 1 # source:False
    struct__SecPkgContext_StreamSizes._fields_ = [
        ('cbHeader', ctypes.c_uint32),
        ('cbTrailer', ctypes.c_uint32),
        ('cbMaximumMessage', ctypes.c_uint32),
        ('cBuffers', ctypes.c_uint32),
        ('cbBlockSize', ctypes.c_uint32),
    ]
    
    class struct_qvector_event_source_t__P_(Structure):
        pass
    
    class struct_event_source_t(Structure):
        pass
    
    struct_qvector_event_source_t__P_._pack_ = 1 # source:False
    struct_qvector_event_source_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_event_source_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__less__qstring_char___(Structure):
        pass
    
    class struct_unz_file_info64_internal_s(Structure):
        pass
    
    struct_unz_file_info64_internal_s._pack_ = 1 # source:False
    struct_unz_file_info64_internal_s._fields_ = [
        ('offset_curfile', ctypes.c_uint64),
    ]
    
    class struct__CERT_REVOCATION_CRL_INFO(Structure):
        pass
    
    class struct__CRL_CONTEXT(Structure):
        pass
    
    class struct__CRL_ENTRY(Structure):
        pass
    
    struct__CERT_REVOCATION_CRL_INFO._pack_ = 1 # source:False
    struct__CERT_REVOCATION_CRL_INFO._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pBaseCrlContext', ctypes.POINTER(struct__CRL_CONTEXT)),
        ('pDeltaCrlContext', ctypes.POINTER(struct__CRL_CONTEXT)),
        ('pCrlEntry', ctypes.POINTER(struct__CRL_ENTRY)),
        ('fDeltaCrlEntry', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_file_in_zip64_read_info_s(Structure):
        pass
    
    class struct_z_stream_s(Structure):
        pass
    
    struct_z_stream_s._pack_ = 1 # source:False
    struct_z_stream_s._fields_ = [
        ('next_in', ctypes.POINTER(ctypes.c_ubyte)),
        ('avail_in', ctypes.c_uint32),
        ('total_in', ctypes.c_uint32),
        ('next_out', ctypes.POINTER(ctypes.c_ubyte)),
        ('avail_out', ctypes.c_uint32),
        ('total_out', ctypes.c_uint32),
        ('msg', ctypes.c_char_p),
        ('state', ctypes.POINTER(None)),
        ('zalloc', ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_uint32)),
        ('zfree', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('opaque', ctypes.POINTER(None)),
        ('data_type', ctypes.c_int32),
        ('adler', ctypes.c_uint32),
        ('reserved', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_zlib_filefunc64_32_def_s(Structure):
        pass
    
    class struct_zlib_filefunc64_def_s(Structure):
        pass
    
    struct_zlib_filefunc64_def_s._pack_ = 1 # source:False
    struct_zlib_filefunc64_def_s._fields_ = [
        ('zopen64_file', ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_int32)),
        ('zread_file', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32)),
        ('zwrite_file', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32)),
        ('ztell64_file', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('zseek64_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_int32)),
        ('zclose_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('zerror_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('opaque', ctypes.POINTER(None)),
    ]
    
    struct_zlib_filefunc64_32_def_s._pack_ = 1 # source:False
    struct_zlib_filefunc64_32_def_s._fields_ = [
        ('zfile_func64', struct_zlib_filefunc64_def_s),
        ('zopen32_file', ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_char_p, ctypes.c_int32)),
        ('ztell32_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('zseek32_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_int32)),
    ]
    
    struct_file_in_zip64_read_info_s._pack_ = 1 # source:False
    struct_file_in_zip64_read_info_s._fields_ = [
        ('read_buffer', ctypes.c_char_p),
        ('stream', struct_z_stream_s),
        ('pos_in_zipfile', ctypes.c_uint64),
        ('stream_initialised', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('offset_local_extrafield', ctypes.c_uint64),
        ('size_local_extrafield', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('pos_local_extrafield', ctypes.c_uint64),
        ('total_out_64', ctypes.c_uint64),
        ('crc32', ctypes.c_uint32),
        ('crc32_wait', ctypes.c_uint32),
        ('rest_read_compressed', ctypes.c_uint64),
        ('rest_read_uncompressed', ctypes.c_uint64),
        ('z_filefunc', struct_zlib_filefunc64_32_def_s),
        ('filestream', ctypes.POINTER(None)),
        ('compression_method', ctypes.c_uint32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('byte_before_the_zipfile', ctypes.c_uint64),
        ('raw', ctypes.c_int32),
        ('PADDING_3', ctypes.c_ubyte * 4),
    ]
    
    class struct_main_thread_initializer_t(Structure):
        pass
    
    class struct_mt_client_handlers_list_t(Structure):
        pass
    
    class struct___qmutex_t(Structure):
        pass
    
    struct_mt_client_handlers_list_t._pack_ = 1 # source:False
    struct_mt_client_handlers_list_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('mutex', ctypes.POINTER(struct___qmutex_t)),
    ]
    
    class struct_qvector_cancellable_op_t_(Structure):
        pass
    
    class struct_cancellable_op_t(Structure):
        pass
    
    struct_qvector_cancellable_op_t_._pack_ = 1 # source:False
    struct_qvector_cancellable_op_t_._fields_ = [
        ('array', ctypes.POINTER(struct_cancellable_op_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_unsigned___int64_(Structure):
        pass
    
    struct_qvector_unsigned___int64_._pack_ = 1 # source:False
    struct_qvector_unsigned___int64_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_uint64)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_filehandle_linput_t_vtbl(Structure):
        pass
    
    class struct_idarpc_stream_t(Structure):
        pass
    
    struct_network_client_handler_t._pack_ = 1 # source:False
    struct_network_client_handler_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_network_client_handler_t_vtbl)),
        ('channels', ctypes.POINTER(struct__iobuf) * 16),
        ('irs', ctypes.POINTER(struct_idarpc_stream_t)),
        ('peer_name', struct__qstring_char_),
        ('session_id', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('session_start', ctypes.c_uint64),
        ('verbose', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    class struct_qstack_cancellable_op_t_(Structure):
        pass
    
    struct_qstack_cancellable_op_t_._pack_ = 1 # source:False
    struct_qstack_cancellable_op_t_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_qstack_unsigned___int64_(Structure):
        pass
    
    struct_qstack_unsigned___int64_._pack_ = 1 # source:False
    struct_qstack_unsigned___int64_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_mem_octet_stream_t_vtbl(Structure):
        pass
    
    class struct__s__CatchableTypeArray(Structure):
        pass
    
    class struct__s__CatchableType(Structure):
        pass
    
    struct__s__CatchableTypeArray._pack_ = 1 # source:True
    struct__s__CatchableTypeArray._fields_ = [
        ('nCatchableTypes', ctypes.c_int32),
        ('arrayOfCatchableTypes', ctypes.POINTER(struct__s__CatchableType) * 0),
    ]
    
    class struct_base_dispatcher_t_vtbl(Structure):
        pass
    
    class struct_client_handlers_list_t(Structure):
        pass
    
    struct_client_handlers_list_t._pack_ = 1 # source:False
    struct_client_handlers_list_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_client_handlers_list_t_vtbl)),
        ('storage', struct_std__map_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____),
    ]
    
    class struct_netnode__mapper_t_vtbl(Structure):
        pass
    
    class struct_qvector__SecBuffer__P_(Structure):
        pass
    
    class struct__SecBuffer(Structure):
        pass
    
    struct_qvector__SecBuffer__P_._pack_ = 1 # source:False
    struct_qvector__SecBuffer__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct__SecBuffer))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_qvector_char_const__P_._pack_ = 1 # source:False
    struct_qvector_char_const__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_char_p)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_range_cache_t_(Structure):
        pass
    
    class struct_range_cache_t(Structure):
        pass
    
    struct_qvector_range_cache_t_._pack_ = 1 # source:False
    struct_qvector_range_cache_t_._fields_ = [
        ('array', ctypes.POINTER(struct_range_cache_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_rangeset_undo_record_t(Structure):
        pass
    
    
    # values for enumeration 'undo_code_t'
    undo_code_t__enumvalues = {
        4294967295: 'UNDO_NONE',
        0: 'UNDO_ACTION_START',
        1: 'UNDO_BTREE',
        2: 'UNDO_LONGNAME_ADD',
        3: 'UNDO_LONGNAME_DEL',
        4: 'UNDO_MAXNODE_GROW',
        5: 'UNDO_MAXLINK_GROW',
        6: 'UNDO_CHFLAGS',
        7: 'UNDO_CHBYTES',
        8: 'UNDO_AFLAGS_UPD',
        9: 'UNDO_AFLAGS_DEL',
        10: 'UNDO_AFLAGS_KILL',
        11: 'UNDO_AFLAGS_INS_RANGE',
        12: 'UNDO_VMEM_RANGES',
        13: 'UNDO_SPARSE_RANGES',
        14: 'UNDO_ZERO_RANGES',
        15: 'UNDO_RANGECB_FILEREGIONS',
        16: 'UNDO_RANGECB_MAPPING',
        17: 'UNDO_RANGECB_SOURCEFILES',
        18: 'UNDO_RANGECB_HIDDEN_RANGES',
        19: 'UNDO_RANGECB_FUNCS',
        20: 'UNDO_RANGECB_SEGS',
        21: 'UNDO_DREF_FROM_INS',
        22: 'UNDO_DREF_FROM_DEL',
        23: 'UNDO_DREF_TO_INS',
        24: 'UNDO_DREF_TO_DEL',
        25: 'UNDO_CREF_FROM_INS',
        26: 'UNDO_CREF_FROM_DEL',
        27: 'UNDO_CREF_TO_INS',
        28: 'UNDO_CREF_TO_DEL',
        29: 'UNDO_VA_FLAGS',
        30: 'UNDO_VA_NAMES',
        31: 'UNDO_FUNCS',
        32: 'UNDO_AU_UNK',
        37: 'UNDO_AU_CODE',
        42: 'UNDO_AU_WEAK',
        47: 'UNDO_AU_PROC',
        52: 'UNDO_AU_TAIL',
        57: 'UNDO_AU_FCHUNK',
        62: 'UNDO_AU_USED',
        67: 'UNDO_AU_TYPE',
        72: 'UNDO_AU_LIBF',
        77: 'UNDO_AU_LBF2',
        82: 'UNDO_AU_LBF3',
        87: 'UNDO_AU_CHLB',
        92: 'UNDO_AU_FINAL',
        97: 'UNDO_AU_HNNODE',
        102: 'UNDO_AU_POSTPONED',
        107: 'UNDO_AU_EMPTY',
        108: 'UNDO_AU_DONE',
        109: 'UNDO_AU_AUTO_STATE',
        110: 'UNDO_AU_WEAK_INS',
        111: 'UNDO_AU_WEAK_DEL',
        112: 'UNDO_SEGS',
        113: 'UNDO_SEGS_SELS_UPD',
        114: 'UNDO_SEGS_SELS_INS',
        115: 'UNDO_SEGS_SELS_DEL',
        116: 'UNDO_SEGS_NAME_ADD',
        117: 'UNDO_SEGS_NAME_DEL',
        118: 'UNDO_SEGS_NAME_EA_ADD',
        119: 'UNDO_SEGS_NAME_EA_DEL',
        120: 'UNDO_SEGS_NAME_CLS_ADD',
        121: 'UNDO_SEGS_NAME_CLS_DEL',
        122: 'UNDO_SEGS_NAME_MOVE',
        123: 'UNDO_STRUC',
        124: 'UNDO_STRUC_NODES',
        125: 'UNDO_STRUC_IDX',
        126: 'UNDO_STRUC_ADJUST_IDX',
        127: 'UNDO_DBG_SYM2EA_INS',
        128: 'UNDO_DBG_SYM2EA_DEL',
        129: 'UNDO_DBG_SYM2EA_KILL',
        130: 'UNDO_DBG_EA2SYM_INS',
        131: 'UNDO_DBG_EA2SYM_DEL',
        132: 'UNDO_DBG_EA2SYM_KILL',
        133: 'UNDO_DBG_EA2SYM_NAMEVEC_INS',
        134: 'UNDO_DBG_EA2SYM_NAMEVEC_DEL',
        135: 'UNDO_MAXSERIALNAME_INC',
        136: 'UNDO_MAXSERIALNAME_RESET',
        137: 'UNDO_LOWTIL_ADDENTRY',
        138: 'UNDO_LOWTIL_DELENTRY',
        139: 'UNDO_LOWTIL_SET_ALIAS',
        140: 'UNDO_LOWTIL_ALLOC_ORDS',
        141: 'UNDO_LOWTIL_ENABLE_NUMBERED',
        142: 'UNDO_LOWTIL_ABINAME',
        143: 'UNDO_IDATIL_ADD',
        144: 'UNDO_IDATIL_DEL',
        145: 'UNDO_IDATIL_STDORD_INS',
        146: 'UNDO_VFTABLES_UPD',
        147: 'UNDO_VFTABLES_DEL',
        148: 'UNDO_VFTABLES_KILL',
        149: 'UNDO_EATIFS_UPDATE',
        150: 'UNDO_EATIFS_DELETE',
        151: 'UNDO_OPTIFS_UPDATE',
        152: 'UNDO_OPTIFS_DELETE',
        153: 'UNDO_MOVE_TINFO_CACHE',
        154: 'UNDO_SPARSE_FLAGS_INS_RANGE',
        155: 'UNDO_DBG_FLAGS_INS_RANGE',
        156: 'UNDO_SPARSE_FLAGS_DEL_RANGE',
        157: 'UNDO_DBG_FLAGS_DEL_RANGE',
        158: 'UNDO_SPARSE_FLAGS_SIZE',
        159: 'UNDO_INF',
        160: 'UNDO_NIMPLIBS',
        161: 'UNDO_FIXUP_DEL',
        162: 'UNDO_FIXUP_DEL_RANGE',
        163: 'UNDO_FIXUP_INS_RANGE',
        164: 'UNDO_FIXUP_UPD',
        165: 'UNDO_TRYBLK_CACHE_INS',
        166: 'UNDO_TRYBLK_CACHE_DEL',
        167: 'UNDO_TRYBLK_EAS_INS',
        168: 'UNDO_TRYBLK_EAS_DEL',
        169: 'UNDO_TRYBLK_MOVE',
        170: 'UNDO_GROUPSEL',
        171: 'UNDO_ENCODING_LIST_ADD',
        172: 'UNDO_ENCODING_LIST_DEL',
        173: 'UNDO_ENCODING_LIST_UPD',
        174: 'UNDO_DEFAULT_ENCODING_IDX',
        175: 'UNDO_OUTFILE_ENCODING_IDX',
        176: 'UNDO_PROBLEM_ROLLBACK_ADD',
        177: 'UNDO_PROBLEM_ROLLBACK_DEL',
        178: 'UNDO_SEGREGS_ADD',
        179: 'UNDO_SEGREGS_DEL',
        180: 'UNDO_SEGREGS_SET_START',
        181: 'UNDO_SEGREGS_SET_END',
        182: 'UNDO_SEGREGS_UPD',
        183: 'UNDO_SEGREGS_INS_RANGE',
        184: 'UNDO_SEGREGS_DEL_RANGE',
        185: 'UNDO_SEGREGS_COPY',
        186: 'UNDO_BPT_ADD',
        187: 'UNDO_BPT_UPD',
        188: 'UNDO_BPT_DEL',
        189: 'UNDO_BPT_ENABLE',
        190: 'UNDO_BPTS_MOVE',
        191: 'UNDO_BPT_SET_LOC_STRING',
        192: 'UNDO_BPTS_CHANGE_BPTLOC',
        193: 'UNDO_BPT_GROUPS_ADD',
        194: 'UNDO_BPT_GROUPS_DEL',
        195: 'UNDO_BPT_GROUPS_RENAME',
        196: 'UNDO_BPT_GROUPS_CHANGE_BPTGRP',
        197: 'UNDO_STRLIST_MOVED',
        198: 'UNDO_DT_LOCAL_TYPES',
        199: 'UNDO_DT_STRUCTS',
        200: 'UNDO_DT_ENUMS',
        201: 'UNDO_DT_FUNCS',
        202: 'UNDO_DT_NAMES',
        203: 'UNDO_DT_IMPORTS',
        204: 'UNDO_DT_BOOKMARKS_IDAPLACE',
        205: 'UNDO_DT_BOOKMARKS_STRUCTS',
        206: 'UNDO_DT_BOOKMARKS_ENUMS',
        207: 'UNDO_DT_BPTS',
        208: 'UNDO_DT_PROBLEMS',
        209: 'UNDO_DT_DIRTY',
        210: 'UNDO_NCACHE',
        211: 'UNDO_NCACHE_MOVE',
        212: 'UNDO_DTW_CUT_PATHS_ADD',
        213: 'UNDO_DTW_CUT_PATHS_DEL',
        214: 'UNDO_POOL_START',
    }
    UNDO_NONE = 4294967295
    UNDO_ACTION_START = 0
    UNDO_BTREE = 1
    UNDO_LONGNAME_ADD = 2
    UNDO_LONGNAME_DEL = 3
    UNDO_MAXNODE_GROW = 4
    UNDO_MAXLINK_GROW = 5
    UNDO_CHFLAGS = 6
    UNDO_CHBYTES = 7
    UNDO_AFLAGS_UPD = 8
    UNDO_AFLAGS_DEL = 9
    UNDO_AFLAGS_KILL = 10
    UNDO_AFLAGS_INS_RANGE = 11
    UNDO_VMEM_RANGES = 12
    UNDO_SPARSE_RANGES = 13
    UNDO_ZERO_RANGES = 14
    UNDO_RANGECB_FILEREGIONS = 15
    UNDO_RANGECB_MAPPING = 16
    UNDO_RANGECB_SOURCEFILES = 17
    UNDO_RANGECB_HIDDEN_RANGES = 18
    UNDO_RANGECB_FUNCS = 19
    UNDO_RANGECB_SEGS = 20
    UNDO_DREF_FROM_INS = 21
    UNDO_DREF_FROM_DEL = 22
    UNDO_DREF_TO_INS = 23
    UNDO_DREF_TO_DEL = 24
    UNDO_CREF_FROM_INS = 25
    UNDO_CREF_FROM_DEL = 26
    UNDO_CREF_TO_INS = 27
    UNDO_CREF_TO_DEL = 28
    UNDO_VA_FLAGS = 29
    UNDO_VA_NAMES = 30
    UNDO_FUNCS = 31
    UNDO_AU_UNK = 32
    UNDO_AU_CODE = 37
    UNDO_AU_WEAK = 42
    UNDO_AU_PROC = 47
    UNDO_AU_TAIL = 52
    UNDO_AU_FCHUNK = 57
    UNDO_AU_USED = 62
    UNDO_AU_TYPE = 67
    UNDO_AU_LIBF = 72
    UNDO_AU_LBF2 = 77
    UNDO_AU_LBF3 = 82
    UNDO_AU_CHLB = 87
    UNDO_AU_FINAL = 92
    UNDO_AU_HNNODE = 97
    UNDO_AU_POSTPONED = 102
    UNDO_AU_EMPTY = 107
    UNDO_AU_DONE = 108
    UNDO_AU_AUTO_STATE = 109
    UNDO_AU_WEAK_INS = 110
    UNDO_AU_WEAK_DEL = 111
    UNDO_SEGS = 112
    UNDO_SEGS_SELS_UPD = 113
    UNDO_SEGS_SELS_INS = 114
    UNDO_SEGS_SELS_DEL = 115
    UNDO_SEGS_NAME_ADD = 116
    UNDO_SEGS_NAME_DEL = 117
    UNDO_SEGS_NAME_EA_ADD = 118
    UNDO_SEGS_NAME_EA_DEL = 119
    UNDO_SEGS_NAME_CLS_ADD = 120
    UNDO_SEGS_NAME_CLS_DEL = 121
    UNDO_SEGS_NAME_MOVE = 122
    UNDO_STRUC = 123
    UNDO_STRUC_NODES = 124
    UNDO_STRUC_IDX = 125
    UNDO_STRUC_ADJUST_IDX = 126
    UNDO_DBG_SYM2EA_INS = 127
    UNDO_DBG_SYM2EA_DEL = 128
    UNDO_DBG_SYM2EA_KILL = 129
    UNDO_DBG_EA2SYM_INS = 130
    UNDO_DBG_EA2SYM_DEL = 131
    UNDO_DBG_EA2SYM_KILL = 132
    UNDO_DBG_EA2SYM_NAMEVEC_INS = 133
    UNDO_DBG_EA2SYM_NAMEVEC_DEL = 134
    UNDO_MAXSERIALNAME_INC = 135
    UNDO_MAXSERIALNAME_RESET = 136
    UNDO_LOWTIL_ADDENTRY = 137
    UNDO_LOWTIL_DELENTRY = 138
    UNDO_LOWTIL_SET_ALIAS = 139
    UNDO_LOWTIL_ALLOC_ORDS = 140
    UNDO_LOWTIL_ENABLE_NUMBERED = 141
    UNDO_LOWTIL_ABINAME = 142
    UNDO_IDATIL_ADD = 143
    UNDO_IDATIL_DEL = 144
    UNDO_IDATIL_STDORD_INS = 145
    UNDO_VFTABLES_UPD = 146
    UNDO_VFTABLES_DEL = 147
    UNDO_VFTABLES_KILL = 148
    UNDO_EATIFS_UPDATE = 149
    UNDO_EATIFS_DELETE = 150
    UNDO_OPTIFS_UPDATE = 151
    UNDO_OPTIFS_DELETE = 152
    UNDO_MOVE_TINFO_CACHE = 153
    UNDO_SPARSE_FLAGS_INS_RANGE = 154
    UNDO_DBG_FLAGS_INS_RANGE = 155
    UNDO_SPARSE_FLAGS_DEL_RANGE = 156
    UNDO_DBG_FLAGS_DEL_RANGE = 157
    UNDO_SPARSE_FLAGS_SIZE = 158
    UNDO_INF = 159
    UNDO_NIMPLIBS = 160
    UNDO_FIXUP_DEL = 161
    UNDO_FIXUP_DEL_RANGE = 162
    UNDO_FIXUP_INS_RANGE = 163
    UNDO_FIXUP_UPD = 164
    UNDO_TRYBLK_CACHE_INS = 165
    UNDO_TRYBLK_CACHE_DEL = 166
    UNDO_TRYBLK_EAS_INS = 167
    UNDO_TRYBLK_EAS_DEL = 168
    UNDO_TRYBLK_MOVE = 169
    UNDO_GROUPSEL = 170
    UNDO_ENCODING_LIST_ADD = 171
    UNDO_ENCODING_LIST_DEL = 172
    UNDO_ENCODING_LIST_UPD = 173
    UNDO_DEFAULT_ENCODING_IDX = 174
    UNDO_OUTFILE_ENCODING_IDX = 175
    UNDO_PROBLEM_ROLLBACK_ADD = 176
    UNDO_PROBLEM_ROLLBACK_DEL = 177
    UNDO_SEGREGS_ADD = 178
    UNDO_SEGREGS_DEL = 179
    UNDO_SEGREGS_SET_START = 180
    UNDO_SEGREGS_SET_END = 181
    UNDO_SEGREGS_UPD = 182
    UNDO_SEGREGS_INS_RANGE = 183
    UNDO_SEGREGS_DEL_RANGE = 184
    UNDO_SEGREGS_COPY = 185
    UNDO_BPT_ADD = 186
    UNDO_BPT_UPD = 187
    UNDO_BPT_DEL = 188
    UNDO_BPT_ENABLE = 189
    UNDO_BPTS_MOVE = 190
    UNDO_BPT_SET_LOC_STRING = 191
    UNDO_BPTS_CHANGE_BPTLOC = 192
    UNDO_BPT_GROUPS_ADD = 193
    UNDO_BPT_GROUPS_DEL = 194
    UNDO_BPT_GROUPS_RENAME = 195
    UNDO_BPT_GROUPS_CHANGE_BPTGRP = 196
    UNDO_STRLIST_MOVED = 197
    UNDO_DT_LOCAL_TYPES = 198
    UNDO_DT_STRUCTS = 199
    UNDO_DT_ENUMS = 200
    UNDO_DT_FUNCS = 201
    UNDO_DT_NAMES = 202
    UNDO_DT_IMPORTS = 203
    UNDO_DT_BOOKMARKS_IDAPLACE = 204
    UNDO_DT_BOOKMARKS_STRUCTS = 205
    UNDO_DT_BOOKMARKS_ENUMS = 206
    UNDO_DT_BPTS = 207
    UNDO_DT_PROBLEMS = 208
    UNDO_DT_DIRTY = 209
    UNDO_NCACHE = 210
    UNDO_NCACHE_MOVE = 211
    UNDO_DTW_CUT_PATHS_ADD = 212
    UNDO_DTW_CUT_PATHS_DEL = 213
    UNDO_POOL_START = 214
    undo_code_t = ctypes.c_uint32 # enum
    struct_rangeset_undo_record_t._pack_ = 1 # source:False
    struct_rangeset_undo_record_t._fields_ = [
        ('actions', struct_qvector_rangeset_undo_record_t__action_t_),
        ('uc', undo_code_t),
        ('ready', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
    ]
    
    class struct_recording_rpc_engine_t(Structure):
        pass
    
    struct_recording_rpc_engine_t._pack_ = 1 # source:False
    struct_recording_rpc_engine_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 56),
        ('rpc_irs', ctypes.POINTER(struct_idarpc_stream_t)),
        ('our_irs', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 7),
        ('conv', ctypes.POINTER(struct__iobuf)),
    ]
    
    class struct_rpc_packet_data_t_vtbl(Structure):
        pass
    
    class struct_rpc_packet_data_t(Structure):
        pass
    
    struct_rpc_packet_type_desc_t._pack_ = 1 # source:False
    struct_rpc_packet_type_desc_t._fields_ = [
        ('code', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('name', ctypes.c_char_p),
        ('instantiate', ctypes.CFUNCTYPE(ctypes.POINTER(struct_rpc_packet_data_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint64, ctypes.c_int32)),
    ]
    
    class struct__CERT_PUBLIC_KEY_INFO(Structure):
        pass
    
    class struct__CRYPT_BIT_BLOB(Structure):
        pass
    
    struct__CRYPT_BIT_BLOB._pack_ = 1 # source:False
    struct__CRYPT_BIT_BLOB._fields_ = [
        ('cbData', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pbData', ctypes.POINTER(ctypes.c_ubyte)),
        ('cUnusedBits', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    struct__CERT_PUBLIC_KEY_INFO._pack_ = 1 # source:False
    struct__CERT_PUBLIC_KEY_INFO._fields_ = [
        ('Algorithm', struct__CRYPT_ALGORITHM_IDENTIFIER),
        ('PublicKey', struct__CRYPT_BIT_BLOB),
    ]
    
    class struct__CERT_REVOCATION_INFO(Structure):
        pass
    
    struct__CERT_REVOCATION_INFO._pack_ = 1 # source:False
    struct__CERT_REVOCATION_INFO._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('dwRevocationResult', ctypes.c_uint32),
        ('pszRevocationOid', ctypes.c_char_p),
        ('pvOidSpecificInfo', ctypes.POINTER(None)),
        ('fHasFreshnessTime', ctypes.c_int32),
        ('dwFreshnessTime', ctypes.c_uint32),
        ('pCrlInfo', ctypes.POINTER(struct__CERT_REVOCATION_CRL_INFO)),
    ]
    
    class struct__CERT_TRUST_LIST_INFO(Structure):
        pass
    
    class struct__CTL_CONTEXT(Structure):
        pass
    
    class struct__CTL_ENTRY(Structure):
        pass
    
    struct__CERT_TRUST_LIST_INFO._pack_ = 1 # source:False
    struct__CERT_TRUST_LIST_INFO._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pCtlEntry', ctypes.POINTER(struct__CTL_ENTRY)),
        ('pCtlContext', ctypes.POINTER(struct__CTL_CONTEXT)),
    ]
    
    struct__RTL_CRITICAL_SECTION._pack_ = 1 # source:False
    struct__RTL_CRITICAL_SECTION._fields_ = [
        ('DebugInfo', ctypes.POINTER(struct__RTL_CRITICAL_SECTION_DEBUG)),
        ('LockCount', ctypes.c_int32),
        ('RecursionCount', ctypes.c_int32),
        ('OwningThread', ctypes.POINTER(None)),
        ('LockSemaphore', ctypes.POINTER(None)),
        ('SpinCount', ctypes.c_uint64),
    ]
    
    class struct_backmap_initializer_t(Structure):
        pass
    
    class struct_device_chooser_t_vtbl(Structure):
        pass
    
    class struct_generic_client_t_vtbl(Structure):
        pass
    
    class struct_inflate_linput_t_vtbl(Structure):
        pass
    
    class struct_qstring_simple_init_t(Structure):
        pass
    
    struct_qstring_simple_init_t._pack_ = 1 # source:False
    struct_qstring_simple_init_t._fields_ = [
        ('body', ctypes.c_ubyte * 24),
    ]
    
    class struct_range_visitor2_t_vtbl(Structure):
        pass
    
    class struct_rangecb_undo_record_t(Structure):
        pass
    
    struct_rangecb_undo_record_t._pack_ = 1 # source:False
    struct_rangecb_undo_record_t._fields_ = [
        ('actions', struct_bytevec_t),
        ('backstore', struct_std__unordered_map_unsigned___int64_bytevec_t_std__hash_unsigned___int64__std__equal_to_unsigned___int64__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____),
        ('last_size', ctypes.c_uint64),
        ('unpacked_actions', struct_qvector_rangecb_undo_record_t__args_t_),
        ('undo_code', undo_code_t),
        ('compound_lvl', ctypes.c_uint32),
    ]
    
    class struct__PROCESS_INFORMATION(Structure):
        pass
    
    struct__PROCESS_INFORMATION._pack_ = 1 # source:False
    struct__PROCESS_INFORMATION._fields_ = [
        ('hProcess', ctypes.POINTER(None)),
        ('hThread', ctypes.POINTER(None)),
        ('dwProcessId', ctypes.c_uint32),
        ('dwThreadId', ctypes.c_uint32),
    ]
    
    class struct__SECURITY_ATTRIBUTES(Structure):
        pass
    
    struct__SECURITY_ATTRIBUTES._pack_ = 1 # source:False
    struct__SECURITY_ATTRIBUTES._fields_ = [
        ('nLength', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('lpSecurityDescriptor', ctypes.POINTER(None)),
        ('bInheritHandle', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    struct_config_t__def_proc_t._pack_ = 1 # source:False
    struct_config_t__def_proc_t._fields_ = [
        ('ext', ctypes.c_char * 10),
        ('proc', ctypes.c_char * 16),
    ]
    
    class struct_event_handler_t_vtbl(Structure):
        pass
    
    class struct_idarpc_stream_t_vtbl(Structure):
        pass
    
    class struct_irs_cancellable_op_t(Structure):
        pass
    
    struct_irs_cancellable_op_t._pack_ = 1 # source:False
    struct_irs_cancellable_op_t._fields_ = [
        ('irs', ctypes.POINTER(struct_idarpc_stream_t)),
    ]
    
    class struct__CERT_CHAIN_CONTEXT(Structure):
        pass
    
    class struct__CERT_SIMPLE_CHAIN(Structure):
        pass
    
    class struct__CERT_TRUST_STATUS(Structure):
        pass
    
    struct__CERT_TRUST_STATUS._pack_ = 1 # source:False
    struct__CERT_TRUST_STATUS._fields_ = [
        ('dwErrorStatus', ctypes.c_uint32),
        ('dwInfoStatus', ctypes.c_uint32),
    ]
    
    class struct__GUID(Structure):
        pass
    
    struct__GUID._pack_ = 1 # source:False
    struct__GUID._fields_ = [
        ('Data1', ctypes.c_uint32),
        ('Data2', ctypes.c_uint16),
        ('Data3', ctypes.c_uint16),
        ('Data4', ctypes.c_ubyte * 8),
    ]
    
    struct__CERT_CHAIN_CONTEXT._pack_ = 1 # source:False
    struct__CERT_CHAIN_CONTEXT._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('TrustStatus', struct__CERT_TRUST_STATUS),
        ('cChain', ctypes.c_uint32),
        ('rgpChain', ctypes.POINTER(ctypes.POINTER(struct__CERT_SIMPLE_CHAIN))),
        ('cLowerQualityChainContext', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rgpLowerQualityChainContext', ctypes.POINTER(ctypes.POINTER(struct__CERT_CHAIN_CONTEXT))),
        ('fHasRevocationFreshnessTime', ctypes.c_int32),
        ('dwRevocationFreshnessTime', ctypes.c_uint32),
        ('dwCreateFlags', ctypes.c_uint32),
        ('ChainId', struct__GUID),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct__CERT_CHAIN_ELEMENT(Structure):
        pass
    
    class struct__CTL_USAGE(Structure):
        pass
    
    class struct__CERT_CONTEXT(Structure):
        pass
    
    struct__CERT_CHAIN_ELEMENT._pack_ = 1 # source:False
    struct__CERT_CHAIN_ELEMENT._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pCertContext', ctypes.POINTER(struct__CERT_CONTEXT)),
        ('TrustStatus', struct__CERT_TRUST_STATUS),
        ('pRevocationInfo', ctypes.POINTER(struct__CERT_REVOCATION_INFO)),
        ('pIssuanceUsage', ctypes.POINTER(struct__CTL_USAGE)),
        ('pApplicationUsage', ctypes.POINTER(struct__CTL_USAGE)),
        ('pwszExtendedErrorInfo', ctypes.POINTER(ctypes.c_wchar)),
    ]
    
    class struct_dual_text_options_t(Structure):
        pass
    
    struct_dual_text_options_t._pack_ = 1 # source:False
    struct_dual_text_options_t._fields_ = [
        ('mysize', ctypes.c_int32),
        ('graph_view', ctypes.c_char),
        ('xrefnum', ctypes.c_ubyte),
        ('s_showpref', ctypes.c_char),
        ('cmt_indent', ctypes.c_ubyte),
        ('indent', ctypes.c_ubyte),
        ('s_limiter', ctypes.c_ubyte),
        ('margin', ctypes.c_uint16),
        ('bin_prefix_size', ctypes.c_uint16),
        ('s_prefflag', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte),
    ]
    
    class struct_event_source_t_vtbl(Structure):
        pass
    
    class struct_filehandle_linput_t(Structure):
        pass
    
    struct_filehandle_linput_t._pack_ = 1 # source:False
    struct_filehandle_linput_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('fd', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_netnode__key_info_t(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('key', struct_bytevec_t),
        ('data', struct_bytevec_t),
         ]
    
    class struct_octet_stream_t_vtbl(Structure):
        pass
    
    class struct_qvector__SecBuffer_(Structure):
        pass
    
    struct_qvector__SecBuffer_._pack_ = 1 # source:False
    struct_qvector__SecBuffer_._fields_ = [
        ('array', ctypes.POINTER(struct__SecBuffer)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_tcpip_stream_t_vtbl(Structure):
        pass
    
    class struct_unz_global_info64_s(Structure):
        pass
    
    struct_unz_global_info64_s._pack_ = 1 # source:False
    struct_unz_global_info64_s._fields_ = [
        ('number_entry', ctypes.c_uint64),
        ('size_comment', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_zlib_filefunc_def_s(Structure):
        pass
    
    struct_zlib_filefunc_def_s._pack_ = 1 # source:False
    struct_zlib_filefunc_def_s._fields_ = [
        ('zopen_file', ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_char_p, ctypes.c_int32)),
        ('zread_file', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32)),
        ('zwrite_file', ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32)),
        ('ztell_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('zseek_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_uint32, ctypes.c_int32)),
        ('zclose_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('zerror_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))),
        ('opaque', ctypes.POINTER(None)),
    ]
    
    struct__CERT_SIMPLE_CHAIN._pack_ = 1 # source:False
    struct__CERT_SIMPLE_CHAIN._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('TrustStatus', struct__CERT_TRUST_STATUS),
        ('cElement', ctypes.c_uint32),
        ('rgpElement', ctypes.POINTER(ctypes.POINTER(struct__CERT_CHAIN_ELEMENT))),
        ('pTrustListInfo', ctypes.POINTER(struct__CERT_TRUST_LIST_INFO)),
        ('fHasRevocationFreshnessTime', ctypes.c_int32),
        ('dwRevocationFreshnessTime', ctypes.c_uint32),
    ]
    
    class struct_codepoint_stream_t(Structure):
        pass
    
    class struct_octet_stream_t(Structure):
        pass
    
    struct_codepoint_stream_t._pack_ = 1 # source:False
    struct_codepoint_stream_t._fields_ = [
        ('octets', ctypes.POINTER(struct_octet_stream_t)),
        ('encoding', ctypes.c_char_p),
        ('octets_consumed', ctypes.c_uint64),
        ('mf', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('validate_byte', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_ubyte)),
        ('is_utf8', ctypes.c_char),
        ('is_utf16', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 6),
    ]
    
    class struct_mem_octet_stream_t(Structure):
        pass
    
    struct_mem_octet_stream_t._pack_ = 1 # source:False
    struct_mem_octet_stream_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('buf', ctypes.POINTER(ctypes.c_ubyte)),
        ('len', ctypes.c_uint64),
        ('idx', ctypes.c_uint64),
    ]
    
    class struct_qvector_bytevec_t_(Structure):
        pass
    
    struct_qvector_bytevec_t_._pack_ = 1 # source:False
    struct_qvector_bytevec_t_._fields_ = [
        ('array', ctypes.POINTER(struct_bytevec_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_static_tree_desc_s(Structure):
        pass
    
    class struct_ct_data_s(Structure):
        pass
    
    struct_static_tree_desc_s._pack_ = 1 # source:False
    struct_static_tree_desc_s._fields_ = [
        ('static_tree', ctypes.POINTER(struct_ct_data_s)),
        ('extra_bits', ctypes.POINTER(ctypes.c_int32)),
        ('extra_base', ctypes.c_int32),
        ('elems', ctypes.c_int32),
        ('max_length', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_IP_ADDRESS_STRING(Structure):
        pass
    
    struct_IP_ADDRESS_STRING._pack_ = 1 # source:False
    struct_IP_ADDRESS_STRING._fields_ = [
        ('String', ctypes.c_char * 16),
    ]
    
    class struct__CERT_USAGE_MATCH(Structure):
        pass
    
    struct__CTL_USAGE._pack_ = 1 # source:False
    struct__CTL_USAGE._fields_ = [
        ('cUsageIdentifier', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rgpszUsageIdentifier', ctypes.POINTER(ctypes.c_char_p)),
    ]
    
    struct__CERT_USAGE_MATCH._pack_ = 1 # source:False
    struct__CERT_USAGE_MATCH._fields_ = [
        ('dwType', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('Usage', struct__CTL_USAGE),
    ]
    
    class struct__TypeDescriptor(Structure):
        pass
    
    class struct__PMD(Structure):
        pass
    
    struct__PMD._pack_ = 1 # source:False
    struct__PMD._fields_ = [
        ('mdisp', ctypes.c_int32),
        ('pdisp', ctypes.c_int32),
        ('vdisp', ctypes.c_int32),
    ]
    
    struct__s__CatchableType._pack_ = 1 # source:True
    struct__s__CatchableType._fields_ = [
        ('properties', ctypes.c_uint32),
        ('pType', ctypes.POINTER(struct__TypeDescriptor)),
        ('thisDisplacement', struct__PMD),
        ('sizeOrOffset', ctypes.c_int32),
        ('copyFunction', ctypes.CFUNCTYPE(None, ctypes.POINTER(None))),
    ]
    
    class struct_base_dispatcher_t(Structure):
        pass
    
    struct_base_dispatcher_t._pack_ = 1 # source:False
    struct_base_dispatcher_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_base_dispatcher_t_vtbl)),
        ('ipv4_address', struct__qstring_char_),
        ('certchain', struct__qstring_char_),
        ('privkey', struct__qstring_char_),
        ('irs', ctypes.POINTER(struct_idarpc_stream_t)),
        ('clients_list', ctypes.POINTER(struct_client_handlers_list_t)),
        ('port_number', ctypes.c_uint16),
        ('use_tls', ctypes.c_char),
        ('verbose', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_ea_range_sorter_t(Structure):
        pass
    
    class struct_netnode__mapper_t(Structure):
        pass
    
    
    # values for enumeration 'netnode__mapper_t__replace_policy_t'
    netnode__mapper_t__replace_policy_t__enumvalues = {
        0: 'RPL_ALL',
        1: 'RPL_NONE',
        2: 'RPL_CHECK',
    }
    RPL_ALL = 0
    RPL_NONE = 1
    RPL_CHECK = 2
    netnode__mapper_t__replace_policy_t = ctypes.c_uint32 # enum
    struct_netnode__mapper_t._pack_ = 1 # source:False
    struct_netnode__mapper_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_netnode__mapper_t_vtbl)),
        ('dest_dbctx', ctypes.POINTER(struct_dbctx_t)),
        ('blobs', ctypes.POINTER(struct_netnode__mapper_t__blobdesc_t)),
        ('replace_policy', netnode__mapper_t__replace_policy_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_range_ea_sorter_t(Structure):
        pass
    
    class struct_rpc_engine_t_vtbl(Structure):
        pass
    
    struct_rpc_packet_data_t._pack_ = 1 # source:False
    struct_rpc_packet_data_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_rpc_packet_data_t_vtbl)),
        ('code', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_schannel_buffer_t(Structure):
        pass
    
    class struct__SecBufferDesc(Structure):
        pass
    
    struct__SecBufferDesc._pack_ = 1 # source:False
    struct__SecBufferDesc._fields_ = [
        ('ulVersion', ctypes.c_uint32),
        ('cBuffers', ctypes.c_uint32),
        ('pBuffers', ctypes.POINTER(struct__SecBuffer)),
    ]
    
    class struct_qvector_bool_(Structure):
        pass
    
    struct_qvector_bool_._pack_ = 1 # source:False
    struct_qvector_bool_._fields_ = [
        ('array', ctypes.c_char_p),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_schannel_buffer_t._pack_ = 1 # source:False
    struct_schannel_buffer_t._fields_ = [
        ('allocated_by_system', struct_qvector_bool_),
        ('buffers', struct_qvector__SecBuffer_),
        ('pbuffers', struct_qvector__SecBuffer__P_),
        ('desc', struct__SecBufferDesc),
    ]
    
    class struct_tls_stream_t_vtbl(Structure):
        pass
    
    class struct_unz_file_info64_s(Structure):
        pass
    
    class struct_tm_unz_s(Structure):
        pass
    
    struct_tm_unz_s._pack_ = 1 # source:False
    struct_tm_unz_s._fields_ = [
        ('tm_sec', ctypes.c_uint32),
        ('tm_min', ctypes.c_uint32),
        ('tm_hour', ctypes.c_uint32),
        ('tm_mday', ctypes.c_uint32),
        ('tm_mon', ctypes.c_uint32),
        ('tm_year', ctypes.c_uint32),
    ]
    
    struct_unz_file_info64_s._pack_ = 1 # source:False
    struct_unz_file_info64_s._fields_ = [
        ('version', ctypes.c_uint32),
        ('version_needed', ctypes.c_uint32),
        ('flag', ctypes.c_uint32),
        ('compression_method', ctypes.c_uint32),
        ('dosDate', ctypes.c_uint32),
        ('crc', ctypes.c_uint32),
        ('compressed_size', ctypes.c_uint64),
        ('uncompressed_size', ctypes.c_uint64),
        ('size_filename', ctypes.c_uint32),
        ('size_file_extra', ctypes.c_uint32),
        ('size_file_comment', ctypes.c_uint32),
        ('disk_num_start', ctypes.c_uint32),
        ('internal_fa', ctypes.c_uint32),
        ('external_fa', ctypes.c_uint32),
        ('tmu_date', struct_tm_unz_s),
    ]
    
    class struct_unz_global_info_s(Structure):
        pass
    
    struct_unz_global_info_s._pack_ = 1 # source:False
    struct_unz_global_info_s._fields_ = [
        ('number_entry', ctypes.c_uint32),
        ('size_comment', ctypes.c_uint32),
    ]
    
    class struct_RUNTIME_FUNCTION(Structure):
        pass
    
    struct_RUNTIME_FUNCTION._pack_ = 1 # source:False
    struct_RUNTIME_FUNCTION._fields_ = [
        ('FunctionStart', ctypes.POINTER(None)),
        ('FunctionEnd', ctypes.POINTER(None)),
        ('UnwindInfo', ctypes.POINTER(None)),
    ]
    
    class struct_WSPIAPI_FUNCTION(Structure):
        pass
    
    struct_WSPIAPI_FUNCTION._pack_ = 1 # source:False
    struct_WSPIAPI_FUNCTION._fields_ = [
        ('pszName', ctypes.c_char_p),
        ('pfAddress', ctypes.CFUNCTYPE(ctypes.c_int64)),
    ]
    
    class struct__CERT_CHAIN_PARA(Structure):
        pass
    
    struct__CERT_CHAIN_PARA._pack_ = 1 # source:False
    struct__CERT_CHAIN_PARA._fields_ = [
        ('cbSize', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('RequestedUsage', struct__CERT_USAGE_MATCH),
    ]
    
    class struct__CRYPT_ATTRIBUTE(Structure):
        pass
    
    struct__CRYPT_ATTRIBUTE._pack_ = 1 # source:False
    struct__CRYPT_ATTRIBUTE._fields_ = [
        ('pszObjId', ctypes.c_char_p),
        ('cValue', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rgValue', ctypes.POINTER(struct__CRYPTOAPI_BLOB)),
    ]
    
    class struct__IP_ADAPTER_INFO(Structure):
        pass
    
    class struct__IP_ADDR_STRING(Structure):
        pass
    
    struct__IP_ADDR_STRING._pack_ = 1 # source:False
    struct__IP_ADDR_STRING._fields_ = [
        ('Next', ctypes.POINTER(struct__IP_ADDR_STRING)),
        ('IpAddress', struct_IP_ADDRESS_STRING),
        ('IpMask', struct_IP_ADDRESS_STRING),
        ('Context', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct__IP_ADAPTER_INFO._pack_ = 1 # source:False
    struct__IP_ADAPTER_INFO._fields_ = [
        ('Next', ctypes.POINTER(struct__IP_ADAPTER_INFO)),
        ('ComboIndex', ctypes.c_uint32),
        ('AdapterName', ctypes.c_char * 260),
        ('Description', ctypes.c_char * 132),
        ('AddressLength', ctypes.c_uint32),
        ('Address', ctypes.c_ubyte * 8),
        ('Index', ctypes.c_uint32),
        ('Type', ctypes.c_uint32),
        ('DhcpEnabled', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('CurrentIpAddress', ctypes.POINTER(struct__IP_ADDR_STRING)),
        ('IpAddressList', struct__IP_ADDR_STRING),
        ('GatewayList', struct__IP_ADDR_STRING),
        ('DhcpServer', struct__IP_ADDR_STRING),
        ('HaveWins', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('PrimaryWinsServer', struct__IP_ADDR_STRING),
        ('SecondaryWinsServer', struct__IP_ADDR_STRING),
        ('LeaseObtained', ctypes.c_int64),
        ('LeaseExpires', ctypes.c_int64),
    ]
    
    struct_cancellable_op_t._pack_ = 1 # source:False
    struct_cancellable_op_t._fields_ = [
        ('goal', ctypes.c_uint64),
        ('processed', ctypes.c_uint64),
        ('next_check', ctypes.c_uint64),
        ('receiving', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_device_chooser_t(Structure):
        pass
    
    struct_device_chooser_t._pack_ = 1 # source:False
    struct_device_chooser_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 184),
        ('names', struct_qvector__qstring_char___),
        ('defdev', struct__qstring_char_),
        ('params', struct_qvector__qstring_char___),
        ('has_params', ctypes.c_char),
        ('have_skipped', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 6),
    ]
    
    class struct_generic_client_t(Structure):
        pass
    
    struct_generic_client_t._pack_ = 1 # source:False
    struct_generic_client_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_generic_client_t_vtbl)),
        ('create_rpc_engine', ctypes.CFUNCTYPE(ctypes.POINTER(struct_recording_rpc_engine_t), ctypes.POINTER(struct_idarpc_stream_t))),
        ('rpc_engine', ctypes.POINTER(struct_recording_rpc_engine_t)),
        ('wait_dialog_contents', struct__qstring_char_),
        ('server_name', ctypes.c_char_p),
        ('protocol_version', ctypes.c_int32),
        ('started_receiving_response', ctypes.c_char),
        ('was_user_cancelled', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 2),
    ]
    
    class struct_inflate_linput_t(Structure):
        pass
    
    
    # values for enumeration 'linput_close_code_t'
    linput_close_code_t__enumvalues = {
        0: 'LOC_CLOSE',
        1: 'LOC_UNMAKE',
        2: 'LOC_KEEP',
    }
    LOC_CLOSE = 0
    LOC_UNMAKE = 1
    LOC_KEEP = 2
    linput_close_code_t = ctypes.c_uint32 # enum
    struct_inflate_linput_t._pack_ = 1 # source:False
    struct_inflate_linput_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('zinput', ctypes.POINTER(struct_linput_t)),
        ('cur_offset', ctypes.c_int64),
        ('zfirst_time', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 7),
        ('csize', ctypes.c_int64),
        ('loc', linput_close_code_t),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('zstream', struct_z_stream_s),
        ('zinbuf', ctypes.c_ubyte * 32768),
    ]
    
    class struct_metablock_info_t(Structure):
        pass
    
    struct_metablock_info_t._pack_ = 1 # source:True
    struct_metablock_info_t._fields_ = [
        ('mblk', ctypes.c_uint16),
        ('subculture', ctypes.c_ubyte),
        ('basic', ctypes.c_ubyte),
        ('shared', ctypes.c_ubyte),
    ]
    
    class struct_qvector_char__P_(Structure):
        pass
    
    struct_qvector_char__P_._pack_ = 1 # source:False
    struct_qvector_char__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_char_p)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_range_visitor2_t(Structure):
        pass
    
    struct_range_visitor2_t._pack_ = 1 # source:False
    struct_range_visitor2_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_range_visitor2_t_vtbl)),
    ]
    
    class struct_unz64_file_pos_s(Structure):
        pass
    
    struct_unz64_file_pos_s._pack_ = 1 # source:False
    struct_unz64_file_pos_s._fields_ = [
        ('pos_in_zip_directory', ctypes.c_uint64),
        ('num_of_file', ctypes.c_uint64),
    ]
    
    class struct_UNWIND_INFO_HDR(Structure):
        pass
    
    struct_UNWIND_INFO_HDR._pack_ = 1 # source:False
    struct_UNWIND_INFO_HDR._fields_ = [
        ('Ver3_Flags', ctypes.c_char),
        ('PrologSize', ctypes.c_char),
        ('CntUnwindCodes', ctypes.c_char),
        ('FrReg_FrRegOff', ctypes.c_char),
    ]
    
    class struct__CERT_EXTENSION(Structure):
        pass
    
    struct__CERT_EXTENSION._pack_ = 1 # source:False
    struct__CERT_EXTENSION._fields_ = [
        ('pszObjId', ctypes.c_char_p),
        ('fCritical', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('Value', struct__CRYPTOAPI_BLOB),
    ]
    
    struct__TypeDescriptor._pack_ = 1 # source:False
    struct__TypeDescriptor._fields_ = [
        ('pVFTable', ctypes.POINTER(None)),
        ('spare', ctypes.POINTER(None)),
        ('name', ctypes.c_char * 0),
    ]
    
    class struct_debugger_init_t(Structure):
        pass
    
    struct_event_handler_t._pack_ = 1 # source:False
    struct_event_handler_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_event_handler_t_vtbl)),
        ('sources', struct_qvector_event_source_t__P_),
    ]
    
    struct_idarpc_stream_t._pack_ = 1 # source:False
    struct_idarpc_stream_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_idarpc_stream_t_vtbl)),
        ('progress_cb_info', struct_idarpc_stream_t__progress_cb_info_t),
    ]
    
    class struct_unz_file_info_s(Structure):
        pass
    
    struct_unz_file_info_s._pack_ = 1 # source:False
    struct_unz_file_info_s._fields_ = [
        ('version', ctypes.c_uint32),
        ('version_needed', ctypes.c_uint32),
        ('flag', ctypes.c_uint32),
        ('compression_method', ctypes.c_uint32),
        ('dosDate', ctypes.c_uint32),
        ('crc', ctypes.c_uint32),
        ('compressed_size', ctypes.c_uint32),
        ('uncompressed_size', ctypes.c_uint32),
        ('size_filename', ctypes.c_uint32),
        ('size_file_extra', ctypes.c_uint32),
        ('size_file_comment', ctypes.c_uint32),
        ('disk_num_start', ctypes.c_uint32),
        ('internal_fa', ctypes.c_uint32),
        ('external_fa', ctypes.c_uint32),
        ('tmu_date', struct_tm_unz_s),
    ]
    
    struct_event_source_t._pack_ = 1 # source:False
    struct_event_source_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_event_source_t_vtbl)),
        ('handlers', struct_qvector_event_handler_t__P_),
    ]
    
    class struct_handler_data_t(Structure):
        pass
    
    class struct___qsemaphore_t(Structure):
        pass
    
    struct_handler_data_t._pack_ = 1 # source:False
    struct_handler_data_t._fields_ = [
        ('dispatcher', ctypes.POINTER(struct_base_dispatcher_t)),
        ('handler', ctypes.POINTER(struct_network_client_handler_t)),
        ('sem', ctypes.POINTER(struct___qsemaphore_t)),
    ]
    
    class struct_hot_encoding_t(Structure):
        pass
    
    struct_hot_encoding_t._pack_ = 1 # source:False
    struct_hot_encoding_t._fields_ = [
        ('cp', ctypes.c_int32),
        ('ticks', ctypes.c_uint32),
        ('iconv_name', ctypes.c_char * 28),
        ('req_name', ctypes.c_char * 28),
    ]
    
    class struct_ida_tls_data_t(Structure):
        pass
    
    struct_ida_tls_data_t._pack_ = 1 # source:False
    struct_ida_tls_data_t._fields_ = [
        ('thr_errval', ctypes.c_uint64 * 4),
        ('thr_errstr', struct_qstring_simple_init_t * 4),
        ('getsys_buf', struct_qstring_simple_init_t),
        ('winerr_buf', struct_qstring_simple_init_t),
        ('strerr_buf', struct_qstring_simple_init_t),
        ('errdesc_buf', struct_qstring_simple_init_t),
        ('qstrerror_buf', struct_qstring_simple_init_t),
        ('thr_qerrno', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_internal_state(Structure):
        pass
    
    struct_internal_state._pack_ = 1 # source:False
    struct_internal_state._fields_ = [
        ('dummy', ctypes.c_int32),
    ]
    
    class struct_last_cp_data_t(Structure):
        pass
    
    struct_last_cp_data_t._pack_ = 1 # source:False
    struct_last_cp_data_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('cp', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_octet_stream_t._pack_ = 1 # source:False
    struct_octet_stream_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_octet_stream_t_vtbl)),
        ('consumed', ctypes.c_uint64),
    ]
    
    class struct_qwstringi_less(Structure):
        pass
    
    class struct_ranges_cache_t(Structure):
        pass
    
    struct_ranges_cache_t._pack_ = 1 # source:False
    struct_ranges_cache_t._fields_ = [
        ('ranges', struct_qvector_range_cache_t_),
        ('plast', ctypes.POINTER(struct_range_cache_t)),
        ('infosize', ctypes.c_uint32),
        ('loaded', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('pending_delete', struct_qstack_unsigned___int64_),
        ('undo_agent', struct_rangecb_undo_record_t),
    ]
    
    class struct_tcpip_stream_t(Structure):
        pass
    
    struct_tcpip_stream_t._pack_ = 1 # source:False
    struct_tcpip_stream_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 32),
        ('cancellable_ops', struct_qstack_cancellable_op_t_),
        ('sock', ctypes.c_uint64),
        ('errbuf', struct__qstring_char_),
        ('errfunc', ctypes.c_char_p),
        ('errcode', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    struct_text_options_t._pack_ = 1 # source:False
    struct_text_options_t._fields_ = [
        ('text', struct_dual_text_options_t),
        ('graph', struct_dual_text_options_t),
    ]
    
    class struct_unz_file_pos_s(Structure):
        pass
    
    struct_unz_file_pos_s._pack_ = 1 # source:False
    struct_unz_file_pos_s._fields_ = [
        ('pos_in_zip_directory', ctypes.c_uint32),
        ('num_of_file', ctypes.c_uint32),
    ]
    
    class struct_win32_thread_t(Structure):
        pass
    
    struct_win32_thread_t._pack_ = 1 # source:False
    struct_win32_thread_t._fields_ = [
        ('h', ctypes.POINTER(None)),
        ('id', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_C_SCOPE_TABLE(Structure):
        pass
    
    struct_C_SCOPE_TABLE._pack_ = 1 # source:False
    struct_C_SCOPE_TABLE._fields_ = [
        ('Begin', ctypes.POINTER(None)),
        ('End', ctypes.POINTER(None)),
        ('Handler', ctypes.POINTER(None)),
        ('Target', ctypes.POINTER(None)),
    ]
    
    class struct__CERT_INFO(Structure):
        pass
    
    struct__CERT_CONTEXT._pack_ = 1 # source:False
    struct__CERT_CONTEXT._fields_ = [
        ('dwCertEncodingType', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pbCertEncoded', ctypes.POINTER(ctypes.c_ubyte)),
        ('cbCertEncoded', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('pCertInfo', ctypes.POINTER(struct__CERT_INFO)),
        ('hCertStore', ctypes.POINTER(None)),
    ]
    
    class struct__STARTUPINFOW(Structure):
        pass
    
    struct__STARTUPINFOW._pack_ = 1 # source:False
    struct__STARTUPINFOW._fields_ = [
        ('cb', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('lpReserved', ctypes.POINTER(ctypes.c_wchar)),
        ('lpDesktop', ctypes.POINTER(ctypes.c_wchar)),
        ('lpTitle', ctypes.POINTER(ctypes.c_wchar)),
        ('dwX', ctypes.c_uint32),
        ('dwY', ctypes.c_uint32),
        ('dwXSize', ctypes.c_uint32),
        ('dwYSize', ctypes.c_uint32),
        ('dwXCountChars', ctypes.c_uint32),
        ('dwYCountChars', ctypes.c_uint32),
        ('dwFillAttribute', ctypes.c_uint32),
        ('dwFlags', ctypes.c_uint32),
        ('wShowWindow', ctypes.c_uint16),
        ('cbReserved2', ctypes.c_uint16),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('lpReserved2', ctypes.POINTER(ctypes.c_ubyte)),
        ('hStdInput', ctypes.POINTER(None)),
        ('hStdOutput', ctypes.POINTER(None)),
        ('hStdError', ctypes.POINTER(None)),
    ]
    
    class struct_hit_counter_t(Structure):
        pass
    
    class struct_incrementer_t(Structure):
        pass
    
    class struct_inflate_state(Structure):
        pass
    
    class struct_code(Structure):
        pass
    
    class struct_gz_header_s(Structure):
        pass
    
    struct_code._pack_ = 1 # source:False
    struct_code._fields_ = [
        ('op', ctypes.c_ubyte),
        ('bits', ctypes.c_ubyte),
        ('val', ctypes.c_uint16),
    ]
    
    
    # values for enumeration 'inflate_mode'
    inflate_mode__enumvalues = {
        0: 'HEAD',
        1: 'FLAGS',
        2: 'TIME',
        3: 'OS',
        4: 'EXLEN',
        5: 'EXTRA',
        6: 'NAME',
        7: 'COMMENT',
        8: 'HCRC',
        9: 'DICTID',
        10: 'DICT',
        11: 'TYPE',
        12: 'TYPEDO',
        13: 'STORED',
        14: 'COPY_',
        15: 'COPY',
        16: 'TABLE',
        17: 'LENLENS',
        18: 'CODELENS',
        19: 'LEN_',
        20: 'LEN',
        21: 'LENEXT',
        22: 'DIST',
        23: 'DISTEXT',
        24: 'MATCH',
        25: 'LIT',
        26: 'CHECK',
        27: 'LENGTH',
        28: 'DONE',
        29: 'BAD',
        30: 'MEM',
        31: 'SYNC',
    }
    HEAD = 0
    FLAGS = 1
    TIME = 2
    OS = 3
    EXLEN = 4
    EXTRA = 5
    NAME = 6
    COMMENT = 7
    HCRC = 8
    DICTID = 9
    DICT = 10
    TYPE = 11
    TYPEDO = 12
    STORED = 13
    COPY_ = 14
    COPY = 15
    TABLE = 16
    LENLENS = 17
    CODELENS = 18
    LEN_ = 19
    LEN = 20
    LENEXT = 21
    DIST = 22
    DISTEXT = 23
    MATCH = 24
    LIT = 25
    CHECK = 26
    LENGTH = 27
    DONE = 28
    BAD = 29
    MEM = 30
    SYNC = 31
    inflate_mode = ctypes.c_uint32 # enum
    struct_inflate_state._pack_ = 1 # source:False
    struct_inflate_state._fields_ = [
        ('mode', inflate_mode),
        ('last', ctypes.c_int32),
        ('wrap', ctypes.c_int32),
        ('havedict', ctypes.c_int32),
        ('flags', ctypes.c_int32),
        ('dmax', ctypes.c_uint32),
        ('check', ctypes.c_uint32),
        ('total', ctypes.c_uint32),
        ('head', ctypes.POINTER(struct_gz_header_s)),
        ('wbits', ctypes.c_uint32),
        ('wsize', ctypes.c_uint32),
        ('whave', ctypes.c_uint32),
        ('wnext', ctypes.c_uint32),
        ('window', ctypes.POINTER(ctypes.c_ubyte)),
        ('hold', ctypes.c_uint32),
        ('bits', ctypes.c_uint32),
        ('length', ctypes.c_uint32),
        ('offset', ctypes.c_uint32),
        ('extra', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('lencode', ctypes.POINTER(struct_code)),
        ('distcode', ctypes.POINTER(struct_code)),
        ('lenbits', ctypes.c_uint32),
        ('distbits', ctypes.c_uint32),
        ('ncode', ctypes.c_uint32),
        ('nlen', ctypes.c_uint32),
        ('ndist', ctypes.c_uint32),
        ('have', ctypes.c_uint32),
        ('next', ctypes.POINTER(struct_code)),
        ('lens', ctypes.c_uint16 * 320),
        ('work', ctypes.c_uint16 * 288),
        ('codes', struct_code * 1444),
        ('sane', ctypes.c_int32),
        ('back', ctypes.c_int32),
        ('was', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_iso2022_esc_t(Structure):
        pass
    
    struct_iso2022_esc_t._pack_ = 1 # source:False
    struct_iso2022_esc_t._fields_ = [
        ('esc', ctypes.c_char_p),
        ('esc_len', ctypes.c_int32),
        ('len', ctypes.c_int32),
        ('cs', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_main_locker_t(Structure):
        pass
    
    struct_main_locker_t._pack_ = 1 # source:False
    struct_main_locker_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_range_cache_t._pack_ = 1 # source:False
    struct_range_cache_t._fields_ = [
        ('range', ctypes.POINTER(struct_range_t)),
        ('locks', ctypes.c_int32),
        ('dirty', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
    ]
    
    class struct_undo_record_t(Structure):
        pass
    
    struct_undo_record_t._pack_ = 1 # source:False
    struct_undo_record_t._fields_ = [
        ('code', undo_code_t),
        ('size', ctypes.c_uint32),
        ('obj', ctypes.POINTER(ctypes.c_ubyte)),
    ]
    
    class struct__CRL_INFO(Structure):
        pass
    
    struct__CRL_CONTEXT._pack_ = 1 # source:False
    struct__CRL_CONTEXT._fields_ = [
        ('dwCertEncodingType', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pbCrlEncoded', ctypes.POINTER(ctypes.c_ubyte)),
        ('cbCrlEncoded', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('pCrlInfo', ctypes.POINTER(struct__CRL_INFO)),
        ('hCertStore', ctypes.POINTER(None)),
    ]
    
    class struct__CTL_INFO(Structure):
        pass
    
    struct__CTL_CONTEXT._pack_ = 1 # source:False
    struct__CTL_CONTEXT._fields_ = [
        ('dwMsgAndCertEncodingType', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('pbCtlEncoded', ctypes.POINTER(ctypes.c_ubyte)),
        ('cbCtlEncoded', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('pCtlInfo', ctypes.POINTER(struct__CTL_INFO)),
        ('hCertStore', ctypes.POINTER(None)),
        ('hCryptMsg', ctypes.POINTER(None)),
        ('pbCtlContent', ctypes.POINTER(ctypes.c_ubyte)),
        ('cbCtlContent', ctypes.c_uint32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class struct__s_ThrowInfo(Structure):
        pass
    
    struct__s_ThrowInfo._pack_ = 1 # source:False
    struct__s_ThrowInfo._fields_ = [
        ('attributes', ctypes.c_uint32),
        ('pmfnUnwind', ctypes.c_int32),
        ('pForwardCompat', ctypes.c_int32),
        ('pCatchableTypeArray', ctypes.c_int32),
    ]
    
    class struct_key_locker_t(Structure):
        pass
    
    class struct_HKEY__(Structure):
        pass
    
    struct_key_locker_t._pack_ = 1 # source:False
    struct_key_locker_t._fields_ = [
        ('hkey', ctypes.POINTER(struct_HKEY__)),
        ('is_new', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_range_info_t(Structure):
        pass
    
    
    # values for enumeration 'range_type_t'
    range_type_t__enumvalues = {
        0: 'rt_one_to_one',
        1: 'rt_coalesced',
    }
    rt_one_to_one = 0
    rt_coalesced = 1
    range_type_t = ctypes.c_uint32 # enum
    struct_range_info_t._pack_ = 1 # source:False
    struct_range_info_t._fields_ = [
        ('cp', ctypes.c_uint32),
        ('index_in_raw', ctypes.c_uint32),
        ('type', range_type_t),
    ]
    
    class struct_rpc_engine_t(Structure):
        pass
    
    struct_rpc_engine_t._pack_ = 1 # source:False
    struct_rpc_engine_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_rpc_engine_t_vtbl)),
        ('network_error', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('ioctl_handler', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_rpc_engine_t), ctypes.c_int32, ctypes.POINTER(None), ctypes.c_uint64, ctypes.POINTER(ctypes.POINTER(None)), ctypes.POINTER(ctypes.c_int64))),
        ('recv_timeout', ctypes.c_int32),
        ('is_client', ctypes.c_char),
        ('logged_in', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 2),
        ('ptypes', struct_qvector_rpc_packet_type_desc_t_),
    ]
    
    class struct_rpc_packet_t(Structure):
        pass
    
    struct_rpc_packet_t._pack_ = 1 # source:True
    struct_rpc_packet_t._fields_ = [
        ('length', ctypes.c_uint32),
        ('code', ctypes.c_ubyte),
    ]
    
    class struct_tls_stream_t(Structure):
        pass
    
    class struct__SecHandle(Structure):
        pass
    
    struct__SecHandle._pack_ = 1 # source:False
    struct__SecHandle._fields_ = [
        ('dwLower', ctypes.c_uint64),
        ('dwUpper', ctypes.c_uint64),
    ]
    
    struct_tls_stream_t._pack_ = 1 # source:False
    struct_tls_stream_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 32),
        ('irs', ctypes.POINTER(struct_idarpc_stream_t)),
        ('errbuf', struct__qstring_char_),
        ('errfunc', ctypes.c_char_p),
        ('errcode', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('self_signed_certificates', struct_qvector_bytevec_t_),
        ('root_ca_certificate', struct_bytevec_t),
        ('cred_handle', struct__SecHandle),
        ('security_ctx', struct__SecHandle),
        ('missing_bytes', ctypes.c_uint64),
        ('_recv_buf', struct_bytevec_t),
        ('_decrypted', struct_bytevec_t),
        ('request_flags', ctypes.c_uint32),
        ('ctx_attributes', ctypes.c_uint32),
        ('stream_sizes', struct__SecPkgContext_StreamSizes),
        ('ctx_initialized', ctypes.c_char),
        ('PADDING_2', ctypes.c_ubyte * 3),
    ]
    
    class struct_unz_closer_t(Structure):
        pass
    
    struct_unz_closer_t._pack_ = 1 # source:False
    struct_unz_closer_t._fields_ = [
        ('uf', ctypes.POINTER(ctypes.POINTER(None))),
    ]
    
    class struct_HINSTANCE__(Structure):
        pass
    
    struct_HINSTANCE__._pack_ = 1 # source:False
    struct_HINSTANCE__._fields_ = [
        ('unused', ctypes.c_int32),
    ]
    
    class struct_UNWIND_CODE(Structure):
        pass
    
    struct_UNWIND_CODE._pack_ = 1 # source:False
    struct_UNWIND_CODE._fields_ = [
        ('PrologOff', ctypes.c_char),
        ('OpCode_OpInfo', ctypes.c_char),
    ]
    
    class struct__OVERLAPPED(Structure):
        pass
    
    class union__98217BFA50FEF0A74464688915FC94A9(Union):
        pass
    
    union__98217BFA50FEF0A74464688915FC94A9._pack_ = 1 # source:False
    union__98217BFA50FEF0A74464688915FC94A9._fields_ = [
        ('__s0', struct__77D3A2E2503DF0742434FD6F35F3BB5C),
        ('Pointer', ctypes.POINTER(None)),
    ]
    
    struct__OVERLAPPED._pack_ = 1 # source:False
    struct__OVERLAPPED._fields_ = [
        ('Internal', ctypes.c_uint64),
        ('InternalHigh', ctypes.c_uint64),
        ('___u2', union__98217BFA50FEF0A74464688915FC94A9),
        ('hEvent', ctypes.POINTER(None)),
    ]
    
    struct_gz_header_s._pack_ = 1 # source:False
    struct_gz_header_s._fields_ = [
        ('text', ctypes.c_int32),
        ('time', ctypes.c_uint32),
        ('xflags', ctypes.c_int32),
        ('os', ctypes.c_int32),
        ('extra', ctypes.POINTER(ctypes.c_ubyte)),
        ('extra_len', ctypes.c_uint32),
        ('extra_max', ctypes.c_uint32),
        ('name', ctypes.POINTER(ctypes.c_ubyte)),
        ('name_max', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('comment', ctypes.POINTER(ctypes.c_ubyte)),
        ('comm_max', ctypes.c_uint32),
        ('hcrc', ctypes.c_int32),
        ('done', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_iconv_cache(Structure):
        pass
    
    struct_iconv_cache._pack_ = 1 # source:False
    struct_iconv_cache._fields_ = [
        ('fromcode', struct__qstring_char_),
        ('tocode', struct__qstring_char_),
        ('cd', ctypes.POINTER(None)),
    ]
    
    class struct_rec_iconv_t(Structure):
        pass
    
    class struct_csconv_t(Structure):
        pass
    
    class struct_compat_t(Structure):
        pass
    
    struct_csconv_t._pack_ = 1 # source:False
    struct_csconv_t._fields_ = [
        ('codepage', ctypes.c_int32),
        ('flags', ctypes.c_int32),
        ('mbtowc', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_csconv_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32, ctypes.POINTER(ctypes.c_uint16), ctypes.POINTER(ctypes.c_int32))),
        ('wctomb', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_csconv_t), ctypes.POINTER(ctypes.c_uint16), ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)),
        ('mblen', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_csconv_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)),
        ('flush', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_csconv_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)),
        ('mode', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('compat', ctypes.POINTER(struct_compat_t)),
    ]
    
    struct_rec_iconv_t._pack_ = 1 # source:False
    struct_rec_iconv_t._fields_ = [
        ('cd', ctypes.POINTER(None)),
        ('iconv_close', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None))),
        ('iconv', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint64))),
        ('_errno', ctypes.CFUNCTYPE(ctypes.POINTER(ctypes.c_int32))),
        ('from', struct_csconv_t),
        ('to', struct_csconv_t),
    ]
    
    class struct_sockaddr_in(Structure):
        pass
    
    class struct_in_addr(Structure):
        pass
    
    class union_in_addr___unnamed_type_S_un_(Union):
        pass
    
    union_in_addr___unnamed_type_S_un_._pack_ = 1 # source:False
    union_in_addr___unnamed_type_S_un_._fields_ = [
        ('S_un_b', struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_b_),
        ('S_un_w', struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_w_),
        ('S_addr', ctypes.c_uint32),
    ]
    
    struct_in_addr._pack_ = 1 # source:False
    struct_in_addr._fields_ = [
        ('S_un', union_in_addr___unnamed_type_S_un_),
    ]
    
    struct_sockaddr_in._pack_ = 1 # source:False
    struct_sockaddr_in._fields_ = [
        ('sin_family', ctypes.c_uint16),
        ('sin_port', ctypes.c_uint16),
        ('sin_addr', struct_in_addr),
        ('sin_zero', ctypes.c_char * 8),
    ]
    
    class struct_tree_desc_s(Structure):
        pass
    
    struct_tree_desc_s._pack_ = 1 # source:False
    struct_tree_desc_s._fields_ = [
        ('dyn_tree', ctypes.POINTER(struct_ct_data_s)),
        ('max_code', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('stat_desc', ctypes.POINTER(None)),
    ]
    
    class struct_validator_t(Structure):
        pass
    
    struct_validator_t._pack_ = 1 # source:False
    struct_validator_t._fields_ = [
        ('val', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_ubyte)),
        ('cp', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct__FILETIME(Structure):
        pass
    
    struct__FILETIME._pack_ = 1 # source:False
    struct__FILETIME._fields_ = [
        ('dwLowDateTime', ctypes.c_uint32),
        ('dwHighDateTime', ctypes.c_uint32),
    ]
    
    struct__CERT_INFO._pack_ = 1 # source:False
    struct__CERT_INFO._fields_ = [
        ('dwVersion', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('SerialNumber', struct__CRYPTOAPI_BLOB),
        ('SignatureAlgorithm', struct__CRYPT_ALGORITHM_IDENTIFIER),
        ('Issuer', struct__CRYPTOAPI_BLOB),
        ('NotBefore', struct__FILETIME),
        ('NotAfter', struct__FILETIME),
        ('Subject', struct__CRYPTOAPI_BLOB),
        ('SubjectPublicKeyInfo', struct__CERT_PUBLIC_KEY_INFO),
        ('IssuerUniqueId', struct__CRYPT_BIT_BLOB),
        ('SubjectUniqueId', struct__CRYPT_BIT_BLOB),
        ('cExtension', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('rgExtension', ctypes.POINTER(struct__CERT_EXTENSION)),
    ]
    
    struct__CRL_ENTRY._pack_ = 1 # source:False
    struct__CRL_ENTRY._fields_ = [
        ('SerialNumber', struct__CRYPTOAPI_BLOB),
        ('RevocationDate', struct__FILETIME),
        ('cExtension', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rgExtension', ctypes.POINTER(struct__CERT_EXTENSION)),
    ]
    
    struct__CTL_ENTRY._pack_ = 1 # source:False
    struct__CTL_ENTRY._fields_ = [
        ('SubjectIdentifier', struct__CRYPTOAPI_BLOB),
        ('cAttribute', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rgAttribute', ctypes.POINTER(struct__CRYPT_ATTRIBUTE)),
    ]
    
    struct__SecBuffer._pack_ = 1 # source:False
    struct__SecBuffer._fields_ = [
        ('cbBuffer', ctypes.c_uint32),
        ('BufferType', ctypes.c_uint32),
        ('pvBuffer', ctypes.POINTER(None)),
    ]
    
    class struct_blkrange_t(Structure):
        pass
    
    struct_blkrange_t._pack_ = 1 # source:False
    struct_blkrange_t._fields_ = [
        ('from', ctypes.c_uint32),
        ('to', ctypes.c_uint32),
    ]
    
    class struct_enc_pair_t(Structure):
        pass
    
    struct_enc_pair_t._pack_ = 1 # source:False
    struct_enc_pair_t._fields_ = [
        ('alias', ctypes.c_char_p),
        ('proper', ctypes.c_char_p),
    ]
    
    struct_lex_vars_t._pack_ = 1 # source:False
    struct_lex_vars_t._fields_ = [
        ('idc_subdirs', struct_qvector__qstring_char___),
        ('header_subdirs', struct_qvector__qstring_char___),
    ]
    
    class struct_sha1_ctx_t(Structure):
        pass
    
    struct_sha1_ctx_t._pack_ = 1 # source:False
    struct_sha1_ctx_t._fields_ = [
        ('state', ctypes.c_uint32 * 5),
        ('count', ctypes.c_uint32 * 2),
        ('buffer', ctypes.c_ubyte * 64),
    ]
    
    class struct_sha256_ctx(Structure):
        pass
    
    struct_sha256_ctx._pack_ = 1 # source:False
    struct_sha256_ctx._fields_ = [
        ('count', ctypes.c_uint32 * 2),
        ('hash', ctypes.c_uint32 * 8),
        ('wbuf', ctypes.c_uint32 * 16),
    ]
    
    struct__CRL_INFO._pack_ = 1 # source:False
    struct__CRL_INFO._fields_ = [
        ('dwVersion', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('SignatureAlgorithm', struct__CRYPT_ALGORITHM_IDENTIFIER),
        ('Issuer', struct__CRYPTOAPI_BLOB),
        ('ThisUpdate', struct__FILETIME),
        ('NextUpdate', struct__FILETIME),
        ('cCRLEntry', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('rgCRLEntry', ctypes.POINTER(struct__CRL_ENTRY)),
        ('cExtension', ctypes.c_uint32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('rgExtension', ctypes.POINTER(struct__CERT_EXTENSION)),
    ]
    
    struct__CTL_INFO._pack_ = 1 # source:False
    struct__CTL_INFO._fields_ = [
        ('dwVersion', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('SubjectUsage', struct__CTL_USAGE),
        ('ListIdentifier', struct__CRYPTOAPI_BLOB),
        ('SequenceNumber', struct__CRYPTOAPI_BLOB),
        ('ThisUpdate', struct__FILETIME),
        ('NextUpdate', struct__FILETIME),
        ('SubjectAlgorithm', struct__CRYPT_ALGORITHM_IDENTIFIER),
        ('cCTLEntry', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('rgCTLEntry', ctypes.POINTER(struct__CTL_ENTRY)),
        ('cExtension', ctypes.c_uint32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('rgExtension', ctypes.POINTER(struct__CERT_EXTENSION)),
    ]
    
    class struct_aes_key_t(Structure):
        pass
    
    struct_aes_key_t._pack_ = 1 # source:False
    struct_aes_key_t._fields_ = [
        ('nr', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('rk', ctypes.POINTER(ctypes.c_uint32)),
        ('buf', ctypes.c_uint32 * 68),
    ]
    
    class struct_cp_data_t(Structure):
        pass
    
    struct_cp_data_t._pack_ = 1 # source:False
    struct_cp_data_t._fields_ = [
        ('block', ctypes.c_uint16),
        ('cat', ctypes.c_ubyte),
        ('trans', ctypes.c_ubyte),
    ]
    
    class union__3FED14670831426F78C1F126725788C0(Union):
        pass
    
    union__3FED14670831426F78C1F126725788C0._pack_ = 1 # source:False
    union__3FED14670831426F78C1F126725788C0._fields_ = [
        ('freq', ctypes.c_uint16),
        ('code', ctypes.c_uint16),
    ]
    
    class union__2467CA9704E0472D4CCF1296A763D23A(Union):
        pass
    
    union__2467CA9704E0472D4CCF1296A763D23A._pack_ = 1 # source:False
    union__2467CA9704E0472D4CCF1296A763D23A._fields_ = [
        ('dad', ctypes.c_uint16),
        ('len', ctypes.c_uint16),
    ]
    
    struct_ct_data_s._pack_ = 1 # source:False
    struct_ct_data_s._fields_ = [
        ('fc', union__3FED14670831426F78C1F126725788C0),
        ('dl', union__2467CA9704E0472D4CCF1296A763D23A),
    ]
    
    
    # values for enumeration 'range_kind_t'
    range_kind_t__enumvalues = {
        0: 'RANGE_KIND_UNKNOWN',
        1: 'RANGE_KIND_FUNC',
        2: 'RANGE_KIND_SEGMENT',
        3: 'RANGE_KIND_HIDDEN_RANGE',
    }
    RANGE_KIND_UNKNOWN = 0
    RANGE_KIND_FUNC = 1
    RANGE_KIND_SEGMENT = 2
    RANGE_KIND_HIDDEN_RANGE = 3
    range_kind_t = ctypes.c_uint32 # enum
    struct_rangecb_t._pack_ = 1 # source:False
    struct_rangecb_t._fields_ = [
        ('rangesCode', ctypes.c_uint64),
        ('infosize', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('lastreq', ctypes.POINTER(None)),
        ('used_cache', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('ranges', ctypes.POINTER(struct_ranges_cache_t)),
        ('range_kind', range_kind_t),
        ('undo_code', undo_code_t),
        ('db', ctypes.POINTER(struct_dbctx_t)),
        ('read_cb', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_range_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte))),
        ('write_cb', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_range_t), ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_ubyte))),
        ('delcache_cb', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_range_t))),
    ]
    
    class struct_addrinfo(Structure):
        pass
    
    class struct_sockaddr(Structure):
        pass
    
    struct_addrinfo._pack_ = 1 # source:False
    struct_addrinfo._fields_ = [
        ('ai_flags', ctypes.c_int32),
        ('ai_family', ctypes.c_int32),
        ('ai_socktype', ctypes.c_int32),
        ('ai_protocol', ctypes.c_int32),
        ('ai_addrlen', ctypes.c_uint64),
        ('ai_canonname', ctypes.c_char_p),
        ('ai_addr', ctypes.POINTER(struct_sockaddr)),
        ('ai_next', ctypes.POINTER(struct_addrinfo)),
    ]
    
    class struct_bf_key_t(Structure):
        pass
    
    struct_bf_key_t._pack_ = 1 # source:False
    struct_bf_key_t._fields_ = [
        ('p', ctypes.c_uint32 * 18),
        ('s', ctypes.c_uint32 * 256 * 4),
    ]
    
    struct_compat_t._pack_ = 1 # source:False
    struct_compat_t._fields_ = [
        ('in', ctypes.c_uint32),
        ('out', ctypes.c_uint32),
        ('flag', ctypes.c_uint32),
    ]
    
    class struct_config_s(Structure):
        pass
    
    
    # values for enumeration 'block_state'
    block_state__enumvalues = {
        0: 'need_more',
        1: 'block_done',
        2: 'finish_started',
        3: 'finish_done',
    }
    need_more = 0
    block_done = 1
    finish_started = 2
    finish_done = 3
    block_state = ctypes.c_uint32 # enum
    struct_config_s._pack_ = 1 # source:False
    struct_config_s._fields_ = [
        ('good_length', ctypes.c_uint16),
        ('max_lazy', ctypes.c_uint16),
        ('nice_length', ctypes.c_uint16),
        ('max_chain', ctypes.c_uint16),
        ('func', ctypes.CFUNCTYPE(block_state, ctypes.POINTER(None), ctypes.c_int32)),
    ]
    
    class struct_gz_state(Structure):
        pass
    
    struct_gz_state._pack_ = 1 # source:False
    struct_gz_state._fields_ = [
        ('mode', ctypes.c_int32),
        ('fd', ctypes.c_int32),
        ('path', ctypes.c_char_p),
        ('pos', ctypes.c_int32),
        ('size', ctypes.c_uint32),
        ('want', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('in', ctypes.POINTER(ctypes.c_ubyte)),
        ('out', ctypes.POINTER(ctypes.c_ubyte)),
        ('next', ctypes.POINTER(ctypes.c_ubyte)),
        ('have', ctypes.c_uint32),
        ('eof', ctypes.c_int32),
        ('start', ctypes.c_int32),
        ('raw', ctypes.c_int32),
        ('how', ctypes.c_int32),
        ('direct', ctypes.c_int32),
        ('level', ctypes.c_int32),
        ('strategy', ctypes.c_int32),
        ('skip', ctypes.c_int32),
        ('seek', ctypes.c_int32),
        ('err', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('msg', ctypes.c_char_p),
        ('strm', struct_z_stream_s),
    ]
    
    class struct_interval(Structure):
        pass
    
    class struct_qwpath_t(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('buf', struct__qstring_wchar_t_),
         ]
    
    struct_sockaddr._pack_ = 1 # source:False
    struct_sockaddr._fields_ = [
        ('sa_family', ctypes.c_uint16),
        ('sa_data', ctypes.c_char * 14),
    ]
    
    class struct_WSAData(Structure):
        pass
    
    struct_WSAData._pack_ = 1 # source:False
    struct_WSAData._fields_ = [
        ('wVersion', ctypes.c_uint16),
        ('wHighVersion', ctypes.c_uint16),
        ('iMaxSockets', ctypes.c_uint16),
        ('iMaxUdpDg', ctypes.c_uint16),
        ('lpVendorInfo', ctypes.c_char_p),
        ('szDescription', ctypes.c_char * 257),
        ('szSystemStatus', ctypes.c_char * 129),
        ('PADDING_0', ctypes.c_ubyte * 6),
    ]
    
    class struct__cpinfo(Structure):
        pass
    
    struct__cpinfo._pack_ = 1 # source:False
    struct__cpinfo._fields_ = [
        ('MaxCharSize', ctypes.c_uint32),
        ('DefaultChar', ctypes.c_ubyte * 2),
        ('LeadByte', ctypes.c_ubyte * 12),
        ('PADDING_0', ctypes.c_ubyte * 2),
    ]
    
    class struct_hostent(Structure):
        pass
    
    struct_hostent._pack_ = 1 # source:False
    struct_hostent._fields_ = [
        ('h_name', ctypes.c_char_p),
        ('h_aliases', ctypes.POINTER(ctypes.c_char_p)),
        ('h_addrtype', ctypes.c_int16),
        ('h_length', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('h_addr_list', ctypes.POINTER(ctypes.c_char_p)),
    ]
    
    class struct_netlink(Structure):
        pass
    
    struct_netlink._pack_ = 1 # source:False
    struct_netlink._fields_ = [
        ('linknumber', ctypes.c_uint64),
    ]
    
    class struct_servent(Structure):
        pass
    
    struct_servent._pack_ = 1 # source:False
    struct_servent._fields_ = [
        ('s_name', ctypes.c_char_p),
        ('s_aliases', ctypes.POINTER(ctypes.c_char_p)),
        ('s_proto', ctypes.c_char_p),
        ('s_port', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 6),
    ]
    
    class struct_timeval(Structure):
        pass
    
    struct_timeval._pack_ = 1 # source:False
    struct_timeval._fields_ = [
        ('tv_sec', ctypes.c_int32),
        ('tv_usec', ctypes.c_int32),
    ]
    
    class struct_unz64_s(Structure):
        pass
    
    struct_unz64_s._pack_ = 1 # source:False
    struct_unz64_s._fields_ = [
        ('z_filefunc', struct_zlib_filefunc64_32_def_s),
        ('is64bitOpenFunction', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('filestream', ctypes.POINTER(None)),
        ('gi', struct_unz_global_info64_s),
        ('byte_before_the_zipfile', ctypes.c_uint64),
        ('num_file', ctypes.c_uint64),
        ('pos_in_central_dir', ctypes.c_uint64),
        ('current_file_ok', ctypes.c_uint64),
        ('central_pos', ctypes.c_uint64),
        ('size_central_dir', ctypes.c_uint64),
        ('offset_central_dir', ctypes.c_uint64),
        ('cur_file_info', struct_unz_file_info64_s),
        ('cur_file_info_internal', struct_unz_file_info64_internal_s),
        ('pfile_in_zip_read', ctypes.POINTER(struct_file_in_zip64_read_info_s)),
        ('encrypted', ctypes.c_int32),
        ('isZip64', ctypes.c_int32),
    ]
    
    struct_HKEY__._pack_ = 1 # source:False
    struct_HKEY__._fields_ = [
        ('unused', ctypes.c_int32),
    ]
    
    class struct_HWND__(Structure):
        pass
    
    struct_HWND__._pack_ = 1 # source:False
    struct_HWND__._fields_ = [
        ('unused', ctypes.c_int32),
    ]
    
    class struct_fd_set(Structure):
        pass
    
    struct_fd_set._pack_ = 1 # source:False
    struct_fd_set._fields_ = [
        ('fd_count', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('fd_array', ctypes.c_uint64 * 64),
    ]
    
    
    # values for enumeration 'std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64______unnamed_enum_bucket_size_'
    std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64______unnamed_enum_bucket_size___enumvalues = {
        1: 'bucket_size',
    }
    bucket_size = 1
    std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64______unnamed_enum_bucket_size_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl'
    std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl__enumvalues = {
    }
    std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl'
    std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues = {
    }
    std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl'
    std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues = {
    }
    std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl'
    std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl__enumvalues = {
    }
    std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl'
    std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl__enumvalues = {
        0: '_Red',
        1: '_Black',
    }
    _Red = 0
    _Black = 1
    std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl = ctypes.c_uint32 # enum
    
    # values for enumeration 'clean_quick_filter_flags____l2___unnamed_enum_UIFILT_QUICK_'
    clean_quick_filter_flags____l2___unnamed_enum_UIFILT_QUICK___enumvalues = {
        2147483648: 'UIFILT_QUICK',
    }
    UIFILT_QUICK = 2147483648
    clean_quick_filter_flags____l2___unnamed_enum_UIFILT_QUICK_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'tls_stream_t__initialize_security_ctx____l2__state_t'
    tls_stream_t__initialize_security_ctx____l2__state_t__enumvalues = {
        0: 'STATE_INIT',
        1: 'SEND_TOKEN',
        2: 'RECV_DATA',
        3: 'STATE_INIT_CONT',
    }
    STATE_INIT = 0
    SEND_TOKEN = 1
    RECV_DATA = 2
    STATE_INIT_CONT = 3
    tls_stream_t__initialize_security_ctx____l2__state_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'rangecb_undo_record_t___unnamed_enum_CREATE_RANGE_'
    rangecb_undo_record_t___unnamed_enum_CREATE_RANGE___enumvalues = {
        0: 'CREATE_RANGE',
        1: 'DEL_RANGE',
        2: 'UPDATE',
        3: 'SET_START',
        4: 'SET_END',
    }
    CREATE_RANGE = 0
    DEL_RANGE = 1
    UPDATE = 2
    SET_START = 3
    SET_END = 4
    rangecb_undo_record_t___unnamed_enum_CREATE_RANGE_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'switch_info_t___unnamed_enum_SWITCH_INFO_VERSION_'
    switch_info_t___unnamed_enum_SWITCH_INFO_VERSION___enumvalues = {
        2: 'SWITCH_INFO_VERSION',
    }
    SWITCH_INFO_VERSION = 2
    switch_info_t___unnamed_enum_SWITCH_INFO_VERSION_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'chooser_base_t___unnamed_enum_NO_SELECTION_'
    chooser_base_t___unnamed_enum_NO_SELECTION___enumvalues = {
        4294967295: 'NO_SELECTION',
        4294967294: 'EMPTY_CHOOSER',
        4294967293: 'ALREADY_EXISTS',
        4294967292: 'NO_ATTR',
    }
    NO_SELECTION = 4294967295
    EMPTY_CHOOSER = 4294967294
    ALREADY_EXISTS = 4294967293
    NO_ATTR = 4294967292
    chooser_base_t___unnamed_enum_NO_SELECTION_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'rangeset_undo_record_t___unnamed_enum_ADD_'
    rangeset_undo_record_t___unnamed_enum_ADD___enumvalues = {
        0: 'ADD',
        1: 'DEL',
    }
    ADD = 0
    DEL = 1
    rangeset_undo_record_t___unnamed_enum_ADD_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'chooser_base_t___unnamed_enum_POPUP_INS_'
    chooser_base_t___unnamed_enum_POPUP_INS___enumvalues = {
        0: 'POPUP_INS',
        1: 'POPUP_DEL',
        2: 'POPUP_EDIT',
        3: 'POPUP_REFRESH',
        4: 'NSTDPOPUPS',
    }
    POPUP_INS = 0
    POPUP_DEL = 1
    POPUP_EDIT = 2
    POPUP_REFRESH = 3
    NSTDPOPUPS = 4
    chooser_base_t___unnamed_enum_POPUP_INS_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'exec_request_t___unnamed_enum_MFF_MAGIC_'
    exec_request_t___unnamed_enum_MFF_MAGIC___enumvalues = {
        305419896: 'MFF_MAGIC',
    }
    MFF_MAGIC = 305419896
    exec_request_t___unnamed_enum_MFF_MAGIC_ = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Tree_node_int_void__P____Redbl'
    std___Tree_node_int_void__P____Redbl__enumvalues = {
    }
    std___Tree_node_int_void__P____Redbl = ctypes.c_uint32 # enum
    class union_sha1_transform____l2__CHAR64LONG16(Union):
        pass
    
    union_sha1_transform____l2__CHAR64LONG16._pack_ = 1 # source:False
    union_sha1_transform____l2__CHAR64LONG16._fields_ = [
        ('l', ctypes.c_uint32 * 16),
    ]
    
    
    # values for enumeration '_09C4AA584BA5AA400AAD2947A5043C7F'
    _09C4AA584BA5AA400AAD2947A5043C7F__enumvalues = {
        1: 'QMOVE_CROSS_FS',
        2: 'QMOVE_OVERWRITE',
        4: 'QMOVE_OVR_RO',
    }
    QMOVE_CROSS_FS = 1
    QMOVE_OVERWRITE = 2
    QMOVE_OVR_RO = 4
    _09C4AA584BA5AA400AAD2947A5043C7F = ctypes.c_uint32 # enum
    class union__3DE6AE7B3A39657473E2A7515E87EC46(Union):
        pass
    
    class struct_lexer_t(Structure):
        pass
    
    class struct_token_t(Structure):
        pass
    
    union__3DE6AE7B3A39657473E2A7515E87EC46._pack_ = 1 # source:False
    union__3DE6AE7B3A39657473E2A7515E87EC46._fields_ = [
        ('ptr', ctypes.POINTER(None)),
        ('mbroff', ctypes.c_uint64),
        ('hnd', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t))),
        ('hnd2', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64)),
        ('hnd3', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(None))),
    ]
    
    class union__54E171B748F453B9C54515BD00780A14(Union):
        pass
    
    union__54E171B748F453B9C54515BD00780A14._pack_ = 1 # source:False
    union__54E171B748F453B9C54515BD00780A14._fields_ = [
        ('ptr', ctypes.POINTER(None)),
        ('mbroff', ctypes.c_uint64),
        ('hnd', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t))),
        ('hnd2', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64)),
        ('hnd3', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(None))),
    ]
    
    class union__5D1D430279E45EFA7377026125DD642A(Union):
        pass
    
    union__5D1D430279E45EFA7377026125DD642A._pack_ = 1 # source:False
    union__5D1D430279E45EFA7377026125DD642A._fields_ = [
        ('frame', ctypes.c_uint64),
        ('owner', ctypes.c_uint64),
    ]
    
    class union__64629AA237317EA5DB00FDB53154C12F(Union):
        pass
    
    union__64629AA237317EA5DB00FDB53154C12F._pack_ = 1 # source:False
    union__64629AA237317EA5DB00FDB53154C12F._fields_ = [
        ('reg', ctypes.c_uint16),
        ('phrase', ctypes.c_uint16),
    ]
    
    class union__8299423771E115C2E8FEC5C7170C0424(Union):
        pass
    
    union__8299423771E115C2E8FEC5C7170C0424._pack_ = 1 # source:False
    union__8299423771E115C2E8FEC5C7170C0424._fields_ = [
        ('unicode', ctypes.c_char),
        ('is_unsigned', ctypes.c_char),
    ]
    
    class union__8F90F20BBE5791577C9666706E8030E8(Union):
        pass
    
    union__8F90F20BBE5791577C9666706E8030E8._pack_ = 1 # source:False
    union__8F90F20BBE5791577C9666706E8030E8._fields_ = [
        ('frregs', ctypes.c_uint16),
        ('referers', ctypes.POINTER(ctypes.c_uint64)),
    ]
    
    class union__A5E17D51D1B600D0B7B66EE4F38162AD(Union):
        pass
    
    union__A5E17D51D1B600D0B7B66EE4F38162AD._pack_ = 1 # source:False
    union__A5E17D51D1B600D0B7B66EE4F38162AD._fields_ = [
        ('auxpref', ctypes.c_uint32),
        ('auxpref_u16', ctypes.c_uint16 * 2),
        ('auxpref_u8', ctypes.c_ubyte * 4),
    ]
    
    class union__CA1F7F8D68BE4BE32BB567D2F056EF78(Union):
        pass
    
    union__CA1F7F8D68BE4BE32BB567D2F056EF78._pack_ = 1 # source:False
    union__CA1F7F8D68BE4BE32BB567D2F056EF78._fields_ = [
        ('values', ctypes.c_uint64),
        ('lowcase', ctypes.c_uint64),
    ]
    
    class union__CDAEAF5FCF1997B6248EE94570C87B85(Union):
        pass
    
    class struct_cfgopt_t__num_range_t(Structure):
        pass
    
    struct_cfgopt_t__num_range_t._pack_ = 1 # source:False
    struct_cfgopt_t__num_range_t._fields_ = [
        ('minval', ctypes.c_int64),
        ('maxval', ctypes.c_int64),
    ]
    
    class struct_cfgopt_t__params_t(Structure):
        pass
    
    struct_cfgopt_t__params_t._pack_ = 1 # source:False
    struct_cfgopt_t__params_t._fields_ = [
        ('p1', ctypes.c_int64),
        ('p2', ctypes.c_int64),
    ]
    
    union__CDAEAF5FCF1997B6248EE94570C87B85._pack_ = 1 # source:False
    union__CDAEAF5FCF1997B6248EE94570C87B85._fields_ = [
        ('buf_size', ctypes.c_uint64),
        ('num_range', struct_cfgopt_t__num_range_t),
        ('bit_flags', ctypes.c_uint32),
        ('params', struct_cfgopt_t__params_t),
        ('mbroff_obj', ctypes.POINTER(None)),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union__D0E407B3630C0B04C6372E28DCB32106(Union):
        pass
    
    union__D0E407B3630C0B04C6372E28DCB32106._pack_ = 1 # source:False
    union__D0E407B3630C0B04C6372E28DCB32106._fields_ = [
        ('buf_size', ctypes.c_uint64),
        ('num_range', struct_cfgopt_t__num_range_t),
        ('bit_flags', ctypes.c_uint32),
        ('params', struct_cfgopt_t__params_t),
        ('mbroff_obj', ctypes.POINTER(None)),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union__D4468D5BF9897CF7F6CFF118171074C3(Union):
        pass
    
    union__D4468D5BF9897CF7F6CFF118171074C3._pack_ = 1 # source:False
    union__D4468D5BF9897CF7F6CFF118171074C3._fields_ = [
        ('buf_size', ctypes.c_uint64),
        ('num_range', struct_cfgopt_t__num_range_t),
        ('bit_flags', ctypes.c_uint32),
        ('params', struct_cfgopt_t__params_t),
        ('mbroff_obj', ctypes.POINTER(None)),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union__D669CC2BBD58AEBA90A37169AF561FDB(Union):
        pass
    
    union__D669CC2BBD58AEBA90A37169AF561FDB._pack_ = 1 # source:False
    union__D669CC2BBD58AEBA90A37169AF561FDB._fields_ = [
        ('frsize', ctypes.c_uint64),
        ('refqty', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__E728194B4577C1D54504CD54AE296467(Union):
        pass
    
    class struct_fpvalue_t(Structure):
        pass
    
    struct_fpvalue_t._pack_ = 1 # source:False
    struct_fpvalue_t._fields_ = [
        ('w', ctypes.c_uint16 * 6),
    ]
    
    union__E728194B4577C1D54504CD54AE296467._pack_ = 1 # source:True
    union__E728194B4577C1D54504CD54AE296467._fields_ = [
        ('fnum', struct_fpvalue_t),
        ('i64', ctypes.c_int64),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    
    # values for enumeration 'DISPLAYCONFIG_SCANLINE_ORDERING'
    DISPLAYCONFIG_SCANLINE_ORDERING__enumvalues = {
        0: 'DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED',
        1: 'DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE',
        2: 'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED',
        2: 'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST',
        3: 'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST',
        4294967295: 'DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32',
    }
    DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED = 0
    DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE = 1
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED = 2
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST = 2
    DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST = 3
    DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32 = 4294967295
    DISPLAYCONFIG_SCANLINE_ORDERING = ctypes.c_uint32 # enum
    
    # values for enumeration 'ReplacesCorHdrNumericDefines'
    ReplacesCorHdrNumericDefines__enumvalues = {
        1: 'COMIMAGE_FLAGS_ILONLY',
        2: 'COMIMAGE_FLAGS_32BITREQUIRED',
        4: 'COMIMAGE_FLAGS_IL_LIBRARY',
        8: 'COMIMAGE_FLAGS_STRONGNAMESIGNED',
        16: 'COMIMAGE_FLAGS_NATIVE_ENTRYPOINT',
        65536: 'COMIMAGE_FLAGS_TRACKDEBUGDATA',
        2: 'COR_VERSION_MAJOR_V2',
        2: 'COR_VERSION_MAJOR',
        0: 'COR_VERSION_MINOR',
        8: 'COR_DELETED_NAME_LENGTH',
        8: 'COR_VTABLEGAP_NAME_LENGTH',
        1: 'NATIVE_TYPE_MAX_CB',
        255: 'COR_ILMETHOD_SECT_SMALL_MAX_DATASIZE',
        1: 'IMAGE_COR_MIH_METHODRVA',
        2: 'IMAGE_COR_MIH_EHRVA',
        8: 'IMAGE_COR_MIH_BASICBLOCK',
        1: 'COR_VTABLE_32BIT',
        2: 'COR_VTABLE_64BIT',
        4: 'COR_VTABLE_FROM_UNMANAGED',
        8: 'COR_VTABLE_FROM_UNMANAGED_RETAIN_APPDOMAIN',
        16: 'COR_VTABLE_CALL_MOST_DERIVED',
        32: 'IMAGE_COR_EATJ_THUNK_SIZE',
        1024: 'MAX_CLASS_NAME',
        1024: 'MAX_PACKAGE_NAME',
    }
    COMIMAGE_FLAGS_ILONLY = 1
    COMIMAGE_FLAGS_32BITREQUIRED = 2
    COMIMAGE_FLAGS_IL_LIBRARY = 4
    COMIMAGE_FLAGS_STRONGNAMESIGNED = 8
    COMIMAGE_FLAGS_NATIVE_ENTRYPOINT = 16
    COMIMAGE_FLAGS_TRACKDEBUGDATA = 65536
    COR_VERSION_MAJOR_V2 = 2
    COR_VERSION_MAJOR = 2
    COR_VERSION_MINOR = 0
    COR_DELETED_NAME_LENGTH = 8
    COR_VTABLEGAP_NAME_LENGTH = 8
    NATIVE_TYPE_MAX_CB = 1
    COR_ILMETHOD_SECT_SMALL_MAX_DATASIZE = 255
    IMAGE_COR_MIH_METHODRVA = 1
    IMAGE_COR_MIH_EHRVA = 2
    IMAGE_COR_MIH_BASICBLOCK = 8
    COR_VTABLE_32BIT = 1
    COR_VTABLE_64BIT = 2
    COR_VTABLE_FROM_UNMANAGED = 4
    COR_VTABLE_FROM_UNMANAGED_RETAIN_APPDOMAIN = 8
    COR_VTABLE_CALL_MOST_DERIVED = 16
    IMAGE_COR_EATJ_THUNK_SIZE = 32
    MAX_CLASS_NAME = 1024
    MAX_PACKAGE_NAME = 1024
    ReplacesCorHdrNumericDefines = ctypes.c_uint32 # enum
    
    # values for enumeration 'codepoint_stream_t__ncp_t'
    codepoint_stream_t__ncp_t__enumvalues = {
        0: 'NCP_OK',
        1: 'NCP_NOBYTE',
        2: 'NCP_NOCONV',
    }
    NCP_OK = 0
    NCP_NOBYTE = 1
    NCP_NOCONV = 2
    codepoint_stream_t__ncp_t = ctypes.c_uint32 # enum
    
    # values for enumeration '__MIDL_ICodeInstall_0001'
    __MIDL_ICodeInstall_0001__enumvalues = {
        0: 'CIP_DISK_FULL',
        1: 'CIP_ACCESS_DENIED',
        2: 'CIP_NEWER_VERSION_EXISTS',
        3: 'CIP_OLDER_VERSION_EXISTS',
        4: 'CIP_NAME_CONFLICT',
        5: 'CIP_TRUST_VERIFICATION_COMPONENT_MISSING',
        6: 'CIP_EXE_SELF_REGISTERATION_TIMEOUT',
        7: 'CIP_UNSAFE_TO_ABORT',
        8: 'CIP_NEED_REBOOT',
        9: 'CIP_NEED_REBOOT_UI_PERMISSION',
    }
    CIP_DISK_FULL = 0
    CIP_ACCESS_DENIED = 1
    CIP_NEWER_VERSION_EXISTS = 2
    CIP_OLDER_VERSION_EXISTS = 3
    CIP_NAME_CONFLICT = 4
    CIP_TRUST_VERIFICATION_COMPONENT_MISSING = 5
    CIP_EXE_SELF_REGISTERATION_TIMEOUT = 6
    CIP_UNSAFE_TO_ABORT = 7
    CIP_NEED_REBOOT = 8
    CIP_NEED_REBOOT_UI_PERMISSION = 9
    __MIDL_ICodeInstall_0001 = ctypes.c_uint32 # enum
    
    # values for enumeration '_tagINTERNETFEATURELIST'
    _tagINTERNETFEATURELIST__enumvalues = {
        0: 'FEATURE_OBJECT_CACHING',
        1: 'FEATURE_ZONE_ELEVATION',
        2: 'FEATURE_MIME_HANDLING',
        3: 'FEATURE_MIME_SNIFFING',
        4: 'FEATURE_WINDOW_RESTRICTIONS',
        5: 'FEATURE_WEBOC_POPUPMANAGEMENT',
        6: 'FEATURE_BEHAVIORS',
        7: 'FEATURE_DISABLE_MK_PROTOCOL',
        8: 'FEATURE_LOCALMACHINE_LOCKDOWN',
        9: 'FEATURE_SECURITYBAND',
        10: 'FEATURE_RESTRICT_ACTIVEXINSTALL',
        11: 'FEATURE_VALIDATE_NAVIGATE_URL',
        12: 'FEATURE_RESTRICT_FILEDOWNLOAD',
        13: 'FEATURE_ADDON_MANAGEMENT',
        14: 'FEATURE_PROTOCOL_LOCKDOWN',
        15: 'FEATURE_HTTP_USERNAME_PASSWORD_DISABLE',
        16: 'FEATURE_SAFE_BINDTOOBJECT',
        17: 'FEATURE_UNC_SAVEDFILECHECK',
        18: 'FEATURE_GET_URL_DOM_FILEPATH_UNENCODED',
        19: 'FEATURE_TABBED_BROWSING',
        20: 'FEATURE_SSLUX',
        21: 'FEATURE_DISABLE_NAVIGATION_SOUNDS',
        22: 'FEATURE_DISABLE_LEGACY_COMPRESSION',
        23: 'FEATURE_FORCE_ADDR_AND_STATUS',
        24: 'FEATURE_XMLHTTP',
        25: 'FEATURE_DISABLE_TELNET_PROTOCOL',
        26: 'FEATURE_FEEDS',
        27: 'FEATURE_BLOCK_INPUT_PROMPTS',
        28: 'FEATURE_ENTRY_COUNT',
    }
    FEATURE_OBJECT_CACHING = 0
    FEATURE_ZONE_ELEVATION = 1
    FEATURE_MIME_HANDLING = 2
    FEATURE_MIME_SNIFFING = 3
    FEATURE_WINDOW_RESTRICTIONS = 4
    FEATURE_WEBOC_POPUPMANAGEMENT = 5
    FEATURE_BEHAVIORS = 6
    FEATURE_DISABLE_MK_PROTOCOL = 7
    FEATURE_LOCALMACHINE_LOCKDOWN = 8
    FEATURE_SECURITYBAND = 9
    FEATURE_RESTRICT_ACTIVEXINSTALL = 10
    FEATURE_VALIDATE_NAVIGATE_URL = 11
    FEATURE_RESTRICT_FILEDOWNLOAD = 12
    FEATURE_ADDON_MANAGEMENT = 13
    FEATURE_PROTOCOL_LOCKDOWN = 14
    FEATURE_HTTP_USERNAME_PASSWORD_DISABLE = 15
    FEATURE_SAFE_BINDTOOBJECT = 16
    FEATURE_UNC_SAVEDFILECHECK = 17
    FEATURE_GET_URL_DOM_FILEPATH_UNENCODED = 18
    FEATURE_TABBED_BROWSING = 19
    FEATURE_SSLUX = 20
    FEATURE_DISABLE_NAVIGATION_SOUNDS = 21
    FEATURE_DISABLE_LEGACY_COMPRESSION = 22
    FEATURE_FORCE_ADDR_AND_STATUS = 23
    FEATURE_XMLHTTP = 24
    FEATURE_DISABLE_TELNET_PROTOCOL = 25
    FEATURE_FEEDS = 26
    FEATURE_BLOCK_INPUT_PROMPTS = 27
    FEATURE_ENTRY_COUNT = 28
    _tagINTERNETFEATURELIST = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagCONDITION_OPERATION'
    tagCONDITION_OPERATION__enumvalues = {
        0: 'COP_IMPLICIT',
        1: 'COP_EQUAL',
        2: 'COP_NOTEQUAL',
        3: 'COP_LESSTHAN',
        4: 'COP_GREATERTHAN',
        5: 'COP_LESSTHANOREQUAL',
        6: 'COP_GREATERTHANOREQUAL',
        7: 'COP_VALUE_STARTSWITH',
        8: 'COP_VALUE_ENDSWITH',
        9: 'COP_VALUE_CONTAINS',
        10: 'COP_VALUE_NOTCONTAINS',
        11: 'COP_DOSWILDCARDS',
        12: 'COP_WORD_EQUAL',
        13: 'COP_WORD_STARTSWITH',
        14: 'COP_APPLICATION_SPECIFIC',
    }
    COP_IMPLICIT = 0
    COP_EQUAL = 1
    COP_NOTEQUAL = 2
    COP_LESSTHAN = 3
    COP_GREATERTHAN = 4
    COP_LESSTHANOREQUAL = 5
    COP_GREATERTHANOREQUAL = 6
    COP_VALUE_STARTSWITH = 7
    COP_VALUE_ENDSWITH = 8
    COP_VALUE_CONTAINS = 9
    COP_VALUE_NOTCONTAINS = 10
    COP_DOSWILDCARDS = 11
    COP_WORD_EQUAL = 12
    COP_WORD_STARTSWITH = 13
    COP_APPLICATION_SPECIFIC = 14
    tagCONDITION_OPERATION = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagGLOBALOPT_EH_VALUES'
    tagGLOBALOPT_EH_VALUES__enumvalues = {
        0: 'COMGLB_EXCEPTION_HANDLE',
        1: 'COMGLB_EXCEPTION_DONOT_HANDLE_FATAL',
        1: 'COMGLB_EXCEPTION_DONOT_HANDLE',
        2: 'COMGLB_EXCEPTION_DONOT_HANDLE_ANY',
    }
    COMGLB_EXCEPTION_HANDLE = 0
    COMGLB_EXCEPTION_DONOT_HANDLE_FATAL = 1
    COMGLB_EXCEPTION_DONOT_HANDLE = 1
    COMGLB_EXCEPTION_DONOT_HANDLE_ANY = 2
    tagGLOBALOPT_EH_VALUES = ctypes.c_uint32 # enum
    
    # values for enumeration 'DEFAULTSAVEFOLDERTYPE'
    DEFAULTSAVEFOLDERTYPE__enumvalues = {
        1: 'DSFT_DETECT',
        2: 'DSFT_PRIVATE',
        3: 'DSFT_PUBLIC',
    }
    DSFT_DETECT = 1
    DSFT_PRIVATE = 2
    DSFT_PUBLIC = 3
    DEFAULTSAVEFOLDERTYPE = ctypes.c_uint32 # enum
    
    # values for enumeration '_TP_CALLBACK_PRIORITY'
    _TP_CALLBACK_PRIORITY__enumvalues = {
        0: 'TP_CALLBACK_PRIORITY_HIGH',
        1: 'TP_CALLBACK_PRIORITY_NORMAL',
        2: 'TP_CALLBACK_PRIORITY_LOW',
        3: 'TP_CALLBACK_PRIORITY_INVALID',
    }
    TP_CALLBACK_PRIORITY_HIGH = 0
    TP_CALLBACK_PRIORITY_NORMAL = 1
    TP_CALLBACK_PRIORITY_LOW = 2
    TP_CALLBACK_PRIORITY_INVALID = 3
    _TP_CALLBACK_PRIORITY = ctypes.c_uint32 # enum
    
    # values for enumeration 'OfflineFolderStatus'
    OfflineFolderStatus__enumvalues = {
        4294967295: 'OFS_INACTIVE',
        0: 'OFS_ONLINE',
        1: 'OFS_OFFLINE',
        2: 'OFS_SERVERBACK',
        3: 'OFS_DIRTYCACHE',
    }
    OFS_INACTIVE = 4294967295
    OFS_ONLINE = 0
    OFS_OFFLINE = 1
    OFS_SERVERBACK = 2
    OFS_DIRTYCACHE = 3
    OfflineFolderStatus = ctypes.c_uint32 # enum
    
    # values for enumeration 'PIDMSI_STATUS_VALUE'
    PIDMSI_STATUS_VALUE__enumvalues = {
        0: 'PIDMSI_STATUS_NORMAL',
        1: 'PIDMSI_STATUS_NEW',
        2: 'PIDMSI_STATUS_PRELIM',
        3: 'PIDMSI_STATUS_DRAFT',
        4: 'PIDMSI_STATUS_INPROGRESS',
        5: 'PIDMSI_STATUS_EDIT',
        6: 'PIDMSI_STATUS_REVIEW',
        7: 'PIDMSI_STATUS_PROOF',
        8: 'PIDMSI_STATUS_FINAL',
        32767: 'PIDMSI_STATUS_OTHER',
    }
    PIDMSI_STATUS_NORMAL = 0
    PIDMSI_STATUS_NEW = 1
    PIDMSI_STATUS_PRELIM = 2
    PIDMSI_STATUS_DRAFT = 3
    PIDMSI_STATUS_INPROGRESS = 4
    PIDMSI_STATUS_EDIT = 5
    PIDMSI_STATUS_REVIEW = 6
    PIDMSI_STATUS_PROOF = 7
    PIDMSI_STATUS_FINAL = 8
    PIDMSI_STATUS_OTHER = 32767
    PIDMSI_STATUS_VALUE = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagApplicationType'
    tagApplicationType__enumvalues = {
        0: 'ServerApplication',
        1: 'LibraryApplication',
    }
    ServerApplication = 0
    LibraryApplication = 1
    tagApplicationType = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagMENUPOPUPSELECT'
    tagMENUPOPUPSELECT__enumvalues = {
        0: 'MPOS_EXECUTE',
        1: 'MPOS_FULLCANCEL',
        2: 'MPOS_CANCELLEVEL',
        3: 'MPOS_SELECTLEFT',
        4: 'MPOS_SELECTRIGHT',
        5: 'MPOS_CHILDTRACKING',
    }
    MPOS_EXECUTE = 0
    MPOS_FULLCANCEL = 1
    MPOS_CANCELLEVEL = 2
    MPOS_SELECTLEFT = 3
    MPOS_SELECTRIGHT = 4
    MPOS_CHILDTRACKING = 5
    tagMENUPOPUPSELECT = ctypes.c_uint32 # enum
    
    # values for enumeration 'KNOWNDESTCATEGORY'
    KNOWNDESTCATEGORY__enumvalues = {
        1: 'KDC_FREQUENT',
        2: 'KDC_RECENT',
    }
    KDC_FREQUENT = 1
    KDC_RECENT = 2
    KNOWNDESTCATEGORY = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagCONDITION_TYPE'
    tagCONDITION_TYPE__enumvalues = {
        0: 'CT_AND_CONDITION',
        1: 'CT_OR_CONDITION',
        2: 'CT_NOT_CONDITION',
        3: 'CT_LEAF_CONDITION',
    }
    CT_AND_CONDITION = 0
    CT_OR_CONDITION = 1
    CT_NOT_CONDITION = 2
    CT_LEAF_CONDITION = 3
    tagCONDITION_TYPE = ctypes.c_uint32 # enum
    
    # values for enumeration 'ASSOCIATIONLEVEL'
    ASSOCIATIONLEVEL__enumvalues = {
        0: 'AL_MACHINE',
        1: 'AL_EFFECTIVE',
        2: 'AL_USER',
    }
    AL_MACHINE = 0
    AL_EFFECTIVE = 1
    AL_USER = 2
    ASSOCIATIONLEVEL = ctypes.c_uint32 # enum
    
    # values for enumeration '__MIDL_IUri_0001'
    __MIDL_IUri_0001__enumvalues = {
        0: 'Uri_PROPERTY_ABSOLUTE_URI',
        0: 'Uri_PROPERTY_STRING_START',
        1: 'Uri_PROPERTY_AUTHORITY',
        2: 'Uri_PROPERTY_DISPLAY_URI',
        3: 'Uri_PROPERTY_DOMAIN',
        4: 'Uri_PROPERTY_EXTENSION',
        5: 'Uri_PROPERTY_FRAGMENT',
        6: 'Uri_PROPERTY_HOST',
        7: 'Uri_PROPERTY_PASSWORD',
        8: 'Uri_PROPERTY_PATH',
        9: 'Uri_PROPERTY_PATH_AND_QUERY',
        10: 'Uri_PROPERTY_QUERY',
        11: 'Uri_PROPERTY_RAW_URI',
        12: 'Uri_PROPERTY_SCHEME_NAME',
        13: 'Uri_PROPERTY_USER_INFO',
        14: 'Uri_PROPERTY_USER_NAME',
        14: 'Uri_PROPERTY_STRING_LAST',
        15: 'Uri_PROPERTY_HOST_TYPE',
        15: 'Uri_PROPERTY_DWORD_START',
        16: 'Uri_PROPERTY_PORT',
        17: 'Uri_PROPERTY_SCHEME',
        18: 'Uri_PROPERTY_ZONE',
        18: 'Uri_PROPERTY_DWORD_LAST',
    }
    Uri_PROPERTY_ABSOLUTE_URI = 0
    Uri_PROPERTY_STRING_START = 0
    Uri_PROPERTY_AUTHORITY = 1
    Uri_PROPERTY_DISPLAY_URI = 2
    Uri_PROPERTY_DOMAIN = 3
    Uri_PROPERTY_EXTENSION = 4
    Uri_PROPERTY_FRAGMENT = 5
    Uri_PROPERTY_HOST = 6
    Uri_PROPERTY_PASSWORD = 7
    Uri_PROPERTY_PATH = 8
    Uri_PROPERTY_PATH_AND_QUERY = 9
    Uri_PROPERTY_QUERY = 10
    Uri_PROPERTY_RAW_URI = 11
    Uri_PROPERTY_SCHEME_NAME = 12
    Uri_PROPERTY_USER_INFO = 13
    Uri_PROPERTY_USER_NAME = 14
    Uri_PROPERTY_STRING_LAST = 14
    Uri_PROPERTY_HOST_TYPE = 15
    Uri_PROPERTY_DWORD_START = 15
    Uri_PROPERTY_PORT = 16
    Uri_PROPERTY_SCHEME = 17
    Uri_PROPERTY_ZONE = 18
    Uri_PROPERTY_DWORD_LAST = 18
    __MIDL_IUri_0001 = ctypes.c_uint32 # enum
    
    # values for enumeration '__MIDL_IUri_0002'
    __MIDL_IUri_0002__enumvalues = {
        0: 'Uri_HOST_UNKNOWN',
        1: 'Uri_HOST_DNS',
        2: 'Uri_HOST_IPV4',
        3: 'Uri_HOST_IPV6',
        4: 'Uri_HOST_IDN',
    }
    Uri_HOST_UNKNOWN = 0
    Uri_HOST_DNS = 1
    Uri_HOST_IPV4 = 2
    Uri_HOST_IPV6 = 3
    Uri_HOST_IDN = 4
    __MIDL_IUri_0002 = ctypes.c_uint32 # enum
    
    # values for enumeration 'base_packet_id_t'
    base_packet_id_t__enumvalues = {
        0: 'RPC_OK',
        1: 'RPC_UNK',
        2: 'RPC_MEM',
        3: 'base_packet_id_last',
    }
    RPC_OK = 0
    RPC_UNK = 1
    RPC_MEM = 2
    base_packet_id_last = 3
    base_packet_id_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'ucdr_atom_type_t'
    ucdr_atom_type_t__enumvalues = {
        0: 'uat_none',
        1: 'uat_cp',
        2: 'uat_range',
        3: 'uat_ucd_cat',
        4: 'uat_ucd_blk',
        5: 'uat_culture',
        6: 'uat_current_culture',
    }
    uat_none = 0
    uat_cp = 1
    uat_range = 2
    uat_ucd_cat = 3
    uat_ucd_blk = 4
    uat_culture = 5
    uat_current_culture = 6
    ucdr_atom_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'undo_direction_t'
    undo_direction_t__enumvalues = {
        0: 'PERFORM_UNDO',
        1: 'PERFORM_REDO',
    }
    PERFORM_UNDO = 0
    PERFORM_REDO = 1
    undo_direction_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'ASSOCIATIONTYPE'
    ASSOCIATIONTYPE__enumvalues = {
        0: 'AT_FILEEXTENSION',
        1: 'AT_URLPROTOCOL',
        2: 'AT_STARTMENUCLIENT',
        3: 'AT_MIMETYPE',
    }
    AT_FILEEXTENSION = 0
    AT_URLPROTOCOL = 1
    AT_STARTMENUCLIENT = 2
    AT_MIMETYPE = 3
    ASSOCIATIONTYPE = ctypes.c_uint32 # enum
    
    # values for enumeration 'FILE_USAGE_TYPE'
    FILE_USAGE_TYPE__enumvalues = {
        0: 'FUT_PLAYING',
        1: 'FUT_EDITING',
        2: 'FUT_GENERIC',
    }
    FUT_PLAYING = 0
    FUT_EDITING = 1
    FUT_GENERIC = 2
    FILE_USAGE_TYPE = ctypes.c_uint32 # enum
    
    # values for enumeration '_tagPARSEACTION'
    _tagPARSEACTION__enumvalues = {
        1: 'PARSE_CANONICALIZE',
        2: 'PARSE_FRIENDLY',
        3: 'PARSE_SECURITY_URL',
        4: 'PARSE_ROOTDOCUMENT',
        5: 'PARSE_DOCUMENT',
        6: 'PARSE_ANCHOR',
        7: 'PARSE_ENCODE_IS_UNESCAPE',
        8: 'PARSE_DECODE_IS_ESCAPE',
        9: 'PARSE_PATH_FROM_URL',
        10: 'PARSE_URL_FROM_PATH',
        11: 'PARSE_MIME',
        12: 'PARSE_SERVER',
        13: 'PARSE_SCHEMA',
        14: 'PARSE_SITE',
        15: 'PARSE_DOMAIN',
        16: 'PARSE_LOCATION',
        17: 'PARSE_SECURITY_DOMAIN',
        18: 'PARSE_ESCAPE',
        19: 'PARSE_UNESCAPE',
    }
    PARSE_CANONICALIZE = 1
    PARSE_FRIENDLY = 2
    PARSE_SECURITY_URL = 3
    PARSE_ROOTDOCUMENT = 4
    PARSE_DOCUMENT = 5
    PARSE_ANCHOR = 6
    PARSE_ENCODE_IS_UNESCAPE = 7
    PARSE_DECODE_IS_ESCAPE = 8
    PARSE_PATH_FROM_URL = 9
    PARSE_URL_FROM_PATH = 10
    PARSE_MIME = 11
    PARSE_SERVER = 12
    PARSE_SCHEMA = 13
    PARSE_SITE = 14
    PARSE_DOMAIN = 15
    PARSE_LOCATION = 16
    PARSE_SECURITY_DOMAIN = 17
    PARSE_ESCAPE = 18
    PARSE_UNESCAPE = 19
    _tagPARSEACTION = ctypes.c_uint32 # enum
    
    # values for enumeration '_tagQUERYOPTION'
    _tagQUERYOPTION__enumvalues = {
        1: 'QUERY_EXPIRATION_DATE',
        2: 'QUERY_TIME_OF_LAST_CHANGE',
        3: 'QUERY_CONTENT_ENCODING',
        4: 'QUERY_CONTENT_TYPE',
        5: 'QUERY_REFRESH',
        6: 'QUERY_RECOMBINE',
        7: 'QUERY_CAN_NAVIGATE',
        8: 'QUERY_USES_NETWORK',
        9: 'QUERY_IS_CACHED',
        10: 'QUERY_IS_INSTALLEDENTRY',
        11: 'QUERY_IS_CACHED_OR_MAPPED',
        12: 'QUERY_USES_CACHE',
        13: 'QUERY_IS_SECURE',
        14: 'QUERY_IS_SAFE',
        15: 'QUERY_USES_HISTORYFOLDER',
    }
    QUERY_EXPIRATION_DATE = 1
    QUERY_TIME_OF_LAST_CHANGE = 2
    QUERY_CONTENT_ENCODING = 3
    QUERY_CONTENT_TYPE = 4
    QUERY_REFRESH = 5
    QUERY_RECOMBINE = 6
    QUERY_CAN_NAVIGATE = 7
    QUERY_USES_NETWORK = 8
    QUERY_IS_CACHED = 9
    QUERY_IS_INSTALLEDENTRY = 10
    QUERY_IS_CACHED_OR_MAPPED = 11
    QUERY_USES_CACHE = 12
    QUERY_IS_SECURE = 13
    QUERY_IS_SAFE = 14
    QUERY_USES_HISTORYFOLDER = 15
    _tagQUERYOPTION = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagShutdownType'
    tagShutdownType__enumvalues = {
        0: 'IdleShutdown',
        1: 'ForcedShutdown',
    }
    IdleShutdown = 0
    ForcedShutdown = 1
    tagShutdownType = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagXMLEMEM_TYPE'
    tagXMLEMEM_TYPE__enumvalues = {
        0: 'XMLELEMTYPE_ELEMENT',
        1: 'XMLELEMTYPE_TEXT',
        2: 'XMLELEMTYPE_COMMENT',
        3: 'XMLELEMTYPE_DOCUMENT',
        4: 'XMLELEMTYPE_DTD',
        5: 'XMLELEMTYPE_PI',
        6: 'XMLELEMTYPE_OTHER',
    }
    XMLELEMTYPE_ELEMENT = 0
    XMLELEMTYPE_TEXT = 1
    XMLELEMTYPE_COMMENT = 2
    XMLELEMTYPE_DOCUMENT = 3
    XMLELEMTYPE_DTD = 4
    XMLELEMTYPE_PI = 5
    XMLELEMTYPE_OTHER = 6
    tagXMLEMEM_TYPE = ctypes.c_uint32 # enum
    
    # values for enumeration 'APPDOCLISTTYPE'
    APPDOCLISTTYPE__enumvalues = {
        0: 'ADLT_RECENT',
        1: 'ADLT_FREQUENT',
    }
    ADLT_RECENT = 0
    ADLT_FREQUENT = 1
    APPDOCLISTTYPE = ctypes.c_uint32 # enum
    
    # values for enumeration 'MARKUPLINKTEXT'
    MARKUPLINKTEXT__enumvalues = {
        0: 'MARKUPLINKTEXT_URL',
        1: 'MARKUPLINKTEXT_ID',
        2: 'MARKUPLINKTEXT_TEXT',
    }
    MARKUPLINKTEXT_URL = 0
    MARKUPLINKTEXT_ID = 1
    MARKUPLINKTEXT_TEXT = 2
    MARKUPLINKTEXT = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagBANDSITECID'
    tagBANDSITECID__enumvalues = {
        0: 'BSID_BANDADDED',
        1: 'BSID_BANDREMOVED',
    }
    BSID_BANDADDED = 0
    BSID_BANDREMOVED = 1
    tagBANDSITECID = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagDOMNodeType'
    tagDOMNodeType__enumvalues = {
        0: 'NODE_INVALID',
        1: 'NODE_ELEMENT',
        2: 'NODE_ATTRIBUTE',
        3: 'NODE_TEXT',
        4: 'NODE_CDATA_SECTION',
        5: 'NODE_ENTITY_REFERENCE',
        6: 'NODE_ENTITY',
        7: 'NODE_PROCESSING_INSTRUCTION',
        8: 'NODE_COMMENT',
        9: 'NODE_DOCUMENT',
        10: 'NODE_DOCUMENT_TYPE',
        11: 'NODE_DOCUMENT_FRAGMENT',
        12: 'NODE_NOTATION',
    }
    NODE_INVALID = 0
    NODE_ELEMENT = 1
    NODE_ATTRIBUTE = 2
    NODE_TEXT = 3
    NODE_CDATA_SECTION = 4
    NODE_ENTITY_REFERENCE = 5
    NODE_ENTITY = 6
    NODE_PROCESSING_INSTRUCTION = 7
    NODE_COMMENT = 8
    NODE_DOCUMENT = 9
    NODE_DOCUMENT_TYPE = 10
    NODE_DOCUMENT_FRAGMENT = 11
    NODE_NOTATION = 12
    tagDOMNodeType = ctypes.c_uint32 # enum
    
    # values for enumeration 'MARKUPMESSAGE'
    MARKUPMESSAGE__enumvalues = {
        0: 'MARKUPMESSAGE_KEYEXECUTE',
        1: 'MARKUPMESSAGE_CLICKEXECUTE',
        2: 'MARKUPMESSAGE_WANTFOCUS',
    }
    MARKUPMESSAGE_KEYEXECUTE = 0
    MARKUPMESSAGE_CLICKEXECUTE = 1
    MARKUPMESSAGE_WANTFOCUS = 2
    MARKUPMESSAGE = ctypes.c_uint32 # enum
    
    # values for enumeration '_tagPSUACTION'
    _tagPSUACTION__enumvalues = {
        1: 'PSU_DEFAULT',
        2: 'PSU_SECURITY_URL_ONLY',
    }
    PSU_DEFAULT = 1
    PSU_SECURITY_URL_ONLY = 2
    _tagPSUACTION = ctypes.c_uint32 # enum
    
    # values for enumeration 'cp_category_t'
    cp_category_t__enumvalues = {
        0: 'CPC_Unknown',
        1: 'CPC_Cc',
        2: 'CPC_Cf',
        3: 'CPC_Cn',
        4: 'CPC_Co',
        5: 'CPC_Cs',
        6: 'CPC_LC',
        7: 'CPC_Ll',
        8: 'CPC_Lm',
        9: 'CPC_Lo',
        10: 'CPC_Lt',
        11: 'CPC_Lu',
        12: 'CPC_Mc',
        13: 'CPC_Me',
        14: 'CPC_Mn',
        15: 'CPC_Nd',
        16: 'CPC_Nl',
        17: 'CPC_No',
        18: 'CPC_Pc',
        19: 'CPC_Pd',
        20: 'CPC_Pe',
        21: 'CPC_Pf',
        22: 'CPC_Pi',
        23: 'CPC_Po',
        24: 'CPC_Ps',
        25: 'CPC_Sc',
        26: 'CPC_Sk',
        27: 'CPC_Sm',
        28: 'CPC_So',
        29: 'CPC_Zl',
        30: 'CPC_Zp',
        31: 'CPC_Zs',
        31: 'CPC_last',
    }
    CPC_Unknown = 0
    CPC_Cc = 1
    CPC_Cf = 2
    CPC_Cn = 3
    CPC_Co = 4
    CPC_Cs = 5
    CPC_LC = 6
    CPC_Ll = 7
    CPC_Lm = 8
    CPC_Lo = 9
    CPC_Lt = 10
    CPC_Lu = 11
    CPC_Mc = 12
    CPC_Me = 13
    CPC_Mn = 14
    CPC_Nd = 15
    CPC_Nl = 16
    CPC_No = 17
    CPC_Pc = 18
    CPC_Pd = 19
    CPC_Pe = 20
    CPC_Pf = 21
    CPC_Pi = 22
    CPC_Po = 23
    CPC_Ps = 24
    CPC_Sc = 25
    CPC_Sk = 26
    CPC_Sm = 27
    CPC_So = 28
    CPC_Zl = 29
    CPC_Zp = 30
    CPC_Zs = 31
    CPC_last = 31
    cp_category_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'merge_state_t'
    merge_state_t__enumvalues = {
        0: 'MERGE_STATE_NONE',
        1: 'MERGE_STATE_OPENING',
        2: 'MERGE_STATE_MERGING',
        4: 'MERGE_STATE_2WAY',
    }
    MERGE_STATE_NONE = 0
    MERGE_STATE_OPENING = 1
    MERGE_STATE_MERGING = 2
    MERGE_STATE_2WAY = 4
    merge_state_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagBINDSTATUS'
    tagBINDSTATUS__enumvalues = {
        1: 'BINDSTATUS_FINDINGRESOURCE',
        2: 'BINDSTATUS_CONNECTING',
        3: 'BINDSTATUS_REDIRECTING',
        4: 'BINDSTATUS_BEGINDOWNLOADDATA',
        5: 'BINDSTATUS_DOWNLOADINGDATA',
        6: 'BINDSTATUS_ENDDOWNLOADDATA',
        7: 'BINDSTATUS_BEGINDOWNLOADCOMPONENTS',
        8: 'BINDSTATUS_INSTALLINGCOMPONENTS',
        9: 'BINDSTATUS_ENDDOWNLOADCOMPONENTS',
        10: 'BINDSTATUS_USINGCACHEDCOPY',
        11: 'BINDSTATUS_SENDINGREQUEST',
        12: 'BINDSTATUS_CLASSIDAVAILABLE',
        13: 'BINDSTATUS_MIMETYPEAVAILABLE',
        14: 'BINDSTATUS_CACHEFILENAMEAVAILABLE',
        15: 'BINDSTATUS_BEGINSYNCOPERATION',
        16: 'BINDSTATUS_ENDSYNCOPERATION',
        17: 'BINDSTATUS_BEGINUPLOADDATA',
        18: 'BINDSTATUS_UPLOADINGDATA',
        19: 'BINDSTATUS_ENDUPLOADDATA',
        20: 'BINDSTATUS_PROTOCOLCLASSID',
        21: 'BINDSTATUS_ENCODING',
        22: 'BINDSTATUS_VERIFIEDMIMETYPEAVAILABLE',
        23: 'BINDSTATUS_CLASSINSTALLLOCATION',
        24: 'BINDSTATUS_DECODING',
        25: 'BINDSTATUS_LOADINGMIMEHANDLER',
        26: 'BINDSTATUS_CONTENTDISPOSITIONATTACH',
        27: 'BINDSTATUS_FILTERREPORTMIMETYPE',
        28: 'BINDSTATUS_CLSIDCANINSTANTIATE',
        29: 'BINDSTATUS_IUNKNOWNAVAILABLE',
        30: 'BINDSTATUS_DIRECTBIND',
        31: 'BINDSTATUS_RAWMIMETYPE',
        32: 'BINDSTATUS_PROXYDETECTING',
        33: 'BINDSTATUS_ACCEPTRANGES',
        34: 'BINDSTATUS_COOKIE_SENT',
        35: 'BINDSTATUS_COMPACT_POLICY_RECEIVED',
        36: 'BINDSTATUS_COOKIE_SUPPRESSED',
        37: 'BINDSTATUS_COOKIE_STATE_UNKNOWN',
        38: 'BINDSTATUS_COOKIE_STATE_ACCEPT',
        39: 'BINDSTATUS_COOKIE_STATE_REJECT',
        40: 'BINDSTATUS_COOKIE_STATE_PROMPT',
        41: 'BINDSTATUS_COOKIE_STATE_LEASH',
        42: 'BINDSTATUS_COOKIE_STATE_DOWNGRADE',
        43: 'BINDSTATUS_POLICY_HREF',
        44: 'BINDSTATUS_P3P_HEADER',
        45: 'BINDSTATUS_SESSION_COOKIE_RECEIVED',
        46: 'BINDSTATUS_PERSISTENT_COOKIE_RECEIVED',
        47: 'BINDSTATUS_SESSION_COOKIES_ALLOWED',
        48: 'BINDSTATUS_CACHECONTROL',
        49: 'BINDSTATUS_CONTENTDISPOSITIONFILENAME',
        50: 'BINDSTATUS_MIMETEXTPLAINMISMATCH',
        51: 'BINDSTATUS_PUBLISHERAVAILABLE',
        52: 'BINDSTATUS_DISPLAYNAMEAVAILABLE',
        53: 'BINDSTATUS_SSLUX_NAVBLOCKED',
        54: 'BINDSTATUS_SERVER_MIMETYPEAVAILABLE',
        55: 'BINDSTATUS_SNIFFED_CLASSIDAVAILABLE',
        56: 'BINDSTATUS_64BIT_PROGRESS',
    }
    BINDSTATUS_FINDINGRESOURCE = 1
    BINDSTATUS_CONNECTING = 2
    BINDSTATUS_REDIRECTING = 3
    BINDSTATUS_BEGINDOWNLOADDATA = 4
    BINDSTATUS_DOWNLOADINGDATA = 5
    BINDSTATUS_ENDDOWNLOADDATA = 6
    BINDSTATUS_BEGINDOWNLOADCOMPONENTS = 7
    BINDSTATUS_INSTALLINGCOMPONENTS = 8
    BINDSTATUS_ENDDOWNLOADCOMPONENTS = 9
    BINDSTATUS_USINGCACHEDCOPY = 10
    BINDSTATUS_SENDINGREQUEST = 11
    BINDSTATUS_CLASSIDAVAILABLE = 12
    BINDSTATUS_MIMETYPEAVAILABLE = 13
    BINDSTATUS_CACHEFILENAMEAVAILABLE = 14
    BINDSTATUS_BEGINSYNCOPERATION = 15
    BINDSTATUS_ENDSYNCOPERATION = 16
    BINDSTATUS_BEGINUPLOADDATA = 17
    BINDSTATUS_UPLOADINGDATA = 18
    BINDSTATUS_ENDUPLOADDATA = 19
    BINDSTATUS_PROTOCOLCLASSID = 20
    BINDSTATUS_ENCODING = 21
    BINDSTATUS_VERIFIEDMIMETYPEAVAILABLE = 22
    BINDSTATUS_CLASSINSTALLLOCATION = 23
    BINDSTATUS_DECODING = 24
    BINDSTATUS_LOADINGMIMEHANDLER = 25
    BINDSTATUS_CONTENTDISPOSITIONATTACH = 26
    BINDSTATUS_FILTERREPORTMIMETYPE = 27
    BINDSTATUS_CLSIDCANINSTANTIATE = 28
    BINDSTATUS_IUNKNOWNAVAILABLE = 29
    BINDSTATUS_DIRECTBIND = 30
    BINDSTATUS_RAWMIMETYPE = 31
    BINDSTATUS_PROXYDETECTING = 32
    BINDSTATUS_ACCEPTRANGES = 33
    BINDSTATUS_COOKIE_SENT = 34
    BINDSTATUS_COMPACT_POLICY_RECEIVED = 35
    BINDSTATUS_COOKIE_SUPPRESSED = 36
    BINDSTATUS_COOKIE_STATE_UNKNOWN = 37
    BINDSTATUS_COOKIE_STATE_ACCEPT = 38
    BINDSTATUS_COOKIE_STATE_REJECT = 39
    BINDSTATUS_COOKIE_STATE_PROMPT = 40
    BINDSTATUS_COOKIE_STATE_LEASH = 41
    BINDSTATUS_COOKIE_STATE_DOWNGRADE = 42
    BINDSTATUS_POLICY_HREF = 43
    BINDSTATUS_P3P_HEADER = 44
    BINDSTATUS_SESSION_COOKIE_RECEIVED = 45
    BINDSTATUS_PERSISTENT_COOKIE_RECEIVED = 46
    BINDSTATUS_SESSION_COOKIES_ALLOWED = 47
    BINDSTATUS_CACHECONTROL = 48
    BINDSTATUS_CONTENTDISPOSITIONFILENAME = 49
    BINDSTATUS_MIMETEXTPLAINMISMATCH = 50
    BINDSTATUS_PUBLISHERAVAILABLE = 51
    BINDSTATUS_DISPLAYNAMEAVAILABLE = 52
    BINDSTATUS_SSLUX_NAVBLOCKED = 53
    BINDSTATUS_SERVER_MIMETYPEAVAILABLE = 54
    BINDSTATUS_SNIFFED_CLASSIDAVAILABLE = 55
    BINDSTATUS_64BIT_PROGRESS = 56
    tagBINDSTATUS = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagBINDSTRING'
    tagBINDSTRING__enumvalues = {
        1: 'BINDSTRING_HEADERS',
        2: 'BINDSTRING_ACCEPT_MIMES',
        3: 'BINDSTRING_EXTRA_URL',
        4: 'BINDSTRING_LANGUAGE',
        5: 'BINDSTRING_USERNAME',
        6: 'BINDSTRING_PASSWORD',
        7: 'BINDSTRING_UA_PIXELS',
        8: 'BINDSTRING_UA_COLOR',
        9: 'BINDSTRING_OS',
        10: 'BINDSTRING_USER_AGENT',
        11: 'BINDSTRING_ACCEPT_ENCODINGS',
        12: 'BINDSTRING_POST_COOKIE',
        13: 'BINDSTRING_POST_DATA_MIME',
        14: 'BINDSTRING_URL',
        15: 'BINDSTRING_IID',
        16: 'BINDSTRING_FLAG_BIND_TO_OBJECT',
        17: 'BINDSTRING_PTR_BIND_CONTEXT',
        18: 'BINDSTRING_XDR_ORIGIN',
    }
    BINDSTRING_HEADERS = 1
    BINDSTRING_ACCEPT_MIMES = 2
    BINDSTRING_EXTRA_URL = 3
    BINDSTRING_LANGUAGE = 4
    BINDSTRING_USERNAME = 5
    BINDSTRING_PASSWORD = 6
    BINDSTRING_UA_PIXELS = 7
    BINDSTRING_UA_COLOR = 8
    BINDSTRING_OS = 9
    BINDSTRING_USER_AGENT = 10
    BINDSTRING_ACCEPT_ENCODINGS = 11
    BINDSTRING_POST_COOKIE = 12
    BINDSTRING_POST_DATA_MIME = 13
    BINDSTRING_URL = 14
    BINDSTRING_IID = 15
    BINDSTRING_FLAG_BIND_TO_OBJECT = 16
    BINDSTRING_PTR_BIND_CONTEXT = 17
    BINDSTRING_XDR_ORIGIN = 18
    tagBINDSTRING = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagCHANGEKIND'
    tagCHANGEKIND__enumvalues = {
        0: 'CHANGEKIND_ADDMEMBER',
        1: 'CHANGEKIND_DELETEMEMBER',
        2: 'CHANGEKIND_SETNAMES',
        3: 'CHANGEKIND_SETDOCUMENTATION',
        4: 'CHANGEKIND_GENERAL',
        5: 'CHANGEKIND_INVALIDATE',
        6: 'CHANGEKIND_CHANGEFAILED',
        7: 'CHANGEKIND_MAX',
    }
    CHANGEKIND_ADDMEMBER = 0
    CHANGEKIND_DELETEMEMBER = 1
    CHANGEKIND_SETNAMES = 2
    CHANGEKIND_SETDOCUMENTATION = 3
    CHANGEKIND_GENERAL = 4
    CHANGEKIND_INVALIDATE = 5
    CHANGEKIND_CHANGEFAILED = 6
    CHANGEKIND_MAX = 7
    tagCHANGEKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagExtentMode'
    tagExtentMode__enumvalues = {
        0: 'DVEXTENT_CONTENT',
        1: 'DVEXTENT_INTEGRAL',
    }
    DVEXTENT_CONTENT = 0
    DVEXTENT_INTEGRAL = 1
    tagExtentMode = ctypes.c_uint32 # enum
    
    # values for enumeration 'undo_event_t'
    undo_event_t__enumvalues = {
        2: 'START_UNDO',
        4: 'END_UNDO',
        0: 'CREATING_UNDO_POINT',
        2: 'STARTING_UNDO',
        3: 'STARTING_REDO',
        4: 'ENDING_UNDO',
        5: 'ENDING_REDO',
    }
    START_UNDO = 2
    END_UNDO = 4
    CREATING_UNDO_POINT = 0
    STARTING_UNDO = 2
    STARTING_REDO = 3
    ENDING_UNDO = 4
    ENDING_REDO = 5
    undo_event_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'undo_param_t'
    undo_param_t__enumvalues = {
        0: 'UNDO_ENABLED',
        1: 'UNDO_MAXSIZE',
        2: 'UNDO_DEPTH',
        3: 'UNDO_DURING_AA',
    }
    UNDO_ENABLED = 0
    UNDO_MAXSIZE = 1
    UNDO_DEPTH = 2
    UNDO_DURING_AA = 3
    undo_param_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'undo_state_t'
    undo_state_t__enumvalues = {
        0: 'UNDO_NOT_REPLAYING',
        1: 'UNDO_STARTING_REPLAYING',
        2: 'UNDO_REPLAYING',
    }
    UNDO_NOT_REPLAYING = 0
    UNDO_STARTING_REPLAYING = 1
    UNDO_REPLAYING = 2
    undo_state_t = ctypes.c_uint32 # enum
    
    # values for enumeration '_URLZONEREG'
    _URLZONEREG__enumvalues = {
        0: 'URLZONEREG_DEFAULT',
        1: 'URLZONEREG_HKLM',
        2: 'URLZONEREG_HKCU',
    }
    URLZONEREG_DEFAULT = 0
    URLZONEREG_HKLM = 1
    URLZONEREG_HKCU = 2
    _URLZONEREG = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagCALLCONV'
    tagCALLCONV__enumvalues = {
        0: 'CC_FASTCALL',
        1: 'CC_CDECL',
        2: 'CC_MSCPASCAL',
        2: 'CC_PASCAL',
        3: 'CC_MACPASCAL',
        4: 'CC_STDCALL',
        5: 'CC_FPFASTCALL',
        6: 'CC_SYSCALL',
        7: 'CC_MPWCDECL',
        8: 'CC_MPWPASCAL',
        9: 'CC_MAX',
    }
    CC_FASTCALL = 0
    CC_CDECL = 1
    CC_MSCPASCAL = 2
    CC_PASCAL = 2
    CC_MACPASCAL = 3
    CC_STDCALL = 4
    CC_FPFASTCALL = 5
    CC_SYSCALL = 6
    CC_MPWCDECL = 7
    CC_MPWPASCAL = 8
    CC_MAX = 9
    tagCALLCONV = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagDESCKIND'
    tagDESCKIND__enumvalues = {
        0: 'DESCKIND_NONE',
        1: 'DESCKIND_FUNCDESC',
        2: 'DESCKIND_VARDESC',
        3: 'DESCKIND_TYPECOMP',
        4: 'DESCKIND_IMPLICITAPPOBJ',
        5: 'DESCKIND_MAX',
    }
    DESCKIND_NONE = 0
    DESCKIND_FUNCDESC = 1
    DESCKIND_VARDESC = 2
    DESCKIND_TYPECOMP = 3
    DESCKIND_IMPLICITAPPOBJ = 4
    DESCKIND_MAX = 5
    tagDESCKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagFUNCKIND'
    tagFUNCKIND__enumvalues = {
        0: 'FUNC_VIRTUAL',
        1: 'FUNC_PUREVIRTUAL',
        2: 'FUNC_NONVIRTUAL',
        3: 'FUNC_STATIC',
        4: 'FUNC_DISPATCH',
    }
    FUNC_VIRTUAL = 0
    FUNC_PUREVIRTUAL = 1
    FUNC_NONVIRTUAL = 2
    FUNC_STATIC = 3
    FUNC_DISPATCH = 4
    tagFUNCKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagTYPEKIND'
    tagTYPEKIND__enumvalues = {
        0: 'TKIND_ENUM',
        1: 'TKIND_RECORD',
        2: 'TKIND_MODULE',
        3: 'TKIND_INTERFACE',
        4: 'TKIND_DISPATCH',
        5: 'TKIND_COCLASS',
        6: 'TKIND_ALIAS',
        7: 'TKIND_UNION',
        8: 'TKIND_MAX',
    }
    TKIND_ENUM = 0
    TKIND_RECORD = 1
    TKIND_MODULE = 2
    TKIND_INTERFACE = 3
    TKIND_DISPATCH = 4
    TKIND_COCLASS = 5
    TKIND_ALIAS = 6
    TKIND_UNION = 7
    TKIND_MAX = 8
    tagTYPEKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'MARKUPSIZE'
    MARKUPSIZE__enumvalues = {
        0: 'MARKUPSIZE_CALCWIDTH',
        1: 'MARKUPSIZE_CALCHEIGHT',
    }
    MARKUPSIZE_CALCWIDTH = 0
    MARKUPSIZE_CALCHEIGHT = 1
    MARKUPSIZE = ctypes.c_uint32 # enum
    
    # values for enumeration '__CT_flags'
    __CT_flags__enumvalues = {
        1: 'CT_IsSimpleType',
        2: 'CT_ByReferenceOnly',
        4: 'CT_HasVirtualBase',
        8: 'CT_IsWinRTHandle',
        16: 'CT_IsStdBadAlloc',
    }
    CT_IsSimpleType = 1
    CT_ByReferenceOnly = 2
    CT_HasVirtualBase = 4
    CT_IsWinRTHandle = 8
    CT_IsStdBadAlloc = 16
    __CT_flags = ctypes.c_uint32 # enum
    
    # values for enumeration '__TI_flags'
    __TI_flags__enumvalues = {
        1: 'TI_IsConst',
        2: 'TI_IsVolatile',
        4: 'TI_IsUnaligned',
        8: 'TI_IsPure',
        16: 'TI_IsWinRT',
    }
    TI_IsConst = 1
    TI_IsVolatile = 2
    TI_IsUnaligned = 4
    TI_IsPure = 8
    TI_IsWinRT = 16
    __TI_flags = ctypes.c_uint32 # enum
    
    # values for enumeration 'cp_block_t'
    cp_block_t__enumvalues = {
        0: 'CPB_Unknown',
        1: 'CPB_Adlam',
        2: 'CPB_Aegean_Numbers',
        3: 'CPB_Ahom',
        4: 'CPB_Alchemical_Symbols',
        5: 'CPB_Alphabetic_Presentation_Forms',
        6: 'CPB_Anatolian_Hieroglyphs',
        7: 'CPB_Ancient_Greek_Musical_Notation',
        8: 'CPB_Ancient_Greek_Numbers',
        9: 'CPB_Ancient_Symbols',
        10: 'CPB_Arabic',
        11: 'CPB_Arabic_Extended_A',
        12: 'CPB_Arabic_Mathematical_Alphabetic_Symbols',
        13: 'CPB_Arabic_Presentation_Forms_A',
        14: 'CPB_Arabic_Presentation_Forms_B',
        15: 'CPB_Arabic_Supplement',
        16: 'CPB_Armenian',
        17: 'CPB_Arrows',
        18: 'CPB_Avestan',
        19: 'CPB_Balinese',
        20: 'CPB_Bamum',
        21: 'CPB_Bamum_Supplement',
        22: 'CPB_Basic_Latin',
        23: 'CPB_Bassa_Vah',
        24: 'CPB_Batak',
        25: 'CPB_Bengali',
        26: 'CPB_Bhaiksuki',
        27: 'CPB_Block_Elements',
        28: 'CPB_Bopomofo',
        29: 'CPB_Bopomofo_Extended',
        30: 'CPB_Box_Drawing',
        31: 'CPB_Brahmi',
        32: 'CPB_Braille_Patterns',
        33: 'CPB_Buginese',
        34: 'CPB_Buhid',
        35: 'CPB_Byzantine_Musical_Symbols',
        36: 'CPB_CJK_Compatibility',
        37: 'CPB_CJK_Compatibility_Forms',
        38: 'CPB_CJK_Compatibility_Ideographs',
        39: 'CPB_CJK_Compatibility_Ideographs_Supplement',
        40: 'CPB_CJK_Radicals_Supplement',
        41: 'CPB_CJK_Strokes',
        42: 'CPB_CJK_Symbols_and_Punctuation',
        43: 'CPB_CJK_Unified_Ideographs',
        44: 'CPB_CJK_Unified_Ideographs_Extension_A',
        45: 'CPB_CJK_Unified_Ideographs_Extension_B',
        46: 'CPB_CJK_Unified_Ideographs_Extension_C',
        47: 'CPB_CJK_Unified_Ideographs_Extension_D',
        48: 'CPB_CJK_Unified_Ideographs_Extension_E',
        49: 'CPB_Carian',
        50: 'CPB_Caucasian_Albanian',
        51: 'CPB_Chakma',
        52: 'CPB_Cham',
        53: 'CPB_Cherokee',
        54: 'CPB_Cherokee_Supplement',
        55: 'CPB_Combining_Diacritical_Marks',
        56: 'CPB_Combining_Diacritical_Marks_Extended',
        57: 'CPB_Combining_Diacritical_Marks_Supplement',
        58: 'CPB_Combining_Diacritical_Marks_for_Symbols',
        59: 'CPB_Combining_Half_Marks',
        60: 'CPB_Common_Indic_Number_Forms',
        61: 'CPB_Control_Pictures',
        62: 'CPB_Coptic',
        63: 'CPB_Coptic_Epact_Numbers',
        64: 'CPB_Counting_Rod_Numerals',
        65: 'CPB_Cuneiform',
        66: 'CPB_Cuneiform_Numbers_and_Punctuation',
        67: 'CPB_Currency_Symbols',
        68: 'CPB_Cypriot_Syllabary',
        69: 'CPB_Cyrillic',
        70: 'CPB_Cyrillic_Extended_A',
        71: 'CPB_Cyrillic_Extended_B',
        72: 'CPB_Cyrillic_Extended_C',
        73: 'CPB_Cyrillic_Supplement',
        74: 'CPB_Deseret',
        75: 'CPB_Devanagari',
        76: 'CPB_Devanagari_Extended',
        77: 'CPB_Dingbats',
        78: 'CPB_Domino_Tiles',
        79: 'CPB_Duployan',
        80: 'CPB_Early_Dynastic_Cuneiform',
        81: 'CPB_Egyptian_Hieroglyphs',
        82: 'CPB_Elbasan',
        83: 'CPB_Emoticons',
        84: 'CPB_Enclosed_Alphanumeric_Supplement',
        85: 'CPB_Enclosed_Alphanumerics',
        86: 'CPB_Enclosed_CJK_Letters_and_Months',
        87: 'CPB_Enclosed_Ideographic_Supplement',
        88: 'CPB_Ethiopic',
        89: 'CPB_Ethiopic_Extended',
        90: 'CPB_Ethiopic_Extended_A',
        91: 'CPB_Ethiopic_Supplement',
        92: 'CPB_General_Punctuation',
        93: 'CPB_Geometric_Shapes',
        94: 'CPB_Geometric_Shapes_Extended',
        95: 'CPB_Georgian',
        96: 'CPB_Georgian_Supplement',
        97: 'CPB_Glagolitic',
        98: 'CPB_Glagolitic_Supplement',
        99: 'CPB_Gothic',
        100: 'CPB_Grantha',
        101: 'CPB_Greek_Extended',
        102: 'CPB_Greek_and_Coptic',
        103: 'CPB_Gujarati',
        104: 'CPB_Gurmukhi',
        105: 'CPB_Halfwidth_and_Fullwidth_Forms',
        106: 'CPB_Hangul_Compatibility_Jamo',
        107: 'CPB_Hangul_Jamo',
        108: 'CPB_Hangul_Jamo_Extended_A',
        109: 'CPB_Hangul_Jamo_Extended_B',
        110: 'CPB_Hangul_Syllables',
        111: 'CPB_Hanunoo',
        112: 'CPB_Hatran',
        113: 'CPB_Hebrew',
        114: 'CPB_High_Private_Use_Surrogates',
        115: 'CPB_High_Surrogates',
        116: 'CPB_Hiragana',
        117: 'CPB_IPA_Extensions',
        118: 'CPB_Ideographic_Description_Characters',
        119: 'CPB_Ideographic_Symbols_and_Punctuation',
        120: 'CPB_Imperial_Aramaic',
        121: 'CPB_Inscriptional_Pahlavi',
        122: 'CPB_Inscriptional_Parthian',
        123: 'CPB_Javanese',
        124: 'CPB_Kaithi',
        125: 'CPB_Kana_Supplement',
        126: 'CPB_Kanbun',
        127: 'CPB_Kangxi_Radicals',
        128: 'CPB_Kannada',
        129: 'CPB_Katakana',
        130: 'CPB_Katakana_Phonetic_Extensions',
        131: 'CPB_Kayah_Li',
        132: 'CPB_Kharoshthi',
        133: 'CPB_Khmer',
        134: 'CPB_Khmer_Symbols',
        135: 'CPB_Khojki',
        136: 'CPB_Khudawadi',
        137: 'CPB_Lao',
        138: 'CPB_Latin_Extended_Additional',
        139: 'CPB_Latin_Extended_A',
        140: 'CPB_Latin_Extended_B',
        141: 'CPB_Latin_Extended_C',
        142: 'CPB_Latin_Extended_D',
        143: 'CPB_Latin_Extended_E',
        144: 'CPB_Latin_1_Supplement',
        145: 'CPB_Lepcha',
        146: 'CPB_Letterlike_Symbols',
        147: 'CPB_Limbu',
        148: 'CPB_Linear_A',
        149: 'CPB_Linear_B_Ideograms',
        150: 'CPB_Linear_B_Syllabary',
        151: 'CPB_Lisu',
        152: 'CPB_Low_Surrogates',
        153: 'CPB_Lycian',
        154: 'CPB_Lydian',
        155: 'CPB_Mahajani',
        156: 'CPB_Mahjong_Tiles',
        157: 'CPB_Malayalam',
        158: 'CPB_Mandaic',
        159: 'CPB_Manichaean',
        160: 'CPB_Marchen',
        161: 'CPB_Mathematical_Alphanumeric_Symbols',
        162: 'CPB_Mathematical_Operators',
        163: 'CPB_Meetei_Mayek',
        164: 'CPB_Meetei_Mayek_Extensions',
        165: 'CPB_Mende_Kikakui',
        166: 'CPB_Meroitic_Cursive',
        167: 'CPB_Meroitic_Hieroglyphs',
        168: 'CPB_Miao',
        169: 'CPB_Miscellaneous_Mathematical_Symbols_A',
        170: 'CPB_Miscellaneous_Mathematical_Symbols_B',
        171: 'CPB_Miscellaneous_Symbols',
        172: 'CPB_Miscellaneous_Symbols_and_Arrows',
        173: 'CPB_Miscellaneous_Symbols_and_Pictographs',
        174: 'CPB_Miscellaneous_Technical',
        175: 'CPB_Modi',
        176: 'CPB_Modifier_Tone_Letters',
        177: 'CPB_Mongolian',
        178: 'CPB_Mongolian_Supplement',
        179: 'CPB_Mro',
        180: 'CPB_Multani',
        181: 'CPB_Musical_Symbols',
        182: 'CPB_Myanmar',
        183: 'CPB_Myanmar_Extended_A',
        184: 'CPB_Myanmar_Extended_B',
        185: 'CPB_NKo',
        186: 'CPB_Nabataean',
        187: 'CPB_New_Tai_Lue',
        188: 'CPB_Newa',
        189: 'CPB_Number_Forms',
        190: 'CPB_Ogham',
        191: 'CPB_Ol_Chiki',
        192: 'CPB_Old_Hungarian',
        193: 'CPB_Old_Italic',
        194: 'CPB_Old_North_Arabian',
        195: 'CPB_Old_Permic',
        196: 'CPB_Old_Persian',
        197: 'CPB_Old_South_Arabian',
        198: 'CPB_Old_Turkic',
        199: 'CPB_Optical_Character_Recognition',
        200: 'CPB_Oriya',
        201: 'CPB_Ornamental_Dingbats',
        202: 'CPB_Osage',
        203: 'CPB_Osmanya',
        204: 'CPB_Pahawh_Hmong',
        205: 'CPB_Palmyrene',
        206: 'CPB_Pau_Cin_Hau',
        207: 'CPB_Phags_pa',
        208: 'CPB_Phaistos_Disc',
        209: 'CPB_Phoenician',
        210: 'CPB_Phonetic_Extensions',
        211: 'CPB_Phonetic_Extensions_Supplement',
        212: 'CPB_Playing_Cards',
        213: 'CPB_Private_Use_Area',
        214: 'CPB_Psalter_Pahlavi',
        215: 'CPB_Rejang',
        216: 'CPB_Rumi_Numeral_Symbols',
        217: 'CPB_Runic',
        218: 'CPB_Samaritan',
        219: 'CPB_Saurashtra',
        220: 'CPB_Sharada',
        221: 'CPB_Shavian',
        222: 'CPB_Shorthand_Format_Controls',
        223: 'CPB_Siddham',
        224: 'CPB_Sinhala',
        225: 'CPB_Sinhala_Archaic_Numbers',
        226: 'CPB_Small_Form_Variants',
        227: 'CPB_Sora_Sompeng',
        228: 'CPB_Spacing_Modifier_Letters',
        229: 'CPB_Specials',
        230: 'CPB_Sundanese',
        231: 'CPB_Sundanese_Supplement',
        232: 'CPB_Superscripts_and_Subscripts',
        233: 'CPB_Supplemental_Arrows_A',
        234: 'CPB_Supplemental_Arrows_B',
        235: 'CPB_Supplemental_Arrows_C',
        236: 'CPB_Supplemental_Mathematical_Operators',
        237: 'CPB_Supplemental_Punctuation',
        238: 'CPB_Supplemental_Symbols_and_Pictographs',
        239: 'CPB_Supplementary_Private_Use_Area_A',
        240: 'CPB_Supplementary_Private_Use_Area_B',
        241: 'CPB_Sutton_SignWriting',
        242: 'CPB_Syloti_Nagri',
        243: 'CPB_Syriac',
        244: 'CPB_Tagalog',
        245: 'CPB_Tagbanwa',
        246: 'CPB_Tags',
        247: 'CPB_Tai_Le',
        248: 'CPB_Tai_Tham',
        249: 'CPB_Tai_Viet',
        250: 'CPB_Tai_Xuan_Jing_Symbols',
        251: 'CPB_Takri',
        252: 'CPB_Tamil',
        253: 'CPB_Tangut',
        254: 'CPB_Tangut_Components',
        255: 'CPB_Telugu',
        256: 'CPB_Thaana',
        257: 'CPB_Thai',
        258: 'CPB_Tibetan',
        259: 'CPB_Tifinagh',
        260: 'CPB_Tirhuta',
        261: 'CPB_Transport_and_Map_Symbols',
        262: 'CPB_Ugaritic',
        263: 'CPB_Unified_Canadian_Aboriginal_Syllabics',
        264: 'CPB_Unified_Canadian_Aboriginal_Syllabics_Extended',
        265: 'CPB_Vai',
        266: 'CPB_Variation_Selectors',
        267: 'CPB_Variation_Selectors_Supplement',
        268: 'CPB_Vedic_Extensions',
        269: 'CPB_Vertical_Forms',
        270: 'CPB_Warang_Citi',
        271: 'CPB_Yi_Radicals',
        272: 'CPB_Yi_Syllables',
        273: 'CPB_Yijing_Hexagram_Symbols',
        273: 'CPB_last',
    }
    CPB_Unknown = 0
    CPB_Adlam = 1
    CPB_Aegean_Numbers = 2
    CPB_Ahom = 3
    CPB_Alchemical_Symbols = 4
    CPB_Alphabetic_Presentation_Forms = 5
    CPB_Anatolian_Hieroglyphs = 6
    CPB_Ancient_Greek_Musical_Notation = 7
    CPB_Ancient_Greek_Numbers = 8
    CPB_Ancient_Symbols = 9
    CPB_Arabic = 10
    CPB_Arabic_Extended_A = 11
    CPB_Arabic_Mathematical_Alphabetic_Symbols = 12
    CPB_Arabic_Presentation_Forms_A = 13
    CPB_Arabic_Presentation_Forms_B = 14
    CPB_Arabic_Supplement = 15
    CPB_Armenian = 16
    CPB_Arrows = 17
    CPB_Avestan = 18
    CPB_Balinese = 19
    CPB_Bamum = 20
    CPB_Bamum_Supplement = 21
    CPB_Basic_Latin = 22
    CPB_Bassa_Vah = 23
    CPB_Batak = 24
    CPB_Bengali = 25
    CPB_Bhaiksuki = 26
    CPB_Block_Elements = 27
    CPB_Bopomofo = 28
    CPB_Bopomofo_Extended = 29
    CPB_Box_Drawing = 30
    CPB_Brahmi = 31
    CPB_Braille_Patterns = 32
    CPB_Buginese = 33
    CPB_Buhid = 34
    CPB_Byzantine_Musical_Symbols = 35
    CPB_CJK_Compatibility = 36
    CPB_CJK_Compatibility_Forms = 37
    CPB_CJK_Compatibility_Ideographs = 38
    CPB_CJK_Compatibility_Ideographs_Supplement = 39
    CPB_CJK_Radicals_Supplement = 40
    CPB_CJK_Strokes = 41
    CPB_CJK_Symbols_and_Punctuation = 42
    CPB_CJK_Unified_Ideographs = 43
    CPB_CJK_Unified_Ideographs_Extension_A = 44
    CPB_CJK_Unified_Ideographs_Extension_B = 45
    CPB_CJK_Unified_Ideographs_Extension_C = 46
    CPB_CJK_Unified_Ideographs_Extension_D = 47
    CPB_CJK_Unified_Ideographs_Extension_E = 48
    CPB_Carian = 49
    CPB_Caucasian_Albanian = 50
    CPB_Chakma = 51
    CPB_Cham = 52
    CPB_Cherokee = 53
    CPB_Cherokee_Supplement = 54
    CPB_Combining_Diacritical_Marks = 55
    CPB_Combining_Diacritical_Marks_Extended = 56
    CPB_Combining_Diacritical_Marks_Supplement = 57
    CPB_Combining_Diacritical_Marks_for_Symbols = 58
    CPB_Combining_Half_Marks = 59
    CPB_Common_Indic_Number_Forms = 60
    CPB_Control_Pictures = 61
    CPB_Coptic = 62
    CPB_Coptic_Epact_Numbers = 63
    CPB_Counting_Rod_Numerals = 64
    CPB_Cuneiform = 65
    CPB_Cuneiform_Numbers_and_Punctuation = 66
    CPB_Currency_Symbols = 67
    CPB_Cypriot_Syllabary = 68
    CPB_Cyrillic = 69
    CPB_Cyrillic_Extended_A = 70
    CPB_Cyrillic_Extended_B = 71
    CPB_Cyrillic_Extended_C = 72
    CPB_Cyrillic_Supplement = 73
    CPB_Deseret = 74
    CPB_Devanagari = 75
    CPB_Devanagari_Extended = 76
    CPB_Dingbats = 77
    CPB_Domino_Tiles = 78
    CPB_Duployan = 79
    CPB_Early_Dynastic_Cuneiform = 80
    CPB_Egyptian_Hieroglyphs = 81
    CPB_Elbasan = 82
    CPB_Emoticons = 83
    CPB_Enclosed_Alphanumeric_Supplement = 84
    CPB_Enclosed_Alphanumerics = 85
    CPB_Enclosed_CJK_Letters_and_Months = 86
    CPB_Enclosed_Ideographic_Supplement = 87
    CPB_Ethiopic = 88
    CPB_Ethiopic_Extended = 89
    CPB_Ethiopic_Extended_A = 90
    CPB_Ethiopic_Supplement = 91
    CPB_General_Punctuation = 92
    CPB_Geometric_Shapes = 93
    CPB_Geometric_Shapes_Extended = 94
    CPB_Georgian = 95
    CPB_Georgian_Supplement = 96
    CPB_Glagolitic = 97
    CPB_Glagolitic_Supplement = 98
    CPB_Gothic = 99
    CPB_Grantha = 100
    CPB_Greek_Extended = 101
    CPB_Greek_and_Coptic = 102
    CPB_Gujarati = 103
    CPB_Gurmukhi = 104
    CPB_Halfwidth_and_Fullwidth_Forms = 105
    CPB_Hangul_Compatibility_Jamo = 106
    CPB_Hangul_Jamo = 107
    CPB_Hangul_Jamo_Extended_A = 108
    CPB_Hangul_Jamo_Extended_B = 109
    CPB_Hangul_Syllables = 110
    CPB_Hanunoo = 111
    CPB_Hatran = 112
    CPB_Hebrew = 113
    CPB_High_Private_Use_Surrogates = 114
    CPB_High_Surrogates = 115
    CPB_Hiragana = 116
    CPB_IPA_Extensions = 117
    CPB_Ideographic_Description_Characters = 118
    CPB_Ideographic_Symbols_and_Punctuation = 119
    CPB_Imperial_Aramaic = 120
    CPB_Inscriptional_Pahlavi = 121
    CPB_Inscriptional_Parthian = 122
    CPB_Javanese = 123
    CPB_Kaithi = 124
    CPB_Kana_Supplement = 125
    CPB_Kanbun = 126
    CPB_Kangxi_Radicals = 127
    CPB_Kannada = 128
    CPB_Katakana = 129
    CPB_Katakana_Phonetic_Extensions = 130
    CPB_Kayah_Li = 131
    CPB_Kharoshthi = 132
    CPB_Khmer = 133
    CPB_Khmer_Symbols = 134
    CPB_Khojki = 135
    CPB_Khudawadi = 136
    CPB_Lao = 137
    CPB_Latin_Extended_Additional = 138
    CPB_Latin_Extended_A = 139
    CPB_Latin_Extended_B = 140
    CPB_Latin_Extended_C = 141
    CPB_Latin_Extended_D = 142
    CPB_Latin_Extended_E = 143
    CPB_Latin_1_Supplement = 144
    CPB_Lepcha = 145
    CPB_Letterlike_Symbols = 146
    CPB_Limbu = 147
    CPB_Linear_A = 148
    CPB_Linear_B_Ideograms = 149
    CPB_Linear_B_Syllabary = 150
    CPB_Lisu = 151
    CPB_Low_Surrogates = 152
    CPB_Lycian = 153
    CPB_Lydian = 154
    CPB_Mahajani = 155
    CPB_Mahjong_Tiles = 156
    CPB_Malayalam = 157
    CPB_Mandaic = 158
    CPB_Manichaean = 159
    CPB_Marchen = 160
    CPB_Mathematical_Alphanumeric_Symbols = 161
    CPB_Mathematical_Operators = 162
    CPB_Meetei_Mayek = 163
    CPB_Meetei_Mayek_Extensions = 164
    CPB_Mende_Kikakui = 165
    CPB_Meroitic_Cursive = 166
    CPB_Meroitic_Hieroglyphs = 167
    CPB_Miao = 168
    CPB_Miscellaneous_Mathematical_Symbols_A = 169
    CPB_Miscellaneous_Mathematical_Symbols_B = 170
    CPB_Miscellaneous_Symbols = 171
    CPB_Miscellaneous_Symbols_and_Arrows = 172
    CPB_Miscellaneous_Symbols_and_Pictographs = 173
    CPB_Miscellaneous_Technical = 174
    CPB_Modi = 175
    CPB_Modifier_Tone_Letters = 176
    CPB_Mongolian = 177
    CPB_Mongolian_Supplement = 178
    CPB_Mro = 179
    CPB_Multani = 180
    CPB_Musical_Symbols = 181
    CPB_Myanmar = 182
    CPB_Myanmar_Extended_A = 183
    CPB_Myanmar_Extended_B = 184
    CPB_NKo = 185
    CPB_Nabataean = 186
    CPB_New_Tai_Lue = 187
    CPB_Newa = 188
    CPB_Number_Forms = 189
    CPB_Ogham = 190
    CPB_Ol_Chiki = 191
    CPB_Old_Hungarian = 192
    CPB_Old_Italic = 193
    CPB_Old_North_Arabian = 194
    CPB_Old_Permic = 195
    CPB_Old_Persian = 196
    CPB_Old_South_Arabian = 197
    CPB_Old_Turkic = 198
    CPB_Optical_Character_Recognition = 199
    CPB_Oriya = 200
    CPB_Ornamental_Dingbats = 201
    CPB_Osage = 202
    CPB_Osmanya = 203
    CPB_Pahawh_Hmong = 204
    CPB_Palmyrene = 205
    CPB_Pau_Cin_Hau = 206
    CPB_Phags_pa = 207
    CPB_Phaistos_Disc = 208
    CPB_Phoenician = 209
    CPB_Phonetic_Extensions = 210
    CPB_Phonetic_Extensions_Supplement = 211
    CPB_Playing_Cards = 212
    CPB_Private_Use_Area = 213
    CPB_Psalter_Pahlavi = 214
    CPB_Rejang = 215
    CPB_Rumi_Numeral_Symbols = 216
    CPB_Runic = 217
    CPB_Samaritan = 218
    CPB_Saurashtra = 219
    CPB_Sharada = 220
    CPB_Shavian = 221
    CPB_Shorthand_Format_Controls = 222
    CPB_Siddham = 223
    CPB_Sinhala = 224
    CPB_Sinhala_Archaic_Numbers = 225
    CPB_Small_Form_Variants = 226
    CPB_Sora_Sompeng = 227
    CPB_Spacing_Modifier_Letters = 228
    CPB_Specials = 229
    CPB_Sundanese = 230
    CPB_Sundanese_Supplement = 231
    CPB_Superscripts_and_Subscripts = 232
    CPB_Supplemental_Arrows_A = 233
    CPB_Supplemental_Arrows_B = 234
    CPB_Supplemental_Arrows_C = 235
    CPB_Supplemental_Mathematical_Operators = 236
    CPB_Supplemental_Punctuation = 237
    CPB_Supplemental_Symbols_and_Pictographs = 238
    CPB_Supplementary_Private_Use_Area_A = 239
    CPB_Supplementary_Private_Use_Area_B = 240
    CPB_Sutton_SignWriting = 241
    CPB_Syloti_Nagri = 242
    CPB_Syriac = 243
    CPB_Tagalog = 244
    CPB_Tagbanwa = 245
    CPB_Tags = 246
    CPB_Tai_Le = 247
    CPB_Tai_Tham = 248
    CPB_Tai_Viet = 249
    CPB_Tai_Xuan_Jing_Symbols = 250
    CPB_Takri = 251
    CPB_Tamil = 252
    CPB_Tangut = 253
    CPB_Tangut_Components = 254
    CPB_Telugu = 255
    CPB_Thaana = 256
    CPB_Thai = 257
    CPB_Tibetan = 258
    CPB_Tifinagh = 259
    CPB_Tirhuta = 260
    CPB_Transport_and_Map_Symbols = 261
    CPB_Ugaritic = 262
    CPB_Unified_Canadian_Aboriginal_Syllabics = 263
    CPB_Unified_Canadian_Aboriginal_Syllabics_Extended = 264
    CPB_Vai = 265
    CPB_Variation_Selectors = 266
    CPB_Variation_Selectors_Supplement = 267
    CPB_Vedic_Extensions = 268
    CPB_Vertical_Forms = 269
    CPB_Warang_Citi = 270
    CPB_Yi_Radicals = 271
    CPB_Yi_Syllables = 272
    CPB_Yijing_Hexagram_Symbols = 273
    CPB_last = 273
    cp_block_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagSYSKIND'
    tagSYSKIND__enumvalues = {
        0: 'SYS_WIN16',
        1: 'SYS_WIN32',
        2: 'SYS_MAC',
        3: 'SYS_WIN64',
    }
    SYS_WIN16 = 0
    SYS_WIN32 = 1
    SYS_MAC = 2
    SYS_WIN64 = 3
    tagSYSKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagURLZONE'
    tagURLZONE__enumvalues = {
        4294967295: 'URLZONE_INVALID',
        0: 'URLZONE_PREDEFINED_MIN',
        0: 'URLZONE_LOCAL_MACHINE',
        1: 'URLZONE_INTRANET',
        2: 'URLZONE_TRUSTED',
        3: 'URLZONE_INTERNET',
        4: 'URLZONE_UNTRUSTED',
        999: 'URLZONE_PREDEFINED_MAX',
        1000: 'URLZONE_USER_MIN',
        10000: 'URLZONE_USER_MAX',
    }
    URLZONE_INVALID = 4294967295
    URLZONE_PREDEFINED_MIN = 0
    URLZONE_LOCAL_MACHINE = 0
    URLZONE_INTRANET = 1
    URLZONE_TRUSTED = 2
    URLZONE_INTERNET = 3
    URLZONE_UNTRUSTED = 4
    URLZONE_PREDEFINED_MAX = 999
    URLZONE_USER_MIN = 1000
    URLZONE_USER_MAX = 10000
    tagURLZONE = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagVARKIND'
    tagVARKIND__enumvalues = {
        0: 'VAR_PERINSTANCE',
        1: 'VAR_STATIC',
        2: 'VAR_CONST',
        3: 'VAR_DISPATCH',
    }
    VAR_PERINSTANCE = 0
    VAR_STATIC = 1
    VAR_CONST = 2
    VAR_DISPATCH = 3
    tagVARKIND = ctypes.c_uint32 # enum
    
    # values for enumeration 'FFFP_MODE'
    FFFP_MODE__enumvalues = {
        0: 'FFFP_EXACTMATCH',
        1: 'FFFP_NEARESTPARENTMATCH',
    }
    FFFP_EXACTMATCH = 0
    FFFP_NEARESTPARENTMATCH = 1
    FFFP_MODE = ctypes.c_uint32 # enum
    
    # values for enumeration 'PKA_FLAGS'
    PKA_FLAGS__enumvalues = {
        0: 'PKA_SET',
        1: 'PKA_APPEND',
        2: 'PKA_DELETE',
    }
    PKA_SET = 0
    PKA_APPEND = 1
    PKA_DELETE = 2
    PKA_FLAGS = ctypes.c_uint32 # enum
    
    # values for enumeration '_SPACTION'
    _SPACTION__enumvalues = {
        0: 'SPACTION_NONE',
        1: 'SPACTION_MOVING',
        2: 'SPACTION_COPYING',
        3: 'SPACTION_RECYCLING',
        4: 'SPACTION_APPLYINGATTRIBS',
        5: 'SPACTION_DOWNLOADING',
        6: 'SPACTION_SEARCHING_INTERNET',
        7: 'SPACTION_CALCULATING',
        8: 'SPACTION_UPLOADING',
        9: 'SPACTION_SEARCHING_FILES',
        10: 'SPACTION_DELETING',
        11: 'SPACTION_RENAMING',
        12: 'SPACTION_FORMATTING',
        13: 'SPACTION_COPY_MOVING',
    }
    SPACTION_NONE = 0
    SPACTION_MOVING = 1
    SPACTION_COPYING = 2
    SPACTION_RECYCLING = 3
    SPACTION_APPLYINGATTRIBS = 4
    SPACTION_DOWNLOADING = 5
    SPACTION_SEARCHING_INTERNET = 6
    SPACTION_CALCULATING = 7
    SPACTION_UPLOADING = 8
    SPACTION_SEARCHING_FILES = 9
    SPACTION_DELETING = 10
    SPACTION_RENAMING = 11
    SPACTION_FORMATTING = 12
    SPACTION_COPY_MOVING = 13
    _SPACTION = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagCLSCTX'
    tagCLSCTX__enumvalues = {
        1: 'CLSCTX_INPROC_SERVER',
        2: 'CLSCTX_INPROC_HANDLER',
        4: 'CLSCTX_LOCAL_SERVER',
        8: 'CLSCTX_INPROC_SERVER16',
        16: 'CLSCTX_REMOTE_SERVER',
        32: 'CLSCTX_INPROC_HANDLER16',
        64: 'CLSCTX_RESERVED1',
        128: 'CLSCTX_RESERVED2',
        256: 'CLSCTX_RESERVED3',
        512: 'CLSCTX_RESERVED4',
        1024: 'CLSCTX_NO_CODE_DOWNLOAD',
        2048: 'CLSCTX_RESERVED5',
        4096: 'CLSCTX_NO_CUSTOM_MARSHAL',
        8192: 'CLSCTX_ENABLE_CODE_DOWNLOAD',
        16384: 'CLSCTX_NO_FAILURE_LOG',
        32768: 'CLSCTX_DISABLE_AAA',
        65536: 'CLSCTX_ENABLE_AAA',
        131072: 'CLSCTX_FROM_DEFAULT_CONTEXT',
        262144: 'CLSCTX_ACTIVATE_32_BIT_SERVER',
        524288: 'CLSCTX_ACTIVATE_64_BIT_SERVER',
        1048576: 'CLSCTX_ENABLE_CLOAKING',
        2147483648: 'CLSCTX_PS_DLL',
    }
    CLSCTX_INPROC_SERVER = 1
    CLSCTX_INPROC_HANDLER = 2
    CLSCTX_LOCAL_SERVER = 4
    CLSCTX_INPROC_SERVER16 = 8
    CLSCTX_REMOTE_SERVER = 16
    CLSCTX_INPROC_HANDLER16 = 32
    CLSCTX_RESERVED1 = 64
    CLSCTX_RESERVED2 = 128
    CLSCTX_RESERVED3 = 256
    CLSCTX_RESERVED4 = 512
    CLSCTX_NO_CODE_DOWNLOAD = 1024
    CLSCTX_RESERVED5 = 2048
    CLSCTX_NO_CUSTOM_MARSHAL = 4096
    CLSCTX_ENABLE_CODE_DOWNLOAD = 8192
    CLSCTX_NO_FAILURE_LOG = 16384
    CLSCTX_DISABLE_AAA = 32768
    CLSCTX_ENABLE_AAA = 65536
    CLSCTX_FROM_DEFAULT_CONTEXT = 131072
    CLSCTX_ACTIVATE_32_BIT_SERVER = 262144
    CLSCTX_ACTIVATE_64_BIT_SERVER = 524288
    CLSCTX_ENABLE_CLOAKING = 1048576
    CLSCTX_PS_DLL = 2147483648
    tagCLSCTX = ctypes.c_uint32 # enum
    
    # values for enumeration 'tagTYSPEC'
    tagTYSPEC__enumvalues = {
        0: 'TYSPEC_CLSID',
        1: 'TYSPEC_FILEEXT',
        2: 'TYSPEC_MIMETYPE',
        3: 'TYSPEC_FILENAME',
        4: 'TYSPEC_PROGID',
        5: 'TYSPEC_PACKAGENAME',
        6: 'TYSPEC_OBJECTID',
    }
    TYSPEC_CLSID = 0
    TYSPEC_FILEEXT = 1
    TYSPEC_MIMETYPE = 2
    TYSPEC_FILENAME = 3
    TYSPEC_PROGID = 4
    TYSPEC_PACKAGENAME = 5
    TYSPEC_OBJECTID = 6
    tagTYSPEC = ctypes.c_uint32 # enum
    
    # values for enumeration 'codetype'
    codetype__enumvalues = {
        0: 'CODES',
        1: 'LENS',
        2: 'DISTS',
    }
    CODES = 0
    LENS = 1
    DISTS = 2
    codetype = ctypes.c_uint32 # enum
    
    # values for enumeration 'IPPROTO'
    IPPROTO__enumvalues = {
        0: 'IPPROTO_HOPOPTS',
        1: 'IPPROTO_ICMP',
        2: 'IPPROTO_IGMP',
        3: 'IPPROTO_GGP',
        4: 'IPPROTO_IPV4',
        5: 'IPPROTO_ST',
        6: 'IPPROTO_TCP',
        7: 'IPPROTO_CBT',
        8: 'IPPROTO_EGP',
        9: 'IPPROTO_IGP',
        12: 'IPPROTO_PUP',
        17: 'IPPROTO_UDP',
        22: 'IPPROTO_IDP',
        27: 'IPPROTO_RDP',
        41: 'IPPROTO_IPV6',
        43: 'IPPROTO_ROUTING',
        44: 'IPPROTO_FRAGMENT',
        50: 'IPPROTO_ESP',
        51: 'IPPROTO_AH',
        58: 'IPPROTO_ICMPV6',
        59: 'IPPROTO_NONE',
        60: 'IPPROTO_DSTOPTS',
        77: 'IPPROTO_ND',
        78: 'IPPROTO_ICLFXBM',
        103: 'IPPROTO_PIM',
        113: 'IPPROTO_PGM',
        115: 'IPPROTO_L2TP',
        132: 'IPPROTO_SCTP',
        255: 'IPPROTO_RAW',
        256: 'IPPROTO_MAX',
        257: 'IPPROTO_RESERVED_RAW',
        258: 'IPPROTO_RESERVED_IPSEC',
        259: 'IPPROTO_RESERVED_IPSECOFFLOAD',
        260: 'IPPROTO_RESERVED_MAX',
    }
    IPPROTO_HOPOPTS = 0
    IPPROTO_ICMP = 1
    IPPROTO_IGMP = 2
    IPPROTO_GGP = 3
    IPPROTO_IPV4 = 4
    IPPROTO_ST = 5
    IPPROTO_TCP = 6
    IPPROTO_CBT = 7
    IPPROTO_EGP = 8
    IPPROTO_IGP = 9
    IPPROTO_PUP = 12
    IPPROTO_UDP = 17
    IPPROTO_IDP = 22
    IPPROTO_RDP = 27
    IPPROTO_IPV6 = 41
    IPPROTO_ROUTING = 43
    IPPROTO_FRAGMENT = 44
    IPPROTO_ESP = 50
    IPPROTO_AH = 51
    IPPROTO_ICMPV6 = 58
    IPPROTO_NONE = 59
    IPPROTO_DSTOPTS = 60
    IPPROTO_ND = 77
    IPPROTO_ICLFXBM = 78
    IPPROTO_PIM = 103
    IPPROTO_PGM = 113
    IPPROTO_L2TP = 115
    IPPROTO_SCTP = 132
    IPPROTO_RAW = 255
    IPPROTO_MAX = 256
    IPPROTO_RESERVED_RAW = 257
    IPPROTO_RESERVED_IPSEC = 258
    IPPROTO_RESERVED_IPSECOFFLOAD = 259
    IPPROTO_RESERVED_MAX = 260
    IPPROTO = ctypes.c_uint32 # enum
    
    # values for enumeration 'VARENUM'
    VARENUM__enumvalues = {
        0: 'VT_EMPTY',
        1: 'VT_NULL',
        2: 'VT_I2',
        3: 'VT_I4',
        4: 'VT_R4',
        5: 'VT_R8',
        6: 'VT_CY',
        7: 'VT_DATE',
        8: 'VT_BSTR',
        9: 'VT_DISPATCH',
        10: 'VT_ERROR',
        11: 'VT_BOOL',
        12: 'VT_VARIANT',
        13: 'VT_UNKNOWN',
        14: 'VT_DECIMAL',
        16: 'VT_I1',
        17: 'VT_UI1',
        18: 'VT_UI2',
        19: 'VT_UI4',
        20: 'VT_I8',
        21: 'VT_UI8',
        22: 'VT_INT',
        23: 'VT_UINT',
        24: 'VT_VOID',
        25: 'VT_HRESULT',
        26: 'VT_PTR',
        27: 'VT_SAFEARRAY',
        28: 'VT_CARRAY',
        29: 'VT_USERDEFINED',
        30: 'VT_LPSTR',
        31: 'VT_LPWSTR',
        36: 'VT_RECORD',
        37: 'VT_INT_PTR',
        38: 'VT_UINT_PTR',
        64: 'VT_FILETIME',
        65: 'VT_BLOB',
        66: 'VT_STREAM',
        67: 'VT_STORAGE',
        68: 'VT_STREAMED_OBJECT',
        69: 'VT_STORED_OBJECT',
        70: 'VT_BLOB_OBJECT',
        71: 'VT_CF',
        72: 'VT_CLSID',
        73: 'VT_VERSIONED_STREAM',
        4095: 'VT_BSTR_BLOB',
        4096: 'VT_VECTOR',
        8192: 'VT_ARRAY',
        16384: 'VT_BYREF',
        32768: 'VT_RESERVED',
        65535: 'VT_ILLEGAL',
        4095: 'VT_ILLEGALMASKED',
        4095: 'VT_TYPEMASK',
    }
    VT_EMPTY = 0
    VT_NULL = 1
    VT_I2 = 2
    VT_I4 = 3
    VT_R4 = 4
    VT_R8 = 5
    VT_CY = 6
    VT_DATE = 7
    VT_BSTR = 8
    VT_DISPATCH = 9
    VT_ERROR = 10
    VT_BOOL = 11
    VT_VARIANT = 12
    VT_UNKNOWN = 13
    VT_DECIMAL = 14
    VT_I1 = 16
    VT_UI1 = 17
    VT_UI2 = 18
    VT_UI4 = 19
    VT_I8 = 20
    VT_UI8 = 21
    VT_INT = 22
    VT_UINT = 23
    VT_VOID = 24
    VT_HRESULT = 25
    VT_PTR = 26
    VT_SAFEARRAY = 27
    VT_CARRAY = 28
    VT_USERDEFINED = 29
    VT_LPSTR = 30
    VT_LPWSTR = 31
    VT_RECORD = 36
    VT_INT_PTR = 37
    VT_UINT_PTR = 38
    VT_FILETIME = 64
    VT_BLOB = 65
    VT_STREAM = 66
    VT_STORAGE = 67
    VT_STREAMED_OBJECT = 68
    VT_STORED_OBJECT = 69
    VT_BLOB_OBJECT = 70
    VT_CF = 71
    VT_CLSID = 72
    VT_VERSIONED_STREAM = 73
    VT_BSTR_BLOB = 4095
    VT_VECTOR = 4096
    VT_ARRAY = 8192
    VT_BYREF = 16384
    VT_RESERVED = 32768
    VT_ILLEGAL = 65535
    VT_ILLEGALMASKED = 4095
    VT_TYPEMASK = 4095
    VARENUM = ctypes.c_uint32 # enum
    
    # values for enumeration '_SPTEXT'
    _SPTEXT__enumvalues = {
        1: 'SPTEXT_ACTIONDESCRIPTION',
        2: 'SPTEXT_ACTIONDETAIL',
    }
    SPTEXT_ACTIONDESCRIPTION = 1
    SPTEXT_ACTIONDETAIL = 2
    _SPTEXT = ctypes.c_uint32 # enum
    
    # values for enumeration 'CPVIEW'
    CPVIEW__enumvalues = {
        0: 'CPVIEW_CLASSIC',
        0: 'CPVIEW_ALLITEMS',
        1: 'CPVIEW_CATEGORY',
        1: 'CPVIEW_HOME',
    }
    CPVIEW_CLASSIC = 0
    CPVIEW_ALLITEMS = 0
    CPVIEW_CATEGORY = 1
    CPVIEW_HOME = 1
    CPVIEW = ctypes.c_uint32 # enum
    
    # values for enumeration '_SIGDN'
    _SIGDN__enumvalues = {
        0: 'SIGDN_NORMALDISPLAY',
        2147581953: 'SIGDN_PARENTRELATIVEPARSING',
        2147647488: 'SIGDN_DESKTOPABSOLUTEPARSING',
        2147684353: 'SIGDN_PARENTRELATIVEEDITING',
        2147794944: 'SIGDN_DESKTOPABSOLUTEEDITING',
        2147844096: 'SIGDN_FILESYSPATH',
        2147909632: 'SIGDN_URL',
        2147991553: 'SIGDN_PARENTRELATIVEFORADDRESSBAR',
        2148007937: 'SIGDN_PARENTRELATIVE',
    }
    SIGDN_NORMALDISPLAY = 0
    SIGDN_PARENTRELATIVEPARSING = 2147581953
    SIGDN_DESKTOPABSOLUTEPARSING = 2147647488
    SIGDN_PARENTRELATIVEEDITING = 2147684353
    SIGDN_DESKTOPABSOLUTEEDITING = 2147794944
    SIGDN_FILESYSPATH = 2147844096
    SIGDN_URL = 2147909632
    SIGDN_PARENTRELATIVEFORADDRESSBAR = 2147991553
    SIGDN_PARENTRELATIVE = 2148007937
    _SIGDN = ctypes.c_uint32 # enum
    PMFN = ctypes.c_int32
    std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0______Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0______Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________________Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________________Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0______Redbl = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl
    std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0______Redbl__enumvalues = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl__enumvalues
    std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0______Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0______Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0______Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0______Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0______Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0______Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0______Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0______Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0______Redbl = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl
    std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0______Redbl__enumvalues = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl__enumvalues
    std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0______Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0______Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P________Redbl = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P________Redbl__enumvalues = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P________Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P________Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P________Redbl = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P________Redbl__enumvalues = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P________Redbl = std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P________Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P________Redbl = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P________Redbl__enumvalues = std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char____________Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char____________Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________Redbl = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________Redbl__enumvalues = std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64________Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64________Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char__________Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char__________Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P________Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P________Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____Redbl = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl
    std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____Redbl__enumvalues = std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl__enumvalues
    std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0______Redbl = std___Tree_node_int_void__P____Redbl
    std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0______Redbl__enumvalues = std___Tree_node_int_void__P____Redbl__enumvalues
    std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P________Redbl = std___Tree_node_int_void__P____Redbl
    std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P________Redbl__enumvalues = std___Tree_node_int_void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_char_const__P_const__P______Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_val_std___Tree_simple_types_char_const__P_const__P______Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_node_char_const__P_const__P_void__P____Redbl = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl
    std___Tree_node_char_const__P_const__P_void__P____Redbl__enumvalues = std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl__enumvalues
    std___Tree_val_std___Tree_simple_types_int______Redbl = std___Tree_node_int_void__P____Redbl
    std___Tree_val_std___Tree_simple_types_int______Redbl__enumvalues = std___Tree_node_int_void__P____Redbl__enumvalues
    class union__276C32F751912DA34557646A17DC8EC7(Union):
        pass
    
    union__276C32F751912DA34557646A17DC8EC7._pack_ = 1 # source:False
    union__276C32F751912DA34557646A17DC8EC7._fields_ = [
        ('addr', ctypes.c_uint64),
        ('addr_shorts', struct_op_t___unnamed_tag____unnamed_type_addr_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__33DC36BD25A1F06FF0DB9DC15CDFBE9B(Union):
        pass
    
    union__33DC36BD25A1F06FF0DB9DC15CDFBE9B._pack_ = 1 # source:False
    union__33DC36BD25A1F06FF0DB9DC15CDFBE9B._fields_ = [
        ('value', ctypes.c_uint64),
        ('value_shorts', struct_op_t___unnamed_tag____unnamed_type_value_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__5E8440A06A2AFEFEAE49F239CCFDFB49(Union):
        pass
    
    union__5E8440A06A2AFEFEAE49F239CCFDFB49._pack_ = 1 # source:False
    union__5E8440A06A2AFEFEAE49F239CCFDFB49._fields_ = [
        ('specval', ctypes.c_uint64),
        ('specval_shorts', struct_op_t___unnamed_tag____unnamed_type_specval_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__6E71FB17325AE2954BF4597A8A4FC61F(Union):
        pass
    
    union__6E71FB17325AE2954BF4597A8A4FC61F._pack_ = 1 # source:False
    union__6E71FB17325AE2954BF4597A8A4FC61F._fields_ = [
        ('specval', ctypes.c_uint64),
        ('specval_shorts', struct_op_t___unnamed_tag____unnamed_type_specval_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__873AABC3E23F76DAD852B3A5ED3D0239(Union):
        pass
    
    union__873AABC3E23F76DAD852B3A5ED3D0239._pack_ = 1 # source:False
    union__873AABC3E23F76DAD852B3A5ED3D0239._fields_ = [
        ('addr', ctypes.c_uint64),
        ('addr_shorts', struct_op_t___unnamed_tag____unnamed_type_addr_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__A79E5FD44D535857D5D82C32CF5C7F3D(Union):
        pass
    
    union__A79E5FD44D535857D5D82C32CF5C7F3D._pack_ = 1 # source:False
    union__A79E5FD44D535857D5D82C32CF5C7F3D._fields_ = [
        ('value', ctypes.c_uint64),
        ('value_shorts', struct_op_t___unnamed_tag____unnamed_type_value_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__DD3B514C20105750B5B46F5AA1F9281B(Union):
        pass
    
    union__DD3B514C20105750B5B46F5AA1F9281B._pack_ = 1 # source:False
    union__DD3B514C20105750B5B46F5AA1F9281B._fields_ = [
        ('value', ctypes.c_uint64),
        ('value_shorts', struct_op_t___unnamed_tag____unnamed_type_value_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__E9F0CCD17EA9996D87C5780C68234140(Union):
        pass
    
    union__E9F0CCD17EA9996D87C5780C68234140._pack_ = 1 # source:False
    union__E9F0CCD17EA9996D87C5780C68234140._fields_ = [
        ('specval', ctypes.c_uint64),
        ('specval_shorts', struct_op_t___unnamed_tag____unnamed_type_specval_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union__F6C33E3B57865EFDC1EE4707AE4184E1(Union):
        pass
    
    union__F6C33E3B57865EFDC1EE4707AE4184E1._pack_ = 1 # source:False
    union__F6C33E3B57865EFDC1EE4707AE4184E1._fields_ = [
        ('addr', ctypes.c_uint64),
        ('addr_shorts', struct_op_t___unnamed_tag____unnamed_type_addr_shorts_),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    ADDRINFOA = struct_addrinfo
    ThrowInfo = struct__s_ThrowInfo
    GUID = struct__GUID
    class union__ULARGE_INTEGER(Union):
        pass
    
    union__ULARGE_INTEGER._pack_ = 1 # source:False
    union__ULARGE_INTEGER._fields_ = [
        ('__s0', struct__B950AFB169DC87688B328897744C612F),
        ('u', struct__ULARGE_INTEGER___unnamed_type_u_),
        ('QuadPart', ctypes.c_uint64),
    ]
    
    class union__LARGE_INTEGER(Union):
        pass
    
    union__LARGE_INTEGER._pack_ = 1 # source:False
    union__LARGE_INTEGER._fields_ = [
        ('__s0', struct__FAF74743FBE1C8632047CFB668F7028A),
        ('u', struct__LARGE_INTEGER___unnamed_type_u_),
        ('QuadPart', ctypes.c_int64),
    ]
    
    LARGE_INTEGER = union__LARGE_INTEGER
    _ThrowInfo = struct__s_ThrowInfo
    __all__ = \
        ['ADD', 'ADDRINFOA', 'ADLT_FREQUENT', 'ADLT_RECENT',
        'ALREADY_EXISTS', 'AL_EFFECTIVE', 'AL_MACHINE', 'AL_USER',
        'APPDOCLISTTYPE', 'ASSOCIATIONLEVEL', 'ASSOCIATIONTYPE',
        'AT_FILEEXTENSION', 'AT_MIMETYPE', 'AT_STARTMENUCLIENT',
        'AT_URLPROTOCOL', 'BAD', 'BINDSTATUS_64BIT_PROGRESS',
        'BINDSTATUS_ACCEPTRANGES', 'BINDSTATUS_BEGINDOWNLOADCOMPONENTS',
        'BINDSTATUS_BEGINDOWNLOADDATA', 'BINDSTATUS_BEGINSYNCOPERATION',
        'BINDSTATUS_BEGINUPLOADDATA', 'BINDSTATUS_CACHECONTROL',
        'BINDSTATUS_CACHEFILENAMEAVAILABLE',
        'BINDSTATUS_CLASSIDAVAILABLE', 'BINDSTATUS_CLASSINSTALLLOCATION',
        'BINDSTATUS_CLSIDCANINSTANTIATE',
        'BINDSTATUS_COMPACT_POLICY_RECEIVED', 'BINDSTATUS_CONNECTING',
        'BINDSTATUS_CONTENTDISPOSITIONATTACH',
        'BINDSTATUS_CONTENTDISPOSITIONFILENAME', 'BINDSTATUS_COOKIE_SENT',
        'BINDSTATUS_COOKIE_STATE_ACCEPT',
        'BINDSTATUS_COOKIE_STATE_DOWNGRADE',
        'BINDSTATUS_COOKIE_STATE_LEASH', 'BINDSTATUS_COOKIE_STATE_PROMPT',
        'BINDSTATUS_COOKIE_STATE_REJECT',
        'BINDSTATUS_COOKIE_STATE_UNKNOWN', 'BINDSTATUS_COOKIE_SUPPRESSED',
        'BINDSTATUS_DECODING', 'BINDSTATUS_DIRECTBIND',
        'BINDSTATUS_DISPLAYNAMEAVAILABLE', 'BINDSTATUS_DOWNLOADINGDATA',
        'BINDSTATUS_ENCODING', 'BINDSTATUS_ENDDOWNLOADCOMPONENTS',
        'BINDSTATUS_ENDDOWNLOADDATA', 'BINDSTATUS_ENDSYNCOPERATION',
        'BINDSTATUS_ENDUPLOADDATA', 'BINDSTATUS_FILTERREPORTMIMETYPE',
        'BINDSTATUS_FINDINGRESOURCE', 'BINDSTATUS_INSTALLINGCOMPONENTS',
        'BINDSTATUS_IUNKNOWNAVAILABLE', 'BINDSTATUS_LOADINGMIMEHANDLER',
        'BINDSTATUS_MIMETEXTPLAINMISMATCH',
        'BINDSTATUS_MIMETYPEAVAILABLE', 'BINDSTATUS_P3P_HEADER',
        'BINDSTATUS_PERSISTENT_COOKIE_RECEIVED', 'BINDSTATUS_POLICY_HREF',
        'BINDSTATUS_PROTOCOLCLASSID', 'BINDSTATUS_PROXYDETECTING',
        'BINDSTATUS_PUBLISHERAVAILABLE', 'BINDSTATUS_RAWMIMETYPE',
        'BINDSTATUS_REDIRECTING', 'BINDSTATUS_SENDINGREQUEST',
        'BINDSTATUS_SERVER_MIMETYPEAVAILABLE',
        'BINDSTATUS_SESSION_COOKIES_ALLOWED',
        'BINDSTATUS_SESSION_COOKIE_RECEIVED',
        'BINDSTATUS_SNIFFED_CLASSIDAVAILABLE',
        'BINDSTATUS_SSLUX_NAVBLOCKED', 'BINDSTATUS_UPLOADINGDATA',
        'BINDSTATUS_USINGCACHEDCOPY',
        'BINDSTATUS_VERIFIEDMIMETYPEAVAILABLE',
        'BINDSTRING_ACCEPT_ENCODINGS', 'BINDSTRING_ACCEPT_MIMES',
        'BINDSTRING_EXTRA_URL', 'BINDSTRING_FLAG_BIND_TO_OBJECT',
        'BINDSTRING_HEADERS', 'BINDSTRING_IID', 'BINDSTRING_LANGUAGE',
        'BINDSTRING_OS', 'BINDSTRING_PASSWORD', 'BINDSTRING_POST_COOKIE',
        'BINDSTRING_POST_DATA_MIME', 'BINDSTRING_PTR_BIND_CONTEXT',
        'BINDSTRING_UA_COLOR', 'BINDSTRING_UA_PIXELS', 'BINDSTRING_URL',
        'BINDSTRING_USERNAME', 'BINDSTRING_USER_AGENT',
        'BINDSTRING_XDR_ORIGIN', 'BSID_BANDADDED', 'BSID_BANDREMOVED',
        'CC_CDECL', 'CC_FASTCALL', 'CC_FPFASTCALL', 'CC_MACPASCAL',
        'CC_MAX', 'CC_MPWCDECL', 'CC_MPWPASCAL', 'CC_MSCPASCAL',
        'CC_PASCAL', 'CC_STDCALL', 'CC_SYSCALL', 'CHANGEKIND_ADDMEMBER',
        'CHANGEKIND_CHANGEFAILED', 'CHANGEKIND_DELETEMEMBER',
        'CHANGEKIND_GENERAL', 'CHANGEKIND_INVALIDATE', 'CHANGEKIND_MAX',
        'CHANGEKIND_SETDOCUMENTATION', 'CHANGEKIND_SETNAMES', 'CHECK',
        'CIP_ACCESS_DENIED', 'CIP_DISK_FULL',
        'CIP_EXE_SELF_REGISTERATION_TIMEOUT', 'CIP_NAME_CONFLICT',
        'CIP_NEED_REBOOT', 'CIP_NEED_REBOOT_UI_PERMISSION',
        'CIP_NEWER_VERSION_EXISTS', 'CIP_OLDER_VERSION_EXISTS',
        'CIP_TRUST_VERIFICATION_COMPONENT_MISSING', 'CIP_UNSAFE_TO_ABORT',
        'CLSCTX_ACTIVATE_32_BIT_SERVER', 'CLSCTX_ACTIVATE_64_BIT_SERVER',
        'CLSCTX_DISABLE_AAA', 'CLSCTX_ENABLE_AAA',
        'CLSCTX_ENABLE_CLOAKING', 'CLSCTX_ENABLE_CODE_DOWNLOAD',
        'CLSCTX_FROM_DEFAULT_CONTEXT', 'CLSCTX_INPROC_HANDLER',
        'CLSCTX_INPROC_HANDLER16', 'CLSCTX_INPROC_SERVER',
        'CLSCTX_INPROC_SERVER16', 'CLSCTX_LOCAL_SERVER',
        'CLSCTX_NO_CODE_DOWNLOAD', 'CLSCTX_NO_CUSTOM_MARSHAL',
        'CLSCTX_NO_FAILURE_LOG', 'CLSCTX_PS_DLL', 'CLSCTX_REMOTE_SERVER',
        'CLSCTX_RESERVED1', 'CLSCTX_RESERVED2', 'CLSCTX_RESERVED3',
        'CLSCTX_RESERVED4', 'CLSCTX_RESERVED5', 'CODELENS', 'CODES',
        'COMGLB_EXCEPTION_DONOT_HANDLE',
        'COMGLB_EXCEPTION_DONOT_HANDLE_ANY',
        'COMGLB_EXCEPTION_DONOT_HANDLE_FATAL', 'COMGLB_EXCEPTION_HANDLE',
        'COMIMAGE_FLAGS_32BITREQUIRED', 'COMIMAGE_FLAGS_ILONLY',
        'COMIMAGE_FLAGS_IL_LIBRARY', 'COMIMAGE_FLAGS_NATIVE_ENTRYPOINT',
        'COMIMAGE_FLAGS_STRONGNAMESIGNED',
        'COMIMAGE_FLAGS_TRACKDEBUGDATA', 'COMMENT', 'COPY', 'COPY_',
        'COP_APPLICATION_SPECIFIC', 'COP_DOSWILDCARDS', 'COP_EQUAL',
        'COP_GREATERTHAN', 'COP_GREATERTHANOREQUAL', 'COP_IMPLICIT',
        'COP_LESSTHAN', 'COP_LESSTHANOREQUAL', 'COP_NOTEQUAL',
        'COP_VALUE_CONTAINS', 'COP_VALUE_ENDSWITH',
        'COP_VALUE_NOTCONTAINS', 'COP_VALUE_STARTSWITH', 'COP_WORD_EQUAL',
        'COP_WORD_STARTSWITH', 'COR_DELETED_NAME_LENGTH',
        'COR_ILMETHOD_SECT_SMALL_MAX_DATASIZE', 'COR_VERSION_MAJOR',
        'COR_VERSION_MAJOR_V2', 'COR_VERSION_MINOR',
        'COR_VTABLEGAP_NAME_LENGTH', 'COR_VTABLE_32BIT',
        'COR_VTABLE_64BIT', 'COR_VTABLE_CALL_MOST_DERIVED',
        'COR_VTABLE_FROM_UNMANAGED',
        'COR_VTABLE_FROM_UNMANAGED_RETAIN_APPDOMAIN', 'CPB_Adlam',
        'CPB_Aegean_Numbers', 'CPB_Ahom', 'CPB_Alchemical_Symbols',
        'CPB_Alphabetic_Presentation_Forms', 'CPB_Anatolian_Hieroglyphs',
        'CPB_Ancient_Greek_Musical_Notation', 'CPB_Ancient_Greek_Numbers',
        'CPB_Ancient_Symbols', 'CPB_Arabic', 'CPB_Arabic_Extended_A',
        'CPB_Arabic_Mathematical_Alphabetic_Symbols',
        'CPB_Arabic_Presentation_Forms_A',
        'CPB_Arabic_Presentation_Forms_B', 'CPB_Arabic_Supplement',
        'CPB_Armenian', 'CPB_Arrows', 'CPB_Avestan', 'CPB_Balinese',
        'CPB_Bamum', 'CPB_Bamum_Supplement', 'CPB_Basic_Latin',
        'CPB_Bassa_Vah', 'CPB_Batak', 'CPB_Bengali', 'CPB_Bhaiksuki',
        'CPB_Block_Elements', 'CPB_Bopomofo', 'CPB_Bopomofo_Extended',
        'CPB_Box_Drawing', 'CPB_Brahmi', 'CPB_Braille_Patterns',
        'CPB_Buginese', 'CPB_Buhid', 'CPB_Byzantine_Musical_Symbols',
        'CPB_CJK_Compatibility', 'CPB_CJK_Compatibility_Forms',
        'CPB_CJK_Compatibility_Ideographs',
        'CPB_CJK_Compatibility_Ideographs_Supplement',
        'CPB_CJK_Radicals_Supplement', 'CPB_CJK_Strokes',
        'CPB_CJK_Symbols_and_Punctuation', 'CPB_CJK_Unified_Ideographs',
        'CPB_CJK_Unified_Ideographs_Extension_A',
        'CPB_CJK_Unified_Ideographs_Extension_B',
        'CPB_CJK_Unified_Ideographs_Extension_C',
        'CPB_CJK_Unified_Ideographs_Extension_D',
        'CPB_CJK_Unified_Ideographs_Extension_E', 'CPB_Carian',
        'CPB_Caucasian_Albanian', 'CPB_Chakma', 'CPB_Cham',
        'CPB_Cherokee', 'CPB_Cherokee_Supplement',
        'CPB_Combining_Diacritical_Marks',
        'CPB_Combining_Diacritical_Marks_Extended',
        'CPB_Combining_Diacritical_Marks_Supplement',
        'CPB_Combining_Diacritical_Marks_for_Symbols',
        'CPB_Combining_Half_Marks', 'CPB_Common_Indic_Number_Forms',
        'CPB_Control_Pictures', 'CPB_Coptic', 'CPB_Coptic_Epact_Numbers',
        'CPB_Counting_Rod_Numerals', 'CPB_Cuneiform',
        'CPB_Cuneiform_Numbers_and_Punctuation', 'CPB_Currency_Symbols',
        'CPB_Cypriot_Syllabary', 'CPB_Cyrillic',
        'CPB_Cyrillic_Extended_A', 'CPB_Cyrillic_Extended_B',
        'CPB_Cyrillic_Extended_C', 'CPB_Cyrillic_Supplement',
        'CPB_Deseret', 'CPB_Devanagari', 'CPB_Devanagari_Extended',
        'CPB_Dingbats', 'CPB_Domino_Tiles', 'CPB_Duployan',
        'CPB_Early_Dynastic_Cuneiform', 'CPB_Egyptian_Hieroglyphs',
        'CPB_Elbasan', 'CPB_Emoticons',
        'CPB_Enclosed_Alphanumeric_Supplement',
        'CPB_Enclosed_Alphanumerics',
        'CPB_Enclosed_CJK_Letters_and_Months',
        'CPB_Enclosed_Ideographic_Supplement', 'CPB_Ethiopic',
        'CPB_Ethiopic_Extended', 'CPB_Ethiopic_Extended_A',
        'CPB_Ethiopic_Supplement', 'CPB_General_Punctuation',
        'CPB_Geometric_Shapes', 'CPB_Geometric_Shapes_Extended',
        'CPB_Georgian', 'CPB_Georgian_Supplement', 'CPB_Glagolitic',
        'CPB_Glagolitic_Supplement', 'CPB_Gothic', 'CPB_Grantha',
        'CPB_Greek_Extended', 'CPB_Greek_and_Coptic', 'CPB_Gujarati',
        'CPB_Gurmukhi', 'CPB_Halfwidth_and_Fullwidth_Forms',
        'CPB_Hangul_Compatibility_Jamo', 'CPB_Hangul_Jamo',
        'CPB_Hangul_Jamo_Extended_A', 'CPB_Hangul_Jamo_Extended_B',
        'CPB_Hangul_Syllables', 'CPB_Hanunoo', 'CPB_Hatran', 'CPB_Hebrew',
        'CPB_High_Private_Use_Surrogates', 'CPB_High_Surrogates',
        'CPB_Hiragana', 'CPB_IPA_Extensions',
        'CPB_Ideographic_Description_Characters',
        'CPB_Ideographic_Symbols_and_Punctuation', 'CPB_Imperial_Aramaic',
        'CPB_Inscriptional_Pahlavi', 'CPB_Inscriptional_Parthian',
        'CPB_Javanese', 'CPB_Kaithi', 'CPB_Kana_Supplement', 'CPB_Kanbun',
        'CPB_Kangxi_Radicals', 'CPB_Kannada', 'CPB_Katakana',
        'CPB_Katakana_Phonetic_Extensions', 'CPB_Kayah_Li',
        'CPB_Kharoshthi', 'CPB_Khmer', 'CPB_Khmer_Symbols', 'CPB_Khojki',
        'CPB_Khudawadi', 'CPB_Lao', 'CPB_Latin_1_Supplement',
        'CPB_Latin_Extended_A', 'CPB_Latin_Extended_Additional',
        'CPB_Latin_Extended_B', 'CPB_Latin_Extended_C',
        'CPB_Latin_Extended_D', 'CPB_Latin_Extended_E', 'CPB_Lepcha',
        'CPB_Letterlike_Symbols', 'CPB_Limbu', 'CPB_Linear_A',
        'CPB_Linear_B_Ideograms', 'CPB_Linear_B_Syllabary', 'CPB_Lisu',
        'CPB_Low_Surrogates', 'CPB_Lycian', 'CPB_Lydian', 'CPB_Mahajani',
        'CPB_Mahjong_Tiles', 'CPB_Malayalam', 'CPB_Mandaic',
        'CPB_Manichaean', 'CPB_Marchen',
        'CPB_Mathematical_Alphanumeric_Symbols',
        'CPB_Mathematical_Operators', 'CPB_Meetei_Mayek',
        'CPB_Meetei_Mayek_Extensions', 'CPB_Mende_Kikakui',
        'CPB_Meroitic_Cursive', 'CPB_Meroitic_Hieroglyphs', 'CPB_Miao',
        'CPB_Miscellaneous_Mathematical_Symbols_A',
        'CPB_Miscellaneous_Mathematical_Symbols_B',
        'CPB_Miscellaneous_Symbols',
        'CPB_Miscellaneous_Symbols_and_Arrows',
        'CPB_Miscellaneous_Symbols_and_Pictographs',
        'CPB_Miscellaneous_Technical', 'CPB_Modi',
        'CPB_Modifier_Tone_Letters', 'CPB_Mongolian',
        'CPB_Mongolian_Supplement', 'CPB_Mro', 'CPB_Multani',
        'CPB_Musical_Symbols', 'CPB_Myanmar', 'CPB_Myanmar_Extended_A',
        'CPB_Myanmar_Extended_B', 'CPB_NKo', 'CPB_Nabataean',
        'CPB_New_Tai_Lue', 'CPB_Newa', 'CPB_Number_Forms', 'CPB_Ogham',
        'CPB_Ol_Chiki', 'CPB_Old_Hungarian', 'CPB_Old_Italic',
        'CPB_Old_North_Arabian', 'CPB_Old_Permic', 'CPB_Old_Persian',
        'CPB_Old_South_Arabian', 'CPB_Old_Turkic',
        'CPB_Optical_Character_Recognition', 'CPB_Oriya',
        'CPB_Ornamental_Dingbats', 'CPB_Osage', 'CPB_Osmanya',
        'CPB_Pahawh_Hmong', 'CPB_Palmyrene', 'CPB_Pau_Cin_Hau',
        'CPB_Phags_pa', 'CPB_Phaistos_Disc', 'CPB_Phoenician',
        'CPB_Phonetic_Extensions', 'CPB_Phonetic_Extensions_Supplement',
        'CPB_Playing_Cards', 'CPB_Private_Use_Area',
        'CPB_Psalter_Pahlavi', 'CPB_Rejang', 'CPB_Rumi_Numeral_Symbols',
        'CPB_Runic', 'CPB_Samaritan', 'CPB_Saurashtra', 'CPB_Sharada',
        'CPB_Shavian', 'CPB_Shorthand_Format_Controls', 'CPB_Siddham',
        'CPB_Sinhala', 'CPB_Sinhala_Archaic_Numbers',
        'CPB_Small_Form_Variants', 'CPB_Sora_Sompeng',
        'CPB_Spacing_Modifier_Letters', 'CPB_Specials', 'CPB_Sundanese',
        'CPB_Sundanese_Supplement', 'CPB_Superscripts_and_Subscripts',
        'CPB_Supplemental_Arrows_A', 'CPB_Supplemental_Arrows_B',
        'CPB_Supplemental_Arrows_C',
        'CPB_Supplemental_Mathematical_Operators',
        'CPB_Supplemental_Punctuation',
        'CPB_Supplemental_Symbols_and_Pictographs',
        'CPB_Supplementary_Private_Use_Area_A',
        'CPB_Supplementary_Private_Use_Area_B', 'CPB_Sutton_SignWriting',
        'CPB_Syloti_Nagri', 'CPB_Syriac', 'CPB_Tagalog', 'CPB_Tagbanwa',
        'CPB_Tags', 'CPB_Tai_Le', 'CPB_Tai_Tham', 'CPB_Tai_Viet',
        'CPB_Tai_Xuan_Jing_Symbols', 'CPB_Takri', 'CPB_Tamil',
        'CPB_Tangut', 'CPB_Tangut_Components', 'CPB_Telugu', 'CPB_Thaana',
        'CPB_Thai', 'CPB_Tibetan', 'CPB_Tifinagh', 'CPB_Tirhuta',
        'CPB_Transport_and_Map_Symbols', 'CPB_Ugaritic',
        'CPB_Unified_Canadian_Aboriginal_Syllabics',
        'CPB_Unified_Canadian_Aboriginal_Syllabics_Extended',
        'CPB_Unknown', 'CPB_Vai', 'CPB_Variation_Selectors',
        'CPB_Variation_Selectors_Supplement', 'CPB_Vedic_Extensions',
        'CPB_Vertical_Forms', 'CPB_Warang_Citi', 'CPB_Yi_Radicals',
        'CPB_Yi_Syllables', 'CPB_Yijing_Hexagram_Symbols', 'CPB_last',
        'CPC_Cc', 'CPC_Cf', 'CPC_Cn', 'CPC_Co', 'CPC_Cs', 'CPC_LC',
        'CPC_Ll', 'CPC_Lm', 'CPC_Lo', 'CPC_Lt', 'CPC_Lu', 'CPC_Mc',
        'CPC_Me', 'CPC_Mn', 'CPC_Nd', 'CPC_Nl', 'CPC_No', 'CPC_Pc',
        'CPC_Pd', 'CPC_Pe', 'CPC_Pf', 'CPC_Pi', 'CPC_Po', 'CPC_Ps',
        'CPC_Sc', 'CPC_Sk', 'CPC_Sm', 'CPC_So', 'CPC_Unknown', 'CPC_Zl',
        'CPC_Zp', 'CPC_Zs', 'CPC_last', 'CPVIEW', 'CPVIEW_ALLITEMS',
        'CPVIEW_CATEGORY', 'CPVIEW_CLASSIC', 'CPVIEW_HOME',
        'CREATE_RANGE', 'CREATING_NEW_IDB', 'CREATING_UNDO_POINT',
        'CT_AND_CONDITION', 'CT_ByReferenceOnly', 'CT_HasVirtualBase',
        'CT_IsSimpleType', 'CT_IsStdBadAlloc', 'CT_IsWinRTHandle',
        'CT_LEAF_CONDITION', 'CT_NOT_CONDITION', 'CT_OR_CONDITION',
        'DEFAULTSAVEFOLDERTYPE', 'DEL', 'DEL_RANGE', 'DESCKIND_FUNCDESC',
        'DESCKIND_IMPLICITAPPOBJ', 'DESCKIND_MAX', 'DESCKIND_NONE',
        'DESCKIND_TYPECOMP', 'DESCKIND_VARDESC', 'DICT', 'DICTID',
        'DISPLAYCONFIG_SCANLINE_ORDERING',
        'DISPLAYCONFIG_SCANLINE_ORDERING_FORCE_UINT32',
        'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED',
        'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_LOWERFIELDFIRST',
        'DISPLAYCONFIG_SCANLINE_ORDERING_INTERLACED_UPPERFIELDFIRST',
        'DISPLAYCONFIG_SCANLINE_ORDERING_PROGRESSIVE',
        'DISPLAYCONFIG_SCANLINE_ORDERING_UNSPECIFIED', 'DIST', 'DISTEXT',
        'DISTS', 'DONE', 'DSFT_DETECT', 'DSFT_PRIVATE', 'DSFT_PUBLIC',
        'DVEXTENT_CONTENT', 'DVEXTENT_INTEGRAL', 'EMPTY_CHOOSER',
        'ENDING_REDO', 'ENDING_UNDO', 'END_UNDO', 'EXLEN', 'EXTRA',
        'FEATURE_ADDON_MANAGEMENT', 'FEATURE_BEHAVIORS',
        'FEATURE_BLOCK_INPUT_PROMPTS',
        'FEATURE_DISABLE_LEGACY_COMPRESSION',
        'FEATURE_DISABLE_MK_PROTOCOL',
        'FEATURE_DISABLE_NAVIGATION_SOUNDS',
        'FEATURE_DISABLE_TELNET_PROTOCOL', 'FEATURE_ENTRY_COUNT',
        'FEATURE_FEEDS', 'FEATURE_FORCE_ADDR_AND_STATUS',
        'FEATURE_GET_URL_DOM_FILEPATH_UNENCODED',
        'FEATURE_HTTP_USERNAME_PASSWORD_DISABLE',
        'FEATURE_LOCALMACHINE_LOCKDOWN', 'FEATURE_MIME_HANDLING',
        'FEATURE_MIME_SNIFFING', 'FEATURE_OBJECT_CACHING',
        'FEATURE_PROTOCOL_LOCKDOWN', 'FEATURE_RESTRICT_ACTIVEXINSTALL',
        'FEATURE_RESTRICT_FILEDOWNLOAD', 'FEATURE_SAFE_BINDTOOBJECT',
        'FEATURE_SECURITYBAND', 'FEATURE_SSLUX',
        'FEATURE_TABBED_BROWSING', 'FEATURE_UNC_SAVEDFILECHECK',
        'FEATURE_VALIDATE_NAVIGATE_URL', 'FEATURE_WEBOC_POPUPMANAGEMENT',
        'FEATURE_WINDOW_RESTRICTIONS', 'FEATURE_XMLHTTP',
        'FEATURE_ZONE_ELEVATION', 'FFFP_EXACTMATCH', 'FFFP_MODE',
        'FFFP_NEARESTPARENTMATCH', 'FILE_USAGE_TYPE', 'FLAGS',
        'FUNC_DISPATCH', 'FUNC_NONVIRTUAL', 'FUNC_PUREVIRTUAL',
        'FUNC_STATIC', 'FUNC_VIRTUAL', 'FUT_EDITING', 'FUT_GENERIC',
        'FUT_PLAYING', 'ForcedShutdown', 'GUID', 'HCRC', 'HEAD',
        'IMAGE_COR_EATJ_THUNK_SIZE', 'IMAGE_COR_MIH_BASICBLOCK',
        'IMAGE_COR_MIH_EHRVA', 'IMAGE_COR_MIH_METHODRVA',
        'INITIALIZING_IDB', 'IPPROTO', 'IPPROTO_AH', 'IPPROTO_CBT',
        'IPPROTO_DSTOPTS', 'IPPROTO_EGP', 'IPPROTO_ESP',
        'IPPROTO_FRAGMENT', 'IPPROTO_GGP', 'IPPROTO_HOPOPTS',
        'IPPROTO_ICLFXBM', 'IPPROTO_ICMP', 'IPPROTO_ICMPV6',
        'IPPROTO_IDP', 'IPPROTO_IGMP', 'IPPROTO_IGP', 'IPPROTO_IPV4',
        'IPPROTO_IPV6', 'IPPROTO_L2TP', 'IPPROTO_MAX', 'IPPROTO_ND',
        'IPPROTO_NONE', 'IPPROTO_PGM', 'IPPROTO_PIM', 'IPPROTO_PUP',
        'IPPROTO_RAW', 'IPPROTO_RDP', 'IPPROTO_RESERVED_IPSEC',
        'IPPROTO_RESERVED_IPSECOFFLOAD', 'IPPROTO_RESERVED_MAX',
        'IPPROTO_RESERVED_RAW', 'IPPROTO_ROUTING', 'IPPROTO_SCTP',
        'IPPROTO_ST', 'IPPROTO_TCP', 'IPPROTO_UDP', 'IdleShutdown',
        'KDC_FREQUENT', 'KDC_RECENT', 'KNOWNDESTCATEGORY',
        'LARGE_INTEGER', 'LEN', 'LENEXT', 'LENGTH', 'LENLENS', 'LENS',
        'LEN_', 'LINPUT_GENERIC', 'LINPUT_LOCAL', 'LINPUT_NONE',
        'LINPUT_PROCMEM', 'LINPUT_RFILE', 'LIT', 'LOC_CLOSE', 'LOC_KEEP',
        'LOC_UNMAKE', 'LibraryApplication', 'MARKUPLINKTEXT',
        'MARKUPLINKTEXT_ID', 'MARKUPLINKTEXT_TEXT', 'MARKUPLINKTEXT_URL',
        'MARKUPMESSAGE', 'MARKUPMESSAGE_CLICKEXECUTE',
        'MARKUPMESSAGE_KEYEXECUTE', 'MARKUPMESSAGE_WANTFOCUS',
        'MARKUPSIZE', 'MARKUPSIZE_CALCHEIGHT', 'MARKUPSIZE_CALCWIDTH',
        'MATCH', 'MAX_CLASS_NAME', 'MAX_PACKAGE_NAME', 'MEM',
        'MERGE_STATE_2WAY', 'MERGE_STATE_MERGING', 'MERGE_STATE_NONE',
        'MERGE_STATE_OPENING', 'MFF_MAGIC', 'MPOS_CANCELLEVEL',
        'MPOS_CHILDTRACKING', 'MPOS_EXECUTE', 'MPOS_FULLCANCEL',
        'MPOS_SELECTLEFT', 'MPOS_SELECTRIGHT', 'NAME',
        'NATIVE_TYPE_MAX_CB', 'NCP_NOBYTE', 'NCP_NOCONV', 'NCP_OK',
        'NODE_ATTRIBUTE', 'NODE_CDATA_SECTION', 'NODE_COMMENT',
        'NODE_DOCUMENT', 'NODE_DOCUMENT_FRAGMENT', 'NODE_DOCUMENT_TYPE',
        'NODE_ELEMENT', 'NODE_ENTITY', 'NODE_ENTITY_REFERENCE',
        'NODE_INVALID', 'NODE_NOTATION', 'NODE_PROCESSING_INSTRUCTION',
        'NODE_TEXT', 'NOT_OPENING_IDB', 'NO_ATTR', 'NO_SELECTION',
        'NSTDPOPUPS', 'OFS_DIRTYCACHE', 'OFS_INACTIVE', 'OFS_OFFLINE',
        'OFS_ONLINE', 'OFS_SERVERBACK', 'OS', 'OfflineFolderStatus',
        'PARSE_ANCHOR', 'PARSE_CANONICALIZE', 'PARSE_DECODE_IS_ESCAPE',
        'PARSE_DOCUMENT', 'PARSE_DOMAIN', 'PARSE_ENCODE_IS_UNESCAPE',
        'PARSE_ESCAPE', 'PARSE_FRIENDLY', 'PARSE_LOCATION', 'PARSE_MIME',
        'PARSE_PATH_FROM_URL', 'PARSE_ROOTDOCUMENT', 'PARSE_SCHEMA',
        'PARSE_SECURITY_DOMAIN', 'PARSE_SECURITY_URL', 'PARSE_SERVER',
        'PARSE_SITE', 'PARSE_UNESCAPE', 'PARSE_URL_FROM_PATH',
        'PERFORM_REDO', 'PERFORM_UNDO', 'PIDMSI_STATUS_DRAFT',
        'PIDMSI_STATUS_EDIT', 'PIDMSI_STATUS_FINAL',
        'PIDMSI_STATUS_INPROGRESS', 'PIDMSI_STATUS_NEW',
        'PIDMSI_STATUS_NORMAL', 'PIDMSI_STATUS_OTHER',
        'PIDMSI_STATUS_PRELIM', 'PIDMSI_STATUS_PROOF',
        'PIDMSI_STATUS_REVIEW', 'PIDMSI_STATUS_VALUE', 'PKA_APPEND',
        'PKA_DELETE', 'PKA_FLAGS', 'PKA_SET', 'PMFN', 'POPUP_DEL',
        'POPUP_EDIT', 'POPUP_INS', 'POPUP_REFRESH', 'PSU_DEFAULT',
        'PSU_SECURITY_URL_ONLY', 'QMOVE_CROSS_FS', 'QMOVE_OVERWRITE',
        'QMOVE_OVR_RO', 'QUERY_CAN_NAVIGATE', 'QUERY_CONTENT_ENCODING',
        'QUERY_CONTENT_TYPE', 'QUERY_EXPIRATION_DATE', 'QUERY_IS_CACHED',
        'QUERY_IS_CACHED_OR_MAPPED', 'QUERY_IS_INSTALLEDENTRY',
        'QUERY_IS_SAFE', 'QUERY_IS_SECURE', 'QUERY_RECOMBINE',
        'QUERY_REFRESH', 'QUERY_TIME_OF_LAST_CHANGE', 'QUERY_USES_CACHE',
        'QUERY_USES_HISTORYFOLDER', 'QUERY_USES_NETWORK',
        'RANGE_KIND_FUNC', 'RANGE_KIND_HIDDEN_RANGE',
        'RANGE_KIND_SEGMENT', 'RANGE_KIND_UNKNOWN', 'RECV_DATA',
        'RPC_MEM', 'RPC_OK', 'RPC_UNK', 'RPL_ALL', 'RPL_CHECK',
        'RPL_NONE', 'ReplacesCorHdrNumericDefines', 'SEND_TOKEN',
        'SET_END', 'SET_START', 'SIGDN_DESKTOPABSOLUTEEDITING',
        'SIGDN_DESKTOPABSOLUTEPARSING', 'SIGDN_FILESYSPATH',
        'SIGDN_NORMALDISPLAY', 'SIGDN_PARENTRELATIVE',
        'SIGDN_PARENTRELATIVEEDITING',
        'SIGDN_PARENTRELATIVEFORADDRESSBAR',
        'SIGDN_PARENTRELATIVEPARSING', 'SIGDN_URL',
        'SPACTION_APPLYINGATTRIBS', 'SPACTION_CALCULATING',
        'SPACTION_COPYING', 'SPACTION_COPY_MOVING', 'SPACTION_DELETING',
        'SPACTION_DOWNLOADING', 'SPACTION_FORMATTING', 'SPACTION_MOVING',
        'SPACTION_NONE', 'SPACTION_RECYCLING', 'SPACTION_RENAMING',
        'SPACTION_SEARCHING_FILES', 'SPACTION_SEARCHING_INTERNET',
        'SPACTION_UPLOADING', 'SPTEXT_ACTIONDESCRIPTION',
        'SPTEXT_ACTIONDETAIL', 'STARTING_REDO', 'STARTING_UNDO',
        'START_UNDO', 'STATE_INIT', 'STATE_INIT_CONT', 'STORED',
        'SWITCH_INFO_VERSION', 'SYNC', 'SYS_MAC', 'SYS_WIN16',
        'SYS_WIN32', 'SYS_WIN64', 'ServerApplication', 'TABLE', 'TIME',
        'TI_IsConst', 'TI_IsPure', 'TI_IsUnaligned', 'TI_IsVolatile',
        'TI_IsWinRT', 'TKIND_ALIAS', 'TKIND_COCLASS', 'TKIND_DISPATCH',
        'TKIND_ENUM', 'TKIND_INTERFACE', 'TKIND_MAX', 'TKIND_MODULE',
        'TKIND_RECORD', 'TKIND_UNION', 'TP_CALLBACK_PRIORITY_HIGH',
        'TP_CALLBACK_PRIORITY_INVALID', 'TP_CALLBACK_PRIORITY_LOW',
        'TP_CALLBACK_PRIORITY_NORMAL', 'TYPE', 'TYPEDO', 'TYSPEC_CLSID',
        'TYSPEC_FILEEXT', 'TYSPEC_FILENAME', 'TYSPEC_MIMETYPE',
        'TYSPEC_OBJECTID', 'TYSPEC_PACKAGENAME', 'TYSPEC_PROGID',
        'ThrowInfo', 'UIFILT_QUICK', 'UNDO_ACTION_START',
        'UNDO_AFLAGS_DEL', 'UNDO_AFLAGS_INS_RANGE', 'UNDO_AFLAGS_KILL',
        'UNDO_AFLAGS_UPD', 'UNDO_AU_AUTO_STATE', 'UNDO_AU_CHLB',
        'UNDO_AU_CODE', 'UNDO_AU_DONE', 'UNDO_AU_EMPTY', 'UNDO_AU_FCHUNK',
        'UNDO_AU_FINAL', 'UNDO_AU_HNNODE', 'UNDO_AU_LBF2', 'UNDO_AU_LBF3',
        'UNDO_AU_LIBF', 'UNDO_AU_POSTPONED', 'UNDO_AU_PROC',
        'UNDO_AU_TAIL', 'UNDO_AU_TYPE', 'UNDO_AU_UNK', 'UNDO_AU_USED',
        'UNDO_AU_WEAK', 'UNDO_AU_WEAK_DEL', 'UNDO_AU_WEAK_INS',
        'UNDO_BPTS_CHANGE_BPTLOC', 'UNDO_BPTS_MOVE', 'UNDO_BPT_ADD',
        'UNDO_BPT_DEL', 'UNDO_BPT_ENABLE', 'UNDO_BPT_GROUPS_ADD',
        'UNDO_BPT_GROUPS_CHANGE_BPTGRP', 'UNDO_BPT_GROUPS_DEL',
        'UNDO_BPT_GROUPS_RENAME', 'UNDO_BPT_SET_LOC_STRING',
        'UNDO_BPT_UPD', 'UNDO_BTREE', 'UNDO_CHBYTES', 'UNDO_CHFLAGS',
        'UNDO_CREF_FROM_DEL', 'UNDO_CREF_FROM_INS', 'UNDO_CREF_TO_DEL',
        'UNDO_CREF_TO_INS', 'UNDO_DBG_EA2SYM_DEL', 'UNDO_DBG_EA2SYM_INS',
        'UNDO_DBG_EA2SYM_KILL', 'UNDO_DBG_EA2SYM_NAMEVEC_DEL',
        'UNDO_DBG_EA2SYM_NAMEVEC_INS', 'UNDO_DBG_FLAGS_DEL_RANGE',
        'UNDO_DBG_FLAGS_INS_RANGE', 'UNDO_DBG_SYM2EA_DEL',
        'UNDO_DBG_SYM2EA_INS', 'UNDO_DBG_SYM2EA_KILL',
        'UNDO_DEFAULT_ENCODING_IDX', 'UNDO_DEPTH', 'UNDO_DREF_FROM_DEL',
        'UNDO_DREF_FROM_INS', 'UNDO_DREF_TO_DEL', 'UNDO_DREF_TO_INS',
        'UNDO_DTW_CUT_PATHS_ADD', 'UNDO_DTW_CUT_PATHS_DEL',
        'UNDO_DT_BOOKMARKS_ENUMS', 'UNDO_DT_BOOKMARKS_IDAPLACE',
        'UNDO_DT_BOOKMARKS_STRUCTS', 'UNDO_DT_BPTS', 'UNDO_DT_DIRTY',
        'UNDO_DT_ENUMS', 'UNDO_DT_FUNCS', 'UNDO_DT_IMPORTS',
        'UNDO_DT_LOCAL_TYPES', 'UNDO_DT_NAMES', 'UNDO_DT_PROBLEMS',
        'UNDO_DT_STRUCTS', 'UNDO_DURING_AA', 'UNDO_EATIFS_DELETE',
        'UNDO_EATIFS_UPDATE', 'UNDO_ENABLED', 'UNDO_ENCODING_LIST_ADD',
        'UNDO_ENCODING_LIST_DEL', 'UNDO_ENCODING_LIST_UPD',
        'UNDO_FIXUP_DEL', 'UNDO_FIXUP_DEL_RANGE', 'UNDO_FIXUP_INS_RANGE',
        'UNDO_FIXUP_UPD', 'UNDO_FUNCS', 'UNDO_GROUPSEL',
        'UNDO_IDATIL_ADD', 'UNDO_IDATIL_DEL', 'UNDO_IDATIL_STDORD_INS',
        'UNDO_INF', 'UNDO_LONGNAME_ADD', 'UNDO_LONGNAME_DEL',
        'UNDO_LOWTIL_ABINAME', 'UNDO_LOWTIL_ADDENTRY',
        'UNDO_LOWTIL_ALLOC_ORDS', 'UNDO_LOWTIL_DELENTRY',
        'UNDO_LOWTIL_ENABLE_NUMBERED', 'UNDO_LOWTIL_SET_ALIAS',
        'UNDO_MAXLINK_GROW', 'UNDO_MAXNODE_GROW',
        'UNDO_MAXSERIALNAME_INC', 'UNDO_MAXSERIALNAME_RESET',
        'UNDO_MAXSIZE', 'UNDO_MOVE_TINFO_CACHE', 'UNDO_NCACHE',
        'UNDO_NCACHE_MOVE', 'UNDO_NIMPLIBS', 'UNDO_NONE',
        'UNDO_NOT_REPLAYING', 'UNDO_OPTIFS_DELETE', 'UNDO_OPTIFS_UPDATE',
        'UNDO_OUTFILE_ENCODING_IDX', 'UNDO_POOL_START',
        'UNDO_PROBLEM_ROLLBACK_ADD', 'UNDO_PROBLEM_ROLLBACK_DEL',
        'UNDO_RANGECB_FILEREGIONS', 'UNDO_RANGECB_FUNCS',
        'UNDO_RANGECB_HIDDEN_RANGES', 'UNDO_RANGECB_MAPPING',
        'UNDO_RANGECB_SEGS', 'UNDO_RANGECB_SOURCEFILES', 'UNDO_REPLAYING',
        'UNDO_SEGREGS_ADD', 'UNDO_SEGREGS_COPY', 'UNDO_SEGREGS_DEL',
        'UNDO_SEGREGS_DEL_RANGE', 'UNDO_SEGREGS_INS_RANGE',
        'UNDO_SEGREGS_SET_END', 'UNDO_SEGREGS_SET_START',
        'UNDO_SEGREGS_UPD', 'UNDO_SEGS', 'UNDO_SEGS_NAME_ADD',
        'UNDO_SEGS_NAME_CLS_ADD', 'UNDO_SEGS_NAME_CLS_DEL',
        'UNDO_SEGS_NAME_DEL', 'UNDO_SEGS_NAME_EA_ADD',
        'UNDO_SEGS_NAME_EA_DEL', 'UNDO_SEGS_NAME_MOVE',
        'UNDO_SEGS_SELS_DEL', 'UNDO_SEGS_SELS_INS', 'UNDO_SEGS_SELS_UPD',
        'UNDO_SPARSE_FLAGS_DEL_RANGE', 'UNDO_SPARSE_FLAGS_INS_RANGE',
        'UNDO_SPARSE_FLAGS_SIZE', 'UNDO_SPARSE_RANGES',
        'UNDO_STARTING_REPLAYING', 'UNDO_STRLIST_MOVED', 'UNDO_STRUC',
        'UNDO_STRUC_ADJUST_IDX', 'UNDO_STRUC_IDX', 'UNDO_STRUC_NODES',
        'UNDO_TRYBLK_CACHE_DEL', 'UNDO_TRYBLK_CACHE_INS',
        'UNDO_TRYBLK_EAS_DEL', 'UNDO_TRYBLK_EAS_INS', 'UNDO_TRYBLK_MOVE',
        'UNDO_VA_FLAGS', 'UNDO_VA_NAMES', 'UNDO_VFTABLES_DEL',
        'UNDO_VFTABLES_KILL', 'UNDO_VFTABLES_UPD', 'UNDO_VMEM_RANGES',
        'UNDO_ZERO_RANGES', 'UPDATE', 'URLZONEREG_DEFAULT',
        'URLZONEREG_HKCU', 'URLZONEREG_HKLM', 'URLZONE_INTERNET',
        'URLZONE_INTRANET', 'URLZONE_INVALID', 'URLZONE_LOCAL_MACHINE',
        'URLZONE_PREDEFINED_MAX', 'URLZONE_PREDEFINED_MIN',
        'URLZONE_TRUSTED', 'URLZONE_UNTRUSTED', 'URLZONE_USER_MAX',
        'URLZONE_USER_MIN', 'Uri_HOST_DNS', 'Uri_HOST_IDN',
        'Uri_HOST_IPV4', 'Uri_HOST_IPV6', 'Uri_HOST_UNKNOWN',
        'Uri_PROPERTY_ABSOLUTE_URI', 'Uri_PROPERTY_AUTHORITY',
        'Uri_PROPERTY_DISPLAY_URI', 'Uri_PROPERTY_DOMAIN',
        'Uri_PROPERTY_DWORD_LAST', 'Uri_PROPERTY_DWORD_START',
        'Uri_PROPERTY_EXTENSION', 'Uri_PROPERTY_FRAGMENT',
        'Uri_PROPERTY_HOST', 'Uri_PROPERTY_HOST_TYPE',
        'Uri_PROPERTY_PASSWORD', 'Uri_PROPERTY_PATH',
        'Uri_PROPERTY_PATH_AND_QUERY', 'Uri_PROPERTY_PORT',
        'Uri_PROPERTY_QUERY', 'Uri_PROPERTY_RAW_URI',
        'Uri_PROPERTY_SCHEME', 'Uri_PROPERTY_SCHEME_NAME',
        'Uri_PROPERTY_STRING_LAST', 'Uri_PROPERTY_STRING_START',
        'Uri_PROPERTY_USER_INFO', 'Uri_PROPERTY_USER_NAME',
        'Uri_PROPERTY_ZONE', 'VARENUM', 'VAR_CONST', 'VAR_DISPATCH',
        'VAR_PERINSTANCE', 'VAR_STATIC', 'VT_ARRAY', 'VT_BLOB',
        'VT_BLOB_OBJECT', 'VT_BOOL', 'VT_BSTR', 'VT_BSTR_BLOB',
        'VT_BYREF', 'VT_CARRAY', 'VT_CF', 'VT_CLSID', 'VT_CY', 'VT_DATE',
        'VT_DECIMAL', 'VT_DISPATCH', 'VT_EMPTY', 'VT_ERROR',
        'VT_FILETIME', 'VT_HRESULT', 'VT_I1', 'VT_I2', 'VT_I4', 'VT_I8',
        'VT_ILLEGAL', 'VT_ILLEGALMASKED', 'VT_INT', 'VT_INT_PTR',
        'VT_LPSTR', 'VT_LPWSTR', 'VT_NULL', 'VT_PTR', 'VT_R4', 'VT_R8',
        'VT_RECORD', 'VT_RESERVED', 'VT_SAFEARRAY', 'VT_STORAGE',
        'VT_STORED_OBJECT', 'VT_STREAM', 'VT_STREAMED_OBJECT',
        'VT_TYPEMASK', 'VT_UI1', 'VT_UI2', 'VT_UI4', 'VT_UI8', 'VT_UINT',
        'VT_UINT_PTR', 'VT_UNKNOWN', 'VT_USERDEFINED', 'VT_VARIANT',
        'VT_VECTOR', 'VT_VERSIONED_STREAM', 'VT_VOID',
        'XMLELEMTYPE_COMMENT', 'XMLELEMTYPE_DOCUMENT', 'XMLELEMTYPE_DTD',
        'XMLELEMTYPE_ELEMENT', 'XMLELEMTYPE_OTHER', 'XMLELEMTYPE_PI',
        'XMLELEMTYPE_TEXT', '_09C4AA584BA5AA400AAD2947A5043C7F', '_Black',
        '_Left', '_Red', '_Right', '_SIGDN', '_SPACTION', '_SPTEXT',
        '_TP_CALLBACK_PRIORITY', '_ThrowInfo', '_URLZONEREG', '_Unused',
        '__CT_flags', '__MIDL_ICodeInstall_0001', '__MIDL_IUri_0001',
        '__MIDL_IUri_0002', '__TI_flags', '_tagINTERNETFEATURELIST',
        '_tagPARSEACTION', '_tagPSUACTION', '_tagQUERYOPTION',
        'base_packet_id_last', 'base_packet_id_t', 'block_done',
        'block_state', 'bucket_size',
        'chooser_base_t___unnamed_enum_NO_SELECTION_',
        'chooser_base_t___unnamed_enum_POPUP_INS_',
        'clean_quick_filter_flags____l2___unnamed_enum_UIFILT_QUICK_',
        'codepoint_stream_t__ncp_t', 'codetype', 'cp_block_t',
        'cp_category_t', 'exec_request_t___unnamed_enum_MFF_MAGIC_',
        'finish_done', 'finish_started', 'inflate_mode',
        'linput_close_code_t', 'linput_type_t', 'merge_state_t',
        'need_more', 'netnode__mapper_t__replace_policy_t',
        'opening_state_t', 'plc_cancel', 'plc_proceed', 'plc_skip_iter',
        'progress_loop_ctrl_t', 'range_kind_t', 'range_type_t',
        'rangecb_undo_record_t___unnamed_enum_CREATE_RANGE_',
        'rangeset_undo_record_t___unnamed_enum_ADD_', 'rt_coalesced',
        'rt_one_to_one', 'std___Tree_child',
        'std___Tree_node_char_const__P_const__P_void__P____Redbl',
        'std___Tree_node_char_const__P_const__P_void__P____Redbl__enumvalues',
        'std___Tree_node_int_void__P____Redbl',
        'std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____Redbl',
        'std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____Redbl__enumvalues',
        'std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____Redbl',
        'std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____Redbl',
        'std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____Redbl__enumvalues',
        'std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____Redbl',
        'std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____Redbl',
        'std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____Redbl',
        'std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____Redbl',
        'std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0______Redbl',
        'std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0______Redbl',
        'std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0______Redbl',
        'std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0______Redbl',
        'std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0______Redbl',
        'std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0______Redbl',
        'std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0______Redbl__enumvalues',
        'std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0______Redbl',
        'std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0______Redbl__enumvalues',
        'std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0______Redbl',
        'std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0______Redbl__enumvalues',
        'std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0______Redbl',
        'std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0______Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P________Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P________Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P________Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P________Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P________Redbl__enumvalues',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P________Redbl',
        'std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_char_const__P_const__P______Redbl',
        'std___Tree_val_std___Tree_simple_types_char_const__P_const__P______Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_int______Redbl',
        'std___Tree_val_std___Tree_simple_types_int______Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char__________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char__________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char____________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char____________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________Redbl__enumvalues',
        'std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P________Redbl',
        'std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P________Redbl__enumvalues',
        'std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64______unnamed_enum_bucket_size_',
        'struct_C_SCOPE_TABLE', 'struct_HINSTANCE__', 'struct_HKEY__',
        'struct_HWND__', 'struct_IP_ADDRESS_STRING',
        'struct_RUNTIME_FUNCTION', 'struct_UNWIND_CODE',
        'struct_UNWIND_INFO_HDR', 'struct_WSAData',
        'struct_WSPIAPI_FUNCTION',
        'struct__0AE2711FE0E2D1D4B43BA550E29B8803',
        'struct__77D3A2E2503DF0742434FD6F35F3BB5C',
        'struct__B950AFB169DC87688B328897744C612F',
        'struct__CERT_CHAIN_CONTEXT', 'struct__CERT_CHAIN_ELEMENT',
        'struct__CERT_CHAIN_PARA', 'struct__CERT_CONTEXT',
        'struct__CERT_EXTENSION', 'struct__CERT_INFO',
        'struct__CERT_PUBLIC_KEY_INFO',
        'struct__CERT_REVOCATION_CRL_INFO',
        'struct__CERT_REVOCATION_INFO', 'struct__CERT_SIMPLE_CHAIN',
        'struct__CERT_TRUST_LIST_INFO', 'struct__CERT_TRUST_STATUS',
        'struct__CERT_USAGE_MATCH', 'struct__CRL_CONTEXT',
        'struct__CRL_ENTRY', 'struct__CRL_INFO', 'struct__CRYPTOAPI_BLOB',
        'struct__CRYPT_ALGORITHM_IDENTIFIER', 'struct__CRYPT_ATTRIBUTE',
        'struct__CRYPT_BIT_BLOB', 'struct__CTL_CONTEXT',
        'struct__CTL_ENTRY', 'struct__CTL_INFO', 'struct__CTL_USAGE',
        'struct__FAF74743FBE1C8632047CFB668F7028A', 'struct__FILETIME',
        'struct__GUID', 'struct__IP_ADAPTER_INFO',
        'struct__IP_ADDR_STRING',
        'struct__LARGE_INTEGER___unnamed_type_u_', 'struct__LIST_ENTRY',
        'struct__OVERLAPPED', 'struct__PMD',
        'struct__PROCESS_INFORMATION', 'struct__RTL_CRITICAL_SECTION',
        'struct__RTL_CRITICAL_SECTION_DEBUG',
        'struct__SECURITY_ATTRIBUTES', 'struct__STARTUPINFOW',
        'struct__SecBuffer', 'struct__SecBufferDesc', 'struct__SecHandle',
        'struct__SecPkgContext_StreamSizes',
        'struct__SecPkgCred_SupportedProtocols', 'struct__TypeDescriptor',
        'struct__ULARGE_INTEGER___unnamed_type_u_', 'struct___qmutex_t',
        'struct___qsemaphore_t', 'struct___qthread_t', 'struct__cpinfo',
        'struct__iobuf', 'struct__qstring_char_',
        'struct__qstring_wchar_t_', 'struct__s_ThrowInfo',
        'struct__s__CatchableType', 'struct__s__CatchableTypeArray',
        'struct_addrinfo', 'struct_aes_key_t', 'struct_allprc_vars_t',
        'struct_asm_t', 'struct_auto_vars_t',
        'struct_backmap_initializer_t', 'struct_base_dispatcher_t',
        'struct_base_dispatcher_t__collect_cliopts____l2__ns_t',
        'struct_base_dispatcher_t_vtbl', 'struct_baseinit_vars_t',
        'struct_bf_key_t', 'struct_blkrange_t', 'struct_bytevec_t',
        'struct_call_atexits____l10__call_exits_req_t',
        'struct_call_atexits____l10__call_exits_req_t_vtbl',
        'struct_cancellable_op_t', 'struct_cfgopt_set_vec_t',
        'struct_cfgopt_t__num_range_t', 'struct_cfgopt_t__params_t',
        'struct_choose_ioport_device____l2__cb_parser_t',
        'struct_choose_ioport_device____l2__cb_parser_t_vtbl',
        'struct_client_handlers_list_t',
        'struct_client_handlers_list_t_vtbl', 'struct_code',
        'struct_codepoint_stream_t', 'struct_compat_t',
        'struct_compiler_info_t', 'struct_config_s', 'struct_config_t',
        'struct_config_t__autorun_plugin_info_t',
        'struct_config_t__def_proc_t', 'struct_config_t__tagged_hash_t',
        'struct_cp_data_t',
        'struct_create_bytearray_linput____l2__bytearray_linput_t',
        'struct_create_bytearray_linput____l2__bytearray_linput_t_vtbl',
        'struct_csconv_t', 'struct_ct_data_s',
        'struct_custom_data_vars_t', 'struct_dbctx_t',
        'struct_dbg_vars_t', 'struct_debugger_init_t',
        'struct_debugger_t', 'struct_demangler_vars_t',
        'struct_device_chooser_t', 'struct_device_chooser_t_vtbl',
        'struct_dirtreeimpl_vars_t', 'struct_dual_text_options_t',
        'struct_ea_range_sorter_t', 'struct_enc_pair_t',
        'struct_encoding_vars_t',
        'struct_enumerate_files____l2__old_enumerator_t',
        'struct_enumerate_files____l2__old_enumerator_t_vtbl',
        'struct_enumerate_sorted_files____l2__collector_t',
        'struct_enumerate_sorted_files____l2__collector_t_vtbl',
        'struct_event_handler_t', 'struct_event_handler_t_vtbl',
        'struct_event_source_t', 'struct_event_source_t_vtbl',
        'struct_fd_set', 'struct_file_in_zip64_read_info_s',
        'struct_filehandle_linput_t', 'struct_filehandle_linput_t_vtbl',
        'struct_fixup_vars_t', 'struct_fpvalue_t', 'struct_ftable_vars_t',
        'struct_func_vars_t', 'struct_gdl_vars_t',
        'struct_generic_client_t', 'struct_generic_client_t_vtbl',
        'struct_generic_linput_t', 'struct_gl_vars_t',
        'struct_group_vars_t', 'struct_gz_header_s', 'struct_gz_state',
        'struct_handler_data_t', 'struct_hit_counter_t', 'struct_hostent',
        'struct_hot_encoding_t', 'struct_iconv_cache',
        'struct_ida_tls_data_t', 'struct_idainfo',
        'struct_idarpc_stream_t',
        'struct_idarpc_stream_t__progress_cb_info_t',
        'struct_idarpc_stream_t_vtbl', 'struct_idatil_vars_t',
        'struct_in_addr',
        'struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_b_',
        'struct_in_addr___unnamed_type_S_un____unnamed_type_S_un_w_',
        'struct_incrementer_t', 'struct_inflate_linput_t',
        'struct_inflate_linput_t_vtbl', 'struct_inflate_state',
        'struct_internal_state', 'struct_interval', 'struct_ints_vars_t',
        'struct_irs_cancellable_op_t', 'struct_iso2022_esc_t',
        'struct_kdata_t', 'struct_key_locker_t', 'struct_last_cp_data_t',
        'struct_lex_vars_t', 'struct_lexer_t', 'struct_lines_vars_t',
        'struct_linput_t', 'struct_loader_vars_t', 'struct_lowtil_vars_t',
        'struct_main_locker_t', 'struct_main_thread_initializer_t',
        'struct_mem_octet_stream_t', 'struct_mem_octet_stream_t_vtbl',
        'struct_metablock_info_t', 'struct_module_vars_t',
        'struct_mt_client_handlers_list_t',
        'struct_mt_client_handlers_list_t_vtbl', 'struct_name_vars_t',
        'struct_ncache_vars_t', 'struct_netlink', 'struct_netnode',
        'struct_netnode__key_info_t', 'struct_netnode__mapper_t',
        'struct_netnode__mapper_t__blobdesc_t',
        'struct_netnode__mapper_t_vtbl', 'struct_netnode_vars_t',
        'struct_network_client_handler_t',
        'struct_network_client_handler_t_vtbl', 'struct_octet_stream_t',
        'struct_octet_stream_t_vtbl',
        'struct_op_t___unnamed_tag____unnamed_type_addr_shorts_',
        'struct_op_t___unnamed_tag____unnamed_type_specval_shorts_',
        'struct_op_t___unnamed_tag____unnamed_type_value_shorts_',
        'struct_plugins_vars_t', 'struct_problems_vars_t',
        'struct_processor_t', 'struct_procmod_t',
        'struct_qstack_cancellable_op_t_',
        'struct_qstack_unsigned___int64_', 'struct_qstring_simple_init_t',
        'struct_qvector__SecBuffer_', 'struct_qvector__SecBuffer__P_',
        'struct_qvector__qstring_char___', 'struct_qvector_bool_',
        'struct_qvector_bytevec_t_', 'struct_qvector_cancellable_op_t_',
        'struct_qvector_char_', 'struct_qvector_char__P_',
        'struct_qvector_char_const__P_',
        'struct_qvector_config_t__autorun_plugin_info_t_',
        'struct_qvector_config_t__def_proc_t_',
        'struct_qvector_event_handler_t__P_',
        'struct_qvector_event_source_t__P_', 'struct_qvector_ioport_t_',
        'struct_qvector_qvector_char_const__P___',
        'struct_qvector_range_cache_t_', 'struct_qvector_rangecb_t__P_',
        'struct_qvector_rangecb_undo_record_t__args_t_',
        'struct_qvector_rangeset_t__P_',
        'struct_qvector_rangeset_undo_record_t__action_t_',
        'struct_qvector_rpc_packet_type_desc_t_',
        'struct_qvector_unsigned___int64_', 'struct_qvector_void__P_',
        'struct_qvector_void____cdecl_P__void__',
        'struct_qvector_wchar_t_', 'struct_qwpath_t',
        'struct_qwstringi_less', 'struct_range_cache_t',
        'struct_range_ea_sorter_t', 'struct_range_info_t',
        'struct_range_t', 'struct_range_visitor2_t',
        'struct_range_visitor2_t_vtbl', 'struct_rangecb_t',
        'struct_rangecb_undo_record_t',
        'struct_rangecb_undo_record_t__args_t', 'struct_ranges_cache_t',
        'struct_rangeset_t', 'struct_rangeset_undo_record_t',
        'struct_rangeset_undo_record_t__action_t', 'struct_rangevec_t',
        'struct_read_ioports____l2__cb_fallback_t',
        'struct_read_ioports____l2__cb_fallback_t_vtbl',
        'struct_rec_iconv_t', 'struct_recording_rpc_engine_t',
        'struct_recording_rpc_engine_t_vtbl',
        'struct_rpc_connection_params_t', 'struct_rpc_engine_t',
        'struct_rpc_engine_t_vtbl', 'struct_rpc_packet_data_t',
        'struct_rpc_packet_data_t_vtbl', 'struct_rpc_packet_t',
        'struct_rpc_packet_type_desc_t', 'struct_schannel_buffer_t',
        'struct_seg_vars_t', 'struct_segregs_vars_t', 'struct_servent',
        'struct_sha1_ctx_t', 'struct_sha256_ctx', 'struct_signs_vars_t',
        'struct_snippets_vars_t', 'struct_sockaddr', 'struct_sockaddr_in',
        'struct_static_tree_desc_s',
        'struct_std___Alloc_construct_ptr_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_int_void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____',
        'struct_std___Alloc_construct_ptr_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____',
        'struct_std___Char_traits_char16_t_unsigned_short_',
        'struct_std___Char_traits_char32_t_unsigned_int_',
        'struct_std___Char_traits_char_int_',
        'struct_std___Char_traits_wchar_t_unsigned_short_',
        'struct_std___Compressed_pair_qwstringi_less_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1__1_',
        'struct_std___Compressed_pair_std__allocator_char16_t__std___String_val_std___Simple_types_char16_t____1_',
        'struct_std___Compressed_pair_std__allocator_char32_t__std___String_val_std___Simple_types_char32_t____1_',
        'struct_std___Compressed_pair_std__allocator_char__std___String_val_std___Simple_types_char____1_',
        'struct_std___Compressed_pair_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P____std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______1_',
        'struct_std___Compressed_pair_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t__________std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t____________1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1_',
        'struct_std___Compressed_pair_std__allocator_wchar_t__std___String_val_std___Simple_types_wchar_t____1_',
        'struct_std___Compressed_pair_std__equal_to_unsigned___int64__float_1_',
        'struct_std___Compressed_pair_std__hash_unsigned___int64__std___Compressed_pair_std__equal_to_unsigned___int64__float_1__1_',
        'struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char________1__1_',
        'struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char__________1__1_',
        'struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______________1__1_',
        'struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______1__1_',
        'struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_char_const__P_const__P_void__P____std___Tree_val_std___Tree_simple_types_char_const__P_const__P____1__1_',
        'struct_std___Compressed_pair_std__less_char_const__P_const__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P____std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______1__1_',
        'struct_std___Compressed_pair_std__less_int__std___Compressed_pair_std__allocator_std___Tree_node_int_void__P____std___Tree_val_std___Tree_simple_types_int____1__1_',
        'struct_std___Compressed_pair_std__less_network_client_handler_t__P__std___Compressed_pair_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P____std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______1__1_',
        'struct_std___Conditionally_enabled_hash_unsigned___int64_1_',
        'struct_std___Default_allocator_traits_std__allocator_char16_t___',
        'struct_std___Default_allocator_traits_std__allocator_char32_t___',
        'struct_std___Default_allocator_traits_std__allocator_char___',
        'struct_std___Default_allocator_traits_std__allocator_char_const__P_const__P___',
        'struct_std___Default_allocator_traits_std__allocator_int___',
        'struct_std___Default_allocator_traits_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_int_void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const___qstring_char_______',
        'struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________',
        'struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________',
        'struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_char__const__unsigned___int64_____',
        'struct_std___Default_allocator_traits_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______',
        'struct_std___Default_allocator_traits_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____',
        'struct_std___Default_allocator_traits_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____',
        'struct_std___Default_allocator_traits_std__allocator_std__pair_unsigned___int64_const__bytevec_t_____',
        'struct_std___Default_allocator_traits_std__allocator_wchar_t___',
        'struct_std___Hash_find_last_result_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_',
        'struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0___',
        'struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Clear_guard',
        'struct_std___Hash_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0______Range_eraser',
        'struct_std___Hash_vec_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________',
        'struct_std___In_place_key_extract_map__qstring_wchar_t__std__pair__qstring_wchar_t___qstring_wchar_t_____',
        'struct_std___In_place_key_extract_map_char_const__P_const__P_std__pair_char_const__P_const__P_unsigned___int64___',
        'struct_std___In_place_key_extract_set_char_const__P_const__P_char_const__P_const__P_',
        'struct_std___In_place_key_extract_set_int_int_',
        'struct_std___List_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______',
        'struct_std___List_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______',
        'struct_std___List_node_emplace_op2_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____',
        'struct_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_',
        'struct_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___',
        'struct_std___List_unchecked_const_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t______std___Iterator_base0_',
        'struct_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_______',
        'struct_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_____',
        'struct_std___Narrow_char_traits_char_int_',
        'struct_std___Simple_types_std__pair_unsigned___int64_const__bytevec_t___',
        'struct_std___String_val_std___Simple_types_char16_t___',
        'struct_std___String_val_std___Simple_types_char32_t___',
        'struct_std___String_val_std___Simple_types_char___',
        'struct_std___String_val_std___Simple_types_wchar_t___',
        'struct_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0_',
        'struct_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0_',
        'struct_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0_',
        'struct_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0_',
        'struct_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0_',
        'struct_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0_',
        'struct_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0_',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P_____',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______',
        'struct_std___Tree_find_result_std___Tree_node_char_const__P_const__P_void__P___P_',
        'struct_std___Tree_find_result_std___Tree_node_int_void__P___P_',
        'struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_',
        'struct_std___Tree_find_result_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_',
        'struct_std___Tree_find_result_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_',
        'struct_std___Tree_find_result_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_',
        'struct_std___Tree_id_std___Tree_node_char_const__P_const__P_void__P___P_',
        'struct_std___Tree_id_std___Tree_node_int_void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_______',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_______',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______',
        'struct_std___Tree_node_char_const__P_const__P_void__P_',
        'struct_std___Tree_node_int_void__P_',
        'struct_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_',
        'struct_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_',
        'struct_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_',
        'struct_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_',
        'struct_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_',
        'struct_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_',
        'struct_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_',
        'struct_std___Tree_std___Tmap_traits__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char______0___',
        'struct_std___Tree_std___Tmap_traits__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char________0___',
        'struct_std___Tree_std___Tmap_traits__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char____________0___',
        'struct_std___Tree_std___Tmap_traits__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64____0___',
        'struct_std___Tree_std___Tmap_traits__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t______0___',
        'struct_std___Tree_std___Tmap_traits_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64____0___',
        'struct_std___Tree_std___Tmap_traits_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P____0___',
        'struct_std___Tree_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0___',
        'struct_std___Tree_std___Tset_traits_int_std__less_int__std__allocator_int__0___',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_int_void__P_____',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____',
        'struct_std___Tree_temp_node_alloc_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_int_void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____',
        'struct_std___Tree_temp_node_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P____std___Iterator_base0_',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int____std___Iterator_base0_',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64______std___Iterator_base0_',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t________std___Iterator_base0_',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64______std___Iterator_base0_',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P______std___Iterator_base0_',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_________',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_______',
        'struct_std___Tree_val_std___Tree_simple_types_char_const__P_const__P___',
        'struct_std___Tree_val_std___Tree_simple_types_int___',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const___qstring_char_______',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__qvector__qstring_char_________',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_char__const__unsigned___int64_____',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t_______',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64_____',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_network_client_handler_t__P_const___qthread_t__P_____',
        'struct_std___Tset_traits_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P__0_',
        'struct_std___Tset_traits_int_std__less_int__std__allocator_int__0_',
        'struct_std___Tuple_val__qstring_char__const__R_',
        'struct_std___Tuple_val_network_client_handler_t__P_const__R_',
        'struct_std___Tuple_val_unsigned___int64_const__R_',
        'struct_std___Uhash_choose_transparency_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64__void_',
        'struct_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64___',
        'struct_std___Umap_traits_unsigned___int64_bytevec_t_std___Uhash_compare_unsigned___int64_std__hash_unsigned___int64__std__equal_to_unsigned___int64____std__allocator_std__pair_unsigned___int64_const__bytevec_t____0_',
        'struct_std___Uninitialized_backout_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________P_',
        'struct_std___Vector_val_std___Simple_types_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________',
        'struct_std__allocator_char_const__P_const__P_',
        'struct_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___',
        'struct_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t_________',
        'struct_std__allocator_std___Tree_node_char_const__P_const__P_void__P___',
        'struct_std__allocator_std___Tree_node_int_void__P___',
        'struct_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P___',
        'struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P___',
        'struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P___',
        'struct_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___',
        'struct_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___',
        'struct_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___',
        'struct_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___',
        'struct_std__allocator_std__pair__qstring_char__const___qstring_char_____',
        'struct_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_______',
        'struct_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char___________',
        'struct_std__allocator_std__pair__qstring_char__const__unsigned___int64___',
        'struct_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_____',
        'struct_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64___',
        'struct_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P___',
        'struct_std__allocator_std__pair_unsigned___int64_const__bytevec_t___',
        'struct_std__allocator_traits_std__allocator_char16_t___',
        'struct_std__allocator_traits_std__allocator_char32_t___',
        'struct_std__allocator_traits_std__allocator_char___',
        'struct_std__allocator_traits_std__allocator_char_const__P_const__P___',
        'struct_std__allocator_traits_std__allocator_int___',
        'struct_std__allocator_traits_std__allocator_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P_____',
        'struct_std__allocator_traits_std__allocator_std___List_unchecked_iterator_std___List_val_std___List_simple_types_std__pair_unsigned___int64_const__bytevec_t___________',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_char_const__P_const__P_void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_int_void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const___qstring_char____void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__qvector__qstring_char______void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char__________void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P_____',
        'struct_std__allocator_traits_std__allocator_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P_____',
        'struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const___qstring_char_______',
        'struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________',
        'struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________',
        'struct_std__allocator_traits_std__allocator_std__pair__qstring_char__const__unsigned___int64_____',
        'struct_std__allocator_traits_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______',
        'struct_std__allocator_traits_std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____',
        'struct_std__allocator_traits_std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____',
        'struct_std__allocator_traits_std__allocator_std__pair_unsigned___int64_const__bytevec_t_____',
        'struct_std__allocator_traits_std__allocator_wchar_t___',
        'struct_std__basic_string_char16_t_std__char_traits_char16_t__std__allocator_char16_t___',
        'struct_std__basic_string_char32_t_std__char_traits_char32_t__std__allocator_char32_t___',
        'struct_std__basic_string_char_std__char_traits_char__std__allocator_char___',
        'struct_std__basic_string_wchar_t_std__char_traits_wchar_t__std__allocator_wchar_t___',
        'struct_std__equal_to_unsigned___int64_',
        'struct_std__hash_unsigned___int64_',
        'struct_std__initializer_list_char_const__P_const__P_',
        'struct_std__initializer_list_std__pair__qstring_wchar_t__const___qstring_wchar_t_____',
        'struct_std__initializer_list_std__pair_char_const__P_const__P_const_unsigned___int64___',
        'struct_std__initializer_list_std__pair_unsigned___int64_const__bytevec_t___',
        'struct_std__integer_sequence_unsigned___int64_',
        'struct_std__integer_sequence_unsigned___int64_0_',
        'struct_std__integral_constant_bool_0_',
        'struct_std__integral_constant_bool_1_',
        'struct_std__less__qstring_char___',
        'struct_std__less__qstring_wchar_t___',
        'struct_std__less_char_const__P_const__P_',
        'struct_std__less_network_client_handler_t__P_',
        'struct_std__list_std__pair_unsigned___int64_const__bytevec_t__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____',
        'struct_std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_______',
        'struct_std__map__qstring_char__qvector__qstring_char____std__less__qstring_char____std__allocator_std__pair__qstring_char__const__qvector__qstring_char_________',
        'struct_std__map__qstring_char__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char________std__less__qstring_char____std__allocator_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_____________',
        'struct_std__map__qstring_char__unsigned___int64_std__less__qstring_char____std__allocator_std__pair__qstring_char__const__unsigned___int64_____',
        'struct_std__map__qstring_wchar_t___qstring_wchar_t__qwstringi_less_std__allocator_std__pair__qstring_wchar_t__const___qstring_wchar_t_______',
        'struct_std__map_char_const__P_const__P_unsigned___int64_std__less_char_const__P_const__P__std__allocator_std__pair_char_const__P_const__P_const_unsigned___int64_____',
        'struct_std__map_network_client_handler_t__P___qthread_t__P_std__less_network_client_handler_t__P__std__allocator_std__pair_network_client_handler_t__P_const___qthread_t__P_____',
        'struct_std__numeric_limits___int64_',
        'struct_std__numeric_limits_unsigned___int64_',
        'struct_std__pair__qstring_char___P__qstring_char___P_',
        'struct_std__pair__qstring_char__const___qstring_char___',
        'struct_std__pair__qstring_char__const__qvector__qstring_char_____',
        'struct_std__pair__qstring_char__const__std__map__qstring_char___qstring_char__std__less__qstring_char____std__allocator_std__pair__qstring_char__const___qstring_char_________',
        'struct_std__pair__qstring_char__const__unsigned___int64_',
        'struct_std__pair__qstring_wchar_t___qstring_wchar_t___',
        'struct_std__pair__qstring_wchar_t__const___qstring_wchar_t___',
        'struct_std__pair_char_const__P_const__P_const_unsigned___int64_',
        'struct_std__pair_char_const__P_const__P_unsigned___int64_',
        'struct_std__pair_network_client_handler_t__P_const___qthread_t__P_',
        'struct_std__pair_std___List_node_std__pair_unsigned___int64_const__bytevec_t__void__P___P_bool_',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_char_const__P_const__P______bool_',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______bool_',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair__qstring_wchar_t__const___qstring_wchar_t__________bool_',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_char_const__P_const__P_const_unsigned___int64________bool_',
        'struct_std__pair_std___Tree_node_char_const__P_const__P_void__P___P_bool_',
        'struct_std__pair_std___Tree_node_int_void__P___P_bool_',
        'struct_std__pair_std___Tree_node_std__pair__qstring_char__const__unsigned___int64__void__P___P_bool_',
        'struct_std__pair_std___Tree_node_std__pair__qstring_wchar_t__const___qstring_wchar_t____void__P___P_bool_',
        'struct_std__pair_std___Tree_node_std__pair_char_const__P_const__P_const_unsigned___int64__void__P___P_bool_',
        'struct_std__pair_std___Tree_node_std__pair_network_client_handler_t__P_const___qthread_t__P__void__P___P_bool_',
        'struct_std__pair_unsigned___int64_const__bytevec_t_',
        'struct_std__pointer_traits_std__pair__qstring_char__const__unsigned___int64___P_',
        'struct_std__pointer_traits_std__pair__qstring_wchar_t__const___qstring_wchar_t_____P_',
        'struct_std__pointer_traits_std__pair_char_const__P_const__P_const_unsigned___int64___P_',
        'struct_std__pointer_traits_std__pair_network_client_handler_t__P_const___qthread_t__P___P_',
        'struct_std__pointer_traits_std__pair_unsigned___int64_const__bytevec_t___P_',
        'struct_std__set_char_const__P_const__P_std__less_char_const__P_const__P__std__allocator_char_const__P_const__P___',
        'struct_std__set_int_std__less_int__std__allocator_int___',
        'struct_std__tuple__qstring_char__const__R_',
        'struct_std__tuple_network_client_handler_t__P_const__R_',
        'struct_std__tuple_unsigned___int64_const__R_',
        'struct_std__unordered_map_unsigned___int64_bytevec_t_std__hash_unsigned___int64__std__equal_to_unsigned___int64__std__allocator_std__pair_unsigned___int64_const__bytevec_t_____',
        'struct_strlist_vars_t', 'struct_strlit_length_cache_t',
        'struct_struct_vars_t', 'struct_tcpip_stream_t',
        'struct_tcpip_stream_t_vtbl', 'struct_text_options_t',
        'struct_tifcache_vars_t', 'struct_timeval', 'struct_tinfo_vars_t',
        'struct_tls_stream_t', 'struct_tls_stream_t_vtbl',
        'struct_tm_unz_s', 'struct_token_t', 'struct_tree_desc_s',
        'struct_trusted_idb_vars_t', 'struct_tryblks_vars_t',
        'struct_undo_record_t', 'struct_undo_vars_t',
        'struct_unz64_file_pos_s', 'struct_unz64_s',
        'struct_unz_closer_t', 'struct_unz_file_info64_internal_s',
        'struct_unz_file_info64_s', 'struct_unz_file_info_s',
        'struct_unz_file_pos_s', 'struct_unz_global_info64_s',
        'struct_unz_global_info_s', 'struct_validator_t',
        'struct_vftable_vars_t', 'struct_win32_thread_t',
        'struct_z_stream_s', 'struct_zlib_filefunc64_32_def_s',
        'struct_zlib_filefunc64_def_s', 'struct_zlib_filefunc_def_s',
        'switch_info_t___unnamed_enum_SWITCH_INFO_VERSION_',
        'tagApplicationType', 'tagBANDSITECID', 'tagBINDSTATUS',
        'tagBINDSTRING', 'tagCALLCONV', 'tagCHANGEKIND', 'tagCLSCTX',
        'tagCONDITION_OPERATION', 'tagCONDITION_TYPE', 'tagDESCKIND',
        'tagDOMNodeType', 'tagExtentMode', 'tagFUNCKIND',
        'tagGLOBALOPT_EH_VALUES', 'tagMENUPOPUPSELECT', 'tagSYSKIND',
        'tagShutdownType', 'tagTYPEKIND', 'tagTYSPEC', 'tagURLZONE',
        'tagVARKIND', 'tagXMLEMEM_TYPE',
        'tls_stream_t__initialize_security_ctx____l2__state_t', 'uat_cp',
        'uat_culture', 'uat_current_culture', 'uat_none', 'uat_range',
        'uat_ucd_blk', 'uat_ucd_cat', 'ucdr_atom_type_t', 'undo_code_t',
        'undo_direction_t', 'undo_event_t', 'undo_param_t',
        'undo_state_t', 'union__2467CA9704E0472D4CCF1296A763D23A',
        'union__276C32F751912DA34557646A17DC8EC7',
        'union__33DC36BD25A1F06FF0DB9DC15CDFBE9B',
        'union__3DE6AE7B3A39657473E2A7515E87EC46',
        'union__3FED14670831426F78C1F126725788C0',
        'union__493D28877E64802C847645E3DAA9D4CA',
        'union__54E171B748F453B9C54515BD00780A14',
        'union__5D1D430279E45EFA7377026125DD642A',
        'union__5E8440A06A2AFEFEAE49F239CCFDFB49',
        'union__64629AA237317EA5DB00FDB53154C12F',
        'union__6E71FB17325AE2954BF4597A8A4FC61F',
        'union__8299423771E115C2E8FEC5C7170C0424',
        'union__873AABC3E23F76DAD852B3A5ED3D0239',
        'union__8F90F20BBE5791577C9666706E8030E8',
        'union__98217BFA50FEF0A74464688915FC94A9',
        'union__A5E17D51D1B600D0B7B66EE4F38162AD',
        'union__A79E5FD44D535857D5D82C32CF5C7F3D',
        'union__CA1F7F8D68BE4BE32BB567D2F056EF78',
        'union__CDAEAF5FCF1997B6248EE94570C87B85',
        'union__D0E407B3630C0B04C6372E28DCB32106',
        'union__D4468D5BF9897CF7F6CFF118171074C3',
        'union__D669CC2BBD58AEBA90A37169AF561FDB',
        'union__DD3B514C20105750B5B46F5AA1F9281B',
        'union__E728194B4577C1D54504CD54AE296467',
        'union__E9F0CCD17EA9996D87C5780C68234140',
        'union__F6C33E3B57865EFDC1EE4707AE4184E1', 'union__LARGE_INTEGER',
        'union__ULARGE_INTEGER', 'union_in_addr___unnamed_type_S_un_',
        'union_sha1_transform____l2__CHAR64LONG16',
        'union_std___String_val_std___Simple_types_char16_t______Bxty',
        'union_std___String_val_std___Simple_types_char32_t______Bxty',
        'union_std___String_val_std___Simple_types_char______Bxty',
        'union_std___String_val_std___Simple_types_wchar_t______Bxty']
    
    return locals()
