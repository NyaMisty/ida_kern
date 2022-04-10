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


class FunctionFactoryStub:
    def __getattr__(self, _):
      return ctypes.CFUNCTYPE(lambda y:y)

# libraries['FIXME_STUB'] explanation
# As you did not list (-l libraryname.so) a library that exports this function
# This is a non-working stub instead. 
# You can either re-run clan2py with -l /path/to/library.so
# Or manually fix this by comment the ctypes.CDLL loading
_libraries = {}
_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')


def ctypeslib_define():
    
    class struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true___true_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___),
    ]
    
    struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true___true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true___true_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true_),
    ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
        ('second', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
    ]
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
        ('second', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
    ]
    
    class struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true___true_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____),
    ]
    
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true___true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true___true_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true_),
    ]
    
    class struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true___true_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___),
    ]
    
    struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true___true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true___true_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true_),
    ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
        ('second', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
    ]
    
    class struct_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___value_compare(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false__(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true___true_),
         ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
        ('second', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
    ]
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
        ('second', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
    ]
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
        ('second', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
    ]
    
    class struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true___true_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___(Structure):
        pass
    
    class struct_std___Tree_node_std__pair_const_int__int___void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___),
    ]
    
    struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true___true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true___true_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true_),
    ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
        ('second', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
    ]
    
    class struct_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___value_compare(Structure):
        pass
    
    class struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____(Structure):
        pass
    
    class struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____(Structure):
        pass
    
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._pack_ = 1 # source:False
    struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____._fields_ = [
        ('first', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
        ('second', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
    ]
    
    class struct_std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false__(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true___true_),
         ]
    
    class struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
         ]
    
    class struct_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___value_compare(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false__(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true___true_),
         ]
    
    class struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____),
         ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
    ]
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true___true_(Structure):
        pass
    
    class struct_std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true_(Structure):
        pass
    
    class struct_std___Tree_val_std___Tree_simple_types_int__(Structure):
        pass
    
    class struct_std___Tree_node_int__void__P_(Structure):
        pass
    
    struct_std___Tree_val_std___Tree_simple_types_int__._pack_ = 1 # source:False
    struct_std___Tree_val_std___Tree_simple_types_int__._fields_ = [
        ('_Myhead', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
        ('_Mysize', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true_._fields_ = [
        ('_Myval2', struct_std___Tree_val_std___Tree_simple_types_int__),
    ]
    
    struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true___true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true___true_._fields_ = [
        ('_Myval2', struct_std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true_),
    ]
    
    class struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____(Structure):
        pass
    
    class struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___(Structure):
        pass
    
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___._pack_ = 1 # source:False
    struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____._pack_ = 1 # source:False
    struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____._fields_ = [
        ('first', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___),
        ('second', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___),
    ]
    
    class struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
         ]
    
    class struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
         ]
    
    class struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____),
         ]
    
    class struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____),
         ]
    
    class struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___P_(Structure):
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
    struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P__(Structure):
        pass
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
    ]
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_(Structure):
        pass
    
    class struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t(Structure):
        pass
    
    class struct_no_regs_t(Structure):
        pass
    
    struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t._pack_ = 1 # source:False
    struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t._fields_ = [
        ('regs', struct_no_regs_t),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('insn_cnt', ctypes.c_uint32),
    ]
    
    struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_._pack_ = 1 # source:False
    struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_._fields_ = [
        ('first', ctypes.c_uint64),
        ('second', struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t),
    ]
    
    std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___value_type),
    ]
    
    class struct_std__initializer_list_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__(Structure):
        pass
    
    struct_std__initializer_list_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)),
        ('_Last', ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)),
    ]
    
    class struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
         ]
    
    class struct_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__(Structure):
        pass
    
    class struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____),
         ]
    
    class struct_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___value_compare(Structure):
        pass
    
    class struct_std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false__(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true___true_),
         ]
    
    class struct_std___Tree_id_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P__(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____(Structure):
        pass
    
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._pack_ = 1 # source:False
    struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P__(Structure):
        pass
    
    class struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('current', struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___),
         ]
    
    class struct_std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_(Structure):
        pass
    
    struct_std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_._pack_ = 1 # source:False
    struct_std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__(Structure):
        pass
    
    class struct_qrefcnt_t_refcnted_regex_t_(Structure):
        pass
    
    class struct_refcnted_regex_t(Structure):
        pass
    
    struct_qrefcnt_t_refcnted_regex_t_._pack_ = 1 # source:False
    struct_qrefcnt_t_refcnted_regex_t_._fields_ = [
        ('ptr', ctypes.POINTER(struct_refcnted_regex_t)),
    ]
    
    class struct__qstring_char_(Structure):
        pass
    
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
    
    struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__._pack_ = 1 # source:False
    struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__._fields_ = [
        ('first', struct__qstring_char_),
        ('second', struct_qrefcnt_t_refcnted_regex_t_),
    ]
    
    std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___value_type),
    ]
    
    class struct_std__initializer_list_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___(Structure):
        pass
    
    struct_std__initializer_list_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)),
        ('_Last', ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)),
    ]
    
    class struct_std__pair_const_unsigned_long_long__unsigned_long_long_(Structure):
        pass
    
    struct_std__pair_const_unsigned_long_long__unsigned_long_long_._pack_ = 1 # source:False
    struct_std__pair_const_unsigned_long_long__unsigned_long_long_._fields_ = [
        ('first', ctypes.c_uint64),
        ('second', ctypes.c_uint64),
    ]
    
    std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('_Myval', std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___value_type),
    ]
    
    class struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___(Structure):
        pass
    
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___._pack_ = 1 # source:False
    struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
    ]
    
    class struct_std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false__(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true___true_),
         ]
    
    class struct_std__initializer_list_std__pair_const_unsigned_long_long__unsigned_long_long__(Structure):
        pass
    
    struct_std__initializer_list_std__pair_const_unsigned_long_long__unsigned_long_long__._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_const_unsigned_long_long__unsigned_long_long__._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)),
        ('_Last', ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)),
    ]
    
    class struct_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___(Structure):
        pass
    
    class struct_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long__(Structure):
        pass
    
    class struct_qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R__(Structure):
        pass
    
    
    # values for enumeration 'syntax_highlight_style'
    syntax_highlight_style__enumvalues = {
        0: 'HF_DEFAULT',
        1: 'HF_KEYWORD1',
        2: 'HF_KEYWORD2',
        3: 'HF_KEYWORD3',
        4: 'HF_STRING',
        5: 'HF_COMMENT',
        6: 'HF_PREPROC',
        7: 'HF_NUMBER',
        8: 'HF_MAX',
    }
    HF_DEFAULT = 0
    HF_KEYWORD1 = 1
    HF_KEYWORD2 = 2
    HF_KEYWORD3 = 3
    HF_STRING = 4
    HF_COMMENT = 5
    HF_PREPROC = 6
    HF_NUMBER = 7
    HF_MAX = 8
    syntax_highlight_style = ctypes.c_uint32 # enum
    struct_qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R__._pack_ = 1 # source:False
    struct_qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R__._fields_ = [
        ('array', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(syntax_highlight_style), ctypes.POINTER(struct__qstring_char_))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std___Tree_id_std___Tree_node_std__pair_const_int__int___void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_std__pair_const_int__int___void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_std__pair_const_int__int___void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std__allocator_std___Tree_node_std__pair_const_int__int___void__P__(Structure):
        pass
    
    class struct_qvector_long_long___P__syntax_highlight_style__P__const_char__P__(Structure):
        pass
    
    struct_qvector_long_long___P__syntax_highlight_style__P__const_char__P__._pack_ = 1 # source:False
    struct_qvector_long_long___P__syntax_highlight_style__P__const_char__P__._fields_ = [
        ('array', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(syntax_highlight_style), ctypes.c_char_p)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__map__qstring_char___qrefcnt_t_refcnted_regex_t__(Structure):
        pass
    
    struct_std__map__qstring_char___qrefcnt_t_refcnted_regex_t__._pack_ = 1 # source:False
    struct_std__map__qstring_char___qrefcnt_t_refcnted_regex_t__._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_qvector_ida_syntax_highlighter_t__keywords_style_t_(Structure):
        pass
    
    class struct_ida_syntax_highlighter_t__keywords_style_t(Structure):
        pass
    
    struct_qvector_ida_syntax_highlighter_t__keywords_style_t_._pack_ = 1 # source:False
    struct_qvector_ida_syntax_highlighter_t__keywords_style_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ida_syntax_highlighter_t__keywords_style_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_ida_syntax_highlighter_t__plain_char_ptr_t_(Structure):
        pass
    
    class struct_ida_syntax_highlighter_t__plain_char_ptr_t(Structure):
        pass
    
    struct_qvector_ida_syntax_highlighter_t__plain_char_ptr_t_._pack_ = 1 # source:False
    struct_qvector_ida_syntax_highlighter_t__plain_char_ptr_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ida_syntax_highlighter_t__plain_char_ptr_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__pair_const_int__int_(Structure):
        pass
    
    struct_std__pair_const_int__int_._pack_ = 1 # source:False
    struct_std__pair_const_int__int_._fields_ = [
        ('first', ctypes.c_int32),
        ('second', ctypes.c_int32),
    ]
    
    std___Tree_node_std__pair_const_int__int___void__P___value_type = struct_std__pair_const_int__int_
    struct_std___Tree_node_std__pair_const_int__int___void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_std__pair_const_int__int___void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('_Myval', std___Tree_node_std__pair_const_int__int___void__P___value_type),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t_(Structure):
        pass
    
    class struct_func_t(Structure):
        pass
    
    class struct_segment_t(Structure):
        pass
    
    class struct_simple_bfi_t(Structure):
        pass
    
    class struct_std__map_unsigned_long_long__unsigned_long_long_(Structure):
        pass
    
    struct_std__map_unsigned_long_long__unsigned_long_long_._pack_ = 1 # source:False
    struct_std__map_unsigned_long_long__unsigned_long_long_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    backward_flow_iterator_t_State__Ctrl___visited_t = struct_std__map_unsigned_long_long__unsigned_long_long_
    backward_flow_iterator_t_no_regs_t__simple_bfi_t___waiting_t = struct_std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t_._pack_ = 1 # source:False
    struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t_._fields_ = [
        ('cur_ea', ctypes.c_uint64),
        ('regs', ctypes.POINTER(struct_no_regs_t)),
        ('ctrl', ctypes.POINTER(struct_simple_bfi_t)),
        ('only_near', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('max_insn_cnt', ctypes.c_uint32),
        ('pfn', ctypes.POINTER(struct_func_t)),
        ('seg', ctypes.POINTER(struct_segment_t)),
        ('start_ea', ctypes.c_uint64),
        ('cur_end', ctypes.c_uint64),
        ('insn_cnt', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('visited', backward_flow_iterator_t_State__Ctrl___visited_t),
        ('waiting', backward_flow_iterator_t_no_regs_t__simple_bfi_t___waiting_t),
    ]
    
    class struct_std__initializer_list_std__pair_const_int__int__(Structure):
        pass
    
    struct_std__initializer_list_std__pair_const_int__int__._pack_ = 1 # source:False
    struct_std__initializer_list_std__pair_const_int__int__._fields_ = [
        ('_First', ctypes.POINTER(struct_std__pair_const_int__int_)),
        ('_Last', ctypes.POINTER(struct_std__pair_const_int__int_)),
    ]
    
    class struct_ida_movable_type_line_rendering_output_entry_t_(Structure):
        pass
    
    class struct_std___Tree_id_std___Tree_node_int__void__P___P_(Structure):
        pass
    
    struct_std___Tree_id_std___Tree_node_int__void__P___P_._pack_ = 1 # source:False
    struct_std___Tree_id_std___Tree_node_int__void__P___P_._fields_ = [
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
        ('_Child', std___Tree_child),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_qlist_ui_request_t__P___const_reverse_iterator(Structure):
        pass
    
    class struct_qrefcnt_t_qiterator_qrefcnt_t_source_file_t___(Structure):
        pass
    
    class struct_qiterator_qrefcnt_t_source_file_t__(Structure):
        pass
    
    struct_qrefcnt_t_qiterator_qrefcnt_t_source_file_t___._pack_ = 1 # source:False
    struct_qrefcnt_t_qiterator_qrefcnt_t_source_file_t___._fields_ = [
        ('ptr', ctypes.POINTER(struct_qiterator_qrefcnt_t_source_file_t__)),
    ]
    
    class struct_qrefcnt_t_qiterator_qrefcnt_t_source_item_t___(Structure):
        pass
    
    class struct_qiterator_qrefcnt_t_source_item_t__(Structure):
        pass
    
    struct_qrefcnt_t_qiterator_qrefcnt_t_source_item_t___._pack_ = 1 # source:False
    struct_qrefcnt_t_qiterator_qrefcnt_t_source_item_t___._fields_ = [
        ('ptr', ctypes.POINTER(struct_qiterator_qrefcnt_t_source_item_t__)),
    ]
    
    class struct_qvector_ida_syntax_highlighter_t__multicmt_t_(Structure):
        pass
    
    class struct_ida_syntax_highlighter_t__multicmt_t(Structure):
        pass
    
    struct_qvector_ida_syntax_highlighter_t__multicmt_t_._pack_ = 1 # source:False
    struct_qvector_ida_syntax_highlighter_t__multicmt_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ida_syntax_highlighter_t__multicmt_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__allocator_std___Tree_node_int__void__P__(Structure):
        pass
    
    struct_ida_syntax_highlighter_t__keywords_style_t._pack_ = 1 # source:False
    struct_ida_syntax_highlighter_t__keywords_style_t._fields_ = [
        ('keywords', struct_qvector_ida_syntax_highlighter_t__plain_char_ptr_t_),
        ('style', syntax_highlight_style),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_ida_syntax_highlighter_t__plain_char_ptr_t._pack_ = 1 # source:False
    struct_ida_syntax_highlighter_t__plain_char_ptr_t._fields_ = [
        ('ptr', ctypes.c_char_p),
    ]
    
    class struct_input_event_t__input_event_keyboard_data_t(Structure):
        pass
    
    struct_input_event_t__input_event_keyboard_data_t._pack_ = 1 # source:False
    struct_input_event_t__input_event_keyboard_data_t._fields_ = [
        ('key', ctypes.c_int32),
        ('text', ctypes.c_char * 8),
    ]
    
    class struct_input_event_t__input_event_shortcut_data_t(Structure):
        pass
    
    struct_input_event_t__input_event_shortcut_data_t._pack_ = 1 # source:False
    struct_input_event_t__input_event_shortcut_data_t._fields_ = [
        ('action_name', ctypes.c_char_p),
    ]
    
    class struct_qvector_line_rendering_output_entry_t__P_(Structure):
        pass
    
    class struct_line_rendering_output_entry_t(Structure):
        pass
    
    struct_qvector_line_rendering_output_entry_t__P_._pack_ = 1 # source:False
    struct_qvector_line_rendering_output_entry_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_line_rendering_output_entry_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__allocator_std__pair_const_int__int__(Structure):
        pass
    
    class struct_qiterator_qrefcnt_t_source_file_t___vtbl(Structure):
        pass
    
    class struct_qiterator_qrefcnt_t_source_item_t___vtbl(Structure):
        pass
    
    class struct_qlist_ui_request_t__P___reverse_iterator(Structure):
        pass
    
    class struct_input_event_t__input_event_mouse_data_t(Structure):
        pass
    
    
    # values for enumeration 'vme_button_t'
    vme_button_t__enumvalues = {
        0: 'VME_UNKNOWN',
        1: 'VME_LEFT_BUTTON',
        2: 'VME_RIGHT_BUTTON',
        3: 'VME_MID_BUTTON',
    }
    VME_UNKNOWN = 0
    VME_LEFT_BUTTON = 1
    VME_RIGHT_BUTTON = 2
    VME_MID_BUTTON = 3
    vme_button_t = ctypes.c_uint32 # enum
    struct_input_event_t__input_event_mouse_data_t._pack_ = 1 # source:False
    struct_input_event_t__input_event_mouse_data_t._fields_ = [
        ('x', ctypes.c_int32),
        ('y', ctypes.c_int32),
        ('button', vme_button_t),
    ]
    
    class struct_ida_movable_type_bitfield_type_data_t_(Structure):
        pass
    
    class struct_qlist_ui_request_t__P___const_iterator(Structure):
        pass
    
    class struct_ida_movable_type_typedef_type_data_t_(Structure):
        pass
    
    class struct_qvector_qvector_const_twinline_t__P__(Structure):
        pass
    
    class struct_qvector_const_twinline_t__P_(Structure):
        pass
    
    struct_qvector_qvector_const_twinline_t__P__._pack_ = 1 # source:False
    struct_qvector_qvector_const_twinline_t__P__._fields_ = [
        ('array', ctypes.POINTER(struct_qvector_const_twinline_t__P_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    qstring = struct__qstring_char_
    struct_ida_syntax_highlighter_t__multicmt_t._pack_ = 1 # source:False
    struct_ida_syntax_highlighter_t__multicmt_t._fields_ = [
        ('open_multicmt', qstring),
        ('close_multicmt', qstring),
    ]
    
    class struct_ida_movable_type_array_type_data_t_(Structure):
        pass
    
    class struct_ida_movable_type_call_stack_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_compiled_binpat_t_(Structure):
        pass
    
    class struct_ida_movable_type_update_bpt_info_t_(Structure):
        pass
    
    struct_qiterator_qrefcnt_t_source_file_t__._pack_ = 1 # source:False
    struct_qiterator_qrefcnt_t_source_file_t__._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    struct_qiterator_qrefcnt_t_source_item_t__._pack_ = 1 # source:False
    struct_qiterator_qrefcnt_t_source_item_t__._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_ida_movable_type_dirtree_cursor_t_(Structure):
        pass
    
    class struct_ida_movable_type_enum_type_data_t_(Structure):
        pass
    
    class struct_ida_movable_type_exception_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_scattered_aloc_t_(Structure):
        pass
    
    class struct_ida_movable_type_scattered_segm_t_(Structure):
        pass
    
    class struct_ida_movable_type_segm_move_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_xreflist_entry_t_(Structure):
        pass
    
    class struct_qlist_ui_request_t__P___listnode_t(Structure):
        pass
    
    struct_qlist_ui_request_t__P___listnode_t._pack_ = 1 # source:False
    struct_qlist_ui_request_t__P___listnode_t._fields_ = [
        ('next', ctypes.POINTER(struct_qlist_ui_request_t__P___listnode_t)),
        ('prev', ctypes.POINTER(struct_qlist_ui_request_t__P___listnode_t)),
    ]
    
    class struct__0B605D7B00AC5C12C153272CF5BD15AF(Structure):
        pass
    
    struct__0B605D7B00AC5C12C153272CF5BD15AF._pack_ = 1 # source:False
    struct__0B605D7B00AC5C12C153272CF5BD15AF._fields_ = [
        ('low', ctypes.c_uint16),
        ('high', ctypes.c_uint16),
    ]
    
    class struct__37EC8ECBAB39934116D1B12D6D12C693(Structure):
        pass
    
    class struct_llabel_t(Structure):
        pass
    
    class struct_stkpnt_t(Structure):
        pass
    
    class struct_regvar_t(Structure):
        pass
    
    class struct_range_t(Structure):
        pass
    
    class struct_regarg_t(Structure):
        pass
    
    struct__37EC8ECBAB39934116D1B12D6D12C693._pack_ = 1 # source:False
    struct__37EC8ECBAB39934116D1B12D6D12C693._fields_ = [
        ('frame', ctypes.c_uint64),
        ('frsize', ctypes.c_uint64),
        ('frregs', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('argsize', ctypes.c_uint64),
        ('fpd', ctypes.c_uint64),
        ('color', ctypes.c_uint32),
        ('pntqty', ctypes.c_uint32),
        ('points', ctypes.POINTER(struct_stkpnt_t)),
        ('regvarqty', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('regvars', ctypes.POINTER(struct_regvar_t)),
        ('llabelqty', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('llabels', ctypes.POINTER(struct_llabel_t)),
        ('regargqty', ctypes.c_int32),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('regargs', ctypes.POINTER(struct_regarg_t)),
        ('tailqty', ctypes.c_int32),
        ('PADDING_4', ctypes.c_ubyte * 4),
        ('tails', ctypes.POINTER(struct_range_t)),
    ]
    
    class struct__C21FB2E1BAA97F44BFD298211C4C916B(Structure):
        pass
    
    struct__C21FB2E1BAA97F44BFD298211C4C916B._pack_ = 1 # source:False
    struct__C21FB2E1BAA97F44BFD298211C4C916B._fields_ = [
        ('ptr', ctypes.CFUNCTYPE(ctypes.c_char)),
        ('adj', ctypes.c_uint64),
    ]
    
    class struct__EBE02DBEC342F8268AFE19180D75885B(Structure):
        pass
    
    struct__EBE02DBEC342F8268AFE19180D75885B._pack_ = 1 # source:False
    struct__EBE02DBEC342F8268AFE19180D75885B._fields_ = [
        ('owner', ctypes.c_uint64),
        ('refqty', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('referers', ctypes.POINTER(ctypes.c_uint64)),
    ]
    
    class struct_ida_movable_type_lochist_entry_t_(Structure):
        pass
    
    class struct_ida_movable_type_ptr_type_data_t_(Structure):
        pass
    
    class struct_ida_movable_type_register_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_tev_reg_value_t_(Structure):
        pass
    
    class struct_ida_movable_type_udt_type_data_t_(Structure):
        pass
    
    class struct_qvector_qrefcnt_t_source_item_t__(Structure):
        pass
    
    class struct_qrefcnt_t_source_item_t_(Structure):
        pass
    
    struct_qvector_qrefcnt_t_source_item_t__._pack_ = 1 # source:False
    struct_qvector_qrefcnt_t_source_item_t__._fields_ = [
        ('array', ctypes.POINTER(struct_qrefcnt_t_source_item_t_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_ida_movable_type_bpt_location_t_(Structure):
        pass
    
    class struct_ida_movable_type_locchange_md_t_(Structure):
        pass
    
    class struct_ida_movable_type_process_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_refinfo_desc_t_(Structure):
        pass
    
    class struct_ida_movable_type_tev_info_reg_t_(Structure):
        pass
    
    class struct_qlist_ui_request_t__P___iterator(Structure):
        pass
    
    class struct_qvector__qstring_unsigned_char__(Structure):
        pass
    
    class struct__qstring_unsigned_char_(Structure):
        pass
    
    struct_qvector__qstring_unsigned_char__._pack_ = 1 # source:False
    struct_qvector__qstring_unsigned_char__._fields_ = [
        ('array', ctypes.POINTER(struct__qstring_unsigned_char_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_ida_movable_type_debug_event_t_(Structure):
        pass
    
    class struct_ida_movable_type_enum_member_t_(Structure):
        pass
    
    class struct_ida_movable_type_memory_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_memreg_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_movbpt_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_string_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_sync_source_t_(Structure):
        pass
    
    class struct_ida_movable_type_try_handler_t_(Structure):
        pass
    
    class struct_qvector_qvector_const_char__P__(Structure):
        pass
    
    class struct_qvector_const_char__P_(Structure):
        pass
    
    struct_qvector_qvector_const_char__P__._pack_ = 1 # source:False
    struct_qvector_qvector_const_char__P__._fields_ = [
        ('array', ctypes.POINTER(struct_qvector_const_char__P_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_ida_movable_type_fixup_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_idc_global_t_(Structure):
        pass
    
    class struct_ida_movable_type_ioport_bit_t_(Structure):
        pass
    
    class struct_ida_movable_type_reg_access_t_(Structure):
        pass
    
    class struct_ida_movable_type_sreg_range_t_(Structure):
        pass
    
    class struct_ida_movable_type_til_symbol_t_(Structure):
        pass
    
    class struct_ida_movable_type_udt_member_t_(Structure):
        pass
    
    class struct_ida_movable_type_idc_value_t_(Structure):
        pass
    
    class struct_ida_movable_type_load_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_simd_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_type_attr_t_(Structure):
        pass
    
    class struct_ida_syntax_highlighter_t_vtbl(Structure):
        pass
    
    class struct_twinline_t(Structure):
        pass
    
    struct_line_rendering_output_entry_t._pack_ = 1 # source:False
    struct_line_rendering_output_entry_t._fields_ = [
        ('line', ctypes.POINTER(struct_twinline_t)),
        ('flags', ctypes.c_uint32),
        ('bg_color', ctypes.c_uint32),
        ('cpx', ctypes.c_int32),
        ('nchars', ctypes.c_int32),
    ]
    
    struct_std___Tree_node_int__void__P_._pack_ = 1 # source:False
    struct_std___Tree_node_int__void__P_._fields_ = [
        ('_Left', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
        ('_Parent', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
        ('_Right', ctypes.POINTER(struct_std___Tree_node_int__void__P_)),
        ('_Color', ctypes.c_char),
        ('_Isnil', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('_Myval', ctypes.c_int32),
    ]
    
    class struct_std__less_unsigned_long_long_(Structure):
        pass
    
    class struct_ida_movable_type_dbg_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_direntry_t_(Structure):
        pass
    
    class struct_ida_movable_type_idp_desc_t_(Structure):
        pass
    
    class struct_ida_movable_type_idp_name_t_(Structure):
        pass
    
    class struct_ida_movable_type_rangeset_t_(Structure):
        pass
    
    class struct_ida_movable_type_reg_info_t_(Structure):
        pass
    
    class struct_ida_movable_type_snapshot_t_(Structure):
        pass
    
    class struct_ida_movable_type_twinline_t_(Structure):
        pass
    
    class struct_qvector_const_rangeset_t__P_(Structure):
        pass
    
    class struct_rangeset_t(Structure):
        pass
    
    struct_qvector_const_rangeset_t__P_._pack_ = 1 # source:False
    struct_qvector_const_rangeset_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_rangeset_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_qvector_const_twinline_t__P_._pack_ = 1 # source:False
    struct_qvector_const_twinline_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_twinline_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_choose_ioport_parser_t_vtbl(Structure):
        pass
    
    class struct_ida_lowertype_helper_t_vtbl(Structure):
        pass
    
    class struct_ida_movable_type_argpart_t_(Structure):
        pass
    
    class struct_ida_movable_type_ea_name_t_(Structure):
        pass
    
    class struct_ida_movable_type_funcarg_t_(Structure):
        pass
    
    class struct_ida_movable_type_lochist_t_(Structure):
        pass
    
    class struct_ida_movable_type_modinfo_t_(Structure):
        pass
    
    class struct_ida_movable_type_valinfo_t_(Structure):
        pass
    
    class struct_qvector_qvector_long_long__(Structure):
        pass
    
    class struct_qvector_long_long_(Structure):
        pass
    
    struct_qvector_qvector_long_long__._pack_ = 1 # source:False
    struct_qvector_qvector_long_long__._fields_ = [
        ('array', ctypes.POINTER(struct_qvector_long_long_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_unsigned_long_long_(Structure):
        pass
    
    struct_qvector_unsigned_long_long_._pack_ = 1 # source:False
    struct_qvector_unsigned_long_long_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_uint64)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_struct_field_visitor_t_vtbl(Structure):
        pass
    
    class struct_enum_member_visitor_t_vtbl(Structure):
        pass
    
    class struct_ida_movable_type_argloc_t_(Structure):
        pass
    
    class struct_ida_movable_type_cliopt_t_(Structure):
        pass
    
    class struct_ida_movable_type_ioport_t_(Structure):
        pass
    
    class struct_ida_movable_type_jvalue_t_(Structure):
        pass
    
    class struct_ida_movable_type_regarg_t_(Structure):
        pass
    
    class struct_ida_movable_type_regobj_t_(Structure):
        pass
    
    class struct_ida_movable_type_regval_t_(Structure):
        pass
    
    class struct_ida_movable_type_regvar_t_(Structure):
        pass
    
    class struct_ida_movable_type_stkpnt_t_(Structure):
        pass
    
    class struct_ida_movable_type_tryblk_t_(Structure):
        pass
    
    class struct_ida_movable_type_valstr_t_(Structure):
        pass
    
    class struct_qvector__qstring_wchar_t__(Structure):
        pass
    
    class struct__qstring_wchar_t_(Structure):
        pass
    
    struct_qvector__qstring_wchar_t__._pack_ = 1 # source:False
    struct_qvector__qstring_wchar_t__._fields_ = [
        ('array', ctypes.POINTER(struct__qstring_wchar_t_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_call_stack_info_t_(Structure):
        pass
    
    class struct_call_stack_info_t(Structure):
        pass
    
    struct_qvector_call_stack_info_t_._pack_ = 1 # source:False
    struct_qvector_call_stack_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_call_stack_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_compiled_binpat_t_(Structure):
        pass
    
    class struct_compiled_binpat_t(Structure):
        pass
    
    struct_qvector_compiled_binpat_t_._pack_ = 1 # source:False
    struct_qvector_compiled_binpat_t_._fields_ = [
        ('array', ctypes.POINTER(struct_compiled_binpat_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_update_bpt_info_t_(Structure):
        pass
    
    class struct_update_bpt_info_t(Structure):
        pass
    
    struct_qvector_update_bpt_info_t_._pack_ = 1 # source:False
    struct_qvector_update_bpt_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_update_bpt_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__initializer_list_int_(Structure):
        pass
    
    struct_std__initializer_list_int_._pack_ = 1 # source:False
    struct_std__initializer_list_int_._fields_ = [
        ('_First', ctypes.POINTER(ctypes.c_int32)),
        ('_Last', ctypes.POINTER(ctypes.c_int32)),
    ]
    
    class struct_user_defined_prefix_t_vtbl(Structure):
        pass
    
    class struct_action_ctx_base_cur_sel_t(Structure):
        pass
    
    class struct_twinpos_t(Structure):
        pass
    
    class struct_place_t(Structure):
        pass
    
    struct_twinpos_t._pack_ = 1 # source:False
    struct_twinpos_t._fields_ = [
        ('at', ctypes.POINTER(struct_place_t)),
        ('x', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_action_ctx_base_cur_sel_t._pack_ = 1 # source:False
    struct_action_ctx_base_cur_sel_t._fields_ = [
        ('from', struct_twinpos_t),
        ('to', struct_twinpos_t),
    ]
    
    class struct_const_aloc_visitor_t_vtbl(Structure):
        pass
    
    class struct_graph_node_visitor_t_vtbl(Structure):
        pass
    
    class struct_graph_path_visitor_t_vtbl(Structure):
        pass
    
    class struct_ida_movable_type_catch_t_(Structure):
        pass
    
    class struct_ida_movable_type_point_t_(Structure):
        pass
    
    class struct_ida_movable_type_range_t_(Structure):
        pass
    
    class struct_ida_movable_type_tinfo_t_(Structure):
        pass
    
    class struct_ida_movable_type_token_t_(Structure):
        pass
    
    class struct_post_event_visitor_t_vtbl(Structure):
        pass
    
    class struct_qvector_dirtree_cursor_t_(Structure):
        pass
    
    class struct_dirtree_cursor_t(Structure):
        pass
    
    struct_qvector_dirtree_cursor_t_._pack_ = 1 # source:False
    struct_qvector_dirtree_cursor_t_._fields_ = [
        ('array', ctypes.POINTER(struct_dirtree_cursor_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_exception_info_t_(Structure):
        pass
    
    class struct_exception_info_t(Structure):
        pass
    
    struct_qvector_exception_info_t_._pack_ = 1 # source:False
    struct_qvector_exception_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_exception_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_scattered_segm_t_(Structure):
        pass
    
    class struct_scattered_segm_t(Structure):
        pass
    
    struct_qvector_scattered_segm_t_._pack_ = 1 # source:False
    struct_qvector_scattered_segm_t_._fields_ = [
        ('array', ctypes.POINTER(struct_scattered_segm_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_segm_move_info_t_(Structure):
        pass
    
    class struct_segm_move_info_t(Structure):
        pass
    
    struct_qvector_segm_move_info_t_._pack_ = 1 # source:False
    struct_qvector_segm_move_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_segm_move_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_selection_item_t_(Structure):
        pass
    
    class struct_selection_item_t(Structure):
        pass
    
    struct_qvector_selection_item_t_._pack_ = 1 # source:False
    struct_qvector_selection_item_t_._fields_ = [
        ('array', ctypes.POINTER(struct_selection_item_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_xreflist_entry_t_(Structure):
        pass
    
    class struct_xreflist_entry_t(Structure):
        pass
    
    struct_qvector_xreflist_entry_t_._pack_ = 1 # source:False
    struct_qvector_xreflist_entry_t_._fields_ = [
        ('array', ctypes.POINTER(struct_xreflist_entry_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_std__less__qstring_char__(Structure):
        pass
    
    class struct_syntax_highlighter_t_vtbl(Structure):
        pass
    
    class struct_altadjust_visitor_t_vtbl(Structure):
        pass
    
    class struct_cancellable_graph_t_vtbl(Structure):
        pass
    
    class struct_custom_refinfo_handler_t(Structure):
        pass
    
    class struct_refinfo_t(Structure):
        pass
    
    struct_custom_refinfo_handler_t._pack_ = 1 # source:False
    struct_custom_refinfo_handler_t._fields_ = [
        ('cbsize', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('desc', ctypes.c_char_p),
        ('props', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('gen_expr', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(struct__qstring_char_), ctypes.c_uint64, ctypes.c_int32, ctypes.POINTER(struct_refinfo_t), ctypes.c_uint64, ctypes.POINTER(ctypes.c_int64), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64), ctypes.c_int32)),
        ('calc_reference_data', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(ctypes.c_uint64), ctypes.c_uint64, ctypes.POINTER(struct_refinfo_t), ctypes.c_int64)),
        ('get_format', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct__qstring_char_))),
    ]
    
    class struct_custom_viewer_handlers_t(Structure):
        pass
    
    class struct_TWidget(Structure):
        pass
    
    class struct_lochist_entry_t(Structure):
        pass
    
    class struct_locchange_md_t(Structure):
        pass
    
    class struct_view_mouse_event_t(Structure):
        pass
    
    struct_custom_viewer_handlers_t._pack_ = 1 # source:False
    struct_custom_viewer_handlers_t._fields_ = [
        ('cb', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('keyboard', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None))),
        ('popup', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))),
        ('mouse_moved', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.POINTER(struct_view_mouse_event_t), ctypes.POINTER(None))),
        ('click', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.POINTER(None))),
        ('dblclick', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.POINTER(None))),
        ('curpos', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))),
        ('close', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))),
        ('help', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))),
        ('adjust_place', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(None))),
        ('get_place_xcoord', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_place_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None))),
        ('location_changed', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_locchange_md_t), ctypes.POINTER(None))),
        ('can_navigate', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_locchange_md_t), ctypes.POINTER(None))),
    ]
    
    class struct_ida_movable_type_edge_t_(Structure):
        pass
    
    class struct_ida_movable_type_func_t_(Structure):
        pass
    
    class struct_ida_movable_type_jarr_t_(Structure):
        pass
    
    class struct_ida_movable_type_jobj_t_(Structure):
        pass
    
    class struct_ida_movable_type_rect_t_(Structure):
        pass
    
    class struct_ida_syntax_highlighter_t(Structure):
        pass
    
    external_colorizers_t = struct_qvector_long_long___P__syntax_highlight_style__P__const_char__P__
    external_ident_colorizers_t = struct_qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R__
    class struct_qvector__qstring_char__(Structure):
        pass
    
    struct_qvector__qstring_char__._pack_ = 1 # source:False
    struct_qvector__qstring_char__._fields_ = [
        ('array', ctypes.POINTER(struct__qstring_char_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    qstrvec_t = struct_qvector__qstring_char__
    ida_syntax_highlighter_t__multicmtvec_t = struct_qvector_ida_syntax_highlighter_t__multicmt_t_
    ida_syntax_highlighter_t__keywords_t = struct_qvector_ida_syntax_highlighter_t__keywords_style_t_
    struct_ida_syntax_highlighter_t._pack_ = 1 # source:False
    struct_ida_syntax_highlighter_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('keyword_memory', qstrvec_t),
        ('keywords', ida_syntax_highlighter_t__keywords_t),
        ('open_cmt', qstring),
        ('multicmts', ida_syntax_highlighter_t__multicmtvec_t),
        ('literal_closer', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('text_color', syntax_highlight_style),
        ('comment_color', syntax_highlight_style),
        ('string_color', syntax_highlight_style),
        ('preprocessor_color', syntax_highlight_style),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('external_colorizers', external_colorizers_t),
        ('external_ident_colorizers', external_ident_colorizers_t),
        ('input', ctypes.c_char_p),
        ('pending', ctypes.c_char_p),
        ('style', syntax_highlight_style),
        ('open_strconst', ctypes.c_char),
        ('close_strconst', ctypes.c_char),
        ('open_chrconst', ctypes.c_char),
        ('close_chrconst', ctypes.c_char),
        ('escape_char', ctypes.c_char),
        ('preprocessor_char', ctypes.c_char),
        ('PADDING_3', ctypes.c_ubyte * 6),
    ]
    
    class struct_lines_rendering_output_t(Structure):
        pass
    
    line_rendering_output_entries_refs_t = struct_qvector_line_rendering_output_entry_t__P_
    struct_lines_rendering_output_t._pack_ = 1 # source:False
    struct_lines_rendering_output_t._fields_ = [
        ('entries', line_rendering_output_entries_refs_t),
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_macro_constructor_t_vtbl(Structure):
        pass
    
    class struct_qrefcnt_t_source_file_t_(Structure):
        pass
    
    class struct_source_file_t(Structure):
        pass
    
    struct_qrefcnt_t_source_file_t_._pack_ = 1 # source:False
    struct_qrefcnt_t_source_file_t_._fields_ = [
        ('ptr', ctypes.POINTER(struct_source_file_t)),
    ]
    
    class struct_source_item_t(Structure):
        pass
    
    struct_qrefcnt_t_source_item_t_._pack_ = 1 # source:False
    struct_qrefcnt_t_source_item_t_._fields_ = [
        ('ptr', ctypes.POINTER(struct_source_item_t)),
    ]
    
    class struct_qvector_channel_redir_t_(Structure):
        pass
    
    class struct_channel_redir_t(Structure):
        pass
    
    struct_qvector_channel_redir_t_._pack_ = 1 # source:False
    struct_qvector_channel_redir_t_._fields_ = [
        ('array', ctypes.POINTER(struct_channel_redir_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_lochist_entry_t_(Structure):
        pass
    
    struct_qvector_lochist_entry_t_._pack_ = 1 # source:False
    struct_qvector_lochist_entry_t_._fields_ = [
        ('array', ctypes.POINTER(struct_lochist_entry_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_register_info_t_(Structure):
        pass
    
    class struct_register_info_t(Structure):
        pass
    
    struct_qvector_register_info_t_._pack_ = 1 # source:False
    struct_qvector_register_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_register_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_tev_reg_value_t_(Structure):
        pass
    
    class struct_tev_reg_value_t(Structure):
        pass
    
    struct_qvector_tev_reg_value_t_._pack_ = 1 # source:False
    struct_qvector_tev_reg_value_t_._fields_ = [
        ('array', ctypes.POINTER(struct_tev_reg_value_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_range_marker_suspender_t(Structure):
        pass
    
    struct_range_marker_suspender_t._pack_ = 1 # source:False
    struct_range_marker_suspender_t._fields_ = [
        ('backup', ctypes.CFUNCTYPE(None, ctypes.c_uint64, ctypes.c_uint64)),
    ]
    
    class struct_screen_graph_selection_t(Structure):
        pass
    
    struct_screen_graph_selection_t._pack_ = 1 # source:False
    struct_screen_graph_selection_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_valstr_t__flatten_args_t(Structure):
        pass
    
    class struct_valstr_t(Structure):
        pass
    
    struct_valstr_t__flatten_args_t._pack_ = 1 # source:False
    struct_valstr_t__flatten_args_t._fields_ = [
        ('may_not_collapse', ctypes.POINTER(struct_valstr_t)),
        ('ptvf', ctypes.c_int32),
        ('max_length', ctypes.c_int32),
        ('margin', ctypes.c_int32),
        ('indent', ctypes.c_int32),
    ]
    
    class struct_qvector_unsigned_char_(Structure):
        pass
    
    struct_qvector_unsigned_char_._pack_ = 1 # source:False
    struct_qvector_unsigned_char_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_ubyte)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct__qstring_unsigned_char_._pack_ = 1 # source:False
    struct__qstring_unsigned_char_._fields_ = [
        ('body', struct_qvector_unsigned_char_),
    ]
    
    class struct_ida_movable_type_bpt_t_(Structure):
        pass
    
    class struct_ida_movable_type_kvp_t_(Structure):
        pass
    
    class struct_ida_movable_type_seh_t_(Structure):
        pass
    
    class struct_ioports_fallback_t_vtbl(Structure):
        pass
    
    class struct_launch_process_params_t(Structure):
        pass
    
    struct_launch_process_params_t._pack_ = 1 # source:False
    struct_launch_process_params_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('path', ctypes.c_char_p),
        ('args', ctypes.c_char_p),
        ('in_handle', ctypes.c_int64),
        ('out_handle', ctypes.c_int64),
        ('err_handle', ctypes.c_int64),
        ('env', ctypes.c_char_p),
        ('startdir', ctypes.c_char_p),
        ('info', ctypes.POINTER(None)),
    ]
    
    class struct_lines_rendering_input_t(Structure):
        pass
    
    class struct_synced_group_t(Structure):
        pass
    
    sections_lines_refs_t = struct_qvector_qvector_const_twinline_t__P__
    struct_lines_rendering_input_t._pack_ = 1 # source:False
    struct_lines_rendering_input_t._fields_ = [
        ('cb', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('sections_lines', sections_lines_refs_t),
        ('sync_group', ctypes.POINTER(struct_synced_group_t)),
    ]
    
    class struct_lowertype_helper_t_vtbl(Structure):
        pass
    
    class struct_qvector_const_bpt_t__P_(Structure):
        pass
    
    class struct_bpt_t(Structure):
        pass
    
    struct_qvector_const_bpt_t__P_._pack_ = 1 # source:False
    struct_qvector_const_bpt_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_bpt_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_group_crinfo_t_(Structure):
        pass
    
    class struct_group_crinfo_t(Structure):
        pass
    
    struct_qvector_group_crinfo_t_._pack_ = 1 # source:False
    struct_qvector_group_crinfo_t_._fields_ = [
        ('array', ctypes.POINTER(struct_group_crinfo_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_process_info_t_(Structure):
        pass
    
    class struct_process_info_t(Structure):
        pass
    
    struct_qvector_process_info_t_._pack_ = 1 # source:False
    struct_qvector_process_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_process_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_qbasic_block_t_(Structure):
        pass
    
    class struct_qbasic_block_t(Structure):
        pass
    
    struct_qvector_qbasic_block_t_._pack_ = 1 # source:False
    struct_qvector_qbasic_block_t_._fields_ = [
        ('array', ctypes.POINTER(struct_qbasic_block_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_refinfo_desc_t_(Structure):
        pass
    
    class struct_refinfo_desc_t(Structure):
        pass
    
    struct_qvector_refinfo_desc_t_._pack_ = 1 # source:False
    struct_qvector_refinfo_desc_t_._fields_ = [
        ('array', ctypes.POINTER(struct_refinfo_desc_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_tev_info_reg_t_(Structure):
        pass
    
    class struct_tev_info_reg_t(Structure):
        pass
    
    struct_qvector_tev_info_reg_t_._pack_ = 1 # source:False
    struct_qvector_tev_info_reg_t_._fields_ = [
        ('array', ctypes.POINTER(struct_tev_info_reg_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_simpleline_place_t_vtbl(Structure):
        pass
    
    class struct_srcinfo_provider_t_vtbl(Structure):
        pass
    
    class struct_user_graph_place_t_vtbl(Structure):
        pass
    
    class struct_argtinfo_helper_t_vtbl(Structure):
        pass
    
    class struct_choose_ioport_parser_t(Structure):
        pass
    
    struct_choose_ioport_parser_t._pack_ = 1 # source:False
    struct_choose_ioport_parser_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_choose_ioport_parser_t_vtbl)),
    ]
    
    class struct_custom_data_type_ids_t(Structure):
        pass
    
    struct_custom_data_type_ids_t._pack_ = 1 # source:False
    struct_custom_data_type_ids_t._fields_ = [
        ('dtid', ctypes.c_int16),
        ('fids', ctypes.c_int16 * 8),
    ]
    
    class struct_dirtree_visitor_t_vtbl(Structure):
        pass
    
    class struct_dynamic_register_set_t(Structure):
        pass
    
    register_info_vec_t = struct_qvector_register_info_t_
    struct_qvector_const_char__P_._pack_ = 1 # source:False
    struct_qvector_const_char__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_char_p)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    dynamic_register_set_t__const_char_vec_t = struct_qvector_const_char__P_
    struct_dynamic_register_set_t._pack_ = 1 # source:False
    struct_dynamic_register_set_t._fields_ = [
        ('ri_vec', register_info_vec_t),
        ('strvec', qstrvec_t),
        ('classname_ptrs', dynamic_register_set_t__const_char_vec_t),
        ('bit_strings_ptrs_vec', struct_qvector_qvector_const_char__P__),
    ]
    
    class struct_extlang_visitor_t_vtbl(Structure):
        pass
    
    class struct_file_enumerator_t_vtbl(Structure):
        pass
    
    class struct_func_parent_iterator_t(Structure):
        pass
    
    struct_func_parent_iterator_t._pack_ = 1 # source:False
    struct_func_parent_iterator_t._fields_ = [
        ('fnt', ctypes.POINTER(struct_func_t)),
        ('idx', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_highlighter_cbs_t_vtbl(Structure):
        pass
    
    class struct_ida_lowertype_helper_t(Structure):
        pass
    
    class struct_tinfo_t(Structure):
        pass
    
    struct_ida_lowertype_helper_t._pack_ = 1 # source:False
    struct_ida_lowertype_helper_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('tif', ctypes.POINTER(struct_tinfo_t)),
        ('ea', ctypes.c_uint64),
        ('purged_bytes', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_janitor_t_linput_t__P_(Structure):
        pass
    
    class struct_linput_t(Structure):
        pass
    
    struct_janitor_t_linput_t__P_._pack_ = 1 # source:False
    struct_janitor_t_linput_t__P_._fields_ = [
        ('resource', ctypes.POINTER(ctypes.POINTER(struct_linput_t))),
    ]
    
    class struct_qlist_ui_request_t__P_(Structure):
        pass
    
    struct_qlist_ui_request_t__P_._pack_ = 1 # source:False
    struct_qlist_ui_request_t__P_._fields_ = [
        ('node', struct_qlist_ui_request_t__P___listnode_t),
        ('length', ctypes.c_uint64),
    ]
    
    class struct_qvector_debug_event_t_(Structure):
        pass
    
    class struct_debug_event_t(Structure):
        pass
    
    struct_qvector_debug_event_t_._pack_ = 1 # source:False
    struct_qvector_debug_event_t_._fields_ = [
        ('array', ctypes.POINTER(struct_debug_event_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_enum_member_t_(Structure):
        pass
    
    class struct_enum_member_t(Structure):
        pass
    
    struct_qvector_enum_member_t_._pack_ = 1 # source:False
    struct_qvector_enum_member_t_._fields_ = [
        ('array', ctypes.POINTER(struct_enum_member_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_memory_info_t_(Structure):
        pass
    
    class struct_memory_info_t(Structure):
        pass
    
    struct_qvector_memory_info_t_._pack_ = 1 # source:False
    struct_qvector_memory_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_memory_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_memreg_info_t_(Structure):
        pass
    
    class struct_memreg_info_t(Structure):
        pass
    
    struct_qvector_memreg_info_t_._pack_ = 1 # source:False
    struct_qvector_memreg_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_memreg_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_movbpt_code_t_(Structure):
        pass
    
    
    # values for enumeration 'movbpt_code_t'
    movbpt_code_t__enumvalues = {
        0: 'MOVBPT_OK',
        1: 'MOVBPT_NOT_FOUND',
        2: 'MOVBPT_DEST_BUSY',
        3: 'MOVBPT_BAD_TYPE',
    }
    MOVBPT_OK = 0
    MOVBPT_NOT_FOUND = 1
    MOVBPT_DEST_BUSY = 2
    MOVBPT_BAD_TYPE = 3
    movbpt_code_t = ctypes.c_uint32 # enum
    struct_qvector_movbpt_code_t_._pack_ = 1 # source:False
    struct_qvector_movbpt_code_t_._fields_ = [
        ('array', ctypes.POINTER(movbpt_code_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_movbpt_info_t_(Structure):
        pass
    
    class struct_movbpt_info_t(Structure):
        pass
    
    struct_qvector_movbpt_info_t_._pack_ = 1 # source:False
    struct_qvector_movbpt_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_movbpt_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_snapshot_t__P_(Structure):
        pass
    
    class struct_snapshot_t(Structure):
        pass
    
    struct_qvector_snapshot_t__P_._pack_ = 1 # source:False
    struct_qvector_snapshot_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_snapshot_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_sync_source_t_(Structure):
        pass
    
    class struct_sync_source_t(Structure):
        pass
    
    struct_qvector_sync_source_t_._pack_ = 1 # source:False
    struct_qvector_sync_source_t_._fields_ = [
        ('array', ctypes.POINTER(struct_sync_source_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_thread_name_t_(Structure):
        pass
    
    class struct_thread_name_t(Structure):
        pass
    
    struct_qvector_thread_name_t_._pack_ = 1 # source:False
    struct_qvector_thread_name_t_._fields_ = [
        ('array', ctypes.POINTER(struct_thread_name_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_struct_field_visitor_t(Structure):
        pass
    
    struct_struct_field_visitor_t._pack_ = 1 # source:False
    struct_struct_field_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_struct_field_visitor_t_vtbl)),
    ]
    
    class struct_abstract_graph_t_vtbl(Structure):
        pass
    
    class struct_action_handler_t_vtbl(Structure):
        pass
    
    class struct_cfgopt_t__num_range_t(Structure):
        pass
    
    struct_cfgopt_t__num_range_t._pack_ = 1 # source:False
    struct_cfgopt_t__num_range_t._fields_ = [
        ('minval', ctypes.c_int64),
        ('maxval', ctypes.c_int64),
    ]
    
    class struct_enum_member_visitor_t(Structure):
        pass
    
    struct_enum_member_visitor_t._pack_ = 1 # source:False
    struct_enum_member_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_enum_member_visitor_t_vtbl)),
    ]
    
    class struct_event_listener_t_vtbl(Structure):
        pass
    
    class struct_generic_linput_t_vtbl(Structure):
        pass
    
    class struct_graph_location_info_t(Structure):
        pass
    
    struct_graph_location_info_t._pack_ = 1 # source:False
    struct_graph_location_info_t._fields_ = [
        ('zoom', ctypes.c_double),
        ('orgx', ctypes.c_double),
        ('orgy', ctypes.c_double),
    ]
    
    class struct_memory_deserializer_t(Structure):
        pass
    
    struct_memory_deserializer_t._pack_ = 1 # source:False
    struct_memory_deserializer_t._fields_ = [
        ('ptr', ctypes.POINTER(ctypes.c_ubyte)),
        ('end', ctypes.POINTER(ctypes.c_ubyte)),
    ]
    
    class struct_qvector_cfgopt_set_t_(Structure):
        pass
    
    class struct_cfgopt_set_t(Structure):
        pass
    
    struct_qvector_cfgopt_set_t_._pack_ = 1 # source:False
    struct_qvector_cfgopt_set_t_._fields_ = [
        ('array', ctypes.POINTER(struct_cfgopt_set_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_extlang_t__P_(Structure):
        pass
    
    class struct_extlang_t(Structure):
        pass
    
    struct_qvector_extlang_t__P_._pack_ = 1 # source:False
    struct_qvector_extlang_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_extlang_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_fixup_info_t_(Structure):
        pass
    
    class struct_fixup_info_t(Structure):
        pass
    
    struct_qvector_fixup_info_t_._pack_ = 1 # source:False
    struct_qvector_fixup_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_fixup_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_idc_global_t_(Structure):
        pass
    
    class struct_idc_global_t(Structure):
        pass
    
    struct_qvector_idc_global_t_._pack_ = 1 # source:False
    struct_qvector_idc_global_t_._fields_ = [
        ('array', ctypes.POINTER(struct_idc_global_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_ioport_bit_t_(Structure):
        pass
    
    class struct_ioport_bit_t(Structure):
        pass
    
    struct_qvector_ioport_bit_t_._pack_ = 1 # source:False
    struct_qvector_ioport_bit_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ioport_bit_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_qvector_int__(Structure):
        pass
    
    class struct_qvector_int_(Structure):
        pass
    
    struct_qvector_qvector_int__._pack_ = 1 # source:False
    struct_qvector_qvector_int__._fields_ = [
        ('array', ctypes.POINTER(struct_qvector_int_)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_reg_access_t_(Structure):
        pass
    
    class struct_reg_access_t(Structure):
        pass
    
    struct_qvector_reg_access_t_._pack_ = 1 # source:False
    struct_qvector_reg_access_t_._fields_ = [
        ('array', ctypes.POINTER(struct_reg_access_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_simpleline_t_(Structure):
        pass
    
    class struct_simpleline_t(Structure):
        pass
    
    struct_qvector_simpleline_t_._pack_ = 1 # source:False
    struct_qvector_simpleline_t_._fields_ = [
        ('array', ctypes.POINTER(struct_simpleline_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_udt_member_t_(Structure):
        pass
    
    class struct_udt_member_t(Structure):
        pass
    
    struct_qvector_udt_member_t_._pack_ = 1 # source:False
    struct_qvector_udt_member_t_._fields_ = [
        ('array', ctypes.POINTER(struct_udt_member_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_unsigned_int_(Structure):
        pass
    
    struct_qvector_unsigned_int_._pack_ = 1 # source:False
    struct_qvector_unsigned_int_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_uint32)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_refcnted_regex_t_vtbl(Structure):
        pass
    
    class struct_user_defined_prefix_t(Structure):
        pass
    
    struct_user_defined_prefix_t._pack_ = 1 # source:False
    struct_user_defined_prefix_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_user_defined_prefix_t_vtbl)),
    ]
    
    class struct_bitfield_type_data_t(Structure):
        pass
    
    struct_bitfield_type_data_t._pack_ = 1 # source:False
    struct_bitfield_type_data_t._fields_ = [
        ('nbytes', ctypes.c_ubyte),
        ('width', ctypes.c_ubyte),
        ('is_unsigned', ctypes.c_char),
    ]
    
    class struct_chooser_item_attrs_t(Structure):
        pass
    
    struct_chooser_item_attrs_t._pack_ = 1 # source:False
    struct_chooser_item_attrs_t._fields_ = [
        ('cb', ctypes.c_int32),
        ('flags', ctypes.c_int32),
        ('color', ctypes.c_uint32),
    ]
    
    class struct_chooser_multi_t_vtbl(Structure):
        pass
    
    class struct_const_aloc_visitor_t(Structure):
        pass
    
    struct_const_aloc_visitor_t._pack_ = 1 # source:False
    struct_const_aloc_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_const_aloc_visitor_t_vtbl)),
    ]
    
    class struct_edge_infos_wrapper_t(Structure):
        pass
    
    class struct_edge_infos_t(Structure):
        pass
    
    struct_edge_infos_wrapper_t._pack_ = 1 # source:False
    struct_edge_infos_wrapper_t._fields_ = [
        ('ptr', ctypes.POINTER(struct_edge_infos_t)),
    ]
    
    class struct_func_item_iterator_t(Structure):
        pass
    
    class struct_func_tail_iterator_t(Structure):
        pass
    
    struct_range_t._pack_ = 1 # source:False
    struct_range_t._fields_ = [
        ('start_ea', ctypes.c_uint64),
        ('end_ea', ctypes.c_uint64),
    ]
    
    struct_func_tail_iterator_t._pack_ = 1 # source:False
    struct_func_tail_iterator_t._fields_ = [
        ('pfn', ctypes.POINTER(struct_func_t)),
        ('idx', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('seglim', struct_range_t),
    ]
    
    struct_func_item_iterator_t._pack_ = 1 # source:False
    struct_func_item_iterator_t._fields_ = [
        ('fti', struct_func_tail_iterator_t),
        ('ea', ctypes.c_uint64),
    ]
    
    class struct_graph_node_visitor_t(Structure):
        pass
    
    class struct_node_set_t(Structure):
        pass
    
    struct_node_set_t._pack_ = 1 # source:False
    struct_node_set_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    struct_graph_node_visitor_t._pack_ = 1 # source:False
    struct_graph_node_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_graph_node_visitor_t_vtbl)),
        ('visited', struct_node_set_t),
    ]
    
    class struct_graph_path_visitor_t(Structure):
        pass
    
    struct_qvector_int_._pack_ = 1 # source:False
    struct_qvector_int_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_int32)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    intvec_t = struct_qvector_int_
    struct_graph_path_visitor_t._pack_ = 1 # source:False
    struct_graph_path_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_graph_path_visitor_t_vtbl)),
        ('path', intvec_t),
        ('prune', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_graph_visitor_t_vtbl(Structure):
        pass
    
    class struct_janitor_t__iobuf__P_(Structure):
        pass
    
    class struct__iobuf(Structure):
        pass
    
    struct_janitor_t__iobuf__P_._pack_ = 1 # source:False
    struct_janitor_t__iobuf__P_._fields_ = [
        ('resource', ctypes.POINTER(ctypes.POINTER(struct__iobuf))),
    ]
    
    class struct_mutable_graph_t_vtbl(Structure):
        pass
    
    class struct_post_event_visitor_t(Structure):
        pass
    
    struct_post_event_visitor_t._pack_ = 1 # source:False
    struct_post_event_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_post_event_visitor_t_vtbl)),
    ]
    
    class struct_qrefcnt_t_extlang_t_(Structure):
        pass
    
    struct_qrefcnt_t_extlang_t_._pack_ = 1 # source:False
    struct_qrefcnt_t_extlang_t_._fields_ = [
        ('ptr', ctypes.POINTER(struct_extlang_t)),
    ]
    
    class struct_qvector_simd_info_t_(Structure):
        pass
    
    class struct_simd_info_t(Structure):
        pass
    
    struct_qvector_simd_info_t_._pack_ = 1 # source:False
    struct_qvector_simd_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_simd_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_type_attr_t_(Structure):
        pass
    
    class struct_type_attr_t(Structure):
        pass
    
    struct_qvector_type_attr_t_._pack_ = 1 # source:False
    struct_qvector_type_attr_t_._fields_ = [
        ('array', ctypes.POINTER(struct_type_attr_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_syntax_highlighter_t(Structure):
        pass
    
    class struct_highlighter_cbs_t(Structure):
        pass
    
    struct_syntax_highlighter_t._pack_ = 1 # source:False
    struct_syntax_highlighter_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_syntax_highlighter_t_vtbl)),
        ('highlight_block', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.POINTER(struct_highlighter_cbs_t), ctypes.POINTER(struct__qstring_char_))),
    ]
    
    class struct_tinfo_visitor_t_vtbl(Structure):
        pass
    
    class struct_aloc_visitor_t_vtbl(Structure):
        pass
    
    class struct_altadjust_visitor_t(Structure):
        pass
    
    struct_altadjust_visitor_t._pack_ = 1 # source:False
    struct_altadjust_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_altadjust_visitor_t_vtbl)),
    ]
    
    class struct_cancellable_graph_t(Structure):
        pass
    
    struct_cancellable_graph_t._pack_ = 1 # source:False
    struct_cancellable_graph_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('cancelled', ctypes.c_char),
        ('padding', ctypes.c_char * 3),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_chooser_base_t_vtbl(Structure):
        pass
    
    class struct_dirtree_selection_t(Structure):
        pass
    
    struct_dirtree_selection_t._pack_ = 1 # source:False
    struct_dirtree_selection_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_edge_layout_point_t(Structure):
        pass
    
    class struct_edge_t(Structure):
        pass
    
    struct_edge_t._pack_ = 1 # source:False
    struct_edge_t._fields_ = [
        ('src', ctypes.c_int32),
        ('dst', ctypes.c_int32),
    ]
    
    struct_edge_layout_point_t._pack_ = 1 # source:False
    struct_edge_layout_point_t._fields_ = [
        ('pidx', ctypes.c_int32),
        ('e', struct_edge_t),
    ]
    
    class struct_exec_request_t_vtbl(Structure):
        pass
    
    class struct_form_actions_t_vtbl(Structure):
        pass
    
    class struct_hexplace_gen_t_vtbl(Structure):
        pass
    
    class struct_idc_resolver_t_vtbl(Structure):
        pass
    
    class struct_jump_pattern_t_vtbl(Structure):
        pass
    
    class struct_macro_constructor_t(Structure):
        pass
    
    struct_macro_constructor_t._pack_ = 1 # source:False
    struct_macro_constructor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_macro_constructor_t_vtbl)),
        ('reserved', ctypes.c_uint64),
    ]
    
    class struct_qvector_bptaddrs_t_(Structure):
        pass
    
    class struct_bptaddrs_t(Structure):
        pass
    
    struct_qvector_bptaddrs_t_._pack_ = 1 # source:False
    struct_qvector_bptaddrs_t_._fields_ = [
        ('array', ctypes.POINTER(struct_bptaddrs_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_direntry_t_(Structure):
        pass
    
    class struct_direntry_t(Structure):
        pass
    
    struct_qvector_direntry_t_._pack_ = 1 # source:False
    struct_qvector_direntry_t_._fields_ = [
        ('array', ctypes.POINTER(struct_direntry_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_idp_desc_t_(Structure):
        pass
    
    class struct_idp_desc_t(Structure):
        pass
    
    struct_qvector_idp_desc_t_._pack_ = 1 # source:False
    struct_qvector_idp_desc_t_._fields_ = [
        ('array', ctypes.POINTER(struct_idp_desc_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_idp_name_t_(Structure):
        pass
    
    class struct_idp_name_t(Structure):
        pass
    
    struct_qvector_idp_name_t_._pack_ = 1 # source:False
    struct_qvector_idp_name_t_._fields_ = [
        ('array', ctypes.POINTER(struct_idp_name_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_node_set_t_(Structure):
        pass
    
    struct_qvector_node_set_t_._pack_ = 1 # source:False
    struct_qvector_node_set_t_._fields_ = [
        ('array', ctypes.POINTER(struct_node_set_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_rangeset_t_(Structure):
        pass
    
    struct_qvector_rangeset_t_._pack_ = 1 # source:False
    struct_qvector_rangeset_t_._fields_ = [
        ('array', ctypes.POINTER(struct_rangeset_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_reg_info_t_(Structure):
        pass
    
    class struct_reg_info_t(Structure):
        pass
    
    struct_qvector_reg_info_t_._pack_ = 1 # source:False
    struct_qvector_reg_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_reg_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_row_info_t_(Structure):
        pass
    
    class struct_row_info_t(Structure):
        pass
    
    struct_qvector_row_info_t_._pack_ = 1 # source:False
    struct_qvector_row_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_row_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_tev_info_t_(Structure):
        pass
    
    class struct_tev_info_t(Structure):
        pass
    
    struct_qvector_tev_info_t_._pack_ = 1 # source:False
    struct_qvector_tev_info_t_._fields_ = [
        ('array', ctypes.POINTER(struct_tev_info_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_twinline_t_(Structure):
        pass
    
    struct_qvector_twinline_t_._pack_ = 1 # source:False
    struct_qvector_twinline_t_._fields_ = [
        ('array', ctypes.POINTER(struct_twinline_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_renderer_info_pos_t(Structure):
        pass
    
    struct_renderer_info_pos_t._pack_ = 1 # source:False
    struct_renderer_info_pos_t._fields_ = [
        ('node', ctypes.c_int32),
        ('cx', ctypes.c_int16),
        ('cy', ctypes.c_int16),
    ]
    
    class struct_renderer_pos_info_t(Structure):
        pass
    
    struct_renderer_pos_info_t._pack_ = 1 # source:False
    struct_renderer_pos_info_t._fields_ = [
        ('node', ctypes.c_int32),
        ('cx', ctypes.c_int16),
        ('cy', ctypes.c_int16),
        ('sx', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
    ]
    
    class struct_std__allocator_int_(Structure):
        pass
    
    class struct_typedef_type_data_t(Structure):
        pass
    
    class struct_til_t(Structure):
        pass
    
    class union_typedef_type_data_t_0(Union):
        pass
    
    union_typedef_type_data_t_0._pack_ = 1 # source:False
    union_typedef_type_data_t_0._fields_ = [
        ('name', ctypes.c_char_p),
        ('ordinal', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_typedef_type_data_t._pack_ = 1 # source:False
    struct_typedef_type_data_t._anonymous_ = ('_0',)
    struct_typedef_type_data_t._fields_ = [
        ('til', ctypes.POINTER(struct_til_t)),
        ('_0', union_typedef_type_data_t_0),
        ('is_ordref', ctypes.c_char),
        ('resolve', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
    ]
    
    class struct_array_parameters_t(Structure):
        pass
    
    struct_array_parameters_t._pack_ = 1 # source:False
    struct_array_parameters_t._fields_ = [
        ('flags', ctypes.c_int32),
        ('lineitems', ctypes.c_int32),
        ('alignment', ctypes.c_int32),
    ]
    
    class struct_bpt_visitor_t_vtbl(Structure):
        pass
    
    class struct_cfgopt_t__params_t(Structure):
        pass
    
    struct_cfgopt_t__params_t._pack_ = 1 # source:False
    struct_cfgopt_t__params_t._fields_ = [
        ('p1', ctypes.c_int64),
        ('p2', ctypes.c_int64),
    ]
    
    class struct_chooser_t__cbret_t(Structure):
        pass
    
    
    # values for enumeration 'chooser_base_t__cbres_t'
    chooser_base_t__cbres_t__enumvalues = {
        0: 'NOTHING_CHANGED',
        1: 'ALL_CHANGED',
        2: 'SELECTION_CHANGED',
    }
    NOTHING_CHANGED = 0
    ALL_CHANGED = 1
    SELECTION_CHANGED = 2
    chooser_base_t__cbres_t = ctypes.c_uint32 # enum
    struct_chooser_t__cbret_t._pack_ = 1 # source:False
    struct_chooser_t__cbret_t._fields_ = [
        ('idx', ctypes.c_int64),
        ('changed', chooser_base_t__cbres_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_depth_first_info_t(Structure):
        pass
    
    class struct_dirtree_iterator_t(Structure):
        pass
    
    struct_dirtree_cursor_t._pack_ = 1 # source:False
    struct_dirtree_cursor_t._fields_ = [
        ('parent', ctypes.c_uint64),
        ('rank', ctypes.c_uint64),
    ]
    
    struct_dirtree_iterator_t._pack_ = 1 # source:False
    struct_dirtree_iterator_t._fields_ = [
        ('pattern', qstring),
        ('cursor', struct_dirtree_cursor_t),
    ]
    
    class struct_format_data_info_t(Structure):
        pass
    
    struct_format_data_info_t._pack_ = 1 # source:False
    struct_format_data_info_t._fields_ = [
        ('ptvf', ctypes.c_int32),
        ('radix', ctypes.c_int32),
        ('max_length', ctypes.c_int32),
        ('arrbase', ctypes.c_int32),
        ('arrnelems', ctypes.c_int32),
        ('margin', ctypes.c_int32),
        ('indent', ctypes.c_int32),
    ]
    
    class struct_ioports_fallback_t(Structure):
        pass
    
    struct_ioports_fallback_t._pack_ = 1 # source:False
    struct_ioports_fallback_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_ioports_fallback_t_vtbl)),
    ]
    
    class struct_lowertype_helper_t(Structure):
        pass
    
    struct_lowertype_helper_t._pack_ = 1 # source:False
    struct_lowertype_helper_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_lowertype_helper_t_vtbl)),
    ]
    
    class struct_outctx_base_t_vtbl(Structure):
        pass
    
    class struct_qflow_chart_t_vtbl(Structure):
        pass
    
    class struct_qrefcnt_obj_t_vtbl(Structure):
        pass
    
    class struct_qvector_argpart_t_(Structure):
        pass
    
    class struct_argpart_t(Structure):
        pass
    
    struct_qvector_argpart_t_._pack_ = 1 # source:False
    struct_qvector_argpart_t_._fields_ = [
        ('array', ctypes.POINTER(struct_argpart_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_ea_name_t_(Structure):
        pass
    
    class struct_ea_name_t(Structure):
        pass
    
    struct_qvector_ea_name_t_._pack_ = 1 # source:False
    struct_qvector_ea_name_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ea_name_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_funcarg_t_(Structure):
        pass
    
    class struct_funcarg_t(Structure):
        pass
    
    struct_qvector_funcarg_t_._pack_ = 1 # source:False
    struct_qvector_funcarg_t_._fields_ = [
        ('array', ctypes.POINTER(struct_funcarg_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_qvector_long_long_._pack_ = 1 # source:False
    struct_qvector_long_long_._fields_ = [
        ('array', ctypes.POINTER(ctypes.c_int64)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_modinfo_t_(Structure):
        pass
    
    class struct_modinfo_t(Structure):
        pass
    
    struct_qvector_modinfo_t_._pack_ = 1 # source:False
    struct_qvector_modinfo_t_._fields_ = [
        ('array', ctypes.POINTER(struct_modinfo_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_simpleline_place_t(Structure):
        pass
    
    struct_simpleline_place_t._pack_ = 1 # source:False
    struct_simpleline_place_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('n', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_source_file_t_vtbl(Structure):
        pass
    
    class struct_source_item_t_vtbl(Structure):
        pass
    
    class struct_srcinfo_provider_t(Structure):
        pass
    
    struct_srcinfo_provider_t._pack_ = 1 # source:False
    struct_srcinfo_provider_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_srcinfo_provider_t_vtbl)),
        ('cb', ctypes.c_uint64),
        ('flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('display_name', ctypes.c_char_p),
    ]
    
    class struct_std__map_int__int_(Structure):
        pass
    
    struct_std__map_int__int_._pack_ = 1 # source:False
    struct_std__map_int__int_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_stkarg_area_info_t(Structure):
        pass
    
    struct_stkarg_area_info_t._pack_ = 1 # source:False
    struct_stkarg_area_info_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('stkarg_offset', ctypes.c_int64),
        ('shadow_size', ctypes.c_int64),
        ('linkage_area', ctypes.c_int64),
    ]
    
    class struct_structplace_t_vtbl(Structure):
        pass
    
    class struct_user_graph_place_t(Structure):
        pass
    
    struct_user_graph_place_t._pack_ = 1 # source:False
    struct_user_graph_place_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('node', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class union_view_mouse_event_location_t(Union):
        pass
    
    union_view_mouse_event_location_t._pack_ = 1 # source:False
    union_view_mouse_event_location_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('item', ctypes.POINTER(struct_selection_item_t)),
    ]
    
    view_mouse_event_t__location_t = union_view_mouse_event_location_t
    
    # values for enumeration 'tcc_renderer_type_t'
    tcc_renderer_type_t__enumvalues = {
        0: 'TCCRT_INVALID',
        1: 'TCCRT_FLAT',
        2: 'TCCRT_GRAPH',
        3: 'TCCRT_PROXIMITY',
    }
    TCCRT_INVALID = 0
    TCCRT_FLAT = 1
    TCCRT_GRAPH = 2
    TCCRT_PROXIMITY = 3
    tcc_renderer_type_t = ctypes.c_uint32 # enum
    struct_view_mouse_event_t._pack_ = 1 # source:False
    struct_view_mouse_event_t._fields_ = [
        ('rtype', tcc_renderer_type_t),
        ('x', ctypes.c_uint32),
        ('y', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('location', view_mouse_event_t__location_t),
        ('state', ctypes.c_int32),
        ('button', vme_button_t),
        ('renderer_pos', struct_renderer_pos_info_t),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
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
    
    class struct_action_ctx_base_t(Structure):
        pass
    
    class struct_struc_t(Structure):
        pass
    
    class struct_member_t(Structure):
        pass
    
    sizevec_t = struct_qvector_unsigned_long_long_
    class union_action_ctx_base_source_t(Union):
        pass
    
    class struct_chooser_base_t(Structure):
        pass
    
    union_action_ctx_base_source_t._pack_ = 1 # source:False
    union_action_ctx_base_source_t._fields_ = [
        ('chooser', ctypes.POINTER(struct_chooser_base_t)),
    ]
    
    struct_action_ctx_base_t._pack_ = 1 # source:False
    struct_action_ctx_base_t._fields_ = [
        ('widget', ctypes.POINTER(struct_TWidget)),
        ('widget_type', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('widget_title', qstring),
        ('chooser_selection', sizevec_t),
        ('action', ctypes.c_char_p),
        ('cur_flags', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('cur_ea', ctypes.c_uint64),
        ('cur_value', ctypes.c_uint64),
        ('cur_func', ctypes.POINTER(struct_func_t)),
        ('cur_fchunk', ctypes.POINTER(struct_func_t)),
        ('cur_struc', ctypes.POINTER(struct_struc_t)),
        ('cur_strmem', ctypes.POINTER(struct_member_t)),
        ('cur_enum', ctypes.c_uint64),
        ('cur_seg', ctypes.POINTER(struct_segment_t)),
        ('cur_sel', struct_action_ctx_base_cur_sel_t),
        ('regname', ctypes.c_char_p),
        ('focus', ctypes.POINTER(struct_TWidget)),
        ('graph_selection', ctypes.POINTER(struct_screen_graph_selection_t)),
        ('cur_enum_member', ctypes.c_uint64),
        ('dirtree_selection', ctypes.POINTER(struct_dirtree_selection_t)),
        ('source', union_action_ctx_base_source_t),
    ]
    
    class struct_argtinfo_helper_t(Structure):
        pass
    
    struct_argtinfo_helper_t._pack_ = 1 # source:False
    struct_argtinfo_helper_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_argtinfo_helper_t_vtbl)),
        ('reserved', ctypes.c_uint64),
    ]
    
    class struct_array_type_data_t(Structure):
        pass
    
    struct_tinfo_t._pack_ = 1 # source:False
    struct_tinfo_t._fields_ = [
        ('typid', ctypes.c_uint32),
    ]
    
    struct_array_type_data_t._pack_ = 1 # source:False
    struct_array_type_data_t._fields_ = [
        ('elem_type', struct_tinfo_t),
        ('base', ctypes.c_uint32),
        ('nelems', ctypes.c_uint32),
    ]
    
    struct_call_stack_info_t._pack_ = 1 # source:False
    struct_call_stack_info_t._fields_ = [
        ('callea', ctypes.c_uint64),
        ('funcea', ctypes.c_uint64),
        ('fp', ctypes.c_uint64),
        ('funcok', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_bytevec_t(Structure):
        pass
    
    struct_bytevec_t._pack_ = 1 # source:False
    struct_bytevec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_rangevec_t(Structure):
        pass
    
    struct_rangevec_t._pack_ = 1 # source:False
    struct_rangevec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_compiled_binpat_t._pack_ = 1 # source:False
    struct_compiled_binpat_t._fields_ = [
        ('bytes', struct_bytevec_t),
        ('mask', struct_bytevec_t),
        ('strlits', struct_rangevec_t),
        ('encidx', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_dirtree_visitor_t(Structure):
        pass
    
    struct_dirtree_visitor_t._pack_ = 1 # source:False
    struct_dirtree_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_dirtree_visitor_t_vtbl)),
    ]
    
    class struct_extlang_visitor_t(Structure):
        pass
    
    struct_extlang_visitor_t._pack_ = 1 # source:False
    struct_extlang_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_extlang_visitor_t_vtbl)),
    ]
    
    class struct_file_enumerator_t(Structure):
        pass
    
    struct_file_enumerator_t._pack_ = 1 # source:False
    struct_file_enumerator_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_file_enumerator_t_vtbl)),
    ]
    
    struct_highlighter_cbs_t._pack_ = 1 # source:False
    struct_highlighter_cbs_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_highlighter_cbs_t_vtbl)),
    ]
    
    class struct_instant_dbgopts_t(Structure):
        pass
    
    struct_instant_dbgopts_t._pack_ = 1 # source:False
    struct_instant_dbgopts_t._fields_ = [
        ('debmod', qstring),
        ('env', qstring),
        ('host', qstring),
        ('pass', qstring),
        ('port', ctypes.c_int32),
        ('pid', ctypes.c_int32),
        ('event_id', ctypes.c_int32),
        ('attach', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
    ]
    
    class struct_interr_exc_t_vtbl(Structure):
        pass
    
    class struct_qvector_argloc_t_(Structure):
        pass
    
    class struct_argloc_t(Structure):
        pass
    
    struct_qvector_argloc_t_._pack_ = 1 # source:False
    struct_qvector_argloc_t_._fields_ = [
        ('array', ctypes.POINTER(struct_argloc_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_bpt_t__P_(Structure):
        pass
    
    struct_qvector_bpt_t__P_._pack_ = 1 # source:False
    struct_qvector_bpt_t__P_._fields_ = [
        ('array', ctypes.POINTER(ctypes.POINTER(struct_bpt_t))),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_cliopt_t_(Structure):
        pass
    
    class struct_cliopt_t(Structure):
        pass
    
    struct_qvector_cliopt_t_._pack_ = 1 # source:False
    struct_qvector_cliopt_t_._fields_ = [
        ('array', ctypes.POINTER(struct_cliopt_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_intmap_t_(Structure):
        pass
    
    class struct_intmap_t(Structure):
        pass
    
    struct_qvector_intmap_t_._pack_ = 1 # source:False
    struct_qvector_intmap_t_._fields_ = [
        ('array', ctypes.POINTER(struct_intmap_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_ioport_t_(Structure):
        pass
    
    class struct_ioport_t(Structure):
        pass
    
    struct_qvector_ioport_t_._pack_ = 1 # source:False
    struct_qvector_ioport_t_._fields_ = [
        ('array', ctypes.POINTER(struct_ioport_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_jvalue_t_(Structure):
        pass
    
    class struct_jvalue_t(Structure):
        pass
    
    struct_qvector_jvalue_t_._pack_ = 1 # source:False
    struct_qvector_jvalue_t_._fields_ = [
        ('array', ctypes.POINTER(struct_jvalue_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_lowcnd_t_(Structure):
        pass
    
    class struct_lowcnd_t(Structure):
        pass
    
    struct_qvector_lowcnd_t_._pack_ = 1 # source:False
    struct_qvector_lowcnd_t_._fields_ = [
        ('array', ctypes.POINTER(struct_lowcnd_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_regobj_t_(Structure):
        pass
    
    class struct_regobj_t(Structure):
        pass
    
    struct_qvector_regobj_t_._pack_ = 1 # source:False
    struct_qvector_regobj_t_._fields_ = [
        ('array', ctypes.POINTER(struct_regobj_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_regval_t_(Structure):
        pass
    
    class struct_regval_t(Structure):
        pass
    
    struct_qvector_regval_t_._pack_ = 1 # source:False
    struct_qvector_regval_t_._fields_ = [
        ('array', ctypes.POINTER(struct_regval_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_stkpnt_t_(Structure):
        pass
    
    struct_qvector_stkpnt_t_._pack_ = 1 # source:False
    struct_qvector_stkpnt_t_._fields_ = [
        ('array', ctypes.POINTER(struct_stkpnt_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_tryblk_t_(Structure):
        pass
    
    class struct_tryblk_t(Structure):
        pass
    
    struct_qvector_tryblk_t_._pack_ = 1 # source:False
    struct_qvector_tryblk_t_._fields_ = [
        ('array', ctypes.POINTER(struct_tryblk_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_valstr_t_(Structure):
        pass
    
    struct_qvector_valstr_t_._pack_ = 1 # source:False
    struct_qvector_valstr_t_._fields_ = [
        ('array', ctypes.POINTER(struct_valstr_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_segm_move_infos_t(Structure):
        pass
    
    struct_segm_move_infos_t._pack_ = 1 # source:False
    struct_segm_move_infos_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_ui_request_t_vtbl(Structure):
        pass
    
    struct_update_bpt_info_t._pack_ = 1 # source:False
    struct_update_bpt_info_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('orgbytes', struct_bytevec_t),
        ('type', ctypes.c_int32),
        ('size', ctypes.c_int32),
        ('code', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('pid', ctypes.c_int32),
        ('tid', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_abstract_graph_t(Structure):
        pass
    
    class struct_point_t(Structure):
        pass
    
    struct_point_t._pack_ = 1 # source:False
    struct_point_t._fields_ = [
        ('x', ctypes.c_int32),
        ('y', ctypes.c_int32),
    ]
    
    struct_abstract_graph_t._pack_ = 1 # source:False
    struct_abstract_graph_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
        ('title', qstring),
        ('rect_edges_made', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('current_layout', ctypes.c_int32),
        ('circle_center', struct_point_t),
        ('circle_radius', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('callback', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(None), ctypes.c_int32, ctypes.POINTER(ctypes.POINTER(None)))),
        ('callback_ud', ctypes.POINTER(None)),
    ]
    
    class struct_action_handler_t(Structure):
        pass
    
    struct_action_handler_t._pack_ = 1 # source:False
    struct_action_handler_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_action_handler_t_vtbl)),
        ('flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_cfgopt_set_vec_t(Structure):
        pass
    
    struct_cfgopt_set_vec_t._pack_ = 1 # source:False
    struct_cfgopt_set_vec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_enum_type_data_t(Structure):
        pass
    
    struct_enum_type_data_t._pack_ = 1 # source:False
    struct_enum_type_data_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('group_sizes', intvec_t),
        ('taenum_bits', ctypes.c_uint32),
        ('bte', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 3),
    ]
    
    class struct_enumplace_t_vtbl(Structure):
        pass
    
    class struct_event_listener_t(Structure):
        pass
    
    struct_event_listener_t._pack_ = 1 # source:False
    struct_event_listener_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_event_listener_t_vtbl)),
        ('listener_flags', ctypes.c_uint64),
    ]
    
    struct_exception_info_t._pack_ = 1 # source:False
    struct_exception_info_t._fields_ = [
        ('code', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('name', qstring),
        ('desc', qstring),
    ]
    
    class struct_func_type_data_t(Structure):
        pass
    
    class union_argloc_t_0(Union):
        pass
    
    class struct_scattered_aloc_t(Structure):
        pass
    
    class struct_rrel_t(Structure):
        pass
    
    union_argloc_t_0._pack_ = 1 # source:False
    union_argloc_t_0._fields_ = [
        ('sval', ctypes.c_int64),
        ('reginfo', ctypes.c_uint32),
        ('rrel', ctypes.POINTER(struct_rrel_t)),
        ('dist', ctypes.POINTER(struct_scattered_aloc_t)),
        ('custom', ctypes.POINTER(None)),
        ('biggest', ctypes.c_uint64),
    ]
    
    struct_argloc_t._pack_ = 1 # source:False
    struct_argloc_t._anonymous_ = ('_0',)
    struct_argloc_t._fields_ = [
        ('type', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('_0', union_argloc_t_0),
    ]
    
    reginfovec_t = struct_qvector_reg_info_t_
    struct_func_type_data_t._pack_ = 1 # source:False
    struct_func_type_data_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('flags', ctypes.c_int32),
        ('rettype', struct_tinfo_t),
        ('retloc', struct_argloc_t),
        ('stkargs', ctypes.c_uint64),
        ('spoiled', reginfovec_t),
        ('cc', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    class struct_gdl_graph_t_vtbl(Structure):
        pass
    
    class struct_generic_linput_t(Structure):
        pass
    
    struct_generic_linput_t._pack_ = 1 # source:False
    struct_generic_linput_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_generic_linput_t_vtbl)),
        ('filesize', ctypes.c_uint64),
        ('blocksize', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_predicate_t_vtbl(Structure):
        pass
    
    class struct_qvector_catch_t_(Structure):
        pass
    
    class struct_catch_t(Structure):
        pass
    
    struct_qvector_catch_t_._pack_ = 1 # source:False
    struct_qvector_catch_t_._fields_ = [
        ('array', ctypes.POINTER(struct_catch_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_point_t_(Structure):
        pass
    
    struct_qvector_point_t_._pack_ = 1 # source:False
    struct_qvector_point_t_._fields_ = [
        ('array', ctypes.POINTER(struct_point_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_range_t_(Structure):
        pass
    
    struct_qvector_range_t_._pack_ = 1 # source:False
    struct_qvector_range_t_._fields_ = [
        ('array', ctypes.POINTER(struct_range_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_tinfo_t_(Structure):
        pass
    
    struct_qvector_tinfo_t_._pack_ = 1 # source:False
    struct_qvector_tinfo_t_._fields_ = [
        ('array', ctypes.POINTER(struct_tinfo_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_token_t_(Structure):
        pass
    
    class struct_token_t(Structure):
        pass
    
    struct_qvector_token_t_._pack_ = 1 # source:False
    struct_qvector_token_t_._fields_ = [
        ('array', ctypes.POINTER(struct_token_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_regex_t(Structure):
        pass
    
    struct_regex_t._pack_ = 1 # source:False
    struct_regex_t._fields_ = [
        ('re_magic', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('re_nsub', ctypes.c_uint64),
        ('re_endp', ctypes.c_char_p),
        ('re_g', ctypes.POINTER(None)),
    ]
    
    struct_refcnted_regex_t._pack_ = 1 # source:False
    struct_refcnted_regex_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('regex', struct_regex_t),
    ]
    
    struct_scattered_aloc_t._pack_ = 1 # source:False
    struct_scattered_aloc_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_scattered_segm_t._pack_ = 1 # source:False
    struct_scattered_segm_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('name', qstring),
    ]
    
    struct_segm_move_info_t._pack_ = 1 # source:False
    struct_segm_move_info_t._fields_ = [
        ('from', ctypes.c_uint64),
        ('to', ctypes.c_uint64),
        ('size', ctypes.c_uint64),
    ]
    
    struct_selection_item_t._pack_ = 1 # source:False
    struct_selection_item_t._fields_ = [
        ('is_node', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('node', ctypes.c_int32),
        ('elp', struct_edge_layout_point_t),
    ]
    
    class struct_text_sink_t_vtbl(Structure):
        pass
    
    struct_xreflist_entry_t._pack_ = 1 # source:False
    struct_xreflist_entry_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('opnum', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 6),
    ]
    
    struct_channel_redir_t._pack_ = 1 # source:False
    struct_channel_redir_t._fields_ = [
        ('fd', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('file', qstring),
        ('flags', ctypes.c_int32),
        ('start', ctypes.c_int32),
        ('length', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_chooser_multi_t(Structure):
        pass
    
    struct_chooser_multi_t._pack_ = 1 # source:False
    struct_chooser_multi_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 184),
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
    
    class struct_edge_segs_vec_t(Structure):
        pass
    
    class struct_expanded_area_t(Structure):
        pass
    
    class struct_fixup_handler_t(Structure):
        pass
    
    class struct_fixup_data_t(Structure):
        pass
    
    struct_fixup_handler_t._pack_ = 1 # source:False
    struct_fixup_handler_t._fields_ = [
        ('cbsize', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('props', ctypes.c_uint32),
        ('size', ctypes.c_ubyte),
        ('width', ctypes.c_ubyte),
        ('shift', ctypes.c_ubyte),
        ('rsrv4', ctypes.c_ubyte),
        ('reftype', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('apply', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_fixup_handler_t), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, ctypes.c_char, ctypes.POINTER(struct_fixup_data_t))),
        ('get_value', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_fixup_handler_t), ctypes.c_uint64)),
        ('patch_value', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_fixup_handler_t), ctypes.c_uint64, ctypes.POINTER(struct_fixup_data_t))),
    ]
    
    class struct_graph_visitor_t(Structure):
        pass
    
    struct_graph_visitor_t._pack_ = 1 # source:False
    struct_graph_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_graph_visitor_t_vtbl)),
        ('g', ctypes.POINTER(struct_abstract_graph_t)),
    ]
    
    class struct_hexplace_t_vtbl(Structure):
        pass
    
    class struct_idaplace_t_vtbl(Structure):
        pass
    
    class struct_linput_buffer_t(Structure):
        pass
    
    struct_linput_buffer_t._pack_ = 1 # source:False
    struct_linput_buffer_t._fields_ = [
        ('li', ctypes.POINTER(struct_linput_t)),
        ('lsize', ctypes.c_int64),
    ]
    
    class struct_renderer_info_t(Structure):
        pass
    
    renderer_info_t__pos_t = struct_renderer_info_pos_t
    struct_renderer_info_t._pack_ = 1 # source:False
    struct_renderer_info_t._fields_ = [
        ('gli', struct_graph_location_info_t),
        ('pos', renderer_info_t__pos_t),
        ('rtype', tcc_renderer_type_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_lochist_entry_t._pack_ = 1 # source:False
    struct_lochist_entry_t._fields_ = [
        ('rinfo', struct_renderer_info_t),
        ('plce', ctypes.POINTER(struct_place_t)),
    ]
    
    class struct_mutable_graph_t(Structure):
        pass
    
    class struct_qvector_rect_t_(Structure):
        pass
    
    class struct_rect_t(Structure):
        pass
    
    struct_qvector_rect_t_._pack_ = 1 # source:False
    struct_qvector_rect_t_._fields_ = [
        ('array', ctypes.POINTER(struct_rect_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    mutable_graph_t__node_layout_t = struct_qvector_rect_t_
    array_of_intvec_t = struct_qvector_qvector_int__
    struct_mutable_graph_t._pack_ = 1 # source:False
    struct_mutable_graph_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 72),
        ('gid', ctypes.c_uint64),
        ('belongs', intvec_t),
        ('node_flags', struct_bytevec_t),
        ('org_succs', array_of_intvec_t),
        ('org_preds', array_of_intvec_t),
        ('succs', array_of_intvec_t),
        ('preds', array_of_intvec_t),
        ('nodes', mutable_graph_t__node_layout_t),
        ('edges', struct_edge_infos_wrapper_t),
    ]
    
    class struct_node_ordering_t(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('node_by_order', intvec_t),
        ('order_by_node', intvec_t),
         ]
    
    class struct_ptr_type_data_t(Structure):
        pass
    
    struct_ptr_type_data_t._pack_ = 1 # source:False
    struct_ptr_type_data_t._fields_ = [
        ('obj_type', struct_tinfo_t),
        ('closure', struct_tinfo_t),
        ('based_ptr_size', ctypes.c_ubyte),
        ('taptr_bits', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('parent', struct_tinfo_t),
        ('delta', ctypes.c_int32),
    ]
    
    class struct_qmutex_locker_t(Structure):
        pass
    
    class struct___qmutex_t(Structure):
        pass
    
    struct_qmutex_locker_t._pack_ = 1 # source:False
    struct_qmutex_locker_t._fields_ = [
        ('lock', ctypes.POINTER(struct___qmutex_t)),
    ]
    
    class struct_qstack_token_t_(Structure):
        pass
    
    struct_qstack_token_t_._pack_ = 1 # source:False
    struct_qstack_token_t_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_qvector_edge_t_(Structure):
        pass
    
    struct_qvector_edge_t_._pack_ = 1 # source:False
    struct_qvector_edge_t_._fields_ = [
        ('array', ctypes.POINTER(struct_edge_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_register_info_t._pack_ = 1 # source:False
    struct_register_info_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('flags', ctypes.c_uint32),
        ('register_class', ctypes.c_ubyte),
        ('dtype', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('bit_strings', ctypes.POINTER(ctypes.c_char_p)),
        ('default_bit_strings_mask', ctypes.c_uint64),
    ]
    
    class union_regval_t_0(Union):
        pass
    
    class struct_fpvalue_t(Structure):
        pass
    
    struct_fpvalue_t._pack_ = 1 # source:False
    struct_fpvalue_t._fields_ = [
        ('w', ctypes.c_uint16 * 6),
    ]
    
    union_regval_t_0._pack_ = 1 # source:False
    union_regval_t_0._fields_ = [
        ('ival', ctypes.c_uint64),
        ('fval', struct_fpvalue_t),
        ('reserve', ctypes.c_ubyte * 24),
    ]
    
    struct_regval_t._pack_ = 1 # source:False
    struct_regval_t._anonymous_ = ('_0',)
    struct_regval_t._fields_ = [
        ('rvtype', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('_0', union_regval_t_0),
    ]
    
    struct_tev_reg_value_t._pack_ = 1 # source:False
    struct_tev_reg_value_t._fields_ = [
        ('value', struct_regval_t),
        ('reg_idx', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_textctrl_info_t(Structure):
        pass
    
    struct_textctrl_info_t._pack_ = 1 # source:False
    struct_textctrl_info_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('text', qstring),
        ('flags', ctypes.c_uint16),
        ('tabsize', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_tinfo_visitor_t(Structure):
        pass
    
    struct_tinfo_visitor_t._pack_ = 1 # source:False
    struct_tinfo_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_tinfo_visitor_t_vtbl)),
        ('state', ctypes.c_int32),
        ('level', ctypes.c_int32),
    ]
    
    class struct_udt_type_data_t(Structure):
        pass
    
    struct_udt_type_data_t._pack_ = 1 # source:False
    struct_udt_type_data_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('total_size', ctypes.c_uint64),
        ('unpadded_size', ctypes.c_uint64),
        ('effalign', ctypes.c_uint32),
        ('taudt_bits', ctypes.c_uint32),
        ('sda', ctypes.c_ubyte),
        ('pack', ctypes.c_ubyte),
        ('is_union', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 5),
    ]
    
    class struct_value_u__d128_t(Structure):
        pass
    
    struct_value_u__d128_t._pack_ = 1 # source:False
    struct_value_u__d128_t._fields_ = [
        ('low', ctypes.c_uint64),
        ('high', ctypes.c_uint64),
    ]
    
    class struct___qsemaphore_t(Structure):
        pass
    
    class struct_aloc_visitor_t(Structure):
        pass
    
    struct_aloc_visitor_t._pack_ = 1 # source:False
    struct_aloc_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_aloc_visitor_t_vtbl)),
    ]
    
    class struct_auto_display_t(Structure):
        pass
    
    struct_auto_display_t._pack_ = 1 # source:False
    struct_auto_display_t._fields_ = [
        ('type', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ea', ctypes.c_uint64),
        ('state', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_bpt_location_t(Structure):
        pass
    
    
    # values for enumeration 'bpt_loctype_t'
    bpt_loctype_t__enumvalues = {
        0: 'BPLT_ABS',
        1: 'BPLT_REL',
        2: 'BPLT_SYM',
        3: 'BPLT_SRC',
    }
    BPLT_ABS = 0
    BPLT_REL = 1
    BPLT_SYM = 2
    BPLT_SRC = 3
    bpt_loctype_t = ctypes.c_uint32 # enum
    struct_bpt_location_t._pack_ = 1 # source:False
    struct_bpt_location_t._fields_ = [
        ('info', ctypes.c_uint64),
        ('index', ctypes.c_int32),
        ('loctype', bpt_loctype_t),
    ]
    
    struct_chooser_base_t._pack_ = 1 # source:False
    struct_chooser_base_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_chooser_base_t_vtbl)),
        ('version', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('x0', ctypes.c_int32),
        ('y0', ctypes.c_int32),
        ('x1', ctypes.c_int32),
        ('y1', ctypes.c_int32),
        ('width', ctypes.c_int32),
        ('height', ctypes.c_int32),
        ('title', ctypes.c_char_p),
        ('columns', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('widths', ctypes.POINTER(ctypes.c_int32)),
        ('header', ctypes.POINTER(ctypes.c_char_p)),
        ('icon', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('popup_names', struct__qstring_char_ * 4),
        ('deflt_col', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class struct_chooser_t_vtbl(Structure):
        pass
    
    class struct_custloc_desc_t(Structure):
        pass
    
    class struct_idc_value_t(Structure):
        pass
    
    class union_value_u(Union):
        pass
    
    struct_custloc_desc_t._pack_ = 1 # source:False
    struct_custloc_desc_t._fields_ = [
        ('cbsize', ctypes.c_uint64),
        ('name', ctypes.c_char_p),
        ('copy', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_argloc_t))),
        ('cleanup', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_argloc_t))),
        ('verify', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.POINTER(struct_rangeset_t), ctypes.c_char)),
        ('compare', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_argloc_t))),
        ('print', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(struct_argloc_t), ctypes.c_uint64, ctypes.c_int32)),
        ('deref_field', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_uint64, ctypes.POINTER(struct__qstring_char_))),
        ('deref_array', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_uint64, ctypes.c_uint64)),
        ('deref_ptr', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_argloc_t))),
        ('read_value', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(union_value_u), ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.POINTER(struct_tinfo_t))),
        ('write_value', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(union_value_u), ctypes.c_int32, ctypes.POINTER(struct__qstring_char_))),
        ('calc_string_length', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t))),
        ('get_string', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_uint64)),
        ('guess_array_size', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t))),
        ('get_tinfo', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_argloc_t))),
        ('calc_number_of_children', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t))),
        ('print_ptr_value', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t))),
    ]
    
    class struct_debapp_attrs_t(Structure):
        pass
    
    struct_debapp_attrs_t._pack_ = 1 # source:False
    struct_debapp_attrs_t._fields_ = [
        ('cbsize', ctypes.c_int32),
        ('addrsize', ctypes.c_int32),
        ('platform', qstring),
        ('is_be', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_dirspec_t_vtbl(Structure):
        pass
    
    class struct_dirtree_impl_t(Structure):
        pass
    
    class struct_edge_segment_t(Structure):
        pass
    
    struct_edge_segment_t._pack_ = 1 # source:False
    struct_edge_segment_t._fields_ = [
        ('e', struct_edge_t),
        ('nseg', ctypes.c_int32),
        ('x0', ctypes.c_int32),
        ('x1', ctypes.c_int32),
    ]
    
    class struct_encoder_t_vtbl(Structure):
        pass
    
    class struct_exec_request_t(Structure):
        pass
    
    struct_exec_request_t._pack_ = 1 # source:False
    struct_exec_request_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_exec_request_t_vtbl)),
        ('code', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('sem', ctypes.POINTER(struct___qsemaphore_t)),
    ]
    
    class struct_form_actions_t(Structure):
        pass
    
    struct_form_actions_t._pack_ = 1 # source:False
    struct_form_actions_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_form_actions_t_vtbl)),
    ]
    
    class struct_getname_info_t(Structure):
        pass
    
    struct_getname_info_t._pack_ = 1 # source:False
    struct_getname_info_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('inhibitor', ctypes.c_int32),
        ('demform', ctypes.c_int32),
        ('demcode', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_group_crinfo_t._pack_ = 1 # source:False
    struct_group_crinfo_t._fields_ = [
        ('nodes', intvec_t),
        ('text', qstring),
    ]
    
    class struct_hexplace_gen_t(Structure):
        pass
    
    struct_hexplace_gen_t._pack_ = 1 # source:False
    struct_hexplace_gen_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_hexplace_gen_t_vtbl)),
    ]
    
    class struct_hidden_range_t(Structure):
        pass
    
    struct_hidden_range_t._pack_ = 1 # source:False
    struct_hidden_range_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('description', ctypes.c_char_p),
        ('header', ctypes.c_char_p),
        ('footer', ctypes.c_char_p),
        ('visible', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('color', ctypes.c_uint32),
    ]
    
    class struct_idc_resolver_t(Structure):
        pass
    
    struct_idc_resolver_t._pack_ = 1 # source:False
    struct_idc_resolver_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_idc_resolver_t_vtbl)),
    ]
    
    class struct_ignore_micro_t(Structure):
        pass
    
    class struct_netnode(Structure):
        pass
    
    struct_netnode._pack_ = 1 # source:False
    struct_netnode._fields_ = [
        ('netnodenumber', ctypes.c_uint64),
    ]
    
    struct_ignore_micro_t._pack_ = 1 # source:False
    struct_ignore_micro_t._fields_ = [
        ('ignore_micro', struct_netnode),
    ]
    
    class struct_jump_pattern_t(Structure):
        pass
    
    class struct_switch_info_t(Structure):
        pass
    
    eavec_t = struct_qvector_unsigned_long_long_
    class struct_insn_t(Structure):
        pass
    
    class union_insn_t_0(Union):
        pass
    
    union_insn_t_0._pack_ = 1 # source:False
    union_insn_t_0._fields_ = [
        ('auxpref', ctypes.c_uint32),
        ('auxpref_u16', ctypes.c_uint16 * 2),
        ('auxpref_u8', ctypes.c_ubyte * 4),
    ]
    
    class struct_op_t(Structure):
        pass
    
    class union_op_t_1(Union):
        pass
    
    union_op_t_1._pack_ = 1 # source:False
    union_op_t_1._fields_ = [
        ('value', ctypes.c_uint64),
        ('value_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_op_t_0(Union):
        pass
    
    union_op_t_0._pack_ = 1 # source:False
    union_op_t_0._fields_ = [
        ('reg', ctypes.c_uint16),
        ('phrase', ctypes.c_uint16),
    ]
    
    class union_op_t_3(Union):
        pass
    
    union_op_t_3._pack_ = 1 # source:False
    union_op_t_3._fields_ = [
        ('specval', ctypes.c_uint64),
        ('specval_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_op_t_2(Union):
        pass
    
    union_op_t_2._pack_ = 1 # source:False
    union_op_t_2._fields_ = [
        ('addr', ctypes.c_uint64),
        ('addr_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_op_t._pack_ = 1 # source:False
    struct_op_t._anonymous_ = ('_0', '_1', '_2', '_3',)
    struct_op_t._fields_ = [
        ('n', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        ('offb', ctypes.c_char),
        ('offo', ctypes.c_char),
        ('flags', ctypes.c_ubyte),
        ('dtype', ctypes.c_ubyte),
        ('_0', union_op_t_0),
        ('_1', union_op_t_1),
        ('_2', union_op_t_2),
        ('_3', union_op_t_3),
        ('specflag1', ctypes.c_char),
        ('specflag2', ctypes.c_char),
        ('specflag3', ctypes.c_char),
        ('specflag4', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_insn_t._pack_ = 1 # source:False
    struct_insn_t._anonymous_ = ('_0',)
    struct_insn_t._fields_ = [
        ('cs', ctypes.c_uint64),
        ('ip', ctypes.c_uint64),
        ('ea', ctypes.c_uint64),
        ('itype', ctypes.c_uint16),
        ('size', ctypes.c_uint16),
        ('_0', union_insn_t_0),
        ('segpref', ctypes.c_char),
        ('insnpref', ctypes.c_char),
        ('flags', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ops', struct_op_t * 8),
    ]
    
    class struct_qvector_op_t_(Structure):
        pass
    
    struct_qvector_op_t_._pack_ = 1 # source:False
    struct_qvector_op_t_._fields_ = [
        ('array', ctypes.POINTER(struct_op_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    tracked_regs_t = struct_qvector_op_t_
    struct_jump_pattern_t._pack_ = 1 # source:False
    struct_jump_pattern_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_jump_pattern_t_vtbl)),
        ('modifying_r32_spoils_r64', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('insn', struct_insn_t),
        ('si', ctypes.POINTER(struct_switch_info_t)),
        ('eas', ctypes.c_uint64 * 16),
        ('skip', ctypes.c_char * 16),
        ('non_spoiled_reg', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('check', struct__C21FB2E1BAA97F44BFD298211C4C916B * 16),
        ('stop_matching', ctypes.c_char),
        ('in_linear_flow', ctypes.c_char),
        ('PADDING_2', ctypes.c_ubyte * 6),
        ('block_end', ctypes.c_uint64),
        ('depends', ctypes.POINTER(ctypes.c_char * 4)),
        ('remote_code', eavec_t),
        ('extra_insn_eas', eavec_t),
        ('regs', tracked_regs_t),
    ]
    
    struct_locchange_md_t._pack_ = 1 # source:False
    struct_locchange_md_t._fields_ = [
        ('cb', ctypes.c_ubyte),
        ('r', ctypes.c_ubyte),
        ('f', ctypes.c_ubyte),
        ('reserved', ctypes.c_ubyte),
    ]
    
    class struct_plugmod_t_vtbl(Structure):
        pass
    
    struct_process_info_t._pack_ = 1 # source:False
    struct_process_info_t._fields_ = [
        ('pid', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', qstring),
    ]
    
    class struct_procmod_t_vtbl(Structure):
        pass
    
    struct_qbasic_block_t._pack_ = 1 # source:False
    struct_qbasic_block_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('succ', intvec_t),
        ('pred', intvec_t),
    ]
    
    class struct_qvector_bpt_t_(Structure):
        pass
    
    struct_qvector_bpt_t_._pack_ = 1 # source:False
    struct_qvector_bpt_t_._fields_ = [
        ('array', ctypes.POINTER(struct_bpt_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_qvector_kvp_t_(Structure):
        pass
    
    class struct_kvp_t(Structure):
        pass
    
    struct_qvector_kvp_t_._pack_ = 1 # source:False
    struct_qvector_kvp_t_._fields_ = [
        ('array', ctypes.POINTER(struct_kvp_t)),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    struct_refinfo_desc_t._pack_ = 1 # source:False
    struct_refinfo_desc_t._fields_ = [
        ('type', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('desc', ctypes.c_char_p),
    ]
    
    class struct_reg_accesses_t(Structure):
        pass
    
    struct_reg_accesses_t._pack_ = 1 # source:False
    struct_reg_accesses_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_std__less_int_(Structure):
        pass
    
    struct_synced_group_t._pack_ = 1 # source:False
    struct_synced_group_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    tev_reg_values_t = struct_qvector_tev_reg_value_t_
    
    # values for enumeration 'tev_type_t'
    tev_type_t__enumvalues = {
        0: 'tev_none',
        1: 'tev_insn',
        2: 'tev_call',
        3: 'tev_ret',
        4: 'tev_bpt',
        5: 'tev_mem',
        6: 'tev_event',
        7: 'tev_max',
    }
    tev_none = 0
    tev_insn = 1
    tev_call = 2
    tev_ret = 3
    tev_bpt = 4
    tev_mem = 5
    tev_event = 6
    tev_max = 7
    tev_type_t = ctypes.c_uint32 # enum
    struct_tev_info_t._pack_ = 1 # source:False
    struct_tev_info_t._fields_ = [
        ('type', tev_type_t),
        ('tid', ctypes.c_int32),
        ('ea', ctypes.c_uint64),
    ]
    
    struct_tev_info_reg_t._pack_ = 1 # source:False
    struct_tev_info_reg_t._fields_ = [
        ('info', struct_tev_info_t),
        ('registers', tev_reg_values_t),
    ]
    
    class struct_udtmembervec_t(Structure):
        pass
    
    struct_udtmembervec_t._pack_ = 1 # source:False
    struct_udtmembervec_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_action_desc_t(Structure):
        pass
    
    struct_action_desc_t._pack_ = 1 # source:False
    struct_action_desc_t._fields_ = [
        ('cb', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('label', ctypes.c_char_p),
        ('handler', ctypes.POINTER(struct_action_handler_t)),
        ('owner', ctypes.POINTER(None)),
        ('shortcut', ctypes.c_char_p),
        ('tooltip', ctypes.c_char_p),
        ('icon', ctypes.c_int32),
        ('flags', ctypes.c_int32),
    ]
    
    class struct_bpt_visitor_t(Structure):
        pass
    
    struct_bpt_visitor_t._pack_ = 1 # source:False
    struct_bpt_visitor_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_bpt_visitor_t_vtbl)),
        ('range', struct_range_t),
        ('name', ctypes.c_char_p),
    ]
    
    class struct_data_format_t(Structure):
        pass
    
    struct_data_format_t._pack_ = 1 # source:False
    struct_data_format_t._fields_ = [
        ('cbsize', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ud', ctypes.POINTER(None)),
        ('props', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('menu_name', ctypes.c_char_p),
        ('hotkey', ctypes.c_char_p),
        ('value_size', ctypes.c_uint64),
        ('text_width', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('print', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(None), ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32)),
        ('scan', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(None), ctypes.POINTER(struct_bytevec_t), ctypes.c_char_p, ctypes.c_uint64, ctypes.c_int32, ctypes.POINTER(struct__qstring_char_))),
        ('analyze', ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_int32)),
    ]
    
    
    # values for enumeration 'event_id_t'
    event_id_t__enumvalues = {
        0: 'NO_EVENT',
        1: 'PROCESS_STARTED',
        2: 'PROCESS_EXITED',
        4: 'THREAD_STARTED',
        8: 'THREAD_EXITED',
        16: 'BREAKPOINT',
        32: 'STEP',
        64: 'EXCEPTION',
        128: 'LIB_LOADED',
        256: 'LIB_UNLOADED',
        512: 'INFORMATION',
        1024: 'PROCESS_ATTACHED',
        2048: 'PROCESS_DETACHED',
        4096: 'PROCESS_SUSPENDED',
        8192: 'TRACE_FULL',
    }
    NO_EVENT = 0
    PROCESS_STARTED = 1
    PROCESS_EXITED = 2
    THREAD_STARTED = 4
    THREAD_EXITED = 8
    BREAKPOINT = 16
    STEP = 32
    EXCEPTION = 64
    LIB_LOADED = 128
    LIB_UNLOADED = 256
    INFORMATION = 512
    PROCESS_ATTACHED = 1024
    PROCESS_DETACHED = 2048
    PROCESS_SUSPENDED = 4096
    TRACE_FULL = 8192
    event_id_t = ctypes.c_uint32 # enum
    struct_debug_event_t._pack_ = 1 # source:False
    struct_debug_event_t._fields_ = [
        ('pid', ctypes.c_int32),
        ('tid', ctypes.c_int32),
        ('ea', ctypes.c_uint64),
        ('handled', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('_eid', event_id_t),
        ('bytes', ctypes.c_char * 48),
    ]
    
    struct_enum_member_t._pack_ = 1 # source:False
    struct_enum_member_t._fields_ = [
        ('name', qstring),
        ('cmt', qstring),
        ('value', ctypes.c_uint64),
    ]
    
    class struct_ext_idcfunc_t(Structure):
        pass
    
    struct_ext_idcfunc_t._pack_ = 1 # source:False
    struct_ext_idcfunc_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('fptr', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t))),
        ('args', ctypes.c_char_p),
        ('defvals', ctypes.POINTER(struct_idc_value_t)),
        ('ndefvals', ctypes.c_int32),
        ('flags', ctypes.c_int32),
    ]
    
    class struct_input_event_t(Structure):
        pass
    
    class union_input_event_t_0(Union):
        pass
    
    union_input_event_t_0._pack_ = 1 # source:False
    union_input_event_t_0._fields_ = [
        ('shortcut', struct_input_event_t__input_event_shortcut_data_t),
        ('keyboard', struct_input_event_t__input_event_keyboard_data_t),
        ('mouse', struct_input_event_t__input_event_mouse_data_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    
    # values for enumeration 'input_event_kind_t'
    input_event_kind_t__enumvalues = {
        0: 'iek_unknown',
        1: 'iek_shortcut',
        2: 'iek_key_press',
        3: 'iek_key_release',
        4: 'iek_mouse_button_press',
        5: 'iek_mouse_button_release',
        6: 'iek_mouse_wheel',
    }
    iek_unknown = 0
    iek_shortcut = 1
    iek_key_press = 2
    iek_key_release = 3
    iek_mouse_button_press = 4
    iek_mouse_button_release = 5
    iek_mouse_wheel = 6
    input_event_kind_t = ctypes.c_uint32 # enum
    struct_input_event_t._pack_ = 1 # source:False
    struct_input_event_t._anonymous_ = ('_0',)
    struct_input_event_t._fields_ = [
        ('cb', ctypes.c_int32),
        ('kind', input_event_kind_t),
        ('modifiers', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('target', ctypes.POINTER(struct_TWidget)),
        ('source', ctypes.POINTER(None)),
        ('_0', union_input_event_t_0),
    ]
    
    struct_memory_info_t._pack_ = 1 # source:False
    struct_memory_info_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('name', qstring),
        ('sclass', qstring),
        ('sbase', ctypes.c_uint64),
        ('bitness', ctypes.c_ubyte),
        ('perm', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 6),
    ]
    
    struct_memreg_info_t._pack_ = 1 # source:False
    struct_memreg_info_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('bytes', struct_bytevec_t),
    ]
    
    struct_movbpt_info_t._pack_ = 1 # source:False
    struct_movbpt_info_t._fields_ = [
        ('from', struct_bpt_location_t),
        ('to', struct_bpt_location_t),
    ]
    
    class struct_node_iterator(Structure):
        pass
    
    class struct_gdl_graph_t(Structure):
        pass
    
    struct_node_iterator._pack_ = 1 # source:False
    struct_node_iterator._fields_ = [
        ('g', ctypes.POINTER(struct_gdl_graph_t)),
        ('i', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_outctx_base_t(Structure):
        pass
    
    struct_outctx_base_t._pack_ = 1 # source:False
    struct_outctx_base_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_outctx_base_t_vtbl)),
        ('insn_ea', ctypes.c_uint64),
        ('outbuf', qstring),
        ('regname_idx', ctypes.c_int64),
        ('suspop', ctypes.c_int32),
        ('F', ctypes.c_uint32),
        ('outvalues', ctypes.POINTER(ctypes.c_uint64)),
        ('outvalue_getn_flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('user_data', ctypes.POINTER(None)),
        ('kern_data', ctypes.POINTER(None)),
        ('lnar', ctypes.POINTER(struct_qvector__qstring_char__)),
        ('lnar_maxsize', ctypes.c_int32),
        ('default_lnnum', ctypes.c_int32),
        ('line_prefix', qstring),
        ('prefix_len', ctypes.c_int64),
        ('ctxflags', ctypes.c_int32),
        ('ind0', ctypes.c_int32),
        ('cmt_ea', ctypes.c_uint64),
        ('cmtbuf', qstring),
        ('cmtptr', ctypes.c_char_p),
        ('cmtcolor', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    class struct_outctx_t_vtbl(Structure):
        pass
    
    class struct_plugin_info_t(Structure):
        pass
    
    class struct_plugin_t(Structure):
        pass
    
    class struct_idadll_t(Structure):
        pass
    
    struct_idadll_t._pack_ = 1 # source:False
    struct_idadll_t._fields_ = [
        ('dllinfo', ctypes.POINTER(None) * 10),
        ('entry', ctypes.POINTER(None)),
    ]
    
    struct_plugin_info_t._pack_ = 1 # source:False
    struct_plugin_info_t._fields_ = [
        ('next', ctypes.POINTER(struct_plugin_info_t)),
        ('path', ctypes.c_char_p),
        ('org_name', ctypes.c_char_p),
        ('name', ctypes.c_char_p),
        ('org_hotkey', ctypes.c_uint16),
        ('hotkey', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('arg', ctypes.c_uint64),
        ('entry', ctypes.POINTER(struct_plugin_t)),
        ('dllmem', struct_idadll_t),
        ('flags', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('comment', ctypes.c_char_p),
    ]
    
    class struct_qflow_chart_t(Structure):
        pass
    
    qflow_chart_t__blocks_t = struct_qvector_qbasic_block_t_
    struct_qflow_chart_t._pack_ = 1 # source:False
    struct_qflow_chart_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('title', qstring),
        ('bounds', struct_range_t),
        ('pfn', ctypes.POINTER(struct_func_t)),
        ('flags', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('blocks', qflow_chart_t__blocks_t),
        ('nproper', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class struct_qrefcnt_obj_t(Structure):
        pass
    
    struct_qrefcnt_obj_t._pack_ = 1 # source:False
    struct_qrefcnt_obj_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_qrefcnt_obj_t_vtbl)),
        ('refcnt', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_qvector_bool_(Structure):
        pass
    
    struct_qvector_bool_._pack_ = 1 # source:False
    struct_qvector_bool_._fields_ = [
        ('array', ctypes.c_char_p),
        ('n', ctypes.c_uint64),
        ('alloc', ctypes.c_uint64),
    ]
    
    class struct_regex_cache_t(Structure):
        pass
    
    regex_cache_t__regex_cache_map_t = struct_std__map__qstring_char___qrefcnt_t_refcnted_regex_t__
    struct_regex_cache_t._pack_ = 1 # source:False
    struct_regex_cache_t._fields_ = [
        ('cache', regex_cache_t__regex_cache_map_t),
    ]
    
    struct_source_file_t._pack_ = 1 # source:False
    struct_source_file_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    struct_source_item_t._pack_ = 1 # source:False
    struct_source_item_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_source_view_t(Structure):
        pass
    
    class struct_std__set_int_(Structure):
        pass
    
    struct_std__set_int_._pack_ = 1 # source:False
    struct_std__set_int_._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_string_info_t(Structure):
        pass
    
    struct_string_info_t._pack_ = 1 # source:False
    struct_string_info_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('length', ctypes.c_int32),
        ('type', ctypes.c_int32),
    ]
    
    class struct_structplace_t(Structure):
        pass
    
    struct_structplace_t._pack_ = 1 # source:False
    struct_structplace_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('idx', ctypes.c_uint64),
        ('offset', ctypes.c_uint64),
    ]
    
    class struct_strwinsetup_t(Structure):
        pass
    
    struct_strwinsetup_t._pack_ = 1 # source:False
    struct_strwinsetup_t._fields_ = [
        ('strtypes', struct_bytevec_t),
        ('minlen', ctypes.c_int64),
        ('display_only_existing_strings', ctypes.c_ubyte),
        ('only_7bit', ctypes.c_ubyte),
        ('ignore_heads', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 5),
    ]
    
    class union_switch_info_t_0(Union):
        pass
    
    union_switch_info_t_0._pack_ = 1 # source:False
    union_switch_info_t_0._fields_ = [
        ('values', ctypes.c_uint64),
        ('lowcase', ctypes.c_uint64),
    ]
    
    struct_switch_info_t._pack_ = 1 # source:False
    struct_switch_info_t._anonymous_ = ('_0',)
    struct_switch_info_t._fields_ = [
        ('flags', ctypes.c_uint32),
        ('ncases', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('jumps', ctypes.c_uint64),
        ('_0', union_switch_info_t_0),
        ('defjump', ctypes.c_uint64),
        ('startea', ctypes.c_uint64),
        ('jcases', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('ind_lowcase', ctypes.c_int64),
        ('elbase', ctypes.c_uint64),
        ('regnum', ctypes.c_int32),
        ('regdtype', ctypes.c_ubyte),
        ('PADDING_2', ctypes.c_ubyte * 3),
        ('custom', ctypes.c_uint64),
        ('version', ctypes.c_int32),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('expr_ea', ctypes.c_uint64),
        ('marks', eavec_t),
    ]
    
    struct_sync_source_t._pack_ = 1 # source:False
    struct_sync_source_t._fields_ = [
        ('storage', ctypes.c_ubyte * 16),
    ]
    
    struct_thread_name_t._pack_ = 1 # source:False
    struct_thread_name_t._fields_ = [
        ('tid', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', qstring),
    ]
    
    class struct_try_handler_t(Structure):
        pass
    
    struct_try_handler_t._pack_ = 1 # source:False
    struct_try_handler_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('disp', ctypes.c_int64),
        ('fpreg', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_ui_requests_t(Structure):
        pass
    
    struct_ui_requests_t._pack_ = 1 # source:False
    struct_ui_requests_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_value_u__dq_t(Structure):
        pass
    
    struct_value_u__dq_t._pack_ = 1 # source:False
    struct_value_u__dq_t._fields_ = [
        ('low', ctypes.c_uint32),
        ('high', ctypes.c_uint32),
    ]
    
    class struct_value_u__dt_t(Structure):
        pass
    
    struct_value_u__dt_t._pack_ = 1 # source:False
    struct_value_u__dt_t._fields_ = [
        ('low', ctypes.c_uint32),
        ('high', ctypes.c_uint32),
        ('upper', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 2),
    ]
    
    class struct_TPointDouble(Structure):
        pass
    
    struct_TPointDouble._pack_ = 1 # source:False
    struct_TPointDouble._fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double),
    ]
    
    class struct_addon_info_t(Structure):
        pass
    
    struct_addon_info_t._pack_ = 1 # source:False
    struct_addon_info_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('id', ctypes.c_char_p),
        ('name', ctypes.c_char_p),
        ('producer', ctypes.c_char_p),
        ('version', ctypes.c_char_p),
        ('url', ctypes.c_char_p),
        ('freeform', ctypes.c_char_p),
        ('custom_data', ctypes.POINTER(None)),
        ('custom_size', ctypes.c_uint64),
    ]
    
    class struct_call_stack_t(Structure):
        pass
    
    struct_call_stack_t._pack_ = 1 # source:False
    struct_call_stack_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_cfgopt_t(Structure):
        pass
    
    struct_cfgopt_set_t._pack_ = 1 # source:False
    struct_cfgopt_set_t._fields_ = [
        ('opts', ctypes.POINTER(struct_cfgopt_t)),
        ('nopts', ctypes.c_uint64),
        ('cb', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_cfgopt_t), ctypes.c_int32, ctypes.POINTER(None))),
        ('obj', ctypes.POINTER(None)),
    ]
    
    class struct_edge_typer_t(Structure):
        pass
    
    class struct_elf_loader_t(Structure):
        pass
    
    class struct_enum_const_t(Structure):
        pass
    
    struct_enum_const_t._pack_ = 1 # source:False
    struct_enum_const_t._fields_ = [
        ('tid', ctypes.c_uint64),
        ('serial', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    struct_fixup_data_t._pack_ = 1 # source:False
    struct_fixup_data_t._fields_ = [
        ('type', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('flags', ctypes.c_uint32),
        ('base', ctypes.c_uint64),
        ('sel', ctypes.c_uint64),
        ('off', ctypes.c_uint64),
        ('displacement', ctypes.c_int64),
    ]
    
    struct_fixup_info_t._pack_ = 1 # source:False
    struct_fixup_info_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('fd', struct_fixup_data_t),
    ]
    
    class struct_graph_item_t(Structure):
        pass
    
    
    # values for enumeration 'graph_item_type_t'
    graph_item_type_t__enumvalues = {
        0: 'git_none',
        1: 'git_edge',
        2: 'git_node',
        3: 'git_tool',
        4: 'git_text',
        5: 'git_elp',
    }
    git_none = 0
    git_edge = 1
    git_node = 2
    git_tool = 3
    git_text = 4
    git_elp = 5
    graph_item_type_t = ctypes.c_uint32 # enum
    struct_graph_item_t._pack_ = 1 # source:False
    struct_graph_item_t._fields_ = [
        ('type', graph_item_type_t),
        ('e', struct_edge_t),
        ('n', ctypes.c_int32),
        ('b', ctypes.c_int32),
        ('p', struct_point_t),
        ('elp', struct_edge_layout_point_t),
    ]
    
    class union_idc_value_t_0(Union):
        pass
    
    class struct_idc_object_t(Structure):
        pass
    
    union_idc_value_t_0._pack_ = 1 # source:False
    union_idc_value_t_0._fields_ = [
        ('num', ctypes.c_int64),
        ('e', struct_fpvalue_t),
        ('obj', ctypes.POINTER(struct_idc_object_t)),
        ('funcidx', ctypes.c_int32),
        ('pvoid', ctypes.POINTER(None)),
        ('i64', ctypes.c_int64),
        ('reserve', ctypes.c_ubyte * 24),
    ]
    
    struct_idc_value_t._pack_ = 1 # source:False
    struct_idc_value_t._anonymous_ = ('_0',)
    struct_idc_value_t._fields_ = [
        ('vtype', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('_0', union_idc_value_t_0),
    ]
    
    struct_idc_global_t._pack_ = 1 # source:False
    struct_idc_global_t._fields_ = [
        ('name', qstring),
        ('value', struct_idc_value_t),
    ]
    
    class struct_idd_opinfo_t(Structure):
        pass
    
    struct_idd_opinfo_t._pack_ = 1 # source:False
    struct_idd_opinfo_t._fields_ = [
        ('modified', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('ea', ctypes.c_uint64),
        ('value', struct_regval_t),
        ('debregidx', ctypes.c_int32),
        ('value_size', ctypes.c_int32),
    ]
    
    class struct_interr_exc_t(Structure):
        pass
    
    struct_interr_exc_t._pack_ = 1 # source:False
    struct_interr_exc_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('code', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    struct_ioport_bit_t._pack_ = 1 # source:False
    struct_ioport_bit_t._fields_ = [
        ('name', qstring),
        ('cmt', qstring),
    ]
    
    class struct_lock_segment(Structure):
        pass
    
    struct_lock_segment._pack_ = 1 # source:False
    struct_lock_segment._fields_ = [
        ('segm', ctypes.POINTER(struct_segment_t)),
    ]
    
    class struct_merge_data_t(Structure):
        pass
    
    class struct_place_t_vtbl(Structure):
        pass
    
    
    # values for enumeration 'access_type_t'
    access_type_t__enumvalues = {
        0: 'NO_ACCESS',
        1: 'WRITE_ACCESS',
        2: 'READ_ACCESS',
        3: 'RW_ACCESS',
    }
    NO_ACCESS = 0
    WRITE_ACCESS = 1
    READ_ACCESS = 2
    RW_ACCESS = 3
    access_type_t = ctypes.c_uint8 # enum
    class struct_bitrange_t(Structure):
        pass
    
    struct_bitrange_t._pack_ = 1 # source:False
    struct_bitrange_t._fields_ = [
        ('offset', ctypes.c_uint16),
        ('nbits', ctypes.c_uint16),
    ]
    
    struct_reg_access_t._pack_ = 1 # source:False
    struct_reg_access_t._fields_ = [
        ('regnum', ctypes.c_int32),
        ('range', struct_bitrange_t),
        ('access_type', access_type_t),
        ('opnum', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 2),
    ]
    
    class struct_reloc_info_t(Structure):
        pass
    
    struct_reloc_info_t._pack_ = 1 # source:False
    struct_reloc_info_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_simple_bfi_t._pack_ = 1 # source:False
    struct_simple_bfi_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 104),
        ('regs_', struct_no_regs_t),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    struct_simpleline_t._pack_ = 1 # source:False
    struct_simpleline_t._fields_ = [
        ('line', qstring),
        ('color', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('bgcolor', ctypes.c_uint32),
    ]
    
    class struct_sreg_range_t(Structure):
        pass
    
    struct_sreg_range_t._pack_ = 1 # source:False
    struct_sreg_range_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('val', ctypes.c_uint64),
        ('tag', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    class struct_til_bucket_t(Structure):
        pass
    
    class struct_til_stream_t(Structure):
        pass
    
    class struct_til_symbol_t(Structure):
        pass
    
    struct_til_symbol_t._pack_ = 1 # source:False
    struct_til_symbol_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('til', ctypes.POINTER(struct_til_t)),
    ]
    
    struct_udt_member_t._pack_ = 1 # source:False
    struct_udt_member_t._fields_ = [
        ('offset', ctypes.c_uint64),
        ('size', ctypes.c_uint64),
        ('name', qstring),
        ('cmt', qstring),
        ('type', struct_tinfo_t),
        ('effalign', ctypes.c_int32),
        ('tafld_bits', ctypes.c_uint32),
        ('fda', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 3),
    ]
    
    class struct_ui_request_t(Structure):
        pass
    
    struct_ui_request_t._pack_ = 1 # source:False
    struct_ui_request_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_ui_request_t_vtbl)),
    ]
    
    class struct___qthread_t(Structure):
        pass
    
    class struct_bookmarks_t(Structure):
        pass
    
    class struct_data_type_t(Structure):
        pass
    
    struct_data_type_t._pack_ = 1 # source:False
    struct_data_type_t._fields_ = [
        ('cbsize', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ud', ctypes.POINTER(None)),
        ('props', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('menu_name', ctypes.c_char_p),
        ('hotkey', ctypes.c_char_p),
        ('asm_keyword', ctypes.c_char_p),
        ('value_size', ctypes.c_uint64),
        ('may_create_at', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_uint64)),
        ('calc_item_size', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_uint64)),
    ]
    
    class struct_edge_info_t(Structure):
        pass
    
    class struct_pointseq_t(Structure):
        pass
    
    struct_pointseq_t._pack_ = 1 # source:False
    struct_pointseq_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_edge_info_t._pack_ = 1 # source:False
    struct_edge_info_t._fields_ = [
        ('color', ctypes.c_uint32),
        ('width', ctypes.c_int32),
        ('srcoff', ctypes.c_int32),
        ('dstoff', ctypes.c_int32),
        ('layout', struct_pointseq_t),
    ]
    
    class struct_enumplace_t(Structure):
        pass
    
    struct_enumplace_t._pack_ = 1 # source:False
    struct_enumplace_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('idx', ctypes.c_uint64),
        ('bmask', ctypes.c_uint64),
        ('value', ctypes.c_uint64),
        ('serial', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    class struct_exehdr_full(Structure):
        pass
    
    struct_exehdr_full._pack_ = 1 # source:False
    struct_exehdr_full._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 28),
        ('res', ctypes.c_uint16 * 4),
        ('oemid', ctypes.c_uint16),
        ('oeminfo', ctypes.c_uint16),
        ('res2', ctypes.c_uint16 * 10),
        ('lfanew', ctypes.c_uint32),
    ]
    
    struct_gdl_graph_t._pack_ = 1 # source:False
    struct_gdl_graph_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_gdl_graph_t_vtbl)),
    ]
    
    class struct_idc_class_t(Structure):
        pass
    
    class struct_lex_value_t(Structure):
        pass
    
    class union_lex_value_t_0(Union):
        pass
    
    union_lex_value_t_0._pack_ = 1 # source:False
    union_lex_value_t_0._fields_ = [
        ('val', ctypes.c_int64),
        ('uval', ctypes.c_uint64),
    ]
    
    struct_lex_value_t._pack_ = 1 # source:False
    struct_lex_value_t._anonymous_ = ('_0',)
    struct_lex_value_t._fields_ = [
        ('is_unsigned', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('_0', union_lex_value_t_0),
    ]
    
    class struct_linearray_t(Structure):
        pass
    
    struct_linearray_t._pack_ = 1 # source:False
    struct_linearray_t._fields_ = [
        ('lines', qstrvec_t),
        ('at', ctypes.POINTER(struct_place_t)),
        ('ud', ctypes.POINTER(None)),
        ('prefix_color', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('bg_color', ctypes.c_uint32),
        ('extra', qstring),
        ('dlnnum', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_load_info_t(Structure):
        pass
    
    
    # values for enumeration 'filetype_t'
    filetype_t__enumvalues = {
        0: 'f_EXE_old',
        1: 'f_COM_old',
        2: 'f_BIN',
        3: 'f_DRV',
        4: 'f_WIN',
        5: 'f_HEX',
        6: 'f_MEX',
        7: 'f_LX',
        8: 'f_LE',
        9: 'f_NLM',
        10: 'f_COFF',
        11: 'f_PE',
        12: 'f_OMF',
        13: 'f_SREC',
        14: 'f_ZIP',
        15: 'f_OMFLIB',
        16: 'f_AR',
        17: 'f_LOADER',
        18: 'f_ELF',
        19: 'f_W32RUN',
        20: 'f_AOUT',
        21: 'f_PRC',
        22: 'f_EXE',
        23: 'f_COM',
        24: 'f_AIXAR',
        25: 'f_MACHO',
        26: 'f_PSXOBJ',
    }
    f_EXE_old = 0
    f_COM_old = 1
    f_BIN = 2
    f_DRV = 3
    f_WIN = 4
    f_HEX = 5
    f_MEX = 6
    f_LX = 7
    f_LE = 8
    f_NLM = 9
    f_COFF = 10
    f_PE = 11
    f_OMF = 12
    f_SREC = 13
    f_ZIP = 14
    f_OMFLIB = 15
    f_AR = 16
    f_LOADER = 17
    f_ELF = 18
    f_W32RUN = 19
    f_AOUT = 20
    f_PRC = 21
    f_EXE = 22
    f_COM = 23
    f_AIXAR = 24
    f_MACHO = 25
    f_PSXOBJ = 26
    filetype_t = ctypes.c_uint32 # enum
    struct_load_info_t._pack_ = 1 # source:False
    struct_load_info_t._fields_ = [
        ('next', ctypes.POINTER(struct_load_info_t)),
        ('dllname', qstring),
        ('ftypename', qstring),
        ('processor', qstring),
        ('ftype', filetype_t),
        ('loader_flags', ctypes.c_uint32),
        ('lflags', ctypes.c_uint32),
        ('pri', ctypes.c_int32),
    ]
    
    class struct_node_info_t(Structure):
        pass
    
    struct_node_info_t._pack_ = 1 # source:False
    struct_node_info_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('bg_color', ctypes.c_uint32),
        ('frame_color', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ea', ctypes.c_uint64),
        ('text', qstring),
    ]
    
    class struct_predicate_t(Structure):
        pass
    
    struct_predicate_t._pack_ = 1 # source:False
    struct_predicate_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_predicate_t_vtbl)),
    ]
    
    class struct_processor_t(Structure):
        pass
    
    class struct_bytes_t(Structure):
        pass
    
    class struct_instruc_t(Structure):
        pass
    
    class struct_asm_t(Structure):
        pass
    
    struct_processor_t._pack_ = 1 # source:False
    struct_processor_t._fields_ = [
        ('version', ctypes.c_int32),
        ('id', ctypes.c_int32),
        ('flag', ctypes.c_uint32),
        ('flag2', ctypes.c_uint32),
        ('cnbits', ctypes.c_int32),
        ('dnbits', ctypes.c_int32),
        ('psnames', ctypes.POINTER(ctypes.c_char_p)),
        ('plnames', ctypes.POINTER(ctypes.c_char_p)),
        ('assemblers', ctypes.POINTER(ctypes.POINTER(struct_asm_t))),
        ('_notify', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(None), ctypes.c_int32, ctypes.POINTER(ctypes.POINTER(None)))),
        ('reg_names', ctypes.POINTER(ctypes.c_char_p)),
        ('regs_num', ctypes.c_int32),
        ('reg_first_sreg', ctypes.c_int32),
        ('reg_last_sreg', ctypes.c_int32),
        ('segreg_size', ctypes.c_int32),
        ('reg_code_sreg', ctypes.c_int32),
        ('reg_data_sreg', ctypes.c_int32),
        ('codestart', ctypes.POINTER(struct_bytes_t)),
        ('retcodes', ctypes.POINTER(struct_bytes_t)),
        ('instruc_start', ctypes.c_int32),
        ('instruc_end', ctypes.c_int32),
        ('instruc', ctypes.POINTER(struct_instruc_t)),
        ('tbyte_size', ctypes.c_uint64),
        ('real_width', ctypes.c_char * 4),
        ('icode_return', ctypes.c_int32),
        ('unused_slot', ctypes.POINTER(None)),
    ]
    
    struct_simd_info_t._pack_ = 1 # source:False
    struct_simd_info_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('tif', struct_tinfo_t),
        ('size', ctypes.c_uint16),
        ('memtype', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte),
    ]
    
    class struct_text_sink_t(Structure):
        pass
    
    struct_text_sink_t._pack_ = 1 # source:False
    struct_text_sink_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_text_sink_t_vtbl)),
    ]
    
    struct_type_attr_t._pack_ = 1 # source:False
    struct_type_attr_t._fields_ = [
        ('key', qstring),
        ('value', struct_bytevec_t),
    ]
    
    class struct_type_mods_t(Structure):
        pass
    
    struct_type_mods_t._pack_ = 1 # source:False
    struct_type_mods_t._fields_ = [
        ('type', struct_tinfo_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', qstring),
        ('cmt', qstring),
        ('flags', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_MD5Context(Structure):
        pass
    
    struct_MD5Context._pack_ = 1 # source:False
    struct_MD5Context._fields_ = [
        ('buf', ctypes.c_uint32 * 4),
        ('bits', ctypes.c_uint32 * 2),
        ('in', ctypes.c_ubyte * 64),
    ]
    
    class struct_TPopupMenu(Structure):
        pass
    
    class struct___qtimer_t(Structure):
        pass
    
    struct_bptaddrs_t._pack_ = 1 # source:False
    struct_bptaddrs_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('bpt', ctypes.POINTER(struct_bpt_t)),
    ]
    
    class struct_callregs_t(Structure):
        pass
    
    
    # values for enumeration 'argreg_policy_t'
    argreg_policy_t__enumvalues = {
        0: 'ARGREGS_POLICY_UNDEFINED',
        1: 'ARGREGS_GP_ONLY',
        2: 'ARGREGS_INDEPENDENT',
        3: 'ARGREGS_BY_SLOTS',
        4: 'ARGREGS_FP_CONSUME_GP',
        5: 'ARGREGS_MIPS_O32',
    }
    ARGREGS_POLICY_UNDEFINED = 0
    ARGREGS_GP_ONLY = 1
    ARGREGS_INDEPENDENT = 2
    ARGREGS_BY_SLOTS = 3
    ARGREGS_FP_CONSUME_GP = 4
    ARGREGS_MIPS_O32 = 5
    argreg_policy_t = ctypes.c_uint32 # enum
    struct_callregs_t._pack_ = 1 # source:False
    struct_callregs_t._fields_ = [
        ('policy', argreg_policy_t),
        ('nregs', ctypes.c_int32),
        ('gpregs', intvec_t),
        ('fpregs', intvec_t),
    ]
    
    class struct_dbg_info_t(Structure):
        pass
    
    class struct_debugger_t(Structure):
        pass
    
    struct_dbg_info_t._pack_ = 1 # source:False
    struct_dbg_info_t._fields_ = [
        ('pi', ctypes.POINTER(struct_plugin_info_t)),
        ('dbg', ctypes.POINTER(struct_debugger_t)),
    ]
    
    struct_debugger_t._pack_ = 1 # source:False
    struct_debugger_t._fields_ = [
        ('version', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('id', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('processor', ctypes.c_char_p),
        ('flags', ctypes.c_uint32),
        ('flags2', ctypes.c_uint32),
        ('regclasses', ctypes.POINTER(ctypes.c_char_p)),
        ('default_regclasses', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('registers', ctypes.POINTER(struct_register_info_t)),
        ('nregs', ctypes.c_int32),
        ('memory_page_size', ctypes.c_int32),
        ('bpt_bytes', ctypes.POINTER(ctypes.c_ubyte)),
        ('bpt_size', ctypes.c_ubyte),
        ('filetype', ctypes.c_ubyte),
        ('resume_modes', ctypes.c_uint16),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('set_dbg_options', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None))),
        ('callback', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(None), ctypes.c_int32, ctypes.POINTER(ctypes.POINTER(None)))),
    ]
    
    struct_direntry_t._pack_ = 1 # source:False
    struct_direntry_t._fields_ = [
        ('idx', ctypes.c_uint64),
        ('isdir', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_eval_ctx_t(Structure):
        pass
    
    struct_eval_ctx_t._pack_ = 1 # source:False
    struct_eval_ctx_t._fields_ = [
        ('size_cb', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ea', ctypes.c_uint64),
    ]
    
    class struct_hexplace_t(Structure):
        pass
    
    struct_hexplace_t._pack_ = 1 # source:False
    struct_hexplace_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('sol', ctypes.c_uint64),
    ]
    
    class struct_idaplace_t(Structure):
        pass
    
    struct_idaplace_t._pack_ = 1 # source:False
    struct_idaplace_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('ea', ctypes.c_uint64),
    ]
    
    class struct_idcfuncs_t(Structure):
        pass
    
    struct_idcfuncs_t._pack_ = 1 # source:False
    struct_idcfuncs_t._fields_ = [
        ('qnty', ctypes.c_uint64),
        ('funcs', ctypes.POINTER(struct_ext_idcfunc_t)),
        ('startup', ctypes.CFUNCTYPE(ctypes.c_int32)),
        ('shutdown', ctypes.CFUNCTYPE(ctypes.c_int32)),
        ('init_idc', ctypes.CFUNCTYPE(None)),
        ('term_idc', ctypes.CFUNCTYPE(None)),
        ('is_database_open', ctypes.CFUNCTYPE(ctypes.c_char)),
        ('ea2str', ctypes.CFUNCTYPE(ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64, ctypes.c_uint64)),
        ('undeclared_variable_ok', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p)),
        ('get_unkvar', ctypes.c_int32),
        ('set_unkvar', ctypes.c_int32),
        ('exec_resolved_func', ctypes.c_int32),
        ('calc_sizeof', ctypes.c_int32),
        ('get_field_ea', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    idp_names_t = struct_qvector_idp_name_t_
    struct_idp_desc_t._pack_ = 1 # source:False
    struct_idp_desc_t._fields_ = [
        ('path', qstring),
        ('mtime', ctypes.c_int64),
        ('family', qstring),
        ('names', idp_names_t),
        ('is_script', ctypes.c_char),
        ('checked', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 6),
    ]
    
    struct_idp_name_t._pack_ = 1 # source:False
    struct_idp_name_t._fields_ = [
        ('lname', qstring),
        ('sname', qstring),
        ('hidden', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_interval_t(Structure):
        pass
    
    struct_interval_t._pack_ = 1 # source:False
    struct_interval_t._fields_ = [
        ('x0', ctypes.c_int32),
        ('x1', ctypes.c_int32),
    ]
    
    class struct_location_t(Structure):
        pass
    
    class struct_proc_def_t(Structure):
        pass
    
    class struct_qffblk64_t(Structure):
        pass
    
    class struct_qffblk_t(Structure):
        pass
    
    struct_qffblk_t._pack_ = 1 # source:False
    struct_qffblk_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('time_create', ctypes.c_int64),
        ('time_access', ctypes.c_int64),
        ('time_write', ctypes.c_int64),
        ('size', ctypes.c_int64),
        ('name', ctypes.c_char * 260),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('handle', ctypes.c_int64),
        ('attr', ctypes.c_int32),
        ('ff_ftime', ctypes.c_uint16),
        ('ff_fdate', ctypes.c_uint16),
    ]
    
    struct_qffblk64_t._pack_ = 1 # source:False
    struct_qffblk64_t._fields_ = [
        ('attrib', ctypes.c_int32),
        ('name', ctypes.c_char * 260),
        ('size', ctypes.c_uint64),
        ('ff_fdate', ctypes.c_uint16),
        ('ff_ftime', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('base', struct_qffblk_t),
    ]
    
    struct_rangeset_t._pack_ = 1 # source:False
    struct_rangeset_t._fields_ = [
        ('bag', struct_rangevec_t),
        ('cache', ctypes.POINTER(struct_range_t)),
        ('undo_code', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_reg_info_t._pack_ = 1 # source:False
    struct_reg_info_t._fields_ = [
        ('reg', ctypes.c_int32),
        ('size', ctypes.c_int32),
    ]
    
    class struct_regmatch_t(Structure):
        pass
    
    struct_regmatch_t._pack_ = 1 # source:False
    struct_regmatch_t._fields_ = [
        ('rm_so', ctypes.c_int32),
        ('rm_eo', ctypes.c_int32),
    ]
    
    struct_row_info_t._pack_ = 1 # source:False
    struct_row_info_t._fields_ = [
        ('nodes', intvec_t),
        ('top', ctypes.c_int32),
        ('bottom', ctypes.c_int32),
    ]
    
    snapshots_t = struct_qvector_snapshot_t__P_
    struct_snapshot_t._pack_ = 1 # source:False
    struct_snapshot_t._fields_ = [
        ('id', ctypes.c_uint64),
        ('flags', ctypes.c_uint16),
        ('desc', ctypes.c_char * 128),
        ('filename', ctypes.c_char * 260),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('children', snapshots_t),
    ]
    
    class struct_strarray_t(Structure):
        pass
    
    struct_strarray_t._pack_ = 1 # source:False
    struct_strarray_t._fields_ = [
        ('code', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('text', ctypes.c_char_p),
    ]
    
    struct_twinline_t._pack_ = 1 # source:False
    struct_twinline_t._fields_ = [
        ('at', ctypes.POINTER(struct_place_t)),
        ('line', qstring),
        ('prefix_color', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('bg_color', ctypes.c_uint32),
        ('is_default', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 7),
    ]
    
    struct_argpart_t._pack_ = 1 # source:False
    struct_argpart_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('off', ctypes.c_uint16),
        ('size', ctypes.c_uint16),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_bptaddr_t(Structure):
        pass
    
    struct_bptaddr_t._pack_ = 1 # source:False
    struct_bptaddr_t._fields_ = [
        ('hea', ctypes.c_uint64),
        ('kea', ctypes.c_uint64),
    ]
    
    class struct_chooser_t(Structure):
        pass
    
    struct_chooser_t._pack_ = 1 # source:False
    struct_chooser_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 184),
    ]
    
    class struct_cliopts_t(Structure):
        pass
    
    struct_cliopts_t._pack_ = 1 # source:False
    struct_cliopts_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('prog_name', qstring),
        ('epilog', qstring),
        ('printer', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p)),
    ]
    
    class struct_destset_t(Structure):
        pass
    
    class struct_dirspec_t(Structure):
        pass
    
    struct_dirspec_t._pack_ = 1 # source:False
    struct_dirspec_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_dirspec_t_vtbl)),
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('id', qstring),
    ]
    
    class struct_dirtree_t(Structure):
        pass
    
    struct_dirtree_t._pack_ = 1 # source:False
    struct_dirtree_t._fields_ = [
        ('d', ctypes.POINTER(struct_dirtree_impl_t)),
    ]
    
    struct_ea_name_t._pack_ = 1 # source:False
    struct_ea_name_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('name', qstring),
    ]
    
    class struct_edgeset_t(Structure):
        pass
    
    class struct_encoder_t(Structure):
        pass
    
    struct_encoder_t._pack_ = 1 # source:False
    struct_encoder_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_encoder_t_vtbl)),
    ]
    
    class struct_excinfo_t(Structure):
        pass
    
    struct_excinfo_t._pack_ = 1 # source:False
    struct_excinfo_t._fields_ = [
        ('code', ctypes.c_uint32),
        ('can_cont', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('ea', ctypes.c_uint64),
        ('info', qstring),
    ]
    
    struct_extlang_t._pack_ = 1 # source:False
    struct_extlang_t._fields_ = [
        ('size', ctypes.c_uint64),
        ('flags', ctypes.c_uint32),
        ('refcnt', ctypes.c_int32),
        ('name', ctypes.c_char_p),
        ('fileext', ctypes.c_char_p),
        ('highlighter', ctypes.POINTER(struct_syntax_highlighter_t)),
        ('compile_expr', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p, ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
        ('compile_file', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
        ('call_func', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct_idc_value_t), ctypes.c_uint64, ctypes.POINTER(struct__qstring_char_))),
        ('eval_expr', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.c_uint64, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
        ('eval_snippet', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
        ('create_object', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct_idc_value_t), ctypes.c_uint64, ctypes.POINTER(struct__qstring_char_))),
        ('get_attr', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p)),
        ('set_attr', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct_idc_value_t))),
        ('call_method', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct_idc_value_t), ctypes.c_uint64, ctypes.POINTER(struct__qstring_char_))),
        ('load_procmod', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
        ('unload_procmod', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
    ]
    
    struct_funcarg_t._pack_ = 1 # source:False
    struct_funcarg_t._fields_ = [
        ('argloc', struct_argloc_t),
        ('name', qstring),
        ('cmt', qstring),
        ('type', struct_tinfo_t),
        ('flags', ctypes.c_uint32),
    ]
    
    class struct_hexview_t(Structure):
        pass
    
    class struct_impinfo_t(Structure):
        pass
    
    struct_impinfo_t._pack_ = 1 # source:False
    struct_impinfo_t._fields_ = [
        ('dllname', ctypes.c_char_p),
        ('func', ctypes.CFUNCTYPE(None, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64)),
        ('node', ctypes.c_uint64),
    ]
    
    struct_instruc_t._pack_ = 1 # source:False
    struct_instruc_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('feature', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_libfunc_t(Structure):
        pass
    
    class struct_lochist_t(Structure):
        pass
    
    struct_lochist_t._pack_ = 1 # source:False
    struct_lochist_t._fields_ = [
        ('ud', ctypes.POINTER(None)),
        ('cur', struct_lochist_entry_t),
        ('node', struct_netnode),
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_lock_func(Structure):
        pass
    
    struct_lock_func._pack_ = 1 # source:False
    struct_lock_func._fields_ = [
        ('pfn', ctypes.POINTER(struct_func_t)),
    ]
    
    struct_modinfo_t._pack_ = 1 # source:False
    struct_modinfo_t._fields_ = [
        ('name', qstring),
        ('base', ctypes.c_uint64),
        ('size', ctypes.c_uint64),
        ('rebase_to', ctypes.c_uint64),
    ]
    
    class struct_plugmod_t(Structure):
        pass
    
    struct_plugmod_t._pack_ = 1 # source:False
    struct_plugmod_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_plugmod_t_vtbl)),
        ('owner', ctypes.c_uint64),
        ('reserved', ctypes.c_uint64),
    ]
    
    class struct_printop_t(Structure):
        pass
    
    class union_opinfo_t(Union):
        pass
    
    struct_refinfo_t._pack_ = 1 # source:False
    struct_refinfo_t._fields_ = [
        ('target', ctypes.c_uint64),
        ('base', ctypes.c_uint64),
        ('tdelta', ctypes.c_int64),
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_strpath_t(Structure):
        pass
    
    struct_strpath_t._pack_ = 1 # source:False
    struct_strpath_t._fields_ = [
        ('len', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ids', ctypes.c_uint64 * 32),
        ('delta', ctypes.c_int64),
    ]
    
    union_opinfo_t._pack_ = 1 # source:False
    union_opinfo_t._fields_ = [
        ('ri', struct_refinfo_t),
        ('tid', ctypes.c_uint64),
        ('path', struct_strpath_t),
        ('strtype', ctypes.c_int32),
        ('ec', struct_enum_const_t),
        ('cd', struct_custom_data_type_ids_t),
        ('PADDING_0', ctypes.c_ubyte * 254),
    ]
    
    struct_printop_t._pack_ = 1 # source:False
    struct_printop_t._fields_ = [
        ('flags', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('ti', union_opinfo_t),
        ('features', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('suspop', ctypes.c_int32),
        ('aflags', ctypes.c_uint32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class struct_procmod_t(Structure):
        pass
    
    struct_procmod_t._pack_ = 1 # source:False
    struct_procmod_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('ph', ctypes.POINTER(struct_processor_t)),
        ('ash', ctypes.POINTER(struct_asm_t)),
        ('procmod_flags', ctypes.c_uint64),
        ('reserved', ctypes.c_uint64),
    ]
    
    class struct_regobjs_t(Structure):
        pass
    
    struct_regobjs_t._pack_ = 1 # source:False
    struct_regobjs_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_segment_t._pack_ = 1 # source:False
    struct_segment_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('name', ctypes.c_uint64),
        ('sclass', ctypes.c_uint64),
        ('orgbase', ctypes.c_uint64),
        ('align', ctypes.c_ubyte),
        ('comb', ctypes.c_ubyte),
        ('perm', ctypes.c_ubyte),
        ('bitness', ctypes.c_ubyte),
        ('flags', ctypes.c_uint16),
        ('PADDING_1', ctypes.c_ubyte * 2),
        ('sel', ctypes.c_uint64),
        ('defsr', ctypes.c_uint64 * 16),
        ('type', ctypes.c_ubyte),
        ('PADDING_2', ctypes.c_ubyte * 3),
        ('color', ctypes.c_uint32),
    ]
    
    class struct_stkpnts_t(Structure):
        pass
    
    struct_stkpnts_t._pack_ = 1 # source:False
    struct_stkpnts_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_valinfo_t(Structure):
        pass
    
    struct_valinfo_t._pack_ = 1 # source:False
    struct_valinfo_t._fields_ = [
        ('loc', struct_argloc_t),
        ('label', qstring),
        ('type', struct_tinfo_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_valstrs_t(Structure):
        pass
    
    struct_valstrs_t._pack_ = 1 # source:False
    struct_valstrs_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_xrefblk_t(Structure):
        pass
    
    struct_xrefblk_t._pack_ = 1 # source:False
    struct_xrefblk_t._fields_ = [
        ('from', ctypes.c_uint64),
        ('to', ctypes.c_uint64),
        ('iscode', ctypes.c_ubyte),
        ('type', ctypes.c_ubyte),
        ('user', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 5),
    ]
    
    class struct_xrefpos_t(Structure):
        pass
    
    struct_xrefpos_t._pack_ = 1 # source:False
    struct_xrefpos_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('type', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class union_cfgopt_t_1(Union):
        pass
    
    union_cfgopt_t_1._pack_ = 1 # source:False
    union_cfgopt_t_1._fields_ = [
        ('buf_size', ctypes.c_uint64),
        ('num_range', struct_cfgopt_t__num_range_t),
        ('bit_flags', ctypes.c_uint32),
        ('params', struct_cfgopt_t__params_t),
        ('mbroff_obj', ctypes.POINTER(None)),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union_cfgopt_t_0(Union):
        pass
    
    class struct_lexer_t(Structure):
        pass
    
    union_cfgopt_t_0._pack_ = 1 # source:False
    union_cfgopt_t_0._fields_ = [
        ('ptr', ctypes.POINTER(None)),
        ('mbroff', ctypes.c_uint64),
        ('hnd', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t))),
        ('hnd2', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64)),
        ('hnd3', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(None))),
    ]
    
    struct_cfgopt_t._pack_ = 1 # source:False
    struct_cfgopt_t._anonymous_ = ('_0', '_1',)
    struct_cfgopt_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('_0', union_cfgopt_t_0),
        ('flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('_1', union_cfgopt_t_1),
    ]
    
    struct_cliopt_t._pack_ = 1 # source:False
    struct_cliopt_t._fields_ = [
        ('shortname', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('longname', ctypes.c_char_p),
        ('help', ctypes.c_char_p),
        ('handler', ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.POINTER(None))),
        ('nargs', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_idasgn_t(Structure):
        pass
    
    struct_intmap_t._pack_ = 1 # source:False
    struct_intmap_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    class struct_intset_t(Structure):
        pass
    
    struct_intset_t._pack_ = 1 # source:False
    struct_intset_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
    ]
    
    ioport_bits_t = struct_qvector_ioport_bit_t_
    struct_ioport_t._pack_ = 1 # source:False
    struct_ioport_t._fields_ = [
        ('address', ctypes.c_uint64),
        ('name', qstring),
        ('cmt', qstring),
        ('bits', ioport_bits_t),
        ('userdata', ctypes.POINTER(None)),
    ]
    
    class union_jvalue_t_0(Union):
        pass
    
    class struct_jarr_t(Structure):
        pass
    
    class struct_jobj_t(Structure):
        pass
    
    union_jvalue_t_0._pack_ = 1 # source:False
    union_jvalue_t_0._fields_ = [
        ('_num', ctypes.c_int64),
        ('_str', ctypes.POINTER(struct__qstring_char_)),
        ('_obj', ctypes.POINTER(struct_jobj_t)),
        ('_arr', ctypes.POINTER(struct_jarr_t)),
        ('_bool', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    
    # values for enumeration 'jtype_t'
    jtype_t__enumvalues = {
        0: 'JT_UNKNOWN',
        1: 'JT_NUM',
        2: 'JT_STR',
        3: 'JT_OBJ',
        4: 'JT_ARR',
        5: 'JT_BOOL',
    }
    JT_UNKNOWN = 0
    JT_NUM = 1
    JT_STR = 2
    JT_OBJ = 3
    JT_ARR = 4
    JT_BOOL = 5
    jtype_t = ctypes.c_uint32 # enum
    struct_jvalue_t._pack_ = 1 # source:False
    struct_jvalue_t._anonymous_ = ('_0',)
    struct_jvalue_t._fields_ = [
        ('_type', jtype_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('_0', union_jvalue_t_0),
    ]
    
    class struct_loader_t(Structure):
        pass
    
    struct_loader_t._pack_ = 1 # source:False
    struct_loader_t._fields_ = [
        ('version', ctypes.c_uint32),
        ('flags', ctypes.c_uint32),
        ('accept_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(struct_linput_t), ctypes.c_char_p)),
        ('load_file', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_linput_t), ctypes.c_uint16, ctypes.c_char_p)),
        ('save_file', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__iobuf), ctypes.c_char_p)),
        ('move_segm', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64, ctypes.c_char_p)),
        ('process_archive', ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(struct_linput_t), ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(ctypes.c_uint16), ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(struct__qstring_char_))),
    ]
    
    struct_lowcnd_t._pack_ = 1 # source:False
    struct_lowcnd_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('cndbody', qstring),
        ('type', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('orgbytes', struct_bytevec_t),
        ('cmd', struct_insn_t),
        ('compiled', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('size', ctypes.c_int32),
    ]
    
    struct_member_t._pack_ = 1 # source:False
    struct_member_t._fields_ = [
        ('id', ctypes.c_uint64),
        ('soff', ctypes.c_uint64),
        ('eoff', ctypes.c_uint64),
        ('flag', ctypes.c_uint32),
        ('props', ctypes.c_uint32),
    ]
    
    class struct_outctx_t(Structure):
        pass
    
    struct_outctx_t._pack_ = 1 # source:False
    struct_outctx_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 192),
        ('bin_ea', ctypes.c_uint64),
        ('bin_state', ctypes.c_char),
        ('PADDING_1', ctypes.c_ubyte * 3),
        ('gl_bpsize', ctypes.c_int32),
        ('bin_width', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('insn', struct_insn_t),
        ('curlabel', qstring),
        ('wif', ctypes.POINTER(struct_printop_t)),
        ('procmod', ctypes.POINTER(struct_procmod_t)),
        ('ph', ctypes.POINTER(struct_processor_t)),
        ('ash', ctypes.POINTER(struct_asm_t)),
        ('saved_immvals', ctypes.c_uint64 * 8),
    ]
    
    struct_plugin_t._pack_ = 1 # source:False
    struct_plugin_t._fields_ = [
        ('version', ctypes.c_int32),
        ('flags', ctypes.c_int32),
        ('init', ctypes.CFUNCTYPE(ctypes.POINTER(struct_plugmod_t))),
        ('term', ctypes.CFUNCTYPE(None)),
        ('run', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_uint64)),
        ('comment', ctypes.c_char_p),
        ('help', ctypes.c_char_p),
        ('wanted_name', ctypes.c_char_p),
        ('wanted_hotkey', ctypes.c_char_p),
    ]
    
    class struct_qstatbuf(Structure):
        pass
    
    struct_qstatbuf._pack_ = 1 # source:False
    struct_qstatbuf._fields_ = [
        ('qst_dev', ctypes.c_uint64),
        ('qst_ino', ctypes.c_uint32),
        ('qst_mode', ctypes.c_uint32),
        ('qst_nlink', ctypes.c_uint32),
        ('qst_uid', ctypes.c_uint32),
        ('qst_gid', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('qst_rdev', ctypes.c_uint64),
        ('qst_size', ctypes.c_int64),
        ('qst_blksize', ctypes.c_int32),
        ('qst_blocks', ctypes.c_int32),
        ('qst_atime', ctypes.c_uint64),
        ('qst_mtime', ctypes.c_uint64),
        ('qst_ctime', ctypes.c_uint64),
    ]
    
    class struct_reader_t(Structure):
        pass
    
    struct_regarg_t._pack_ = 1 # source:False
    struct_regarg_t._fields_ = [
        ('reg', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('type', ctypes.POINTER(ctypes.c_ubyte)),
        ('name', ctypes.c_char_p),
    ]
    
    struct_regobj_t._pack_ = 1 # source:False
    struct_regobj_t._fields_ = [
        ('regidx', ctypes.c_int32),
        ('relocate', ctypes.c_int32),
        ('value', struct_bytevec_t),
    ]
    
    struct_regvar_t._pack_ = 1 # source:False
    struct_regvar_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('canon', ctypes.c_char_p),
        ('user', ctypes.c_char_p),
        ('cmt', ctypes.c_char_p),
    ]
    
    class struct_relobj_t(Structure):
        pass
    
    struct_relobj_t._pack_ = 1 # source:False
    struct_relobj_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('base', ctypes.c_uint64),
        ('ri', struct_reloc_info_t),
    ]
    
    struct_stkpnt_t._pack_ = 1 # source:False
    struct_stkpnt_t._fields_ = [
        ('ea', ctypes.c_uint64),
        ('spd', ctypes.c_int64),
    ]
    
    struct_tryblk_t._pack_ = 1 # source:False
    struct_tryblk_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
        ('reserve', ctypes.c_char * 72),
        ('cb', ctypes.c_ubyte),
        ('kind', ctypes.c_ubyte),
        ('level', ctypes.c_ubyte),
        ('PADDING_1', ctypes.c_ubyte * 5),
    ]
    
    struct_valstr_t._pack_ = 1 # source:False
    struct_valstr_t._fields_ = [
        ('oneline', qstring),
        ('length', ctypes.c_uint64),
        ('members', ctypes.POINTER(struct_valstrs_t)),
        ('info', ctypes.POINTER(struct_valinfo_t)),
        ('props', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_bytes_t._pack_ = 1 # source:False
    struct_bytes_t._fields_ = [
        ('len', ctypes.c_ubyte),
        ('PADDING_0', ctypes.c_ubyte * 7),
        ('bytes', ctypes.POINTER(ctypes.c_ubyte)),
    ]
    
    struct_catch_t._pack_ = 1 # source:False
    struct_catch_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 40),
        ('obj', ctypes.c_int64),
        ('type_id', ctypes.c_int64),
    ]
    
    class struct_dbctx_t(Structure):
        pass
    
    class struct_idainfo(Structure):
        pass
    
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
    
    class struct_minsn_t(Structure):
        pass
    
    struct_place_t._pack_ = 1 # source:False
    struct_place_t._fields_ = [
        ('__vftable', ctypes.POINTER(struct_place_t_vtbl)),
        ('lnnum', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_struc_t._pack_ = 1 # source:False
    struct_struc_t._fields_ = [
        ('id', ctypes.c_uint64),
        ('memqty', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('members', ctypes.POINTER(struct_member_t)),
        ('age', ctypes.c_uint16),
        ('PADDING_1', ctypes.c_ubyte * 2),
        ('props', ctypes.c_uint32),
        ('ordinal', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class union_token_t_1(Union):
        pass
    
    union_token_t_1._pack_ = 1 # source:False
    union_token_t_1._fields_ = [
        ('fnum', struct_fpvalue_t),
        ('i64', ctypes.c_int64),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union_token_t_0(Union):
        pass
    
    union_token_t_0._pack_ = 1 # source:False
    union_token_t_0._fields_ = [
        ('unicode', ctypes.c_char),
        ('is_unsigned', ctypes.c_char),
    ]
    
    struct_token_t._pack_ = 1 # source:False
    struct_token_t._anonymous_ = ('_0', '_1',)
    struct_token_t._fields_ = [
        ('str', qstring),
        ('type', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('num', ctypes.c_int64),
        ('_0', union_token_t_0),
        ('PADDING_1', ctypes.c_ubyte * 7),
        ('_1', union_token_t_1),
    ]
    
    class struct_uint128(Structure):
        pass
    
    struct_uint128._pack_ = 1 # source:False
    struct_uint128._fields_ = [
        ('l', ctypes.c_uint64),
        ('h', ctypes.c_uint64),
    ]
    
    class struct_cast_t(Structure):
        pass
    
    struct_cast_t._pack_ = 1 # source:False
    struct_cast_t._fields_ = [
        ('is_unsigned', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 3),
        ('size', ctypes.c_int32),
    ]
    
    class struct_exehdr(Structure):
        pass
    
    struct_exehdr._pack_ = 1 # source:False
    struct_exehdr._fields_ = [
        ('exe_ident', ctypes.c_uint16),
        ('PartPag', ctypes.c_uint16),
        ('PageCnt', ctypes.c_uint16),
        ('ReloCnt', ctypes.c_uint16),
        ('HdrSize', ctypes.c_uint16),
        ('MinMem', ctypes.c_uint16),
        ('MaxMem', ctypes.c_uint16),
        ('ReloSS', ctypes.c_uint16),
        ('ExeSP', ctypes.c_uint16),
        ('ChkSum', ctypes.c_uint16),
        ('ExeIP', ctypes.c_uint16),
        ('ReloCS', ctypes.c_uint16),
        ('TablOff', ctypes.c_uint16),
        ('Overlay', ctypes.c_uint16),
    ]
    
    class union_func_t_0(Union):
        pass
    
    class struct_func_t_0_0(Structure):
        pass
    
    struct_func_t_0_0._pack_ = 1 # source:False
    struct_func_t_0_0._fields_ = [
        ('frame', ctypes.c_uint64),
        ('frsize', ctypes.c_uint64),
        ('frregs', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('argsize', ctypes.c_uint64),
        ('fpd', ctypes.c_uint64),
        ('color', ctypes.c_uint32),
        ('pntqty', ctypes.c_uint32),
        ('points', ctypes.POINTER(struct_stkpnt_t)),
        ('regvarqty', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('regvars', ctypes.POINTER(struct_regvar_t)),
        ('llabelqty', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('llabels', ctypes.POINTER(struct_llabel_t)),
        ('regargqty', ctypes.c_int32),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('regargs', ctypes.POINTER(struct_regarg_t)),
        ('tailqty', ctypes.c_int32),
        ('PADDING_4', ctypes.c_ubyte * 4),
        ('tails', ctypes.POINTER(struct_range_t)),
    ]
    
    class struct_func_t_0_1(Structure):
        pass
    
    struct_func_t_0_1._pack_ = 1 # source:False
    struct_func_t_0_1._fields_ = [
        ('owner', ctypes.c_uint64),
        ('refqty', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('referers', ctypes.POINTER(ctypes.c_uint64)),
    ]
    
    union_func_t_0._pack_ = 1 # source:False
    union_func_t_0._anonymous_ = ('_0', '_1',)
    union_func_t_0._fields_ = [
        ('_0', struct_func_t_0_0),
        ('_1', struct_func_t_0_1),
        ('PADDING_0', ctypes.c_ubyte * 96),
    ]
    
    struct_func_t._pack_ = 1 # source:False
    struct_func_t._anonymous_ = ('_0',)
    struct_func_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 16),
        ('flags', ctypes.c_uint64),
        ('_0', union_func_t_0),
    ]
    
    class struct_int128(Structure):
        pass
    
    struct_int128._pack_ = 1 # source:False
    struct_int128._fields_ = [
        ('l', ctypes.c_uint64),
        ('h', ctypes.c_int64),
    ]
    
    jvalues_t = struct_qvector_jvalue_t_
    struct_jarr_t._pack_ = 1 # source:False
    struct_jarr_t._fields_ = [
        ('values', jvalues_t),
    ]
    
    struct_jobj_t._pack_ = 1 # source:False
    struct_jobj_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    struct_rect_t._pack_ = 1 # source:False
    struct_rect_t._fields_ = [
        ('left', ctypes.c_int32),
        ('top', ctypes.c_int32),
        ('right', ctypes.c_int32),
        ('bottom', ctypes.c_int32),
    ]
    
    struct_rrel_t._pack_ = 1 # source:False
    struct_rrel_t._fields_ = [
        ('off', ctypes.c_int64),
        ('reg', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    struct_asm_t._pack_ = 1 # source:False
    struct_asm_t._fields_ = [
        ('flag', ctypes.c_uint32),
        ('uflag', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('name', ctypes.c_char_p),
        ('help', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('header', ctypes.POINTER(ctypes.c_char_p)),
        ('origin', ctypes.c_char_p),
        ('end', ctypes.c_char_p),
        ('cmnt', ctypes.c_char_p),
        ('ascsep', ctypes.c_char),
        ('accsep', ctypes.c_char),
        ('PADDING_2', ctypes.c_ubyte * 6),
        ('esccodes', ctypes.c_char_p),
        ('a_ascii', ctypes.c_char_p),
        ('a_byte', ctypes.c_char_p),
        ('a_word', ctypes.c_char_p),
        ('a_dword', ctypes.c_char_p),
        ('a_qword', ctypes.c_char_p),
        ('a_oword', ctypes.c_char_p),
        ('a_float', ctypes.c_char_p),
        ('a_double', ctypes.c_char_p),
        ('a_tbyte', ctypes.c_char_p),
        ('a_packreal', ctypes.c_char_p),
        ('a_dups', ctypes.c_char_p),
        ('a_bss', ctypes.c_char_p),
        ('a_equ', ctypes.c_char_p),
        ('a_seg', ctypes.c_char_p),
        ('a_curip', ctypes.c_char_p),
        ('out_func_header', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_outctx_t), ctypes.POINTER(struct_func_t))),
        ('out_func_footer', ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_outctx_t), ctypes.POINTER(struct_func_t))),
        ('a_public', ctypes.c_char_p),
        ('a_weak', ctypes.c_char_p),
        ('a_extrn', ctypes.c_char_p),
        ('a_comdef', ctypes.c_char_p),
        ('get_type_name', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(struct__qstring_char_), ctypes.c_uint32, ctypes.c_uint64)),
        ('a_align', ctypes.c_char_p),
        ('lbrace', ctypes.c_char),
        ('rbrace', ctypes.c_char),
        ('PADDING_3', ctypes.c_ubyte * 6),
        ('a_mod', ctypes.c_char_p),
        ('a_band', ctypes.c_char_p),
        ('a_bor', ctypes.c_char_p),
        ('a_xor', ctypes.c_char_p),
        ('a_bnot', ctypes.c_char_p),
        ('a_shl', ctypes.c_char_p),
        ('a_shr', ctypes.c_char_p),
        ('a_sizeof_fmt', ctypes.c_char_p),
        ('flag2', ctypes.c_uint32),
        ('PADDING_4', ctypes.c_ubyte * 4),
        ('cmnt2', ctypes.c_char_p),
        ('low8', ctypes.c_char_p),
        ('high8', ctypes.c_char_p),
        ('low16', ctypes.c_char_p),
        ('high16', ctypes.c_char_p),
        ('a_include_fmt', ctypes.c_char_p),
        ('a_vstruc_fmt', ctypes.c_char_p),
        ('a_rva', ctypes.c_char_p),
        ('a_yword', ctypes.c_char_p),
        ('a_zword', ctypes.c_char_p),
    ]
    
    struct_bpt_t._pack_ = 1 # source:False
    struct_bpt_t._fields_ = [
        ('cb', ctypes.c_uint64),
        ('cndbody', qstring),
        ('loc', struct_bpt_location_t),
        ('pid', ctypes.c_int32),
        ('tid', ctypes.c_int32),
        ('ea', ctypes.c_uint64),
        ('type', ctypes.c_int32),
        ('pass_count', ctypes.c_int32),
        ('flags', ctypes.c_uint32),
        ('props', ctypes.c_uint32),
        ('size', ctypes.c_int32),
        ('cndidx', ctypes.c_int32),
        ('bptid', ctypes.c_uint64),
    ]
    
    class struct_cli_t(Structure):
        pass
    
    struct_cli_t._pack_ = 1 # source:False
    struct_cli_t._fields_ = [
        ('size', ctypes.c_uint64),
        ('flags', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('sname', ctypes.c_char_p),
        ('lname', ctypes.c_char_p),
        ('hint', ctypes.c_char_p),
        ('execute_line', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_char_p)),
        ('unused', ctypes.POINTER(None)),
        ('keydown', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct__qstring_char_), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32)),
        ('find_completions', ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_qvector__qstring_char__), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, ctypes.c_int32)),
    ]
    
    struct_kvp_t._pack_ = 1 # source:False
    struct_kvp_t._fields_ = [
        ('key', qstring),
        ('value', struct_jvalue_t),
    ]
    
    class struct_seh_t(Structure):
        pass
    
    struct_seh_t._pack_ = 1 # source:False
    struct_seh_t._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 40),
        ('filter', struct_rangevec_t),
        ('seh_code', ctypes.c_uint64),
    ]
    
    struct_til_t._pack_ = 1 # source:False
    struct_til_t._fields_ = [
        ('name', ctypes.c_char_p),
        ('desc', ctypes.c_char_p),
        ('nbases', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('base', ctypes.POINTER(ctypes.POINTER(struct_til_t))),
        ('flags', ctypes.c_uint32),
        ('cc', struct_compiler_info_t),
        ('PADDING_1', ctypes.c_ubyte * 2),
        ('syms', ctypes.POINTER(struct_til_bucket_t)),
        ('types', ctypes.POINTER(struct_til_bucket_t)),
        ('macros', ctypes.POINTER(struct_til_bucket_t)),
        ('nrefs', ctypes.c_int32),
        ('nstreams', ctypes.c_int32),
        ('streams', ctypes.POINTER(ctypes.POINTER(struct_til_stream_t))),
    ]
    
    std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___key_type = ctypes.c_uint64
    std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____ = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___key_type = ctypes.c_uint64
    std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____ = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Default_allocator_traits_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____size_type = ctypes.c_uint64
    std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P__ = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______ = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____ = ctypes.c_int64
    std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____ = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______ = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____ = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____size_type = ctypes.c_uint64
    std___Default_allocator_traits_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______size_type = ctypes.c_uint64
    std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P__ = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Default_allocator_traits_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long_____size_type = ctypes.c_uint64
    std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P__ = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____ = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____ = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___key_type = ctypes.c_int32
    std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___key_type = ctypes.c_uint64
    std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____size_type = ctypes.c_uint64
    std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____ = ctypes.c_int64
    std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____ = ctypes.POINTER(ctypes.c_int32)
    std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____size_type = ctypes.c_uint64
    std___Default_allocator_traits_std__allocator_std__pair_const_int__int_____size_type = ctypes.c_uint64
    std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_int__int___void__P__ = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tset_traits_int__std__less_int___std__allocator_int___false___value_type = ctypes.c_int32
    std___Tset_traits_int__std__less_int___std__allocator_int___false___key_type = ctypes.c_int32
    qvector_ida_syntax_highlighter_t__keywords_style_t___const_iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__keywords_style_t)
    qvector_ida_syntax_highlighter_t__plain_char_ptr_t___const_iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__plain_char_ptr_t)
    std___Default_allocator_traits_std__allocator_int____size_type = ctypes.c_uint64
    std___Rebind_pointer_t_void__P__std___Tree_node_int__void__P__ = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    qvector_ida_syntax_highlighter_t__keywords_style_t___iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__keywords_style_t)
    qvector_ida_syntax_highlighter_t__multicmt_t___const_iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__multicmt_t)
    qvector_ida_syntax_highlighter_t__plain_char_ptr_t___iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__plain_char_ptr_t)
    std__map_unsigned_long_long__unsigned_long_long___mapped_type = ctypes.c_uint64
    std__map_unsigned_long_long__unsigned_long_long___key_type = ctypes.c_uint64
    qvector_line_rendering_output_entry_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_line_rendering_output_entry_t))
    std___Simple_types_std__pair_const_int__int____size_type = ctypes.c_uint64
    qvector_ida_syntax_highlighter_t__multicmt_t___iterator = ctypes.POINTER(struct_ida_syntax_highlighter_t__multicmt_t)
    qvector_qvector_const_twinline_t__P____const_iterator = ctypes.POINTER(struct_qvector_const_twinline_t__P_)
    qvector_line_rendering_output_entry_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_line_rendering_output_entry_t))
    qvector_qrefcnt_t_source_item_t____const_iterator = ctypes.POINTER(struct_qrefcnt_t_source_item_t_)
    qvector__qstring_unsigned_char____const_iterator = ctypes.POINTER(struct__qstring_unsigned_char_)
    qvector_qvector_const_char__P____const_iterator = ctypes.POINTER(struct_qvector_const_char__P_)
    qvector_qvector_const_twinline_t__P____iterator = ctypes.POINTER(struct_qvector_const_twinline_t__P_)
    qvector_const_rangeset_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_rangeset_t))
    qvector_const_twinline_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_twinline_t))
    qvector_qrefcnt_t_source_item_t____iterator = ctypes.POINTER(struct_qrefcnt_t_source_item_t_)
    qvector_qvector_long_long____const_iterator = ctypes.POINTER(struct_qvector_long_long_)
    qvector_unsigned_long_long___const_iterator = ctypes.POINTER(ctypes.c_uint64)
    qvector__qstring_unsigned_char____iterator = ctypes.POINTER(struct__qstring_unsigned_char_)
    qvector__qstring_wchar_t____const_iterator = ctypes.POINTER(struct__qstring_wchar_t_)
    qvector_call_stack_info_t___const_iterator = ctypes.POINTER(struct_call_stack_info_t)
    qvector_compiled_binpat_t___const_iterator = ctypes.POINTER(struct_compiled_binpat_t)
    qvector_update_bpt_info_t___const_iterator = ctypes.POINTER(struct_update_bpt_info_t)
    class union_token_t___8299423771E115C2E8FEC5C7170C0424(Union):
        pass
    
    union_token_t___8299423771E115C2E8FEC5C7170C0424._pack_ = 1 # source:False
    union_token_t___8299423771E115C2E8FEC5C7170C0424._fields_ = [
        ('unicode', ctypes.c_char),
        ('is_unsigned', ctypes.c_char),
    ]
    
    qvector_dirtree_cursor_t___const_iterator = ctypes.POINTER(struct_dirtree_cursor_t)
    qvector_exception_info_t___const_iterator = ctypes.POINTER(struct_exception_info_t)
    qvector_qvector_const_char__P____iterator = ctypes.POINTER(struct_qvector_const_char__P_)
    qvector_scattered_segm_t___const_iterator = ctypes.POINTER(struct_scattered_segm_t)
    qvector_segm_move_info_t___const_iterator = ctypes.POINTER(struct_segm_move_info_t)
    qvector_selection_item_t___const_iterator = ctypes.POINTER(struct_selection_item_t)
    qvector_xreflist_entry_t___const_iterator = ctypes.POINTER(struct_xreflist_entry_t)
    std___Tree_node_int__void__P___value_type = ctypes.c_int32
    qvector_channel_redir_t___const_iterator = ctypes.POINTER(struct_channel_redir_t)
    qvector_lochist_entry_t___const_iterator = ctypes.POINTER(struct_lochist_entry_t)
    qvector_register_info_t___const_iterator = ctypes.POINTER(struct_register_info_t)
    qvector_tev_reg_value_t___const_iterator = ctypes.POINTER(struct_tev_reg_value_t)
    _qstring_unsigned_char___const_iterator = ctypes.POINTER(ctypes.c_ubyte)
    qvector__qstring_char____const_iterator = ctypes.POINTER(struct__qstring_char_)
    qvector_const_bpt_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_bpt_t))
    qvector_group_crinfo_t___const_iterator = ctypes.POINTER(struct_group_crinfo_t)
    qvector_process_info_t___const_iterator = ctypes.POINTER(struct_process_info_t)
    qvector_qbasic_block_t___const_iterator = ctypes.POINTER(struct_qbasic_block_t)
    qvector_refinfo_desc_t___const_iterator = ctypes.POINTER(struct_refinfo_desc_t)
    qvector_tev_info_reg_t___const_iterator = ctypes.POINTER(struct_tev_info_reg_t)
    qvector_const_char__P___const_iterator = ctypes.POINTER(ctypes.c_char_p)
    qvector_const_rangeset_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_rangeset_t))
    qvector_const_twinline_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_twinline_t))
    qvector_debug_event_t___const_iterator = ctypes.POINTER(struct_debug_event_t)
    qvector_enum_member_t___const_iterator = ctypes.POINTER(struct_enum_member_t)
    qvector_memory_info_t___const_iterator = ctypes.POINTER(struct_memory_info_t)
    qvector_memreg_info_t___const_iterator = ctypes.POINTER(struct_memreg_info_t)
    qvector_movbpt_info_t___const_iterator = ctypes.POINTER(struct_movbpt_info_t)
    qvector_snapshot_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_snapshot_t))
    qvector_sync_source_t___const_iterator = ctypes.POINTER(struct_sync_source_t)
    qvector_thread_name_t___const_iterator = ctypes.POINTER(struct_thread_name_t)
    qvector_unsigned_char___const_iterator = ctypes.POINTER(ctypes.c_ubyte)
    qvector_cfgopt_set_t___const_iterator = ctypes.POINTER(struct_cfgopt_set_t)
    qvector_extlang_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_extlang_t))
    qvector_fixup_info_t___const_iterator = ctypes.POINTER(struct_fixup_info_t)
    qvector_idc_global_t___const_iterator = ctypes.POINTER(struct_idc_global_t)
    qvector_ioport_bit_t___const_iterator = ctypes.POINTER(struct_ioport_bit_t)
    qvector_qvector_int____const_iterator = ctypes.POINTER(struct_qvector_int_)
    qvector_qvector_long_long____iterator = ctypes.POINTER(struct_qvector_long_long_)
    qvector_reg_access_t___const_iterator = ctypes.POINTER(struct_reg_access_t)
    qvector_simpleline_t___const_iterator = ctypes.POINTER(struct_simpleline_t)
    qvector_udt_member_t___const_iterator = ctypes.POINTER(struct_udt_member_t)
    qvector_unsigned_int___const_iterator = ctypes.POINTER(ctypes.c_uint32)
    qvector_unsigned_long_long___iterator = ctypes.POINTER(ctypes.c_uint64)
    qvector__qstring_wchar_t____iterator = ctypes.POINTER(struct__qstring_wchar_t_)
    qvector_call_stack_info_t___iterator = ctypes.POINTER(struct_call_stack_info_t)
    qvector_compiled_binpat_t___iterator = ctypes.POINTER(struct_compiled_binpat_t)
    qvector_simd_info_t___const_iterator = ctypes.POINTER(struct_simd_info_t)
    qvector_type_attr_t___const_iterator = ctypes.POINTER(struct_type_attr_t)
    qvector_update_bpt_info_t___iterator = ctypes.POINTER(struct_update_bpt_info_t)
    qvector_bptaddrs_t___const_iterator = ctypes.POINTER(struct_bptaddrs_t)
    qvector_direntry_t___const_iterator = ctypes.POINTER(struct_direntry_t)
    qvector_dirtree_cursor_t___iterator = ctypes.POINTER(struct_dirtree_cursor_t)
    qvector_exception_info_t___iterator = ctypes.POINTER(struct_exception_info_t)
    qvector_idp_desc_t___const_iterator = ctypes.POINTER(struct_idp_desc_t)
    qvector_idp_name_t___const_iterator = ctypes.POINTER(struct_idp_name_t)
    qvector_node_set_t___const_iterator = ctypes.POINTER(struct_node_set_t)
    qvector_rangeset_t___const_iterator = ctypes.POINTER(struct_rangeset_t)
    qvector_reg_info_t___const_iterator = ctypes.POINTER(struct_reg_info_t)
    qvector_row_info_t___const_iterator = ctypes.POINTER(struct_row_info_t)
    qvector_scattered_segm_t___iterator = ctypes.POINTER(struct_scattered_segm_t)
    qvector_segm_move_info_t___iterator = ctypes.POINTER(struct_segm_move_info_t)
    qvector_selection_item_t___iterator = ctypes.POINTER(struct_selection_item_t)
    qvector_tev_info_t___const_iterator = ctypes.POINTER(struct_tev_info_t)
    qvector_twinline_t___const_iterator = ctypes.POINTER(struct_twinline_t)
    qvector_xreflist_entry_t___iterator = ctypes.POINTER(struct_xreflist_entry_t)
    std___Simple_types_int___value_type = ctypes.c_int32
    qvector_argpart_t___const_iterator = ctypes.POINTER(struct_argpart_t)
    qvector_channel_redir_t___iterator = ctypes.POINTER(struct_channel_redir_t)
    qvector_ea_name_t___const_iterator = ctypes.POINTER(struct_ea_name_t)
    qvector_funcarg_t___const_iterator = ctypes.POINTER(struct_funcarg_t)
    qvector_lochist_entry_t___iterator = ctypes.POINTER(struct_lochist_entry_t)
    qvector_long_long___const_iterator = ctypes.POINTER(ctypes.c_int64)
    qvector_modinfo_t___const_iterator = ctypes.POINTER(struct_modinfo_t)
    qvector_register_info_t___iterator = ctypes.POINTER(struct_register_info_t)
    qvector_tev_reg_value_t___iterator = ctypes.POINTER(struct_tev_reg_value_t)
    std___Simple_types_int___size_type = ctypes.c_uint64
    _0425F8F1A3AE8F87FA89CDE6305293FE = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_locchange_md_t), ctypes.POINTER(None))
    _0F4B5B224EF598EAC96C9D985A235D75 = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.POINTER(None))
    _12B695DC843A94285F7310A143C8C434 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_insn_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32))
    _13DEA147606768949B8709A1F27A1AE6 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__iobuf))
    _223DCB884574D5DE586AD2D6B7376847 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.c_char_p)
    _2B5C0BD264F9291D6A7F6F791424403F = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t))
    _2C0E99206E7908236DCABCB2B91A8D4F = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char, ctypes.c_char)
    _47FFB0B1AABFAE006217B68E4FFCB4B3 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_locchange_md_t), ctypes.POINTER(None))
    _53B156155FBE7E40597743DACE3276C6 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None))
    _6748483DB9EEBDB64F2EA25B987191DF = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(struct_form_actions_t))
    
    # values for enumeration '_7014156F94AE1B7FC5F5E3560392A8C4'
    _7014156F94AE1B7FC5F5E3560392A8C4__enumvalues = {
        0: 'DTN_FULL_NAME',
        1: 'DTN_DISPLAY_NAME',
    }
    DTN_FULL_NAME = 0
    DTN_DISPLAY_NAME = 1
    _7014156F94AE1B7FC5F5E3560392A8C4 = ctypes.c_uint32 # enum
    _7148FF134A2561D170DBC235C372E12B = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p)
    _776C644986E1218BAA015F499D7289A7 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_place_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None))
    _79278B08C9A02D276B5400213E6E8772 = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_cfgopt_t), ctypes.c_int32, ctypes.POINTER(None))
    _7A67CD558302B3EA29FC91F77D84E941 = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.POINTER(struct_view_mouse_event_t), ctypes.POINTER(None))
    _7C51D3F4B871613F1BA7F83DBEBC3FD5 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))
    
    # values for enumeration '_94D4D585A38CDA12BD4A7F760DAFD340'
    _94D4D585A38CDA12BD4A7F760DAFD340__enumvalues = {
        0: 'JT_NONE',
        1: 'JT_SWITCH',
        2: 'JT_CALL',
    }
    JT_NONE = 0
    JT_SWITCH = 1
    JT_CALL = 2
    _94D4D585A38CDA12BD4A7F760DAFD340 = ctypes.c_uint32 # enum
    _9F642B09C10686E3843EA25A959506D5 = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(None))
    
    # values for enumeration '_A32948CF266C727D9CC1D79F2B35CC28'
    _A32948CF266C727D9CC1D79F2B35CC28__enumvalues = {
        1: 'QMOVE_CROSS_FS',
        2: 'QMOVE_OVERWRITE',
        4: 'QMOVE_OVR_RO',
    }
    QMOVE_CROSS_FS = 1
    QMOVE_OVERWRITE = 2
    QMOVE_OVR_RO = 4
    _A32948CF266C727D9CC1D79F2B35CC28 = ctypes.c_uint32 # enum
    _A6F93F8BAFF0D1A2AF75D768A5FCB062 = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(None))
    _AF4ED28A64411848F4EED41572FA4CE1 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.c_char_p, ctypes.c_int32, ctypes.c_char_p)
    _B4F266B0568ADA5794EA29B6B9D8A3FE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None))
    _B583FC0ED2D81EF34EE9B85011DA3455 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_place_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(None))
    
    # values for enumeration '_C7C212E52085C0E483DB7F2B4EDAB218'
    _C7C212E52085C0E483DB7F2B4EDAB218__enumvalues = {
        1: 'REG_ASSERT',
        2: 'REG_BADBR',
        3: 'REG_BADPAT',
        4: 'REG_BADRPT',
        5: 'REG_EBRACE',
        6: 'REG_EBRACK',
        7: 'REG_ECOLLATE',
        8: 'REG_ECTYPE',
        9: 'REG_EESCAPE',
        10: 'REG_EMPTY',
        11: 'REG_EPAREN',
        12: 'REG_ERANGE',
        13: 'REG_ESIZE',
        14: 'REG_ESPACE',
        15: 'REG_ESUBREG',
        16: 'REG_INVARG',
        17: 'REG_NOMATCH',
    }
    REG_ASSERT = 1
    REG_BADBR = 2
    REG_BADPAT = 3
    REG_BADRPT = 4
    REG_EBRACE = 5
    REG_EBRACK = 6
    REG_ECOLLATE = 7
    REG_ECTYPE = 8
    REG_EESCAPE = 9
    REG_EMPTY = 10
    REG_EPAREN = 11
    REG_ERANGE = 12
    REG_ESIZE = 13
    REG_ESPACE = 14
    REG_ESUBREG = 15
    REG_INVARG = 16
    REG_NOMATCH = 17
    _C7C212E52085C0E483DB7F2B4EDAB218 = ctypes.c_uint32 # enum
    _C9E14A82B8291B557AC92E2F5A452CE5 = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.POINTER(None), ctypes.c_char)
    _DB40683AED1FE27CD84662F2517C7BCC = ctypes.CFUNCTYPE(None, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_place_t), ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None))
    _EFB3D94CDC38BD29E337526787ABDBEA = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_linput_t), ctypes.POINTER(struct_impinfo_t))
    _F6359FE077454C49B917BFA4BFA37580 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.c_int32, ctypes.POINTER(None))
    _qstring_unsigned_char___iterator = ctypes.POINTER(ctypes.c_ubyte)
    _qstring_wchar_t___const_iterator = ctypes.POINTER(ctypes.c_int16)
    qvector__qstring_char____iterator = ctypes.POINTER(struct__qstring_char_)
    qvector_argloc_t___const_iterator = ctypes.POINTER(struct_argloc_t)
    qvector_bpt_t__P___const_iterator = ctypes.POINTER(ctypes.POINTER(struct_bpt_t))
    qvector_cliopt_t___const_iterator = ctypes.POINTER(struct_cliopt_t)
    qvector_const_bpt_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_bpt_t))
    qvector_group_crinfo_t___iterator = ctypes.POINTER(struct_group_crinfo_t)
    qvector_intmap_t___const_iterator = ctypes.POINTER(struct_intmap_t)
    qvector_ioport_t___const_iterator = ctypes.POINTER(struct_ioport_t)
    qvector_jvalue_t___const_iterator = ctypes.POINTER(struct_jvalue_t)
    qvector_lowcnd_t___const_iterator = ctypes.POINTER(struct_lowcnd_t)
    qvector_process_info_t___iterator = ctypes.POINTER(struct_process_info_t)
    qvector_qbasic_block_t___iterator = ctypes.POINTER(struct_qbasic_block_t)
    qvector_refinfo_desc_t___iterator = ctypes.POINTER(struct_refinfo_desc_t)
    qvector_regobj_t___const_iterator = ctypes.POINTER(struct_regobj_t)
    qvector_regval_t___const_iterator = ctypes.POINTER(struct_regval_t)
    qvector_stkpnt_t___const_iterator = ctypes.POINTER(struct_stkpnt_t)
    qvector_tev_info_reg_t___iterator = ctypes.POINTER(struct_tev_info_reg_t)
    qvector_tryblk_t___const_iterator = ctypes.POINTER(struct_tryblk_t)
    qvector_valstr_t___const_iterator = ctypes.POINTER(struct_valstr_t)
    qvector_catch_t___const_iterator = ctypes.POINTER(struct_catch_t)
    qvector_const_char__P___iterator = ctypes.POINTER(ctypes.c_char_p)
    qvector_debug_event_t___iterator = ctypes.POINTER(struct_debug_event_t)
    qvector_enum_member_t___iterator = ctypes.POINTER(struct_enum_member_t)
    qvector_memory_info_t___iterator = ctypes.POINTER(struct_memory_info_t)
    qvector_memreg_info_t___iterator = ctypes.POINTER(struct_memreg_info_t)
    qvector_movbpt_info_t___iterator = ctypes.POINTER(struct_movbpt_info_t)
    qvector_point_t___const_iterator = ctypes.POINTER(struct_point_t)
    qvector_range_t___const_iterator = ctypes.POINTER(struct_range_t)
    qvector_snapshot_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_snapshot_t))
    qvector_sync_source_t___iterator = ctypes.POINTER(struct_sync_source_t)
    qvector_thread_name_t___iterator = ctypes.POINTER(struct_thread_name_t)
    qvector_tinfo_t___const_iterator = ctypes.POINTER(struct_tinfo_t)
    qvector_token_t___const_iterator = ctypes.POINTER(struct_token_t)
    qvector_unsigned_char___iterator = ctypes.POINTER(ctypes.c_ubyte)
    qvector_wchar_t___const_iterator = ctypes.POINTER(ctypes.c_int16)
    qvector_cfgopt_set_t___iterator = ctypes.POINTER(struct_cfgopt_set_t)
    qvector_edge_t___const_iterator = ctypes.POINTER(struct_edge_t)
    qvector_extlang_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_extlang_t))
    qvector_fixup_info_t___iterator = ctypes.POINTER(struct_fixup_info_t)
    qvector_idc_global_t___iterator = ctypes.POINTER(struct_idc_global_t)
    qvector_ioport_bit_t___iterator = ctypes.POINTER(struct_ioport_bit_t)
    qvector_qvector_int____iterator = ctypes.POINTER(struct_qvector_int_)
    qvector_rect_t___const_iterator = ctypes.POINTER(struct_rect_t)
    qvector_reg_access_t___iterator = ctypes.POINTER(struct_reg_access_t)
    qvector_simpleline_t___iterator = ctypes.POINTER(struct_simpleline_t)
    qvector_udt_member_t___iterator = ctypes.POINTER(struct_udt_member_t)
    qvector_unsigned_int___iterator = ctypes.POINTER(ctypes.c_uint32)
    std__map_int__int___mapped_type = ctypes.c_int32
    _qstring_char___const_iterator = ctypes.c_char_p
    qvector_bpt_t___const_iterator = ctypes.POINTER(struct_bpt_t)
    qvector_kvp_t___const_iterator = ctypes.POINTER(struct_kvp_t)
    qvector_simd_info_t___iterator = ctypes.POINTER(struct_simd_info_t)
    qvector_type_attr_t___iterator = ctypes.POINTER(struct_type_attr_t)
    qvector_bool___const_iterator = ctypes.c_char_p
    qvector_bptaddrs_t___iterator = ctypes.POINTER(struct_bptaddrs_t)
    qvector_char___const_iterator = ctypes.c_char_p
    qvector_direntry_t___iterator = ctypes.POINTER(struct_direntry_t)
    qvector_idp_desc_t___iterator = ctypes.POINTER(struct_idp_desc_t)
    qvector_idp_name_t___iterator = ctypes.POINTER(struct_idp_name_t)
    qvector_node_set_t___iterator = ctypes.POINTER(struct_node_set_t)
    qvector_op_t___const_iterator = ctypes.POINTER(struct_op_t)
    qvector_rangeset_t___iterator = ctypes.POINTER(struct_rangeset_t)
    qvector_reg_info_t___iterator = ctypes.POINTER(struct_reg_info_t)
    qvector_row_info_t___iterator = ctypes.POINTER(struct_row_info_t)
    qvector_tev_info_t___iterator = ctypes.POINTER(struct_tev_info_t)
    qvector_twinline_t___iterator = ctypes.POINTER(struct_twinline_t)
    
    # values for enumeration 'hexplace_gen_t__int_format_t'
    hexplace_gen_t__int_format_t__enumvalues = {
        0: 'if_hex',
        1: 'if_signed',
        2: 'if_unsigned',
    }
    if_hex = 0
    if_signed = 1
    if_unsigned = 2
    hexplace_gen_t__int_format_t = ctypes.c_uint32 # enum
    qvector_argpart_t___iterator = ctypes.POINTER(struct_argpart_t)
    qvector_ea_name_t___iterator = ctypes.POINTER(struct_ea_name_t)
    qvector_funcarg_t___iterator = ctypes.POINTER(struct_funcarg_t)
    qvector_int___const_iterator = ctypes.POINTER(ctypes.c_int32)
    qvector_long_long___iterator = ctypes.POINTER(ctypes.c_int64)
    qvector_modinfo_t___iterator = ctypes.POINTER(struct_modinfo_t)
    std__map_int__int___key_type = ctypes.c_int32
    _qstring_wchar_t___iterator = ctypes.POINTER(ctypes.c_int16)
    
    # values for enumeration 'hexplace_gen_t__byte_kind_t'
    hexplace_gen_t__byte_kind_t__enumvalues = {
        0: 'BK_VALID',
        1: 'BK_INVALIDADDR',
        2: 'BK_NOVALUE',
    }
    BK_VALID = 0
    BK_INVALIDADDR = 1
    BK_NOVALUE = 2
    hexplace_gen_t__byte_kind_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'hexplace_gen_t__data_kind_t'
    hexplace_gen_t__data_kind_t__enumvalues = {
        0: 'dk_float',
        1: 'dk_int',
        2: 'dk_addr_names',
        3: 'dk_addr_text',
    }
    dk_float = 0
    dk_int = 1
    dk_addr_names = 2
    dk_addr_text = 3
    hexplace_gen_t__data_kind_t = ctypes.c_uint32 # enum
    qvector_argloc_t___iterator = ctypes.POINTER(struct_argloc_t)
    qvector_bpt_t__P___iterator = ctypes.POINTER(ctypes.POINTER(struct_bpt_t))
    qvector_cliopt_t___iterator = ctypes.POINTER(struct_cliopt_t)
    qvector_intmap_t___iterator = ctypes.POINTER(struct_intmap_t)
    qvector_ioport_t___iterator = ctypes.POINTER(struct_ioport_t)
    qvector_jvalue_t___iterator = ctypes.POINTER(struct_jvalue_t)
    qvector_lowcnd_t___iterator = ctypes.POINTER(struct_lowcnd_t)
    qvector_regobj_t___iterator = ctypes.POINTER(struct_regobj_t)
    qvector_regval_t___iterator = ctypes.POINTER(struct_regval_t)
    qvector_stkpnt_t___iterator = ctypes.POINTER(struct_stkpnt_t)
    qvector_tryblk_t___iterator = ctypes.POINTER(struct_tryblk_t)
    qvector_valstr_t___iterator = ctypes.POINTER(struct_valstr_t)
    cliopts_t__usage_printer_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p)
    
    # values for enumeration 'custom_viewer_handler_id_t'
    custom_viewer_handler_id_t__enumvalues = {
        0: 'CVH_USERDATA',
        1: 'CVH_KEYDOWN',
        2: 'CVH_POPUP',
        3: 'CVH_DBLCLICK',
        4: 'CVH_CURPOS',
        5: 'CVH_CLOSE',
        6: 'CVH_CLICK',
        7: 'CVH_QT_AWARE',
        8: 'CVH_HELP',
        9: 'CVH_MOUSEMOVE',
        1000: 'CDVH_USERDATA',
        1001: 'CDVH_SRCVIEW',
        1002: 'CDVH_LINES_CLICK',
        1003: 'CDVH_LINES_DBLCLICK',
        1004: 'CDVH_LINES_POPUP',
        1005: 'CDVH_LINES_DRAWICON',
        1006: 'CDVH_LINES_LINENUM',
        1007: 'CDVH_LINES_ICONMARGIN',
        1008: 'CDVH_LINES_RADIX',
        1009: 'CDVH_LINES_ALIGNMENT',
    }
    CVH_USERDATA = 0
    CVH_KEYDOWN = 1
    CVH_POPUP = 2
    CVH_DBLCLICK = 3
    CVH_CURPOS = 4
    CVH_CLOSE = 5
    CVH_CLICK = 6
    CVH_QT_AWARE = 7
    CVH_HELP = 8
    CVH_MOUSEMOVE = 9
    CDVH_USERDATA = 1000
    CDVH_SRCVIEW = 1001
    CDVH_LINES_CLICK = 1002
    CDVH_LINES_DBLCLICK = 1003
    CDVH_LINES_POPUP = 1004
    CDVH_LINES_DRAWICON = 1005
    CDVH_LINES_LINENUM = 1006
    CDVH_LINES_ICONMARGIN = 1007
    CDVH_LINES_RADIX = 1008
    CDVH_LINES_ALIGNMENT = 1009
    custom_viewer_handler_id_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'encoder_t__notify_recerr_t'
    encoder_t__notify_recerr_t__enumvalues = {
        0: 'nr_none',
        1: 'nr_once',
    }
    nr_none = 0
    nr_once = 1
    encoder_t__notify_recerr_t = ctypes.c_uint32 # enum
    qvector_catch_t___iterator = ctypes.POINTER(struct_catch_t)
    qvector_point_t___iterator = ctypes.POINTER(struct_point_t)
    qvector_range_t___iterator = ctypes.POINTER(struct_range_t)
    qvector_tinfo_t___iterator = ctypes.POINTER(struct_tinfo_t)
    qvector_token_t___iterator = ctypes.POINTER(struct_token_t)
    qvector_wchar_t___iterator = ctypes.POINTER(ctypes.c_int16)
    qvector_edge_t___iterator = ctypes.POINTER(struct_edge_t)
    qvector_rect_t___iterator = ctypes.POINTER(struct_rect_t)
    _qstring_char___iterator = ctypes.c_char_p
    
    # values for enumeration 'form_actions_t__dlgbtn_t'
    form_actions_t__dlgbtn_t__enumvalues = {
        0: 'dbt_yes',
        1: 'dbt_cancel',
        2: 'dbt_no',
    }
    dbt_yes = 0
    dbt_cancel = 1
    dbt_no = 2
    form_actions_t__dlgbtn_t = ctypes.c_uint32 # enum
    qvector_bpt_t___iterator = ctypes.POINTER(struct_bpt_t)
    qvector_kvp_t___iterator = ctypes.POINTER(struct_kvp_t)
    
    # values for enumeration 'idb_event__event_code_t'
    idb_event__event_code_t__enumvalues = {
        0: 'closebase',
        1: 'savebase',
        2: 'upgraded',
        3: 'auto_empty',
        4: 'auto_empty_finally',
        5: 'determined_main',
        6: 'local_types_changed',
        7: 'extlang_changed',
        8: 'idasgn_loaded',
        9: 'kernel_config_loaded',
        10: 'loader_finished',
        11: 'flow_chart_created',
        12: 'compiler_changed',
        13: 'changing_ti',
        14: 'ti_changed',
        15: 'changing_op_ti',
        16: 'op_ti_changed',
        17: 'changing_op_type',
        18: 'op_type_changed',
        19: 'enum_created',
        20: 'deleting_enum',
        21: 'enum_deleted',
        22: 'renaming_enum',
        23: 'enum_renamed',
        24: 'changing_enum_bf',
        25: 'enum_bf_changed',
        26: 'changing_enum_cmt',
        27: 'enum_cmt_changed',
        28: 'enum_member_created',
        29: 'deleting_enum_member',
        30: 'enum_member_deleted',
        31: 'struc_created',
        32: 'deleting_struc',
        33: 'struc_deleted',
        34: 'changing_struc_align',
        35: 'struc_align_changed',
        36: 'renaming_struc',
        37: 'struc_renamed',
        38: 'expanding_struc',
        39: 'struc_expanded',
        40: 'struc_member_created',
        41: 'deleting_struc_member',
        42: 'struc_member_deleted',
        43: 'renaming_struc_member',
        44: 'struc_member_renamed',
        45: 'changing_struc_member',
        46: 'struc_member_changed',
        47: 'changing_struc_cmt',
        48: 'struc_cmt_changed',
        49: 'segm_added',
        50: 'deleting_segm',
        51: 'segm_deleted',
        52: 'changing_segm_start',
        53: 'segm_start_changed',
        54: 'changing_segm_end',
        55: 'segm_end_changed',
        56: 'changing_segm_name',
        57: 'segm_name_changed',
        58: 'changing_segm_class',
        59: 'segm_class_changed',
        60: 'segm_attrs_updated',
        61: 'segm_moved',
        62: 'allsegs_moved',
        63: 'func_added',
        64: 'func_updated',
        65: 'set_func_start',
        66: 'set_func_end',
        67: 'deleting_func',
        68: 'frame_deleted',
        69: 'thunk_func_created',
        70: 'func_tail_appended',
        71: 'deleting_func_tail',
        72: 'func_tail_deleted',
        73: 'tail_owner_changed',
        74: 'func_noret_changed',
        75: 'stkpnts_changed',
        76: 'updating_tryblks',
        77: 'tryblks_updated',
        78: 'deleting_tryblks',
        79: 'sgr_changed',
        80: 'make_code',
        81: 'make_data',
        82: 'destroyed_items',
        83: 'renamed',
        84: 'byte_patched',
        85: 'changing_cmt',
        86: 'cmt_changed',
        87: 'changing_range_cmt',
        88: 'range_cmt_changed',
        89: 'extra_cmt_changed',
        90: 'item_color_changed',
        91: 'callee_addr_changed',
        92: 'bookmark_changed',
        93: 'sgr_deleted',
        94: 'adding_segm',
        95: 'func_deleted',
        96: 'dirtree_mkdir',
        97: 'dirtree_rmdir',
        98: 'dirtree_link',
        99: 'dirtree_move',
        100: 'dirtree_rank',
        101: 'dirtree_rminode',
        102: 'dirtree_segm_moved',
        103: 'enum_width_changed',
        104: 'enum_flag_changed',
        105: 'enum_ordinal_changed',
    }
    closebase = 0
    savebase = 1
    upgraded = 2
    auto_empty = 3
    auto_empty_finally = 4
    determined_main = 5
    local_types_changed = 6
    extlang_changed = 7
    idasgn_loaded = 8
    kernel_config_loaded = 9
    loader_finished = 10
    flow_chart_created = 11
    compiler_changed = 12
    changing_ti = 13
    ti_changed = 14
    changing_op_ti = 15
    op_ti_changed = 16
    changing_op_type = 17
    op_type_changed = 18
    enum_created = 19
    deleting_enum = 20
    enum_deleted = 21
    renaming_enum = 22
    enum_renamed = 23
    changing_enum_bf = 24
    enum_bf_changed = 25
    changing_enum_cmt = 26
    enum_cmt_changed = 27
    enum_member_created = 28
    deleting_enum_member = 29
    enum_member_deleted = 30
    struc_created = 31
    deleting_struc = 32
    struc_deleted = 33
    changing_struc_align = 34
    struc_align_changed = 35
    renaming_struc = 36
    struc_renamed = 37
    expanding_struc = 38
    struc_expanded = 39
    struc_member_created = 40
    deleting_struc_member = 41
    struc_member_deleted = 42
    renaming_struc_member = 43
    struc_member_renamed = 44
    changing_struc_member = 45
    struc_member_changed = 46
    changing_struc_cmt = 47
    struc_cmt_changed = 48
    segm_added = 49
    deleting_segm = 50
    segm_deleted = 51
    changing_segm_start = 52
    segm_start_changed = 53
    changing_segm_end = 54
    segm_end_changed = 55
    changing_segm_name = 56
    segm_name_changed = 57
    changing_segm_class = 58
    segm_class_changed = 59
    segm_attrs_updated = 60
    segm_moved = 61
    allsegs_moved = 62
    func_added = 63
    func_updated = 64
    set_func_start = 65
    set_func_end = 66
    deleting_func = 67
    frame_deleted = 68
    thunk_func_created = 69
    func_tail_appended = 70
    deleting_func_tail = 71
    func_tail_deleted = 72
    tail_owner_changed = 73
    func_noret_changed = 74
    stkpnts_changed = 75
    updating_tryblks = 76
    tryblks_updated = 77
    deleting_tryblks = 78
    sgr_changed = 79
    make_code = 80
    make_data = 81
    destroyed_items = 82
    renamed = 83
    byte_patched = 84
    changing_cmt = 85
    cmt_changed = 86
    changing_range_cmt = 87
    range_cmt_changed = 88
    extra_cmt_changed = 89
    item_color_changed = 90
    callee_addr_changed = 91
    bookmark_changed = 92
    sgr_deleted = 93
    adding_segm = 94
    func_deleted = 95
    dirtree_mkdir = 96
    dirtree_rmdir = 97
    dirtree_link = 98
    dirtree_move = 99
    dirtree_rank = 100
    dirtree_rminode = 101
    dirtree_segm_moved = 102
    enum_width_changed = 103
    enum_flag_changed = 104
    enum_ordinal_changed = 105
    idb_event__event_code_t = ctypes.c_uint32 # enum
    input_event_modifiers_t = ctypes.c_int32
    qvector_bool___iterator = ctypes.c_char_p
    qvector_char___iterator = ctypes.c_char_p
    qvector_op_t___iterator = ctypes.POINTER(struct_op_t)
    qvector_int___iterator = ctypes.POINTER(ctypes.c_int32)
    cliopt_poly_handler_t = ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(None))
    
    # values for enumeration 'graph_notification_t'
    graph_notification_t__enumvalues = {
        0: 'grcode_calculating_layout',
        1: 'grcode_layout_calculated',
        2: 'grcode_changed_graph',
        3: 'grcode_reserved',
        4: 'grcode_clicked',
        5: 'grcode_dblclicked',
        6: 'grcode_creating_group',
        7: 'grcode_deleting_group',
        8: 'grcode_group_visibility',
        9: 'grcode_gotfocus',
        10: 'grcode_lostfocus',
        11: 'grcode_user_refresh',
        12: 'grcode_reserved2',
        13: 'grcode_user_text',
        14: 'grcode_user_size',
        15: 'grcode_user_title',
        16: 'grcode_user_draw',
        17: 'grcode_user_hint',
        18: 'grcode_destroyed',
        256: 'grcode_create_graph_viewer',
        257: 'grcode_get_graph_viewer',
        258: 'grcode_get_viewer_graph',
        259: 'grcode_create_mutable_graph',
        260: 'grcode_set_viewer_graph',
        261: 'grcode_refresh_viewer',
        262: 'grcode_fit_window',
        263: 'grcode_get_curnode',
        264: 'grcode_center_on',
        265: 'grcode_get_selection',
        266: 'grcode_del_custom_layout',
        267: 'grcode_set_custom_layout',
        268: 'grcode_set_graph_groups',
        269: 'grcode_clear',
        270: 'grcode_create_digraph_layout',
        271: 'grcode_create_tree_layout',
        272: 'grcode_create_circle_layout',
        273: 'grcode_get_node_representative',
        274: 'grcode_find_subgraph_node',
        275: 'grcode_create_group',
        276: 'grcode_get_custom_layout',
        277: 'grcode_get_graph_groups',
        278: 'grcode_empty',
        279: 'grcode_is_visible_node',
        280: 'grcode_delete_group',
        281: 'grcode_change_group_visibility',
        282: 'grcode_set_edge',
        283: 'grcode_node_qty',
        284: 'grcode_nrect',
        285: 'grcode_set_titlebar_height',
        286: 'grcode_create_user_graph_place',
        287: 'grcode_create_disasm_graph1',
        288: 'grcode_create_disasm_graph2',
        289: 'grcode_set_node_info',
        290: 'grcode_get_node_info',
        291: 'grcode_del_node_info',
        292: 'grcode_viewer_create_groups',
        293: 'grcode_viewer_delete_groups',
        294: 'grcode_viewer_groups_visibility',
        295: 'grcode_viewer_create_groups_vec',
        296: 'grcode_viewer_delete_groups_vec',
        297: 'grcode_viewer_groups_visibility_vec',
        298: 'grcode_delete_mutable_graph',
        299: 'grcode_edge_infos_wrapper_copy',
        300: 'grcode_edge_infos_wrapper_clear',
        301: 'grcode_attach_menu_item',
        302: 'grcode_set_gli',
        303: 'grcode_get_gli',
    }
    grcode_calculating_layout = 0
    grcode_layout_calculated = 1
    grcode_changed_graph = 2
    grcode_reserved = 3
    grcode_clicked = 4
    grcode_dblclicked = 5
    grcode_creating_group = 6
    grcode_deleting_group = 7
    grcode_group_visibility = 8
    grcode_gotfocus = 9
    grcode_lostfocus = 10
    grcode_user_refresh = 11
    grcode_reserved2 = 12
    grcode_user_text = 13
    grcode_user_size = 14
    grcode_user_title = 15
    grcode_user_draw = 16
    grcode_user_hint = 17
    grcode_destroyed = 18
    grcode_create_graph_viewer = 256
    grcode_get_graph_viewer = 257
    grcode_get_viewer_graph = 258
    grcode_create_mutable_graph = 259
    grcode_set_viewer_graph = 260
    grcode_refresh_viewer = 261
    grcode_fit_window = 262
    grcode_get_curnode = 263
    grcode_center_on = 264
    grcode_get_selection = 265
    grcode_del_custom_layout = 266
    grcode_set_custom_layout = 267
    grcode_set_graph_groups = 268
    grcode_clear = 269
    grcode_create_digraph_layout = 270
    grcode_create_tree_layout = 271
    grcode_create_circle_layout = 272
    grcode_get_node_representative = 273
    grcode_find_subgraph_node = 274
    grcode_create_group = 275
    grcode_get_custom_layout = 276
    grcode_get_graph_groups = 277
    grcode_empty = 278
    grcode_is_visible_node = 279
    grcode_delete_group = 280
    grcode_change_group_visibility = 281
    grcode_set_edge = 282
    grcode_node_qty = 283
    grcode_nrect = 284
    grcode_set_titlebar_height = 285
    grcode_create_user_graph_place = 286
    grcode_create_disasm_graph1 = 287
    grcode_create_disasm_graph2 = 288
    grcode_set_node_info = 289
    grcode_get_node_info = 290
    grcode_del_node_info = 291
    grcode_viewer_create_groups = 292
    grcode_viewer_delete_groups = 293
    grcode_viewer_groups_visibility = 294
    grcode_viewer_create_groups_vec = 295
    grcode_viewer_delete_groups_vec = 296
    grcode_viewer_groups_visibility_vec = 297
    grcode_delete_mutable_graph = 298
    grcode_edge_infos_wrapper_copy = 299
    grcode_edge_infos_wrapper_clear = 300
    grcode_attach_menu_item = 301
    grcode_set_gli = 302
    grcode_get_gli = 303
    graph_notification_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'processor_t__event_t'
    processor_t__event_t__enumvalues = {
        0: 'ev_init',
        1: 'ev_term',
        2: 'ev_newprc',
        3: 'ev_newasm',
        4: 'ev_newfile',
        5: 'ev_oldfile',
        6: 'ev_newbinary',
        7: 'ev_endbinary',
        8: 'ev_set_idp_options',
        9: 'ev_set_proc_options',
        10: 'ev_ana_insn',
        11: 'ev_emu_insn',
        12: 'ev_out_header',
        13: 'ev_out_footer',
        14: 'ev_out_segstart',
        15: 'ev_out_segend',
        16: 'ev_out_assumes',
        17: 'ev_out_insn',
        18: 'ev_out_mnem',
        19: 'ev_out_operand',
        20: 'ev_out_data',
        21: 'ev_out_label',
        22: 'ev_out_special_item',
        23: 'ev_gen_stkvar_def',
        24: 'ev_gen_regvar_def',
        25: 'ev_gen_src_file_lnnum',
        26: 'ev_creating_segm',
        27: 'ev_moving_segm',
        28: 'ev_coagulate',
        29: 'ev_undefine',
        30: 'ev_treat_hindering_item',
        31: 'ev_rename',
        32: 'ev_is_far_jump',
        33: 'ev_is_sane_insn',
        34: 'ev_is_cond_insn',
        35: 'ev_is_call_insn',
        36: 'ev_is_ret_insn',
        37: 'ev_may_be_func',
        38: 'ev_is_basic_block_end',
        39: 'ev_is_indirect_jump',
        40: 'ev_is_insn_table_jump',
        41: 'ev_is_switch',
        42: 'ev_calc_switch_cases',
        43: 'ev_create_switch_xrefs',
        44: 'ev_is_align_insn',
        45: 'ev_is_alloca_probe',
        46: 'ev_delay_slot_insn',
        47: 'ev_is_sp_based',
        48: 'ev_can_have_type',
        49: 'ev_cmp_operands',
        50: 'ev_adjust_refinfo',
        51: 'ev_get_operand_string',
        52: 'ev_get_reg_name',
        53: 'ev_str2reg',
        54: 'ev_get_autocmt',
        55: 'ev_get_bg_color',
        56: 'ev_is_jump_func',
        57: 'ev_func_bounds',
        58: 'ev_verify_sp',
        59: 'ev_verify_noreturn',
        60: 'ev_create_func_frame',
        61: 'ev_get_frame_retsize',
        62: 'ev_get_stkvar_scale_factor',
        63: 'ev_demangle_name',
        64: 'ev_add_cref',
        65: 'ev_add_dref',
        66: 'ev_del_cref',
        67: 'ev_del_dref',
        68: 'ev_coagulate_dref',
        69: 'ev_may_show_sreg',
        70: 'ev_loader_elf_machine',
        71: 'ev_auto_queue_empty',
        72: 'ev_validate_flirt_func',
        73: 'ev_adjust_libfunc_ea',
        74: 'ev_assemble',
        75: 'ev_extract_address',
        76: 'ev_realcvt',
        77: 'ev_gen_asm_or_lst',
        78: 'ev_gen_map_file',
        79: 'ev_create_flat_group',
        80: 'ev_getreg',
        81: 'ev_analyze_prolog',
        82: 'ev_calc_spdelta',
        83: 'ev_calcrel',
        84: 'ev_find_reg_value',
        85: 'ev_find_op_value',
        86: 'ev_replaying_undo',
        87: 'ev_ending_undo',
        88: 'ev_set_code16_mode',
        89: 'ev_get_code16_mode',
        90: 'ev_get_procmod',
        91: 'ev_asm_installed',
        92: 'ev_get_reg_accesses',
        93: 'ev_is_control_flow_guard',
        94: 'ev_broadcast',
        95: 'ev_create_merge_handlers',
        96: 'ev_privrange_changed',
        97: 'ev_last_cb_before_debugger',
        1000: 'ev_next_exec_insn',
        1001: 'ev_calc_step_over',
        1002: 'ev_calc_next_eas',
        1003: 'ev_get_macro_insn_head',
        1004: 'ev_get_dbr_opnum',
        1005: 'ev_insn_reads_tbit',
        1006: 'ev_clean_tbit',
        1007: 'ev_get_idd_opinfo',
        1008: 'ev_get_reg_info',
        1009: 'ev_update_call_stack',
        1010: 'ev_last_cb_before_type_callbacks',
        2000: 'ev_setup_til',
        2001: 'ev_get_abi_info',
        2002: 'ev_max_ptr_size',
        2003: 'ev_get_default_enum_size',
        2004: 'ev_get_cc_regs',
        2005: 'ev_obsolete1',
        2006: 'ev_obsolete2',
        2007: 'ev_get_simd_types',
        2008: 'ev_calc_cdecl_purged_bytes',
        2009: 'ev_calc_purged_bytes',
        2010: 'ev_calc_retloc',
        2011: 'ev_calc_arglocs',
        2012: 'ev_calc_varglocs',
        2013: 'ev_adjust_argloc',
        2014: 'ev_lower_func_type',
        2015: 'ev_equal_reglocs',
        2016: 'ev_use_stkarg_type',
        2017: 'ev_use_regarg_type',
        2018: 'ev_use_arg_types',
        2019: 'ev_arg_addrs_ready',
        2020: 'ev_decorate_name',
        2021: 'ev_arch_changed',
        2022: 'ev_get_stkarg_area_info',
        2023: 'ev_last_cb_before_loader',
        3000: 'ev_loader',
    }
    ev_init = 0
    ev_term = 1
    ev_newprc = 2
    ev_newasm = 3
    ev_newfile = 4
    ev_oldfile = 5
    ev_newbinary = 6
    ev_endbinary = 7
    ev_set_idp_options = 8
    ev_set_proc_options = 9
    ev_ana_insn = 10
    ev_emu_insn = 11
    ev_out_header = 12
    ev_out_footer = 13
    ev_out_segstart = 14
    ev_out_segend = 15
    ev_out_assumes = 16
    ev_out_insn = 17
    ev_out_mnem = 18
    ev_out_operand = 19
    ev_out_data = 20
    ev_out_label = 21
    ev_out_special_item = 22
    ev_gen_stkvar_def = 23
    ev_gen_regvar_def = 24
    ev_gen_src_file_lnnum = 25
    ev_creating_segm = 26
    ev_moving_segm = 27
    ev_coagulate = 28
    ev_undefine = 29
    ev_treat_hindering_item = 30
    ev_rename = 31
    ev_is_far_jump = 32
    ev_is_sane_insn = 33
    ev_is_cond_insn = 34
    ev_is_call_insn = 35
    ev_is_ret_insn = 36
    ev_may_be_func = 37
    ev_is_basic_block_end = 38
    ev_is_indirect_jump = 39
    ev_is_insn_table_jump = 40
    ev_is_switch = 41
    ev_calc_switch_cases = 42
    ev_create_switch_xrefs = 43
    ev_is_align_insn = 44
    ev_is_alloca_probe = 45
    ev_delay_slot_insn = 46
    ev_is_sp_based = 47
    ev_can_have_type = 48
    ev_cmp_operands = 49
    ev_adjust_refinfo = 50
    ev_get_operand_string = 51
    ev_get_reg_name = 52
    ev_str2reg = 53
    ev_get_autocmt = 54
    ev_get_bg_color = 55
    ev_is_jump_func = 56
    ev_func_bounds = 57
    ev_verify_sp = 58
    ev_verify_noreturn = 59
    ev_create_func_frame = 60
    ev_get_frame_retsize = 61
    ev_get_stkvar_scale_factor = 62
    ev_demangle_name = 63
    ev_add_cref = 64
    ev_add_dref = 65
    ev_del_cref = 66
    ev_del_dref = 67
    ev_coagulate_dref = 68
    ev_may_show_sreg = 69
    ev_loader_elf_machine = 70
    ev_auto_queue_empty = 71
    ev_validate_flirt_func = 72
    ev_adjust_libfunc_ea = 73
    ev_assemble = 74
    ev_extract_address = 75
    ev_realcvt = 76
    ev_gen_asm_or_lst = 77
    ev_gen_map_file = 78
    ev_create_flat_group = 79
    ev_getreg = 80
    ev_analyze_prolog = 81
    ev_calc_spdelta = 82
    ev_calcrel = 83
    ev_find_reg_value = 84
    ev_find_op_value = 85
    ev_replaying_undo = 86
    ev_ending_undo = 87
    ev_set_code16_mode = 88
    ev_get_code16_mode = 89
    ev_get_procmod = 90
    ev_asm_installed = 91
    ev_get_reg_accesses = 92
    ev_is_control_flow_guard = 93
    ev_broadcast = 94
    ev_create_merge_handlers = 95
    ev_privrange_changed = 96
    ev_last_cb_before_debugger = 97
    ev_next_exec_insn = 1000
    ev_calc_step_over = 1001
    ev_calc_next_eas = 1002
    ev_get_macro_insn_head = 1003
    ev_get_dbr_opnum = 1004
    ev_insn_reads_tbit = 1005
    ev_clean_tbit = 1006
    ev_get_idd_opinfo = 1007
    ev_get_reg_info = 1008
    ev_update_call_stack = 1009
    ev_last_cb_before_type_callbacks = 1010
    ev_setup_til = 2000
    ev_get_abi_info = 2001
    ev_max_ptr_size = 2002
    ev_get_default_enum_size = 2003
    ev_get_cc_regs = 2004
    ev_obsolete1 = 2005
    ev_obsolete2 = 2006
    ev_get_simd_types = 2007
    ev_calc_cdecl_purged_bytes = 2008
    ev_calc_purged_bytes = 2009
    ev_calc_retloc = 2010
    ev_calc_arglocs = 2011
    ev_calc_varglocs = 2012
    ev_adjust_argloc = 2013
    ev_lower_func_type = 2014
    ev_equal_reglocs = 2015
    ev_use_stkarg_type = 2016
    ev_use_regarg_type = 2017
    ev_use_arg_types = 2018
    ev_arg_addrs_ready = 2019
    ev_decorate_name = 2020
    ev_arch_changed = 2021
    ev_get_stkarg_area_info = 2022
    ev_last_cb_before_loader = 2023
    ev_loader = 3000
    processor_t__event_t = ctypes.c_uint32 # enum
    argloc_t__biggest_t = ctypes.c_uint64
    
    # values for enumeration 'debugger_t__event_t'
    debugger_t__event_t__enumvalues = {
        0: 'ev_init_debugger',
        1: 'ev_term_debugger',
        2: 'ev_get_processes',
        3: 'ev_start_process',
        4: 'ev_attach_process',
        5: 'ev_detach_process',
        6: 'ev_get_debapp_attrs',
        7: 'ev_rebase_if_required_to',
        8: 'ev_request_pause',
        9: 'ev_exit_process',
        10: 'ev_get_debug_event',
        11: 'ev_resume',
        12: 'ev_set_exception_info',
        13: 'ev_suspended',
        14: 'ev_thread_suspend',
        15: 'ev_thread_continue',
        16: 'ev_set_resume_mode',
        17: 'ev_read_registers',
        18: 'ev_write_register',
        19: 'ev_thread_get_sreg_base',
        20: 'ev_get_memory_info',
        21: 'ev_read_memory',
        22: 'ev_write_memory',
        23: 'ev_check_bpt',
        24: 'ev_update_bpts',
        25: 'ev_update_lowcnds',
        26: 'ev_open_file',
        27: 'ev_close_file',
        28: 'ev_read_file',
        29: 'ev_write_file',
        30: 'ev_map_address',
        31: 'ev_get_debmod_extensions',
        32: 'ev_update_call_stack',
        33: 'ev_appcall',
        34: 'ev_cleanup_appcall',
        35: 'ev_eval_lowcnd',
        36: 'ev_send_ioctl',
        37: 'ev_dbg_enable_trace',
        38: 'ev_is_tracing_enabled',
        39: 'ev_rexec',
        40: 'ev_get_srcinfo_path',
        41: 'ev_bin_search',
    }
    ev_init_debugger = 0
    ev_term_debugger = 1
    ev_get_processes = 2
    ev_start_process = 3
    ev_attach_process = 4
    ev_detach_process = 5
    ev_get_debapp_attrs = 6
    ev_rebase_if_required_to = 7
    ev_request_pause = 8
    ev_exit_process = 9
    ev_get_debug_event = 10
    ev_resume = 11
    ev_set_exception_info = 12
    ev_suspended = 13
    ev_thread_suspend = 14
    ev_thread_continue = 15
    ev_set_resume_mode = 16
    ev_read_registers = 17
    ev_write_register = 18
    ev_thread_get_sreg_base = 19
    ev_get_memory_info = 20
    ev_read_memory = 21
    ev_write_memory = 22
    ev_check_bpt = 23
    ev_update_bpts = 24
    ev_update_lowcnds = 25
    ev_open_file = 26
    ev_close_file = 27
    ev_read_file = 28
    ev_write_file = 29
    ev_map_address = 30
    ev_get_debmod_extensions = 31
    ev_update_call_stack = 32
    ev_appcall = 33
    ev_cleanup_appcall = 34
    ev_eval_lowcnd = 35
    ev_send_ioctl = 36
    ev_dbg_enable_trace = 37
    ev_is_tracing_enabled = 38
    ev_rexec = 39
    ev_get_srcinfo_path = 40
    ev_bin_search = 41
    debugger_t__event_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'find_extlang_kind_t'
    find_extlang_kind_t__enumvalues = {
        0: 'FIND_EXTLANG_BY_EXT',
        1: 'FIND_EXTLANG_BY_NAME',
        2: 'FIND_EXTLANG_BY_IDX',
    }
    FIND_EXTLANG_BY_EXT = 0
    FIND_EXTLANG_BY_NAME = 1
    FIND_EXTLANG_BY_IDX = 2
    find_extlang_kind_t = ctypes.c_uint32 # enum
    
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
    mangled_name_type_t = ctypes.c_int32
    
    # values for enumeration 'view_notification_t'
    view_notification_t__enumvalues = {
        0: 'view_activated',
        1: 'view_deactivated',
        2: 'view_keydown',
        3: 'view_click',
        4: 'view_dblclick',
        5: 'view_curpos',
        6: 'view_created',
        7: 'view_close',
        8: 'view_switched',
        9: 'view_mouse_over',
        10: 'view_loc_changed',
        11: 'view_mouse_moved',
    }
    view_activated = 0
    view_deactivated = 1
    view_keydown = 2
    view_click = 3
    view_dblclick = 4
    view_curpos = 5
    view_created = 6
    view_close = 7
    view_switched = 8
    view_mouse_over = 9
    view_loc_changed = 10
    view_mouse_moved = 11
    view_notification_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'dbg_notification_t'
    dbg_notification_t__enumvalues = {
        0: 'dbg_null',
        1: 'dbg_process_start',
        2: 'dbg_process_exit',
        3: 'dbg_process_attach',
        4: 'dbg_process_detach',
        5: 'dbg_thread_start',
        6: 'dbg_thread_exit',
        7: 'dbg_library_load',
        8: 'dbg_library_unload',
        9: 'dbg_information',
        10: 'dbg_exception',
        11: 'dbg_suspend_process',
        12: 'dbg_bpt',
        13: 'dbg_trace',
        14: 'dbg_request_error',
        15: 'dbg_step_into',
        16: 'dbg_step_over',
        17: 'dbg_run_to',
        18: 'dbg_step_until_ret',
        19: 'dbg_bpt_changed',
        20: 'dbg_started_loading_bpts',
        21: 'dbg_finished_loading_bpts',
        22: 'dbg_last',
    }
    dbg_null = 0
    dbg_process_start = 1
    dbg_process_exit = 2
    dbg_process_attach = 3
    dbg_process_detach = 4
    dbg_thread_start = 5
    dbg_thread_exit = 6
    dbg_library_load = 7
    dbg_library_unload = 8
    dbg_information = 9
    dbg_exception = 10
    dbg_suspend_process = 11
    dbg_bpt = 12
    dbg_trace = 13
    dbg_request_error = 14
    dbg_step_into = 15
    dbg_step_over = 16
    dbg_run_to = 17
    dbg_step_until_ret = 18
    dbg_bpt_changed = 19
    dbg_started_loading_bpts = 20
    dbg_finished_loading_bpts = 21
    dbg_last = 22
    dbg_notification_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'locchange_reason_t'
    locchange_reason_t__enumvalues = {
        0: 'lcr_unknown',
        1: 'lcr_goto',
        2: 'lcr_user_switch',
        3: 'lcr_auto_switch',
        4: 'lcr_jump',
        5: 'lcr_navigate',
        6: 'lcr_scroll',
        7: 'lcr_internal',
    }
    lcr_unknown = 0
    lcr_goto = 1
    lcr_user_switch = 2
    lcr_auto_switch = 3
    lcr_jump = 4
    lcr_navigate = 5
    lcr_scroll = 6
    lcr_internal = 7
    locchange_reason_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'msg_notification_t'
    msg_notification_t__enumvalues = {
        0: 'msg_activated',
        1: 'msg_deactivated',
        2: 'msg_click',
        3: 'msg_dblclick',
        4: 'msg_closed',
        5: 'msg_keydown',
    }
    msg_activated = 0
    msg_deactivated = 1
    msg_click = 2
    msg_dblclick = 3
    msg_closed = 4
    msg_keydown = 5
    msg_notification_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'format_functype_t'
    format_functype_t__enumvalues = {
        0: 'FMTFUNC_PRINTF',
        1: 'FMTFUNC_SCANF',
        2: 'FMTFUNC_STRFTIME',
        3: 'FMTFUNC_STRFMON',
    }
    FMTFUNC_PRINTF = 0
    FMTFUNC_SCANF = 1
    FMTFUNC_STRFTIME = 2
    FMTFUNC_STRFMON = 3
    format_functype_t = ctypes.c_uint32 # enum
    ignore_name_def_t = ctypes.c_int32
    
    # values for enumeration 'save_reg_values_t'
    save_reg_values_t__enumvalues = {
        0: 'SAVE_ALL_VALUES',
        1: 'SAVE_DIFF',
        2: 'SAVE_NONE',
    }
    SAVE_ALL_VALUES = 0
    SAVE_DIFF = 1
    SAVE_NONE = 2
    save_reg_values_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'ui_notification_t'
    ui_notification_t__enumvalues = {
        0: 'ui_null',
        1: 'ui_range',
        2: 'ui_refresh_choosers',
        3: 'ui_idcstart',
        4: 'ui_idcstop',
        5: 'ui_suspend',
        6: 'ui_resume',
        7: 'ui_broadcast',
        8: 'ui_read_selection',
        9: 'ui_read_range_selection',
        10: 'ui_unmarksel',
        11: 'ui_screenea',
        12: 'ui_saving',
        13: 'ui_saved',
        14: 'ui_refreshmarked',
        15: 'ui_refresh',
        16: 'ui_choose',
        17: 'ui_close_chooser',
        18: 'ui_banner',
        19: 'ui_setidle',
        20: 'ui_database_closed',
        21: 'ui_beep',
        22: 'ui_is_msg_inited',
        23: 'ui_msg',
        24: 'ui_mbox',
        25: 'ui_clr_cancelled',
        26: 'ui_set_cancelled',
        27: 'ui_test_cancelled',
        28: 'ui_ask_buttons',
        29: 'ui_ask_file',
        30: 'ui_ask_form',
        31: 'ui_ask_text',
        32: 'ui_ask_str',
        33: 'ui_ask_addr',
        34: 'ui_ask_seg',
        35: 'ui_ask_long',
        36: 'ui_add_idckey',
        37: 'ui_obsolete_del_idckey',
        38: 'ui_analyzer_options',
        39: 'ui_load_file',
        40: 'ui_run_dbg',
        41: 'ui_get_cursor',
        42: 'ui_get_curline',
        43: 'ui_copywarn',
        44: 'ui_noabort',
        45: 'ui_lock_range_refresh',
        46: 'ui_unlock_range_refresh',
        47: 'ui_genfile_callback',
        48: 'ui_open_url',
        49: 'ui_hexdumpea',
        50: 'ui_get_key_code',
        51: 'ui_setup_plugins_menu',
        52: 'ui_get_kernel_version',
        53: 'ui_is_idaq',
        54: 'ui_refresh_navband',
        55: 'ui_debugger_menu_change',
        56: 'ui_get_curplace',
        57: 'ui_obsolete_display_widget',
        58: 'ui_close_widget',
        59: 'ui_activate_widget',
        60: 'ui_find_widget',
        61: 'ui_get_current_widget',
        62: 'ui_widget_visible',
        63: 'ui_widget_closing',
        64: 'ui_widget_invisible',
        65: 'ui_get_ea_hint',
        66: 'ui_get_item_hint',
        67: 'ui_refresh_custom_viewer',
        68: 'ui_destroy_custom_viewer',
        69: 'ui_jump_in_custom_viewer',
        70: 'ui_get_custom_viewer_curline',
        71: 'ui_get_current_viewer',
        72: 'ui_is_idaview',
        73: 'ui_get_custom_viewer_hint',
        74: 'ui_set_custom_viewer_range',
        75: 'ui_database_inited',
        76: 'ui_ready_to_run',
        77: 'ui_set_custom_viewer_handler',
        78: 'ui_refresh_chooser',
        79: 'ui_open_builtin',
        80: 'ui_preprocess_action',
        81: 'ui_postprocess_action',
        82: 'ui_set_custom_viewer_mode',
        83: 'ui_gen_disasm_text',
        84: 'ui_gen_idanode_text',
        85: 'ui_install_cli',
        86: 'ui_execute_sync',
        87: 'ui_get_chooser_obj',
        88: 'ui_enable_chooser_item_attrs',
        89: 'ui_get_chooser_item_attrs',
        90: 'ui_set_dock_pos',
        91: 'ui_get_opnum',
        92: 'ui_install_custom_datatype_menu',
        93: 'ui_install_custom_optype_menu',
        94: 'ui_get_range_marker',
        95: 'ui_lookup_key_code',
        96: 'ui_load_custom_icon_file',
        97: 'ui_load_custom_icon',
        98: 'ui_free_custom_icon',
        99: 'ui_process_action',
        100: 'ui_create_code_viewer',
        101: 'ui_addons',
        102: 'ui_execute_ui_requests',
        103: 'ui_execute_ui_requests_list',
        104: 'ui_register_timer',
        105: 'ui_unregister_timer',
        106: 'ui_take_database_snapshot',
        107: 'ui_restore_database_snapshot',
        108: 'ui_set_code_viewer_line_handlers',
        109: 'ui_obsolete_refresh_custom_code_viewer',
        110: 'ui_create_source_viewer',
        111: 'ui_get_tab_size',
        112: 'ui_repaint_qwidget',
        113: 'ui_custom_viewer_set_userdata',
        114: 'ui_jumpto',
        115: 'ui_cancel_exec_request',
        116: 'ui_open_form',
        117: 'ui_unrecognized_config_directive',
        118: 'ui_get_output_cursor',
        119: 'ui_get_output_curline',
        120: 'ui_get_output_selected_text',
        121: 'ui_get_renderer_type',
        122: 'ui_set_renderer_type',
        123: 'ui_get_viewer_user_data',
        124: 'ui_get_viewer_place_type',
        125: 'ui_ea_viewer_history_push_and_jump',
        126: 'ui_ea_viewer_history_info',
        127: 'ui_register_action',
        128: 'ui_unregister_action',
        129: 'ui_attach_action_to_menu',
        130: 'ui_detach_action_from_menu',
        131: 'ui_attach_action_to_popup',
        132: 'ui_detach_action_from_popup',
        133: 'ui_attach_dynamic_action_to_popup',
        134: 'ui_attach_action_to_toolbar',
        135: 'ui_detach_action_from_toolbar',
        136: 'ui_updating_actions',
        137: 'ui_updated_actions',
        138: 'ui_populating_widget_popup',
        139: 'ui_finish_populating_widget_popup',
        140: 'ui_update_action_attr',
        141: 'ui_get_action_attr',
        142: 'ui_plugin_loaded',
        143: 'ui_plugin_unloading',
        144: 'ui_get_widget_type',
        145: 'ui_current_widget_changed',
        146: 'ui_get_widget_title',
        147: 'ui_obsolete_get_user_strlist_options',
        148: 'ui_create_custom_viewer',
        149: 'ui_custom_viewer_jump',
        150: 'ui_set_custom_viewer_handlers',
        151: 'ui_get_registered_actions',
        152: 'ui_create_toolbar',
        153: 'ui_delete_toolbar',
        154: 'ui_create_menu',
        155: 'ui_delete_menu',
        156: 'ui_obsolete_set_nav_colorizer',
        157: 'ui_get_chooser_data',
        158: 'ui_obsolete_get_highlight',
        159: 'ui_set_highlight',
        160: 'ui_set_mappings',
        161: 'ui_create_empty_widget',
        162: 'ui_msg_clear',
        163: 'ui_msg_save',
        164: 'ui_msg_get_lines',
        165: 'ui_chooser_default_enter',
        166: 'ui_screen_ea_changed',
        167: 'ui_get_active_modal_widget',
        168: 'ui_navband_pixel',
        169: 'ui_navband_ea',
        170: 'ui_get_window_id',
        171: 'ui_create_desktop_widget',
        172: 'ui_strchoose',
        173: 'ui_set_nav_colorizer',
        174: 'ui_display_widget',
        175: 'ui_get_lines_rendering_info',
        176: 'ui_sync_sources',
        177: 'ui_get_widget_config',
        178: 'ui_set_widget_config',
        179: 'ui_get_custom_viewer_location',
        180: 'ui_initing_database',
        181: 'ui_destroying_procmod',
        182: 'ui_destroying_plugmod',
        183: 'ui_update_file_history',
        184: 'ui_cancel_thread_exec_requests',
        185: 'ui_get_synced_group',
        186: 'ui_show_rename_dialog',
        187: 'ui_desktop_applied',
        188: 'ui_choose_bookmark',
        189: 'ui_get_custom_viewer_place_xcoord',
        190: 'ui_get_user_input_event',
        191: 'ui_get_highlight_2',
        192: 'ui_last',
        1000: 'ui_dbg_begin',
        1000: 'ui_dbg_run_requests',
        1001: 'ui_dbg_get_running_request',
        1002: 'ui_dbg_get_running_notification',
        1003: 'ui_dbg_clear_requests_queue',
        1004: 'ui_dbg_get_process_state',
        1005: 'ui_dbg_start_process',
        1006: 'ui_dbg_request_start_process',
        1007: 'ui_dbg_suspend_process',
        1008: 'ui_dbg_request_suspend_process',
        1009: 'ui_dbg_continue_process',
        1010: 'ui_dbg_request_continue_process',
        1011: 'ui_dbg_exit_process',
        1012: 'ui_dbg_request_exit_process',
        1013: 'ui_dbg_get_thread_qty',
        1014: 'ui_dbg_getn_thread',
        1015: 'ui_dbg_select_thread',
        1016: 'ui_dbg_request_select_thread',
        1017: 'ui_dbg_step_into',
        1018: 'ui_dbg_request_step_into',
        1019: 'ui_dbg_step_over',
        1020: 'ui_dbg_request_step_over',
        1021: 'ui_dbg_run_to',
        1022: 'ui_dbg_request_run_to',
        1023: 'ui_dbg_step_until_ret',
        1024: 'ui_dbg_request_step_until_ret',
        1025: 'ui_dbg_get_bpt_qty',
        1026: 'ui_dbg_add_oldbpt',
        1027: 'ui_dbg_request_add_oldbpt',
        1028: 'ui_dbg_del_oldbpt',
        1029: 'ui_dbg_request_del_oldbpt',
        1030: 'ui_dbg_enable_oldbpt',
        1031: 'ui_dbg_request_enable_oldbpt',
        1032: 'ui_dbg_set_trace_size',
        1033: 'ui_dbg_clear_trace',
        1034: 'ui_dbg_request_clear_trace',
        1035: 'ui_dbg_is_step_trace_enabled',
        1036: 'ui_dbg_enable_step_trace',
        1037: 'ui_dbg_request_enable_step_trace',
        1038: 'ui_dbg_get_step_trace_options',
        1039: 'ui_dbg_set_step_trace_options',
        1040: 'ui_dbg_request_set_step_trace_options',
        1041: 'ui_dbg_is_insn_trace_enabled',
        1042: 'ui_dbg_enable_insn_trace',
        1043: 'ui_dbg_request_enable_insn_trace',
        1044: 'ui_dbg_get_insn_trace_options',
        1045: 'ui_dbg_set_insn_trace_options',
        1046: 'ui_dbg_request_set_insn_trace_options',
        1047: 'ui_dbg_is_func_trace_enabled',
        1048: 'ui_dbg_enable_func_trace',
        1049: 'ui_dbg_request_enable_func_trace',
        1050: 'ui_dbg_get_func_trace_options',
        1051: 'ui_dbg_set_func_trace_options',
        1052: 'ui_dbg_request_set_func_trace_options',
        1053: 'ui_dbg_get_tev_qty',
        1054: 'ui_dbg_get_tev_info',
        1055: 'ui_dbg_get_call_tev_callee',
        1056: 'ui_dbg_get_ret_tev_return',
        1057: 'ui_dbg_get_bpt_tev_ea',
        1058: 'ui_dbg_get_reg_value_type',
        1059: 'ui_dbg_get_processes',
        1060: 'ui_dbg_attach_process',
        1061: 'ui_dbg_request_attach_process',
        1062: 'ui_dbg_detach_process',
        1063: 'ui_dbg_request_detach_process',
        1064: 'ui_dbg_get_first_module',
        1065: 'ui_dbg_get_next_module',
        1066: 'ui_dbg_bring_to_front',
        1067: 'ui_dbg_get_current_thread',
        1068: 'ui_dbg_wait_for_next_event',
        1069: 'ui_dbg_get_debug_event',
        1070: 'ui_dbg_set_debugger_options',
        1071: 'ui_dbg_set_remote_debugger',
        1072: 'ui_dbg_load_debugger',
        1073: 'ui_dbg_retrieve_exceptions',
        1074: 'ui_dbg_store_exceptions',
        1075: 'ui_dbg_define_exception',
        1076: 'ui_dbg_suspend_thread',
        1077: 'ui_dbg_request_suspend_thread',
        1078: 'ui_dbg_resume_thread',
        1079: 'ui_dbg_request_resume_thread',
        1080: 'ui_dbg_get_process_options',
        1081: 'ui_dbg_check_bpt',
        1082: 'ui_dbg_set_process_state',
        1083: 'ui_dbg_get_manual_regions',
        1084: 'ui_dbg_set_manual_regions',
        1085: 'ui_dbg_enable_manual_regions',
        1086: 'ui_dbg_set_process_options',
        1087: 'ui_dbg_is_busy',
        1088: 'ui_dbg_hide_all_bpts',
        1089: 'ui_dbg_edit_manual_regions',
        1090: 'ui_dbg_get_sp_val',
        1091: 'ui_dbg_get_ip_val',
        1092: 'ui_dbg_get_reg_val',
        1093: 'ui_dbg_set_reg_val',
        1094: 'ui_dbg_request_set_reg_val',
        1095: 'ui_dbg_get_insn_tev_reg_val',
        1096: 'ui_dbg_get_insn_tev_reg_result',
        1097: 'ui_dbg_register_provider',
        1098: 'ui_dbg_unregister_provider',
        1099: 'ui_dbg_handle_debug_event',
        1100: 'ui_dbg_add_vmod',
        1101: 'ui_dbg_del_vmod',
        1102: 'ui_dbg_compare_bpt_locs',
        1103: 'ui_obsolete_dbg_save_bpts',
        1104: 'ui_dbg_set_bptloc_string',
        1105: 'ui_dbg_get_bptloc_string',
        1106: 'ui_dbg_internal_appcall',
        1107: 'ui_dbg_internal_cleanup_appcall',
        1108: 'ui_dbg_internal_get_sreg_base',
        1109: 'ui_dbg_internal_ioctl',
        1110: 'ui_dbg_read_memory',
        1111: 'ui_dbg_write_memory',
        1112: 'ui_dbg_read_registers',
        1113: 'ui_dbg_write_register',
        1114: 'ui_dbg_get_memory_info',
        1115: 'ui_dbg_get_event_cond',
        1116: 'ui_dbg_set_event_cond',
        1117: 'ui_dbg_enable_bpt',
        1118: 'ui_dbg_request_enable_bpt',
        1119: 'ui_dbg_del_bpt',
        1120: 'ui_dbg_request_del_bpt',
        1121: 'ui_dbg_map_source_path',
        1122: 'ui_dbg_map_source_file_path',
        1123: 'ui_dbg_modify_source_paths',
        1124: 'ui_dbg_is_bblk_trace_enabled',
        1125: 'ui_dbg_enable_bblk_trace',
        1126: 'ui_dbg_request_enable_bblk_trace',
        1127: 'ui_dbg_get_bblk_trace_options',
        1128: 'ui_dbg_set_bblk_trace_options',
        1129: 'ui_dbg_request_set_bblk_trace_options',
        1130: 'ui_dbg_load_trace_file',
        1131: 'ui_dbg_save_trace_file',
        1132: 'ui_dbg_is_valid_trace_file',
        1133: 'ui_dbg_set_trace_file_desc',
        1134: 'ui_dbg_get_trace_file_desc',
        1135: 'ui_dbg_choose_trace_file',
        1136: 'ui_dbg_diff_trace_file',
        1137: 'ui_dbg_graph_trace',
        1138: 'ui_dbg_get_tev_memory_info',
        1139: 'ui_dbg_get_tev_event',
        1140: 'ui_dbg_get_insn_tev_reg_mem',
        1141: 'ui_dbg_getn_bpt',
        1142: 'ui_dbg_get_bpt',
        1143: 'ui_dbg_find_bpt',
        1144: 'ui_dbg_add_bpt',
        1145: 'ui_dbg_request_add_bpt',
        1146: 'ui_dbg_update_bpt',
        1147: 'ui_dbg_for_all_bpts',
        1148: 'ui_dbg_get_tev_ea',
        1149: 'ui_dbg_get_tev_type',
        1150: 'ui_dbg_get_tev_tid',
        1151: 'ui_dbg_get_trace_base_address',
        1152: 'ui_dbg_set_trace_base_address',
        1153: 'ui_dbg_add_tev',
        1154: 'ui_dbg_add_insn_tev',
        1155: 'ui_dbg_add_call_tev',
        1156: 'ui_dbg_add_ret_tev',
        1157: 'ui_dbg_add_bpt_tev',
        1158: 'ui_dbg_add_debug_event',
        1159: 'ui_dbg_add_thread',
        1160: 'ui_dbg_del_thread',
        1161: 'ui_dbg_add_many_tevs',
        1162: 'ui_dbg_set_bpt_group',
        1163: 'ui_dbg_set_highlight_trace_options',
        1164: 'ui_dbg_set_trace_platform',
        1165: 'ui_dbg_get_trace_platform',
        1166: 'ui_dbg_internal_get_elang',
        1167: 'ui_dbg_internal_set_elang',
        1168: 'ui_dbg_load_dbg_dbginfo',
        1169: 'ui_dbg_set_resume_mode',
        1170: 'ui_dbg_request_set_resume_mode',
        1171: 'ui_dbg_set_bptloc_group',
        1172: 'ui_dbg_list_bptgrps',
        1173: 'ui_dbg_rename_bptgrp',
        1174: 'ui_dbg_del_bptgrp',
        1175: 'ui_dbg_get_grp_bpts',
        1176: 'ui_dbg_get_bpt_group',
        1177: 'ui_dbg_change_bptlocs',
        1178: 'ui_dbg_collect_stack_trace',
        1179: 'ui_dbg_get_module_info',
        1180: 'ui_dbg_get_srcinfo_provider',
        1181: 'ui_dbg_get_global_var',
        1182: 'ui_dbg_get_local_var',
        1183: 'ui_dbg_get_local_vars',
        1184: 'ui_dbg_add_path_mapping',
        1185: 'ui_dbg_get_current_source_file',
        1186: 'ui_dbg_get_current_source_line',
        1187: 'ui_dbg_srcdbg_step_into',
        1188: 'ui_dbg_srcdbg_request_step_into',
        1189: 'ui_dbg_srcdbg_step_over',
        1190: 'ui_dbg_srcdbg_request_step_over',
        1191: 'ui_dbg_srcdbg_step_until_ret',
        1192: 'ui_dbg_srcdbg_request_step_until_ret',
        1193: 'ui_dbg_getn_thread_name',
        1194: 'ui_dbg_bin_search',
        1195: 'ui_dbg_get_insn_tev_reg_val_i',
        1196: 'ui_dbg_get_insn_tev_reg_result_i',
        1197: 'ui_dbg_get_reg_val_i',
        1198: 'ui_dbg_set_reg_val_i',
        1199: 'ui_dbg_get_reg_info',
        1200: 'ui_dbg_set_trace_dynamic_register_set',
        1201: 'ui_dbg_get_trace_dynamic_register_set',
        1202: 'ui_dbg_enable_bptgrp',
        1203: 'ui_dbg_end',
    }
    ui_null = 0
    ui_range = 1
    ui_refresh_choosers = 2
    ui_idcstart = 3
    ui_idcstop = 4
    ui_suspend = 5
    ui_resume = 6
    ui_broadcast = 7
    ui_read_selection = 8
    ui_read_range_selection = 9
    ui_unmarksel = 10
    ui_screenea = 11
    ui_saving = 12
    ui_saved = 13
    ui_refreshmarked = 14
    ui_refresh = 15
    ui_choose = 16
    ui_close_chooser = 17
    ui_banner = 18
    ui_setidle = 19
    ui_database_closed = 20
    ui_beep = 21
    ui_is_msg_inited = 22
    ui_msg = 23
    ui_mbox = 24
    ui_clr_cancelled = 25
    ui_set_cancelled = 26
    ui_test_cancelled = 27
    ui_ask_buttons = 28
    ui_ask_file = 29
    ui_ask_form = 30
    ui_ask_text = 31
    ui_ask_str = 32
    ui_ask_addr = 33
    ui_ask_seg = 34
    ui_ask_long = 35
    ui_add_idckey = 36
    ui_obsolete_del_idckey = 37
    ui_analyzer_options = 38
    ui_load_file = 39
    ui_run_dbg = 40
    ui_get_cursor = 41
    ui_get_curline = 42
    ui_copywarn = 43
    ui_noabort = 44
    ui_lock_range_refresh = 45
    ui_unlock_range_refresh = 46
    ui_genfile_callback = 47
    ui_open_url = 48
    ui_hexdumpea = 49
    ui_get_key_code = 50
    ui_setup_plugins_menu = 51
    ui_get_kernel_version = 52
    ui_is_idaq = 53
    ui_refresh_navband = 54
    ui_debugger_menu_change = 55
    ui_get_curplace = 56
    ui_obsolete_display_widget = 57
    ui_close_widget = 58
    ui_activate_widget = 59
    ui_find_widget = 60
    ui_get_current_widget = 61
    ui_widget_visible = 62
    ui_widget_closing = 63
    ui_widget_invisible = 64
    ui_get_ea_hint = 65
    ui_get_item_hint = 66
    ui_refresh_custom_viewer = 67
    ui_destroy_custom_viewer = 68
    ui_jump_in_custom_viewer = 69
    ui_get_custom_viewer_curline = 70
    ui_get_current_viewer = 71
    ui_is_idaview = 72
    ui_get_custom_viewer_hint = 73
    ui_set_custom_viewer_range = 74
    ui_database_inited = 75
    ui_ready_to_run = 76
    ui_set_custom_viewer_handler = 77
    ui_refresh_chooser = 78
    ui_open_builtin = 79
    ui_preprocess_action = 80
    ui_postprocess_action = 81
    ui_set_custom_viewer_mode = 82
    ui_gen_disasm_text = 83
    ui_gen_idanode_text = 84
    ui_install_cli = 85
    ui_execute_sync = 86
    ui_get_chooser_obj = 87
    ui_enable_chooser_item_attrs = 88
    ui_get_chooser_item_attrs = 89
    ui_set_dock_pos = 90
    ui_get_opnum = 91
    ui_install_custom_datatype_menu = 92
    ui_install_custom_optype_menu = 93
    ui_get_range_marker = 94
    ui_lookup_key_code = 95
    ui_load_custom_icon_file = 96
    ui_load_custom_icon = 97
    ui_free_custom_icon = 98
    ui_process_action = 99
    ui_create_code_viewer = 100
    ui_addons = 101
    ui_execute_ui_requests = 102
    ui_execute_ui_requests_list = 103
    ui_register_timer = 104
    ui_unregister_timer = 105
    ui_take_database_snapshot = 106
    ui_restore_database_snapshot = 107
    ui_set_code_viewer_line_handlers = 108
    ui_obsolete_refresh_custom_code_viewer = 109
    ui_create_source_viewer = 110
    ui_get_tab_size = 111
    ui_repaint_qwidget = 112
    ui_custom_viewer_set_userdata = 113
    ui_jumpto = 114
    ui_cancel_exec_request = 115
    ui_open_form = 116
    ui_unrecognized_config_directive = 117
    ui_get_output_cursor = 118
    ui_get_output_curline = 119
    ui_get_output_selected_text = 120
    ui_get_renderer_type = 121
    ui_set_renderer_type = 122
    ui_get_viewer_user_data = 123
    ui_get_viewer_place_type = 124
    ui_ea_viewer_history_push_and_jump = 125
    ui_ea_viewer_history_info = 126
    ui_register_action = 127
    ui_unregister_action = 128
    ui_attach_action_to_menu = 129
    ui_detach_action_from_menu = 130
    ui_attach_action_to_popup = 131
    ui_detach_action_from_popup = 132
    ui_attach_dynamic_action_to_popup = 133
    ui_attach_action_to_toolbar = 134
    ui_detach_action_from_toolbar = 135
    ui_updating_actions = 136
    ui_updated_actions = 137
    ui_populating_widget_popup = 138
    ui_finish_populating_widget_popup = 139
    ui_update_action_attr = 140
    ui_get_action_attr = 141
    ui_plugin_loaded = 142
    ui_plugin_unloading = 143
    ui_get_widget_type = 144
    ui_current_widget_changed = 145
    ui_get_widget_title = 146
    ui_obsolete_get_user_strlist_options = 147
    ui_create_custom_viewer = 148
    ui_custom_viewer_jump = 149
    ui_set_custom_viewer_handlers = 150
    ui_get_registered_actions = 151
    ui_create_toolbar = 152
    ui_delete_toolbar = 153
    ui_create_menu = 154
    ui_delete_menu = 155
    ui_obsolete_set_nav_colorizer = 156
    ui_get_chooser_data = 157
    ui_obsolete_get_highlight = 158
    ui_set_highlight = 159
    ui_set_mappings = 160
    ui_create_empty_widget = 161
    ui_msg_clear = 162
    ui_msg_save = 163
    ui_msg_get_lines = 164
    ui_chooser_default_enter = 165
    ui_screen_ea_changed = 166
    ui_get_active_modal_widget = 167
    ui_navband_pixel = 168
    ui_navband_ea = 169
    ui_get_window_id = 170
    ui_create_desktop_widget = 171
    ui_strchoose = 172
    ui_set_nav_colorizer = 173
    ui_display_widget = 174
    ui_get_lines_rendering_info = 175
    ui_sync_sources = 176
    ui_get_widget_config = 177
    ui_set_widget_config = 178
    ui_get_custom_viewer_location = 179
    ui_initing_database = 180
    ui_destroying_procmod = 181
    ui_destroying_plugmod = 182
    ui_update_file_history = 183
    ui_cancel_thread_exec_requests = 184
    ui_get_synced_group = 185
    ui_show_rename_dialog = 186
    ui_desktop_applied = 187
    ui_choose_bookmark = 188
    ui_get_custom_viewer_place_xcoord = 189
    ui_get_user_input_event = 190
    ui_get_highlight_2 = 191
    ui_last = 192
    ui_dbg_begin = 1000
    ui_dbg_run_requests = 1000
    ui_dbg_get_running_request = 1001
    ui_dbg_get_running_notification = 1002
    ui_dbg_clear_requests_queue = 1003
    ui_dbg_get_process_state = 1004
    ui_dbg_start_process = 1005
    ui_dbg_request_start_process = 1006
    ui_dbg_suspend_process = 1007
    ui_dbg_request_suspend_process = 1008
    ui_dbg_continue_process = 1009
    ui_dbg_request_continue_process = 1010
    ui_dbg_exit_process = 1011
    ui_dbg_request_exit_process = 1012
    ui_dbg_get_thread_qty = 1013
    ui_dbg_getn_thread = 1014
    ui_dbg_select_thread = 1015
    ui_dbg_request_select_thread = 1016
    ui_dbg_step_into = 1017
    ui_dbg_request_step_into = 1018
    ui_dbg_step_over = 1019
    ui_dbg_request_step_over = 1020
    ui_dbg_run_to = 1021
    ui_dbg_request_run_to = 1022
    ui_dbg_step_until_ret = 1023
    ui_dbg_request_step_until_ret = 1024
    ui_dbg_get_bpt_qty = 1025
    ui_dbg_add_oldbpt = 1026
    ui_dbg_request_add_oldbpt = 1027
    ui_dbg_del_oldbpt = 1028
    ui_dbg_request_del_oldbpt = 1029
    ui_dbg_enable_oldbpt = 1030
    ui_dbg_request_enable_oldbpt = 1031
    ui_dbg_set_trace_size = 1032
    ui_dbg_clear_trace = 1033
    ui_dbg_request_clear_trace = 1034
    ui_dbg_is_step_trace_enabled = 1035
    ui_dbg_enable_step_trace = 1036
    ui_dbg_request_enable_step_trace = 1037
    ui_dbg_get_step_trace_options = 1038
    ui_dbg_set_step_trace_options = 1039
    ui_dbg_request_set_step_trace_options = 1040
    ui_dbg_is_insn_trace_enabled = 1041
    ui_dbg_enable_insn_trace = 1042
    ui_dbg_request_enable_insn_trace = 1043
    ui_dbg_get_insn_trace_options = 1044
    ui_dbg_set_insn_trace_options = 1045
    ui_dbg_request_set_insn_trace_options = 1046
    ui_dbg_is_func_trace_enabled = 1047
    ui_dbg_enable_func_trace = 1048
    ui_dbg_request_enable_func_trace = 1049
    ui_dbg_get_func_trace_options = 1050
    ui_dbg_set_func_trace_options = 1051
    ui_dbg_request_set_func_trace_options = 1052
    ui_dbg_get_tev_qty = 1053
    ui_dbg_get_tev_info = 1054
    ui_dbg_get_call_tev_callee = 1055
    ui_dbg_get_ret_tev_return = 1056
    ui_dbg_get_bpt_tev_ea = 1057
    ui_dbg_get_reg_value_type = 1058
    ui_dbg_get_processes = 1059
    ui_dbg_attach_process = 1060
    ui_dbg_request_attach_process = 1061
    ui_dbg_detach_process = 1062
    ui_dbg_request_detach_process = 1063
    ui_dbg_get_first_module = 1064
    ui_dbg_get_next_module = 1065
    ui_dbg_bring_to_front = 1066
    ui_dbg_get_current_thread = 1067
    ui_dbg_wait_for_next_event = 1068
    ui_dbg_get_debug_event = 1069
    ui_dbg_set_debugger_options = 1070
    ui_dbg_set_remote_debugger = 1071
    ui_dbg_load_debugger = 1072
    ui_dbg_retrieve_exceptions = 1073
    ui_dbg_store_exceptions = 1074
    ui_dbg_define_exception = 1075
    ui_dbg_suspend_thread = 1076
    ui_dbg_request_suspend_thread = 1077
    ui_dbg_resume_thread = 1078
    ui_dbg_request_resume_thread = 1079
    ui_dbg_get_process_options = 1080
    ui_dbg_check_bpt = 1081
    ui_dbg_set_process_state = 1082
    ui_dbg_get_manual_regions = 1083
    ui_dbg_set_manual_regions = 1084
    ui_dbg_enable_manual_regions = 1085
    ui_dbg_set_process_options = 1086
    ui_dbg_is_busy = 1087
    ui_dbg_hide_all_bpts = 1088
    ui_dbg_edit_manual_regions = 1089
    ui_dbg_get_sp_val = 1090
    ui_dbg_get_ip_val = 1091
    ui_dbg_get_reg_val = 1092
    ui_dbg_set_reg_val = 1093
    ui_dbg_request_set_reg_val = 1094
    ui_dbg_get_insn_tev_reg_val = 1095
    ui_dbg_get_insn_tev_reg_result = 1096
    ui_dbg_register_provider = 1097
    ui_dbg_unregister_provider = 1098
    ui_dbg_handle_debug_event = 1099
    ui_dbg_add_vmod = 1100
    ui_dbg_del_vmod = 1101
    ui_dbg_compare_bpt_locs = 1102
    ui_obsolete_dbg_save_bpts = 1103
    ui_dbg_set_bptloc_string = 1104
    ui_dbg_get_bptloc_string = 1105
    ui_dbg_internal_appcall = 1106
    ui_dbg_internal_cleanup_appcall = 1107
    ui_dbg_internal_get_sreg_base = 1108
    ui_dbg_internal_ioctl = 1109
    ui_dbg_read_memory = 1110
    ui_dbg_write_memory = 1111
    ui_dbg_read_registers = 1112
    ui_dbg_write_register = 1113
    ui_dbg_get_memory_info = 1114
    ui_dbg_get_event_cond = 1115
    ui_dbg_set_event_cond = 1116
    ui_dbg_enable_bpt = 1117
    ui_dbg_request_enable_bpt = 1118
    ui_dbg_del_bpt = 1119
    ui_dbg_request_del_bpt = 1120
    ui_dbg_map_source_path = 1121
    ui_dbg_map_source_file_path = 1122
    ui_dbg_modify_source_paths = 1123
    ui_dbg_is_bblk_trace_enabled = 1124
    ui_dbg_enable_bblk_trace = 1125
    ui_dbg_request_enable_bblk_trace = 1126
    ui_dbg_get_bblk_trace_options = 1127
    ui_dbg_set_bblk_trace_options = 1128
    ui_dbg_request_set_bblk_trace_options = 1129
    ui_dbg_load_trace_file = 1130
    ui_dbg_save_trace_file = 1131
    ui_dbg_is_valid_trace_file = 1132
    ui_dbg_set_trace_file_desc = 1133
    ui_dbg_get_trace_file_desc = 1134
    ui_dbg_choose_trace_file = 1135
    ui_dbg_diff_trace_file = 1136
    ui_dbg_graph_trace = 1137
    ui_dbg_get_tev_memory_info = 1138
    ui_dbg_get_tev_event = 1139
    ui_dbg_get_insn_tev_reg_mem = 1140
    ui_dbg_getn_bpt = 1141
    ui_dbg_get_bpt = 1142
    ui_dbg_find_bpt = 1143
    ui_dbg_add_bpt = 1144
    ui_dbg_request_add_bpt = 1145
    ui_dbg_update_bpt = 1146
    ui_dbg_for_all_bpts = 1147
    ui_dbg_get_tev_ea = 1148
    ui_dbg_get_tev_type = 1149
    ui_dbg_get_tev_tid = 1150
    ui_dbg_get_trace_base_address = 1151
    ui_dbg_set_trace_base_address = 1152
    ui_dbg_add_tev = 1153
    ui_dbg_add_insn_tev = 1154
    ui_dbg_add_call_tev = 1155
    ui_dbg_add_ret_tev = 1156
    ui_dbg_add_bpt_tev = 1157
    ui_dbg_add_debug_event = 1158
    ui_dbg_add_thread = 1159
    ui_dbg_del_thread = 1160
    ui_dbg_add_many_tevs = 1161
    ui_dbg_set_bpt_group = 1162
    ui_dbg_set_highlight_trace_options = 1163
    ui_dbg_set_trace_platform = 1164
    ui_dbg_get_trace_platform = 1165
    ui_dbg_internal_get_elang = 1166
    ui_dbg_internal_set_elang = 1167
    ui_dbg_load_dbg_dbginfo = 1168
    ui_dbg_set_resume_mode = 1169
    ui_dbg_request_set_resume_mode = 1170
    ui_dbg_set_bptloc_group = 1171
    ui_dbg_list_bptgrps = 1172
    ui_dbg_rename_bptgrp = 1173
    ui_dbg_del_bptgrp = 1174
    ui_dbg_get_grp_bpts = 1175
    ui_dbg_get_bpt_group = 1176
    ui_dbg_change_bptlocs = 1177
    ui_dbg_collect_stack_trace = 1178
    ui_dbg_get_module_info = 1179
    ui_dbg_get_srcinfo_provider = 1180
    ui_dbg_get_global_var = 1181
    ui_dbg_get_local_var = 1182
    ui_dbg_get_local_vars = 1183
    ui_dbg_add_path_mapping = 1184
    ui_dbg_get_current_source_file = 1185
    ui_dbg_get_current_source_line = 1186
    ui_dbg_srcdbg_step_into = 1187
    ui_dbg_srcdbg_request_step_into = 1188
    ui_dbg_srcdbg_step_over = 1189
    ui_dbg_srcdbg_request_step_over = 1190
    ui_dbg_srcdbg_step_until_ret = 1191
    ui_dbg_srcdbg_request_step_until_ret = 1192
    ui_dbg_getn_thread_name = 1193
    ui_dbg_bin_search = 1194
    ui_dbg_get_insn_tev_reg_val_i = 1195
    ui_dbg_get_insn_tev_reg_result_i = 1196
    ui_dbg_get_reg_val_i = 1197
    ui_dbg_set_reg_val_i = 1198
    ui_dbg_get_reg_info = 1199
    ui_dbg_set_trace_dynamic_register_set = 1200
    ui_dbg_get_trace_dynamic_register_set = 1201
    ui_dbg_enable_bptgrp = 1202
    ui_dbg_end = 1203
    ui_notification_t = ctypes.c_uint32 # enum
    cliopt_handler_t = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.POINTER(None))
    
    # values for enumeration 'dbg_event_code_t'
    dbg_event_code_t__enumvalues = {
        4294967294: 'DEC_NOTASK',
        4294967295: 'DEC_ERROR',
        0: 'DEC_TIMEOUT',
    }
    DEC_NOTASK = 4294967294
    DEC_ERROR = 4294967295
    DEC_TIMEOUT = 0
    dbg_event_code_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'debug_name_how_t'
    debug_name_how_t__enumvalues = {
        0: 'DEBNAME_EXACT',
        1: 'DEBNAME_LOWER',
        2: 'DEBNAME_UPPER',
        3: 'DEBNAME_NICE',
    }
    DEBNAME_EXACT = 0
    DEBNAME_LOWER = 1
    DEBNAME_UPPER = 2
    DEBNAME_NICE = 3
    debug_name_how_t = ctypes.c_uint32 # enum
    register_class_t = ctypes.c_ubyte
    
    # values for enumeration 'tcc_place_type_t'
    tcc_place_type_t__enumvalues = {
        0: 'TCCPT_INVALID',
        1: 'TCCPT_PLACE',
        2: 'TCCPT_SIMPLELINE_PLACE',
        3: 'TCCPT_IDAPLACE',
        4: 'TCCPT_ENUMPLACE',
        5: 'TCCPT_STRUCTPLACE',
    }
    TCCPT_INVALID = 0
    TCCPT_PLACE = 1
    TCCPT_SIMPLELINE_PLACE = 2
    TCCPT_IDAPLACE = 3
    TCCPT_ENUMPLACE = 4
    TCCPT_STRUCTPLACE = 5
    tcc_place_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'fc_block_type_t'
    fc_block_type_t__enumvalues = {
        0: 'fcb_normal',
        1: 'fcb_indjump',
        2: 'fcb_ret',
        3: 'fcb_cndret',
        4: 'fcb_noret',
        5: 'fcb_enoret',
        6: 'fcb_extern',
        7: 'fcb_error',
    }
    fcb_normal = 0
    fcb_indjump = 1
    fcb_ret = 2
    fcb_cndret = 3
    fcb_noret = 4
    fcb_enoret = 5
    fcb_extern = 6
    fcb_error = 7
    fc_block_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'fpvalue_error_t'
    fpvalue_error_t__enumvalues = {
        0: 'REAL_ERROR_OK',
        4294967295: 'REAL_ERROR_FORMAT',
        4294967294: 'REAL_ERROR_RANGE',
        4294967293: 'REAL_ERROR_BADDATA',
        1: 'REAL_ERROR_FPOVER',
        2: 'REAL_ERROR_BADSTR',
        3: 'REAL_ERROR_ZERODIV',
        4: 'REAL_ERROR_INTOVER',
    }
    REAL_ERROR_OK = 0
    REAL_ERROR_FORMAT = 4294967295
    REAL_ERROR_RANGE = 4294967294
    REAL_ERROR_BADDATA = 4294967293
    REAL_ERROR_FPOVER = 1
    REAL_ERROR_BADSTR = 2
    REAL_ERROR_ZERODIV = 3
    REAL_ERROR_INTOVER = 4
    fpvalue_error_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'setproc_level_t'
    setproc_level_t__enumvalues = {
        0: 'SETPROC_IDB',
        1: 'SETPROC_LOADER',
        2: 'SETPROC_LOADER_NON_FATAL',
        3: 'SETPROC_USER',
    }
    SETPROC_IDB = 0
    SETPROC_LOADER = 1
    SETPROC_LOADER_NON_FATAL = 2
    SETPROC_USER = 3
    setproc_level_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'src_item_kind_t'
    src_item_kind_t__enumvalues = {
        0: 'SRCIT_NONE',
        1: 'SRCIT_MODULE',
        2: 'SRCIT_FUNC',
        3: 'SRCIT_STMT',
        4: 'SRCIT_EXPR',
        5: 'SRCIT_STTVAR',
        6: 'SRCIT_LOCVAR',
    }
    SRCIT_NONE = 0
    SRCIT_MODULE = 1
    SRCIT_FUNC = 2
    SRCIT_STMT = 3
    SRCIT_EXPR = 4
    SRCIT_STTVAR = 5
    SRCIT_LOCVAR = 6
    src_item_kind_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'stock_type_id_t'
    stock_type_id_t__enumvalues = {
        0: 'STI_PCHAR',
        1: 'STI_PUCHAR',
        2: 'STI_PCCHAR',
        3: 'STI_PCUCHAR',
        4: 'STI_PBYTE',
        5: 'STI_PINT',
        6: 'STI_PUINT',
        7: 'STI_PVOID',
        8: 'STI_PPVOID',
        9: 'STI_PCVOID',
        10: 'STI_ACHAR',
        11: 'STI_AUCHAR',
        12: 'STI_ACCHAR',
        13: 'STI_ACUCHAR',
        14: 'STI_FPURGING',
        15: 'STI_FDELOP',
        16: 'STI_MSGSEND',
        17: 'STI_AEABI_LCMP',
        18: 'STI_AEABI_ULCMP',
        19: 'STI_DONT_USE',
        20: 'STI_SIZE_T',
        21: 'STI_SSIZE_T',
        22: 'STI_AEABI_MEMCPY',
        23: 'STI_AEABI_MEMSET',
        24: 'STI_AEABI_MEMCLR',
        25: 'STI_RTC_CHECK_2',
        26: 'STI_RTC_CHECK_4',
        27: 'STI_RTC_CHECK_8',
        28: 'STI_COMPLEX64',
        29: 'STI_COMPLEX128',
        30: 'STI_LAST',
    }
    STI_PCHAR = 0
    STI_PUCHAR = 1
    STI_PCCHAR = 2
    STI_PCUCHAR = 3
    STI_PBYTE = 4
    STI_PINT = 5
    STI_PUINT = 6
    STI_PVOID = 7
    STI_PPVOID = 8
    STI_PCVOID = 9
    STI_ACHAR = 10
    STI_AUCHAR = 11
    STI_ACCHAR = 12
    STI_ACUCHAR = 13
    STI_FPURGING = 14
    STI_FDELOP = 15
    STI_MSGSEND = 16
    STI_AEABI_LCMP = 17
    STI_AEABI_ULCMP = 18
    STI_DONT_USE = 19
    STI_SIZE_T = 20
    STI_SSIZE_T = 21
    STI_AEABI_MEMCPY = 22
    STI_AEABI_MEMSET = 23
    STI_AEABI_MEMCLR = 24
    STI_RTC_CHECK_2 = 25
    STI_RTC_CHECK_4 = 26
    STI_RTC_CHECK_8 = 27
    STI_COMPLEX64 = 28
    STI_COMPLEX128 = 29
    STI_LAST = 30
    stock_type_id_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'action_state_t'
    action_state_t__enumvalues = {
        0: 'AST_ENABLE_ALWAYS',
        1: 'AST_ENABLE_FOR_IDB',
        2: 'AST_ENABLE_FOR_WIDGET',
        3: 'AST_ENABLE',
        4: 'AST_DISABLE_ALWAYS',
        5: 'AST_DISABLE_FOR_IDB',
        6: 'AST_DISABLE_FOR_WIDGET',
        7: 'AST_DISABLE',
    }
    AST_ENABLE_ALWAYS = 0
    AST_ENABLE_FOR_IDB = 1
    AST_ENABLE_FOR_WIDGET = 2
    AST_ENABLE = 3
    AST_DISABLE_ALWAYS = 4
    AST_DISABLE_FOR_IDB = 5
    AST_DISABLE_FOR_WIDGET = 6
    AST_DISABLE = 7
    action_state_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'fpvalue_kind_t'
    fpvalue_kind_t__enumvalues = {
        0: 'FPV_BADARG',
        1: 'FPV_NORM',
        2: 'FPV_NAN',
        3: 'FPV_PINF',
        4: 'FPV_NINF',
    }
    FPV_BADARG = 0
    FPV_NORM = 1
    FPV_NAN = 2
    FPV_PINF = 3
    FPV_NINF = 4
    fpvalue_kind_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'navaddr_type_t'
    navaddr_type_t__enumvalues = {
        0: 'nat_lib',
        1: 'nat_fun',
        2: 'nat_cod',
        3: 'nat_dat',
        4: 'nat_und',
        5: 'nat_ext',
        6: 'nat_err',
        7: 'nat_gap',
        8: 'nat_cur',
        9: 'nat_auto',
        10: 'nat_lum',
        11: 'nat_hlo',
        12: 'nat_last',
    }
    nat_lib = 0
    nat_fun = 1
    nat_cod = 2
    nat_dat = 3
    nat_und = 4
    nat_ext = 5
    nat_err = 6
    nat_gap = 7
    nat_cur = 8
    nat_auto = 9
    nat_lum = 10
    nat_hlo = 11
    nat_last = 12
    navaddr_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'storage_type_t'
    storage_type_t__enumvalues = {
        4294967295: 'STT_CUR',
        0: 'STT_VA',
        1: 'STT_MM',
        2: 'STT_DBG',
    }
    STT_CUR = 4294967295
    STT_VA = 0
    STT_MM = 1
    STT_DBG = 2
    storage_type_t = ctypes.c_uint32 # enum
    twidget_type_t = ctypes.c_int32
    
    # values for enumeration 'action_attr_t'
    action_attr_t__enumvalues = {
        0: 'AA_NONE',
        1: 'AA_LABEL',
        2: 'AA_SHORTCUT',
        3: 'AA_TOOLTIP',
        4: 'AA_ICON',
        5: 'AA_STATE',
        6: 'AA_CHECKABLE',
        7: 'AA_CHECKED',
        8: 'AA_VISIBILITY',
    }
    AA_NONE = 0
    AA_LABEL = 1
    AA_SHORTCUT = 2
    AA_TOOLTIP = 3
    AA_ICON = 4
    AA_STATE = 5
    AA_CHECKABLE = 6
    AA_CHECKED = 7
    AA_VISIBILITY = 8
    action_attr_t = ctypes.c_uint32 # enum
    argloc_type_t = ctypes.c_int32
    
    # values for enumeration 'choose_type_t'
    choose_type_t__enumvalues = {
        0: 'chtype_generic',
        1: 'chtype_idasgn',
        2: 'chtype_entry',
        3: 'chtype_name',
        4: 'chtype_stkvar_xref',
        5: 'chtype_xref',
        6: 'chtype_enum',
        7: 'chtype_enum_by_value',
        8: 'chtype_func',
        9: 'chtype_segm',
        10: 'chtype_struc',
        11: 'chtype_strpath',
        12: 'chtype_idatil',
        13: 'chtype_enum_by_value_and_size',
        14: 'chtype_srcp',
    }
    chtype_generic = 0
    chtype_idasgn = 1
    chtype_entry = 2
    chtype_name = 3
    chtype_stkvar_xref = 4
    chtype_xref = 5
    chtype_enum = 6
    chtype_enum_by_value = 7
    chtype_func = 8
    chtype_segm = 9
    chtype_struc = 10
    chtype_strpath = 11
    chtype_idatil = 12
    chtype_enum_by_value_and_size = 13
    chtype_srcp = 14
    choose_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'demreq_type_t'
    demreq_type_t__enumvalues = {
        4294967288: 'DQT_NPURGED_8',
        4294967292: 'DQT_NPURGED_4',
        4294967294: 'DQT_NPURGED_2',
        0: 'DQT_COMPILER',
        1: 'DQT_NAME_TYPE',
        2: 'DQT_FULL',
    }
    DQT_NPURGED_8 = 4294967288
    DQT_NPURGED_4 = 4294967292
    DQT_NPURGED_2 = 4294967294
    DQT_COMPILER = 0
    DQT_NAME_TYPE = 1
    DQT_FULL = 2
    demreq_type_t = ctypes.c_uint32 # enum
    layout_type_t = ctypes.c_int32
    
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
    
    # values for enumeration 'regval_type_t'
    regval_type_t__enumvalues = {
        0: 'reg_unknown',
        1: 'reg_sz',
        3: 'reg_binary',
        4: 'reg_dword',
    }
    reg_unknown = 0
    reg_sz = 1
    reg_binary = 3
    reg_dword = 4
    regval_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'resume_mode_t'
    resume_mode_t__enumvalues = {
        0: 'RESMOD_NONE',
        1: 'RESMOD_INTO',
        2: 'RESMOD_OVER',
        3: 'RESMOD_OUT',
        4: 'RESMOD_SRCINTO',
        5: 'RESMOD_SRCOVER',
        6: 'RESMOD_SRCOUT',
        7: 'RESMOD_USER',
        8: 'RESMOD_HANDLE',
        9: 'RESMOD_MAX',
    }
    RESMOD_NONE = 0
    RESMOD_INTO = 1
    RESMOD_OVER = 2
    RESMOD_OUT = 3
    RESMOD_SRCINTO = 4
    RESMOD_SRCOVER = 5
    RESMOD_SRCOUT = 6
    RESMOD_USER = 7
    RESMOD_HANDLE = 8
    RESMOD_MAX = 9
    resume_mode_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'struc_error_t'
    struc_error_t__enumvalues = {
        0: 'STRUC_ERROR_MEMBER_OK',
        4294967295: 'STRUC_ERROR_MEMBER_NAME',
        4294967294: 'STRUC_ERROR_MEMBER_OFFSET',
        4294967293: 'STRUC_ERROR_MEMBER_SIZE',
        4294967292: 'STRUC_ERROR_MEMBER_TINFO',
        4294967291: 'STRUC_ERROR_MEMBER_STRUCT',
        4294967290: 'STRUC_ERROR_MEMBER_UNIVAR',
        4294967289: 'STRUC_ERROR_MEMBER_VARLAST',
        4294967288: 'STRUC_ERROR_MEMBER_NESTED',
    }
    STRUC_ERROR_MEMBER_OK = 0
    STRUC_ERROR_MEMBER_NAME = 4294967295
    STRUC_ERROR_MEMBER_OFFSET = 4294967294
    STRUC_ERROR_MEMBER_SIZE = 4294967293
    STRUC_ERROR_MEMBER_TINFO = 4294967292
    STRUC_ERROR_MEMBER_STRUCT = 4294967291
    STRUC_ERROR_MEMBER_UNIVAR = 4294967290
    STRUC_ERROR_MEMBER_VARLAST = 4294967289
    STRUC_ERROR_MEMBER_NESTED = 4294967288
    struc_error_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'tty_control_t'
    tty_control_t__enumvalues = {
        0: 'TCT_UNKNOWN',
        1: 'TCT_OWNER',
        2: 'TCT_NOT_OWNER',
    }
    TCT_UNKNOWN = 0
    TCT_OWNER = 1
    TCT_NOT_OWNER = 2
    tty_control_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'update_type_t'
    update_type_t__enumvalues = {
        0: 'UTP_ENUM',
        1: 'UTP_STRUCT',
    }
    UTP_ENUM = 0
    UTP_STRUCT = 1
    update_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'dirtree_id_t'
    dirtree_id_t__enumvalues = {
        0: 'DIRTREE_LOCAL_TYPES',
        1: 'DIRTREE_STRUCTS',
        2: 'DIRTREE_ENUMS',
        3: 'DIRTREE_FUNCS',
        4: 'DIRTREE_NAMES',
        5: 'DIRTREE_IMPORTS',
        6: 'DIRTREE_IDAPLACE_BOOKMARKS',
        7: 'DIRTREE_STRUCTS_BOOKMARKS',
        8: 'DIRTREE_ENUMS_BOOKMARKS',
        9: 'DIRTREE_BPTS',
        10: 'DIRTREE_END',
    }
    DIRTREE_LOCAL_TYPES = 0
    DIRTREE_STRUCTS = 1
    DIRTREE_ENUMS = 2
    DIRTREE_FUNCS = 3
    DIRTREE_NAMES = 4
    DIRTREE_IMPORTS = 5
    DIRTREE_IDAPLACE_BOOKMARKS = 6
    DIRTREE_STRUCTS_BOOKMARKS = 7
    DIRTREE_ENUMS_BOOKMARKS = 8
    DIRTREE_BPTS = 9
    DIRTREE_END = 10
    dirtree_id_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'frame_part_t'
    frame_part_t__enumvalues = {
        0: 'FPC_ARGS',
        1: 'FPC_RETADDR',
        2: 'FPC_SAVREGS',
        3: 'FPC_LVARS',
    }
    FPC_ARGS = 0
    FPC_RETADDR = 1
    FPC_SAVREGS = 2
    FPC_LVARS = 3
    frame_part_t = ctypes.c_uint32 # enum
    is_pattern_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_switch_info_t), ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_procmod_t))
    
    # values for enumeration 'lecvt_code_t'
    lecvt_code_t__enumvalues = {
        4294967295: 'LECVT_CANCELED',
        0: 'LECVT_ERROR',
        1: 'LECVT_OK',
    }
    LECVT_CANCELED = 4294967295
    LECVT_ERROR = 0
    LECVT_OK = 1
    lecvt_code_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'ofile_type_t'
    ofile_type_t__enumvalues = {
        0: 'OFILE_MAP',
        1: 'OFILE_EXE',
        2: 'OFILE_IDC',
        3: 'OFILE_LST',
        4: 'OFILE_ASM',
        5: 'OFILE_DIF',
    }
    OFILE_MAP = 0
    OFILE_EXE = 1
    OFILE_IDC = 2
    OFILE_LST = 3
    OFILE_ASM = 4
    OFILE_DIF = 5
    ofile_type_t = ctypes.c_uint32 # enum
    qsemaphore_t = ctypes.POINTER(struct___qsemaphore_t)
    
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
    
    # values for enumeration 'tinfo_code_t'
    tinfo_code_t__enumvalues = {
        0: 'TERR_OK',
        4294967295: 'TERR_SAVE',
        4294967294: 'TERR_SERIALIZE',
        4294967293: 'TERR_WRONGNAME',
        4294967292: 'TERR_BADSYNC',
    }
    TERR_OK = 0
    TERR_SAVE = 4294967295
    TERR_SERIALIZE = 4294967294
    TERR_WRONGNAME = 4294967293
    TERR_BADSYNC = 4294967292
    tinfo_code_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'edge_type_t'
    edge_type_t__enumvalues = {
        0: 'edge_error',
        1: 'edge_tree',
        2: 'edge_forward',
        3: 'edge_back',
        4: 'edge_cross',
        5: 'edge_subgraph',
    }
    edge_error = 0
    edge_tree = 1
    edge_forward = 2
    edge_back = 3
    edge_cross = 4
    edge_subgraph = 5
    edge_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'hook_type_t'
    hook_type_t__enumvalues = {
        0: 'HT_IDP',
        1: 'HT_UI',
        2: 'HT_DBG',
        3: 'HT_IDB',
        4: 'HT_DEV',
        5: 'HT_VIEW',
        6: 'HT_OUTPUT',
        7: 'HT_GRAPH',
        8: 'HT_IDD',
        9: 'HT_LAST',
    }
    HT_IDP = 0
    HT_UI = 1
    HT_DBG = 2
    HT_IDB = 3
    HT_DEV = 4
    HT_VIEW = 5
    HT_OUTPUT = 6
    HT_GRAPH = 7
    HT_IDD = 8
    HT_LAST = 9
    hook_type_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'mbox_kind_t'
    mbox_kind_t__enumvalues = {
        0: 'mbox_internal',
        1: 'mbox_info',
        2: 'mbox_warning',
        3: 'mbox_error',
        4: 'mbox_nomem',
        5: 'mbox_feedback',
        6: 'mbox_readerror',
        7: 'mbox_writeerror',
        8: 'mbox_filestruct',
        9: 'mbox_wait',
        10: 'mbox_hide',
        11: 'mbox_replace',
    }
    mbox_internal = 0
    mbox_info = 1
    mbox_warning = 2
    mbox_error = 3
    mbox_nomem = 4
    mbox_feedback = 5
    mbox_readerror = 6
    mbox_writeerror = 7
    mbox_filestruct = 8
    mbox_wait = 9
    mbox_hide = 10
    mbox_replace = 11
    mbox_kind_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'path_type_t'
    path_type_t__enumvalues = {
        0: 'PATH_TYPE_CMD',
        1: 'PATH_TYPE_IDB',
        2: 'PATH_TYPE_ID0',
    }
    PATH_TYPE_CMD = 0
    PATH_TYPE_IDB = 1
    PATH_TYPE_ID0 = 2
    path_type_t = ctypes.c_uint32 # enum
    type_sign_t = ctypes.c_int32
    
    # values for enumeration 'ucdr_kind_t'
    ucdr_kind_t__enumvalues = {
        1: 'UCDR_STRLIT',
        2: 'UCDR_NAME',
        4: 'UCDR_MANGLED',
        8: 'UCDR_TYPE',
    }
    UCDR_STRLIT = 1
    UCDR_NAME = 2
    UCDR_MANGLED = 4
    UCDR_TYPE = 8
    ucdr_kind_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'gtd_func_t'
    gtd_func_t__enumvalues = {
        0: 'GTD_CALC_ARGLOCS',
        128: 'GTD_NO_ARGLOCS',
    }
    GTD_CALC_ARGLOCS = 0
    GTD_NO_ARGLOCS = 128
    gtd_func_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'gts_code_t'
    gts_code_t__enumvalues = {
        1: 'GTS_NESTED',
        2: 'GTS_BASECLASS',
    }
    GTS_NESTED = 1
    GTS_BASECLASS = 2
    gts_code_t = ctypes.c_uint32 # enum
    idastate_t = ctypes.c_int32
    
    # values for enumeration 'nametype_t'
    nametype_t__enumvalues = {
        6: 'VNT_IDENT',
        8: 'VNT_TYPE',
        2: 'VNT_UDTMEM',
        1: 'VNT_STRLIT',
        2: 'VNT_VISIBLE',
    }
    VNT_IDENT = 6
    VNT_TYPE = 8
    VNT_UDTMEM = 2
    VNT_STRLIT = 1
    VNT_VISIBLE = 2
    nametype_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'smt_code_t'
    smt_code_t__enumvalues = {
        4294967290: 'SMT_BADARG',
        4294967291: 'SMT_NOCOMPAT',
        4294967292: 'SMT_WORSE',
        4294967293: 'SMT_SIZE',
        4294967294: 'SMT_ARRAY',
        4294967295: 'SMT_OVERLAP',
        0: 'SMT_FAILED',
        1: 'SMT_OK',
        2: 'SMT_KEEP',
    }
    SMT_BADARG = 4294967290
    SMT_NOCOMPAT = 4294967291
    SMT_WORSE = 4294967292
    SMT_SIZE = 4294967293
    SMT_ARRAY = 4294967294
    SMT_OVERLAP = 4294967295
    SMT_FAILED = 0
    SMT_OK = 1
    SMT_KEEP = 2
    smt_code_t = ctypes.c_uint32 # enum
    bpttype_t = ctypes.c_int32
    diffpos_t = ctypes.c_uint64
    
    # values for enumeration 'gdecode_t'
    gdecode_t__enumvalues = {
        4294967295: 'GDE_ERROR',
        0: 'GDE_NO_EVENT',
        1: 'GDE_ONE_EVENT',
        2: 'GDE_MANY_EVENTS',
    }
    GDE_ERROR = 4294967295
    GDE_NO_EVENT = 0
    GDE_ONE_EVENT = 1
    GDE_MANY_EVENTS = 2
    gdecode_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'gtd_udt_t'
    gtd_udt_t__enumvalues = {
        0: 'GTD_CALC_LAYOUT',
        128: 'GTD_NO_LAYOUT',
        64: 'GTD_DEL_BITFLDS',
    }
    GTD_CALC_LAYOUT = 0
    GTD_NO_LAYOUT = 128
    GTD_DEL_BITFLDS = 64
    gtd_udt_t = ctypes.c_uint32 # enum
    printer_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p)
    qhandle_t = ctypes.POINTER(None)
    qthread_t = ctypes.POINTER(struct___qthread_t)
    ulonglong = ctypes.c_uint64
    wchar16_t = ctypes.c_int16
    hexdsp_t = ctypes.CFUNCTYPE(ctypes.POINTER(None), ctypes.c_int32)
    
    # values for enumeration 'inftag_t'
    inftag_t__enumvalues = {
        0: 'INF_VERSION',
        1: 'INF_PROCNAME',
        2: 'INF_GENFLAGS',
        3: 'INF_LFLAGS',
        4: 'INF_DATABASE_CHANGE_COUNT',
        5: 'INF_FILETYPE',
        6: 'INF_OSTYPE',
        7: 'INF_APPTYPE',
        8: 'INF_ASMTYPE',
        9: 'INF_SPECSEGS',
        10: 'INF_AF',
        11: 'INF_AF2',
        12: 'INF_BASEADDR',
        13: 'INF_START_SS',
        14: 'INF_START_CS',
        15: 'INF_START_IP',
        16: 'INF_START_EA',
        17: 'INF_START_SP',
        18: 'INF_MAIN',
        19: 'INF_MIN_EA',
        20: 'INF_MAX_EA',
        21: 'INF_OMIN_EA',
        22: 'INF_OMAX_EA',
        23: 'INF_LOWOFF',
        24: 'INF_HIGHOFF',
        25: 'INF_MAXREF',
        26: 'INF_PRIVRANGE',
        27: 'INF_PRIVRANGE_START_EA',
        28: 'INF_PRIVRANGE_END_EA',
        29: 'INF_NETDELTA',
        30: 'INF_XREFNUM',
        31: 'INF_TYPE_XREFNUM',
        32: 'INF_REFCMTNUM',
        33: 'INF_XREFFLAG',
        34: 'INF_MAX_AUTONAME_LEN',
        35: 'INF_NAMETYPE',
        36: 'INF_SHORT_DEMNAMES',
        37: 'INF_LONG_DEMNAMES',
        38: 'INF_DEMNAMES',
        39: 'INF_LISTNAMES',
        40: 'INF_INDENT',
        41: 'INF_CMT_INDENT',
        42: 'INF_MARGIN',
        43: 'INF_LENXREF',
        44: 'INF_OUTFLAGS',
        45: 'INF_CMTFLG',
        46: 'INF_LIMITER',
        47: 'INF_BIN_PREFIX_SIZE',
        48: 'INF_PREFFLAG',
        49: 'INF_STRLIT_FLAGS',
        50: 'INF_STRLIT_BREAK',
        51: 'INF_STRLIT_ZEROES',
        52: 'INF_STRTYPE',
        53: 'INF_STRLIT_PREF',
        54: 'INF_STRLIT_SERNUM',
        55: 'INF_DATATYPES',
        56: 'INF_CC',
        57: 'INF_CC_ID',
        58: 'INF_CC_CM',
        59: 'INF_CC_SIZE_I',
        60: 'INF_CC_SIZE_B',
        61: 'INF_CC_SIZE_E',
        62: 'INF_CC_DEFALIGN',
        63: 'INF_CC_SIZE_S',
        64: 'INF_CC_SIZE_L',
        65: 'INF_CC_SIZE_LL',
        66: 'INF_CC_SIZE_LDBL',
        67: 'INF_ABIBITS',
        68: 'INF_APPCALL_OPTIONS',
        69: 'INF_FILE_FORMAT_NAME',
        70: 'INF_GROUPS',
        71: 'INF_H_PATH',
        72: 'INF_C_MACROS',
        73: 'INF_INCLUDE',
        74: 'INF_DUALOP_GRAPH',
        75: 'INF_DUALOP_TEXT',
        76: 'INF_MD5',
        77: 'INF_IDA_VERSION',
        78: 'INF_STR_ENCODINGS',
        79: 'INF_DBG_BINPATHS',
        80: 'INF_SHA256',
        81: 'INF_ABINAME',
        82: 'INF_ARCHIVE_PATH',
        83: 'INF_PROBLEMS',
        84: 'INF_SELECTORS',
        85: 'INF_NOTEPAD',
        86: 'INF_SRCDBG_PATHS',
        87: 'INF_SRCDBG_UNDESIRED',
        88: 'INF_INITIAL_VERSION',
        89: 'INF_CTIME',
        90: 'INF_ELAPSED',
        91: 'INF_NOPENS',
        92: 'INF_CRC32',
        93: 'INF_IMAGEBASE',
        94: 'INF_IDSNODE',
        95: 'INF_FSIZE',
        96: 'INF_OUTFILEENC',
        97: 'INF_INPUT_FILE_PATH',
        98: 'INF_LAST',
    }
    INF_VERSION = 0
    INF_PROCNAME = 1
    INF_GENFLAGS = 2
    INF_LFLAGS = 3
    INF_DATABASE_CHANGE_COUNT = 4
    INF_FILETYPE = 5
    INF_OSTYPE = 6
    INF_APPTYPE = 7
    INF_ASMTYPE = 8
    INF_SPECSEGS = 9
    INF_AF = 10
    INF_AF2 = 11
    INF_BASEADDR = 12
    INF_START_SS = 13
    INF_START_CS = 14
    INF_START_IP = 15
    INF_START_EA = 16
    INF_START_SP = 17
    INF_MAIN = 18
    INF_MIN_EA = 19
    INF_MAX_EA = 20
    INF_OMIN_EA = 21
    INF_OMAX_EA = 22
    INF_LOWOFF = 23
    INF_HIGHOFF = 24
    INF_MAXREF = 25
    INF_PRIVRANGE = 26
    INF_PRIVRANGE_START_EA = 27
    INF_PRIVRANGE_END_EA = 28
    INF_NETDELTA = 29
    INF_XREFNUM = 30
    INF_TYPE_XREFNUM = 31
    INF_REFCMTNUM = 32
    INF_XREFFLAG = 33
    INF_MAX_AUTONAME_LEN = 34
    INF_NAMETYPE = 35
    INF_SHORT_DEMNAMES = 36
    INF_LONG_DEMNAMES = 37
    INF_DEMNAMES = 38
    INF_LISTNAMES = 39
    INF_INDENT = 40
    INF_CMT_INDENT = 41
    INF_MARGIN = 42
    INF_LENXREF = 43
    INF_OUTFLAGS = 44
    INF_CMTFLG = 45
    INF_LIMITER = 46
    INF_BIN_PREFIX_SIZE = 47
    INF_PREFFLAG = 48
    INF_STRLIT_FLAGS = 49
    INF_STRLIT_BREAK = 50
    INF_STRLIT_ZEROES = 51
    INF_STRTYPE = 52
    INF_STRLIT_PREF = 53
    INF_STRLIT_SERNUM = 54
    INF_DATATYPES = 55
    INF_CC = 56
    INF_CC_ID = 57
    INF_CC_CM = 58
    INF_CC_SIZE_I = 59
    INF_CC_SIZE_B = 60
    INF_CC_SIZE_E = 61
    INF_CC_DEFALIGN = 62
    INF_CC_SIZE_S = 63
    INF_CC_SIZE_L = 64
    INF_CC_SIZE_LL = 65
    INF_CC_SIZE_LDBL = 66
    INF_ABIBITS = 67
    INF_APPCALL_OPTIONS = 68
    INF_FILE_FORMAT_NAME = 69
    INF_GROUPS = 70
    INF_H_PATH = 71
    INF_C_MACROS = 72
    INF_INCLUDE = 73
    INF_DUALOP_GRAPH = 74
    INF_DUALOP_TEXT = 75
    INF_MD5 = 76
    INF_IDA_VERSION = 77
    INF_STR_ENCODINGS = 78
    INF_DBG_BINPATHS = 79
    INF_SHA256 = 80
    INF_ABINAME = 81
    INF_ARCHIVE_PATH = 82
    INF_PROBLEMS = 83
    INF_SELECTORS = 84
    INF_NOTEPAD = 85
    INF_SRCDBG_PATHS = 86
    INF_SRCDBG_UNDESIRED = 87
    INF_INITIAL_VERSION = 88
    INF_CTIME = 89
    INF_ELAPSED = 90
    INF_NOPENS = 91
    INF_CRC32 = 92
    INF_IMAGEBASE = 93
    INF_IDSNODE = 94
    INF_FSIZE = 95
    INF_OUTFILEENC = 96
    INF_INPUT_FILE_PATH = 97
    INF_LAST = 98
    inftag_t = ctypes.c_uint32 # enum
    longlong = ctypes.c_int64
    qmutex_t = ctypes.POINTER(struct___qmutex_t)
    qtimer_t = ctypes.POINTER(struct___qtimer_t)
    regoff_t = ctypes.c_int32
    
    # values for enumeration 'sclass_t'
    sclass_t__enumvalues = {
        0: 'sc_unk',
        1: 'sc_type',
        2: 'sc_ext',
        3: 'sc_stat',
        4: 'sc_reg',
        5: 'sc_auto',
        6: 'sc_friend',
        7: 'sc_virt',
    }
    sc_unk = 0
    sc_type = 1
    sc_ext = 2
    sc_stat = 3
    sc_reg = 4
    sc_auto = 5
    sc_friend = 6
    sc_virt = 7
    sclass_t = ctypes.c_uint32 # enum
    atype_t = ctypes.c_int32
    
    # values for enumeration 'dterr_t'
    dterr_t__enumvalues = {
        0: 'DTE_OK',
        1: 'DTE_ALREADY_EXISTS',
        2: 'DTE_NOT_FOUND',
        3: 'DTE_NOT_DIRECTORY',
        4: 'DTE_NOT_EMPTY',
        5: 'DTE_BAD_PATH',
        6: 'DTE_CANT_RENAME',
        7: 'DTE_OWN_CHILD',
        8: 'DTE_MAX_DIR',
        9: 'DTE_LAST',
    }
    DTE_OK = 0
    DTE_ALREADY_EXISTS = 1
    DTE_NOT_FOUND = 2
    DTE_NOT_DIRECTORY = 3
    DTE_NOT_EMPTY = 4
    DTE_BAD_PATH = 5
    DTE_CANT_RENAME = 6
    DTE_OWN_CHILD = 7
    DTE_MAX_DIR = 8
    DTE_LAST = 9
    dterr_t = ctypes.c_uint32 # enum
    error_t = ctypes.c_int32
    ssize_t = ctypes.c_int64
    
    # values for enumeration 'beep_t'
    beep_t__enumvalues = {
        0: 'beep_default',
    }
    beep_default = 0
    beep_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'cref_t'
    cref_t__enumvalues = {
        0: 'fl_U',
        16: 'fl_CF',
        17: 'fl_CN',
        18: 'fl_JF',
        19: 'fl_JN',
        20: 'fl_USobsolete',
        21: 'fl_F',
    }
    fl_U = 0
    fl_CF = 16
    fl_CN = 17
    fl_JF = 18
    fl_JN = 19
    fl_USobsolete = 20
    fl_F = 21
    cref_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'dref_t'
    dref_t__enumvalues = {
        0: 'dr_U',
        1: 'dr_O',
        2: 'dr_W',
        3: 'dr_R',
        4: 'dr_T',
        5: 'dr_I',
        6: 'dr_S',
    }
    dr_U = 0
    dr_O = 1
    dr_W = 2
    dr_R = 3
    dr_T = 4
    dr_I = 5
    dr_S = 6
    dref_t = ctypes.c_uint32 # enum
    help_t = ctypes.c_int32
    thid_t = ctypes.c_int32
    uint16 = ctypes.c_uint16
    uint32 = ctypes.c_uint32
    ushort = ctypes.c_uint16
    
    # values for enumeration 'abs_t'
    abs_t__enumvalues = {
        0: 'abs_unk',
        1: 'abs_no',
        2: 'abs_yes',
    }
    abs_unk = 0
    abs_no = 1
    abs_yes = 2
    abs_t = ctypes.c_uint32 # enum
    
    # values for enumeration 'cb_id'
    cb_id__enumvalues = {
        4294967295: 'CB_INIT',
        4294967294: 'CB_YES',
        4294967293: 'CB_CLOSE',
        4294967292: 'CB_INVISIBLE',
        4294967291: 'CB_DESTROYING',
    }
    CB_INIT = 4294967295
    CB_YES = 4294967294
    CB_CLOSE = 4294967293
    CB_INVISIBLE = 4294967292
    CB_DESTROYING = 4294967291
    cb_id = ctypes.c_uint32 # enum
    
    # values for enumeration 'drc_t'
    drc_t__enumvalues = {
        3: 'DRC_EVENTS',
        2: 'DRC_CRC',
        1: 'DRC_OK',
        0: 'DRC_NONE',
        4294967295: 'DRC_FAILED',
        4294967294: 'DRC_NETERR',
        4294967293: 'DRC_NOFILE',
        4294967292: 'DRC_IDBSEG',
        4294967291: 'DRC_NOPROC',
        4294967290: 'DRC_NOCHG',
        4294967289: 'DRC_ERROR',
    }
    DRC_EVENTS = 3
    DRC_CRC = 2
    DRC_OK = 1
    DRC_NONE = 0
    DRC_FAILED = 4294967295
    DRC_NETERR = 4294967294
    DRC_NOFILE = 4294967293
    DRC_IDBSEG = 4294967292
    DRC_NOPROC = 4294967291
    DRC_NOCHG = 4294967290
    DRC_ERROR = 4294967289
    drc_t = ctypes.c_uint32 # enum
    int16 = ctypes.c_int16
    int32 = ctypes.c_int32
    pid_t = ctypes.c_int32
    sint8 = ctypes.c_char
    uchar = ctypes.c_ubyte
    uint8 = ctypes.c_ubyte
    int8 = ctypes.c_char
    uint = ctypes.c_uint32
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____value_compare = struct_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___value_compare
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____size_type = ctypes.c_uint64
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____key_type = ctypes.c_uint64
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Alnode = struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P__
    std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__
    std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___key_compare = struct_std__less_unsigned_long_long_
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______difference_type = ctypes.c_int64
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____value_compare = struct_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___value_compare
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____size_type = ctypes.c_uint64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______difference_type = ctypes.c_int64
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Alnode = struct_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P__
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____value_compare = struct_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___value_compare
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____size_type = ctypes.c_uint64
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___allocator_type = struct_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____key_type = ctypes.c_uint64
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Alnode = struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P__
    std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___key_compare = struct_std__less__qstring_char__
    std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long__
    std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___key_compare = struct_std__less_unsigned_long_long_
    std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________difference_type = ctypes.c_int64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______difference_type = ctypes.c_int64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________difference_type = ctypes.c_int64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______difference_type = ctypes.c_int64
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____size_type = ctypes.c_uint64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______difference_type = ctypes.c_int64
    std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______difference_type = ctypes.c_int64
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____value_compare = struct_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___value_compare
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____size_type = ctypes.c_uint64
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____key_type = ctypes.c_int32
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Alnode = struct_std__allocator_std___Tree_node_std__pair_const_int__int___void__P__
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______size_type = ctypes.c_uint64
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______difference_type = ctypes.c_int64
    std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___allocator_type = struct_std__allocator_std__pair_const_int__int__
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____size_type = ctypes.c_uint64
    std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___key_compare = struct_std__less_int_
    std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___value_type = struct_std__pair_const_int__int_
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______reference = ctypes.POINTER(ctypes.c_int32)
    std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___key_compare = struct_std__less_unsigned_long_long_
    std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____value_type = ctypes.c_int32
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____size_type = ctypes.c_uint64
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____key_type = ctypes.c_int32
    std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Alnode = struct_std__allocator_std___Tree_node_int__void__P__
    qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R____const_iterator = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(syntax_highlight_style), ctypes.POINTER(struct__qstring_char_))
    std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tset_traits_int__std__less_int___std__allocator_int___false___allocator_type = struct_std__allocator_int_
    qvector_long_long___P__syntax_highlight_style__P__const_char__P____const_iterator = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(syntax_highlight_style), ctypes.c_char_p)
    qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R____iterator = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(syntax_highlight_style), ctypes.POINTER(struct__qstring_char_))
    std___Tset_traits_int__std__less_int___std__allocator_int___false___key_compare = struct_std__less_int_
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____size_type = ctypes.c_uint64
    qvector_long_long___P__syntax_highlight_style__P__const_char__P____iterator = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(syntax_highlight_style), ctypes.c_char_p)
    std__map__qstring_char___qrefcnt_t_refcnted_regex_t____key_compare = struct_std__less__qstring_char__
    std__map__qstring_char___qrefcnt_t_refcnted_regex_t____mapped_type = struct_qrefcnt_t_refcnted_regex_t_
    std___Tree_node_std__pair_const_int__int___void__P____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std__map_unsigned_long_long__unsigned_long_long___key_compare = struct_std__less_unsigned_long_long_
    std___Simple_types_std__pair_const_int__int____value_type = struct_std__pair_const_int__int_
    std___Tree_val_std___Tree_simple_types_int____value_type = ctypes.c_int32
    std___Tree_val_std___Tree_simple_types_int____size_type = ctypes.c_uint64
    std___Simple_types_std__pair_const_int__int____pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    class union_typedef_type_data_t___F773DD8B4C420A056648FD7EB1349F55(Union):
        pass
    
    union_typedef_type_data_t___F773DD8B4C420A056648FD7EB1349F55._pack_ = 1 # source:False
    union_typedef_type_data_t___F773DD8B4C420A056648FD7EB1349F55._fields_ = [
        ('name', ctypes.c_char_p),
        ('ordinal', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_op_t___9FE5DDDE6246481B3EE86C7EEB25DDF5(Union):
        pass
    
    union_op_t___9FE5DDDE6246481B3EE86C7EEB25DDF5._pack_ = 1 # source:False
    union_op_t___9FE5DDDE6246481B3EE86C7EEB25DDF5._fields_ = [
        ('reg', ctypes.c_uint16),
        ('phrase', ctypes.c_uint16),
    ]
    
    std___Tree_node_int__void__P____Nodeptr = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    qvector_movbpt_code_t___const_iterator = ctypes.POINTER(movbpt_code_t)
    std___Simple_types_int___const_pointer = ctypes.POINTER(ctypes.c_int32)
    _486A9EF9057A4F79C352527BA63EDFD3 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t))
    _5199E2C0DF2CA3E7E8DCA56464B8E928 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_uint32, ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(None))
    _C09AF1331CFCFC509FB4233AA5230FB3 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(None), ctypes.c_int32, ctypes.POINTER(ctypes.POINTER(None)))
    qvector_movbpt_code_t___iterator = ctypes.POINTER(movbpt_code_t)
    std__map_int__int___key_compare = struct_std__less_int_
    screen_graph_selection_base_t = struct_qvector_selection_item_t_
    jump_pattern_t__check_insn_t = struct__C21FB2E1BAA97F44BFD298211C4C916B
    rangeset_t__const_iterator = ctypes.POINTER(struct_range_t)
    std__set_int___key_compare = struct_std__less_int_
    _source_file_iterator = struct_qiterator_qrefcnt_t_source_file_t__
    _source_item_iterator = struct_qiterator_qrefcnt_t_source_item_t__
    compiled_binpat_vec_t = struct_qvector_compiled_binpat_t_
    dirtree_cursor_vec_t = struct_qvector_dirtree_cursor_t_
    rangeset_t__iterator = ctypes.POINTER(struct_range_t)
    section_lines_refs_t = struct_qvector_const_twinline_t__P_
    segm_move_info_vec_t = struct_qvector_segm_move_info_t_
    source_file_iterator = struct_qrefcnt_t_qiterator_qrefcnt_t_source_file_t___
    source_item_iterator = struct_qrefcnt_t_qiterator_qrefcnt_t_source_item_t___
    array_of_node_set_t = struct_qvector_node_set_t_
    lochist_entry_vec_t = struct_qvector_lochist_entry_t_
    array_of_rangesets = struct_qvector_rangeset_t_
    bpt_constptr_vec_t = struct_qvector_const_bpt_t__P_
    rangeset_crefvec_t = struct_qvector_const_rangeset_t__P_
    refinfo_desc_vec_t = struct_qvector_refinfo_desc_t_
    view_event_state_t = ctypes.c_int32
    array_of_intmap_t = struct_qvector_intmap_t_
    enum_member_vec_t = struct_qvector_enum_member_t_
    scattered_image_t = struct_qvector_scattered_segm_t_
    sync_source_vec_t = struct_qvector_sync_source_t_
    thread_name_vec_t = struct_qvector_thread_name_t_
    channel_redirs_t = struct_qvector_channel_redir_t_
    extlang_object_t = struct_qrefcnt_t_extlang_t_
    graph_row_info_t = struct_qvector_row_info_t_
    groups_crinfos_t = struct_qvector_group_crinfo_t_
    linput_janitor_t = struct_janitor_t_linput_t__P_
    reg_access_vec_t = struct_qvector_reg_access_t_
    tevinforeg_vec_t = struct_qvector_tev_info_reg_t_
    update_bpt_vec_t = struct_qvector_update_bpt_info_t_
    lx_parse_cast_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_cast_t), ctypes.POINTER(struct_token_t))
    rangevec_base_t = struct_qvector_range_t_
    simd_info_vec_t = struct_qvector_simd_info_t_
    source_file_ptr = struct_qrefcnt_t_source_file_t_
    source_item_ptr = struct_qrefcnt_t_source_item_t_
    direntry_vec_t = struct_qvector_direntry_t_
    file_janitor_t = struct_janitor_t__iobuf__P_
    graph_viewer_t = struct_TWidget
    memreg_infos_t = struct_qvector_memreg_info_t_
    movbpt_codes_t = struct_qvector_movbpt_code_t_
    movbpt_infos_t = struct_qvector_movbpt_info_t_
    procinfo_vec_t = struct_qvector_process_info_t_
    source_items_t = struct_qvector_qrefcnt_t_source_item_t__
    ea_name_vec_t = struct_qvector_ea_name_t_
    meminfo_vec_t = struct_qvector_memory_info_t_
    problist_id_t = ctypes.c_ubyte
    tevinfo_vec_t = struct_qvector_tev_info_t_
    argpartvec_t = struct_qvector_argpart_t_
    bptptr_vec_t = struct_qvector_bpt_t__P_
    dbgevt_vec_t = struct_qvector_debug_event_t_
    fixup_type_t = ctypes.c_uint16
    funcargvec_t = struct_qvector_funcarg_t_
    lowcnd_vec_t = struct_qvector_lowcnd_t_
    modinfovec_t = struct_qvector_modinfo_t_
    tokenstack_t = struct_qstack_token_t_
    type_attrs_t = struct_qvector_type_attr_t_
    idp_descs_t = struct_qvector_idp_desc_t_
    regex_ptr_t = struct_qrefcnt_t_refcnted_regex_t_
    regobjvec_t = struct_qvector_regobj_t_
    valstrvec_t = struct_qvector_valstr_t_
    catchvec_t = struct_qvector_catch_t_
    extlangs_t = struct_qvector_extlang_t__P_
    idc_vars_t = struct_qvector_idc_global_t_
    inodevec_t = struct_qvector_unsigned_long_long_
    op_dtype_t = ctypes.c_ubyte
    pointvec_t = struct_qvector_point_t_
    qwstrvec_t = struct_qvector__qstring_wchar_t__
    tinfovec_t = struct_qvector_tinfo_t_
    xreflist_t = struct_qvector_xreflist_entry_t_
    arglocs_t = struct_qvector_argloc_t_
    bgcolor_t = ctypes.c_uint32
    boolvec_t = struct_qvector_bool_
    bpt_vec_t = struct_qvector_bpt_t_
    casevec_t = struct_qvector_qvector_long_long__
    compvec_t = struct_qvector_unsigned_char_
    edgevec_t = struct_qvector_edge_t_
    ioports_t = struct_qvector_ioport_t_
    qtime32_t = ctypes.c_int32
    reftype_t = ctypes.c_ubyte
    regvals_t = struct_qvector_regval_t_
    svalvec_t = struct_qvector_long_long_
    tryblks_t = struct_qvector_tryblk_t_
    uvalvec_t = struct_qvector_unsigned_long_long_
    wchar32_t = ctypes.c_uint32
    bpteas_t = struct_qvector_bptaddrs_t_
    dirvec_t = struct_qvector_unsigned_long_long_
    excvec_t = struct_qvector_exception_info_t_
    fixups_t = struct_qvector_fixup_info_t_
    optype_t = ctypes.c_ubyte
    ordvec_t = struct_qvector_unsigned_int_
    p_string = ctypes.c_ubyte
    qwstring = struct__qstring_wchar_t_
    strvec_t = struct_qvector_simpleline_t_
    color_t = ctypes.c_ubyte
    flags_t = ctypes.c_uint32
    comp_t = ctypes.c_ubyte
    lxtype = ctypes.c_uint16
    p_list = ctypes.c_ubyte
    text_t = struct_qvector_twinline_t_
    type_t = ctypes.c_ubyte
    uint64 = ctypes.c_uint64
    bte_t = ctypes.c_ubyte
    int64 = ctypes.c_int64
    qtype = struct__qstring_unsigned_char_
    sel_t = ctypes.c_uint64
    cm_t = ctypes.c_ubyte
    ea_t = ctypes.c_uint64
    eNI = ctypes.c_uint16 * 9
    class union_lex_value_t___6E94C03EE084EC1E8773E8F11C206FDC(Union):
        pass
    
    union_lex_value_t___6E94C03EE084EC1E8773E8F11C206FDC._pack_ = 1 # source:False
    union_lex_value_t___6E94C03EE084EC1E8773E8F11C206FDC._fields_ = [
        ('val', ctypes.c_int64),
        ('uval', ctypes.c_uint64),
    ]
    
    class union_token_t___EFD300335D00E904D0DC340AFA3DF967(Union):
        pass
    
    union_token_t___EFD300335D00E904D0DC340AFA3DF967._pack_ = 1 # source:False
    union_token_t___EFD300335D00E904D0DC340AFA3DF967._fields_ = [
        ('fnum', struct_fpvalue_t),
        ('i64', ctypes.c_int64),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    class union_op_t___03EE851906E7470B48652C42A8F5F22F(Union):
        pass
    
    union_op_t___03EE851906E7470B48652C42A8F5F22F._pack_ = 1 # source:False
    union_op_t___03EE851906E7470B48652C42A8F5F22F._fields_ = [
        ('specval', ctypes.c_uint64),
        ('specval_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_op_t___63479489C28A4014434636A3BFC4DC99(Union):
        pass
    
    union_op_t___63479489C28A4014434636A3BFC4DC99._pack_ = 1 # source:False
    union_op_t___63479489C28A4014434636A3BFC4DC99._fields_ = [
        ('addr', ctypes.c_uint64),
        ('addr_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    _06ACCA0CDDC5718C62D5A4485E2E115D = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct__iobuf), ctypes.POINTER(struct__qstring_char_), ctypes.c_uint32, ctypes.c_uint32)
    _47EB95A8857FB680635907AB7DCDCDE8 = ctypes.CFUNCTYPE(lecvt_code_t, ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_TWidget), ctypes.c_uint32)
    _492C834E753BED590AB0BAB80BEB78E7 = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.POINTER(syntax_highlight_style), ctypes.c_char_p)
    _94760D3F2768AB73DF4E13DC5B377508 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(syntax_highlight_style), ctypes.POINTER(struct__qstring_char_))
    class union_input_event_t___4953DA15226C435F033B39D89D558652(Union):
        pass
    
    union_input_event_t___4953DA15226C435F033B39D89D558652._pack_ = 1 # source:False
    union_input_event_t___4953DA15226C435F033B39D89D558652._fields_ = [
        ('shortcut', struct_input_event_t__input_event_shortcut_data_t),
        ('keyboard', struct_input_event_t__input_event_keyboard_data_t),
        ('mouse', struct_input_event_t__input_event_mouse_data_t),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_regval_t___E2461B07C1F03128F15079BB1FB5F381(Union):
        pass
    
    union_regval_t___E2461B07C1F03128F15079BB1FB5F381._pack_ = 1 # source:False
    union_regval_t___E2461B07C1F03128F15079BB1FB5F381._fields_ = [
        ('ival', ctypes.c_uint64),
        ('fval', struct_fpvalue_t),
        ('reserve', ctypes.c_ubyte * 24),
    ]
    
    class union_insn_t___F4FA00FEEF275F329AD5381050035CF8(Union):
        pass
    
    union_insn_t___F4FA00FEEF275F329AD5381050035CF8._pack_ = 1 # source:False
    union_insn_t___F4FA00FEEF275F329AD5381050035CF8._fields_ = [
        ('auxpref', ctypes.c_uint32),
        ('auxpref_u16', ctypes.c_uint16 * 2),
        ('auxpref_u8', ctypes.c_ubyte * 4),
    ]
    
    _5D6657710F2FD348305D4B59534642C3 = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.c_uint32, ctypes.c_char_p, ctypes.c_uint32)
    class union_jvalue_t___86FD308AB52B8F8AFE7E7C65068A43C3(Union):
        pass
    
    union_jvalue_t___86FD308AB52B8F8AFE7E7C65068A43C3._pack_ = 1 # source:False
    union_jvalue_t___86FD308AB52B8F8AFE7E7C65068A43C3._fields_ = [
        ('_num', ctypes.c_int64),
        ('_str', ctypes.POINTER(struct__qstring_char_)),
        ('_obj', ctypes.POINTER(struct_jobj_t)),
        ('_arr', ctypes.POINTER(struct_jarr_t)),
        ('_bool', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____key_compare = struct_std__less_unsigned_long_long_
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____allocator_type = struct_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____key_compare = struct_std__less__qstring_char__
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long__
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____key_compare = struct_std__less_unsigned_long_long_
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___key_type = struct__qstring_char_
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____allocator_type = struct_std__allocator_std__pair_const_int__int__
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____key_compare = struct_std__less_int_
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____value_type = struct_std__pair_const_int__int_
    std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____value_type = struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__
    std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___mapped_type = struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____allocator_type = struct_std__allocator_int_
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____value_type = ctypes.c_int32
    std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____reference = ctypes.POINTER(ctypes.c_int32)
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____key_compare = struct_std__less_int_
    std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____const_pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____Node = struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____value_type = ctypes.c_int32
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____reference = ctypes.POINTER(ctypes.c_int32)
    std___Tset_traits_int__std__less_int___std__allocator_int___false___value_compare = struct_std__less_int_
    std__allocator_std___Tree_node_std__pair_const_int__int___void__P____value_type = struct_std___Tree_node_std__pair_const_int__int___void__P_
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____value_type = struct_std__pair_const_int__int_
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std__map__qstring_char___qrefcnt_t_refcnted_regex_t____allocator_type = struct_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___
    std__map_unsigned_long_long__unsigned_long_long___allocator_type = struct_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long__
    std__map__qstring_char___qrefcnt_t_refcnted_regex_t____key_type = struct__qstring_char_
    std___Simple_types_std__pair_const_int__int____const_pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_val_std___Tree_simple_types_int____const_pointer = ctypes.POINTER(ctypes.c_int32)
    std___Tree_simple_types_std__pair_const_int__int_____Node = struct_std___Tree_node_std__pair_const_int__int___void__P_
    std__allocator_std___Tree_node_int__void__P____value_type = struct_std___Tree_node_int__void__P_
    std___Tree_simple_types_int____Node = struct_std___Tree_node_int__void__P_
    std__map_int__int___allocator_type = struct_std__allocator_std__pair_const_int__int__
    _403A3450421E1FA417431FD6F5C6B815 = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64)
    _40A15942B64B468D028A9EDC3BF273C3 = ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(None))
    _77081ABAD94FC9A5EE14B650E0DBF110 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_uint32, ctypes.POINTER(None))
    _9E76F4EBF8BA4D34546A573D2A95E8EF = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.c_uint64)
    _A2117BA638E63C1EAFEA64D9666358AE = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(None))
    std__set_int___allocator_type = struct_std__allocator_int_
    table_checker_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_switch_info_t), ctypes.c_uint64, ctypes.c_int32, ctypes.POINTER(struct_procmod_t))
    blob_idx_t = ctypes.c_uint64
    graph_id_t = ctypes.c_uint64
    nodeidx_t = ctypes.c_uint64
    qtime64_t = ctypes.c_uint64
    aflags_t = ctypes.c_uint32
    adiff_t = ctypes.c_int64
    asize_t = ctypes.c_uint64
    ea64_t = ctypes.c_uint64
    sval_t = ctypes.c_int64
    uval_t = ctypes.c_uint64
    tid_t = ctypes.c_uint64
    class union_switch_info_t___76B1A80AA47B7214ED24D33A3285D956(Union):
        pass
    
    union_switch_info_t___76B1A80AA47B7214ED24D33A3285D956._pack_ = 1 # source:False
    union_switch_info_t___76B1A80AA47B7214ED24D33A3285D956._fields_ = [
        ('values', ctypes.c_uint64),
        ('lowcase', ctypes.c_uint64),
    ]
    
    class union_op_t___1DAE607E75260845BFCA6DE571F2D359(Union):
        pass
    
    union_op_t___1DAE607E75260845BFCA6DE571F2D359._pack_ = 1 # source:False
    union_op_t___1DAE607E75260845BFCA6DE571F2D359._fields_ = [
        ('value', ctypes.c_uint64),
        ('value_shorts', struct__0B605D7B00AC5C12C153272CF5BD15AF),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    _BCFAB6CAE5EB6A58B72F2C0C12D28D2B = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_uint64, ctypes.c_char_p, ctypes.c_uint64, ctypes.POINTER(None))
    lx_resolver_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(None), ctypes.POINTER(struct_token_t), ctypes.POINTER(ctypes.c_int64))
    class union_cfgopt_t___275FC9DDBA9D1187AC5032610B4D4F63(Union):
        pass
    
    union_cfgopt_t___275FC9DDBA9D1187AC5032610B4D4F63._pack_ = 1 # source:False
    union_cfgopt_t___275FC9DDBA9D1187AC5032610B4D4F63._fields_ = [
        ('buf_size', ctypes.c_uint64),
        ('num_range', struct_cfgopt_t__num_range_t),
        ('bit_flags', ctypes.c_uint32),
        ('params', struct_cfgopt_t__params_t),
        ('mbroff_obj', ctypes.POINTER(None)),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    _5DBD8E863343736E5AD8CF23F5B72447 = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(None))
    class union_idc_value_t___D589224ACA3955A7C89073061DACDDE8(Union):
        pass
    
    union_idc_value_t___D589224ACA3955A7C89073061DACDDE8._pack_ = 1 # source:False
    union_idc_value_t___D589224ACA3955A7C89073061DACDDE8._fields_ = [
        ('num', ctypes.c_int64),
        ('e', struct_fpvalue_t),
        ('obj', ctypes.POINTER(struct_idc_object_t)),
        ('funcidx', ctypes.c_int32),
        ('pvoid', ctypes.POINTER(None)),
        ('i64', ctypes.c_int64),
        ('reserve', ctypes.c_ubyte * 24),
    ]
    
    union_value_u._pack_ = 1 # source:False
    union_value_u._fields_ = [
        ('v_char', ctypes.c_ubyte),
        ('v_short', ctypes.c_uint16),
        ('v_long', ctypes.c_uint32),
        ('v_int64', ctypes.c_uint64),
        ('v_uval', ctypes.c_uint64),
        ('_dq', struct_value_u__dq_t),
        ('dt', struct_value_u__dt_t),
        ('d128', struct_value_u__d128_t),
        ('byte16', ctypes.c_ubyte * 16),
        ('dword3', ctypes.c_uint32 * 3),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class union_callui_t(Union):
        pass
    
    union_callui_t._pack_ = 1 # source:False
    union_callui_t._fields_ = [
        ('cnd', ctypes.c_char),
        ('i8', ctypes.c_char),
        ('i', ctypes.c_int32),
        ('i16', ctypes.c_int16),
        ('i32', ctypes.c_int32),
        ('u8', ctypes.c_ubyte),
        ('u16', ctypes.c_uint16),
        ('u32', ctypes.c_uint32),
        ('cptr', ctypes.c_char_p),
        ('vptr', ctypes.POINTER(None)),
        ('ssize', ctypes.c_int64),
        ('fptr', ctypes.POINTER(struct_func_t)),
        ('segptr', ctypes.POINTER(struct_segment_t)),
        ('strptr', ctypes.POINTER(struct_struc_t)),
        ('pluginptr', ctypes.POINTER(struct_plugin_t)),
        ('sraptr', ctypes.POINTER(struct_sreg_range_t)),
    ]
    
    std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____key_type = struct__qstring_char_
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_____value_type = struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_____pointer = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type = struct_std__pair_const_unsigned_long_long__unsigned_long_long_
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type = struct_std__pair_const_int__int_
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____value_type = struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_int__int___void__P_____value_type = struct_std___Tree_node_std__pair_const_int__int___void__P_
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____const_pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type = struct_std__pair_const_int__int_
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_int__int___void__P_____pointer = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type = struct_std__pair_const_int__int_
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type = struct_std__pair_const_int__int_
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____const_pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____value_compare = struct_std__less_int_
    std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______Node = struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_
    std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____pointer = ctypes.POINTER(ctypes.c_int32)
    std___Default_allocator_traits_std__allocator_std___Tree_node_int__void__P_____value_type = struct_std___Tree_node_int__void__P_
    std___Default_allocator_traits_std__allocator_std___Tree_node_int__void__P_____pointer = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____const_pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____pointer = ctypes.POINTER(ctypes.c_int32)
    std___Tree_simple_types_std__pair_const_int__int_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tree_simple_types_int____Nodeptr = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    _F6553CF4C635466D7A900A328CA0BFD3 = ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_TWidget), ctypes.POINTER(struct_place_t), ctypes.POINTER(ctypes.c_uint64), ctypes.POINTER(None))
    diridx_t = ctypes.c_uint64
    bmask_t = ctypes.c_uint64
    const_t = ctypes.c_uint64
    inode_t = ctypes.c_uint64
    enum_t = ctypes.c_uint64
    class union_cfgopt_t___072F956EBF1D0FA65345CBEA02E26438(Union):
        pass
    
    union_cfgopt_t___072F956EBF1D0FA65345CBEA02E26438._pack_ = 1 # source:False
    union_cfgopt_t___072F956EBF1D0FA65345CBEA02E26438._fields_ = [
        ('ptr', ctypes.POINTER(None)),
        ('mbroff', ctypes.c_uint64),
        ('hnd', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t))),
        ('hnd2', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64)),
        ('hnd3', ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(None))),
    ]
    
    class union_argloc_t___F4A6A313BC9EA9730D72EF3AFDF761E4(Union):
        pass
    
    union_argloc_t___F4A6A313BC9EA9730D72EF3AFDF761E4._pack_ = 1 # source:False
    union_argloc_t___F4A6A313BC9EA9730D72EF3AFDF761E4._fields_ = [
        ('sval', ctypes.c_int64),
        ('reginfo', ctypes.c_uint32),
        ('rrel', ctypes.POINTER(struct_rrel_t)),
        ('dist', ctypes.POINTER(struct_scattered_aloc_t)),
        ('custom', ctypes.POINTER(None)),
        ('biggest', ctypes.c_uint64),
    ]
    
    class union_func_t___C940058B2272AD9112E2141245617273(Union):
        pass
    
    class struct_func_t___C940058B2272AD9112E2141245617273_0(Structure):
        pass
    
    struct_func_t___C940058B2272AD9112E2141245617273_0._pack_ = 1 # source:False
    struct_func_t___C940058B2272AD9112E2141245617273_0._fields_ = [
        ('frame', ctypes.c_uint64),
        ('frsize', ctypes.c_uint64),
        ('frregs', ctypes.c_uint16),
        ('PADDING_0', ctypes.c_ubyte * 6),
        ('argsize', ctypes.c_uint64),
        ('fpd', ctypes.c_uint64),
        ('color', ctypes.c_uint32),
        ('pntqty', ctypes.c_uint32),
        ('points', ctypes.POINTER(struct_stkpnt_t)),
        ('regvarqty', ctypes.c_int32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('regvars', ctypes.POINTER(struct_regvar_t)),
        ('llabelqty', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
        ('llabels', ctypes.POINTER(struct_llabel_t)),
        ('regargqty', ctypes.c_int32),
        ('PADDING_3', ctypes.c_ubyte * 4),
        ('regargs', ctypes.POINTER(struct_regarg_t)),
        ('tailqty', ctypes.c_int32),
        ('PADDING_4', ctypes.c_ubyte * 4),
        ('tails', ctypes.POINTER(struct_range_t)),
    ]
    
    class struct_func_t___C940058B2272AD9112E2141245617273_1(Structure):
        pass
    
    struct_func_t___C940058B2272AD9112E2141245617273_1._pack_ = 1 # source:False
    struct_func_t___C940058B2272AD9112E2141245617273_1._fields_ = [
        ('owner', ctypes.c_uint64),
        ('refqty', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('referers', ctypes.POINTER(ctypes.c_uint64)),
    ]
    
    union_func_t___C940058B2272AD9112E2141245617273._pack_ = 1 # source:False
    union_func_t___C940058B2272AD9112E2141245617273._anonymous_ = ('_0', '_1',)
    union_func_t___C940058B2272AD9112E2141245617273._fields_ = [
        ('_0', struct_func_t___C940058B2272AD9112E2141245617273_0),
        ('_1', struct_func_t___C940058B2272AD9112E2141245617273_1),
        ('PADDING_0', ctypes.c_ubyte * 96),
    ]
    
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____value_type = struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_____value_type = struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_____pointer = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type = struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____const_pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____Node = struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_
    std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______const_pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______pointer = ctypes.POINTER(ctypes.c_int32)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______pointer = ctypes.POINTER(ctypes.c_int32)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tree_val_std___Tree_simple_types_int_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    action_activation_ctx_t = struct_action_ctx_base_t
    action_update_ctx_t = struct_action_ctx_base_t
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Scary_val = struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_____value_type = struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_____pointer = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type = struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__unsigned_long_long_)
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____const_pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer = ctypes.POINTER(struct_std__pair_const_int__int_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Scary_val = struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_int__int___void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int______Nodeptr = ctypes.POINTER(struct_std___Tree_node_int__void__P_)
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Scary_val = struct_std___Tree_val_std___Tree_simple_types_int__
    std___Tree_val_std___Tree_simple_types_int_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Unchecked_iterator = struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Scary_val = struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____const_iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____
    std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____iterator = struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____
    std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer = ctypes.POINTER(struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____
    std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Unchecked_iterator = struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____const_iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____iterator = struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Unchecked_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____const_iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Scary_val = struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Unchecked_iterator = struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____const_reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____const_iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____
    std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____reverse_iterator = struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____iterator = struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____
    std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer = ctypes.POINTER(struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_)
    std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______Nodeptr = ctypes.POINTER(struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_)
    std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____const_reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____
    std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____reverse_iterator = struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____const_reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____
    std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Unchecked_const_iterator = struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Unchecked_iterator = struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____const_iterator = struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____iterator = struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____const_reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______
    std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____reverse_iterator = struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____const_reverse_iterator = struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____
    std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____reverse_iterator = struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____
    dirtree_link = _libraries['FIXME_STUB'].dirtree_link
    dirtree_link.restype = dterr_t
    dirtree_link.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p, ctypes.c_char]
    dirtree_mkdir = _libraries['FIXME_STUB'].dirtree_mkdir
    dirtree_mkdir.restype = dterr_t
    dirtree_mkdir.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_rmdir = _libraries['FIXME_STUB'].dirtree_rmdir
    dirtree_rmdir.restype = dterr_t
    dirtree_rmdir.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    MD5Final = _libraries['FIXME_STUB'].MD5Final
    MD5Final.restype = None
    MD5Final.argtypes = [ctypes.c_ubyte * 16, ctypes.POINTER(struct_MD5Context)]
    MD5Init = _libraries['FIXME_STUB'].MD5Init
    MD5Init.restype = None
    MD5Init.argtypes = [ctypes.POINTER(struct_MD5Context)]
    MD5Transform = _libraries['FIXME_STUB'].MD5Transform
    MD5Transform.restype = None
    MD5Transform.argtypes = [ctypes.c_uint32 * 4, ctypes.c_uint32 * 16]
    size_t = ctypes.c_uint64
    MD5Update = _libraries['FIXME_STUB'].MD5Update
    MD5Update.restype = None
    MD5Update.argtypes = [ctypes.POINTER(struct_MD5Context), ctypes.POINTER(None), size_t]
    PLUGIN = ctypes_in_dll(struct_plugin_t, _libraries['FIXME_STUB'], 'PLUGIN')
    add_auto_stkpnt = _libraries['FIXME_STUB'].add_auto_stkpnt
    add_auto_stkpnt.restype = ctypes.c_char
    add_auto_stkpnt.argtypes = [ctypes.POINTER(struct_func_t), ea_t, sval_t]
    add_base_tils = _libraries['FIXME_STUB'].add_base_tils
    add_base_tils.restype = ctypes.c_int32
    add_base_tils.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char]
    add_byte = _libraries['FIXME_STUB'].add_byte
    add_byte.restype = None
    add_byte.argtypes = [ea_t, uint32]
    add_cref = _libraries['FIXME_STUB'].add_cref
    add_cref.restype = ctypes.c_char
    add_cref.argtypes = [ea_t, ea_t, cref_t]
    add_dref = _libraries['FIXME_STUB'].add_dref
    add_dref.restype = ctypes.c_char
    add_dref.argtypes = [ea_t, ea_t, dref_t]
    add_dword = _libraries['FIXME_STUB'].add_dword
    add_dword.restype = None
    add_dword.argtypes = [ea_t, uint64]
    add_encoding = _libraries['FIXME_STUB'].add_encoding
    add_encoding.restype = ctypes.c_int32
    add_encoding.argtypes = [ctypes.c_char_p]
    add_entry = _libraries['FIXME_STUB'].add_entry
    add_entry.restype = ctypes.c_char
    add_entry.argtypes = [uval_t, ea_t, ctypes.c_char_p, ctypes.c_char, ctypes.c_int32]
    add_enum = _libraries['FIXME_STUB'].add_enum
    add_enum.restype = enum_t
    add_enum.argtypes = [size_t, ctypes.c_char_p, flags_t]
    add_enum_member = _libraries['FIXME_STUB'].add_enum_member
    add_enum_member.restype = ctypes.c_int32
    add_enum_member.argtypes = [enum_t, ctypes.c_char_p, uval_t, bmask_t]
    add_frame = _libraries['FIXME_STUB'].add_frame
    add_frame.restype = ctypes.c_char
    add_frame.argtypes = [ctypes.POINTER(struct_func_t), sval_t, ushort, asize_t]
    add_func_ex = _libraries['FIXME_STUB'].add_func_ex
    add_func_ex.restype = ctypes.c_char
    add_func_ex.argtypes = [ctypes.POINTER(struct_func_t)]
    add_hidden_range = _libraries['FIXME_STUB'].add_hidden_range
    add_hidden_range.restype = ctypes.c_char
    add_hidden_range.argtypes = [ea_t, ea_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, bgcolor_t]
    add_idc_class = _libraries['FIXME_STUB'].add_idc_class
    add_idc_class.restype = ctypes.POINTER(struct_idc_class_t)
    add_idc_class.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_idc_class_t)]
    add_idc_func = _libraries['FIXME_STUB'].add_idc_func
    add_idc_func.restype = ctypes.c_char
    add_idc_func.argtypes = [ctypes.POINTER(struct_ext_idcfunc_t)]
    add_idc_gvar = _libraries['FIXME_STUB'].add_idc_gvar
    add_idc_gvar.restype = ctypes.POINTER(struct_idc_value_t)
    add_idc_gvar.argtypes = [ctypes.c_char_p]
    add_mapping = _libraries['FIXME_STUB'].add_mapping
    add_mapping.restype = ctypes.c_char
    add_mapping.argtypes = [ea_t, ea_t, asize_t]
    add_qword = _libraries['FIXME_STUB'].add_qword
    add_qword.restype = None
    add_qword.argtypes = [ea_t, uint64]
    add_refinfo_dref = _libraries['FIXME_STUB'].add_refinfo_dref
    add_refinfo_dref.restype = ea_t
    add_refinfo_dref.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.POINTER(struct_refinfo_t), adiff_t, dref_t, ctypes.c_int32]
    add_regarg = _libraries['FIXME_STUB'].add_regarg
    add_regarg.restype = None
    add_regarg.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_int32, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p]
    add_regvar = _libraries['FIXME_STUB'].add_regvar
    add_regvar.restype = ctypes.c_int32
    add_regvar.argtypes = [ctypes.POINTER(struct_func_t), ea_t, ea_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    add_segm = _libraries['FIXME_STUB'].add_segm
    add_segm.restype = ctypes.c_char
    add_segm.argtypes = [ea_t, ea_t, ea_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]
    add_segm_ex = _libraries['FIXME_STUB'].add_segm_ex
    add_segm_ex.restype = ctypes.c_char
    add_segm_ex.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]
    add_segment_translation = _libraries['FIXME_STUB'].add_segment_translation
    add_segment_translation.restype = ctypes.c_char
    add_segment_translation.argtypes = [ea_t, ea_t]
    add_sourcefile = _libraries['FIXME_STUB'].add_sourcefile
    add_sourcefile.restype = ctypes.c_char
    add_sourcefile.argtypes = [ea_t, ea_t, ctypes.c_char_p]
    add_spaces = _libraries['FIXME_STUB'].add_spaces
    add_spaces.restype = ctypes.c_char_p
    add_spaces.argtypes = [ctypes.c_char_p, size_t, ssize_t]
    add_stkvar = _libraries['FIXME_STUB'].add_stkvar
    add_stkvar.restype = ctypes.c_char
    add_stkvar.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), sval_t, ctypes.c_int32]
    add_struc = _libraries['FIXME_STUB'].add_struc
    add_struc.restype = tid_t
    add_struc.argtypes = [uval_t, ctypes.c_char_p, ctypes.c_char]
    add_struc_member = _libraries['FIXME_STUB'].add_struc_member
    add_struc_member.restype = struc_error_t
    add_struc_member.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_char_p, ea_t, flags_t, ctypes.POINTER(union_opinfo_t), asize_t]
    add_til = _libraries['FIXME_STUB'].add_til
    add_til.restype = ctypes.c_int32
    add_til.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    add_tryblk = _libraries['FIXME_STUB'].add_tryblk
    add_tryblk.restype = ctypes.c_int32
    add_tryblk.argtypes = [ctypes.POINTER(struct_tryblk_t)]
    add_user_stkpnt = _libraries['FIXME_STUB'].add_user_stkpnt
    add_user_stkpnt.restype = ctypes.c_char
    add_user_stkpnt.argtypes = [ea_t, sval_t]
    add_word = _libraries['FIXME_STUB'].add_word
    add_word.restype = None
    add_word.argtypes = [ea_t, uint64]
    align_down_to_stack = _libraries['FIXME_STUB'].align_down_to_stack
    align_down_to_stack.restype = ea_t
    align_down_to_stack.argtypes = [ea_t]
    align_up_to_stack = _libraries['FIXME_STUB'].align_up_to_stack
    align_up_to_stack.restype = ea_t
    align_up_to_stack.argtypes = [ea_t, ea_t]
    alloc_type_ordinals = _libraries['FIXME_STUB'].alloc_type_ordinals
    alloc_type_ordinals.restype = uint32
    alloc_type_ordinals.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_int32]
    allocate_selector = _libraries['FIXME_STUB'].allocate_selector
    allocate_selector.restype = sel_t
    allocate_selector.argtypes = [ea_t]
    append_abi_opts = _libraries['FIXME_STUB'].append_abi_opts
    append_abi_opts.restype = ctypes.c_char
    append_abi_opts.argtypes = [ctypes.c_char_p, ctypes.c_char]
    append_argloc = _libraries['FIXME_STUB'].append_argloc
    append_argloc.restype = ctypes.c_char
    append_argloc.argtypes = [ctypes.POINTER(qtype), ctypes.POINTER(struct_argloc_t)]
    append_cmt = _libraries['FIXME_STUB'].append_cmt
    append_cmt.restype = ctypes.c_char
    append_cmt.argtypes = [ea_t, ctypes.c_char_p, ctypes.c_char]
    append_disp = _libraries['FIXME_STUB'].append_disp
    append_disp.restype = None
    append_disp.argtypes = [ctypes.POINTER(qstring), adiff_t, ctypes.c_char]
    append_func_tail = _libraries['FIXME_STUB'].append_func_tail
    append_func_tail.restype = ctypes.c_char
    append_func_tail.argtypes = [ctypes.POINTER(struct_func_t), ea_t, ea_t]
    append_snprintf = _libraries['FIXME_STUB'].append_snprintf
    append_snprintf.restype = ctypes.c_int32
    append_snprintf.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    append_struct_fields = _libraries['FIXME_STUB'].append_struct_fields
    append_struct_fields.restype = flags_t
    append_struct_fields.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(adiff_t), ctypes.c_int32, ctypes.POINTER(tid_t), ctypes.c_int32, flags_t, adiff_t, ctypes.c_char]
    append_tinfo_covered = _libraries['FIXME_STUB'].append_tinfo_covered
    append_tinfo_covered.restype = ctypes.c_char
    append_tinfo_covered.argtypes = [ctypes.POINTER(struct_rangeset_t), uint32, uint64]
    append_to_flowchart = _libraries['FIXME_STUB'].append_to_flowchart
    append_to_flowchart.restype = ctypes.c_char
    append_to_flowchart.argtypes = [ctypes.POINTER(struct_qflow_chart_t), ea_t, ea_t]
    apply_callee_tinfo = _libraries['FIXME_STUB'].apply_callee_tinfo
    apply_callee_tinfo.restype = ctypes.c_char
    apply_callee_tinfo.argtypes = [ea_t, ctypes.POINTER(struct_tinfo_t)]
    apply_cdecl = _libraries['FIXME_STUB'].apply_cdecl
    apply_cdecl.restype = ctypes.c_char
    apply_cdecl.argtypes = [ctypes.POINTER(struct_til_t), ea_t, ctypes.c_char_p, ctypes.c_int32]
    apply_fixup = _libraries['FIXME_STUB'].apply_fixup
    apply_fixup.restype = ctypes.c_char
    apply_fixup.argtypes = [ea_t, ea_t, ctypes.c_int32, ctypes.c_char]
    apply_idasgn_to = _libraries['FIXME_STUB'].apply_idasgn_to
    apply_idasgn_to.restype = ctypes.c_int32
    apply_idasgn_to.argtypes = [ctypes.c_char_p, ea_t, ctypes.c_char]
    apply_named_type = _libraries['FIXME_STUB'].apply_named_type
    apply_named_type.restype = ctypes.c_char
    apply_named_type.argtypes = [ea_t, ctypes.c_char_p]
    apply_once_tinfo_and_name = _libraries['FIXME_STUB'].apply_once_tinfo_and_name
    apply_once_tinfo_and_name.restype = ctypes.c_char
    apply_once_tinfo_and_name.argtypes = [ea_t, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p]
    apply_startup_sig = _libraries['FIXME_STUB'].apply_startup_sig
    apply_startup_sig.restype = ctypes.c_char
    apply_startup_sig.argtypes = [ea_t, ctypes.c_char_p]
    apply_tinfo = _libraries['FIXME_STUB'].apply_tinfo
    apply_tinfo.restype = ctypes.c_char
    apply_tinfo.argtypes = [ea_t, ctypes.POINTER(struct_tinfo_t), uint32]
    apply_tinfo_to_stkarg = _libraries['FIXME_STUB'].apply_tinfo_to_stkarg
    apply_tinfo_to_stkarg.restype = ctypes.c_char
    apply_tinfo_to_stkarg.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), uval_t, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p]
    asctoreal = _libraries['FIXME_STUB'].asctoreal
    asctoreal.restype = fpvalue_error_t
    asctoreal.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(struct_fpvalue_t)]
    ash = ctypes_in_dll(struct_asm_t, _libraries['FIXME_STUB'], 'ash')
    atob32 = _libraries['FIXME_STUB'].atob32
    atob32.restype = ctypes.c_char
    atob32.argtypes = [ctypes.POINTER(uint32), ctypes.c_char_p]
    atob64 = _libraries['FIXME_STUB'].atob64
    atob64.restype = ctypes.c_char
    atob64.argtypes = [ctypes.POINTER(uint64), ctypes.c_char_p]
    atoea = _libraries['FIXME_STUB'].atoea
    atoea.restype = ctypes.c_char
    atoea.argtypes = [ctypes.POINTER(ea_t), ctypes.c_char_p]
    atos = _libraries['FIXME_STUB'].atos
    atos.restype = ctypes.c_int32
    atos.argtypes = [ctypes.POINTER(sel_t), ctypes.c_char_p]
    attach_custom_data_format = _libraries['FIXME_STUB'].attach_custom_data_format
    attach_custom_data_format.restype = ctypes.c_char
    attach_custom_data_format.argtypes = [ctypes.c_int32, ctypes.c_int32]
    auto_apply_tail = _libraries['FIXME_STUB'].auto_apply_tail
    auto_apply_tail.restype = None
    auto_apply_tail.argtypes = [ea_t, ea_t]
    auto_apply_type = _libraries['FIXME_STUB'].auto_apply_type
    auto_apply_type.restype = None
    auto_apply_type.argtypes = [ea_t, ea_t]
    auto_cancel = _libraries['FIXME_STUB'].auto_cancel
    auto_cancel.restype = None
    auto_cancel.argtypes = [ea_t, ea_t]
    auto_get = _libraries['FIXME_STUB'].auto_get
    auto_get.restype = ea_t
    auto_get.argtypes = [ctypes.POINTER(atype_t), ea_t, ea_t]
    auto_is_ok = _libraries['FIXME_STUB'].auto_is_ok
    auto_is_ok.restype = ctypes.c_char
    auto_is_ok.argtypes = []
    auto_make_step = _libraries['FIXME_STUB'].auto_make_step
    auto_make_step.restype = ctypes.c_char
    auto_make_step.argtypes = [ea_t, ea_t]
    auto_mark_range = _libraries['FIXME_STUB'].auto_mark_range
    auto_mark_range.restype = None
    auto_mark_range.argtypes = [ea_t, ea_t, atype_t]
    auto_recreate_insn = _libraries['FIXME_STUB'].auto_recreate_insn
    auto_recreate_insn.restype = ctypes.c_int32
    auto_recreate_insn.argtypes = [ea_t]
    auto_unmark = _libraries['FIXME_STUB'].auto_unmark
    auto_unmark.restype = None
    auto_unmark.argtypes = [ea_t, ea_t, atype_t]
    auto_wait = _libraries['FIXME_STUB'].auto_wait
    auto_wait.restype = ctypes.c_char
    auto_wait.argtypes = []
    auto_wait_range = _libraries['FIXME_STUB'].auto_wait_range
    auto_wait_range.restype = ssize_t
    auto_wait_range.argtypes = [ea_t, ea_t]
    b2a32 = _libraries['FIXME_STUB'].b2a32
    b2a32.restype = size_t
    b2a32.argtypes = [ctypes.c_char_p, size_t, uint32, ctypes.c_int32, ctypes.c_int32]
    b2a64 = _libraries['FIXME_STUB'].b2a64
    b2a64.restype = size_t
    b2a64.argtypes = [ctypes.c_char_p, size_t, uint64, ctypes.c_int32, ctypes.c_int32]
    b2a_width = _libraries['FIXME_STUB'].b2a_width
    b2a_width.restype = size_t
    b2a_width.argtypes = [ctypes.c_int32, ctypes.c_int32]
    back_char = _libraries['FIXME_STUB'].back_char
    back_char.restype = ctypes.c_char
    back_char.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    struct__iobuf._pack_ = 1 # source:False
    struct__iobuf._fields_ = [
        ('_Placeholder', ctypes.POINTER(None)),
    ]
    
    FILE = struct__iobuf
    base2file = _libraries['FIXME_STUB'].base2file
    base2file.restype = ctypes.c_int32
    base2file.argtypes = [ctypes.POINTER(FILE), int64, ea_t, ea_t]
    base64_decode = _libraries['FIXME_STUB'].base64_decode
    base64_decode.restype = ctypes.c_char
    base64_decode.argtypes = [ctypes.POINTER(struct_bytevec_t), ctypes.c_char_p, size_t]
    base64_encode = _libraries['FIXME_STUB'].base64_encode
    base64_encode.restype = ctypes.c_char
    base64_encode.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(None), size_t]
    batch = ctypes_in_dll(ctypes.c_char, _libraries['FIXME_STUB'], 'batch')
    begin_type_updating = _libraries['FIXME_STUB'].begin_type_updating
    begin_type_updating.restype = None
    begin_type_updating.argtypes = [update_type_t]
    bin_search = _libraries['FIXME_STUB'].bin_search
    bin_search.restype = ea_t
    bin_search.argtypes = [ea_t, ea_t, ctypes.POINTER(uchar), ctypes.POINTER(uchar), size_t, ctypes.c_int32, ctypes.c_int32]
    bin_search2 = _libraries['FIXME_STUB'].bin_search2
    bin_search2.restype = ea_t
    bin_search2.argtypes = [ea_t, ea_t, ctypes.POINTER(compiled_binpat_vec_t), ctypes.c_int32]
    bin_search3 = _libraries['FIXME_STUB'].bin_search3
    bin_search3.restype = ea_t
    bin_search3.argtypes = [ctypes.POINTER(size_t), ea_t, ea_t, ctypes.POINTER(compiled_binpat_vec_t), ctypes.c_int32]
    bitcount = _libraries['FIXME_STUB'].bitcount
    bitcount.restype = ctypes.c_int32
    bitcount.argtypes = [uint64]
    bitrange_t_extract_using_bitrange = _libraries['FIXME_STUB'].bitrange_t_extract_using_bitrange
    bitrange_t_extract_using_bitrange.restype = ctypes.c_char
    bitrange_t_extract_using_bitrange.argtypes = [ctypes.POINTER(struct_bitrange_t), ctypes.POINTER(None), size_t, ctypes.POINTER(None), size_t, ctypes.c_char]
    bitrange_t_inject_using_bitrange = _libraries['FIXME_STUB'].bitrange_t_inject_using_bitrange
    bitrange_t_inject_using_bitrange.restype = ctypes.c_char
    bitrange_t_inject_using_bitrange.argtypes = [ctypes.POINTER(struct_bitrange_t), ctypes.POINTER(None), size_t, ctypes.POINTER(None), size_t, ctypes.c_char]
    bookmarks_t_erase = _libraries['FIXME_STUB'].bookmarks_t_erase
    bookmarks_t_erase.restype = ctypes.c_char
    bookmarks_t_erase.argtypes = [ctypes.POINTER(struct_lochist_entry_t), uint32, ctypes.POINTER(None)]
    bookmarks_t_find_index = _libraries['FIXME_STUB'].bookmarks_t_find_index
    bookmarks_t_find_index.restype = uint32
    bookmarks_t_find_index.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(None)]
    bookmarks_t_get = _libraries['FIXME_STUB'].bookmarks_t_get
    bookmarks_t_get.restype = ctypes.c_char
    bookmarks_t_get.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(qstring), ctypes.POINTER(uint32), ctypes.POINTER(None)]
    bookmarks_t_get_desc = _libraries['FIXME_STUB'].bookmarks_t_get_desc
    bookmarks_t_get_desc.restype = ctypes.c_char
    bookmarks_t_get_desc.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_lochist_entry_t), uint32, ctypes.POINTER(None)]
    bookmarks_t_get_dirtree_id = _libraries['FIXME_STUB'].bookmarks_t_get_dirtree_id
    bookmarks_t_get_dirtree_id.restype = dirtree_id_t
    bookmarks_t_get_dirtree_id.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(None)]
    bookmarks_t_mark = _libraries['FIXME_STUB'].bookmarks_t_mark
    bookmarks_t_mark.restype = uint32
    bookmarks_t_mark.argtypes = [ctypes.POINTER(struct_lochist_entry_t), uint32, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(None)]
    bookmarks_t_set_desc = _libraries['FIXME_STUB'].bookmarks_t_set_desc
    bookmarks_t_set_desc.restype = ctypes.c_char
    bookmarks_t_set_desc.argtypes = [qstring, ctypes.POINTER(struct_lochist_entry_t), uint32, ctypes.POINTER(None)]
    bookmarks_t_size = _libraries['FIXME_STUB'].bookmarks_t_size
    bookmarks_t_size.restype = uint32
    bookmarks_t_size.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(None)]
    btoa128 = _libraries['FIXME_STUB'].btoa128
    btoa128.restype = size_t
    btoa128.argtypes = [ctypes.c_char_p, size_t, struct_uint128, ctypes.c_int32]
    btoa32 = _libraries['FIXME_STUB'].btoa32
    btoa32.restype = size_t
    btoa32.argtypes = [ctypes.c_char_p, size_t, uint32, ctypes.c_int32]
    btoa64 = _libraries['FIXME_STUB'].btoa64
    btoa64.restype = size_t
    btoa64.argtypes = [ctypes.c_char_p, size_t, uint64, ctypes.c_int32]
    btoa_width = _libraries['FIXME_STUB'].btoa_width
    btoa_width.restype = size_t
    btoa_width.argtypes = [ctypes.c_int32, flags_t, ctypes.c_int32]
    build_anon_type_name = _libraries['FIXME_STUB'].build_anon_type_name
    build_anon_type_name.restype = None
    build_anon_type_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(type_t), ctypes.POINTER(p_list)]
    build_loaders_list = _libraries['FIXME_STUB'].build_loaders_list
    build_loaders_list.restype = ctypes.POINTER(struct_load_info_t)
    build_loaders_list.argtypes = [ctypes.POINTER(struct_linput_t), ctypes.c_char_p]
    build_snapshot_tree = _libraries['FIXME_STUB'].build_snapshot_tree
    build_snapshot_tree.restype = ctypes.c_char
    build_snapshot_tree.argtypes = [ctypes.POINTER(struct_snapshot_t)]
    build_stkvar_name = _libraries['FIXME_STUB'].build_stkvar_name
    build_stkvar_name.restype = ssize_t
    build_stkvar_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_func_t), sval_t]
    build_stkvar_xrefs = _libraries['FIXME_STUB'].build_stkvar_xrefs
    build_stkvar_xrefs.restype = None
    build_stkvar_xrefs.argtypes = [ctypes.POINTER(xreflist_t), ctypes.POINTER(struct_func_t), ctypes.POINTER(struct_member_t)]
    build_strlist = _libraries['FIXME_STUB'].build_strlist
    build_strlist.restype = None
    build_strlist.argtypes = []
    calc_bg_color = _libraries['FIXME_STUB'].calc_bg_color
    calc_bg_color.restype = bgcolor_t
    calc_bg_color.argtypes = [ea_t]
    calc_c_cpp_name = _libraries['FIXME_STUB'].calc_c_cpp_name
    calc_c_cpp_name.restype = ssize_t
    calc_c_cpp_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.POINTER(struct_tinfo_t), ctypes.c_int32]
    calc_crc32 = _libraries['FIXME_STUB'].calc_crc32
    calc_crc32.restype = uint32
    calc_crc32.argtypes = [uint32, ctypes.POINTER(None), size_t]
    calc_dataseg = _libraries['FIXME_STUB'].calc_dataseg
    calc_dataseg.restype = ea_t
    calc_dataseg.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.c_int32, ctypes.c_int32]
    calc_def_align = _libraries['FIXME_STUB'].calc_def_align
    calc_def_align.restype = ctypes.c_int32
    calc_def_align.argtypes = [ea_t, ctypes.c_int32, ctypes.c_int32]
    calc_file_crc32 = _libraries['FIXME_STUB'].calc_file_crc32
    calc_file_crc32.restype = uint32
    calc_file_crc32.argtypes = [ctypes.POINTER(struct_linput_t)]
    calc_fixup_size = _libraries['FIXME_STUB'].calc_fixup_size
    calc_fixup_size.restype = ctypes.c_int32
    calc_fixup_size.argtypes = [fixup_type_t]
    calc_func_size = _libraries['FIXME_STUB'].calc_func_size
    calc_func_size.restype = asize_t
    calc_func_size.argtypes = [ctypes.POINTER(struct_func_t)]
    calc_idasgn_state = _libraries['FIXME_STUB'].calc_idasgn_state
    calc_idasgn_state.restype = ctypes.c_int32
    calc_idasgn_state.argtypes = [ctypes.c_int32]
    calc_max_align = _libraries['FIXME_STUB'].calc_max_align
    calc_max_align.restype = ctypes.c_int32
    calc_max_align.argtypes = [ea_t]
    calc_max_item_end = _libraries['FIXME_STUB'].calc_max_item_end
    calc_max_item_end.restype = ea_t
    calc_max_item_end.argtypes = [ea_t, ctypes.c_int32]
    calc_min_align = _libraries['FIXME_STUB'].calc_min_align
    calc_min_align.restype = ctypes.c_int32
    calc_min_align.argtypes = [asize_t]
    calc_number_of_children = _libraries['FIXME_STUB'].calc_number_of_children
    calc_number_of_children.restype = ctypes.c_int32
    calc_number_of_children.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_char]
    calc_offset_base = _libraries['FIXME_STUB'].calc_offset_base
    calc_offset_base.restype = ea_t
    calc_offset_base.argtypes = [ea_t, ctypes.c_int32]
    calc_prefix_color = _libraries['FIXME_STUB'].calc_prefix_color
    calc_prefix_color.restype = color_t
    calc_prefix_color.argtypes = [ea_t]
    calc_probable_base_by_value = _libraries['FIXME_STUB'].calc_probable_base_by_value
    calc_probable_base_by_value.restype = ea_t
    calc_probable_base_by_value.argtypes = [ea_t, uval_t]
    calc_reference_data = _libraries['FIXME_STUB'].calc_reference_data
    calc_reference_data.restype = ctypes.c_char
    calc_reference_data.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(ea_t), ea_t, ctypes.POINTER(struct_refinfo_t), adiff_t]
    calc_stkvar_struc_offset = _libraries['FIXME_STUB'].calc_stkvar_struc_offset
    calc_stkvar_struc_offset.restype = ea_t
    calc_stkvar_struc_offset.argtypes = [ctypes.POINTER(struct_func_t), ctypes.POINTER(struct_insn_t), ctypes.c_int32]
    calc_switch_cases = _libraries['FIXME_STUB'].calc_switch_cases
    calc_switch_cases.restype = ctypes.c_char
    calc_switch_cases.argtypes = [ctypes.POINTER(casevec_t), ctypes.POINTER(eavec_t), ea_t, ctypes.POINTER(struct_switch_info_t)]
    calc_thunk_func_target = _libraries['FIXME_STUB'].calc_thunk_func_target
    calc_thunk_func_target.restype = ea_t
    calc_thunk_func_target.argtypes = [ctypes.POINTER(struct_func_t), ctypes.POINTER(ea_t)]
    calc_tinfo_gaps = _libraries['FIXME_STUB'].calc_tinfo_gaps
    calc_tinfo_gaps.restype = ctypes.c_char
    calc_tinfo_gaps.argtypes = [ctypes.POINTER(struct_rangeset_t), uint32]
    call_idc_func = _libraries['FIXME_STUB'].call_idc_func
    call_idc_func.restype = ctypes.c_char
    call_idc_func.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, struct_idc_value_t * 0, size_t, ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_resolver_t)]
    call_system = _libraries['FIXME_STUB'].call_system
    call_system.restype = ctypes.c_int32
    call_system.argtypes = [ctypes.c_char_p]
    callui = ctypes_in_dll(ctypes.CFUNCTYPE(union_callui_t, ui_notification_t), _libraries['FIXME_STUB'], 'callui')
    can_be_off32 = _libraries['FIXME_STUB'].can_be_off32
    can_be_off32.restype = ea_t
    can_be_off32.argtypes = [ea_t]
    can_define_item = _libraries['FIXME_STUB'].can_define_item
    can_define_item.restype = ctypes.c_char
    can_define_item.argtypes = [ea_t, asize_t, flags_t]
    cfgopt_t__apply = _libraries['FIXME_STUB'].cfgopt_t__apply
    cfgopt_t__apply.restype = ctypes.c_char_p
    cfgopt_t__apply.argtypes = [ctypes.POINTER(struct_cfgopt_t), ctypes.c_int32, ctypes.POINTER(None)]
    cfgopt_t__apply2 = _libraries['FIXME_STUB'].cfgopt_t__apply2
    cfgopt_t__apply2.restype = ctypes.c_char_p
    cfgopt_t__apply2.argtypes = [ctypes.POINTER(struct_cfgopt_t), ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None)]
    cfgopt_t__apply3 = _libraries['FIXME_STUB'].cfgopt_t__apply3
    cfgopt_t__apply3.restype = ctypes.c_char_p
    cfgopt_t__apply3.argtypes = [ctypes.POINTER(struct_cfgopt_t), ctypes.POINTER(struct_lexer_t), ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None)]
    change_codepage = _libraries['FIXME_STUB'].change_codepage
    change_codepage.restype = ctypes.c_char
    change_codepage.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    change_segment_status = _libraries['FIXME_STUB'].change_segment_status
    change_segment_status.restype = ctypes.c_int32
    change_segment_status.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char]
    change_storage_type = _libraries['FIXME_STUB'].change_storage_type
    change_storage_type.restype = error_t
    change_storage_type.argtypes = [ea_t, ea_t, storage_type_t]
    check_flat_jump_table = _libraries['FIXME_STUB'].check_flat_jump_table
    check_flat_jump_table.restype = ctypes.c_int32
    check_flat_jump_table.argtypes = [ctypes.POINTER(struct_switch_info_t), ea_t, ctypes.c_int32]
    check_for_table_jump = _libraries['FIXME_STUB'].check_for_table_jump
    check_for_table_jump.restype = ctypes.c_char
    check_for_table_jump.argtypes = [ctypes.POINTER(struct_switch_info_t), ctypes.POINTER(struct_insn_t), ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_switch_info_t), ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_procmod_t)) * 0, size_t, table_checker_t, ctypes.c_char_p]
    check_process_exit = _libraries['FIXME_STUB'].check_process_exit
    check_process_exit.restype = ctypes.c_int32
    check_process_exit.argtypes = [ctypes.POINTER(None), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    check_spoiled_jpt = _libraries['FIXME_STUB'].check_spoiled_jpt
    check_spoiled_jpt.restype = None
    check_spoiled_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.POINTER(tracked_regs_t)]
    choose_ioport_device = _libraries['FIXME_STUB'].choose_ioport_device
    choose_ioport_device.restype = ctypes.c_char
    choose_ioport_device.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.c_char_p)]
    choose_ioport_device2 = _libraries['FIXME_STUB'].choose_ioport_device2
    choose_ioport_device2.restype = ctypes.c_char
    choose_ioport_device2.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.POINTER(struct_choose_ioport_parser_t)]
    choose_local_tinfo = _libraries['FIXME_STUB'].choose_local_tinfo
    choose_local_tinfo.restype = uint32
    choose_local_tinfo.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int32, uint32, ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(None)), uint32, ctypes.POINTER(None)]
    choose_local_tinfo_and_delta = _libraries['FIXME_STUB'].choose_local_tinfo_and_delta
    choose_local_tinfo_and_delta.restype = uint32
    choose_local_tinfo_and_delta.argtypes = [ctypes.POINTER(int32), ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int32, uint32, ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(None)), uint32, ctypes.POINTER(None)]
    choose_named_type = _libraries['FIXME_STUB'].choose_named_type
    choose_named_type.restype = ctypes.c_char
    choose_named_type.argtypes = [ctypes.POINTER(struct_til_symbol_t), ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_int32, ctypes.POINTER(struct_predicate_t)]
    chunk_size = _libraries['FIXME_STUB'].chunk_size
    chunk_size.restype = asize_t
    chunk_size.argtypes = [ea_t]
    chunk_start = _libraries['FIXME_STUB'].chunk_start
    chunk_start.restype = ea_t
    chunk_start.argtypes = [ea_t]
    cleanup_appcall = _libraries['FIXME_STUB'].cleanup_appcall
    cleanup_appcall.restype = error_t
    cleanup_appcall.argtypes = [thid_t]
    cleanup_argloc = _libraries['FIXME_STUB'].cleanup_argloc
    cleanup_argloc.restype = None
    cleanup_argloc.argtypes = [ctypes.POINTER(struct_argloc_t)]
    cleanup_name = _libraries['FIXME_STUB'].cleanup_name
    cleanup_name.restype = ctypes.c_char
    cleanup_name.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_char_p, uint32]
    clear_strlist = _libraries['FIXME_STUB'].clear_strlist
    clear_strlist.restype = None
    clear_strlist.argtypes = []
    clear_tinfo_t = _libraries['FIXME_STUB'].clear_tinfo_t
    clear_tinfo_t.restype = None
    clear_tinfo_t.argtypes = [ctypes.POINTER(struct_tinfo_t)]
    cliopts_t_add = _libraries['FIXME_STUB'].cliopts_t_add
    cliopts_t_add.restype = None
    cliopts_t_add.argtypes = [ctypes.POINTER(struct_cliopts_t), ctypes.POINTER(struct_cliopt_t), size_t]
    cliopts_t_apply = _libraries['FIXME_STUB'].cliopts_t_apply
    cliopts_t_apply.restype = None
    cliopts_t_apply.argtypes = [ctypes.POINTER(struct_cliopts_t), ctypes.c_int32, ctypes.c_char_p * 0, ctypes.POINTER(None)]
    cliopts_t_find_long = _libraries['FIXME_STUB'].cliopts_t_find_long
    cliopts_t_find_long.restype = ctypes.POINTER(struct_cliopt_t)
    cliopts_t_find_long.argtypes = [ctypes.POINTER(struct_cliopts_t), ctypes.c_char_p]
    cliopts_t_find_short = _libraries['FIXME_STUB'].cliopts_t_find_short
    cliopts_t_find_short.restype = ctypes.POINTER(struct_cliopt_t)
    cliopts_t_find_short.argtypes = [ctypes.POINTER(struct_cliopts_t), ctypes.c_char]
    cliopts_t_usage = _libraries['FIXME_STUB'].cliopts_t_usage
    cliopts_t_usage.restype = None
    cliopts_t_usage.argtypes = [ctypes.POINTER(struct_cliopts_t), ctypes.c_char]
    close_linput = _libraries['FIXME_STUB'].close_linput
    close_linput.restype = None
    close_linput.argtypes = [ctypes.POINTER(struct_linput_t)]
    closing_comment = _libraries['FIXME_STUB'].closing_comment
    closing_comment.restype = ctypes.c_char_p
    closing_comment.argtypes = []
    clr_abits = _libraries['FIXME_STUB'].clr_abits
    clr_abits.restype = None
    clr_abits.argtypes = [ea_t, aflags_t]
    clr_lzero = _libraries['FIXME_STUB'].clr_lzero
    clr_lzero.restype = ctypes.c_char
    clr_lzero.argtypes = [ea_t, ctypes.c_int32]
    clr_module_data = _libraries['FIXME_STUB'].clr_module_data
    clr_module_data.restype = ctypes.POINTER(None)
    clr_module_data.argtypes = [ctypes.c_int32]
    clr_node_info = _libraries['FIXME_STUB'].clr_node_info
    clr_node_info.restype = None
    clr_node_info.argtypes = [graph_id_t, ctypes.c_int32, uint32]
    clr_op_type = _libraries['FIXME_STUB'].clr_op_type
    clr_op_type.restype = ctypes.c_char
    clr_op_type.argtypes = [ea_t, ctypes.c_int32]
    code_highlight_block = _libraries['FIXME_STUB'].code_highlight_block
    code_highlight_block.restype = None
    code_highlight_block.argtypes = [ctypes.POINTER(None), ctypes.POINTER(struct_highlighter_cbs_t), ctypes.POINTER(qstring)]
    combine_regs_jpt = _libraries['FIXME_STUB'].combine_regs_jpt
    combine_regs_jpt.restype = None
    combine_regs_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.POINTER(tracked_regs_t), ctypes.POINTER(tracked_regs_t), ea_t]
    compact_numbered_types = _libraries['FIXME_STUB'].compact_numbered_types
    compact_numbered_types.restype = ctypes.c_int32
    compact_numbered_types.argtypes = [ctypes.POINTER(struct_til_t), uint32, ctypes.POINTER(intvec_t), ctypes.c_int32]
    compact_til = _libraries['FIXME_STUB'].compact_til
    compact_til.restype = ctypes.c_char
    compact_til.argtypes = [ctypes.POINTER(struct_til_t)]
    compare_arglocs = _libraries['FIXME_STUB'].compare_arglocs
    compare_arglocs.restype = ctypes.c_int32
    compare_arglocs.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_argloc_t)]
    compare_tinfo = _libraries['FIXME_STUB'].compare_tinfo
    compare_tinfo.restype = ctypes.c_char
    compare_tinfo.argtypes = [uint32, uint32, ctypes.c_int32]
    compile_idc_file = _libraries['FIXME_STUB'].compile_idc_file
    compile_idc_file.restype = ctypes.c_char
    compile_idc_file.argtypes = [ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.c_int32]
    compile_idc_snippet = _libraries['FIXME_STUB'].compile_idc_snippet
    compile_idc_snippet.restype = ctypes.c_char
    compile_idc_snippet.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_resolver_t), ctypes.c_char]
    compile_idc_text = _libraries['FIXME_STUB'].compile_idc_text
    compile_idc_text.restype = ctypes.c_char
    compile_idc_text.argtypes = [ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_resolver_t), ctypes.c_char]
    construct_macro = _libraries['FIXME_STUB'].construct_macro
    construct_macro.restype = ctypes.c_char
    construct_macro.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.c_char, ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_insn_t), ctypes.c_char)]
    construct_macro2 = _libraries['FIXME_STUB'].construct_macro2
    construct_macro2.restype = ctypes.c_char
    construct_macro2.argtypes = [ctypes.POINTER(struct_macro_constructor_t), ctypes.POINTER(struct_insn_t), ctypes.c_char]
    convert_encoding = _libraries['FIXME_STUB'].convert_encoding
    convert_encoding.restype = ssize_t
    convert_encoding.argtypes = [ctypes.POINTER(struct_bytevec_t), ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(uchar), ssize_t, ctypes.c_int32]
    copy_argloc = _libraries['FIXME_STUB'].copy_argloc
    copy_argloc.restype = None
    copy_argloc.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.POINTER(struct_argloc_t)]
    copy_debug_event = _libraries['FIXME_STUB'].copy_debug_event
    copy_debug_event.restype = None
    copy_debug_event.argtypes = [ctypes.POINTER(struct_debug_event_t), ctypes.POINTER(struct_debug_event_t)]
    copy_idcv = _libraries['FIXME_STUB'].copy_idcv
    copy_idcv.restype = error_t
    copy_idcv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)]
    copy_named_type = _libraries['FIXME_STUB'].copy_named_type
    copy_named_type.restype = uint32
    copy_named_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.POINTER(struct_til_t), ctypes.c_char_p]
    copy_sreg_ranges = _libraries['FIXME_STUB'].copy_sreg_ranges
    copy_sreg_ranges.restype = None
    copy_sreg_ranges.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_char]
    copy_tinfo_t = _libraries['FIXME_STUB'].copy_tinfo_t
    copy_tinfo_t.restype = None
    copy_tinfo_t.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_tinfo_t)]
    create_16bit_data = _libraries['FIXME_STUB'].create_16bit_data
    create_16bit_data.restype = ctypes.c_char
    create_16bit_data.argtypes = [ea_t, asize_t]
    create_32bit_data = _libraries['FIXME_STUB'].create_32bit_data
    create_32bit_data.restype = ctypes.c_char
    create_32bit_data.argtypes = [ea_t, asize_t]
    create_align = _libraries['FIXME_STUB'].create_align
    create_align.restype = ctypes.c_char
    create_align.argtypes = [ea_t, asize_t, ctypes.c_int32]
    create_bytearray_linput = _libraries['FIXME_STUB'].create_bytearray_linput
    create_bytearray_linput.restype = ctypes.POINTER(struct_linput_t)
    create_bytearray_linput.argtypes = [ctypes.POINTER(uchar), size_t]
    create_data = _libraries['FIXME_STUB'].create_data
    create_data.restype = ctypes.c_char
    create_data.argtypes = [ea_t, flags_t, asize_t, tid_t]
    create_dirtree = _libraries['FIXME_STUB'].create_dirtree
    create_dirtree.restype = ctypes.POINTER(struct_dirtree_impl_t)
    create_dirtree.argtypes = [ctypes.POINTER(struct_dirtree_t), ctypes.POINTER(struct_dirspec_t)]
    create_encoding_helper = _libraries['FIXME_STUB'].create_encoding_helper
    create_encoding_helper.restype = ctypes.POINTER(struct_encoder_t)
    create_encoding_helper.argtypes = [ctypes.c_int32, encoder_t__notify_recerr_t]
    create_filename_cmt = _libraries['FIXME_STUB'].create_filename_cmt
    create_filename_cmt.restype = None
    create_filename_cmt.argtypes = []
    create_generic_linput = _libraries['FIXME_STUB'].create_generic_linput
    create_generic_linput.restype = ctypes.POINTER(struct_linput_t)
    create_generic_linput.argtypes = [ctypes.POINTER(struct_generic_linput_t)]
    create_idcv_ref = _libraries['FIXME_STUB'].create_idcv_ref
    create_idcv_ref.restype = ctypes.c_char
    create_idcv_ref.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)]
    create_insn = _libraries['FIXME_STUB'].create_insn
    create_insn.restype = ctypes.c_int32
    create_insn.argtypes = [ea_t, ctypes.POINTER(struct_insn_t)]
    create_lexer = _libraries['FIXME_STUB'].create_lexer
    create_lexer.restype = ctypes.POINTER(struct_lexer_t)
    create_lexer.argtypes = [ctypes.POINTER(ctypes.c_char_p), size_t, ctypes.POINTER(None)]
    create_memory_linput = _libraries['FIXME_STUB'].create_memory_linput
    create_memory_linput.restype = ctypes.POINTER(struct_linput_t)
    create_memory_linput.argtypes = [ea_t, asize_t]
    create_multirange_qflow_chart = _libraries['FIXME_STUB'].create_multirange_qflow_chart
    create_multirange_qflow_chart.restype = ctypes.c_char
    create_multirange_qflow_chart.argtypes = [ctypes.POINTER(struct_qflow_chart_t), ctypes.POINTER(struct_rangevec_t)]
    create_numbered_type_name = _libraries['FIXME_STUB'].create_numbered_type_name
    create_numbered_type_name.restype = ssize_t
    create_numbered_type_name.argtypes = [ctypes.POINTER(qstring), int32]
    create_outctx = _libraries['FIXME_STUB'].create_outctx
    create_outctx.restype = ctypes.POINTER(struct_outctx_base_t)
    create_outctx.argtypes = [ea_t, flags_t, ctypes.c_int32]
    create_qflow_chart = _libraries['FIXME_STUB'].create_qflow_chart
    create_qflow_chart.restype = None
    create_qflow_chart.argtypes = [ctypes.POINTER(struct_qflow_chart_t)]
    create_strlit = _libraries['FIXME_STUB'].create_strlit
    create_strlit.restype = ctypes.c_char
    create_strlit.argtypes = [ea_t, size_t, int32]
    create_switch_table = _libraries['FIXME_STUB'].create_switch_table
    create_switch_table.restype = ctypes.c_char
    create_switch_table.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t)]
    create_switch_xrefs = _libraries['FIXME_STUB'].create_switch_xrefs
    create_switch_xrefs.restype = None
    create_switch_xrefs.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t)]
    create_tinfo = _libraries['FIXME_STUB'].create_tinfo
    create_tinfo.restype = ctypes.c_char
    create_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), type_t, type_t, ctypes.POINTER(None)]
    create_xrefs_from = _libraries['FIXME_STUB'].create_xrefs_from
    create_xrefs_from.restype = ctypes.c_char
    create_xrefs_from.argtypes = [ea_t]
    create_zip_linput = _libraries['FIXME_STUB'].create_zip_linput
    create_zip_linput.restype = ctypes.POINTER(struct_linput_t)
    create_zip_linput.argtypes = [ctypes.POINTER(struct_linput_t), ssize_t, linput_close_code_t]
    dbg = ctypes_in_dll(ctypes.POINTER(struct_debugger_t), _libraries['FIXME_STUB'], 'dbg')
    dbg_appcall = _libraries['FIXME_STUB'].dbg_appcall
    dbg_appcall.restype = error_t
    dbg_appcall.argtypes = [ctypes.POINTER(struct_idc_value_t), ea_t, thid_t, ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_idc_value_t), size_t]
    dbg_get_input_path = _libraries['FIXME_STUB'].dbg_get_input_path
    dbg_get_input_path.restype = ssize_t
    dbg_get_input_path.argtypes = [ctypes.c_char_p, size_t]
    debug = ctypes_in_dll(ctypes.c_uint32, _libraries['FIXME_STUB'], 'debug')
    decode_insn = _libraries['FIXME_STUB'].decode_insn
    decode_insn.restype = ctypes.c_int32
    decode_insn.argtypes = [ctypes.POINTER(struct_insn_t), ea_t]
    decode_preceding_insn = _libraries['FIXME_STUB'].decode_preceding_insn
    decode_preceding_insn.restype = ea_t
    decode_preceding_insn.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.c_char_p]
    decode_prev_insn = _libraries['FIXME_STUB'].decode_prev_insn
    decode_prev_insn.restype = ea_t
    decode_prev_insn.argtypes = [ctypes.POINTER(struct_insn_t), ea_t]
    decorate_name = _libraries['FIXME_STUB'].decorate_name
    decorate_name.restype = ctypes.c_char
    decorate_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_char, cm_t, ctypes.POINTER(struct_tinfo_t)]
    deep_copy_idcv = _libraries['FIXME_STUB'].deep_copy_idcv
    deep_copy_idcv.restype = error_t
    deep_copy_idcv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)]
    define_stkvar = _libraries['FIXME_STUB'].define_stkvar
    define_stkvar.restype = ctypes.c_char
    define_stkvar.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char_p, sval_t, flags_t, ctypes.POINTER(union_opinfo_t), asize_t]
    del_aflags = _libraries['FIXME_STUB'].del_aflags
    del_aflags.restype = None
    del_aflags.argtypes = [ea_t]
    del_cref = _libraries['FIXME_STUB'].del_cref
    del_cref.restype = ctypes.c_char
    del_cref.argtypes = [ea_t, ea_t, ctypes.c_char]
    del_debug_names = _libraries['FIXME_STUB'].del_debug_names
    del_debug_names.restype = None
    del_debug_names.argtypes = [ea_t, ea_t]
    del_dref = _libraries['FIXME_STUB'].del_dref
    del_dref.restype = None
    del_dref.argtypes = [ea_t, ea_t]
    del_encoding = _libraries['FIXME_STUB'].del_encoding
    del_encoding.restype = ctypes.c_char
    del_encoding.argtypes = [ctypes.c_int32]
    del_enum = _libraries['FIXME_STUB'].del_enum
    del_enum.restype = None
    del_enum.argtypes = [enum_t]
    del_enum_member = _libraries['FIXME_STUB'].del_enum_member
    del_enum_member.restype = ctypes.c_char
    del_enum_member.argtypes = [enum_t, uval_t, uchar, bmask_t]
    del_extra_cmt = _libraries['FIXME_STUB'].del_extra_cmt
    del_extra_cmt.restype = None
    del_extra_cmt.argtypes = [ea_t, ctypes.c_int32]
    del_fixup = _libraries['FIXME_STUB'].del_fixup
    del_fixup.restype = None
    del_fixup.argtypes = [ea_t]
    del_frame = _libraries['FIXME_STUB'].del_frame
    del_frame.restype = ctypes.c_char
    del_frame.argtypes = [ctypes.POINTER(struct_func_t)]
    del_func = _libraries['FIXME_STUB'].del_func
    del_func.restype = ctypes.c_char
    del_func.argtypes = [ea_t]
    del_hidden_range = _libraries['FIXME_STUB'].del_hidden_range
    del_hidden_range.restype = ctypes.c_char
    del_hidden_range.argtypes = [ea_t]
    del_idasgn = _libraries['FIXME_STUB'].del_idasgn
    del_idasgn.restype = ctypes.c_int32
    del_idasgn.argtypes = [ctypes.c_int32]
    del_idc_func = _libraries['FIXME_STUB'].del_idc_func
    del_idc_func.restype = ctypes.c_char
    del_idc_func.argtypes = [ctypes.c_char_p]
    del_idcv_attr = _libraries['FIXME_STUB'].del_idcv_attr
    del_idcv_attr.restype = error_t
    del_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p]
    del_item_color = _libraries['FIXME_STUB'].del_item_color
    del_item_color.restype = ctypes.c_char
    del_item_color.argtypes = [ea_t]
    del_items = _libraries['FIXME_STUB'].del_items
    del_items.restype = ctypes.c_char
    del_items.argtypes = [ea_t, ctypes.c_int32, asize_t, ctypes.CFUNCTYPE(ctypes.c_char, ea_t)]
    del_mapping = _libraries['FIXME_STUB'].del_mapping
    del_mapping.restype = None
    del_mapping.argtypes = [ea_t]
    del_member_tinfo = _libraries['FIXME_STUB'].del_member_tinfo
    del_member_tinfo.restype = ctypes.c_char
    del_member_tinfo.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.POINTER(struct_member_t)]
    del_named_type = _libraries['FIXME_STUB'].del_named_type
    del_named_type.restype = ctypes.c_char
    del_named_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_int32]
    del_node_info = _libraries['FIXME_STUB'].del_node_info
    del_node_info.restype = None
    del_node_info.argtypes = [graph_id_t, ctypes.c_int32]
    del_numbered_type = _libraries['FIXME_STUB'].del_numbered_type
    del_numbered_type.restype = ctypes.c_char
    del_numbered_type.argtypes = [ctypes.POINTER(struct_til_t), uint32]
    del_qatexit = _libraries['FIXME_STUB'].del_qatexit
    del_qatexit.restype = None
    del_qatexit.argtypes = [ctypes.CFUNCTYPE(None)]
    del_refinfo = _libraries['FIXME_STUB'].del_refinfo
    del_refinfo.restype = ctypes.c_char
    del_refinfo.argtypes = [ea_t, ctypes.c_int32]
    del_regvar = _libraries['FIXME_STUB'].del_regvar
    del_regvar.restype = ctypes.c_int32
    del_regvar.argtypes = [ctypes.POINTER(struct_func_t), ea_t, ea_t, ctypes.c_char_p]
    del_segm = _libraries['FIXME_STUB'].del_segm
    del_segm.restype = ctypes.c_char
    del_segm.argtypes = [ea_t, ctypes.c_int32]
    del_segment_translations = _libraries['FIXME_STUB'].del_segment_translations
    del_segment_translations.restype = None
    del_segment_translations.argtypes = [ea_t]
    del_selector = _libraries['FIXME_STUB'].del_selector
    del_selector.restype = None
    del_selector.argtypes = [sel_t]
    del_source_linnum = _libraries['FIXME_STUB'].del_source_linnum
    del_source_linnum.restype = None
    del_source_linnum.argtypes = [ea_t]
    del_sourcefile = _libraries['FIXME_STUB'].del_sourcefile
    del_sourcefile.restype = ctypes.c_char
    del_sourcefile.argtypes = [ea_t]
    del_sreg_range = _libraries['FIXME_STUB'].del_sreg_range
    del_sreg_range.restype = ctypes.c_char
    del_sreg_range.argtypes = [ea_t, ctypes.c_int32]
    del_stkpnt = _libraries['FIXME_STUB'].del_stkpnt
    del_stkpnt.restype = ctypes.c_char
    del_stkpnt.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    del_str_type = _libraries['FIXME_STUB'].del_str_type
    del_str_type.restype = None
    del_str_type.argtypes = [ea_t]
    del_struc = _libraries['FIXME_STUB'].del_struc
    del_struc.restype = ctypes.c_char
    del_struc.argtypes = [ctypes.POINTER(struct_struc_t)]
    del_struc_member = _libraries['FIXME_STUB'].del_struc_member
    del_struc_member.restype = ctypes.c_char
    del_struc_member.argtypes = [ctypes.POINTER(struct_struc_t), ea_t]
    del_struc_members = _libraries['FIXME_STUB'].del_struc_members
    del_struc_members.restype = ctypes.c_int32
    del_struc_members.argtypes = [ctypes.POINTER(struct_struc_t), ea_t, ea_t]
    del_switch_info = _libraries['FIXME_STUB'].del_switch_info
    del_switch_info.restype = None
    del_switch_info.argtypes = [ea_t]
    del_til = _libraries['FIXME_STUB'].del_til
    del_til.restype = ctypes.c_char
    del_til.argtypes = [ctypes.c_char_p]
    del_tinfo_attr = _libraries['FIXME_STUB'].del_tinfo_attr
    del_tinfo_attr.restype = ctypes.c_char
    del_tinfo_attr.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(qstring), ctypes.c_char]
    del_tryblks = _libraries['FIXME_STUB'].del_tryblks
    del_tryblks.restype = None
    del_tryblks.argtypes = [ctypes.POINTER(struct_range_t)]
    del_value = _libraries['FIXME_STUB'].del_value
    del_value.restype = None
    del_value.argtypes = [ea_t]
    delete_all_xrefs_from = _libraries['FIXME_STUB'].delete_all_xrefs_from
    delete_all_xrefs_from.restype = None
    delete_all_xrefs_from.argtypes = [ea_t, ctypes.c_char]
    delete_dirtree = _libraries['FIXME_STUB'].delete_dirtree
    delete_dirtree.restype = None
    delete_dirtree.argtypes = [ctypes.POINTER(struct_dirtree_impl_t)]
    delete_extra_cmts = _libraries['FIXME_STUB'].delete_extra_cmts
    delete_extra_cmts.restype = None
    delete_extra_cmts.argtypes = [ea_t, ctypes.c_int32]
    delete_imports = _libraries['FIXME_STUB'].delete_imports
    delete_imports.restype = None
    delete_imports.argtypes = []
    delete_switch_table = _libraries['FIXME_STUB'].delete_switch_table
    delete_switch_table.restype = None
    delete_switch_table.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t)]
    delete_unreferenced_stkvars = _libraries['FIXME_STUB'].delete_unreferenced_stkvars
    delete_unreferenced_stkvars.restype = ctypes.c_int32
    delete_unreferenced_stkvars.argtypes = [ctypes.POINTER(struct_func_t)]
    delete_wrong_stkvar_ops = _libraries['FIXME_STUB'].delete_wrong_stkvar_ops
    delete_wrong_stkvar_ops.restype = ctypes.c_int32
    delete_wrong_stkvar_ops.argtypes = [ctypes.POINTER(struct_func_t)]
    delinf = _libraries['FIXME_STUB'].delinf
    delinf.restype = ctypes.c_char
    delinf.argtypes = [inftag_t]
    demangle = _libraries['FIXME_STUB'].demangle
    demangle.restype = int32
    demangle.argtypes = [ctypes.c_char_p, uint, ctypes.c_char_p, uint32]
    demangle_name = _libraries['FIXME_STUB'].demangle_name
    demangle_name.restype = int32
    demangle_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, uint32, demreq_type_t]
    deref_idcv = _libraries['FIXME_STUB'].deref_idcv
    deref_idcv.restype = ctypes.POINTER(struct_idc_value_t)
    deref_idcv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_int32]
    deref_ptr = _libraries['FIXME_STUB'].deref_ptr
    deref_ptr.restype = ctypes.c_char
    deref_ptr.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(ea_t)]
    deserialize_dynamic_register_set = _libraries['FIXME_STUB'].deserialize_dynamic_register_set
    deserialize_dynamic_register_set.restype = None
    deserialize_dynamic_register_set.argtypes = [ctypes.POINTER(struct_dynamic_register_set_t), ctypes.POINTER(struct_memory_deserializer_t)]
    deserialize_tinfo = _libraries['FIXME_STUB'].deserialize_tinfo
    deserialize_tinfo.restype = ctypes.c_char
    deserialize_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_til_t), ctypes.POINTER(ctypes.POINTER(type_t)), ctypes.POINTER(ctypes.POINTER(p_list)), ctypes.POINTER(ctypes.POINTER(p_list))]
    destroy_lexer = _libraries['FIXME_STUB'].destroy_lexer
    destroy_lexer.restype = None
    destroy_lexer.argtypes = [ctypes.POINTER(struct_lexer_t)]
    detach_custom_data_format = _libraries['FIXME_STUB'].detach_custom_data_format
    detach_custom_data_format.restype = ctypes.c_char
    detach_custom_data_format.argtypes = [ctypes.c_int32, ctypes.c_int32]
    determine_rtl = _libraries['FIXME_STUB'].determine_rtl
    determine_rtl.restype = None
    determine_rtl.argtypes = []
    dirtree_change_rank = _libraries['FIXME_STUB'].dirtree_change_rank
    dirtree_change_rank.restype = dterr_t
    dirtree_change_rank.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p, ssize_t]
    dirtree_chdir = _libraries['FIXME_STUB'].dirtree_chdir
    dirtree_chdir.restype = dterr_t
    dirtree_chdir.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_errstr = _libraries['FIXME_STUB'].dirtree_errstr
    dirtree_errstr.restype = ctypes.c_char_p
    dirtree_errstr.argtypes = [dterr_t]
    dirtree_find_entry = _libraries['FIXME_STUB'].dirtree_find_entry
    dirtree_find_entry.restype = dterr_t
    dirtree_find_entry.argtypes = [ctypes.POINTER(struct_dirtree_cursor_t), ctypes.POINTER(struct_dirtree_t), ctypes.POINTER(struct_direntry_t)]
    dirtree_findfirst = _libraries['FIXME_STUB'].dirtree_findfirst
    dirtree_findfirst.restype = ctypes.c_char
    dirtree_findfirst.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_iterator_t), ctypes.c_char_p]
    dirtree_findnext = _libraries['FIXME_STUB'].dirtree_findnext
    dirtree_findnext.restype = ctypes.c_char
    dirtree_findnext.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_iterator_t)]
    dirtree_get_abspath_by_cursor = _libraries['FIXME_STUB'].dirtree_get_abspath_by_cursor
    dirtree_get_abspath_by_cursor.restype = ctypes.c_char
    dirtree_get_abspath_by_cursor.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_cursor_t)]
    dirtree_get_abspath_by_relpath = _libraries['FIXME_STUB'].dirtree_get_abspath_by_relpath
    dirtree_get_abspath_by_relpath.restype = ctypes.c_char
    dirtree_get_abspath_by_relpath.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_get_dir_size = _libraries['FIXME_STUB'].dirtree_get_dir_size
    dirtree_get_dir_size.restype = ssize_t
    dirtree_get_dir_size.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), diridx_t]
    dirtree_get_entry_attrs = _libraries['FIXME_STUB'].dirtree_get_entry_attrs
    dirtree_get_entry_attrs.restype = None
    dirtree_get_entry_attrs.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_direntry_t)]
    dirtree_get_entry_name = _libraries['FIXME_STUB'].dirtree_get_entry_name
    dirtree_get_entry_name.restype = ctypes.c_char
    dirtree_get_entry_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_direntry_t), uint32]
    dirtree_get_id = _libraries['FIXME_STUB'].dirtree_get_id
    dirtree_get_id.restype = ctypes.c_char_p
    dirtree_get_id.argtypes = [ctypes.POINTER(struct_dirtree_impl_t)]
    dirtree_get_nodename = _libraries['FIXME_STUB'].dirtree_get_nodename
    dirtree_get_nodename.restype = ctypes.c_char_p
    dirtree_get_nodename.argtypes = [ctypes.POINTER(struct_dirtree_impl_t)]
    dirtree_get_parent_cursor = _libraries['FIXME_STUB'].dirtree_get_parent_cursor
    dirtree_get_parent_cursor.restype = None
    dirtree_get_parent_cursor.argtypes = [ctypes.POINTER(struct_dirtree_cursor_t), ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_cursor_t)]
    dirtree_get_rank = _libraries['FIXME_STUB'].dirtree_get_rank
    dirtree_get_rank.restype = ssize_t
    dirtree_get_rank.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), diridx_t, ctypes.POINTER(struct_direntry_t)]
    dirtree_getcwd = _libraries['FIXME_STUB'].dirtree_getcwd
    dirtree_getcwd.restype = None
    dirtree_getcwd.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_dirtree_impl_t)]
    dirtree_link_inode = _libraries['FIXME_STUB'].dirtree_link_inode
    dirtree_link_inode.restype = dterr_t
    dirtree_link_inode.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), inode_t, ctypes.c_char]
    dirtree_rename = _libraries['FIXME_STUB'].dirtree_rename
    dirtree_rename.restype = dterr_t
    dirtree_rename.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p, ctypes.c_char_p]
    dirtree_resolve_cursor = _libraries['FIXME_STUB'].dirtree_resolve_cursor
    dirtree_resolve_cursor.restype = None
    dirtree_resolve_cursor.argtypes = [ctypes.POINTER(struct_direntry_t), ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_cursor_t)]
    dirtree_resolve_path = _libraries['FIXME_STUB'].dirtree_resolve_path
    dirtree_resolve_path.restype = None
    dirtree_resolve_path.argtypes = [ctypes.POINTER(struct_direntry_t), ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_set_id = _libraries['FIXME_STUB'].dirtree_set_id
    dirtree_set_id.restype = None
    dirtree_set_id.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_set_nodename = _libraries['FIXME_STUB'].dirtree_set_nodename
    dirtree_set_nodename.restype = None
    dirtree_set_nodename.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char_p]
    dirtree_traverse = _libraries['FIXME_STUB'].dirtree_traverse
    dirtree_traverse.restype = ssize_t
    dirtree_traverse.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.POINTER(struct_dirtree_visitor_t)]
    disable_flags = _libraries['FIXME_STUB'].disable_flags
    disable_flags.restype = error_t
    disable_flags.argtypes = [ea_t, ea_t]
    display_gdl = _libraries['FIXME_STUB'].display_gdl
    display_gdl.restype = ctypes.c_int32
    display_gdl.argtypes = [ctypes.c_char_p]
    dstr_tinfo = _libraries['FIXME_STUB'].dstr_tinfo
    dstr_tinfo.restype = ctypes.c_char_p
    dstr_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t)]
    dummy_name_ea = _libraries['FIXME_STUB'].dummy_name_ea
    dummy_name_ea.restype = ea_t
    dummy_name_ea.argtypes = [ctypes.c_char_p]
    dump_func_type_data = _libraries['FIXME_STUB'].dump_func_type_data
    dump_func_type_data.restype = ctypes.c_char
    dump_func_type_data.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_func_type_data_t), ctypes.c_int32]
    ea2node = _libraries['FIXME_STUB'].ea2node
    ea2node.restype = nodeidx_t
    ea2node.argtypes = [ea_t]
    ea2str = _libraries['FIXME_STUB'].ea2str
    ea2str.restype = size_t
    ea2str.argtypes = [ctypes.c_char_p, size_t, ea_t]
    eadd = _libraries['FIXME_STUB'].eadd
    eadd.restype = fpvalue_error_t
    eadd.argtypes = [ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t), ctypes.c_char]
    echsize = _libraries['FIXME_STUB'].echsize
    echsize.restype = None
    echsize.argtypes = [ctypes.POINTER(FILE), uint64]
    eclose = _libraries['FIXME_STUB'].eclose
    eclose.restype = None
    eclose.argtypes = [ctypes.POINTER(FILE)]
    ecmp = _libraries['FIXME_STUB'].ecmp
    ecmp.restype = ctypes.c_int32
    ecmp.argtypes = [ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t)]
    ecreate = _libraries['FIXME_STUB'].ecreate
    ecreate.restype = ctypes.POINTER(FILE)
    ecreate.argtypes = [ctypes.c_char_p]
    ediv = _libraries['FIXME_STUB'].ediv
    ediv.restype = fpvalue_error_t
    ediv.argtypes = [ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t)]
    eetol = _libraries['FIXME_STUB'].eetol
    eetol.restype = fpvalue_error_t
    eetol.argtypes = [ctypes.POINTER(sval_t), ctypes.POINTER(struct_fpvalue_t), ctypes.c_char]
    eetol64 = _libraries['FIXME_STUB'].eetol64
    eetol64.restype = fpvalue_error_t
    eetol64.argtypes = [ctypes.POINTER(int64), ctypes.POINTER(struct_fpvalue_t), ctypes.c_char]
    eetol64u = _libraries['FIXME_STUB'].eetol64u
    eetol64u.restype = fpvalue_error_t
    eetol64u.argtypes = [ctypes.POINTER(uint64), ctypes.POINTER(struct_fpvalue_t), ctypes.c_char]
    eldexp = _libraries['FIXME_STUB'].eldexp
    eldexp.restype = fpvalue_error_t
    eldexp.argtypes = [ctypes.POINTER(struct_fpvalue_t), int32, ctypes.POINTER(struct_fpvalue_t)]
    eltoe = _libraries['FIXME_STUB'].eltoe
    eltoe.restype = None
    eltoe.argtypes = [sval_t, ctypes.POINTER(struct_fpvalue_t)]
    eltoe64 = _libraries['FIXME_STUB'].eltoe64
    eltoe64.restype = None
    eltoe64.argtypes = [int64, ctypes.POINTER(struct_fpvalue_t)]
    eltoe64u = _libraries['FIXME_STUB'].eltoe64u
    eltoe64u.restype = None
    eltoe64u.argtypes = [uint64, ctypes.POINTER(struct_fpvalue_t)]
    emdnorm = _libraries['FIXME_STUB'].emdnorm
    emdnorm.restype = ctypes.c_char
    emdnorm.argtypes = [eNI, ctypes.c_char, ctypes.c_char, int32, ctypes.c_int32]
    emovi = _libraries['FIXME_STUB'].emovi
    emovi.restype = None
    emovi.argtypes = [ctypes.POINTER(struct_fpvalue_t), eNI]
    emovo = _libraries['FIXME_STUB'].emovo
    emovo.restype = None
    emovo.argtypes = [eNI, ctypes.POINTER(struct_fpvalue_t)]
    emul = _libraries['FIXME_STUB'].emul
    emul.restype = fpvalue_error_t
    emul.argtypes = [ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t), ctypes.POINTER(struct_fpvalue_t)]
    enable_auto = _libraries['FIXME_STUB'].enable_auto
    enable_auto.restype = ctypes.c_char
    enable_auto.argtypes = [ctypes.c_char]
    enable_flags = _libraries['FIXME_STUB'].enable_flags
    enable_flags.restype = error_t
    enable_flags.argtypes = [ea_t, ea_t, storage_type_t]
    enable_numbered_types = _libraries['FIXME_STUB'].enable_numbered_types
    enable_numbered_types.restype = ctypes.c_char
    enable_numbered_types.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char]
    end_type_updating = _libraries['FIXME_STUB'].end_type_updating
    end_type_updating.restype = None
    end_type_updating.argtypes = [update_type_t]
    enum_import_names = _libraries['FIXME_STUB'].enum_import_names
    enum_import_names.restype = ctypes.c_int32
    enum_import_names.argtypes = [ctypes.c_int32, ctypes.CFUNCTYPE(ctypes.c_int32, ea_t, ctypes.c_char_p, uval_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    enumerate_files = _libraries['FIXME_STUB'].enumerate_files
    enumerate_files.restype = ctypes.c_int32
    enumerate_files.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(None)), ctypes.POINTER(None)]
    enumerate_files2 = _libraries['FIXME_STUB'].enumerate_files2
    enumerate_files2.restype = ctypes.c_int32
    enumerate_files2.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(struct_file_enumerator_t)]
    enumerate_segments_with_selector = _libraries['FIXME_STUB'].enumerate_segments_with_selector
    enumerate_segments_with_selector.restype = ea_t
    enumerate_segments_with_selector.argtypes = [sel_t, ctypes.CFUNCTYPE(ea_t, ctypes.POINTER(struct_segment_t), ctypes.POINTER(None)), ctypes.POINTER(None)]
    enumerate_selectors = _libraries['FIXME_STUB'].enumerate_selectors
    enumerate_selectors.restype = ctypes.c_int32
    enumerate_selectors.argtypes = [ctypes.CFUNCTYPE(ctypes.c_int32, sel_t, ea_t)]
    enumplace_t__adjust = _libraries['FIXME_STUB'].enumplace_t__adjust
    enumplace_t__adjust.restype = None
    enumplace_t__adjust.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    enumplace_t__beginning = _libraries['FIXME_STUB'].enumplace_t__beginning
    enumplace_t__beginning.restype = ctypes.c_char
    enumplace_t__beginning.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    enumplace_t__clone = _libraries['FIXME_STUB'].enumplace_t__clone
    enumplace_t__clone.restype = ctypes.POINTER(struct_place_t)
    enumplace_t__clone.argtypes = [ctypes.POINTER(struct_enumplace_t)]
    enumplace_t__compare = _libraries['FIXME_STUB'].enumplace_t__compare
    enumplace_t__compare.restype = ctypes.c_int32
    enumplace_t__compare.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(struct_place_t)]
    enumplace_t__compare2 = _libraries['FIXME_STUB'].enumplace_t__compare2
    enumplace_t__compare2.restype = ctypes.c_int32
    enumplace_t__compare2.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    enumplace_t__copyfrom = _libraries['FIXME_STUB'].enumplace_t__copyfrom
    enumplace_t__copyfrom.restype = None
    enumplace_t__copyfrom.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(struct_place_t)]
    enumplace_t__deserialize = _libraries['FIXME_STUB'].enumplace_t__deserialize
    enumplace_t__deserialize.restype = ctypes.c_char
    enumplace_t__deserialize.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    enumplace_t__ending = _libraries['FIXME_STUB'].enumplace_t__ending
    enumplace_t__ending.restype = ctypes.c_char
    enumplace_t__ending.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    enumplace_t__enter = _libraries['FIXME_STUB'].enumplace_t__enter
    enumplace_t__enter.restype = ctypes.POINTER(struct_place_t)
    enumplace_t__enter.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(uint32)]
    enumplace_t__generate = _libraries['FIXME_STUB'].enumplace_t__generate
    enumplace_t__generate.restype = ctypes.c_int32
    enumplace_t__generate.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(color_t), ctypes.POINTER(bgcolor_t), ctypes.POINTER(None), ctypes.c_int32]
    enumplace_t__id = _libraries['FIXME_STUB'].enumplace_t__id
    enumplace_t__id.restype = ctypes.c_int32
    enumplace_t__id.argtypes = [ctypes.POINTER(struct_enumplace_t)]
    enumplace_t__leave = _libraries['FIXME_STUB'].enumplace_t__leave
    enumplace_t__leave.restype = None
    enumplace_t__leave.argtypes = [ctypes.POINTER(struct_enumplace_t), uint32]
    enumplace_t__makeplace = _libraries['FIXME_STUB'].enumplace_t__makeplace
    enumplace_t__makeplace.restype = ctypes.POINTER(struct_place_t)
    enumplace_t__makeplace.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None), uval_t, ctypes.c_int32]
    enumplace_t__name = _libraries['FIXME_STUB'].enumplace_t__name
    enumplace_t__name.restype = ctypes.c_char_p
    enumplace_t__name.argtypes = [ctypes.POINTER(struct_enumplace_t)]
    enumplace_t__next = _libraries['FIXME_STUB'].enumplace_t__next
    enumplace_t__next.restype = ctypes.c_char
    enumplace_t__next.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    enumplace_t__prev = _libraries['FIXME_STUB'].enumplace_t__prev
    enumplace_t__prev.restype = ctypes.c_char
    enumplace_t__prev.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    enumplace_t__print = _libraries['FIXME_STUB'].enumplace_t__print
    enumplace_t__print.restype = None
    enumplace_t__print.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(qstring), ctypes.POINTER(None)]
    enumplace_t__rebase = _libraries['FIXME_STUB'].enumplace_t__rebase
    enumplace_t__rebase.restype = ctypes.c_char
    enumplace_t__rebase.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(struct_segm_move_infos_t)]
    enumplace_t__serialize = _libraries['FIXME_STUB'].enumplace_t__serialize
    enumplace_t__serialize.restype = None
    enumplace_t__serialize.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(struct_bytevec_t)]
    enumplace_t__toea = _libraries['FIXME_STUB'].enumplace_t__toea
    enumplace_t__toea.restype = ea_t
    enumplace_t__toea.argtypes = [ctypes.POINTER(struct_enumplace_t)]
    enumplace_t__touval = _libraries['FIXME_STUB'].enumplace_t__touval
    enumplace_t__touval.restype = uval_t
    enumplace_t__touval.argtypes = [ctypes.POINTER(struct_enumplace_t), ctypes.POINTER(None)]
    equal_bytes = _libraries['FIXME_STUB'].equal_bytes
    equal_bytes.restype = ctypes.c_char
    equal_bytes.argtypes = [ea_t, ctypes.POINTER(uchar), ctypes.POINTER(uchar), size_t, ctypes.c_int32]
    eread = _libraries['FIXME_STUB'].eread
    eread.restype = None
    eread.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), size_t]
    errorexit = ctypes_in_dll(ctypes.c_int32, _libraries['FIXME_STUB'], 'errorexit')
    eseek = _libraries['FIXME_STUB'].eseek
    eseek.restype = None
    eseek.argtypes = [ctypes.POINTER(FILE), int64]
    eshift = _libraries['FIXME_STUB'].eshift
    eshift.restype = ctypes.c_int32
    eshift.argtypes = [eNI, ctypes.c_int32]
    eval_expr = _libraries['FIXME_STUB'].eval_expr
    eval_expr.restype = ctypes.c_char
    eval_expr.argtypes = [ctypes.POINTER(struct_idc_value_t), ea_t, ctypes.c_char_p, ctypes.POINTER(qstring)]
    eval_expr_long = _libraries['FIXME_STUB'].eval_expr_long
    eval_expr_long.restype = ctypes.c_char
    eval_expr_long.argtypes = [ctypes.POINTER(sval_t), ea_t, ctypes.c_char_p, ctypes.POINTER(qstring)]
    eval_idc_expr = _libraries['FIXME_STUB'].eval_idc_expr
    eval_idc_expr.restype = ctypes.c_char
    eval_idc_expr.argtypes = [ctypes.POINTER(struct_idc_value_t), ea_t, ctypes.c_char_p, ctypes.POINTER(qstring)]
    eval_idc_snippet = _libraries['FIXME_STUB'].eval_idc_snippet
    eval_idc_snippet.restype = ctypes.c_char
    eval_idc_snippet.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_resolver_t)]
    ewrite = _libraries['FIXME_STUB'].ewrite
    ewrite.restype = None
    ewrite.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), size_t]
    exec_system_script = _libraries['FIXME_STUB'].exec_system_script
    exec_system_script.restype = ctypes.c_char
    exec_system_script.argtypes = [ctypes.c_char_p, ctypes.c_char]
    expand_struc = _libraries['FIXME_STUB'].expand_struc
    expand_struc.restype = ctypes.c_char
    expand_struc.argtypes = [ctypes.POINTER(struct_struc_t), ea_t, adiff_t, ctypes.c_char]
    extend_sign = _libraries['FIXME_STUB'].extend_sign
    extend_sign.restype = uint64
    extend_sign.argtypes = [uint64, ctypes.c_int32, ctypes.c_char]
    extract_argloc = _libraries['FIXME_STUB'].extract_argloc
    extract_argloc.restype = ctypes.c_char
    extract_argloc.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.POINTER(ctypes.POINTER(type_t)), ctypes.c_char]
    extract_module_from_archive = _libraries['FIXME_STUB'].extract_module_from_archive
    extract_module_from_archive.restype = ctypes.c_char
    extract_module_from_archive.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(ctypes.c_char_p), ctypes.c_char]
    extract_name = _libraries['FIXME_STUB'].extract_name
    extract_name.restype = ssize_t
    extract_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    fc_calc_block_type = _libraries['FIXME_STUB'].fc_calc_block_type
    fc_calc_block_type.restype = fc_block_type_t
    fc_calc_block_type.argtypes = [ctypes.POINTER(struct_qflow_chart_t), size_t]
    file2base = _libraries['FIXME_STUB'].file2base
    file2base.restype = ctypes.c_int32
    file2base.argtypes = [ctypes.POINTER(struct_linput_t), int64, ea_t, ea_t, ctypes.c_int32]
    find_binary = _libraries['FIXME_STUB'].find_binary
    find_binary.restype = ea_t
    find_binary.argtypes = [ea_t, ea_t, ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    find_byte = _libraries['FIXME_STUB'].find_byte
    find_byte.restype = ea_t
    find_byte.argtypes = [ea_t, asize_t, uchar, ctypes.c_int32]
    find_byter = _libraries['FIXME_STUB'].find_byter
    find_byter.restype = ea_t
    find_byter.argtypes = [ea_t, asize_t, uchar, ctypes.c_int32]
    find_code = _libraries['FIXME_STUB'].find_code
    find_code.restype = ea_t
    find_code.argtypes = [ea_t, ctypes.c_int32]
    find_custom_data_format = _libraries['FIXME_STUB'].find_custom_data_format
    find_custom_data_format.restype = ctypes.c_int32
    find_custom_data_format.argtypes = [ctypes.c_char_p]
    find_custom_data_type = _libraries['FIXME_STUB'].find_custom_data_type
    find_custom_data_type.restype = ctypes.c_int32
    find_custom_data_type.argtypes = [ctypes.c_char_p]
    find_custom_fixup = _libraries['FIXME_STUB'].find_custom_fixup
    find_custom_fixup.restype = fixup_type_t
    find_custom_fixup.argtypes = [ctypes.c_char_p]
    find_custom_refinfo = _libraries['FIXME_STUB'].find_custom_refinfo
    find_custom_refinfo.restype = ctypes.c_int32
    find_custom_refinfo.argtypes = [ctypes.c_char_p]
    find_data = _libraries['FIXME_STUB'].find_data
    find_data.restype = ea_t
    find_data.argtypes = [ea_t, ctypes.c_int32]
    find_defined = _libraries['FIXME_STUB'].find_defined
    find_defined.restype = ea_t
    find_defined.argtypes = [ea_t, ctypes.c_int32]
    find_defjump_from_table = _libraries['FIXME_STUB'].find_defjump_from_table
    find_defjump_from_table.restype = ea_t
    find_defjump_from_table.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t)]
    find_error = _libraries['FIXME_STUB'].find_error
    find_error.restype = ea_t
    find_error.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
    find_extlang = _libraries['FIXME_STUB'].find_extlang
    find_extlang.restype = ctypes.POINTER(None)
    find_extlang.argtypes = [ctypes.POINTER(None), find_extlang_kind_t]
    find_free_selector = _libraries['FIXME_STUB'].find_free_selector
    find_free_selector.restype = sel_t
    find_free_selector.argtypes = []
    find_func_bounds = _libraries['FIXME_STUB'].find_func_bounds
    find_func_bounds.restype = ctypes.c_int32
    find_func_bounds.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_int32]
    find_idc_class = _libraries['FIXME_STUB'].find_idc_class
    find_idc_class.restype = ctypes.POINTER(struct_idc_class_t)
    find_idc_class.argtypes = [ctypes.c_char_p]
    find_idc_func = _libraries['FIXME_STUB'].find_idc_func
    find_idc_func.restype = ctypes.c_char
    find_idc_func.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    find_idc_gvar = _libraries['FIXME_STUB'].find_idc_gvar
    find_idc_gvar.restype = ctypes.POINTER(struct_idc_value_t)
    find_idc_gvar.argtypes = [ctypes.c_char_p]
    find_imm = _libraries['FIXME_STUB'].find_imm
    find_imm.restype = ea_t
    find_imm.argtypes = [ea_t, ctypes.c_int32, uval_t, ctypes.POINTER(ctypes.c_int32)]
    find_ioport = _libraries['FIXME_STUB'].find_ioport
    find_ioport.restype = ctypes.POINTER(struct_ioport_t)
    find_ioport.argtypes = [ctypes.POINTER(ioports_t), ea_t]
    find_ioport_bit = _libraries['FIXME_STUB'].find_ioport_bit
    find_ioport_bit.restype = ctypes.POINTER(struct_ioport_bit_t)
    find_ioport_bit.argtypes = [ctypes.POINTER(ioports_t), ea_t, size_t]
    find_jtable_size = _libraries['FIXME_STUB'].find_jtable_size
    find_jtable_size.restype = ctypes.c_char
    find_jtable_size.argtypes = [ctypes.POINTER(struct_switch_info_t)]
    find_not_func = _libraries['FIXME_STUB'].find_not_func
    find_not_func.restype = ea_t
    find_not_func.argtypes = [ea_t, ctypes.c_int32]
    find_notype = _libraries['FIXME_STUB'].find_notype
    find_notype.restype = ea_t
    find_notype.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
    find_plugin = _libraries['FIXME_STUB'].find_plugin
    find_plugin.restype = ctypes.POINTER(struct_plugin_t)
    find_plugin.argtypes = [ctypes.c_char_p, ctypes.c_char]
    find_reg_access = _libraries['FIXME_STUB'].find_reg_access
    find_reg_access.restype = ea_t
    find_reg_access.argtypes = [ctypes.POINTER(struct_reg_access_t), ea_t, ea_t, ctypes.c_char_p, ctypes.c_int32]
    find_regvar = _libraries['FIXME_STUB'].find_regvar
    find_regvar.restype = ctypes.POINTER(struct_regvar_t)
    find_regvar.argtypes = [ctypes.POINTER(struct_func_t), ea_t, ea_t, ctypes.c_char_p, ctypes.c_char_p]
    find_selector = _libraries['FIXME_STUB'].find_selector
    find_selector.restype = sel_t
    find_selector.argtypes = [ea_t]
    find_suspop = _libraries['FIXME_STUB'].find_suspop
    find_suspop.restype = ea_t
    find_suspop.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
    find_syseh = _libraries['FIXME_STUB'].find_syseh
    find_syseh.restype = ea_t
    find_syseh.argtypes = [ea_t]
    find_text = _libraries['FIXME_STUB'].find_text
    find_text.restype = ea_t
    find_text.argtypes = [ea_t, ctypes.c_int32, ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32]
    find_tinfo_udt_member = _libraries['FIXME_STUB'].find_tinfo_udt_member
    find_tinfo_udt_member.restype = ctypes.c_int32
    find_tinfo_udt_member.argtypes = [ctypes.POINTER(struct_udt_member_t), uint32, ctypes.c_int32]
    find_unknown = _libraries['FIXME_STUB'].find_unknown
    find_unknown.restype = ea_t
    find_unknown.argtypes = [ea_t, ctypes.c_int32]
    first_idcv_attr = _libraries['FIXME_STUB'].first_idcv_attr
    first_idcv_attr.restype = ctypes.c_char_p
    first_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    first_named_type = _libraries['FIXME_STUB'].first_named_type
    first_named_type.restype = ctypes.c_char_p
    first_named_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_int32]
    flush_buffers = _libraries['FIXME_STUB'].flush_buffers
    flush_buffers.restype = ctypes.c_int32
    flush_buffers.argtypes = []
    fopenA = _libraries['FIXME_STUB'].fopenA
    fopenA.restype = ctypes.POINTER(FILE)
    fopenA.argtypes = [ctypes.c_char_p]
    fopenM = _libraries['FIXME_STUB'].fopenM
    fopenM.restype = ctypes.POINTER(FILE)
    fopenM.argtypes = [ctypes.c_char_p]
    fopenRB = _libraries['FIXME_STUB'].fopenRB
    fopenRB.restype = ctypes.POINTER(FILE)
    fopenRB.argtypes = [ctypes.c_char_p]
    fopenRT = _libraries['FIXME_STUB'].fopenRT
    fopenRT.restype = ctypes.POINTER(FILE)
    fopenRT.argtypes = [ctypes.c_char_p]
    fopenWB = _libraries['FIXME_STUB'].fopenWB
    fopenWB.restype = ctypes.POINTER(FILE)
    fopenWB.argtypes = [ctypes.c_char_p]
    fopenWT = _libraries['FIXME_STUB'].fopenWT
    fopenWT.restype = ctypes.POINTER(FILE)
    fopenWT.argtypes = [ctypes.c_char_p]
    for_all_arglocs = _libraries['FIXME_STUB'].for_all_arglocs
    for_all_arglocs.restype = ctypes.c_int32
    for_all_arglocs.argtypes = [ctypes.POINTER(struct_aloc_visitor_t), ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.c_int32]
    for_all_enum_members = _libraries['FIXME_STUB'].for_all_enum_members
    for_all_enum_members.restype = ctypes.c_int32
    for_all_enum_members.argtypes = [enum_t, ctypes.POINTER(struct_enum_member_visitor_t)]
    for_all_extlangs = _libraries['FIXME_STUB'].for_all_extlangs
    for_all_extlangs.restype = ssize_t
    for_all_extlangs.argtypes = [ctypes.POINTER(struct_extlang_visitor_t), ctypes.c_char]
    forget_problem = _libraries['FIXME_STUB'].forget_problem
    forget_problem.restype = ctypes.c_char
    forget_problem.argtypes = [problist_id_t, ea_t]
    format_c_number = _libraries['FIXME_STUB'].format_c_number
    format_c_number.restype = size_t
    format_c_number.argtypes = [ctypes.c_char_p, size_t, struct_uint128, ctypes.c_int32, ctypes.c_int32]
    format_cdata = _libraries['FIXME_STUB'].format_cdata
    format_cdata.restype = ctypes.c_char
    format_cdata.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_valstr_t), ctypes.POINTER(struct_format_data_info_t)]
    format_charlit = _libraries['FIXME_STUB'].format_charlit
    format_charlit.restype = ctypes.c_char
    format_charlit.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(ctypes.POINTER(uchar)), size_t, uint32, ctypes.c_int32]
    freadbytes = _libraries['FIXME_STUB'].freadbytes
    freadbytes.restype = ctypes.c_int32
    freadbytes.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), ctypes.c_int32, ctypes.c_int32]
    free_chunk = _libraries['FIXME_STUB'].free_chunk
    free_chunk.restype = ea_t
    free_chunk.argtypes = [ea_t, asize_t, int32]
    free_debug_event = _libraries['FIXME_STUB'].free_debug_event
    free_debug_event.restype = None
    free_debug_event.argtypes = [ctypes.POINTER(struct_debug_event_t)]
    free_dll = _libraries['FIXME_STUB'].free_dll
    free_dll.restype = None
    free_dll.argtypes = [ctypes.POINTER(struct_idadll_t)]
    free_idcv = _libraries['FIXME_STUB'].free_idcv
    free_idcv.restype = None
    free_idcv.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    free_loaders_list = _libraries['FIXME_STUB'].free_loaders_list
    free_loaders_list.restype = None
    free_loaders_list.argtypes = [ctypes.POINTER(struct_load_info_t)]
    free_regarg = _libraries['FIXME_STUB'].free_regarg
    free_regarg.restype = None
    free_regarg.argtypes = [ctypes.POINTER(struct_regarg_t)]
    free_regvar = _libraries['FIXME_STUB'].free_regvar
    free_regvar.restype = None
    free_regvar.argtypes = [ctypes.POINTER(struct_regvar_t)]
    free_til = _libraries['FIXME_STUB'].free_til
    free_til.restype = None
    free_til.argtypes = [ctypes.POINTER(struct_til_t)]
    func_does_return = _libraries['FIXME_STUB'].func_does_return
    func_does_return.restype = ctypes.c_char
    func_does_return.argtypes = [ea_t]
    func_has_stkframe_hole = _libraries['FIXME_STUB'].func_has_stkframe_hole
    func_has_stkframe_hole.restype = ctypes.c_char
    func_has_stkframe_hole.argtypes = [ea_t, ctypes.POINTER(struct_func_type_data_t)]
    func_item_iterator_decode_preceding_insn = _libraries['FIXME_STUB'].func_item_iterator_decode_preceding_insn
    func_item_iterator_decode_preceding_insn.restype = ctypes.c_char
    func_item_iterator_decode_preceding_insn.argtypes = [ctypes.POINTER(struct_func_item_iterator_t), ctypes.POINTER(eavec_t), ctypes.c_char_p, ctypes.POINTER(struct_insn_t)]
    func_item_iterator_decode_prev_insn = _libraries['FIXME_STUB'].func_item_iterator_decode_prev_insn
    func_item_iterator_decode_prev_insn.restype = ctypes.c_char
    func_item_iterator_decode_prev_insn.argtypes = [ctypes.POINTER(struct_func_item_iterator_t), ctypes.POINTER(struct_insn_t)]
    func_item_iterator_next = _libraries['FIXME_STUB'].func_item_iterator_next
    func_item_iterator_next.restype = ctypes.c_char
    func_item_iterator_next.argtypes = [ctypes.POINTER(struct_func_item_iterator_t), ctypes.CFUNCTYPE(ctypes.c_char, flags_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    func_item_iterator_prev = _libraries['FIXME_STUB'].func_item_iterator_prev
    func_item_iterator_prev.restype = ctypes.c_char
    func_item_iterator_prev.argtypes = [ctypes.POINTER(struct_func_item_iterator_t), ctypes.CFUNCTYPE(ctypes.c_char, flags_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    func_item_iterator_succ = _libraries['FIXME_STUB'].func_item_iterator_succ
    func_item_iterator_succ.restype = ctypes.c_char
    func_item_iterator_succ.argtypes = [ctypes.POINTER(struct_func_item_iterator_t), ctypes.CFUNCTYPE(ctypes.c_char, flags_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    func_parent_iterator_set = _libraries['FIXME_STUB'].func_parent_iterator_set
    func_parent_iterator_set.restype = ctypes.c_char
    func_parent_iterator_set.argtypes = [ctypes.POINTER(struct_func_parent_iterator_t), ctypes.POINTER(struct_func_t)]
    func_tail_iterator_set = _libraries['FIXME_STUB'].func_tail_iterator_set
    func_tail_iterator_set.restype = ctypes.c_char
    func_tail_iterator_set.argtypes = [ctypes.POINTER(struct_func_tail_iterator_t), ctypes.POINTER(struct_func_t), ea_t]
    func_tail_iterator_set_ea = _libraries['FIXME_STUB'].func_tail_iterator_set_ea
    func_tail_iterator_set_ea.restype = ctypes.c_char
    func_tail_iterator_set_ea.argtypes = [ctypes.POINTER(struct_func_tail_iterator_t), ea_t]
    fwritebytes = _libraries['FIXME_STUB'].fwritebytes
    fwritebytes.restype = ctypes.c_int32
    fwritebytes.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), ctypes.c_int32, ctypes.c_int32]
    gen_complex_call_chart = _libraries['FIXME_STUB'].gen_complex_call_chart
    gen_complex_call_chart.restype = ctypes.c_char
    gen_complex_call_chart.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ea_t, ea_t, ctypes.c_int32, int32]
    gen_decorate_name = _libraries['FIXME_STUB'].gen_decorate_name
    gen_decorate_name.restype = ctypes.c_char
    gen_decorate_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_char, cm_t, ctypes.POINTER(struct_tinfo_t)]
    gen_exe_file = _libraries['FIXME_STUB'].gen_exe_file
    gen_exe_file.restype = ctypes.c_int32
    gen_exe_file.argtypes = [ctypes.POINTER(FILE)]
    gen_file = _libraries['FIXME_STUB'].gen_file
    gen_file.restype = ctypes.c_int32
    gen_file.argtypes = [ofile_type_t, ctypes.POINTER(FILE), ea_t, ea_t, ctypes.c_int32]
    gen_fix_fixups = _libraries['FIXME_STUB'].gen_fix_fixups
    gen_fix_fixups.restype = None
    gen_fix_fixups.argtypes = [ea_t, ea_t, asize_t]
    gen_flow_graph = _libraries['FIXME_STUB'].gen_flow_graph
    gen_flow_graph.restype = ctypes.c_char
    gen_flow_graph.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(struct_func_t), ea_t, ea_t, ctypes.c_int32]
    gen_gdl = _libraries['FIXME_STUB'].gen_gdl
    gen_gdl.restype = None
    gen_gdl.argtypes = [ctypes.POINTER(struct_gdl_graph_t), ctypes.c_char_p]
    gen_rand_buf = _libraries['FIXME_STUB'].gen_rand_buf
    gen_rand_buf.restype = ctypes.c_char
    gen_rand_buf.argtypes = [ctypes.POINTER(None), size_t]
    gen_simple_call_chart = _libraries['FIXME_STUB'].gen_simple_call_chart
    gen_simple_call_chart.restype = ctypes.c_char
    gen_simple_call_chart.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]
    gen_use_arg_tinfos = _libraries['FIXME_STUB'].gen_use_arg_tinfos
    gen_use_arg_tinfos.restype = None
    gen_use_arg_tinfos.argtypes = [ea_t, ctypes.POINTER(struct_func_type_data_t), ctypes.POINTER(funcargvec_t), ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p), ctypes.CFUNCTYPE(ctypes.c_char, ctypes.POINTER(struct_insn_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)), ctypes.CFUNCTYPE(ctypes.c_char, ea_t)]
    gen_use_arg_tinfos2 = _libraries['FIXME_STUB'].gen_use_arg_tinfos2
    gen_use_arg_tinfos2.restype = None
    gen_use_arg_tinfos2.argtypes = [ctypes.POINTER(struct_argtinfo_helper_t), ea_t, ctypes.POINTER(struct_func_type_data_t), ctypes.POINTER(funcargvec_t)]
    generate_disasm_line = _libraries['FIXME_STUB'].generate_disasm_line
    generate_disasm_line.restype = ctypes.c_char
    generate_disasm_line.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32]
    generate_disassembly = _libraries['FIXME_STUB'].generate_disassembly
    generate_disassembly.restype = ctypes.c_int32
    generate_disassembly.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ea_t, ctypes.c_int32, ctypes.c_char]
    get_16bit = _libraries['FIXME_STUB'].get_16bit
    get_16bit.restype = uint32
    get_16bit.argtypes = [ea_t]
    get_32bit = _libraries['FIXME_STUB'].get_32bit
    get_32bit.restype = uint32
    get_32bit.argtypes = [ea_t]
    get_64bit = _libraries['FIXME_STUB'].get_64bit
    get_64bit.restype = uint64
    get_64bit.argtypes = [ea_t]
    get_8bit = _libraries['FIXME_STUB'].get_8bit
    get_8bit.restype = uchar
    get_8bit.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(uint32), ctypes.POINTER(ctypes.c_int32)]
    get_abi_name = _libraries['FIXME_STUB'].get_abi_name
    get_abi_name.restype = ssize_t
    get_abi_name.argtypes = [ctypes.POINTER(qstring)]
    get_aflags = _libraries['FIXME_STUB'].get_aflags
    get_aflags.restype = aflags_t
    get_aflags.argtypes = [ea_t]
    get_alias_target = _libraries['FIXME_STUB'].get_alias_target
    get_alias_target.restype = uint32
    get_alias_target.argtypes = [ctypes.POINTER(struct_til_t), uint32]
    get_arg_addrs = _libraries['FIXME_STUB'].get_arg_addrs
    get_arg_addrs.restype = ctypes.c_char
    get_arg_addrs.argtypes = [ctypes.POINTER(eavec_t), ea_t]
    get_array_parameters = _libraries['FIXME_STUB'].get_array_parameters
    get_array_parameters.restype = ssize_t
    get_array_parameters.argtypes = [ctypes.POINTER(struct_array_parameters_t), ea_t]
    get_ash = _libraries['FIXME_STUB'].get_ash
    get_ash.restype = ctypes.POINTER(struct_asm_t)
    get_ash.argtypes = []
    get_auto_display = _libraries['FIXME_STUB'].get_auto_display
    get_auto_display.restype = ctypes.c_char
    get_auto_display.argtypes = [ctypes.POINTER(struct_auto_display_t)]
    get_auto_state = _libraries['FIXME_STUB'].get_auto_state
    get_auto_state.restype = atype_t
    get_auto_state.argtypes = []
    get_basic_file_type = _libraries['FIXME_STUB'].get_basic_file_type
    get_basic_file_type.restype = filetype_t
    get_basic_file_type.argtypes = [ctypes.POINTER(struct_linput_t)]
    get_best_fit_member = _libraries['FIXME_STUB'].get_best_fit_member
    get_best_fit_member.restype = ctypes.POINTER(struct_member_t)
    get_best_fit_member.argtypes = [ctypes.POINTER(struct_struc_t), asize_t]
    get_bmask_cmt = _libraries['FIXME_STUB'].get_bmask_cmt
    get_bmask_cmt.restype = ssize_t
    get_bmask_cmt.argtypes = [ctypes.POINTER(qstring), enum_t, bmask_t, ctypes.c_char]
    get_bmask_name = _libraries['FIXME_STUB'].get_bmask_name
    get_bmask_name.restype = ssize_t
    get_bmask_name.argtypes = [ctypes.POINTER(qstring), enum_t, bmask_t]
    get_byte = _libraries['FIXME_STUB'].get_byte
    get_byte.restype = uchar
    get_byte.argtypes = [ea_t]
    get_bytes = _libraries['FIXME_STUB'].get_bytes
    get_bytes.restype = ssize_t
    get_bytes.argtypes = [ctypes.POINTER(None), ssize_t, ea_t, ctypes.c_int32, ctypes.POINTER(None)]
    get_cmt = _libraries['FIXME_STUB'].get_cmt
    get_cmt.restype = ssize_t
    get_cmt.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_char]
    get_compiler_abbr = _libraries['FIXME_STUB'].get_compiler_abbr
    get_compiler_abbr.restype = ctypes.c_char_p
    get_compiler_abbr.argtypes = [comp_t]
    get_compiler_name = _libraries['FIXME_STUB'].get_compiler_name
    get_compiler_name.restype = ctypes.c_char_p
    get_compiler_name.argtypes = [comp_t]
    get_compilers = _libraries['FIXME_STUB'].get_compilers
    get_compilers.restype = None
    get_compilers.argtypes = [ctypes.POINTER(compvec_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(qstrvec_t)]
    get_cp_validity = _libraries['FIXME_STUB'].get_cp_validity
    get_cp_validity.restype = ctypes.c_char
    get_cp_validity.argtypes = [ucdr_kind_t, wchar32_t, wchar32_t]
    get_current_extlang = _libraries['FIXME_STUB'].get_current_extlang
    get_current_extlang.restype = ctypes.POINTER(None)
    get_current_extlang.argtypes = []
    get_current_idasgn = _libraries['FIXME_STUB'].get_current_idasgn
    get_current_idasgn.restype = ctypes.c_int32
    get_current_idasgn.argtypes = []
    get_custom_data_format = _libraries['FIXME_STUB'].get_custom_data_format
    get_custom_data_format.restype = ctypes.POINTER(struct_data_format_t)
    get_custom_data_format.argtypes = [ctypes.c_int32]
    get_custom_data_formats = _libraries['FIXME_STUB'].get_custom_data_formats
    get_custom_data_formats.restype = ctypes.c_int32
    get_custom_data_formats.argtypes = [ctypes.POINTER(intvec_t), ctypes.c_int32]
    get_custom_data_type = _libraries['FIXME_STUB'].get_custom_data_type
    get_custom_data_type.restype = ctypes.POINTER(struct_data_type_t)
    get_custom_data_type.argtypes = [ctypes.c_int32]
    get_custom_data_type_ids = _libraries['FIXME_STUB'].get_custom_data_type_ids
    get_custom_data_type_ids.restype = ctypes.c_int32
    get_custom_data_type_ids.argtypes = [ctypes.POINTER(struct_custom_data_type_ids_t), ea_t]
    get_custom_data_types = _libraries['FIXME_STUB'].get_custom_data_types
    get_custom_data_types.restype = ctypes.c_int32
    get_custom_data_types.argtypes = [ctypes.POINTER(intvec_t), asize_t, asize_t]
    get_custom_refinfo = _libraries['FIXME_STUB'].get_custom_refinfo
    get_custom_refinfo.restype = ctypes.POINTER(struct_custom_refinfo_handler_t)
    get_custom_refinfo.argtypes = [ctypes.c_int32]
    get_data_elsize = _libraries['FIXME_STUB'].get_data_elsize
    get_data_elsize.restype = asize_t
    get_data_elsize.argtypes = [ea_t, flags_t, ctypes.POINTER(union_opinfo_t)]
    get_data_value = _libraries['FIXME_STUB'].get_data_value
    get_data_value.restype = ctypes.c_char
    get_data_value.argtypes = [ctypes.POINTER(uval_t), ea_t, asize_t]
    get_db_byte = _libraries['FIXME_STUB'].get_db_byte
    get_db_byte.restype = uchar
    get_db_byte.argtypes = [ea_t]
    get_dbctx_id = _libraries['FIXME_STUB'].get_dbctx_id
    get_dbctx_id.restype = ssize_t
    get_dbctx_id.argtypes = []
    get_dbctx_qty = _libraries['FIXME_STUB'].get_dbctx_qty
    get_dbctx_qty.restype = size_t
    get_dbctx_qty.argtypes = []
    get_dbg_byte = _libraries['FIXME_STUB'].get_dbg_byte
    get_dbg_byte.restype = ctypes.c_char
    get_dbg_byte.argtypes = [ctypes.POINTER(uint32), ea_t]
    get_debug_name = _libraries['FIXME_STUB'].get_debug_name
    get_debug_name.restype = ssize_t
    get_debug_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(ea_t), debug_name_how_t]
    get_debug_name_ea = _libraries['FIXME_STUB'].get_debug_name_ea
    get_debug_name_ea.restype = ea_t
    get_debug_name_ea.argtypes = [ctypes.c_char_p]
    get_debug_names = _libraries['FIXME_STUB'].get_debug_names
    get_debug_names.restype = None
    get_debug_names.argtypes = [ctypes.POINTER(ea_name_vec_t), ea_t, ea_t]
    get_debugger_plugins = _libraries['FIXME_STUB'].get_debugger_plugins
    get_debugger_plugins.restype = size_t
    get_debugger_plugins.argtypes = [ctypes.POINTER(ctypes.POINTER(struct_dbg_info_t))]
    get_default_encoding_idx = _libraries['FIXME_STUB'].get_default_encoding_idx
    get_default_encoding_idx.restype = ctypes.c_int32
    get_default_encoding_idx.argtypes = [ctypes.c_int32]
    get_default_radix = _libraries['FIXME_STUB'].get_default_radix
    get_default_radix.restype = ctypes.c_int32
    get_default_radix.argtypes = []
    get_default_reftype = _libraries['FIXME_STUB'].get_default_reftype
    get_default_reftype.restype = reftype_t
    get_default_reftype.argtypes = [ea_t]
    get_dirty_infos = _libraries['FIXME_STUB'].get_dirty_infos
    get_dirty_infos.restype = uint64
    get_dirty_infos.argtypes = []
    get_dtype_by_size = _libraries['FIXME_STUB'].get_dtype_by_size
    get_dtype_by_size.restype = op_dtype_t
    get_dtype_by_size.argtypes = [asize_t]
    get_dtype_flag = _libraries['FIXME_STUB'].get_dtype_flag
    get_dtype_flag.restype = flags_t
    get_dtype_flag.argtypes = [op_dtype_t]
    get_dtype_size = _libraries['FIXME_STUB'].get_dtype_size
    get_dtype_size.restype = size_t
    get_dtype_size.argtypes = [op_dtype_t]
    get_dword = _libraries['FIXME_STUB'].get_dword
    get_dword.restype = uint32
    get_dword.argtypes = [ea_t]
    get_ea_name = _libraries['FIXME_STUB'].get_ea_name
    get_ea_name.restype = ssize_t
    get_ea_name.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ctypes.POINTER(struct_getname_info_t)]
    get_effective_spd = _libraries['FIXME_STUB'].get_effective_spd
    get_effective_spd.restype = sval_t
    get_effective_spd.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_elf_debug_file_directory = _libraries['FIXME_STUB'].get_elf_debug_file_directory
    get_elf_debug_file_directory.restype = ctypes.c_char_p
    get_elf_debug_file_directory.argtypes = []
    get_encoding_bpu = _libraries['FIXME_STUB'].get_encoding_bpu
    get_encoding_bpu.restype = ctypes.c_int32
    get_encoding_bpu.argtypes = [ctypes.c_int32]
    get_encoding_bpu_by_name = _libraries['FIXME_STUB'].get_encoding_bpu_by_name
    get_encoding_bpu_by_name.restype = ctypes.c_int32
    get_encoding_bpu_by_name.argtypes = [ctypes.c_char_p]
    get_encoding_name = _libraries['FIXME_STUB'].get_encoding_name
    get_encoding_name.restype = ctypes.c_char_p
    get_encoding_name.argtypes = [ctypes.c_int32]
    get_encoding_qty = _libraries['FIXME_STUB'].get_encoding_qty
    get_encoding_qty.restype = ctypes.c_int32
    get_encoding_qty.argtypes = []
    get_entry = _libraries['FIXME_STUB'].get_entry
    get_entry.restype = ea_t
    get_entry.argtypes = [uval_t]
    get_entry_forwarder = _libraries['FIXME_STUB'].get_entry_forwarder
    get_entry_forwarder.restype = ssize_t
    get_entry_forwarder.argtypes = [ctypes.POINTER(qstring), uval_t]
    get_entry_name = _libraries['FIXME_STUB'].get_entry_name
    get_entry_name.restype = ssize_t
    get_entry_name.argtypes = [ctypes.POINTER(qstring), uval_t]
    get_entry_ordinal = _libraries['FIXME_STUB'].get_entry_ordinal
    get_entry_ordinal.restype = uval_t
    get_entry_ordinal.argtypes = [size_t]
    get_entry_qty = _libraries['FIXME_STUB'].get_entry_qty
    get_entry_qty.restype = size_t
    get_entry_qty.argtypes = []
    get_enum = _libraries['FIXME_STUB'].get_enum
    get_enum.restype = enum_t
    get_enum.argtypes = [ctypes.c_char_p]
    get_enum_cmt = _libraries['FIXME_STUB'].get_enum_cmt
    get_enum_cmt.restype = ssize_t
    get_enum_cmt.argtypes = [ctypes.POINTER(qstring), enum_t, ctypes.c_char]
    get_enum_flag = _libraries['FIXME_STUB'].get_enum_flag
    get_enum_flag.restype = flags_t
    get_enum_flag.argtypes = [enum_t]
    get_enum_id = _libraries['FIXME_STUB'].get_enum_id
    get_enum_id.restype = enum_t
    get_enum_id.argtypes = [ctypes.POINTER(uchar), ea_t, ctypes.c_int32]
    get_enum_idx = _libraries['FIXME_STUB'].get_enum_idx
    get_enum_idx.restype = uval_t
    get_enum_idx.argtypes = [enum_t]
    get_enum_member = _libraries['FIXME_STUB'].get_enum_member
    get_enum_member.restype = const_t
    get_enum_member.argtypes = [enum_t, uval_t, ctypes.c_int32, bmask_t]
    get_enum_member_bmask = _libraries['FIXME_STUB'].get_enum_member_bmask
    get_enum_member_bmask.restype = bmask_t
    get_enum_member_bmask.argtypes = [const_t]
    get_enum_member_by_name = _libraries['FIXME_STUB'].get_enum_member_by_name
    get_enum_member_by_name.restype = const_t
    get_enum_member_by_name.argtypes = [ctypes.c_char_p]
    get_enum_member_cmt = _libraries['FIXME_STUB'].get_enum_member_cmt
    get_enum_member_cmt.restype = ssize_t
    get_enum_member_cmt.argtypes = [ctypes.POINTER(qstring), const_t, ctypes.c_char]
    get_enum_member_enum = _libraries['FIXME_STUB'].get_enum_member_enum
    get_enum_member_enum.restype = enum_t
    get_enum_member_enum.argtypes = [const_t]
    get_enum_member_expr = _libraries['FIXME_STUB'].get_enum_member_expr
    get_enum_member_expr.restype = ctypes.c_char
    get_enum_member_expr.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_tinfo_t), ctypes.c_int32, uint64]
    get_enum_member_name = _libraries['FIXME_STUB'].get_enum_member_name
    get_enum_member_name.restype = ssize_t
    get_enum_member_name.argtypes = [ctypes.POINTER(qstring), const_t]
    get_enum_member_serial = _libraries['FIXME_STUB'].get_enum_member_serial
    get_enum_member_serial.restype = uchar
    get_enum_member_serial.argtypes = [const_t]
    get_enum_member_value = _libraries['FIXME_STUB'].get_enum_member_value
    get_enum_member_value.restype = uval_t
    get_enum_member_value.argtypes = [const_t]
    get_enum_name = _libraries['FIXME_STUB'].get_enum_name
    get_enum_name.restype = ssize_t
    get_enum_name.argtypes = [ctypes.POINTER(qstring), enum_t]
    get_enum_name2 = _libraries['FIXME_STUB'].get_enum_name2
    get_enum_name2.restype = ssize_t
    get_enum_name2.argtypes = [ctypes.POINTER(qstring), enum_t, ctypes.c_int32]
    get_enum_qty = _libraries['FIXME_STUB'].get_enum_qty
    get_enum_qty.restype = size_t
    get_enum_qty.argtypes = []
    get_enum_size = _libraries['FIXME_STUB'].get_enum_size
    get_enum_size.restype = size_t
    get_enum_size.argtypes = [enum_t]
    get_enum_type_ordinal = _libraries['FIXME_STUB'].get_enum_type_ordinal
    get_enum_type_ordinal.restype = int32
    get_enum_type_ordinal.argtypes = [enum_t]
    get_enum_width = _libraries['FIXME_STUB'].get_enum_width
    get_enum_width.restype = size_t
    get_enum_width.argtypes = [enum_t]
    get_errdesc = _libraries['FIXME_STUB'].get_errdesc
    get_errdesc.restype = ctypes.c_char_p
    get_errdesc.argtypes = [ctypes.c_char_p, error_t]
    get_error_data = _libraries['FIXME_STUB'].get_error_data
    get_error_data.restype = size_t
    get_error_data.argtypes = [ctypes.c_int32]
    get_error_string = _libraries['FIXME_STUB'].get_error_string
    get_error_string.restype = ctypes.c_char_p
    get_error_string.argtypes = [ctypes.c_int32]
    get_extra_cmt = _libraries['FIXME_STUB'].get_extra_cmt
    get_extra_cmt.restype = ssize_t
    get_extra_cmt.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32]
    get_fchunk = _libraries['FIXME_STUB'].get_fchunk
    get_fchunk.restype = ctypes.POINTER(struct_func_t)
    get_fchunk.argtypes = [ea_t]
    get_fchunk_num = _libraries['FIXME_STUB'].get_fchunk_num
    get_fchunk_num.restype = ctypes.c_int32
    get_fchunk_num.argtypes = [ea_t]
    get_fchunk_qty = _libraries['FIXME_STUB'].get_fchunk_qty
    get_fchunk_qty.restype = size_t
    get_fchunk_qty.argtypes = []
    get_file_ext = _libraries['FIXME_STUB'].get_file_ext
    get_file_ext.restype = ctypes.c_char_p
    get_file_ext.argtypes = [ctypes.c_char_p]
    get_file_type_name = _libraries['FIXME_STUB'].get_file_type_name
    get_file_type_name.restype = size_t
    get_file_type_name.argtypes = [ctypes.c_char_p, size_t]
    get_fileregion_ea = _libraries['FIXME_STUB'].get_fileregion_ea
    get_fileregion_ea.restype = ea_t
    get_fileregion_ea.argtypes = [int64]
    get_fileregion_offset = _libraries['FIXME_STUB'].get_fileregion_offset
    get_fileregion_offset.restype = int64
    get_fileregion_offset.argtypes = [ea_t]
    get_first_bmask = _libraries['FIXME_STUB'].get_first_bmask
    get_first_bmask.restype = bmask_t
    get_first_bmask.argtypes = [enum_t]
    get_first_cref_from = _libraries['FIXME_STUB'].get_first_cref_from
    get_first_cref_from.restype = ea_t
    get_first_cref_from.argtypes = [ea_t]
    get_first_cref_to = _libraries['FIXME_STUB'].get_first_cref_to
    get_first_cref_to.restype = ea_t
    get_first_cref_to.argtypes = [ea_t]
    get_first_dref_from = _libraries['FIXME_STUB'].get_first_dref_from
    get_first_dref_from.restype = ea_t
    get_first_dref_from.argtypes = [ea_t]
    get_first_dref_to = _libraries['FIXME_STUB'].get_first_dref_to
    get_first_dref_to.restype = ea_t
    get_first_dref_to.argtypes = [ea_t]
    get_first_enum_member = _libraries['FIXME_STUB'].get_first_enum_member
    get_first_enum_member.restype = uval_t
    get_first_enum_member.argtypes = [enum_t, bmask_t]
    get_first_fcref_from = _libraries['FIXME_STUB'].get_first_fcref_from
    get_first_fcref_from.restype = ea_t
    get_first_fcref_from.argtypes = [ea_t]
    get_first_fcref_to = _libraries['FIXME_STUB'].get_first_fcref_to
    get_first_fcref_to.restype = ea_t
    get_first_fcref_to.argtypes = [ea_t]
    get_first_fixup_ea = _libraries['FIXME_STUB'].get_first_fixup_ea
    get_first_fixup_ea.restype = ea_t
    get_first_fixup_ea.argtypes = []
    get_first_free_extra_cmtidx = _libraries['FIXME_STUB'].get_first_free_extra_cmtidx
    get_first_free_extra_cmtidx.restype = ctypes.c_int32
    get_first_free_extra_cmtidx.argtypes = [ea_t, ctypes.c_int32]
    get_first_hidden_range = _libraries['FIXME_STUB'].get_first_hidden_range
    get_first_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    get_first_hidden_range.argtypes = []
    get_first_seg = _libraries['FIXME_STUB'].get_first_seg
    get_first_seg.restype = ctypes.POINTER(struct_segment_t)
    get_first_seg.argtypes = []
    get_first_serial_enum_member = _libraries['FIXME_STUB'].get_first_serial_enum_member
    get_first_serial_enum_member.restype = const_t
    get_first_serial_enum_member.argtypes = [ctypes.POINTER(uchar), enum_t, uval_t, bmask_t]
    get_first_struc_idx = _libraries['FIXME_STUB'].get_first_struc_idx
    get_first_struc_idx.restype = uval_t
    get_first_struc_idx.argtypes = []
    get_fixup = _libraries['FIXME_STUB'].get_fixup
    get_fixup.restype = ctypes.c_char
    get_fixup.argtypes = [ctypes.POINTER(struct_fixup_data_t), ea_t]
    get_fixup_desc = _libraries['FIXME_STUB'].get_fixup_desc
    get_fixup_desc.restype = ctypes.c_char_p
    get_fixup_desc.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.POINTER(struct_fixup_data_t)]
    get_fixup_handler = _libraries['FIXME_STUB'].get_fixup_handler
    get_fixup_handler.restype = ctypes.POINTER(struct_fixup_handler_t)
    get_fixup_handler.argtypes = [fixup_type_t]
    get_fixup_value = _libraries['FIXME_STUB'].get_fixup_value
    get_fixup_value.restype = uval_t
    get_fixup_value.argtypes = [ea_t, fixup_type_t]
    get_fixups = _libraries['FIXME_STUB'].get_fixups
    get_fixups.restype = ctypes.c_char
    get_fixups.argtypes = [ctypes.POINTER(fixups_t), ea_t, asize_t]
    get_flags_by_size = _libraries['FIXME_STUB'].get_flags_by_size
    get_flags_by_size.restype = flags_t
    get_flags_by_size.argtypes = [size_t]
    get_flags_ex = _libraries['FIXME_STUB'].get_flags_ex
    get_flags_ex.restype = flags_t
    get_flags_ex.argtypes = [ea_t, ctypes.c_int32]
    get_forced_operand = _libraries['FIXME_STUB'].get_forced_operand
    get_forced_operand.restype = ssize_t
    get_forced_operand.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32]
    get_fpvalue_kind = _libraries['FIXME_STUB'].get_fpvalue_kind
    get_fpvalue_kind.restype = fpvalue_kind_t
    get_fpvalue_kind.argtypes = [ctypes.POINTER(struct_fpvalue_t), uint16]
    get_frame = _libraries['FIXME_STUB'].get_frame
    get_frame.restype = ctypes.POINTER(struct_struc_t)
    get_frame.argtypes = [ctypes.POINTER(struct_func_t)]
    get_frame_part = _libraries['FIXME_STUB'].get_frame_part
    get_frame_part.restype = None
    get_frame_part.argtypes = [ctypes.POINTER(struct_range_t), ctypes.POINTER(struct_func_t), frame_part_t]
    get_frame_retsize = _libraries['FIXME_STUB'].get_frame_retsize
    get_frame_retsize.restype = ctypes.c_int32
    get_frame_retsize.argtypes = [ctypes.POINTER(struct_func_t)]
    get_frame_size = _libraries['FIXME_STUB'].get_frame_size
    get_frame_size.restype = asize_t
    get_frame_size.argtypes = [ctypes.POINTER(struct_func_t)]
    get_free_disk_space = _libraries['FIXME_STUB'].get_free_disk_space
    get_free_disk_space.restype = uint64
    get_free_disk_space.argtypes = [ctypes.c_char_p]
    get_func = _libraries['FIXME_STUB'].get_func
    get_func.restype = ctypes.POINTER(struct_func_t)
    get_func.argtypes = [ea_t]
    get_func_bitness = _libraries['FIXME_STUB'].get_func_bitness
    get_func_bitness.restype = ctypes.c_int32
    get_func_bitness.argtypes = [ctypes.POINTER(struct_func_t)]
    get_func_by_frame = _libraries['FIXME_STUB'].get_func_by_frame
    get_func_by_frame.restype = ea_t
    get_func_by_frame.argtypes = [tid_t]
    get_func_chunknum = _libraries['FIXME_STUB'].get_func_chunknum
    get_func_chunknum.restype = ctypes.c_int32
    get_func_chunknum.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_func_cmt = _libraries['FIXME_STUB'].get_func_cmt
    get_func_cmt.restype = ssize_t
    get_func_cmt.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_func_t), ctypes.c_char]
    get_func_name = _libraries['FIXME_STUB'].get_func_name
    get_func_name.restype = ssize_t
    get_func_name.argtypes = [ctypes.POINTER(qstring), ea_t]
    get_func_num = _libraries['FIXME_STUB'].get_func_num
    get_func_num.restype = ctypes.c_int32
    get_func_num.argtypes = [ea_t]
    get_func_qty = _libraries['FIXME_STUB'].get_func_qty
    get_func_qty.restype = size_t
    get_func_qty.argtypes = []
    get_func_ranges = _libraries['FIXME_STUB'].get_func_ranges
    get_func_ranges.restype = ea_t
    get_func_ranges.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_func_t)]
    get_group_selector = _libraries['FIXME_STUB'].get_group_selector
    get_group_selector.restype = sel_t
    get_group_selector.argtypes = [sel_t]
    get_hexdsp = _libraries['FIXME_STUB'].get_hexdsp
    get_hexdsp.restype = hexdsp_t
    get_hexdsp.argtypes = []
    get_hidden_range = _libraries['FIXME_STUB'].get_hidden_range
    get_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    get_hidden_range.argtypes = [ea_t]
    get_hidden_range_num = _libraries['FIXME_STUB'].get_hidden_range_num
    get_hidden_range_num.restype = ctypes.c_int32
    get_hidden_range_num.argtypes = [ea_t]
    get_hidden_range_qty = _libraries['FIXME_STUB'].get_hidden_range_qty
    get_hidden_range_qty.restype = ctypes.c_int32
    get_hidden_range_qty.argtypes = []
    get_ida_subdirs = _libraries['FIXME_STUB'].get_ida_subdirs
    get_ida_subdirs.restype = ctypes.c_int32
    get_ida_subdirs.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.c_char_p, ctypes.c_int32]
    get_idainfo_by_type = _libraries['FIXME_STUB'].get_idainfo_by_type
    get_idainfo_by_type.restype = ctypes.c_char
    get_idainfo_by_type.argtypes = [ctypes.POINTER(size_t), ctypes.POINTER(flags_t), ctypes.POINTER(union_opinfo_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(size_t)]
    get_idasgn_desc = _libraries['FIXME_STUB'].get_idasgn_desc
    get_idasgn_desc.restype = int32
    get_idasgn_desc.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(qstring), ctypes.c_int32]
    get_idasgn_header_by_short_name = _libraries['FIXME_STUB'].get_idasgn_header_by_short_name
    get_idasgn_header_by_short_name.restype = ctypes.POINTER(struct_idasgn_t)
    get_idasgn_header_by_short_name.argtypes = [ctypes.c_char_p]
    get_idasgn_qty = _libraries['FIXME_STUB'].get_idasgn_qty
    get_idasgn_qty.restype = ctypes.c_int32
    get_idasgn_qty.argtypes = []
    get_idasgn_title = _libraries['FIXME_STUB'].get_idasgn_title
    get_idasgn_title.restype = ssize_t
    get_idasgn_title.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p]
    get_idati = _libraries['FIXME_STUB'].get_idati
    get_idati.restype = ctypes.POINTER(struct_til_t)
    get_idati.argtypes = []
    get_idc_filename = _libraries['FIXME_STUB'].get_idc_filename
    get_idc_filename.restype = ctypes.c_char_p
    get_idc_filename.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    get_idcv_attr = _libraries['FIXME_STUB'].get_idcv_attr
    get_idcv_attr.restype = error_t
    get_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.c_char]
    get_idcv_class_name = _libraries['FIXME_STUB'].get_idcv_class_name
    get_idcv_class_name.restype = error_t
    get_idcv_class_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_value_t)]
    get_idcv_slice = _libraries['FIXME_STUB'].get_idcv_slice
    get_idcv_slice.restype = error_t
    get_idcv_slice.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t), uval_t, uval_t, ctypes.c_int32]
    get_idp_descs = _libraries['FIXME_STUB'].get_idp_descs
    get_idp_descs.restype = ctypes.POINTER(idp_descs_t)
    get_idp_descs.argtypes = []
    get_idp_name = _libraries['FIXME_STUB'].get_idp_name
    get_idp_name.restype = ctypes.c_char_p
    get_idp_name.argtypes = [ctypes.c_char_p, size_t]
    get_immvals = _libraries['FIXME_STUB'].get_immvals
    get_immvals.restype = size_t
    get_immvals.argtypes = [ctypes.POINTER(uval_t), ea_t, ctypes.c_int32, flags_t, ctypes.POINTER(struct_insn_t)]
    get_import_module_name = _libraries['FIXME_STUB'].get_import_module_name
    get_import_module_name.restype = ctypes.c_char
    get_import_module_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_int32]
    get_import_module_qty = _libraries['FIXME_STUB'].get_import_module_qty
    get_import_module_qty.restype = uint
    get_import_module_qty.argtypes = []
    get_innermost_member = _libraries['FIXME_STUB'].get_innermost_member
    get_innermost_member.restype = ctypes.POINTER(struct_member_t)
    get_innermost_member.argtypes = [ctypes.POINTER(ctypes.POINTER(struct_struc_t)), ctypes.POINTER(asize_t)]
    get_item_color = _libraries['FIXME_STUB'].get_item_color
    get_item_color.restype = bgcolor_t
    get_item_color.argtypes = [ea_t]
    get_item_end = _libraries['FIXME_STUB'].get_item_end
    get_item_end.restype = ea_t
    get_item_end.argtypes = [ea_t]
    get_item_flag = _libraries['FIXME_STUB'].get_item_flag
    get_item_flag.restype = flags_t
    get_item_flag.argtypes = [ea_t, ctypes.c_int32, ea_t, ctypes.c_char]
    get_jtable_target = _libraries['FIXME_STUB'].get_jtable_target
    get_jtable_target.restype = ea_t
    get_jtable_target.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t), ctypes.c_int32]
    get_last_bmask = _libraries['FIXME_STUB'].get_last_bmask
    get_last_bmask.restype = bmask_t
    get_last_bmask.argtypes = [enum_t]
    get_last_enum_member = _libraries['FIXME_STUB'].get_last_enum_member
    get_last_enum_member.restype = uval_t
    get_last_enum_member.argtypes = [enum_t, bmask_t]
    get_last_hidden_range = _libraries['FIXME_STUB'].get_last_hidden_range
    get_last_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    get_last_hidden_range.argtypes = []
    get_last_pfxlen = _libraries['FIXME_STUB'].get_last_pfxlen
    get_last_pfxlen.restype = ctypes.c_int32
    get_last_pfxlen.argtypes = []
    get_last_seg = _libraries['FIXME_STUB'].get_last_seg
    get_last_seg.restype = ctypes.POINTER(struct_segment_t)
    get_last_seg.argtypes = []
    get_last_serial_enum_member = _libraries['FIXME_STUB'].get_last_serial_enum_member
    get_last_serial_enum_member.restype = const_t
    get_last_serial_enum_member.argtypes = [ctypes.POINTER(uchar), enum_t, uval_t, bmask_t]
    get_last_struc_idx = _libraries['FIXME_STUB'].get_last_struc_idx
    get_last_struc_idx.restype = uval_t
    get_last_struc_idx.argtypes = []
    get_loader_name = _libraries['FIXME_STUB'].get_loader_name
    get_loader_name.restype = ssize_t
    get_loader_name.argtypes = [ctypes.c_char_p, size_t]
    get_loader_name_from_dll = _libraries['FIXME_STUB'].get_loader_name_from_dll
    get_loader_name_from_dll.restype = ctypes.c_char_p
    get_loader_name_from_dll.argtypes = [ctypes.c_char_p]
    get_lookback = _libraries['FIXME_STUB'].get_lookback
    get_lookback.restype = ctypes.c_int32
    get_lookback.argtypes = []
    get_mangled_name_type = _libraries['FIXME_STUB'].get_mangled_name_type
    get_mangled_name_type.restype = mangled_name_type_t
    get_mangled_name_type.argtypes = [ctypes.c_char_p]
    get_manual_insn = _libraries['FIXME_STUB'].get_manual_insn
    get_manual_insn.restype = ssize_t
    get_manual_insn.argtypes = [ctypes.POINTER(qstring), ea_t]
    get_mapping = _libraries['FIXME_STUB'].get_mapping
    get_mapping.restype = ctypes.c_char
    get_mapping.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(ea_t), ctypes.POINTER(asize_t), size_t]
    get_mappings_qty = _libraries['FIXME_STUB'].get_mappings_qty
    get_mappings_qty.restype = size_t
    get_mappings_qty.argtypes = []
    get_max_strlit_length = _libraries['FIXME_STUB'].get_max_strlit_length
    get_max_strlit_length.restype = size_t
    get_max_strlit_length.argtypes = [ea_t, int32, ctypes.c_int32]
    get_member = _libraries['FIXME_STUB'].get_member
    get_member.restype = ctypes.POINTER(struct_member_t)
    get_member.argtypes = [ctypes.POINTER(struct_struc_t), asize_t]
    get_member_by_fullname = _libraries['FIXME_STUB'].get_member_by_fullname
    get_member_by_fullname.restype = ctypes.POINTER(struct_member_t)
    get_member_by_fullname.argtypes = [ctypes.POINTER(ctypes.POINTER(struct_struc_t)), ctypes.c_char_p]
    get_member_by_id = _libraries['FIXME_STUB'].get_member_by_id
    get_member_by_id.restype = ctypes.POINTER(struct_member_t)
    get_member_by_id.argtypes = [tid_t, ctypes.POINTER(ctypes.POINTER(struct_struc_t))]
    get_member_by_name = _libraries['FIXME_STUB'].get_member_by_name
    get_member_by_name.restype = ctypes.POINTER(struct_member_t)
    get_member_by_name.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_char_p]
    get_member_fullname = _libraries['FIXME_STUB'].get_member_fullname
    get_member_fullname.restype = ssize_t
    get_member_fullname.argtypes = [ctypes.POINTER(qstring), tid_t]
    get_member_name = _libraries['FIXME_STUB'].get_member_name
    get_member_name.restype = ssize_t
    get_member_name.argtypes = [ctypes.POINTER(qstring), tid_t]
    get_member_struc = _libraries['FIXME_STUB'].get_member_struc
    get_member_struc.restype = ctypes.POINTER(struct_struc_t)
    get_member_struc.argtypes = [ctypes.c_char_p]
    get_member_tinfo = _libraries['FIXME_STUB'].get_member_tinfo
    get_member_tinfo.restype = ctypes.c_char
    get_member_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_member_t)]
    get_min_spd_ea = _libraries['FIXME_STUB'].get_min_spd_ea
    get_min_spd_ea.restype = ea_t
    get_min_spd_ea.argtypes = [ctypes.POINTER(struct_func_t)]
    get_module_data = _libraries['FIXME_STUB'].get_module_data
    get_module_data.restype = ctypes.POINTER(None)
    get_module_data.argtypes = [ctypes.c_int32]
    get_name_base_ea = _libraries['FIXME_STUB'].get_name_base_ea
    get_name_base_ea.restype = ea_t
    get_name_base_ea.argtypes = [ea_t, ea_t]
    get_name_color = _libraries['FIXME_STUB'].get_name_color
    get_name_color.restype = color_t
    get_name_color.argtypes = [ea_t, ea_t]
    get_name_ea = _libraries['FIXME_STUB'].get_name_ea
    get_name_ea.restype = ea_t
    get_name_ea.argtypes = [ea_t, ctypes.c_char_p]
    get_name_expr = _libraries['FIXME_STUB'].get_name_expr
    get_name_expr.restype = ssize_t
    get_name_expr.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ea_t, uval_t, ctypes.c_int32]
    get_name_value = _libraries['FIXME_STUB'].get_name_value
    get_name_value.restype = ctypes.c_int32
    get_name_value.argtypes = [ctypes.POINTER(uval_t), ea_t, ctypes.c_char_p]
    get_named_type = _libraries['FIXME_STUB'].get_named_type
    get_named_type.restype = ctypes.c_int32
    get_named_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_int32, ctypes.POINTER(ctypes.POINTER(type_t)), ctypes.POINTER(ctypes.POINTER(p_list)), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.POINTER(p_list)), ctypes.POINTER(sclass_t), ctypes.POINTER(uint32)]
    get_next_bmask = _libraries['FIXME_STUB'].get_next_bmask
    get_next_bmask.restype = bmask_t
    get_next_bmask.argtypes = [enum_t, bmask_t]
    get_next_cref_from = _libraries['FIXME_STUB'].get_next_cref_from
    get_next_cref_from.restype = ea_t
    get_next_cref_from.argtypes = [ea_t, ea_t]
    get_next_cref_to = _libraries['FIXME_STUB'].get_next_cref_to
    get_next_cref_to.restype = ea_t
    get_next_cref_to.argtypes = [ea_t, ea_t]
    get_next_dref_from = _libraries['FIXME_STUB'].get_next_dref_from
    get_next_dref_from.restype = ea_t
    get_next_dref_from.argtypes = [ea_t, ea_t]
    get_next_dref_to = _libraries['FIXME_STUB'].get_next_dref_to
    get_next_dref_to.restype = ea_t
    get_next_dref_to.argtypes = [ea_t, ea_t]
    get_next_enum_member = _libraries['FIXME_STUB'].get_next_enum_member
    get_next_enum_member.restype = uval_t
    get_next_enum_member.argtypes = [enum_t, uval_t, bmask_t]
    get_next_fchunk = _libraries['FIXME_STUB'].get_next_fchunk
    get_next_fchunk.restype = ctypes.POINTER(struct_func_t)
    get_next_fchunk.argtypes = [ea_t]
    get_next_fcref_from = _libraries['FIXME_STUB'].get_next_fcref_from
    get_next_fcref_from.restype = ea_t
    get_next_fcref_from.argtypes = [ea_t, ea_t]
    get_next_fcref_to = _libraries['FIXME_STUB'].get_next_fcref_to
    get_next_fcref_to.restype = ea_t
    get_next_fcref_to.argtypes = [ea_t, ea_t]
    get_next_fixup_ea = _libraries['FIXME_STUB'].get_next_fixup_ea
    get_next_fixup_ea.restype = ea_t
    get_next_fixup_ea.argtypes = [ea_t]
    get_next_func = _libraries['FIXME_STUB'].get_next_func
    get_next_func.restype = ctypes.POINTER(struct_func_t)
    get_next_func.argtypes = [ea_t]
    get_next_func_addr = _libraries['FIXME_STUB'].get_next_func_addr
    get_next_func_addr.restype = ea_t
    get_next_func_addr.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_next_hidden_range = _libraries['FIXME_STUB'].get_next_hidden_range
    get_next_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    get_next_hidden_range.argtypes = [ea_t]
    get_next_member_idx = _libraries['FIXME_STUB'].get_next_member_idx
    get_next_member_idx.restype = ssize_t
    get_next_member_idx.argtypes = [ctypes.POINTER(struct_struc_t), asize_t]
    get_next_seg = _libraries['FIXME_STUB'].get_next_seg
    get_next_seg.restype = ctypes.POINTER(struct_segment_t)
    get_next_seg.argtypes = [ea_t]
    get_next_serial_enum_member = _libraries['FIXME_STUB'].get_next_serial_enum_member
    get_next_serial_enum_member.restype = const_t
    get_next_serial_enum_member.argtypes = [ctypes.POINTER(uchar), const_t]
    get_next_struc_idx = _libraries['FIXME_STUB'].get_next_struc_idx
    get_next_struc_idx.restype = uval_t
    get_next_struc_idx.argtypes = [uval_t]
    get_nice_colored_name = _libraries['FIXME_STUB'].get_nice_colored_name
    get_nice_colored_name.restype = ssize_t
    get_nice_colored_name.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32]
    get_nlist_ea = _libraries['FIXME_STUB'].get_nlist_ea
    get_nlist_ea.restype = ea_t
    get_nlist_ea.argtypes = [size_t]
    get_nlist_idx = _libraries['FIXME_STUB'].get_nlist_idx
    get_nlist_idx.restype = size_t
    get_nlist_idx.argtypes = [ea_t]
    get_nlist_name = _libraries['FIXME_STUB'].get_nlist_name
    get_nlist_name.restype = ctypes.c_char_p
    get_nlist_name.argtypes = [size_t]
    get_nlist_size = _libraries['FIXME_STUB'].get_nlist_size
    get_nlist_size.restype = size_t
    get_nlist_size.argtypes = []
    get_node_info = _libraries['FIXME_STUB'].get_node_info
    get_node_info.restype = ctypes.c_char
    get_node_info.argtypes = [ctypes.POINTER(struct_node_info_t), graph_id_t, ctypes.c_int32]
    get_nsec_stamp = _libraries['FIXME_STUB'].get_nsec_stamp
    get_nsec_stamp.restype = uint64
    get_nsec_stamp.argtypes = []
    get_numbered_type = _libraries['FIXME_STUB'].get_numbered_type
    get_numbered_type.restype = ctypes.c_char
    get_numbered_type.argtypes = [ctypes.POINTER(struct_til_t), uint32, ctypes.POINTER(ctypes.POINTER(type_t)), ctypes.POINTER(ctypes.POINTER(p_list)), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.POINTER(p_list)), ctypes.POINTER(sclass_t)]
    get_numbered_type_name = _libraries['FIXME_STUB'].get_numbered_type_name
    get_numbered_type_name.restype = ctypes.c_char_p
    get_numbered_type_name.argtypes = [ctypes.POINTER(struct_til_t), uint32]
    get_octet = _libraries['FIXME_STUB'].get_octet
    get_octet.restype = uchar
    get_octet.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(uint64), ctypes.POINTER(ctypes.c_int32)]
    get_offset_expr = _libraries['FIXME_STUB'].get_offset_expr
    get_offset_expr.restype = ctypes.c_int32
    get_offset_expr.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ctypes.POINTER(struct_refinfo_t), ea_t, adiff_t, ctypes.c_int32]
    get_offset_expression = _libraries['FIXME_STUB'].get_offset_expression
    get_offset_expression.restype = ctypes.c_int32
    get_offset_expression.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ea_t, adiff_t, ctypes.c_int32]
    get_op_tinfo = _libraries['FIXME_STUB'].get_op_tinfo
    get_op_tinfo.restype = ctypes.c_char
    get_op_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ea_t, ctypes.c_int32]
    get_opinfo = _libraries['FIXME_STUB'].get_opinfo
    get_opinfo.restype = ctypes.POINTER(union_opinfo_t)
    get_opinfo.argtypes = [ctypes.POINTER(union_opinfo_t), ea_t, ctypes.c_int32, flags_t]
    get_or_guess_member_tinfo = _libraries['FIXME_STUB'].get_or_guess_member_tinfo
    get_or_guess_member_tinfo.restype = ctypes.c_char
    get_or_guess_member_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_member_t)]
    get_ordinal_from_idb_type = _libraries['FIXME_STUB'].get_ordinal_from_idb_type
    get_ordinal_from_idb_type.restype = ctypes.c_int32
    get_ordinal_from_idb_type.argtypes = [ctypes.c_char_p, ctypes.POINTER(type_t)]
    get_ordinal_qty = _libraries['FIXME_STUB'].get_ordinal_qty
    get_ordinal_qty.restype = uint32
    get_ordinal_qty.argtypes = [ctypes.POINTER(struct_til_t)]
    get_original_byte = _libraries['FIXME_STUB'].get_original_byte
    get_original_byte.restype = uint64
    get_original_byte.argtypes = [ea_t]
    get_original_dword = _libraries['FIXME_STUB'].get_original_dword
    get_original_dword.restype = uint64
    get_original_dword.argtypes = [ea_t]
    get_original_qword = _libraries['FIXME_STUB'].get_original_qword
    get_original_qword.restype = uint64
    get_original_qword.argtypes = [ea_t]
    get_original_word = _libraries['FIXME_STUB'].get_original_word
    get_original_word.restype = uint64
    get_original_word.argtypes = [ea_t]
    get_outfile_encoding_idx = _libraries['FIXME_STUB'].get_outfile_encoding_idx
    get_outfile_encoding_idx.restype = ctypes.c_int32
    get_outfile_encoding_idx.argtypes = []
    get_path = _libraries['FIXME_STUB'].get_path
    get_path.restype = ctypes.c_char_p
    get_path.argtypes = [path_type_t]
    get_ph = _libraries['FIXME_STUB'].get_ph
    get_ph.restype = ctypes.POINTER(struct_processor_t)
    get_ph.argtypes = []
    get_place_class = _libraries['FIXME_STUB'].get_place_class
    get_place_class.restype = ctypes.POINTER(struct_place_t)
    get_place_class.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    get_place_class_id = _libraries['FIXME_STUB'].get_place_class_id
    get_place_class_id.restype = ctypes.c_int32
    get_place_class_id.argtypes = [ctypes.c_char_p]
    get_plugin_options = _libraries['FIXME_STUB'].get_plugin_options
    get_plugin_options.restype = ctypes.c_char_p
    get_plugin_options.argtypes = [ctypes.c_char_p]
    get_plugins = _libraries['FIXME_STUB'].get_plugins
    get_plugins.restype = ctypes.POINTER(struct_plugin_info_t)
    get_plugins.argtypes = []
    get_predef_insn_cmt = _libraries['FIXME_STUB'].get_predef_insn_cmt
    get_predef_insn_cmt.restype = ssize_t
    get_predef_insn_cmt.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_insn_t)]
    get_prev_bmask = _libraries['FIXME_STUB'].get_prev_bmask
    get_prev_bmask.restype = bmask_t
    get_prev_bmask.argtypes = [enum_t, bmask_t]
    get_prev_enum_member = _libraries['FIXME_STUB'].get_prev_enum_member
    get_prev_enum_member.restype = uval_t
    get_prev_enum_member.argtypes = [enum_t, uval_t, bmask_t]
    get_prev_fchunk = _libraries['FIXME_STUB'].get_prev_fchunk
    get_prev_fchunk.restype = ctypes.POINTER(struct_func_t)
    get_prev_fchunk.argtypes = [ea_t]
    get_prev_fixup_ea = _libraries['FIXME_STUB'].get_prev_fixup_ea
    get_prev_fixup_ea.restype = ea_t
    get_prev_fixup_ea.argtypes = [ea_t]
    get_prev_func = _libraries['FIXME_STUB'].get_prev_func
    get_prev_func.restype = ctypes.POINTER(struct_func_t)
    get_prev_func.argtypes = [ea_t]
    get_prev_func_addr = _libraries['FIXME_STUB'].get_prev_func_addr
    get_prev_func_addr.restype = ea_t
    get_prev_func_addr.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_prev_hidden_range = _libraries['FIXME_STUB'].get_prev_hidden_range
    get_prev_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    get_prev_hidden_range.argtypes = [ea_t]
    get_prev_member_idx = _libraries['FIXME_STUB'].get_prev_member_idx
    get_prev_member_idx.restype = ssize_t
    get_prev_member_idx.argtypes = [ctypes.POINTER(struct_struc_t), asize_t]
    get_prev_seg = _libraries['FIXME_STUB'].get_prev_seg
    get_prev_seg.restype = ctypes.POINTER(struct_segment_t)
    get_prev_seg.argtypes = [ea_t]
    get_prev_serial_enum_member = _libraries['FIXME_STUB'].get_prev_serial_enum_member
    get_prev_serial_enum_member.restype = const_t
    get_prev_serial_enum_member.argtypes = [ctypes.POINTER(uchar), const_t]
    get_prev_sreg_range = _libraries['FIXME_STUB'].get_prev_sreg_range
    get_prev_sreg_range.restype = ctypes.c_char
    get_prev_sreg_range.argtypes = [ctypes.POINTER(struct_sreg_range_t), ea_t, ctypes.c_int32]
    get_problem = _libraries['FIXME_STUB'].get_problem
    get_problem.restype = ea_t
    get_problem.argtypes = [problist_id_t, ea_t]
    get_problem_desc = _libraries['FIXME_STUB'].get_problem_desc
    get_problem_desc.restype = ssize_t
    get_problem_desc.argtypes = [ctypes.POINTER(qstring), problist_id_t, ea_t]
    get_problem_name = _libraries['FIXME_STUB'].get_problem_name
    get_problem_name.restype = ctypes.c_char_p
    get_problem_name.argtypes = [problist_id_t, ctypes.c_char]
    get_qerrno = _libraries['FIXME_STUB'].get_qerrno
    get_qerrno.restype = error_t
    get_qerrno.argtypes = []
    get_qword = _libraries['FIXME_STUB'].get_qword
    get_qword.restype = uint64
    get_qword.argtypes = [ea_t]
    get_radix = _libraries['FIXME_STUB'].get_radix
    get_radix.restype = ctypes.c_int32
    get_radix.argtypes = [flags_t, ctypes.c_int32]
    get_refinfo = _libraries['FIXME_STUB'].get_refinfo
    get_refinfo.restype = ctypes.c_char
    get_refinfo.argtypes = [ctypes.POINTER(struct_refinfo_t), ea_t, ctypes.c_int32]
    get_refinfo_descs = _libraries['FIXME_STUB'].get_refinfo_descs
    get_refinfo_descs.restype = None
    get_refinfo_descs.argtypes = [ctypes.POINTER(refinfo_desc_vec_t)]
    get_reftype_by_size = _libraries['FIXME_STUB'].get_reftype_by_size
    get_reftype_by_size.restype = reftype_t
    get_reftype_by_size.argtypes = [size_t]
    get_reg_name = _libraries['FIXME_STUB'].get_reg_name
    get_reg_name.restype = ssize_t
    get_reg_name.argtypes = [ctypes.POINTER(qstring), ctypes.c_int32, size_t, ctypes.c_int32]
    get_root_filename = _libraries['FIXME_STUB'].get_root_filename
    get_root_filename.restype = ssize_t
    get_root_filename.argtypes = [ctypes.c_char_p, size_t]
    get_scalar_bt = _libraries['FIXME_STUB'].get_scalar_bt
    get_scalar_bt.restype = type_t
    get_scalar_bt.argtypes = [ctypes.c_int32]
    get_segm_base = _libraries['FIXME_STUB'].get_segm_base
    get_segm_base.restype = ea_t
    get_segm_base.argtypes = [ctypes.POINTER(struct_segment_t)]
    get_segm_by_name = _libraries['FIXME_STUB'].get_segm_by_name
    get_segm_by_name.restype = ctypes.POINTER(struct_segment_t)
    get_segm_by_name.argtypes = [ctypes.c_char_p]
    get_segm_by_sel = _libraries['FIXME_STUB'].get_segm_by_sel
    get_segm_by_sel.restype = ctypes.POINTER(struct_segment_t)
    get_segm_by_sel.argtypes = [sel_t]
    get_segm_class = _libraries['FIXME_STUB'].get_segm_class
    get_segm_class.restype = ssize_t
    get_segm_class.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_segment_t)]
    get_segm_name = _libraries['FIXME_STUB'].get_segm_name
    get_segm_name.restype = ssize_t
    get_segm_name.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_segment_t), ctypes.c_int32]
    get_segm_num = _libraries['FIXME_STUB'].get_segm_num
    get_segm_num.restype = ctypes.c_int32
    get_segm_num.argtypes = [ea_t]
    get_segm_para = _libraries['FIXME_STUB'].get_segm_para
    get_segm_para.restype = ea_t
    get_segm_para.argtypes = [ctypes.POINTER(struct_segment_t)]
    get_segm_qty = _libraries['FIXME_STUB'].get_segm_qty
    get_segm_qty.restype = ctypes.c_int32
    get_segm_qty.argtypes = []
    get_segment_alignment = _libraries['FIXME_STUB'].get_segment_alignment
    get_segment_alignment.restype = ctypes.c_char_p
    get_segment_alignment.argtypes = [uchar]
    get_segment_cmt = _libraries['FIXME_STUB'].get_segment_cmt
    get_segment_cmt.restype = ssize_t
    get_segment_cmt.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_segment_t), ctypes.c_char]
    get_segment_combination = _libraries['FIXME_STUB'].get_segment_combination
    get_segment_combination.restype = ctypes.c_char_p
    get_segment_combination.argtypes = [uchar]
    get_segment_translations = _libraries['FIXME_STUB'].get_segment_translations
    get_segment_translations.restype = ssize_t
    get_segment_translations.argtypes = [ctypes.POINTER(eavec_t), ea_t]
    get_selector_qty = _libraries['FIXME_STUB'].get_selector_qty
    get_selector_qty.restype = size_t
    get_selector_qty.argtypes = []
    get_source_linnum = _libraries['FIXME_STUB'].get_source_linnum
    get_source_linnum.restype = uval_t
    get_source_linnum.argtypes = [ea_t]
    get_sourcefile = _libraries['FIXME_STUB'].get_sourcefile
    get_sourcefile.restype = ctypes.c_char_p
    get_sourcefile.argtypes = [ea_t, ctypes.POINTER(struct_range_t)]
    get_sp_delta = _libraries['FIXME_STUB'].get_sp_delta
    get_sp_delta.restype = sval_t
    get_sp_delta.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_spd = _libraries['FIXME_STUB'].get_spd
    get_spd.restype = sval_t
    get_spd.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    get_special_folder = _libraries['FIXME_STUB'].get_special_folder
    get_special_folder.restype = ctypes.c_char
    get_special_folder.argtypes = [ctypes.c_char_p, size_t, ctypes.c_int32]
    get_spoiled_reg = _libraries['FIXME_STUB'].get_spoiled_reg
    get_spoiled_reg.restype = ctypes.c_int32
    get_spoiled_reg.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.POINTER(uint32), size_t]
    get_sptr = _libraries['FIXME_STUB'].get_sptr
    get_sptr.restype = ctypes.POINTER(struct_struc_t)
    get_sptr.argtypes = [ctypes.POINTER(struct_member_t)]
    get_sreg = _libraries['FIXME_STUB'].get_sreg
    get_sreg.restype = sel_t
    get_sreg.argtypes = [ea_t, ctypes.c_int32]
    get_sreg_range = _libraries['FIXME_STUB'].get_sreg_range
    get_sreg_range.restype = ctypes.c_char
    get_sreg_range.argtypes = [ctypes.POINTER(struct_sreg_range_t), ea_t, ctypes.c_int32]
    get_sreg_range_num = _libraries['FIXME_STUB'].get_sreg_range_num
    get_sreg_range_num.restype = ctypes.c_int32
    get_sreg_range_num.argtypes = [ea_t, ctypes.c_int32]
    get_sreg_ranges_qty = _libraries['FIXME_STUB'].get_sreg_ranges_qty
    get_sreg_ranges_qty.restype = size_t
    get_sreg_ranges_qty.argtypes = [ctypes.c_int32]
    get_std_dirtree = _libraries['FIXME_STUB'].get_std_dirtree
    get_std_dirtree.restype = ctypes.POINTER(struct_dirtree_t)
    get_std_dirtree.argtypes = [dirtree_id_t]
    get_stkvar = _libraries['FIXME_STUB'].get_stkvar
    get_stkvar.restype = ctypes.POINTER(struct_member_t)
    get_stkvar.argtypes = [ctypes.POINTER(sval_t), ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), sval_t]
    get_stock_tinfo = _libraries['FIXME_STUB'].get_stock_tinfo
    get_stock_tinfo.restype = ctypes.c_char
    get_stock_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), stock_type_id_t]
    get_str_type = _libraries['FIXME_STUB'].get_str_type
    get_str_type.restype = uint32
    get_str_type.argtypes = [ea_t]
    get_strid = _libraries['FIXME_STUB'].get_strid
    get_strid.restype = tid_t
    get_strid.argtypes = [ea_t]
    get_strlist_item = _libraries['FIXME_STUB'].get_strlist_item
    get_strlist_item.restype = ctypes.c_char
    get_strlist_item.argtypes = [ctypes.POINTER(struct_string_info_t), size_t]
    get_strlist_options = _libraries['FIXME_STUB'].get_strlist_options
    get_strlist_options.restype = ctypes.POINTER(struct_strwinsetup_t)
    get_strlist_options.argtypes = []
    get_strlist_qty = _libraries['FIXME_STUB'].get_strlist_qty
    get_strlist_qty.restype = size_t
    get_strlist_qty.argtypes = []
    get_strlit_contents = _libraries['FIXME_STUB'].get_strlit_contents
    get_strlit_contents.restype = ssize_t
    get_strlit_contents.argtypes = [ctypes.POINTER(qstring), ea_t, size_t, int32, ctypes.POINTER(size_t), ctypes.c_int32]
    get_stroff_path = _libraries['FIXME_STUB'].get_stroff_path
    get_stroff_path.restype = ctypes.c_int32
    get_stroff_path.argtypes = [ctypes.POINTER(tid_t), ctypes.POINTER(adiff_t), ea_t, ctypes.c_int32]
    get_struc = _libraries['FIXME_STUB'].get_struc
    get_struc.restype = ctypes.POINTER(struct_struc_t)
    get_struc.argtypes = [tid_t]
    get_struc_by_idx = _libraries['FIXME_STUB'].get_struc_by_idx
    get_struc_by_idx.restype = tid_t
    get_struc_by_idx.argtypes = [uval_t]
    get_struc_first_offset = _libraries['FIXME_STUB'].get_struc_first_offset
    get_struc_first_offset.restype = ea_t
    get_struc_first_offset.argtypes = [ctypes.POINTER(struct_struc_t)]
    get_struc_id = _libraries['FIXME_STUB'].get_struc_id
    get_struc_id.restype = tid_t
    get_struc_id.argtypes = [ctypes.c_char_p]
    get_struc_idx = _libraries['FIXME_STUB'].get_struc_idx
    get_struc_idx.restype = uval_t
    get_struc_idx.argtypes = [tid_t]
    get_struc_last_offset = _libraries['FIXME_STUB'].get_struc_last_offset
    get_struc_last_offset.restype = ea_t
    get_struc_last_offset.argtypes = [ctypes.POINTER(struct_struc_t)]
    get_struc_name = _libraries['FIXME_STUB'].get_struc_name
    get_struc_name.restype = ssize_t
    get_struc_name.argtypes = [ctypes.POINTER(qstring), tid_t, ctypes.c_int32]
    get_struc_next_offset = _libraries['FIXME_STUB'].get_struc_next_offset
    get_struc_next_offset.restype = ea_t
    get_struc_next_offset.argtypes = [ctypes.POINTER(struct_struc_t), ea_t]
    get_struc_prev_offset = _libraries['FIXME_STUB'].get_struc_prev_offset
    get_struc_prev_offset.restype = ea_t
    get_struc_prev_offset.argtypes = [ctypes.POINTER(struct_struc_t), ea_t]
    get_struc_qty = _libraries['FIXME_STUB'].get_struc_qty
    get_struc_qty.restype = size_t
    get_struc_qty.argtypes = []
    get_struc_size = _libraries['FIXME_STUB'].get_struc_size
    get_struc_size.restype = asize_t
    get_struc_size.argtypes = [ctypes.POINTER(struct_struc_t)]
    get_struct_operand = _libraries['FIXME_STUB'].get_struct_operand
    get_struct_operand.restype = ctypes.c_int32
    get_struct_operand.argtypes = [ctypes.POINTER(adiff_t), ctypes.POINTER(adiff_t), ctypes.POINTER(tid_t), ea_t, ctypes.c_int32]
    get_switch_info = _libraries['FIXME_STUB'].get_switch_info
    get_switch_info.restype = ssize_t
    get_switch_info.argtypes = [ctypes.POINTER(struct_switch_info_t), ea_t]
    get_tinfo = _libraries['FIXME_STUB'].get_tinfo
    get_tinfo.restype = ctypes.c_char
    get_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ea_t]
    get_tinfo_attr = _libraries['FIXME_STUB'].get_tinfo_attr
    get_tinfo_attr.restype = ctypes.c_char
    get_tinfo_attr.argtypes = [uint32, ctypes.POINTER(qstring), ctypes.POINTER(struct_bytevec_t), ctypes.c_char]
    get_tinfo_attrs = _libraries['FIXME_STUB'].get_tinfo_attrs
    get_tinfo_attrs.restype = ctypes.c_char
    get_tinfo_attrs.argtypes = [uint32, ctypes.POINTER(type_attrs_t), ctypes.c_char]
    get_tinfo_details = _libraries['FIXME_STUB'].get_tinfo_details
    get_tinfo_details.restype = ctypes.c_char
    get_tinfo_details.argtypes = [uint32, type_t, ctypes.POINTER(None)]
    get_tinfo_pdata = _libraries['FIXME_STUB'].get_tinfo_pdata
    get_tinfo_pdata.restype = size_t
    get_tinfo_pdata.argtypes = [ctypes.POINTER(None), uint32, ctypes.c_int32]
    get_tinfo_property = _libraries['FIXME_STUB'].get_tinfo_property
    get_tinfo_property.restype = size_t
    get_tinfo_property.argtypes = [uint32, ctypes.c_int32]
    get_tinfo_size = _libraries['FIXME_STUB'].get_tinfo_size
    get_tinfo_size.restype = size_t
    get_tinfo_size.argtypes = [ctypes.POINTER(uint32), uint32, ctypes.c_int32]
    get_tryblks = _libraries['FIXME_STUB'].get_tryblks
    get_tryblks.restype = size_t
    get_tryblks.argtypes = [ctypes.POINTER(tryblks_t), ctypes.POINTER(struct_range_t)]
    get_type_ordinal = _libraries['FIXME_STUB'].get_type_ordinal
    get_type_ordinal.restype = int32
    get_type_ordinal.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p]
    get_user_idadir = _libraries['FIXME_STUB'].get_user_idadir
    get_user_idadir.restype = ctypes.c_char_p
    get_user_idadir.argtypes = []
    get_utf8_char = _libraries['FIXME_STUB'].get_utf8_char
    get_utf8_char.restype = wchar32_t
    get_utf8_char.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    get_vftable_ea = _libraries['FIXME_STUB'].get_vftable_ea
    get_vftable_ea.restype = ea_t
    get_vftable_ea.argtypes = [uint32]
    get_vftable_ordinal = _libraries['FIXME_STUB'].get_vftable_ordinal
    get_vftable_ordinal.restype = uint32
    get_vftable_ordinal.argtypes = [ea_t]
    get_wide_byte = _libraries['FIXME_STUB'].get_wide_byte
    get_wide_byte.restype = uint64
    get_wide_byte.argtypes = [ea_t]
    get_wide_dword = _libraries['FIXME_STUB'].get_wide_dword
    get_wide_dword.restype = uint64
    get_wide_dword.argtypes = [ea_t]
    get_wide_word = _libraries['FIXME_STUB'].get_wide_word
    get_wide_word.restype = uint64
    get_wide_word.argtypes = [ea_t]
    get_word = _libraries['FIXME_STUB'].get_word
    get_word.restype = ushort
    get_word.argtypes = [ea_t]
    get_xrefpos = _libraries['FIXME_STUB'].get_xrefpos
    get_xrefpos.restype = ssize_t
    get_xrefpos.argtypes = [ctypes.POINTER(struct_xrefpos_t), ea_t]
    get_zero_ranges = _libraries['FIXME_STUB'].get_zero_ranges
    get_zero_ranges.restype = ctypes.c_char
    get_zero_ranges.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_range_t)]
    getinf = _libraries['FIXME_STUB'].getinf
    getinf.restype = size_t
    getinf.argtypes = [inftag_t]
    getinf_buf = _libraries['FIXME_STUB'].getinf_buf
    getinf_buf.restype = ssize_t
    getinf_buf.argtypes = [inftag_t, ctypes.POINTER(None), size_t]
    getinf_flag = _libraries['FIXME_STUB'].getinf_flag
    getinf_flag.restype = ctypes.c_char
    getinf_flag.argtypes = [inftag_t, uint32]
    getinf_str = _libraries['FIXME_STUB'].getinf_str
    getinf_str.restype = ssize_t
    getinf_str.argtypes = [ctypes.POINTER(qstring), inftag_t]
    getn_enum = _libraries['FIXME_STUB'].getn_enum
    getn_enum.restype = enum_t
    getn_enum.argtypes = [size_t]
    getn_fchunk = _libraries['FIXME_STUB'].getn_fchunk
    getn_fchunk.restype = ctypes.POINTER(struct_func_t)
    getn_fchunk.argtypes = [ctypes.c_int32]
    getn_func = _libraries['FIXME_STUB'].getn_func
    getn_func.restype = ctypes.POINTER(struct_func_t)
    getn_func.argtypes = [size_t]
    getn_hidden_range = _libraries['FIXME_STUB'].getn_hidden_range
    getn_hidden_range.restype = ctypes.POINTER(struct_hidden_range_t)
    getn_hidden_range.argtypes = [ctypes.c_int32]
    getn_selector = _libraries['FIXME_STUB'].getn_selector
    getn_selector.restype = ctypes.c_char
    getn_selector.argtypes = [ctypes.POINTER(sel_t), ctypes.POINTER(ea_t), ctypes.c_int32]
    getn_sreg_range = _libraries['FIXME_STUB'].getn_sreg_range
    getn_sreg_range.restype = ctypes.c_char
    getn_sreg_range.argtypes = [ctypes.POINTER(struct_sreg_range_t), ctypes.c_int32, ctypes.c_int32]
    getnseg = _libraries['FIXME_STUB'].getnseg
    getnseg.restype = ctypes.POINTER(struct_segment_t)
    getnseg.argtypes = [ctypes.c_int32]
    getseg = _libraries['FIXME_STUB'].getseg
    getseg.restype = ctypes.POINTER(struct_segment_t)
    getseg.argtypes = [ea_t]
    getsysfile = _libraries['FIXME_STUB'].getsysfile
    getsysfile.restype = ctypes.c_char_p
    getsysfile.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p]
    guess_func_cc = _libraries['FIXME_STUB'].guess_func_cc
    guess_func_cc.restype = cm_t
    guess_func_cc.argtypes = [ctypes.POINTER(struct_func_type_data_t), ctypes.c_int32, ctypes.c_int32]
    guess_tinfo = _libraries['FIXME_STUB'].guess_tinfo
    guess_tinfo.restype = ctypes.c_int32
    guess_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), tid_t]
    h2ti = _libraries['FIXME_STUB'].h2ti
    h2ti.restype = ctypes.c_int32
    h2ti.argtypes = [ctypes.POINTER(struct_til_t), ctypes.POINTER(struct_lexer_t), ctypes.c_char_p, ctypes.c_int32, ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.POINTER(uint64), ctypes.POINTER(None)), ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.POINTER(uint64), ctypes.POINTER(None)), printer_t, ctypes.POINTER(None), abs_t]
    handle_fixups_in_macro = _libraries['FIXME_STUB'].handle_fixups_in_macro
    handle_fixups_in_macro.restype = ctypes.c_char
    handle_fixups_in_macro.argtypes = [ctypes.POINTER(struct_refinfo_t), ea_t, fixup_type_t, uint32]
    has_external_refs = _libraries['FIXME_STUB'].has_external_refs
    has_external_refs.restype = ctypes.c_char
    has_external_refs.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    has_insn_feature = _libraries['FIXME_STUB'].has_insn_feature
    has_insn_feature.restype = ctypes.c_char
    has_insn_feature.argtypes = [ctypes.c_int32, uint32]
    hexplace_t__adjust = _libraries['FIXME_STUB'].hexplace_t__adjust
    hexplace_t__adjust.restype = None
    hexplace_t__adjust.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hexplace_t__beginning = _libraries['FIXME_STUB'].hexplace_t__beginning
    hexplace_t__beginning.restype = ctypes.c_char
    hexplace_t__beginning.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hexplace_t__clone = _libraries['FIXME_STUB'].hexplace_t__clone
    hexplace_t__clone.restype = ctypes.POINTER(struct_place_t)
    hexplace_t__clone.argtypes = [ctypes.POINTER(struct_hexplace_t)]
    hexplace_t__compare = _libraries['FIXME_STUB'].hexplace_t__compare
    hexplace_t__compare.restype = ctypes.c_int32
    hexplace_t__compare.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_place_t)]
    hexplace_t__compare2 = _libraries['FIXME_STUB'].hexplace_t__compare2
    hexplace_t__compare2.restype = ctypes.c_int32
    hexplace_t__compare2.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    hexplace_t__copyfrom = _libraries['FIXME_STUB'].hexplace_t__copyfrom
    hexplace_t__copyfrom.restype = None
    hexplace_t__copyfrom.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_place_t)]
    hexplace_t__deserialize = _libraries['FIXME_STUB'].hexplace_t__deserialize
    hexplace_t__deserialize.restype = ctypes.c_char
    hexplace_t__deserialize.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    hexplace_t__ea2str = _libraries['FIXME_STUB'].hexplace_t__ea2str
    hexplace_t__ea2str.restype = size_t
    hexplace_t__ea2str.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(struct_hexplace_gen_t), ea_t]
    hexplace_t__ending = _libraries['FIXME_STUB'].hexplace_t__ending
    hexplace_t__ending.restype = ctypes.c_char
    hexplace_t__ending.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hexplace_t__enter = _libraries['FIXME_STUB'].hexplace_t__enter
    hexplace_t__enter.restype = ctypes.POINTER(struct_place_t)
    hexplace_t__enter.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(uint32)]
    hexplace_t__generate = _libraries['FIXME_STUB'].hexplace_t__generate
    hexplace_t__generate.restype = ctypes.c_int32
    hexplace_t__generate.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(color_t), ctypes.POINTER(bgcolor_t), ctypes.POINTER(None), ctypes.c_int32]
    hexplace_t__id = _libraries['FIXME_STUB'].hexplace_t__id
    hexplace_t__id.restype = ctypes.c_int32
    hexplace_t__id.argtypes = [ctypes.POINTER(struct_hexplace_t)]
    hexplace_t__leave = _libraries['FIXME_STUB'].hexplace_t__leave
    hexplace_t__leave.restype = None
    hexplace_t__leave.argtypes = [ctypes.POINTER(struct_hexplace_t), uint32]
    hexplace_t__makeplace = _libraries['FIXME_STUB'].hexplace_t__makeplace
    hexplace_t__makeplace.restype = ctypes.POINTER(struct_place_t)
    hexplace_t__makeplace.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None), uval_t, ctypes.c_int32]
    hexplace_t__name = _libraries['FIXME_STUB'].hexplace_t__name
    hexplace_t__name.restype = ctypes.c_char_p
    hexplace_t__name.argtypes = [ctypes.POINTER(struct_hexplace_t)]
    hexplace_t__next = _libraries['FIXME_STUB'].hexplace_t__next
    hexplace_t__next.restype = ctypes.c_char
    hexplace_t__next.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hexplace_t__out_one_item = _libraries['FIXME_STUB'].hexplace_t__out_one_item
    hexplace_t__out_one_item.restype = None
    hexplace_t__out_one_item.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_outctx_base_t), ctypes.POINTER(struct_hexplace_gen_t), ctypes.c_int32, ctypes.POINTER(color_t), color_t]
    hexplace_t__prev = _libraries['FIXME_STUB'].hexplace_t__prev
    hexplace_t__prev.restype = ctypes.c_char
    hexplace_t__prev.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hexplace_t__print = _libraries['FIXME_STUB'].hexplace_t__print
    hexplace_t__print.restype = None
    hexplace_t__print.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(qstring), ctypes.POINTER(None)]
    hexplace_t__rebase = _libraries['FIXME_STUB'].hexplace_t__rebase
    hexplace_t__rebase.restype = ctypes.c_char
    hexplace_t__rebase.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_segm_move_infos_t)]
    hexplace_t__serialize = _libraries['FIXME_STUB'].hexplace_t__serialize
    hexplace_t__serialize.restype = None
    hexplace_t__serialize.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(struct_bytevec_t)]
    hexplace_t__toea = _libraries['FIXME_STUB'].hexplace_t__toea
    hexplace_t__toea.restype = ea_t
    hexplace_t__toea.argtypes = [ctypes.POINTER(struct_hexplace_t)]
    hexplace_t__touval = _libraries['FIXME_STUB'].hexplace_t__touval
    hexplace_t__touval.restype = uval_t
    hexplace_t__touval.argtypes = [ctypes.POINTER(struct_hexplace_t), ctypes.POINTER(None)]
    hide_name = _libraries['FIXME_STUB'].hide_name
    hide_name.restype = None
    hide_name.argtypes = [ea_t]
    hook_event_listener = _libraries['FIXME_STUB'].hook_event_listener
    hook_event_listener.restype = ctypes.c_char
    hook_event_listener.argtypes = [hook_type_t, ctypes.POINTER(struct_event_listener_t), ctypes.POINTER(None), ctypes.c_int32]
    va_list = ctypes.POINTER(ctypes.POINTER(None))
    hook_to_notification_point = _libraries['FIXME_STUB'].hook_to_notification_point
    hook_to_notification_point.restype = ctypes.c_char
    hook_to_notification_point.argtypes = [hook_type_t, ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.c_int32, va_list), ctypes.POINTER(None)]
    ida_checkmem = _libraries['FIXME_STUB'].ida_checkmem
    ida_checkmem.restype = None
    ida_checkmem.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    idadir = _libraries['FIXME_STUB'].idadir
    idadir.restype = ctypes.c_char_p
    idadir.argtypes = [ctypes.c_char_p]
    idaplace_t__adjust = _libraries['FIXME_STUB'].idaplace_t__adjust
    idaplace_t__adjust.restype = None
    idaplace_t__adjust.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idaplace_t__beginning = _libraries['FIXME_STUB'].idaplace_t__beginning
    idaplace_t__beginning.restype = ctypes.c_char
    idaplace_t__beginning.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idaplace_t__clone = _libraries['FIXME_STUB'].idaplace_t__clone
    idaplace_t__clone.restype = ctypes.POINTER(struct_place_t)
    idaplace_t__clone.argtypes = [ctypes.POINTER(struct_idaplace_t)]
    idaplace_t__compare = _libraries['FIXME_STUB'].idaplace_t__compare
    idaplace_t__compare.restype = ctypes.c_int32
    idaplace_t__compare.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(struct_place_t)]
    idaplace_t__compare2 = _libraries['FIXME_STUB'].idaplace_t__compare2
    idaplace_t__compare2.restype = ctypes.c_int32
    idaplace_t__compare2.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    idaplace_t__copyfrom = _libraries['FIXME_STUB'].idaplace_t__copyfrom
    idaplace_t__copyfrom.restype = None
    idaplace_t__copyfrom.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(struct_place_t)]
    idaplace_t__deserialize = _libraries['FIXME_STUB'].idaplace_t__deserialize
    idaplace_t__deserialize.restype = ctypes.c_char
    idaplace_t__deserialize.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    idaplace_t__ending = _libraries['FIXME_STUB'].idaplace_t__ending
    idaplace_t__ending.restype = ctypes.c_char
    idaplace_t__ending.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idaplace_t__enter = _libraries['FIXME_STUB'].idaplace_t__enter
    idaplace_t__enter.restype = ctypes.POINTER(struct_place_t)
    idaplace_t__enter.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(uint32)]
    idaplace_t__generate = _libraries['FIXME_STUB'].idaplace_t__generate
    idaplace_t__generate.restype = ctypes.c_int32
    idaplace_t__generate.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(color_t), ctypes.POINTER(bgcolor_t), ctypes.POINTER(None), ctypes.c_int32]
    idaplace_t__id = _libraries['FIXME_STUB'].idaplace_t__id
    idaplace_t__id.restype = ctypes.c_int32
    idaplace_t__id.argtypes = [ctypes.POINTER(struct_idaplace_t)]
    idaplace_t__leave = _libraries['FIXME_STUB'].idaplace_t__leave
    idaplace_t__leave.restype = None
    idaplace_t__leave.argtypes = [ctypes.POINTER(struct_idaplace_t), uint32]
    idaplace_t__makeplace = _libraries['FIXME_STUB'].idaplace_t__makeplace
    idaplace_t__makeplace.restype = ctypes.POINTER(struct_place_t)
    idaplace_t__makeplace.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None), uval_t, ctypes.c_int32]
    idaplace_t__name = _libraries['FIXME_STUB'].idaplace_t__name
    idaplace_t__name.restype = ctypes.c_char_p
    idaplace_t__name.argtypes = [ctypes.POINTER(struct_idaplace_t)]
    idaplace_t__next = _libraries['FIXME_STUB'].idaplace_t__next
    idaplace_t__next.restype = ctypes.c_char
    idaplace_t__next.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idaplace_t__prev = _libraries['FIXME_STUB'].idaplace_t__prev
    idaplace_t__prev.restype = ctypes.c_char
    idaplace_t__prev.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idaplace_t__print = _libraries['FIXME_STUB'].idaplace_t__print
    idaplace_t__print.restype = None
    idaplace_t__print.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(qstring), ctypes.POINTER(None)]
    idaplace_t__rebase = _libraries['FIXME_STUB'].idaplace_t__rebase
    idaplace_t__rebase.restype = ctypes.c_char
    idaplace_t__rebase.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(struct_segm_move_infos_t)]
    idaplace_t__serialize = _libraries['FIXME_STUB'].idaplace_t__serialize
    idaplace_t__serialize.restype = None
    idaplace_t__serialize.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(struct_bytevec_t)]
    idaplace_t__toea = _libraries['FIXME_STUB'].idaplace_t__toea
    idaplace_t__toea.restype = ea_t
    idaplace_t__toea.argtypes = [ctypes.POINTER(struct_idaplace_t)]
    idaplace_t__touval = _libraries['FIXME_STUB'].idaplace_t__touval
    idaplace_t__touval.restype = uval_t
    idaplace_t__touval.argtypes = [ctypes.POINTER(struct_idaplace_t), ctypes.POINTER(None)]
    idb_utf8 = _libraries['FIXME_STUB'].idb_utf8
    idb_utf8.restype = ctypes.c_char
    idb_utf8.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    idcv_float = _libraries['FIXME_STUB'].idcv_float
    idcv_float.restype = error_t
    idcv_float.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    idcv_int64 = _libraries['FIXME_STUB'].idcv_int64
    idcv_int64.restype = error_t
    idcv_int64.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    idcv_long = _libraries['FIXME_STUB'].idcv_long
    idcv_long.restype = error_t
    idcv_long.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    idcv_num = _libraries['FIXME_STUB'].idcv_num
    idcv_num.restype = error_t
    idcv_num.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    idcv_object = _libraries['FIXME_STUB'].idcv_object
    idcv_object.restype = error_t
    idcv_object.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_class_t)]
    idcv_string = _libraries['FIXME_STUB'].idcv_string
    idcv_string.restype = error_t
    idcv_string.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    ieee_realcvt = _libraries['FIXME_STUB'].ieee_realcvt
    ieee_realcvt.restype = fpvalue_error_t
    ieee_realcvt.argtypes = [ctypes.POINTER(None), ctypes.POINTER(struct_fpvalue_t), uint16]
    import_module = _libraries['FIXME_STUB'].import_module
    import_module.restype = None
    import_module.argtypes = [ctypes.c_char_p, ctypes.c_char_p, uval_t, ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_linput_t), ctypes.POINTER(struct_impinfo_t)), ctypes.c_char_p]
    import_type = _libraries['FIXME_STUB'].import_type
    import_type.restype = tid_t
    import_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32]
    inf = ctypes_in_dll(struct_idainfo, _libraries['FIXME_STUB'], 'inf')
    init_database = _libraries['FIXME_STUB'].init_database
    init_database.restype = ctypes.c_int32
    init_database.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_int32)]
    init_plugins = _libraries['FIXME_STUB'].init_plugins
    init_plugins.restype = None
    init_plugins.argtypes = [ctypes.c_int32]
    insn_add_cref = _libraries['FIXME_STUB'].insn_add_cref
    insn_add_cref.restype = None
    insn_add_cref.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.c_int32, cref_t]
    insn_add_dref = _libraries['FIXME_STUB'].insn_add_dref
    insn_add_dref.restype = None
    insn_add_dref.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.c_int32, dref_t]
    insn_add_off_drefs = _libraries['FIXME_STUB'].insn_add_off_drefs
    insn_add_off_drefs.restype = ea_t
    insn_add_off_drefs.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), dref_t, ctypes.c_int32]
    insn_create_op_data = _libraries['FIXME_STUB'].insn_create_op_data
    insn_create_op_data.restype = ctypes.c_char
    insn_create_op_data.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.c_int32, op_dtype_t]
    insn_create_stkvar = _libraries['FIXME_STUB'].insn_create_stkvar
    insn_create_stkvar.restype = ctypes.c_char
    insn_create_stkvar.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.POINTER(struct_op_t), adiff_t, ctypes.c_int32]
    install_custom_argloc = _libraries['FIXME_STUB'].install_custom_argloc
    install_custom_argloc.restype = ctypes.c_int32
    install_custom_argloc.argtypes = [ctypes.POINTER(struct_custloc_desc_t)]
    install_extlang = _libraries['FIXME_STUB'].install_extlang
    install_extlang.restype = ssize_t
    install_extlang.argtypes = [ctypes.POINTER(struct_extlang_t)]
    install_user_defined_prefix = _libraries['FIXME_STUB'].install_user_defined_prefix
    install_user_defined_prefix.restype = ctypes.c_char
    install_user_defined_prefix.argtypes = [size_t, ctypes.POINTER(struct_user_defined_prefix_t), ctypes.POINTER(None)]
    internal_register_place_class = _libraries['FIXME_STUB'].internal_register_place_class
    internal_register_place_class.restype = ctypes.c_int32
    internal_register_place_class.argtypes = [ctypes.POINTER(struct_place_t), ctypes.c_int32, ctypes.POINTER(struct_plugin_t), ctypes.c_int32]
    interr = _libraries['FIXME_STUB'].interr
    interr.restype = None
    interr.argtypes = [ctypes.c_int32]
    interr_should_throw = ctypes_in_dll(ctypes.c_char, _libraries['FIXME_STUB'], 'interr_should_throw')
    invalidate_dbgmem_config = _libraries['FIXME_STUB'].invalidate_dbgmem_config
    invalidate_dbgmem_config.restype = None
    invalidate_dbgmem_config.argtypes = []
    invalidate_dbgmem_contents = _libraries['FIXME_STUB'].invalidate_dbgmem_contents
    invalidate_dbgmem_contents.restype = None
    invalidate_dbgmem_contents.argtypes = [ea_t, asize_t]
    invoke_callbacks = _libraries['FIXME_STUB'].invoke_callbacks
    invoke_callbacks.restype = ssize_t
    invoke_callbacks.argtypes = [hook_type_t, ctypes.c_int32, va_list]
    invoke_plugin = _libraries['FIXME_STUB'].invoke_plugin
    invoke_plugin.restype = ctypes.c_char
    invoke_plugin.argtypes = [ctypes.POINTER(struct_plugin_info_t)]
    is_align_insn = _libraries['FIXME_STUB'].is_align_insn
    is_align_insn.restype = ctypes.c_int32
    is_align_insn.argtypes = [ea_t]
    is_attached_custom_data_format = _libraries['FIXME_STUB'].is_attached_custom_data_format
    is_attached_custom_data_format.restype = ctypes.c_char
    is_attached_custom_data_format.argtypes = [ctypes.c_int32, ctypes.c_int32]
    is_auto_enabled = _libraries['FIXME_STUB'].is_auto_enabled
    is_auto_enabled.restype = ctypes.c_char
    is_auto_enabled.argtypes = []
    is_basic_block_end = _libraries['FIXME_STUB'].is_basic_block_end
    is_basic_block_end.restype = ctypes.c_char
    is_basic_block_end.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.c_char]
    is_bf = _libraries['FIXME_STUB'].is_bf
    is_bf.restype = ctypes.c_char
    is_bf.argtypes = [enum_t]
    is_bnot = _libraries['FIXME_STUB'].is_bnot
    is_bnot.restype = ctypes.c_char
    is_bnot.argtypes = [ea_t, flags_t, ctypes.c_int32]
    is_call_insn = _libraries['FIXME_STUB'].is_call_insn
    is_call_insn.restype = ctypes.c_char
    is_call_insn.argtypes = [ctypes.POINTER(struct_insn_t)]
    is_char = _libraries['FIXME_STUB'].is_char
    is_char.restype = ctypes.c_char
    is_char.argtypes = [flags_t, ctypes.c_int32]
    is_control_tty = _libraries['FIXME_STUB'].is_control_tty
    is_control_tty.restype = tty_control_t
    is_control_tty.argtypes = [ctypes.c_int32]
    is_cp_graphical = _libraries['FIXME_STUB'].is_cp_graphical
    is_cp_graphical.restype = ctypes.c_char
    is_cp_graphical.argtypes = [wchar32_t]
    is_custfmt = _libraries['FIXME_STUB'].is_custfmt
    is_custfmt.restype = ctypes.c_char
    is_custfmt.argtypes = [flags_t, ctypes.c_int32]
    is_database_ext = _libraries['FIXME_STUB'].is_database_ext
    is_database_ext.restype = ctypes.c_char
    is_database_ext.argtypes = [ctypes.c_char_p]
    is_database_flag = _libraries['FIXME_STUB'].is_database_flag
    is_database_flag.restype = ctypes.c_char
    is_database_flag.argtypes = [uint32]
    is_debugger_memory = _libraries['FIXME_STUB'].is_debugger_memory
    is_debugger_memory.restype = ctypes.c_char
    is_debugger_memory.argtypes = [ea_t]
    is_debugger_on = _libraries['FIXME_STUB'].is_debugger_on
    is_debugger_on.restype = ctypes.c_char
    is_debugger_on.argtypes = []
    is_defarg = _libraries['FIXME_STUB'].is_defarg
    is_defarg.restype = ctypes.c_char
    is_defarg.argtypes = [flags_t, ctypes.c_int32]
    is_ea_tryblks = _libraries['FIXME_STUB'].is_ea_tryblks
    is_ea_tryblks.restype = ctypes.c_char
    is_ea_tryblks.argtypes = [ea_t, uint32]
    is_enum = _libraries['FIXME_STUB'].is_enum
    is_enum.restype = ctypes.c_char
    is_enum.argtypes = [flags_t, ctypes.c_int32]
    is_enum_fromtil = _libraries['FIXME_STUB'].is_enum_fromtil
    is_enum_fromtil.restype = ctypes.c_char
    is_enum_fromtil.argtypes = [enum_t]
    is_enum_hidden = _libraries['FIXME_STUB'].is_enum_hidden
    is_enum_hidden.restype = ctypes.c_char
    is_enum_hidden.argtypes = [enum_t]
    is_fltnum = _libraries['FIXME_STUB'].is_fltnum
    is_fltnum.restype = ctypes.c_char
    is_fltnum.argtypes = [flags_t, ctypes.c_int32]
    is_forced_operand = _libraries['FIXME_STUB'].is_forced_operand
    is_forced_operand.restype = ctypes.c_char
    is_forced_operand.argtypes = [ea_t, ctypes.c_int32]
    is_func_locked = _libraries['FIXME_STUB'].is_func_locked
    is_func_locked.restype = ctypes.c_char
    is_func_locked.argtypes = [ctypes.POINTER(struct_func_t)]
    is_ghost_enum = _libraries['FIXME_STUB'].is_ghost_enum
    is_ghost_enum.restype = ctypes.c_char
    is_ghost_enum.argtypes = [enum_t]
    is_ida_kernel = ctypes_in_dll(ctypes.c_char, _libraries['FIXME_STUB'], 'is_ida_kernel')
    is_ident = _libraries['FIXME_STUB'].is_ident
    is_ident.restype = ctypes.c_char
    is_ident.argtypes = [ctypes.c_char_p]
    is_in_nlist = _libraries['FIXME_STUB'].is_in_nlist
    is_in_nlist.restype = ctypes.c_char
    is_in_nlist.argtypes = [ea_t]
    is_indirect_jump_insn = _libraries['FIXME_STUB'].is_indirect_jump_insn
    is_indirect_jump_insn.restype = ctypes.c_char
    is_indirect_jump_insn.argtypes = [ctypes.POINTER(struct_insn_t)]
    is_invsign = _libraries['FIXME_STUB'].is_invsign
    is_invsign.restype = ctypes.c_char
    is_invsign.argtypes = [ea_t, flags_t, ctypes.c_int32]
    is_loaded = _libraries['FIXME_STUB'].is_loaded
    is_loaded.restype = ctypes.c_char
    is_loaded.argtypes = [ea_t]
    is_lzero = _libraries['FIXME_STUB'].is_lzero
    is_lzero.restype = ctypes.c_char
    is_lzero.argtypes = [ea_t, ctypes.c_int32]
    is_main_thread = _libraries['FIXME_STUB'].is_main_thread
    is_main_thread.restype = ctypes.c_char
    is_main_thread.argtypes = []
    is_manual = _libraries['FIXME_STUB'].is_manual
    is_manual.restype = ctypes.c_char
    is_manual.argtypes = [flags_t, ctypes.c_int32]
    is_manual_insn = _libraries['FIXME_STUB'].is_manual_insn
    is_manual_insn.restype = ctypes.c_char
    is_manual_insn.argtypes = [ea_t]
    is_mapped = _libraries['FIXME_STUB'].is_mapped
    is_mapped.restype = ctypes.c_char
    is_mapped.argtypes = [ea_t]
    is_member_id = _libraries['FIXME_STUB'].is_member_id
    is_member_id.restype = ctypes.c_char
    is_member_id.argtypes = [tid_t]
    is_miniidb = _libraries['FIXME_STUB'].is_miniidb
    is_miniidb.restype = ctypes.c_char
    is_miniidb.argtypes = []
    is_name_defined_locally = _libraries['FIXME_STUB'].is_name_defined_locally
    is_name_defined_locally.restype = ctypes.c_char
    is_name_defined_locally.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char_p, ignore_name_def_t, ea_t, ea_t]
    is_numop = _libraries['FIXME_STUB'].is_numop
    is_numop.restype = ctypes.c_char
    is_numop.argtypes = [flags_t, ctypes.c_int32]
    is_numop0 = _libraries['FIXME_STUB'].is_numop0
    is_numop0.restype = ctypes.c_char
    is_numop0.argtypes = [flags_t]
    is_numop1 = _libraries['FIXME_STUB'].is_numop1
    is_numop1.restype = ctypes.c_char
    is_numop1.argtypes = [flags_t]
    is_off = _libraries['FIXME_STUB'].is_off
    is_off.restype = ctypes.c_char
    is_off.argtypes = [flags_t, ctypes.c_int32]
    is_ordinal_name = _libraries['FIXME_STUB'].is_ordinal_name
    is_ordinal_name.restype = ctypes.c_char
    is_ordinal_name.argtypes = [ctypes.c_char_p, ctypes.POINTER(uint32)]
    is_problem_present = _libraries['FIXME_STUB'].is_problem_present
    is_problem_present.restype = ctypes.c_char
    is_problem_present.argtypes = [problist_id_t, ea_t]
    is_public_name = _libraries['FIXME_STUB'].is_public_name
    is_public_name.restype = ctypes.c_char
    is_public_name.argtypes = [ea_t]
    is_refresh_requested = _libraries['FIXME_STUB'].is_refresh_requested
    is_refresh_requested.restype = ctypes.c_char
    is_refresh_requested.argtypes = [uint64]
    is_ret_insn = _libraries['FIXME_STUB'].is_ret_insn
    is_ret_insn.restype = ctypes.c_char
    is_ret_insn.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.c_char]
    is_seg = _libraries['FIXME_STUB'].is_seg
    is_seg.restype = ctypes.c_char
    is_seg.argtypes = [flags_t, ctypes.c_int32]
    is_segm_locked = _libraries['FIXME_STUB'].is_segm_locked
    is_segm_locked.restype = ctypes.c_char
    is_segm_locked.argtypes = [ctypes.POINTER(struct_segment_t)]
    is_spec_ea = _libraries['FIXME_STUB'].is_spec_ea
    is_spec_ea.restype = ctypes.c_char
    is_spec_ea.argtypes = [ea_t]
    is_spec_segm = _libraries['FIXME_STUB'].is_spec_segm
    is_spec_segm.restype = ctypes.c_char
    is_spec_segm.argtypes = [uchar]
    is_special_member = _libraries['FIXME_STUB'].is_special_member
    is_special_member.restype = ctypes.c_char
    is_special_member.argtypes = [tid_t]
    is_stkvar = _libraries['FIXME_STUB'].is_stkvar
    is_stkvar.restype = ctypes.c_char
    is_stkvar.argtypes = [flags_t, ctypes.c_int32]
    is_stroff = _libraries['FIXME_STUB'].is_stroff
    is_stroff.restype = ctypes.c_char
    is_stroff.argtypes = [flags_t, ctypes.c_int32]
    is_suspop = _libraries['FIXME_STUB'].is_suspop
    is_suspop.restype = ctypes.c_char
    is_suspop.argtypes = [ea_t, flags_t, ctypes.c_int32]
    is_trusted_idb = _libraries['FIXME_STUB'].is_trusted_idb
    is_trusted_idb.restype = ctypes.c_char
    is_trusted_idb.argtypes = []
    is_uname = _libraries['FIXME_STUB'].is_uname
    is_uname.restype = ctypes.c_char
    is_uname.argtypes = [ctypes.c_char_p]
    is_valid_cp = _libraries['FIXME_STUB'].is_valid_cp
    is_valid_cp.restype = ctypes.c_char
    is_valid_cp.argtypes = [wchar32_t, nametype_t, ctypes.POINTER(None)]
    is_valid_typename = _libraries['FIXME_STUB'].is_valid_typename
    is_valid_typename.restype = ctypes.c_char
    is_valid_typename.argtypes = [ctypes.c_char_p]
    is_valid_utf8 = _libraries['FIXME_STUB'].is_valid_utf8
    is_valid_utf8.restype = ctypes.c_char
    is_valid_utf8.argtypes = [ctypes.c_char_p]
    is_varmember = _libraries['FIXME_STUB'].is_varmember
    is_varmember.restype = ctypes.c_char
    is_varmember.argtypes = [ctypes.POINTER(struct_member_t)]
    is_varsize_item = _libraries['FIXME_STUB'].is_varsize_item
    is_varsize_item.restype = ctypes.c_int32
    is_varsize_item.argtypes = [ea_t, flags_t, ctypes.POINTER(union_opinfo_t), ctypes.POINTER(asize_t)]
    is_weak_name = _libraries['FIXME_STUB'].is_weak_name
    is_weak_name.restype = ctypes.c_char
    is_weak_name.argtypes = [ea_t]
    iterate_func_chunks = _libraries['FIXME_STUB'].iterate_func_chunks
    iterate_func_chunks.restype = None
    iterate_func_chunks.argtypes = [ctypes.POINTER(struct_func_t), ctypes.CFUNCTYPE(None, ea_t, ea_t, ctypes.POINTER(None)), ctypes.POINTER(None), ctypes.c_char]
    itext = _libraries['FIXME_STUB'].itext
    itext.restype = ctypes.c_char_p
    itext.argtypes = [help_t]
    jvalue_t_clear = _libraries['FIXME_STUB'].jvalue_t_clear
    jvalue_t_clear.restype = None
    jvalue_t_clear.argtypes = [ctypes.POINTER(struct_jvalue_t)]
    jvalue_t_copy = _libraries['FIXME_STUB'].jvalue_t_copy
    jvalue_t_copy.restype = None
    jvalue_t_copy.argtypes = [ctypes.POINTER(struct_jvalue_t), ctypes.POINTER(struct_jvalue_t)]
    l_compare = _libraries['FIXME_STUB'].l_compare
    l_compare.restype = ctypes.c_int32
    l_compare.argtypes = [ctypes.POINTER(struct_place_t), ctypes.POINTER(struct_place_t)]
    l_compare2 = _libraries['FIXME_STUB'].l_compare2
    l_compare2.restype = ctypes.c_int32
    l_compare2.argtypes = [ctypes.POINTER(struct_place_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    last_idcv_attr = _libraries['FIXME_STUB'].last_idcv_attr
    last_idcv_attr.restype = ctypes.c_char_p
    last_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t)]
    launch_process = _libraries['FIXME_STUB'].launch_process
    launch_process.restype = ctypes.POINTER(None)
    launch_process.argtypes = [ctypes.POINTER(struct_launch_process_params_t), ctypes.POINTER(qstring)]
    leading_zero_important = _libraries['FIXME_STUB'].leading_zero_important
    leading_zero_important.restype = ctypes.c_char
    leading_zero_important.argtypes = [ea_t, ctypes.c_int32]
    lex_define_macro = _libraries['FIXME_STUB'].lex_define_macro
    lex_define_macro.restype = error_t
    lex_define_macro.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char]
    lex_get_file_line = _libraries['FIXME_STUB'].lex_get_file_line
    lex_get_file_line.restype = ctypes.c_char_p
    lex_get_file_line.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.POINTER(int32), ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    lex_get_token = _libraries['FIXME_STUB'].lex_get_token
    lex_get_token.restype = error_t
    lex_get_token.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t)]
    lex_get_token2 = _libraries['FIXME_STUB'].lex_get_token2
    lex_get_token2.restype = error_t
    lex_get_token2.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(int32)]
    lex_init_file = _libraries['FIXME_STUB'].lex_init_file
    lex_init_file.restype = error_t
    lex_init_file.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_char_p]
    lex_init_string = _libraries['FIXME_STUB'].lex_init_string
    lex_init_string.restype = error_t
    lex_init_string.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_char_p, ctypes.POINTER(None)]
    lex_print_token = _libraries['FIXME_STUB'].lex_print_token
    lex_print_token.restype = ctypes.c_char_p
    lex_print_token.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_token_t)]
    lex_set_options = _libraries['FIXME_STUB'].lex_set_options
    lex_set_options.restype = ctypes.c_int32
    lex_set_options.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_int32]
    lex_term_file = _libraries['FIXME_STUB'].lex_term_file
    lex_term_file.restype = None
    lex_term_file.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_char]
    lex_undefine_macro = _libraries['FIXME_STUB'].lex_undefine_macro
    lex_undefine_macro.restype = None
    lex_undefine_macro.argtypes = [ctypes.POINTER(struct_lexer_t), ctypes.c_char_p]
    lexcompare_tinfo = _libraries['FIXME_STUB'].lexcompare_tinfo
    lexcompare_tinfo.restype = ctypes.c_int32
    lexcompare_tinfo.argtypes = [uint32, uint32, ctypes.c_int32]
    linearray_t_beginning = _libraries['FIXME_STUB'].linearray_t_beginning
    linearray_t_beginning.restype = ctypes.c_char
    linearray_t_beginning.argtypes = [ctypes.POINTER(struct_linearray_t)]
    linearray_t_ctr = _libraries['FIXME_STUB'].linearray_t_ctr
    linearray_t_ctr.restype = None
    linearray_t_ctr.argtypes = [ctypes.POINTER(struct_linearray_t), ctypes.POINTER(None)]
    linearray_t_down = _libraries['FIXME_STUB'].linearray_t_down
    linearray_t_down.restype = ctypes.POINTER(qstring)
    linearray_t_down.argtypes = [ctypes.POINTER(struct_linearray_t)]
    linearray_t_dtr = _libraries['FIXME_STUB'].linearray_t_dtr
    linearray_t_dtr.restype = None
    linearray_t_dtr.argtypes = [ctypes.POINTER(struct_linearray_t)]
    linearray_t_ending = _libraries['FIXME_STUB'].linearray_t_ending
    linearray_t_ending.restype = ctypes.c_char
    linearray_t_ending.argtypes = [ctypes.POINTER(struct_linearray_t)]
    linearray_t_set_place = _libraries['FIXME_STUB'].linearray_t_set_place
    linearray_t_set_place.restype = ctypes.c_int32
    linearray_t_set_place.argtypes = [ctypes.POINTER(struct_linearray_t), ctypes.POINTER(struct_place_t)]
    linearray_t_up = _libraries['FIXME_STUB'].linearray_t_up
    linearray_t_up.restype = ctypes.POINTER(qstring)
    linearray_t_up.argtypes = [ctypes.POINTER(struct_linearray_t)]
    llong_scan = _libraries['FIXME_STUB'].llong_scan
    llong_scan.restype = longlong
    llong_scan.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.POINTER(ctypes.c_char_p)]
    load_binary_file = _libraries['FIXME_STUB'].load_binary_file
    load_binary_file.restype = ctypes.c_char
    load_binary_file.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_linput_t), ushort, int64, ea_t, ea_t, uint64]
    load_core_module = _libraries['FIXME_STUB'].load_core_module
    load_core_module.restype = ctypes.c_char
    load_core_module.argtypes = [ctypes.POINTER(struct_idadll_t), ctypes.c_char_p, ctypes.c_char_p]
    load_dirtree = _libraries['FIXME_STUB'].load_dirtree
    load_dirtree.restype = ctypes.c_char
    load_dirtree.argtypes = [ctypes.POINTER(struct_dirtree_impl_t)]
    load_ids_module = _libraries['FIXME_STUB'].load_ids_module
    load_ids_module.restype = ctypes.c_int32
    load_ids_module.argtypes = [ctypes.c_char_p]
    load_nonbinary_file = _libraries['FIXME_STUB'].load_nonbinary_file
    load_nonbinary_file.restype = ctypes.c_char
    load_nonbinary_file.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_linput_t), ctypes.c_char_p, ushort, ctypes.POINTER(struct_load_info_t)]
    load_til = _libraries['FIXME_STUB'].load_til
    load_til.restype = ctypes.POINTER(struct_til_t)
    load_til.argtypes = [ctypes.c_char_p, ctypes.POINTER(qstring), ctypes.c_char_p]
    load_til_header = _libraries['FIXME_STUB'].load_til_header
    load_til_header.restype = ctypes.POINTER(struct_til_t)
    load_til_header.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(qstring)]
    lochist_entry_t_deserialize = _libraries['FIXME_STUB'].lochist_entry_t_deserialize
    lochist_entry_t_deserialize.restype = ctypes.c_char
    lochist_entry_t_deserialize.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar), ctypes.POINTER(struct_place_t)]
    lochist_entry_t_serialize = _libraries['FIXME_STUB'].lochist_entry_t_serialize
    lochist_entry_t_serialize.restype = None
    lochist_entry_t_serialize.argtypes = [ctypes.POINTER(struct_bytevec_t), ctypes.POINTER(struct_lochist_entry_t)]
    lochist_t_back = _libraries['FIXME_STUB'].lochist_t_back
    lochist_t_back.restype = ctypes.c_char
    lochist_t_back.argtypes = [ctypes.POINTER(struct_lochist_t), uint32, ctypes.c_char]
    lochist_t_clear = _libraries['FIXME_STUB'].lochist_t_clear
    lochist_t_clear.restype = None
    lochist_t_clear.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_current_index = _libraries['FIXME_STUB'].lochist_t_current_index
    lochist_t_current_index.restype = uint32
    lochist_t_current_index.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_deregister_live = _libraries['FIXME_STUB'].lochist_t_deregister_live
    lochist_t_deregister_live.restype = None
    lochist_t_deregister_live.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_fwd = _libraries['FIXME_STUB'].lochist_t_fwd
    lochist_t_fwd.restype = ctypes.c_char
    lochist_t_fwd.argtypes = [ctypes.POINTER(struct_lochist_t), uint32, ctypes.c_char]
    lochist_t_get = _libraries['FIXME_STUB'].lochist_t_get
    lochist_t_get.restype = ctypes.c_char
    lochist_t_get.argtypes = [ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_t), uint32]
    lochist_t_get_current = _libraries['FIXME_STUB'].lochist_t_get_current
    lochist_t_get_current.restype = ctypes.POINTER(struct_lochist_entry_t)
    lochist_t_get_current.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_init = _libraries['FIXME_STUB'].lochist_t_init
    lochist_t_init.restype = ctypes.c_char
    lochist_t_init.argtypes = [ctypes.POINTER(struct_lochist_t), ctypes.c_char_p, ctypes.POINTER(struct_place_t), ctypes.POINTER(None), uint32]
    lochist_t_jump = _libraries['FIXME_STUB'].lochist_t_jump
    lochist_t_jump.restype = None
    lochist_t_jump.argtypes = [ctypes.POINTER(struct_lochist_t), ctypes.c_char, ctypes.POINTER(struct_lochist_entry_t)]
    lochist_t_register_live = _libraries['FIXME_STUB'].lochist_t_register_live
    lochist_t_register_live.restype = None
    lochist_t_register_live.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_save = _libraries['FIXME_STUB'].lochist_t_save
    lochist_t_save.restype = None
    lochist_t_save.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lochist_t_seek = _libraries['FIXME_STUB'].lochist_t_seek
    lochist_t_seek.restype = ctypes.c_char
    lochist_t_seek.argtypes = [ctypes.POINTER(struct_lochist_t), uint32, ctypes.c_char, ctypes.c_char]
    lochist_t_set = _libraries['FIXME_STUB'].lochist_t_set
    lochist_t_set.restype = None
    lochist_t_set.argtypes = [ctypes.POINTER(struct_lochist_t), uint32, ctypes.POINTER(struct_lochist_entry_t)]
    lochist_t_size = _libraries['FIXME_STUB'].lochist_t_size
    lochist_t_size.restype = uint32
    lochist_t_size.argtypes = [ctypes.POINTER(struct_lochist_t)]
    lock_dbgmem_config = _libraries['FIXME_STUB'].lock_dbgmem_config
    lock_dbgmem_config.restype = None
    lock_dbgmem_config.argtypes = []
    lock_func_range = _libraries['FIXME_STUB'].lock_func_range
    lock_func_range.restype = None
    lock_func_range.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char]
    lock_segm = _libraries['FIXME_STUB'].lock_segm
    lock_segm.restype = None
    lock_segm.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char]
    log2ceil = _libraries['FIXME_STUB'].log2ceil
    log2ceil.restype = ctypes.c_int32
    log2ceil.argtypes = [uint64]
    log2floor = _libraries['FIXME_STUB'].log2floor
    log2floor.restype = ctypes.c_int32
    log2floor.argtypes = [uint64]
    lookup_loc_converter2 = _libraries['FIXME_STUB'].lookup_loc_converter2
    lookup_loc_converter2.restype = ctypes.CFUNCTYPE(lecvt_code_t, ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_TWidget), uint32)
    lookup_loc_converter2.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lower_type = _libraries['FIXME_STUB'].lower_type
    lower_type.restype = ctypes.c_int32
    lower_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.POINTER(struct_lowertype_helper_t)]
    lread = _libraries['FIXME_STUB'].lread
    lread.restype = None
    lread.argtypes = [ctypes.POINTER(struct_linput_t), ctypes.POINTER(None), size_t]
    lreadbytes = _libraries['FIXME_STUB'].lreadbytes
    lreadbytes.restype = ctypes.c_int32
    lreadbytes.argtypes = [ctypes.POINTER(struct_linput_t), ctypes.POINTER(None), size_t, ctypes.c_char]
    make_linput = _libraries['FIXME_STUB'].make_linput
    make_linput.restype = ctypes.POINTER(struct_linput_t)
    make_linput.argtypes = [ctypes.POINTER(FILE)]
    make_name_auto = _libraries['FIXME_STUB'].make_name_auto
    make_name_auto.restype = ctypes.c_char
    make_name_auto.argtypes = [ea_t]
    make_name_non_public = _libraries['FIXME_STUB'].make_name_non_public
    make_name_non_public.restype = None
    make_name_non_public.argtypes = [ea_t]
    make_name_non_weak = _libraries['FIXME_STUB'].make_name_non_weak
    make_name_non_weak.restype = None
    make_name_non_weak.argtypes = [ea_t]
    make_name_public = _libraries['FIXME_STUB'].make_name_public
    make_name_public.restype = None
    make_name_public.argtypes = [ea_t]
    make_name_user = _libraries['FIXME_STUB'].make_name_user
    make_name_user.restype = ctypes.c_char
    make_name_user.argtypes = [ea_t]
    make_name_weak = _libraries['FIXME_STUB'].make_name_weak
    make_name_weak.restype = None
    make_name_weak.argtypes = [ea_t]
    map_code_ea = _libraries['FIXME_STUB'].map_code_ea
    map_code_ea.restype = ea_t
    map_code_ea.argtypes = [ctypes.POINTER(struct_insn_t), ea_t, ctypes.c_int32]
    mark_switch_insns_jpt = _libraries['FIXME_STUB'].mark_switch_insns_jpt
    mark_switch_insns_jpt.restype = None
    mark_switch_insns_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.c_int32, ctypes.c_int32]
    match_jpt = _libraries['FIXME_STUB'].match_jpt
    match_jpt.restype = ctypes.c_char
    match_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t)]
    mem2base = _libraries['FIXME_STUB'].mem2base
    mem2base.restype = ctypes.c_int32
    mem2base.argtypes = [ctypes.POINTER(None), ea_t, ea_t, int64]
    memrev = _libraries['FIXME_STUB'].memrev
    memrev.restype = ctypes.POINTER(None)
    memrev.argtypes = [ctypes.POINTER(None), ssize_t]
    move_idcv = _libraries['FIXME_STUB'].move_idcv
    move_idcv.restype = error_t
    move_idcv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)]
    move_segm = _libraries['FIXME_STUB'].move_segm
    move_segm.restype = ctypes.c_int32
    move_segm.argtypes = [ctypes.POINTER(struct_segment_t), ea_t, ctypes.c_int32]
    move_segm_start = _libraries['FIXME_STUB'].move_segm_start
    move_segm_start.restype = ctypes.c_char
    move_segm_start.argtypes = [ea_t, ea_t, ctypes.c_int32]
    name_requires_qualifier = _libraries['FIXME_STUB'].name_requires_qualifier
    name_requires_qualifier.restype = ctypes.c_char
    name_requires_qualifier.argtypes = [ctypes.POINTER(qstring), uint32, ctypes.c_char_p, uint64]
    nbits = _libraries['FIXME_STUB'].nbits
    nbits.restype = ctypes.c_int32
    nbits.argtypes = [ea_t]
    netnode_altadjust = _libraries['FIXME_STUB'].netnode_altadjust
    netnode_altadjust.restype = None
    netnode_altadjust.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, nodeidx_t, ctypes.CFUNCTYPE(ctypes.c_char, nodeidx_t)]
    netnode_altadjust2 = _libraries['FIXME_STUB'].netnode_altadjust2
    netnode_altadjust2.restype = None
    netnode_altadjust2.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, nodeidx_t, ctypes.POINTER(struct_altadjust_visitor_t)]
    netnode_altshift = _libraries['FIXME_STUB'].netnode_altshift
    netnode_altshift.restype = size_t
    netnode_altshift.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_altval = _libraries['FIXME_STUB'].netnode_altval
    netnode_altval.restype = nodeidx_t
    netnode_altval.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_altval_idx8 = _libraries['FIXME_STUB'].netnode_altval_idx8
    netnode_altval_idx8.restype = nodeidx_t
    netnode_altval_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_blobsize = _libraries['FIXME_STUB'].netnode_blobsize
    netnode_blobsize.restype = size_t
    netnode_blobsize.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_charshift = _libraries['FIXME_STUB'].netnode_charshift
    netnode_charshift.restype = size_t
    netnode_charshift.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_charval = _libraries['FIXME_STUB'].netnode_charval
    netnode_charval.restype = uchar
    netnode_charval.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_charval_idx8 = _libraries['FIXME_STUB'].netnode_charval_idx8
    netnode_charval_idx8.restype = uchar
    netnode_charval_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_check = _libraries['FIXME_STUB'].netnode_check
    netnode_check.restype = ctypes.c_char
    netnode_check.argtypes = [ctypes.POINTER(struct_netnode), ctypes.c_char_p, size_t, ctypes.c_char]
    netnode_copy = _libraries['FIXME_STUB'].netnode_copy
    netnode_copy.restype = size_t
    netnode_copy.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_char]
    netnode_delblob = _libraries['FIXME_STUB'].netnode_delblob
    netnode_delblob.restype = ctypes.c_int32
    netnode_delblob.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_delvalue = _libraries['FIXME_STUB'].netnode_delvalue
    netnode_delvalue.restype = ctypes.c_char
    netnode_delvalue.argtypes = [nodeidx_t]
    netnode_end = _libraries['FIXME_STUB'].netnode_end
    netnode_end.restype = ctypes.c_char
    netnode_end.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_exist = _libraries['FIXME_STUB'].netnode_exist
    netnode_exist.restype = ctypes.c_char
    netnode_exist.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_get_name = _libraries['FIXME_STUB'].netnode_get_name
    netnode_get_name.restype = ssize_t
    netnode_get_name.argtypes = [nodeidx_t, ctypes.POINTER(qstring)]
    netnode_getblob = _libraries['FIXME_STUB'].netnode_getblob
    netnode_getblob.restype = ctypes.POINTER(None)
    netnode_getblob.argtypes = [nodeidx_t, ctypes.POINTER(None), ctypes.POINTER(size_t), nodeidx_t, ctypes.c_int32]
    netnode_hashdel = _libraries['FIXME_STUB'].netnode_hashdel
    netnode_hashdel.restype = ctypes.c_char
    netnode_hashdel.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.c_int32]
    netnode_hashfirst = _libraries['FIXME_STUB'].netnode_hashfirst
    netnode_hashfirst.restype = ssize_t
    netnode_hashfirst.argtypes = [nodeidx_t, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_hashlast = _libraries['FIXME_STUB'].netnode_hashlast
    netnode_hashlast.restype = ssize_t
    netnode_hashlast.argtypes = [nodeidx_t, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_hashnext = _libraries['FIXME_STUB'].netnode_hashnext
    netnode_hashnext.restype = ssize_t
    netnode_hashnext.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_hashprev = _libraries['FIXME_STUB'].netnode_hashprev
    netnode_hashprev.restype = ssize_t
    netnode_hashprev.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_hashset = _libraries['FIXME_STUB'].netnode_hashset
    netnode_hashset.restype = ctypes.c_char
    netnode_hashset.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_hashstr = _libraries['FIXME_STUB'].netnode_hashstr
    netnode_hashstr.restype = ssize_t
    netnode_hashstr.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_hashval = _libraries['FIXME_STUB'].netnode_hashval
    netnode_hashval.restype = ssize_t
    netnode_hashval.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_hashval_long = _libraries['FIXME_STUB'].netnode_hashval_long
    netnode_hashval_long.restype = nodeidx_t
    netnode_hashval_long.argtypes = [nodeidx_t, ctypes.c_char_p, ctypes.c_int32]
    netnode_inited = _libraries['FIXME_STUB'].netnode_inited
    netnode_inited.restype = ctypes.c_char
    netnode_inited.argtypes = []
    netnode_is_available = _libraries['FIXME_STUB'].netnode_is_available
    netnode_is_available.restype = ctypes.c_char
    netnode_is_available.argtypes = []
    netnode_kill = _libraries['FIXME_STUB'].netnode_kill
    netnode_kill.restype = None
    netnode_kill.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_lower_bound = _libraries['FIXME_STUB'].netnode_lower_bound
    netnode_lower_bound.restype = nodeidx_t
    netnode_lower_bound.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_lower_bound_idx8 = _libraries['FIXME_STUB'].netnode_lower_bound_idx8
    netnode_lower_bound_idx8.restype = nodeidx_t
    netnode_lower_bound_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_next = _libraries['FIXME_STUB'].netnode_next
    netnode_next.restype = ctypes.c_char
    netnode_next.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_prev = _libraries['FIXME_STUB'].netnode_prev
    netnode_prev.restype = ctypes.c_char
    netnode_prev.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_qgetblob = _libraries['FIXME_STUB'].netnode_qgetblob
    netnode_qgetblob.restype = ssize_t
    netnode_qgetblob.argtypes = [nodeidx_t, ctypes.POINTER(struct_bytevec_t), size_t, nodeidx_t, ctypes.c_int32]
    netnode_qhashfirst = _libraries['FIXME_STUB'].netnode_qhashfirst
    netnode_qhashfirst.restype = ssize_t
    netnode_qhashfirst.argtypes = [nodeidx_t, ctypes.POINTER(qstring), ctypes.c_int32]
    netnode_qhashlast = _libraries['FIXME_STUB'].netnode_qhashlast
    netnode_qhashlast.restype = ssize_t
    netnode_qhashlast.argtypes = [nodeidx_t, ctypes.POINTER(qstring), ctypes.c_int32]
    netnode_qhashnext = _libraries['FIXME_STUB'].netnode_qhashnext
    netnode_qhashnext.restype = ssize_t
    netnode_qhashnext.argtypes = [nodeidx_t, ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    netnode_qhashprev = _libraries['FIXME_STUB'].netnode_qhashprev
    netnode_qhashprev.restype = ssize_t
    netnode_qhashprev.argtypes = [nodeidx_t, ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    netnode_qhashstr = _libraries['FIXME_STUB'].netnode_qhashstr
    netnode_qhashstr.restype = ssize_t
    netnode_qhashstr.argtypes = [nodeidx_t, ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    netnode_qsupstr = _libraries['FIXME_STUB'].netnode_qsupstr
    netnode_qsupstr.restype = ssize_t
    netnode_qsupstr.argtypes = [nodeidx_t, ctypes.POINTER(qstring), nodeidx_t, ctypes.c_int32]
    netnode_qsupstr_idx8 = _libraries['FIXME_STUB'].netnode_qsupstr_idx8
    netnode_qsupstr_idx8.restype = ssize_t
    netnode_qsupstr_idx8.argtypes = [nodeidx_t, ctypes.POINTER(qstring), uchar, ctypes.c_int32]
    netnode_qvalstr = _libraries['FIXME_STUB'].netnode_qvalstr
    netnode_qvalstr.restype = ssize_t
    netnode_qvalstr.argtypes = [nodeidx_t, ctypes.POINTER(qstring)]
    netnode_rename = _libraries['FIXME_STUB'].netnode_rename
    netnode_rename.restype = ctypes.c_char
    netnode_rename.argtypes = [nodeidx_t, ctypes.c_char_p, size_t]
    netnode_set = _libraries['FIXME_STUB'].netnode_set
    netnode_set.restype = ctypes.c_char
    netnode_set.argtypes = [nodeidx_t, ctypes.POINTER(None), size_t]
    netnode_setblob = _libraries['FIXME_STUB'].netnode_setblob
    netnode_setblob.restype = ctypes.c_char
    netnode_setblob.argtypes = [nodeidx_t, ctypes.POINTER(None), size_t, nodeidx_t, ctypes.c_int32]
    netnode_start = _libraries['FIXME_STUB'].netnode_start
    netnode_start.restype = ctypes.c_char
    netnode_start.argtypes = [ctypes.POINTER(struct_netnode)]
    netnode_supdel = _libraries['FIXME_STUB'].netnode_supdel
    netnode_supdel.restype = ctypes.c_char
    netnode_supdel.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supdel_all = _libraries['FIXME_STUB'].netnode_supdel_all
    netnode_supdel_all.restype = ctypes.c_char
    netnode_supdel_all.argtypes = [nodeidx_t, ctypes.c_int32]
    netnode_supdel_idx8 = _libraries['FIXME_STUB'].netnode_supdel_idx8
    netnode_supdel_idx8.restype = ctypes.c_char
    netnode_supdel_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_supdel_range = _libraries['FIXME_STUB'].netnode_supdel_range
    netnode_supdel_range.restype = ctypes.c_int32
    netnode_supdel_range.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supdel_range_idx8 = _libraries['FIXME_STUB'].netnode_supdel_range_idx8
    netnode_supdel_range_idx8.restype = ctypes.c_int32
    netnode_supdel_range_idx8.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supfirst = _libraries['FIXME_STUB'].netnode_supfirst
    netnode_supfirst.restype = nodeidx_t
    netnode_supfirst.argtypes = [nodeidx_t, ctypes.c_int32]
    netnode_supfirst_idx8 = _libraries['FIXME_STUB'].netnode_supfirst_idx8
    netnode_supfirst_idx8.restype = nodeidx_t
    netnode_supfirst_idx8.argtypes = [nodeidx_t, ctypes.c_int32]
    netnode_suplast = _libraries['FIXME_STUB'].netnode_suplast
    netnode_suplast.restype = nodeidx_t
    netnode_suplast.argtypes = [nodeidx_t, ctypes.c_int32]
    netnode_suplast_idx8 = _libraries['FIXME_STUB'].netnode_suplast_idx8
    netnode_suplast_idx8.restype = nodeidx_t
    netnode_suplast_idx8.argtypes = [nodeidx_t, ctypes.c_int32]
    netnode_supnext = _libraries['FIXME_STUB'].netnode_supnext
    netnode_supnext.restype = nodeidx_t
    netnode_supnext.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supnext_idx8 = _libraries['FIXME_STUB'].netnode_supnext_idx8
    netnode_supnext_idx8.restype = nodeidx_t
    netnode_supnext_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_supprev = _libraries['FIXME_STUB'].netnode_supprev
    netnode_supprev.restype = nodeidx_t
    netnode_supprev.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supprev_idx8 = _libraries['FIXME_STUB'].netnode_supprev_idx8
    netnode_supprev_idx8.restype = nodeidx_t
    netnode_supprev_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_int32]
    netnode_supset = _libraries['FIXME_STUB'].netnode_supset
    netnode_supset.restype = ctypes.c_char
    netnode_supset.argtypes = [nodeidx_t, nodeidx_t, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_supset_idx8 = _libraries['FIXME_STUB'].netnode_supset_idx8
    netnode_supset_idx8.restype = ctypes.c_char
    netnode_supset_idx8.argtypes = [nodeidx_t, uchar, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_supshift = _libraries['FIXME_STUB'].netnode_supshift
    netnode_supshift.restype = size_t
    netnode_supshift.argtypes = [nodeidx_t, nodeidx_t, nodeidx_t, nodeidx_t, ctypes.c_int32]
    netnode_supstr = _libraries['FIXME_STUB'].netnode_supstr
    netnode_supstr.restype = ssize_t
    netnode_supstr.argtypes = [nodeidx_t, nodeidx_t, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_supstr_idx8 = _libraries['FIXME_STUB'].netnode_supstr_idx8
    netnode_supstr_idx8.restype = ssize_t
    netnode_supstr_idx8.argtypes = [nodeidx_t, uchar, ctypes.c_char_p, size_t, ctypes.c_int32]
    netnode_supval = _libraries['FIXME_STUB'].netnode_supval
    netnode_supval.restype = ssize_t
    netnode_supval.argtypes = [nodeidx_t, nodeidx_t, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_supval_idx8 = _libraries['FIXME_STUB'].netnode_supval_idx8
    netnode_supval_idx8.restype = ssize_t
    netnode_supval_idx8.argtypes = [nodeidx_t, uchar, ctypes.POINTER(None), size_t, ctypes.c_int32]
    netnode_valobj = _libraries['FIXME_STUB'].netnode_valobj
    netnode_valobj.restype = ssize_t
    netnode_valobj.argtypes = [nodeidx_t, ctypes.POINTER(None), size_t]
    netnode_valstr = _libraries['FIXME_STUB'].netnode_valstr
    netnode_valstr.restype = ssize_t
    netnode_valstr.argtypes = [nodeidx_t, ctypes.c_char_p, size_t]
    new_til = _libraries['FIXME_STUB'].new_til
    new_til.restype = ctypes.POINTER(struct_til_t)
    new_til.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    next_addr = _libraries['FIXME_STUB'].next_addr
    next_addr.restype = ea_t
    next_addr.argtypes = [ea_t]
    next_chunk = _libraries['FIXME_STUB'].next_chunk
    next_chunk.restype = ea_t
    next_chunk.argtypes = [ea_t]
    next_head = _libraries['FIXME_STUB'].next_head
    next_head.restype = ea_t
    next_head.argtypes = [ea_t, ea_t]
    next_idcv_attr = _libraries['FIXME_STUB'].next_idcv_attr
    next_idcv_attr.restype = ctypes.c_char_p
    next_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p]
    next_named_type = _libraries['FIXME_STUB'].next_named_type
    next_named_type.restype = ctypes.c_char_p
    next_named_type.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_int32]
    next_not_tail = _libraries['FIXME_STUB'].next_not_tail
    next_not_tail.restype = ea_t
    next_not_tail.argtypes = [ea_t]
    next_that = _libraries['FIXME_STUB'].next_that
    next_that.restype = ea_t
    next_that.argtypes = [ea_t, ea_t, ctypes.CFUNCTYPE(ctypes.c_char, flags_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    next_visea = _libraries['FIXME_STUB'].next_visea
    next_visea.restype = ea_t
    next_visea.argtypes = [ea_t]
    node2ea = _libraries['FIXME_STUB'].node2ea
    node2ea.restype = ea_t
    node2ea.argtypes = [nodeidx_t]
    node_iterator_goup = _libraries['FIXME_STUB'].node_iterator_goup
    node_iterator_goup.restype = ctypes.POINTER(struct_node_iterator)
    node_iterator_goup.argtypes = [ctypes.POINTER(struct_node_iterator)]
    notify_dirtree = _libraries['FIXME_STUB'].notify_dirtree
    notify_dirtree.restype = None
    notify_dirtree.argtypes = [ctypes.POINTER(struct_dirtree_impl_t), ctypes.c_char, inode_t]
    num_flag = _libraries['FIXME_STUB'].num_flag
    num_flag.restype = flags_t
    num_flag.argtypes = []
    numop2str = _libraries['FIXME_STUB'].numop2str
    numop2str.restype = size_t
    numop2str.argtypes = [ctypes.c_char_p, size_t, ea_t, ctypes.c_int32, uint64, ctypes.c_int32, ctypes.c_int32]
    op_adds_xrefs = _libraries['FIXME_STUB'].op_adds_xrefs
    op_adds_xrefs.restype = ctypes.c_char
    op_adds_xrefs.argtypes = [flags_t, ctypes.c_int32]
    op_custfmt = _libraries['FIXME_STUB'].op_custfmt
    op_custfmt.restype = ctypes.c_char
    op_custfmt.argtypes = [ea_t, ctypes.c_int32, ctypes.c_int32]
    op_enum = _libraries['FIXME_STUB'].op_enum
    op_enum.restype = ctypes.c_char
    op_enum.argtypes = [ea_t, ctypes.c_int32, enum_t, uchar]
    op_offset = _libraries['FIXME_STUB'].op_offset
    op_offset.restype = ctypes.c_char
    op_offset.argtypes = [ea_t, ctypes.c_int32, uint32, ea_t, ea_t, adiff_t]
    op_offset_ex = _libraries['FIXME_STUB'].op_offset_ex
    op_offset_ex.restype = ctypes.c_char
    op_offset_ex.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(struct_refinfo_t)]
    op_seg = _libraries['FIXME_STUB'].op_seg
    op_seg.restype = ctypes.c_char
    op_seg.argtypes = [ea_t, ctypes.c_int32]
    op_stkvar = _libraries['FIXME_STUB'].op_stkvar
    op_stkvar.restype = ctypes.c_char
    op_stkvar.argtypes = [ea_t, ctypes.c_int32]
    op_stroff = _libraries['FIXME_STUB'].op_stroff
    op_stroff.restype = ctypes.c_char
    op_stroff.argtypes = [ctypes.POINTER(struct_insn_t), ctypes.c_int32, ctypes.POINTER(tid_t), ctypes.c_int32, adiff_t]
    openM = _libraries['FIXME_STUB'].openM
    openM.restype = ctypes.POINTER(FILE)
    openM.argtypes = [ctypes.c_char_p]
    openR = _libraries['FIXME_STUB'].openR
    openR.restype = ctypes.POINTER(FILE)
    openR.argtypes = [ctypes.c_char_p]
    openRT = _libraries['FIXME_STUB'].openRT
    openRT.restype = ctypes.POINTER(FILE)
    openRT.argtypes = [ctypes.c_char_p]
    open_linput = _libraries['FIXME_STUB'].open_linput
    open_linput.restype = ctypes.POINTER(struct_linput_t)
    open_linput.argtypes = [ctypes.c_char_p, ctypes.c_char]
    optimize_argloc = _libraries['FIXME_STUB'].optimize_argloc
    optimize_argloc.restype = ctypes.c_char
    optimize_argloc.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.POINTER(struct_rangeset_t)]
    pack_dd = _libraries['FIXME_STUB'].pack_dd
    pack_dd.restype = ctypes.POINTER(uchar)
    pack_dd.argtypes = [ctypes.POINTER(uchar), ctypes.POINTER(uchar), uint32]
    pack_dq = _libraries['FIXME_STUB'].pack_dq
    pack_dq.restype = ctypes.POINTER(uchar)
    pack_dq.argtypes = [ctypes.POINTER(uchar), ctypes.POINTER(uchar), uint64]
    pack_ds = _libraries['FIXME_STUB'].pack_ds
    pack_ds.restype = ctypes.POINTER(uchar)
    pack_ds.argtypes = [ctypes.POINTER(uchar), ctypes.POINTER(uchar), ctypes.c_char_p, size_t]
    pack_dw = _libraries['FIXME_STUB'].pack_dw
    pack_dw.restype = ctypes.POINTER(uchar)
    pack_dw.argtypes = [ctypes.POINTER(uchar), ctypes.POINTER(uchar), uint16]
    pack_idcobj_to_bv = _libraries['FIXME_STUB'].pack_idcobj_to_bv
    pack_idcobj_to_bv.restype = error_t
    pack_idcobj_to_bv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_relobj_t), ctypes.POINTER(None), ctypes.c_int32]
    pack_idcobj_to_idb = _libraries['FIXME_STUB'].pack_idcobj_to_idb
    pack_idcobj_to_idb.restype = error_t
    pack_idcobj_to_idb.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ea_t, ctypes.c_int32]
    parse_binpat_str = _libraries['FIXME_STUB'].parse_binpat_str
    parse_binpat_str.restype = ctypes.c_char
    parse_binpat_str.argtypes = [ctypes.POINTER(compiled_binpat_vec_t), ea_t, ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(qstring)]
    parse_command_line = _libraries['FIXME_STUB'].parse_command_line
    parse_command_line.restype = size_t
    parse_command_line.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.POINTER(channel_redirs_t), ctypes.c_char_p, ctypes.c_int32]
    parse_config_value = _libraries['FIXME_STUB'].parse_config_value
    parse_config_value.restype = ctypes.c_char
    parse_config_value.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t)]
    parse_dbgopts = _libraries['FIXME_STUB'].parse_dbgopts
    parse_dbgopts.restype = ctypes.c_char
    parse_dbgopts.argtypes = [ctypes.POINTER(struct_instant_dbgopts_t), ctypes.c_char_p]
    parse_decl = _libraries['FIXME_STUB'].parse_decl
    parse_decl.restype = ctypes.c_char
    parse_decl.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(qstring), ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_int32]
    parse_decls = _libraries['FIXME_STUB'].parse_decls
    parse_decls.restype = ctypes.c_int32
    parse_decls.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, printer_t, ctypes.c_int32]
    parse_json = _libraries['FIXME_STUB'].parse_json
    parse_json.restype = error_t
    parse_json.argtypes = [ctypes.POINTER(struct_jvalue_t), ctypes.POINTER(struct_lexer_t), ctypes.POINTER(tokenstack_t)]
    parse_json_string = _libraries['FIXME_STUB'].parse_json_string
    parse_json_string.restype = error_t
    parse_json_string.argtypes = [ctypes.POINTER(struct_jvalue_t), ctypes.c_char_p]
    parse_reg_name = _libraries['FIXME_STUB'].parse_reg_name
    parse_reg_name.restype = ctypes.c_char
    parse_reg_name.argtypes = [ctypes.POINTER(struct_reg_info_t), ctypes.c_char_p]
    patch_byte = _libraries['FIXME_STUB'].patch_byte
    patch_byte.restype = ctypes.c_char
    patch_byte.argtypes = [ea_t, uint64]
    patch_bytes = _libraries['FIXME_STUB'].patch_bytes
    patch_bytes.restype = None
    patch_bytes.argtypes = [ea_t, ctypes.POINTER(None), size_t]
    patch_dword = _libraries['FIXME_STUB'].patch_dword
    patch_dword.restype = ctypes.c_char
    patch_dword.argtypes = [ea_t, uint64]
    patch_fixup_value = _libraries['FIXME_STUB'].patch_fixup_value
    patch_fixup_value.restype = ctypes.c_char
    patch_fixup_value.argtypes = [ea_t, ctypes.POINTER(struct_fixup_data_t)]
    patch_qword = _libraries['FIXME_STUB'].patch_qword
    patch_qword.restype = ctypes.c_char
    patch_qword.argtypes = [ea_t, uint64]
    patch_word = _libraries['FIXME_STUB'].patch_word
    patch_word.restype = ctypes.c_char
    patch_word.argtypes = [ea_t, uint64]
    peek_auto_queue = _libraries['FIXME_STUB'].peek_auto_queue
    peek_auto_queue.restype = ea_t
    peek_auto_queue.argtypes = [ea_t, atype_t]
    ph = ctypes_in_dll(struct_processor_t, _libraries['FIXME_STUB'], 'ph')
    plan_and_wait = _libraries['FIXME_STUB'].plan_and_wait
    plan_and_wait.restype = ctypes.c_int32
    plan_and_wait.argtypes = [ea_t, ea_t, ctypes.c_char]
    plan_to_apply_idasgn = _libraries['FIXME_STUB'].plan_to_apply_idasgn
    plan_to_apply_idasgn.restype = ctypes.c_int32
    plan_to_apply_idasgn.argtypes = [ctypes.c_char_p]
    prev_addr = _libraries['FIXME_STUB'].prev_addr
    prev_addr.restype = ea_t
    prev_addr.argtypes = [ea_t]
    prev_chunk = _libraries['FIXME_STUB'].prev_chunk
    prev_chunk.restype = ea_t
    prev_chunk.argtypes = [ea_t]
    prev_head = _libraries['FIXME_STUB'].prev_head
    prev_head.restype = ea_t
    prev_head.argtypes = [ea_t, ea_t]
    prev_idcv_attr = _libraries['FIXME_STUB'].prev_idcv_attr
    prev_idcv_attr.restype = ctypes.c_char_p
    prev_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p]
    prev_not_tail = _libraries['FIXME_STUB'].prev_not_tail
    prev_not_tail.restype = ea_t
    prev_not_tail.argtypes = [ea_t]
    prev_that = _libraries['FIXME_STUB'].prev_that
    prev_that.restype = ea_t
    prev_that.argtypes = [ea_t, ea_t, ctypes.CFUNCTYPE(ctypes.c_char, flags_t, ctypes.POINTER(None)), ctypes.POINTER(None)]
    prev_utf8_char = _libraries['FIXME_STUB'].prev_utf8_char
    prev_utf8_char.restype = ctypes.c_char
    prev_utf8_char.argtypes = [ctypes.POINTER(wchar32_t), ctypes.POINTER(ctypes.c_char_p), ctypes.c_char_p]
    prev_visea = _libraries['FIXME_STUB'].prev_visea
    prev_visea.restype = ea_t
    prev_visea.argtypes = [ea_t]
    print_argloc = _libraries['FIXME_STUB'].print_argloc
    print_argloc.restype = size_t
    print_argloc.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.c_int32]
    print_cdata = _libraries['FIXME_STUB'].print_cdata
    print_cdata.restype = ctypes.c_int32
    print_cdata.argtypes = [ctypes.POINTER(struct_text_sink_t), ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_format_data_info_t)]
    print_charlit = _libraries['FIXME_STUB'].print_charlit
    print_charlit.restype = ctypes.c_char
    print_charlit.argtypes = [ctypes.c_char_p, ctypes.POINTER(None), ctypes.c_int32]
    print_decls = _libraries['FIXME_STUB'].print_decls
    print_decls.restype = ctypes.c_int32
    print_decls.argtypes = [ctypes.POINTER(struct_text_sink_t), ctypes.POINTER(struct_til_t), ctypes.POINTER(ordvec_t), uint32]
    print_fpval = _libraries['FIXME_STUB'].print_fpval
    print_fpval.restype = ctypes.c_char
    print_fpval.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(None), ctypes.c_int32]
    print_idcv = _libraries['FIXME_STUB'].print_idcv
    print_idcv.restype = ctypes.c_char
    print_idcv.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.c_int32]
    print_insn_mnem = _libraries['FIXME_STUB'].print_insn_mnem
    print_insn_mnem.restype = ctypes.c_char
    print_insn_mnem.argtypes = [ctypes.POINTER(qstring), ea_t]
    print_operand = _libraries['FIXME_STUB'].print_operand
    print_operand.restype = ctypes.c_char
    print_operand.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(struct_printop_t)]
    print_strlit_type = _libraries['FIXME_STUB'].print_strlit_type
    print_strlit_type.restype = ctypes.c_char
    print_strlit_type.argtypes = [ctypes.POINTER(qstring), int32, ctypes.POINTER(qstring), ctypes.c_int32]
    print_tinfo = _libraries['FIXME_STUB'].print_tinfo
    print_tinfo.restype = ctypes.c_char
    print_tinfo.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.c_char_p]
    print_type = _libraries['FIXME_STUB'].print_type
    print_type.restype = ctypes.c_char
    print_type.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_int32]
    process_archive = _libraries['FIXME_STUB'].process_archive
    process_archive.restype = ctypes.c_int32
    process_archive.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_linput_t), ctypes.POINTER(qstring), ctypes.POINTER(ushort), ctypes.c_char_p, ctypes.POINTER(struct_load_info_t), ctypes.POINTER(qstring)]
    process_zip_linput = _libraries['FIXME_STUB'].process_zip_linput
    process_zip_linput.restype = ctypes.c_int32
    process_zip_linput.argtypes = [ctypes.POINTER(struct_linput_t), ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), int64, ctypes.c_int32, uint64, uint64, uint32, ctypes.c_char_p), ctypes.POINTER(None)]
    process_zipfile = _libraries['FIXME_STUB'].process_zipfile
    process_zipfile.restype = ctypes.c_int32
    process_zipfile.argtypes = [ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), int64, ctypes.c_int32, uint64, uint64, uint32, ctypes.c_char_p), ctypes.POINTER(None)]
    process_zipfile_entry = _libraries['FIXME_STUB'].process_zipfile_entry
    process_zipfile_entry.restype = ctypes.c_int32
    process_zipfile_entry.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), int64, ctypes.c_int32, uint64, uint64, uint32, ctypes.c_char_p), ctypes.POINTER(None), ctypes.c_char]
    put_byte = _libraries['FIXME_STUB'].put_byte
    put_byte.restype = ctypes.c_char
    put_byte.argtypes = [ea_t, uint64]
    put_bytes = _libraries['FIXME_STUB'].put_bytes
    put_bytes.restype = None
    put_bytes.argtypes = [ea_t, ctypes.POINTER(None), size_t]
    put_dbg_byte = _libraries['FIXME_STUB'].put_dbg_byte
    put_dbg_byte.restype = ctypes.c_char
    put_dbg_byte.argtypes = [ea_t, uint32]
    put_dword = _libraries['FIXME_STUB'].put_dword
    put_dword.restype = None
    put_dword.argtypes = [ea_t, uint64]
    put_qword = _libraries['FIXME_STUB'].put_qword
    put_qword.restype = None
    put_qword.argtypes = [ea_t, uint64]
    put_utf8_char = _libraries['FIXME_STUB'].put_utf8_char
    put_utf8_char.restype = ssize_t
    put_utf8_char.argtypes = [ctypes.c_char_p, wchar32_t]
    put_word = _libraries['FIXME_STUB'].put_word
    put_word.restype = None
    put_word.argtypes = [ea_t, uint64]
    qaccess = _libraries['FIXME_STUB'].qaccess
    qaccess.restype = ctypes.c_int32
    qaccess.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    qalloc = _libraries['FIXME_STUB'].qalloc
    qalloc.restype = ctypes.POINTER(None)
    qalloc.argtypes = [size_t]
    qalloc_or_throw = _libraries['FIXME_STUB'].qalloc_or_throw
    qalloc_or_throw.restype = ctypes.POINTER(None)
    qalloc_or_throw.argtypes = [size_t]
    qatexit = _libraries['FIXME_STUB'].qatexit
    qatexit.restype = None
    qatexit.argtypes = [ctypes.CFUNCTYPE(None)]
    qbasename = _libraries['FIXME_STUB'].qbasename
    qbasename.restype = ctypes.c_char_p
    qbasename.argtypes = [ctypes.c_char_p]
    qcalloc = _libraries['FIXME_STUB'].qcalloc
    qcalloc.restype = ctypes.POINTER(None)
    qcalloc.argtypes = [size_t, size_t]
    qchdir = _libraries['FIXME_STUB'].qchdir
    qchdir.restype = ctypes.c_int32
    qchdir.argtypes = [ctypes.c_char_p]
    qchsize = _libraries['FIXME_STUB'].qchsize
    qchsize.restype = ctypes.c_int32
    qchsize.argtypes = [ctypes.c_int32, uint64]
    qcleanline = _libraries['FIXME_STUB'].qcleanline
    qcleanline.restype = ssize_t
    qcleanline.argtypes = [ctypes.POINTER(qstring), ctypes.c_char, uint32]
    qclose = _libraries['FIXME_STUB'].qclose
    qclose.restype = ctypes.c_int32
    qclose.argtypes = [ctypes.c_int32]
    qcontrol_tty = _libraries['FIXME_STUB'].qcontrol_tty
    qcontrol_tty.restype = None
    qcontrol_tty.argtypes = []
    qcopyfile = _libraries['FIXME_STUB'].qcopyfile
    qcopyfile.restype = ctypes.c_int32
    qcopyfile.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char, ctypes.CFUNCTYPE(ctypes.c_char, uint64, uint64, ctypes.POINTER(None)), ctypes.POINTER(None), ctypes.c_int32]
    qcreate = _libraries['FIXME_STUB'].qcreate
    qcreate.restype = ctypes.c_int32
    qcreate.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    qctime = _libraries['FIXME_STUB'].qctime
    qctime.restype = ctypes.c_char
    qctime.argtypes = [ctypes.c_char_p, size_t, qtime32_t]
    qctime_utc = _libraries['FIXME_STUB'].qctime_utc
    qctime_utc.restype = ctypes.c_char
    qctime_utc.argtypes = [ctypes.c_char_p, size_t, qtime32_t]
    qdetach_tty = _libraries['FIXME_STUB'].qdetach_tty
    qdetach_tty.restype = None
    qdetach_tty.argtypes = []
    qdirname = _libraries['FIXME_STUB'].qdirname
    qdirname.restype = ctypes.c_char
    qdirname.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    qdup = _libraries['FIXME_STUB'].qdup
    qdup.restype = ctypes.c_int32
    qdup.argtypes = [ctypes.c_int32]
    qerrcode = _libraries['FIXME_STUB'].qerrcode
    qerrcode.restype = ctypes.c_int32
    qerrcode.argtypes = [ctypes.c_int32]
    qerrstr = _libraries['FIXME_STUB'].qerrstr
    qerrstr.restype = ctypes.c_char_p
    qerrstr.argtypes = [ctypes.c_int32]
    qexit = _libraries['FIXME_STUB'].qexit
    qexit.restype = None
    qexit.argtypes = [ctypes.c_int32]
    qfclose = _libraries['FIXME_STUB'].qfclose
    qfclose.restype = ctypes.c_int32
    qfclose.argtypes = [ctypes.POINTER(FILE)]
    qfgetc = _libraries['FIXME_STUB'].qfgetc
    qfgetc.restype = ctypes.c_int32
    qfgetc.argtypes = [ctypes.POINTER(FILE)]
    qfgets = _libraries['FIXME_STUB'].qfgets
    qfgets.restype = ctypes.c_char_p
    qfgets.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(FILE)]
    qfileexist = _libraries['FIXME_STUB'].qfileexist
    qfileexist.restype = ctypes.c_char
    qfileexist.argtypes = [ctypes.c_char_p]
    qfilelength = _libraries['FIXME_STUB'].qfilelength
    qfilelength.restype = uint64
    qfilelength.argtypes = [ctypes.c_int32]
    qfilesize = _libraries['FIXME_STUB'].qfilesize
    qfilesize.restype = uint64
    qfilesize.argtypes = [ctypes.c_char_p]
    qfindclose = _libraries['FIXME_STUB'].qfindclose
    qfindclose.restype = None
    qfindclose.argtypes = [ctypes.POINTER(struct_qffblk64_t)]
    qfindfirst = _libraries['FIXME_STUB'].qfindfirst
    qfindfirst.restype = ctypes.c_int32
    qfindfirst.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_qffblk64_t), ctypes.c_int32]
    qfindnext = _libraries['FIXME_STUB'].qfindnext
    qfindnext.restype = ctypes.c_int32
    qfindnext.argtypes = [ctypes.POINTER(struct_qffblk64_t)]
    qflush = _libraries['FIXME_STUB'].qflush
    qflush.restype = ctypes.c_int32
    qflush.argtypes = [ctypes.POINTER(FILE)]
    qfopen = _libraries['FIXME_STUB'].qfopen
    qfopen.restype = ctypes.POINTER(FILE)
    qfopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    qfputc = _libraries['FIXME_STUB'].qfputc
    qfputc.restype = ctypes.c_int32
    qfputc.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    qfputs = _libraries['FIXME_STUB'].qfputs
    qfputs.restype = ctypes.c_int32
    qfputs.argtypes = [ctypes.c_char_p, ctypes.POINTER(FILE)]
    qfread = _libraries['FIXME_STUB'].qfread
    qfread.restype = ssize_t
    qfread.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), size_t]
    qfree = _libraries['FIXME_STUB'].qfree
    qfree.restype = None
    qfree.argtypes = [ctypes.POINTER(None)]
    qfseek = _libraries['FIXME_STUB'].qfseek
    qfseek.restype = ctypes.c_int32
    qfseek.argtypes = [ctypes.POINTER(FILE), int64, ctypes.c_int32]
    qfsize = _libraries['FIXME_STUB'].qfsize
    qfsize.restype = uint64
    qfsize.argtypes = [ctypes.POINTER(FILE)]
    qfstat = _libraries['FIXME_STUB'].qfstat
    qfstat.restype = ctypes.c_int32
    qfstat.argtypes = [ctypes.c_int32, ctypes.POINTER(struct_qstatbuf)]
    qfsync = _libraries['FIXME_STUB'].qfsync
    qfsync.restype = ctypes.c_int32
    qfsync.argtypes = [ctypes.c_int32]
    qftell = _libraries['FIXME_STUB'].qftell
    qftell.restype = int64
    qftell.argtypes = [ctypes.POINTER(FILE)]
    qfwrite = _libraries['FIXME_STUB'].qfwrite
    qfwrite.restype = ssize_t
    qfwrite.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(None), size_t]
    qgetcwd = _libraries['FIXME_STUB'].qgetcwd
    qgetcwd.restype = None
    qgetcwd.argtypes = [ctypes.c_char_p, size_t]
    qgetenv = _libraries['FIXME_STUB'].qgetenv
    qgetenv.restype = ctypes.c_char
    qgetenv.argtypes = [ctypes.c_char_p, ctypes.POINTER(qstring)]
    qgetline = _libraries['FIXME_STUB'].qgetline
    qgetline.restype = ssize_t
    qgetline.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(FILE)]
    qgets = _libraries['FIXME_STUB'].qgets
    qgets.restype = ctypes.c_char_p
    qgets.argtypes = [ctypes.c_char_p, size_t]
    class struct_tm(Structure):
        pass
    
    qgmtime = _libraries['FIXME_STUB'].qgmtime
    qgmtime.restype = ctypes.c_char
    qgmtime.argtypes = [ctypes.POINTER(struct_tm), qtime32_t]
    qisabspath = _libraries['FIXME_STUB'].qisabspath
    qisabspath.restype = ctypes.c_char
    qisabspath.argtypes = [ctypes.c_char_p]
    qisdir = _libraries['FIXME_STUB'].qisdir
    qisdir.restype = ctypes.c_char
    qisdir.argtypes = [ctypes.c_char_p]
    qlfile = _libraries['FIXME_STUB'].qlfile
    qlfile.restype = ctypes.POINTER(FILE)
    qlfile.argtypes = [ctypes.POINTER(struct_linput_t)]
    qlgetc = _libraries['FIXME_STUB'].qlgetc
    qlgetc.restype = ctypes.c_int32
    qlgetc.argtypes = [ctypes.POINTER(struct_linput_t)]
    qlgets = _libraries['FIXME_STUB'].qlgets
    qlgets.restype = ctypes.c_char_p
    qlgets.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(struct_linput_t)]
    qlgetz = _libraries['FIXME_STUB'].qlgetz
    qlgetz.restype = ctypes.c_char_p
    qlgetz.argtypes = [ctypes.POINTER(struct_linput_t), int64, ctypes.c_char_p, size_t]
    qlocaltime = _libraries['FIXME_STUB'].qlocaltime
    qlocaltime.restype = ctypes.c_char
    qlocaltime.argtypes = [ctypes.POINTER(struct_tm), qtime32_t]
    qlread = _libraries['FIXME_STUB'].qlread
    qlread.restype = ssize_t
    qlread.argtypes = [ctypes.POINTER(struct_linput_t), ctypes.POINTER(None), size_t]
    qlseek = _libraries['FIXME_STUB'].qlseek
    qlseek.restype = int64
    qlseek.argtypes = [ctypes.POINTER(struct_linput_t), int64, ctypes.c_int32]
    qlsize = _libraries['FIXME_STUB'].qlsize
    qlsize.restype = int64
    qlsize.argtypes = [ctypes.POINTER(struct_linput_t)]
    qmake_full_path = _libraries['FIXME_STUB'].qmake_full_path
    qmake_full_path.restype = ctypes.c_char_p
    qmake_full_path.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    qmakefile = _libraries['FIXME_STUB'].qmakefile
    qmakefile.restype = ctypes.c_char_p
    qmakefile.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p]
    qmakepath = _libraries['FIXME_STUB'].qmakepath
    qmakepath.restype = ctypes.c_char_p
    qmakepath.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    qmkdir = _libraries['FIXME_STUB'].qmkdir
    qmkdir.restype = ctypes.c_int32
    qmkdir.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    qmove = _libraries['FIXME_STUB'].qmove
    qmove.restype = ctypes.c_int32
    qmove.argtypes = [ctypes.c_char_p, ctypes.c_char_p, uint32]
    qmutex_create = _libraries['FIXME_STUB'].qmutex_create
    qmutex_create.restype = qmutex_t
    qmutex_create.argtypes = []
    qmutex_free = _libraries['FIXME_STUB'].qmutex_free
    qmutex_free.restype = ctypes.c_char
    qmutex_free.argtypes = [qmutex_t]
    qmutex_lock = _libraries['FIXME_STUB'].qmutex_lock
    qmutex_lock.restype = ctypes.c_char
    qmutex_lock.argtypes = [qmutex_t]
    qmutex_unlock = _libraries['FIXME_STUB'].qmutex_unlock
    qmutex_unlock.restype = ctypes.c_char
    qmutex_unlock.argtypes = [qmutex_t]
    qopen = _libraries['FIXME_STUB'].qopen
    qopen.restype = ctypes.c_int32
    qopen.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    qopen_shared = _libraries['FIXME_STUB'].qopen_shared
    qopen_shared.restype = ctypes.c_int32
    qopen_shared.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    qpipe_close = _libraries['FIXME_STUB'].qpipe_close
    qpipe_close.restype = ctypes.c_int32
    qpipe_close.argtypes = [qhandle_t]
    qpipe_create = _libraries['FIXME_STUB'].qpipe_create
    qpipe_create.restype = ctypes.c_int32
    qpipe_create.argtypes = [ctypes.POINTER(None) * 2]
    qpipe_read = _libraries['FIXME_STUB'].qpipe_read
    qpipe_read.restype = ssize_t
    qpipe_read.argtypes = [qhandle_t, ctypes.POINTER(None), size_t]
    qpipe_write = _libraries['FIXME_STUB'].qpipe_write
    qpipe_write.restype = ssize_t
    qpipe_write.argtypes = [qhandle_t, ctypes.POINTER(None), size_t]
    qread = _libraries['FIXME_STUB'].qread
    qread.restype = ctypes.c_int32
    qread.argtypes = [ctypes.c_int32, ctypes.POINTER(None), size_t]
    qrealloc = _libraries['FIXME_STUB'].qrealloc
    qrealloc.restype = ctypes.POINTER(None)
    qrealloc.argtypes = [ctypes.POINTER(None), size_t]
    qrealloc_or_throw = _libraries['FIXME_STUB'].qrealloc_or_throw
    qrealloc_or_throw.restype = ctypes.POINTER(None)
    qrealloc_or_throw.argtypes = [ctypes.POINTER(None), size_t]
    qregcomp = _libraries['FIXME_STUB'].qregcomp
    qregcomp.restype = ctypes.c_int32
    qregcomp.argtypes = [ctypes.POINTER(struct_regex_t), ctypes.c_char_p, ctypes.c_int32]
    qregerror = _libraries['FIXME_STUB'].qregerror
    qregerror.restype = size_t
    qregerror.argtypes = [ctypes.c_int32, ctypes.POINTER(struct_regex_t), ctypes.c_char_p, size_t]
    qregexec = _libraries['FIXME_STUB'].qregexec
    qregexec.restype = ctypes.c_int32
    qregexec.argtypes = [ctypes.POINTER(struct_regex_t), ctypes.c_char_p, size_t, struct_regmatch_t * 0, ctypes.c_int32]
    qregfree = _libraries['FIXME_STUB'].qregfree
    qregfree.restype = None
    qregfree.argtypes = [ctypes.POINTER(struct_regex_t)]
    qrename = _libraries['FIXME_STUB'].qrename
    qrename.restype = ctypes.c_int32
    qrename.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    qrmdir = _libraries['FIXME_STUB'].qrmdir
    qrmdir.restype = ctypes.c_int32
    qrmdir.argtypes = [ctypes.c_char_p]
    qseek = _libraries['FIXME_STUB'].qseek
    qseek.restype = int64
    qseek.argtypes = [ctypes.c_int32, int64, ctypes.c_int32]
    qsem_create = _libraries['FIXME_STUB'].qsem_create
    qsem_create.restype = qsemaphore_t
    qsem_create.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    qsem_free = _libraries['FIXME_STUB'].qsem_free
    qsem_free.restype = ctypes.c_char
    qsem_free.argtypes = [qsemaphore_t]
    qsem_post = _libraries['FIXME_STUB'].qsem_post
    qsem_post.restype = ctypes.c_char
    qsem_post.argtypes = [qsemaphore_t]
    qsem_wait = _libraries['FIXME_STUB'].qsem_wait
    qsem_wait.restype = ctypes.c_char
    qsem_wait.argtypes = [qsemaphore_t, ctypes.c_int32]
    qsetenv = _libraries['FIXME_STUB'].qsetenv
    qsetenv.restype = ctypes.c_char
    qsetenv.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    qsleep = _libraries['FIXME_STUB'].qsleep
    qsleep.restype = None
    qsleep.argtypes = [ctypes.c_int32]
    qsnprintf = _libraries['FIXME_STUB'].qsnprintf
    qsnprintf.restype = ctypes.c_int32
    qsnprintf.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    qsplitfile = _libraries['FIXME_STUB'].qsplitfile
    qsplitfile.restype = ctypes.c_char_p
    qsplitfile.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_char_p)]
    qsscanf = _libraries['FIXME_STUB'].qsscanf
    qsscanf.restype = ctypes.c_int32
    qsscanf.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    qstat = _libraries['FIXME_STUB'].qstat
    qstat.restype = ctypes.c_int32
    qstat.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_qstatbuf)]
    qstpncpy = _libraries['FIXME_STUB'].qstpncpy
    qstpncpy.restype = ctypes.c_char_p
    qstpncpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    qstr2user = _libraries['FIXME_STUB'].qstr2user
    qstr2user.restype = None
    qstr2user.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    qstrchr = _libraries['FIXME_STUB'].qstrchr
    qstrchr.restype = ctypes.POINTER(wchar16_t)
    qstrchr.argtypes = [ctypes.POINTER(wchar16_t), wchar16_t]
    qstrcmp = _libraries['FIXME_STUB'].qstrcmp
    qstrcmp.restype = ctypes.c_int32
    qstrcmp.argtypes = [ctypes.POINTER(wchar16_t), ctypes.POINTER(wchar16_t)]
    qstrdup = _libraries['FIXME_STUB'].qstrdup
    qstrdup.restype = ctypes.c_char_p
    qstrdup.argtypes = [ctypes.c_char_p]
    qstrerror = _libraries['FIXME_STUB'].qstrerror
    qstrerror.restype = ctypes.c_char_p
    qstrerror.argtypes = [error_t]
    qstrftime = _libraries['FIXME_STUB'].qstrftime
    qstrftime.restype = size_t
    qstrftime.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, qtime32_t]
    qstrftime64 = _libraries['FIXME_STUB'].qstrftime64
    qstrftime64.restype = size_t
    qstrftime64.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, qtime64_t]
    qstrlen = _libraries['FIXME_STUB'].qstrlen
    qstrlen.restype = size_t
    qstrlen.argtypes = [ctypes.POINTER(wchar16_t)]
    qstrlwr = _libraries['FIXME_STUB'].qstrlwr
    qstrlwr.restype = ctypes.c_char_p
    qstrlwr.argtypes = [ctypes.c_char_p]
    qstrncat = _libraries['FIXME_STUB'].qstrncat
    qstrncat.restype = ctypes.c_char_p
    qstrncat.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    qstrncpy = _libraries['FIXME_STUB'].qstrncpy
    qstrncpy.restype = ctypes.c_char_p
    qstrncpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    qstrrchr = _libraries['FIXME_STUB'].qstrrchr
    qstrrchr.restype = ctypes.POINTER(wchar16_t)
    qstrrchr.argtypes = [ctypes.POINTER(wchar16_t), wchar16_t]
    qstrtok = _libraries['FIXME_STUB'].qstrtok
    qstrtok.restype = ctypes.c_char_p
    qstrtok.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
    qstrupr = _libraries['FIXME_STUB'].qstrupr
    qstrupr.restype = ctypes.c_char_p
    qstrupr.argtypes = [ctypes.c_char_p]
    qtell = _libraries['FIXME_STUB'].qtell
    qtell.restype = int64
    qtell.argtypes = [ctypes.c_int32]
    qthread_create = _libraries['FIXME_STUB'].qthread_create
    qthread_create.restype = qthread_t
    qthread_create.argtypes = [ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None)), ctypes.POINTER(None)]
    qthread_equal = _libraries['FIXME_STUB'].qthread_equal
    qthread_equal.restype = ctypes.c_char
    qthread_equal.argtypes = [qthread_t, qthread_t]
    qthread_free = _libraries['FIXME_STUB'].qthread_free
    qthread_free.restype = None
    qthread_free.argtypes = [qthread_t]
    qthread_join = _libraries['FIXME_STUB'].qthread_join
    qthread_join.restype = ctypes.c_char
    qthread_join.argtypes = [qthread_t]
    qthread_kill = _libraries['FIXME_STUB'].qthread_kill
    qthread_kill.restype = ctypes.c_char
    qthread_kill.argtypes = [qthread_t]
    qthread_same = _libraries['FIXME_STUB'].qthread_same
    qthread_same.restype = ctypes.c_char
    qthread_same.argtypes = [qthread_t]
    qthread_self = _libraries['FIXME_STUB'].qthread_self
    qthread_self.restype = qthread_t
    qthread_self.argtypes = []
    qtime64 = _libraries['FIXME_STUB'].qtime64
    qtime64.restype = qtime64_t
    qtime64.argtypes = []
    qtimegm = _libraries['FIXME_STUB'].qtimegm
    qtimegm.restype = qtime32_t
    qtimegm.argtypes = [ctypes.POINTER(struct_tm)]
    qtmpfile = _libraries['FIXME_STUB'].qtmpfile
    qtmpfile.restype = ctypes.POINTER(FILE)
    qtmpfile.argtypes = []
    qtmpnam = _libraries['FIXME_STUB'].qtmpnam
    qtmpnam.restype = ctypes.c_char_p
    qtmpnam.argtypes = [ctypes.c_char_p, size_t]
    qunlink = _libraries['FIXME_STUB'].qunlink
    qunlink.restype = ctypes.c_int32
    qunlink.argtypes = [ctypes.c_char_p]
    quote_cmdline_arg = _libraries['FIXME_STUB'].quote_cmdline_arg
    quote_cmdline_arg.restype = ctypes.c_char
    quote_cmdline_arg.argtypes = [ctypes.POINTER(qstring)]
    qustrlen = _libraries['FIXME_STUB'].qustrlen
    qustrlen.restype = size_t
    qustrlen.argtypes = [ctypes.c_char_p]
    qustrncpy = _libraries['FIXME_STUB'].qustrncpy
    qustrncpy.restype = ctypes.c_char
    qustrncpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    qvector_reserve = _libraries['FIXME_STUB'].qvector_reserve
    qvector_reserve.restype = ctypes.POINTER(None)
    qvector_reserve.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t, size_t]
    qveprintf = _libraries['FIXME_STUB'].qveprintf
    qveprintf.restype = ctypes.c_int32
    qveprintf.argtypes = [ctypes.c_char_p, va_list]
    qvfprintf = _libraries['FIXME_STUB'].qvfprintf
    qvfprintf.restype = ctypes.c_int32
    qvfprintf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    qvfscanf = _libraries['FIXME_STUB'].qvfscanf
    qvfscanf.restype = ctypes.c_int32
    qvfscanf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    qvprintf = _libraries['FIXME_STUB'].qvprintf
    qvprintf.restype = ctypes.c_int32
    qvprintf.argtypes = [ctypes.c_char_p, va_list]
    qvsnprintf = _libraries['FIXME_STUB'].qvsnprintf
    qvsnprintf.restype = ctypes.c_int32
    qvsnprintf.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    qvsscanf = _libraries['FIXME_STUB'].qvsscanf
    qvsscanf.restype = ctypes.c_int32
    qvsscanf.argtypes = [ctypes.c_char_p, ctypes.c_char_p, va_list]
    qwait_for_handles = _libraries['FIXME_STUB'].qwait_for_handles
    qwait_for_handles.restype = ctypes.c_int32
    qwait_for_handles.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(qhandle_t), ctypes.c_int32, uint32, ctypes.c_int32]
    qwait_timed = _libraries['FIXME_STUB'].qwait_timed
    qwait_timed.restype = ctypes.c_int32
    qwait_timed.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    qwrite = _libraries['FIXME_STUB'].qwrite
    qwrite.restype = ctypes.c_int32
    qwrite.argtypes = [ctypes.c_int32, ctypes.POINTER(None), size_t]
    r50_to_asc = _libraries['FIXME_STUB'].r50_to_asc
    r50_to_asc.restype = ctypes.c_int32
    r50_to_asc.argtypes = [ctypes.c_char_p, ctypes.POINTER(ushort), ctypes.c_int32]
    range_t_print = _libraries['FIXME_STUB'].range_t_print
    range_t_print.restype = size_t
    range_t_print.argtypes = [ctypes.POINTER(struct_range_t), ctypes.c_char_p, size_t]
    rangeset_t_add = _libraries['FIXME_STUB'].rangeset_t_add
    rangeset_t_add.restype = ctypes.c_char
    rangeset_t_add.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_range_t)]
    rangeset_t_add2 = _libraries['FIXME_STUB'].rangeset_t_add2
    rangeset_t_add2.restype = ctypes.c_char
    rangeset_t_add2.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_contains = _libraries['FIXME_STUB'].rangeset_t_contains
    rangeset_t_contains.restype = ctypes.c_char
    rangeset_t_contains.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_find_range = _libraries['FIXME_STUB'].rangeset_t_find_range
    rangeset_t_find_range.restype = ctypes.POINTER(struct_range_t)
    rangeset_t_find_range.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_has_common = _libraries['FIXME_STUB'].rangeset_t_has_common
    rangeset_t_has_common.restype = ctypes.c_char
    rangeset_t_has_common.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_range_t), ctypes.c_char]
    rangeset_t_has_common2 = _libraries['FIXME_STUB'].rangeset_t_has_common2
    rangeset_t_has_common2.restype = ctypes.c_char
    rangeset_t_has_common2.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_intersect = _libraries['FIXME_STUB'].rangeset_t_intersect
    rangeset_t_intersect.restype = ctypes.c_char
    rangeset_t_intersect.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_lower_bound = _libraries['FIXME_STUB'].rangeset_t_lower_bound
    rangeset_t_lower_bound.restype = qvector_range_t___const_iterator
    rangeset_t_lower_bound.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_next_addr = _libraries['FIXME_STUB'].rangeset_t_next_addr
    rangeset_t_next_addr.restype = ea_t
    rangeset_t_next_addr.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_next_range = _libraries['FIXME_STUB'].rangeset_t_next_range
    rangeset_t_next_range.restype = ea_t
    rangeset_t_next_range.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_prev_addr = _libraries['FIXME_STUB'].rangeset_t_prev_addr
    rangeset_t_prev_addr.restype = ea_t
    rangeset_t_prev_addr.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_prev_range = _libraries['FIXME_STUB'].rangeset_t_prev_range
    rangeset_t_prev_range.restype = ea_t
    rangeset_t_prev_range.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    rangeset_t_print = _libraries['FIXME_STUB'].rangeset_t_print
    rangeset_t_print.restype = size_t
    rangeset_t_print.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.c_char_p, size_t]
    rangeset_t_sub = _libraries['FIXME_STUB'].rangeset_t_sub
    rangeset_t_sub.restype = ctypes.c_char
    rangeset_t_sub.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_range_t)]
    rangeset_t_sub2 = _libraries['FIXME_STUB'].rangeset_t_sub2
    rangeset_t_sub2.restype = ctypes.c_char
    rangeset_t_sub2.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_swap = _libraries['FIXME_STUB'].rangeset_t_swap
    rangeset_t_swap.restype = None
    rangeset_t_swap.argtypes = [ctypes.POINTER(struct_rangeset_t), ctypes.POINTER(struct_rangeset_t)]
    rangeset_t_upper_bound = _libraries['FIXME_STUB'].rangeset_t_upper_bound
    rangeset_t_upper_bound.restype = qvector_range_t___const_iterator
    rangeset_t_upper_bound.argtypes = [ctypes.POINTER(struct_rangeset_t), ea_t]
    read2bytes = _libraries['FIXME_STUB'].read2bytes
    read2bytes.restype = ctypes.c_int32
    read2bytes.argtypes = [ctypes.c_int32, ctypes.POINTER(uint16), ctypes.c_char]
    read_config = _libraries['FIXME_STUB'].read_config
    read_config.restype = ctypes.c_char
    read_config.argtypes = [ctypes.c_char_p, ctypes.c_char, struct_cfgopt_t * 0, size_t, ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t)), ctypes.POINTER(ctypes.c_char_p), size_t]
    read_config2 = _libraries['FIXME_STUB'].read_config2
    read_config2.restype = ctypes.c_char
    read_config2.argtypes = [ctypes.c_char_p, ctypes.c_char, struct_cfgopt_t * 0, size_t, ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(struct_lexer_t), ctypes.POINTER(struct_token_t), ctypes.POINTER(struct_token_t)), ctypes.POINTER(ctypes.c_char_p), size_t, ctypes.POINTER(None)]
    read_ioports = _libraries['FIXME_STUB'].read_ioports
    read_ioports.restype = ssize_t
    read_ioports.argtypes = [ctypes.POINTER(ioports_t), ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.CFUNCTYPE(ctypes.c_char_p, ctypes.POINTER(ioports_t), ctypes.c_char_p)]
    read_ioports2 = _libraries['FIXME_STUB'].read_ioports2
    read_ioports2.restype = ssize_t
    read_ioports2.argtypes = [ctypes.POINTER(ioports_t), ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.POINTER(struct_ioports_fallback_t)]
    read_regargs = _libraries['FIXME_STUB'].read_regargs
    read_regargs.restype = None
    read_regargs.argtypes = [ctypes.POINTER(struct_func_t)]
    read_struc_path = _libraries['FIXME_STUB'].read_struc_path
    read_struc_path.restype = ctypes.c_int32
    read_struc_path.argtypes = [ctypes.POINTER(tid_t), ctypes.POINTER(adiff_t), ea_t, ctypes.c_int32]
    read_tinfo_bitfield_value = _libraries['FIXME_STUB'].read_tinfo_bitfield_value
    read_tinfo_bitfield_value.restype = uint64
    read_tinfo_bitfield_value.argtypes = [uint32, uint64, ctypes.c_int32]
    readbytes = _libraries['FIXME_STUB'].readbytes
    readbytes.restype = ctypes.c_int32
    readbytes.argtypes = [ctypes.c_int32, ctypes.POINTER(uint32), ctypes.c_int32, ctypes.c_char]
    realtoasc = _libraries['FIXME_STUB'].realtoasc
    realtoasc.restype = None
    realtoasc.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(struct_fpvalue_t), uint]
    reanalyze_callers = _libraries['FIXME_STUB'].reanalyze_callers
    reanalyze_callers.restype = None
    reanalyze_callers.argtypes = [ea_t, ctypes.c_char]
    reanalyze_function = _libraries['FIXME_STUB'].reanalyze_function
    reanalyze_function.restype = None
    reanalyze_function.argtypes = [ctypes.POINTER(struct_func_t), ea_t, ea_t, ctypes.c_char]
    reanalyze_noret_flag = _libraries['FIXME_STUB'].reanalyze_noret_flag
    reanalyze_noret_flag.restype = ctypes.c_char
    reanalyze_noret_flag.argtypes = [ea_t]
    rebase_program = _libraries['FIXME_STUB'].rebase_program
    rebase_program.restype = ctypes.c_int32
    rebase_program.argtypes = [adiff_t, ctypes.c_int32]
    rebuild_nlist = _libraries['FIXME_STUB'].rebuild_nlist
    rebuild_nlist.restype = None
    rebuild_nlist.argtypes = []
    recalc_spd = _libraries['FIXME_STUB'].recalc_spd
    recalc_spd.restype = ctypes.c_char
    recalc_spd.argtypes = [ea_t]
    reg_bin_op = _libraries['FIXME_STUB'].reg_bin_op
    reg_bin_op.restype = ctypes.c_char
    reg_bin_op.argtypes = [ctypes.c_char_p, ctypes.c_char, ctypes.POINTER(None), size_t, ctypes.c_char_p, ctypes.c_int32]
    reg_data_type = _libraries['FIXME_STUB'].reg_data_type
    reg_data_type.restype = ctypes.c_char
    reg_data_type.argtypes = [ctypes.POINTER(regval_type_t), ctypes.c_char_p, ctypes.c_char_p]
    reg_delete = _libraries['FIXME_STUB'].reg_delete
    reg_delete.restype = ctypes.c_char
    reg_delete.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    reg_delete_subkey = _libraries['FIXME_STUB'].reg_delete_subkey
    reg_delete_subkey.restype = ctypes.c_char
    reg_delete_subkey.argtypes = [ctypes.c_char_p]
    reg_delete_tree = _libraries['FIXME_STUB'].reg_delete_tree
    reg_delete_tree.restype = ctypes.c_char
    reg_delete_tree.argtypes = [ctypes.c_char_p]
    reg_exists = _libraries['FIXME_STUB'].reg_exists
    reg_exists.restype = ctypes.c_char
    reg_exists.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    reg_flush = _libraries['FIXME_STUB'].reg_flush
    reg_flush.restype = None
    reg_flush.argtypes = []
    reg_int_op = _libraries['FIXME_STUB'].reg_int_op
    reg_int_op.restype = ctypes.c_int32
    reg_int_op.argtypes = [ctypes.c_char_p, ctypes.c_char, ctypes.c_int32, ctypes.c_char_p]
    reg_load = _libraries['FIXME_STUB'].reg_load
    reg_load.restype = None
    reg_load.argtypes = []
    reg_read_strlist = _libraries['FIXME_STUB'].reg_read_strlist
    reg_read_strlist.restype = None
    reg_read_strlist.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.c_char_p]
    reg_str_get = _libraries['FIXME_STUB'].reg_str_get
    reg_str_get.restype = ctypes.c_char
    reg_str_get.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_char_p]
    reg_str_set = _libraries['FIXME_STUB'].reg_str_set
    reg_str_set.restype = None
    reg_str_set.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    reg_subkey_children = _libraries['FIXME_STUB'].reg_subkey_children
    reg_subkey_children.restype = ctypes.c_char
    reg_subkey_children.argtypes = [ctypes.POINTER(qstrvec_t), ctypes.c_char_p, ctypes.c_char]
    reg_subkey_exists = _libraries['FIXME_STUB'].reg_subkey_exists
    reg_subkey_exists.restype = ctypes.c_char
    reg_subkey_exists.argtypes = [ctypes.c_char_p]
    reg_update_strlist = _libraries['FIXME_STUB'].reg_update_strlist
    reg_update_strlist.restype = None
    reg_update_strlist.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char]
    regcomp = _libraries['FIXME_STUB'].regcomp
    regcomp.restype = ctypes.c_int32
    regcomp.argtypes = [ctypes.POINTER(struct_regex_t), ctypes.c_char_p, ctypes.c_int32]
    regerror = _libraries['FIXME_STUB'].regerror
    regerror.restype = size_t
    regerror.argtypes = [ctypes.c_int32, ctypes.POINTER(struct_regex_t), ctypes.c_char_p, size_t]
    regex_match = _libraries['FIXME_STUB'].regex_match
    regex_match.restype = ctypes.c_int32
    regex_match.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char]
    regexec = _libraries['FIXME_STUB'].regexec
    regexec.restype = ctypes.c_int32
    regexec.argtypes = [ctypes.POINTER(struct_regex_t), ctypes.c_char_p, size_t, struct_regmatch_t * 0, ctypes.c_int32]
    regfree = _libraries['FIXME_STUB'].regfree
    regfree.restype = None
    regfree.argtypes = [ctypes.POINTER(struct_regex_t)]
    register_custom_data_format = _libraries['FIXME_STUB'].register_custom_data_format
    register_custom_data_format.restype = ctypes.c_int32
    register_custom_data_format.argtypes = [ctypes.POINTER(struct_data_format_t)]
    register_custom_data_type = _libraries['FIXME_STUB'].register_custom_data_type
    register_custom_data_type.restype = ctypes.c_int32
    register_custom_data_type.argtypes = [ctypes.POINTER(struct_data_type_t)]
    register_custom_fixup = _libraries['FIXME_STUB'].register_custom_fixup
    register_custom_fixup.restype = fixup_type_t
    register_custom_fixup.argtypes = [ctypes.POINTER(struct_fixup_handler_t)]
    register_custom_refinfo = _libraries['FIXME_STUB'].register_custom_refinfo
    register_custom_refinfo.restype = ctypes.c_int32
    register_custom_refinfo.argtypes = [ctypes.POINTER(struct_custom_refinfo_handler_t)]
    register_loc_converter2 = _libraries['FIXME_STUB'].register_loc_converter2
    register_loc_converter2.restype = None
    register_loc_converter2.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.CFUNCTYPE(lecvt_code_t, ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_lochist_entry_t), ctypes.POINTER(struct_TWidget), uint32)]
    register_post_event_visitor = _libraries['FIXME_STUB'].register_post_event_visitor
    register_post_event_visitor.restype = ctypes.c_char
    register_post_event_visitor.argtypes = [hook_type_t, ctypes.POINTER(struct_post_event_visitor_t), ctypes.POINTER(struct_plugmod_t)]
    reload_file = _libraries['FIXME_STUB'].reload_file
    reload_file.restype = ctypes.c_char
    reload_file.argtypes = [ctypes.c_char_p, ctypes.c_char]
    reloc_value = _libraries['FIXME_STUB'].reloc_value
    reloc_value.restype = None
    reloc_value.argtypes = [ctypes.POINTER(None), ctypes.c_int32, adiff_t, ctypes.c_char]
    relocate_relobj = _libraries['FIXME_STUB'].relocate_relobj
    relocate_relobj.restype = ctypes.c_char
    relocate_relobj.argtypes = [ctypes.POINTER(struct_relobj_t), ea_t, ctypes.c_char]
    remember_problem = _libraries['FIXME_STUB'].remember_problem
    remember_problem.restype = None
    remember_problem.argtypes = [problist_id_t, ea_t, ctypes.c_char_p]
    remove_abi_opts = _libraries['FIXME_STUB'].remove_abi_opts
    remove_abi_opts.restype = ctypes.c_char
    remove_abi_opts.argtypes = [ctypes.c_char_p, ctypes.c_char]
    remove_custom_argloc = _libraries['FIXME_STUB'].remove_custom_argloc
    remove_custom_argloc.restype = ctypes.c_char
    remove_custom_argloc.argtypes = [ctypes.c_int32]
    remove_event_listener = _libraries['FIXME_STUB'].remove_event_listener
    remove_event_listener.restype = None
    remove_event_listener.argtypes = [ctypes.POINTER(struct_event_listener_t)]
    remove_extlang = _libraries['FIXME_STUB'].remove_extlang
    remove_extlang.restype = ctypes.c_char
    remove_extlang.argtypes = [ctypes.POINTER(struct_extlang_t)]
    remove_func_tail = _libraries['FIXME_STUB'].remove_func_tail
    remove_func_tail.restype = ctypes.c_char
    remove_func_tail.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    remove_tinfo_pointer = _libraries['FIXME_STUB'].remove_tinfo_pointer
    remove_tinfo_pointer.restype = ctypes.c_char
    remove_tinfo_pointer.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(struct_til_t)]
    rename_encoding = _libraries['FIXME_STUB'].rename_encoding
    rename_encoding.restype = ctypes.c_char
    rename_encoding.argtypes = [ctypes.c_int32, ctypes.c_char_p]
    rename_entry = _libraries['FIXME_STUB'].rename_entry
    rename_entry.restype = ctypes.c_char
    rename_entry.argtypes = [uval_t, ctypes.c_char_p, ctypes.c_int32]
    rename_regvar = _libraries['FIXME_STUB'].rename_regvar
    rename_regvar.restype = ctypes.c_int32
    rename_regvar.argtypes = [ctypes.POINTER(struct_func_t), ctypes.POINTER(struct_regvar_t), ctypes.c_char_p]
    reorder_dummy_names = _libraries['FIXME_STUB'].reorder_dummy_names
    reorder_dummy_names.restype = None
    reorder_dummy_names.argtypes = []
    replace_ordinal_typerefs = _libraries['FIXME_STUB'].replace_ordinal_typerefs
    replace_ordinal_typerefs.restype = ctypes.c_int32
    replace_ordinal_typerefs.argtypes = [ctypes.POINTER(struct_til_t), ctypes.POINTER(struct_tinfo_t)]
    replace_tabs = _libraries['FIXME_STUB'].replace_tabs
    replace_tabs.restype = ctypes.c_char
    replace_tabs.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    request_refresh = _libraries['FIXME_STUB'].request_refresh
    request_refresh.restype = None
    request_refresh.argtypes = [uint64, ctypes.c_char]
    resolve_typedef = _libraries['FIXME_STUB'].resolve_typedef
    resolve_typedef.restype = ctypes.POINTER(type_t)
    resolve_typedef.argtypes = [ctypes.POINTER(struct_til_t), ctypes.POINTER(type_t)]
    retrieve_custom_argloc = _libraries['FIXME_STUB'].retrieve_custom_argloc
    retrieve_custom_argloc.restype = ctypes.POINTER(struct_custloc_desc_t)
    retrieve_custom_argloc.argtypes = [ctypes.c_int32]
    revert_byte = _libraries['FIXME_STUB'].revert_byte
    revert_byte.restype = ctypes.c_char
    revert_byte.argtypes = [ea_t]
    revert_ida_decisions = _libraries['FIXME_STUB'].revert_ida_decisions
    revert_ida_decisions.restype = None
    revert_ida_decisions.argtypes = [ea_t, ea_t]
    root_node = ctypes_in_dll(struct_netnode, _libraries['FIXME_STUB'], 'root_node')
    rotate_left = _libraries['FIXME_STUB'].rotate_left
    rotate_left.restype = uval_t
    rotate_left.argtypes = [uval_t, ctypes.c_int32, size_t, size_t]
    round_down_power2 = _libraries['FIXME_STUB'].round_down_power2
    round_down_power2.restype = uint32
    round_down_power2.argtypes = [uint32]
    round_up_power2 = _libraries['FIXME_STUB'].round_up_power2
    round_up_power2.restype = uint32
    round_up_power2.argtypes = [uint32]
    run_plugin = _libraries['FIXME_STUB'].run_plugin
    run_plugin.restype = ctypes.c_char
    run_plugin.argtypes = [ctypes.POINTER(struct_plugin_t), size_t]
    same_value_jpt = _libraries['FIXME_STUB'].same_value_jpt
    same_value_jpt.restype = ctypes.c_char
    same_value_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.POINTER(struct_op_t), ctypes.c_int32]
    sanitize_file_name = _libraries['FIXME_STUB'].sanitize_file_name
    sanitize_file_name.restype = ctypes.c_char
    sanitize_file_name.argtypes = [ctypes.c_char_p, size_t]
    save_database = _libraries['FIXME_STUB'].save_database
    save_database.restype = ctypes.c_char
    save_database.argtypes = [ctypes.c_char_p, uint32, ctypes.POINTER(struct_snapshot_t), ctypes.POINTER(struct_snapshot_t)]
    save_dirtree = _libraries['FIXME_STUB'].save_dirtree
    save_dirtree.restype = ctypes.c_char
    save_dirtree.argtypes = [ctypes.POINTER(struct_dirtree_impl_t)]
    save_struc = _libraries['FIXME_STUB'].save_struc
    save_struc.restype = None
    save_struc.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_char]
    save_tinfo = _libraries['FIXME_STUB'].save_tinfo
    save_tinfo.restype = tinfo_code_t
    save_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_til_t), size_t, ctypes.c_char_p, ctypes.c_int32]
    score_tinfo = _libraries['FIXME_STUB'].score_tinfo
    score_tinfo.restype = uint32
    score_tinfo.argtypes = [ctypes.POINTER(struct_tinfo_t)]
    search = _libraries['FIXME_STUB'].search
    search.restype = ctypes.c_int32
    search.argtypes = [ctypes.POINTER(None), ctypes.POINTER(struct_place_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, ctypes.c_int32]
    search_path = _libraries['FIXME_STUB'].search_path
    search_path.restype = ctypes.c_char
    search_path.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char]
    segm_adjust_diff = _libraries['FIXME_STUB'].segm_adjust_diff
    segm_adjust_diff.restype = adiff_t
    segm_adjust_diff.argtypes = [ctypes.POINTER(struct_segment_t), adiff_t]
    segm_adjust_ea = _libraries['FIXME_STUB'].segm_adjust_ea
    segm_adjust_ea.restype = ea_t
    segm_adjust_ea.argtypes = [ctypes.POINTER(struct_segment_t), ea_t]
    segtype = _libraries['FIXME_STUB'].segtype
    segtype.restype = uchar
    segtype.argtypes = [ea_t]
    sel2para = _libraries['FIXME_STUB'].sel2para
    sel2para.restype = ea_t
    sel2para.argtypes = [sel_t]
    select_extlang = _libraries['FIXME_STUB'].select_extlang
    select_extlang.restype = ctypes.c_char
    select_extlang.argtypes = [ctypes.POINTER(struct_extlang_t)]
    serialize_dynamic_register_set = _libraries['FIXME_STUB'].serialize_dynamic_register_set
    serialize_dynamic_register_set.restype = None
    serialize_dynamic_register_set.argtypes = [ctypes.POINTER(struct_bytevec_t), ctypes.POINTER(struct_dynamic_register_set_t)]
    serialize_json = _libraries['FIXME_STUB'].serialize_json
    serialize_json.restype = ctypes.c_char
    serialize_json.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(struct_jvalue_t), uint32]
    serialize_tinfo = _libraries['FIXME_STUB'].serialize_tinfo
    serialize_tinfo.restype = ctypes.c_char
    serialize_tinfo.argtypes = [ctypes.POINTER(qtype), ctypes.POINTER(qtype), ctypes.POINTER(qtype), ctypes.POINTER(struct_tinfo_t), ctypes.c_int32]
    set_abits = _libraries['FIXME_STUB'].set_abits
    set_abits.restype = None
    set_abits.argtypes = [ea_t, aflags_t]
    set_aflags = _libraries['FIXME_STUB'].set_aflags
    set_aflags.restype = None
    set_aflags.argtypes = [ea_t, aflags_t]
    set_array_parameters = _libraries['FIXME_STUB'].set_array_parameters
    set_array_parameters.restype = None
    set_array_parameters.argtypes = [ea_t, ctypes.POINTER(struct_array_parameters_t)]
    set_auto_state = _libraries['FIXME_STUB'].set_auto_state
    set_auto_state.restype = atype_t
    set_auto_state.argtypes = [atype_t]
    set_bmask_cmt = _libraries['FIXME_STUB'].set_bmask_cmt
    set_bmask_cmt.restype = ctypes.c_char
    set_bmask_cmt.argtypes = [enum_t, bmask_t, ctypes.c_char_p, ctypes.c_char]
    set_bmask_name = _libraries['FIXME_STUB'].set_bmask_name
    set_bmask_name.restype = ctypes.c_char
    set_bmask_name.argtypes = [enum_t, bmask_t, ctypes.c_char_p]
    set_cmt = _libraries['FIXME_STUB'].set_cmt
    set_cmt.restype = ctypes.c_char
    set_cmt.argtypes = [ea_t, ctypes.c_char_p, ctypes.c_char]
    set_compiler = _libraries['FIXME_STUB'].set_compiler
    set_compiler.restype = ctypes.c_char
    set_compiler.argtypes = [ctypes.POINTER(struct_compiler_info_t), ctypes.c_int32, ctypes.c_char_p]
    set_compiler_string = _libraries['FIXME_STUB'].set_compiler_string
    set_compiler_string.restype = ctypes.c_char
    set_compiler_string.argtypes = [ctypes.c_char_p, ctypes.c_char]
    set_cp_validity = _libraries['FIXME_STUB'].set_cp_validity
    set_cp_validity.restype = None
    set_cp_validity.argtypes = [ucdr_kind_t, wchar32_t, wchar32_t, ctypes.c_char]
    set_custom_data_type_ids = _libraries['FIXME_STUB'].set_custom_data_type_ids
    set_custom_data_type_ids.restype = None
    set_custom_data_type_ids.argtypes = [ea_t, ctypes.POINTER(struct_custom_data_type_ids_t)]
    set_database_flag = _libraries['FIXME_STUB'].set_database_flag
    set_database_flag.restype = None
    set_database_flag.argtypes = [uint32, ctypes.c_char]
    set_dbgmem_source = _libraries['FIXME_STUB'].set_dbgmem_source
    set_dbgmem_source.restype = None
    set_dbgmem_source.argtypes = [ctypes.CFUNCTYPE(ctypes.POINTER(struct_range_t), ctypes.POINTER(ctypes.c_int32)), ctypes.CFUNCTYPE(ctypes.c_int32, ea_t, ctypes.POINTER(None), ctypes.c_int32), ctypes.CFUNCTYPE(ctypes.c_int32, ea_t, ctypes.POINTER(None), ctypes.c_int32)]
    set_debug_event_code = _libraries['FIXME_STUB'].set_debug_event_code
    set_debug_event_code.restype = None
    set_debug_event_code.argtypes = [ctypes.POINTER(struct_debug_event_t), event_id_t]
    set_debug_name = _libraries['FIXME_STUB'].set_debug_name
    set_debug_name.restype = ctypes.c_char
    set_debug_name.argtypes = [ea_t, ctypes.c_char_p]
    set_debug_names = _libraries['FIXME_STUB'].set_debug_names
    set_debug_names.restype = ctypes.c_int32
    set_debug_names.argtypes = [ctypes.POINTER(ea_t), ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    set_default_dataseg = _libraries['FIXME_STUB'].set_default_dataseg
    set_default_dataseg.restype = None
    set_default_dataseg.argtypes = [sel_t]
    set_default_encoding_idx = _libraries['FIXME_STUB'].set_default_encoding_idx
    set_default_encoding_idx.restype = ctypes.c_char
    set_default_encoding_idx.argtypes = [ctypes.c_int32, ctypes.c_int32]
    set_default_sreg_value = _libraries['FIXME_STUB'].set_default_sreg_value
    set_default_sreg_value.restype = ctypes.c_char
    set_default_sreg_value.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_int32, sel_t]
    set_dummy_name = _libraries['FIXME_STUB'].set_dummy_name
    set_dummy_name.restype = ctypes.c_char
    set_dummy_name.argtypes = [ea_t, ea_t]
    set_entry_forwarder = _libraries['FIXME_STUB'].set_entry_forwarder
    set_entry_forwarder.restype = ctypes.c_char
    set_entry_forwarder.argtypes = [uval_t, ctypes.c_char_p, ctypes.c_int32]
    set_enum_bf = _libraries['FIXME_STUB'].set_enum_bf
    set_enum_bf.restype = ctypes.c_char
    set_enum_bf.argtypes = [enum_t, ctypes.c_char]
    set_enum_cmt = _libraries['FIXME_STUB'].set_enum_cmt
    set_enum_cmt.restype = ctypes.c_char
    set_enum_cmt.argtypes = [enum_t, ctypes.c_char_p, ctypes.c_char]
    set_enum_flag = _libraries['FIXME_STUB'].set_enum_flag
    set_enum_flag.restype = ctypes.c_char
    set_enum_flag.argtypes = [enum_t, flags_t]
    set_enum_fromtil = _libraries['FIXME_STUB'].set_enum_fromtil
    set_enum_fromtil.restype = ctypes.c_char
    set_enum_fromtil.argtypes = [enum_t, ctypes.c_char]
    set_enum_ghost = _libraries['FIXME_STUB'].set_enum_ghost
    set_enum_ghost.restype = ctypes.c_char
    set_enum_ghost.argtypes = [enum_t, ctypes.c_char]
    set_enum_hidden = _libraries['FIXME_STUB'].set_enum_hidden
    set_enum_hidden.restype = ctypes.c_char
    set_enum_hidden.argtypes = [enum_t, ctypes.c_char]
    set_enum_idx = _libraries['FIXME_STUB'].set_enum_idx
    set_enum_idx.restype = ctypes.c_char
    set_enum_idx.argtypes = [enum_t, size_t]
    set_enum_member_name = _libraries['FIXME_STUB'].set_enum_member_name
    set_enum_member_name.restype = ctypes.c_char
    set_enum_member_name.argtypes = [const_t, ctypes.c_char_p]
    set_enum_name = _libraries['FIXME_STUB'].set_enum_name
    set_enum_name.restype = ctypes.c_char
    set_enum_name.argtypes = [enum_t, ctypes.c_char_p]
    set_enum_type_ordinal = _libraries['FIXME_STUB'].set_enum_type_ordinal
    set_enum_type_ordinal.restype = None
    set_enum_type_ordinal.argtypes = [enum_t, int32]
    set_enum_width = _libraries['FIXME_STUB'].set_enum_width
    set_enum_width.restype = ctypes.c_char
    set_enum_width.argtypes = [enum_t, ctypes.c_int32]
    set_error_data = _libraries['FIXME_STUB'].set_error_data
    set_error_data.restype = None
    set_error_data.argtypes = [ctypes.c_int32, size_t]
    set_error_string = _libraries['FIXME_STUB'].set_error_string
    set_error_string.restype = None
    set_error_string.argtypes = [ctypes.c_int32, ctypes.c_char_p]
    set_file_ext = _libraries['FIXME_STUB'].set_file_ext
    set_file_ext.restype = ctypes.c_char_p
    set_file_ext.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p]
    set_fixup = _libraries['FIXME_STUB'].set_fixup
    set_fixup.restype = None
    set_fixup.argtypes = [ea_t, ctypes.POINTER(struct_fixup_data_t)]
    set_forced_operand = _libraries['FIXME_STUB'].set_forced_operand
    set_forced_operand.restype = ctypes.c_char
    set_forced_operand.argtypes = [ea_t, ctypes.c_int32, ctypes.c_char_p]
    set_frame_size = _libraries['FIXME_STUB'].set_frame_size
    set_frame_size.restype = ctypes.c_char
    set_frame_size.argtypes = [ctypes.POINTER(struct_func_t), asize_t, ushort, asize_t]
    set_func_cmt = _libraries['FIXME_STUB'].set_func_cmt
    set_func_cmt.restype = ctypes.c_char
    set_func_cmt.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char_p, ctypes.c_char]
    set_func_name_if_jumpfunc = _libraries['FIXME_STUB'].set_func_name_if_jumpfunc
    set_func_name_if_jumpfunc.restype = ctypes.c_int32
    set_func_name_if_jumpfunc.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char_p]
    set_group_selector = _libraries['FIXME_STUB'].set_group_selector
    set_group_selector.restype = ctypes.c_int32
    set_group_selector.argtypes = [sel_t, sel_t]
    set_header_path = _libraries['FIXME_STUB'].set_header_path
    set_header_path.restype = ctypes.c_char
    set_header_path.argtypes = [ctypes.c_char_p, ctypes.c_char]
    set_hexdsp = _libraries['FIXME_STUB'].set_hexdsp
    set_hexdsp.restype = None
    set_hexdsp.argtypes = [hexdsp_t]
    set_ida_state = _libraries['FIXME_STUB'].set_ida_state
    set_ida_state.restype = idastate_t
    set_ida_state.argtypes = [idastate_t]
    set_idc_dtor = _libraries['FIXME_STUB'].set_idc_dtor
    set_idc_dtor.restype = ctypes.c_char_p
    set_idc_dtor.argtypes = [ctypes.POINTER(struct_idc_class_t), ctypes.c_char_p]
    set_idc_getattr = _libraries['FIXME_STUB'].set_idc_getattr
    set_idc_getattr.restype = ctypes.c_char_p
    set_idc_getattr.argtypes = [ctypes.POINTER(struct_idc_class_t), ctypes.c_char_p]
    set_idc_method = _libraries['FIXME_STUB'].set_idc_method
    set_idc_method.restype = ctypes.c_char
    set_idc_method.argtypes = [ctypes.POINTER(struct_idc_class_t), ctypes.c_char_p]
    set_idc_setattr = _libraries['FIXME_STUB'].set_idc_setattr
    set_idc_setattr.restype = ctypes.c_char_p
    set_idc_setattr.argtypes = [ctypes.POINTER(struct_idc_class_t), ctypes.c_char_p]
    set_idcv_attr = _libraries['FIXME_STUB'].set_idcv_attr
    set_idcv_attr.restype = error_t
    set_idcv_attr.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p, ctypes.POINTER(struct_idc_value_t), ctypes.c_char]
    set_idcv_slice = _libraries['FIXME_STUB'].set_idcv_slice
    set_idcv_slice.restype = error_t
    set_idcv_slice.argtypes = [ctypes.POINTER(struct_idc_value_t), uval_t, uval_t, ctypes.POINTER(struct_idc_value_t), ctypes.c_int32]
    set_immd = _libraries['FIXME_STUB'].set_immd
    set_immd.restype = ctypes.c_char
    set_immd.argtypes = [ea_t]
    set_import_name = _libraries['FIXME_STUB'].set_import_name
    set_import_name.restype = None
    set_import_name.argtypes = [uval_t, ea_t, ctypes.c_char_p]
    set_import_ordinal = _libraries['FIXME_STUB'].set_import_ordinal
    set_import_ordinal.restype = None
    set_import_ordinal.argtypes = [uval_t, ea_t, uval_t]
    set_item_color = _libraries['FIXME_STUB'].set_item_color
    set_item_color.restype = None
    set_item_color.argtypes = [ea_t, bgcolor_t]
    set_lzero = _libraries['FIXME_STUB'].set_lzero
    set_lzero.restype = ctypes.c_char
    set_lzero.argtypes = [ea_t, ctypes.c_int32]
    set_manual_insn = _libraries['FIXME_STUB'].set_manual_insn
    set_manual_insn.restype = None
    set_manual_insn.argtypes = [ea_t, ctypes.c_char_p]
    set_member_cmt = _libraries['FIXME_STUB'].set_member_cmt
    set_member_cmt.restype = ctypes.c_char
    set_member_cmt.argtypes = [ctypes.POINTER(struct_member_t), ctypes.c_char_p, ctypes.c_char]
    set_member_name = _libraries['FIXME_STUB'].set_member_name
    set_member_name.restype = ctypes.c_char
    set_member_name.argtypes = [ctypes.POINTER(struct_struc_t), ea_t, ctypes.c_char_p]
    set_member_tinfo = _libraries['FIXME_STUB'].set_member_tinfo
    set_member_tinfo.restype = smt_code_t
    set_member_tinfo.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.POINTER(struct_member_t), uval_t, ctypes.POINTER(struct_tinfo_t), ctypes.c_int32]
    set_member_type = _libraries['FIXME_STUB'].set_member_type
    set_member_type.restype = ctypes.c_char
    set_member_type.argtypes = [ctypes.POINTER(struct_struc_t), ea_t, flags_t, ctypes.POINTER(union_opinfo_t), asize_t]
    set_module_data = _libraries['FIXME_STUB'].set_module_data
    set_module_data.restype = ctypes.POINTER(None)
    set_module_data.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(None)]
    set_moved_jpt = _libraries['FIXME_STUB'].set_moved_jpt
    set_moved_jpt.restype = ctypes.c_char
    set_moved_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.POINTER(struct_op_t), ctypes.POINTER(struct_op_t), ctypes.POINTER(tracked_regs_t), op_dtype_t, op_dtype_t]
    set_name = _libraries['FIXME_STUB'].set_name
    set_name.restype = ctypes.c_char
    set_name.argtypes = [ea_t, ctypes.c_char_p, ctypes.c_int32]
    set_node_info = _libraries['FIXME_STUB'].set_node_info
    set_node_info.restype = None
    set_node_info.argtypes = [graph_id_t, ctypes.c_int32, ctypes.POINTER(struct_node_info_t), uint32]
    set_noret_insn = _libraries['FIXME_STUB'].set_noret_insn
    set_noret_insn.restype = ctypes.c_char
    set_noret_insn.argtypes = [ea_t, ctypes.c_char]
    set_notcode = _libraries['FIXME_STUB'].set_notcode
    set_notcode.restype = None
    set_notcode.argtypes = [ea_t]
    set_numbered_type = _libraries['FIXME_STUB'].set_numbered_type
    set_numbered_type.restype = tinfo_code_t
    set_numbered_type.argtypes = [ctypes.POINTER(struct_til_t), uint32, ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(type_t), ctypes.POINTER(p_list), ctypes.c_char_p, ctypes.POINTER(p_list), ctypes.POINTER(sclass_t)]
    set_op_tinfo = _libraries['FIXME_STUB'].set_op_tinfo
    set_op_tinfo.restype = ctypes.c_char
    set_op_tinfo.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(struct_tinfo_t)]
    set_op_type = _libraries['FIXME_STUB'].set_op_type
    set_op_type.restype = ctypes.c_char
    set_op_type.argtypes = [ea_t, flags_t, ctypes.c_int32]
    set_opinfo = _libraries['FIXME_STUB'].set_opinfo
    set_opinfo.restype = ctypes.c_char
    set_opinfo.argtypes = [ea_t, ctypes.c_int32, flags_t, ctypes.POINTER(union_opinfo_t), ctypes.c_char]
    set_outfile_encoding_idx = _libraries['FIXME_STUB'].set_outfile_encoding_idx
    set_outfile_encoding_idx.restype = ctypes.c_char
    set_outfile_encoding_idx.argtypes = [ctypes.c_int32]
    set_path = _libraries['FIXME_STUB'].set_path
    set_path.restype = None
    set_path.argtypes = [path_type_t, ctypes.c_char_p]
    set_processor_type = _libraries['FIXME_STUB'].set_processor_type
    set_processor_type.restype = ctypes.c_char
    set_processor_type.argtypes = [ctypes.c_char_p, setproc_level_t]
    set_purged = _libraries['FIXME_STUB'].set_purged
    set_purged.restype = ctypes.c_char
    set_purged.argtypes = [ea_t, ctypes.c_int32, ctypes.c_char]
    set_qerrno = _libraries['FIXME_STUB'].set_qerrno
    set_qerrno.restype = error_t
    set_qerrno.argtypes = [error_t]
    set_refinfo = _libraries['FIXME_STUB'].set_refinfo
    set_refinfo.restype = ctypes.c_char
    set_refinfo.argtypes = [ea_t, ctypes.c_int32, reftype_t, ea_t, ea_t, adiff_t]
    set_refinfo_ex = _libraries['FIXME_STUB'].set_refinfo_ex
    set_refinfo_ex.restype = ctypes.c_char
    set_refinfo_ex.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(struct_refinfo_t)]
    set_regvar_cmt = _libraries['FIXME_STUB'].set_regvar_cmt
    set_regvar_cmt.restype = ctypes.c_int32
    set_regvar_cmt.argtypes = [ctypes.POINTER(struct_func_t), ctypes.POINTER(struct_regvar_t), ctypes.c_char_p]
    set_segm_addressing = _libraries['FIXME_STUB'].set_segm_addressing
    set_segm_addressing.restype = ctypes.c_char
    set_segm_addressing.argtypes = [ctypes.POINTER(struct_segment_t), size_t]
    set_segm_base = _libraries['FIXME_STUB'].set_segm_base
    set_segm_base.restype = ctypes.c_char
    set_segm_base.argtypes = [ctypes.POINTER(struct_segment_t), ea_t]
    set_segm_class = _libraries['FIXME_STUB'].set_segm_class
    set_segm_class.restype = ctypes.c_int32
    set_segm_class.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char_p, ctypes.c_int32]
    set_segm_end = _libraries['FIXME_STUB'].set_segm_end
    set_segm_end.restype = ctypes.c_char
    set_segm_end.argtypes = [ea_t, ea_t, ctypes.c_int32]
    set_segm_name = _libraries['FIXME_STUB'].set_segm_name
    set_segm_name.restype = ctypes.c_int32
    set_segm_name.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char_p, ctypes.c_int32]
    set_segm_start = _libraries['FIXME_STUB'].set_segm_start
    set_segm_start.restype = ctypes.c_char
    set_segm_start.argtypes = [ea_t, ea_t, ctypes.c_int32]
    set_segment_cmt = _libraries['FIXME_STUB'].set_segment_cmt
    set_segment_cmt.restype = None
    set_segment_cmt.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char_p, ctypes.c_char]
    set_segment_translations = _libraries['FIXME_STUB'].set_segment_translations
    set_segment_translations.restype = ctypes.c_char
    set_segment_translations.argtypes = [ea_t, ctypes.POINTER(eavec_t)]
    set_selector = _libraries['FIXME_STUB'].set_selector
    set_selector.restype = ctypes.c_int32
    set_selector.argtypes = [sel_t, ea_t]
    set_source_linnum = _libraries['FIXME_STUB'].set_source_linnum
    set_source_linnum.restype = None
    set_source_linnum.argtypes = [ea_t, uval_t]
    set_sreg_at_next_code = _libraries['FIXME_STUB'].set_sreg_at_next_code
    set_sreg_at_next_code.restype = None
    set_sreg_at_next_code.argtypes = [ea_t, ea_t, ctypes.c_int32, sel_t]
    set_str_type = _libraries['FIXME_STUB'].set_str_type
    set_str_type.restype = None
    set_str_type.argtypes = [ea_t, uint32]
    set_struc_align = _libraries['FIXME_STUB'].set_struc_align
    set_struc_align.restype = ctypes.c_char
    set_struc_align.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_int32]
    set_struc_cmt = _libraries['FIXME_STUB'].set_struc_cmt
    set_struc_cmt.restype = ctypes.c_char
    set_struc_cmt.argtypes = [tid_t, ctypes.c_char_p, ctypes.c_char]
    set_struc_hidden = _libraries['FIXME_STUB'].set_struc_hidden
    set_struc_hidden.restype = None
    set_struc_hidden.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_char]
    set_struc_idx = _libraries['FIXME_STUB'].set_struc_idx
    set_struc_idx.restype = ctypes.c_char
    set_struc_idx.argtypes = [ctypes.POINTER(struct_struc_t), uval_t]
    set_struc_listed = _libraries['FIXME_STUB'].set_struc_listed
    set_struc_listed.restype = None
    set_struc_listed.argtypes = [ctypes.POINTER(struct_struc_t), ctypes.c_char]
    set_struc_name = _libraries['FIXME_STUB'].set_struc_name
    set_struc_name.restype = ctypes.c_char
    set_struc_name.argtypes = [tid_t, ctypes.c_char_p]
    set_switch_info = _libraries['FIXME_STUB'].set_switch_info
    set_switch_info.restype = None
    set_switch_info.argtypes = [ea_t, ctypes.POINTER(struct_switch_info_t)]
    set_tail_owner = _libraries['FIXME_STUB'].set_tail_owner
    set_tail_owner.restype = ctypes.c_char
    set_tail_owner.argtypes = [ctypes.POINTER(struct_func_t), ea_t]
    set_target_assembler = _libraries['FIXME_STUB'].set_target_assembler
    set_target_assembler.restype = ctypes.c_char
    set_target_assembler.argtypes = [ctypes.c_int32]
    set_tinfo = _libraries['FIXME_STUB'].set_tinfo
    set_tinfo.restype = ctypes.c_char
    set_tinfo.argtypes = [ea_t, ctypes.POINTER(struct_tinfo_t)]
    set_tinfo_attr = _libraries['FIXME_STUB'].set_tinfo_attr
    set_tinfo_attr.restype = ctypes.c_char
    set_tinfo_attr.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_type_attr_t), ctypes.c_char]
    set_tinfo_attrs = _libraries['FIXME_STUB'].set_tinfo_attrs
    set_tinfo_attrs.restype = ctypes.c_char
    set_tinfo_attrs.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(type_attrs_t)]
    set_tinfo_property = _libraries['FIXME_STUB'].set_tinfo_property
    set_tinfo_property.restype = size_t
    set_tinfo_property.argtypes = [ctypes.POINTER(struct_tinfo_t), ctypes.c_int32, size_t]
    set_type_alias = _libraries['FIXME_STUB'].set_type_alias
    set_type_alias.restype = ctypes.c_char
    set_type_alias.argtypes = [ctypes.POINTER(struct_til_t), uint32, uint32]
    set_user_defined_prefix = _libraries['FIXME_STUB'].set_user_defined_prefix
    set_user_defined_prefix.restype = None
    set_user_defined_prefix.argtypes = [size_t, ctypes.CFUNCTYPE(None, ctypes.POINTER(qstring), ea_t, ctypes.c_int32, ctypes.c_int32, ctypes.c_char_p)]
    set_vftable_ea = _libraries['FIXME_STUB'].set_vftable_ea
    set_vftable_ea.restype = ctypes.c_char
    set_vftable_ea.argtypes = [uint32, ea_t]
    set_visible_func = _libraries['FIXME_STUB'].set_visible_func
    set_visible_func.restype = None
    set_visible_func.argtypes = [ctypes.POINTER(struct_func_t), ctypes.c_char]
    set_visible_segm = _libraries['FIXME_STUB'].set_visible_segm
    set_visible_segm.restype = None
    set_visible_segm.argtypes = [ctypes.POINTER(struct_segment_t), ctypes.c_char]
    set_xrefpos = _libraries['FIXME_STUB'].set_xrefpos
    set_xrefpos.restype = None
    set_xrefpos.argtypes = [ea_t, ctypes.POINTER(struct_xrefpos_t)]
    setinf = _libraries['FIXME_STUB'].setinf
    setinf.restype = ctypes.c_char
    setinf.argtypes = [inftag_t, ssize_t]
    setinf_buf = _libraries['FIXME_STUB'].setinf_buf
    setinf_buf.restype = ctypes.c_char
    setinf_buf.argtypes = [inftag_t, ctypes.POINTER(None), size_t]
    setinf_flag = _libraries['FIXME_STUB'].setinf_flag
    setinf_flag.restype = ctypes.c_char
    setinf_flag.argtypes = [inftag_t, uint32, ctypes.c_char]
    setup_graph_subsystem = _libraries['FIXME_STUB'].setup_graph_subsystem
    setup_graph_subsystem.restype = None
    setup_graph_subsystem.argtypes = [ctypes.c_char_p, ctypes.CFUNCTYPE(bgcolor_t, ctypes.c_int32)]
    setup_lowcnd_regfuncs = _libraries['FIXME_STUB'].setup_lowcnd_regfuncs
    setup_lowcnd_regfuncs.restype = None
    setup_lowcnd_regfuncs.argtypes = [ctypes.CFUNCTYPE(error_t, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)), ctypes.CFUNCTYPE(error_t, ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t))]
    setup_selector = _libraries['FIXME_STUB'].setup_selector
    setup_selector.restype = sel_t
    setup_selector.argtypes = [ea_t]
    show_auto = _libraries['FIXME_STUB'].show_auto
    show_auto.restype = None
    show_auto.argtypes = [ea_t, atype_t]
    show_name = _libraries['FIXME_STUB'].show_name
    show_name.restype = None
    show_name.argtypes = [ea_t]
    simpleline_place_t__adjust = _libraries['FIXME_STUB'].simpleline_place_t__adjust
    simpleline_place_t__adjust.restype = None
    simpleline_place_t__adjust.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    simpleline_place_t__beginning = _libraries['FIXME_STUB'].simpleline_place_t__beginning
    simpleline_place_t__beginning.restype = ctypes.c_char
    simpleline_place_t__beginning.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    simpleline_place_t__clone = _libraries['FIXME_STUB'].simpleline_place_t__clone
    simpleline_place_t__clone.restype = ctypes.POINTER(struct_place_t)
    simpleline_place_t__clone.argtypes = [ctypes.POINTER(struct_simpleline_place_t)]
    simpleline_place_t__compare = _libraries['FIXME_STUB'].simpleline_place_t__compare
    simpleline_place_t__compare.restype = ctypes.c_int32
    simpleline_place_t__compare.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(struct_place_t)]
    simpleline_place_t__compare2 = _libraries['FIXME_STUB'].simpleline_place_t__compare2
    simpleline_place_t__compare2.restype = ctypes.c_int32
    simpleline_place_t__compare2.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    simpleline_place_t__copyfrom = _libraries['FIXME_STUB'].simpleline_place_t__copyfrom
    simpleline_place_t__copyfrom.restype = None
    simpleline_place_t__copyfrom.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(struct_place_t)]
    simpleline_place_t__deserialize = _libraries['FIXME_STUB'].simpleline_place_t__deserialize
    simpleline_place_t__deserialize.restype = ctypes.c_char
    simpleline_place_t__deserialize.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    simpleline_place_t__ending = _libraries['FIXME_STUB'].simpleline_place_t__ending
    simpleline_place_t__ending.restype = ctypes.c_char
    simpleline_place_t__ending.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    simpleline_place_t__enter = _libraries['FIXME_STUB'].simpleline_place_t__enter
    simpleline_place_t__enter.restype = ctypes.POINTER(struct_place_t)
    simpleline_place_t__enter.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(uint32)]
    simpleline_place_t__generate = _libraries['FIXME_STUB'].simpleline_place_t__generate
    simpleline_place_t__generate.restype = ctypes.c_int32
    simpleline_place_t__generate.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(color_t), ctypes.POINTER(bgcolor_t), ctypes.POINTER(None), ctypes.c_int32]
    simpleline_place_t__id = _libraries['FIXME_STUB'].simpleline_place_t__id
    simpleline_place_t__id.restype = ctypes.c_int32
    simpleline_place_t__id.argtypes = [ctypes.POINTER(struct_simpleline_place_t)]
    simpleline_place_t__leave = _libraries['FIXME_STUB'].simpleline_place_t__leave
    simpleline_place_t__leave.restype = None
    simpleline_place_t__leave.argtypes = [ctypes.POINTER(struct_simpleline_place_t), uint32]
    simpleline_place_t__makeplace = _libraries['FIXME_STUB'].simpleline_place_t__makeplace
    simpleline_place_t__makeplace.restype = ctypes.POINTER(struct_place_t)
    simpleline_place_t__makeplace.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None), uval_t, ctypes.c_int32]
    simpleline_place_t__name = _libraries['FIXME_STUB'].simpleline_place_t__name
    simpleline_place_t__name.restype = ctypes.c_char_p
    simpleline_place_t__name.argtypes = [ctypes.POINTER(struct_simpleline_place_t)]
    simpleline_place_t__next = _libraries['FIXME_STUB'].simpleline_place_t__next
    simpleline_place_t__next.restype = ctypes.c_char
    simpleline_place_t__next.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    simpleline_place_t__prev = _libraries['FIXME_STUB'].simpleline_place_t__prev
    simpleline_place_t__prev.restype = ctypes.c_char
    simpleline_place_t__prev.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    simpleline_place_t__print = _libraries['FIXME_STUB'].simpleline_place_t__print
    simpleline_place_t__print.restype = None
    simpleline_place_t__print.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(qstring), ctypes.POINTER(None)]
    simpleline_place_t__rebase = _libraries['FIXME_STUB'].simpleline_place_t__rebase
    simpleline_place_t__rebase.restype = ctypes.c_char
    simpleline_place_t__rebase.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(struct_segm_move_infos_t)]
    simpleline_place_t__serialize = _libraries['FIXME_STUB'].simpleline_place_t__serialize
    simpleline_place_t__serialize.restype = None
    simpleline_place_t__serialize.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(struct_bytevec_t)]
    simpleline_place_t__toea = _libraries['FIXME_STUB'].simpleline_place_t__toea
    simpleline_place_t__toea.restype = ea_t
    simpleline_place_t__toea.argtypes = [ctypes.POINTER(struct_simpleline_place_t)]
    simpleline_place_t__touval = _libraries['FIXME_STUB'].simpleline_place_t__touval
    simpleline_place_t__touval.restype = uval_t
    simpleline_place_t__touval.argtypes = [ctypes.POINTER(struct_simpleline_place_t), ctypes.POINTER(None)]
    skip_spaces = _libraries['FIXME_STUB'].skip_spaces
    skip_spaces.restype = ctypes.c_char_p
    skip_spaces.argtypes = [ctypes.c_char_p]
    skip_utf8 = _libraries['FIXME_STUB'].skip_utf8
    skip_utf8.restype = size_t
    skip_utf8.argtypes = [ctypes.POINTER(ctypes.c_char_p), size_t]
    sort_til = _libraries['FIXME_STUB'].sort_til
    sort_til.restype = ctypes.c_char
    sort_til.argtypes = [ctypes.POINTER(struct_til_t)]
    split_sreg_range = _libraries['FIXME_STUB'].split_sreg_range
    split_sreg_range.restype = ctypes.c_char
    split_sreg_range.argtypes = [ea_t, ctypes.c_int32, sel_t, uchar, ctypes.c_char]
    std_out_segm_footer = _libraries['FIXME_STUB'].std_out_segm_footer
    std_out_segm_footer.restype = None
    std_out_segm_footer.argtypes = [ctypes.POINTER(struct_outctx_t), ctypes.POINTER(struct_segment_t)]
    stoa = _libraries['FIXME_STUB'].stoa
    stoa.restype = size_t
    stoa.argtypes = [ctypes.POINTER(qstring), ea_t, sel_t]
    store_til = _libraries['FIXME_STUB'].store_til
    store_til.restype = ctypes.c_char
    store_til.argtypes = [ctypes.POINTER(struct_til_t), ctypes.c_char_p, ctypes.c_char_p]
    str2ea = _libraries['FIXME_STUB'].str2ea
    str2ea.restype = ctypes.c_char
    str2ea.argtypes = [ctypes.POINTER(ea_t), ctypes.c_char_p, ea_t]
    str2ea_ex = _libraries['FIXME_STUB'].str2ea_ex
    str2ea_ex.restype = ctypes.c_char
    str2ea_ex.argtypes = [ctypes.POINTER(ea_t), ctypes.c_char_p, ea_t, ctypes.c_int32]
    str2reg = _libraries['FIXME_STUB'].str2reg
    str2reg.restype = ctypes.c_int32
    str2reg.argtypes = [ctypes.c_char_p]
    str2user = _libraries['FIXME_STUB'].str2user
    str2user.restype = ctypes.c_char_p
    str2user.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strarray = _libraries['FIXME_STUB'].strarray
    strarray.restype = ctypes.c_char_p
    strarray.argtypes = [ctypes.POINTER(struct_strarray_t), size_t, ctypes.c_int32]
    stristr = _libraries['FIXME_STUB'].stristr
    stristr.restype = ctypes.c_char_p
    stristr.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strrpl = _libraries['FIXME_STUB'].strrpl
    strrpl.restype = ctypes.c_char_p
    strrpl.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    structplace_t__adjust = _libraries['FIXME_STUB'].structplace_t__adjust
    structplace_t__adjust.restype = None
    structplace_t__adjust.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    structplace_t__beginning = _libraries['FIXME_STUB'].structplace_t__beginning
    structplace_t__beginning.restype = ctypes.c_char
    structplace_t__beginning.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    structplace_t__clone = _libraries['FIXME_STUB'].structplace_t__clone
    structplace_t__clone.restype = ctypes.POINTER(struct_place_t)
    structplace_t__clone.argtypes = [ctypes.POINTER(struct_structplace_t)]
    structplace_t__compare = _libraries['FIXME_STUB'].structplace_t__compare
    structplace_t__compare.restype = ctypes.c_int32
    structplace_t__compare.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(struct_place_t)]
    structplace_t__compare2 = _libraries['FIXME_STUB'].structplace_t__compare2
    structplace_t__compare2.restype = ctypes.c_int32
    structplace_t__compare2.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(struct_place_t), ctypes.POINTER(None)]
    structplace_t__copyfrom = _libraries['FIXME_STUB'].structplace_t__copyfrom
    structplace_t__copyfrom.restype = None
    structplace_t__copyfrom.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(struct_place_t)]
    structplace_t__deserialize = _libraries['FIXME_STUB'].structplace_t__deserialize
    structplace_t__deserialize.restype = ctypes.c_char
    structplace_t__deserialize.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    structplace_t__ending = _libraries['FIXME_STUB'].structplace_t__ending
    structplace_t__ending.restype = ctypes.c_char
    structplace_t__ending.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    structplace_t__enter = _libraries['FIXME_STUB'].structplace_t__enter
    structplace_t__enter.restype = ctypes.POINTER(struct_place_t)
    structplace_t__enter.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(uint32)]
    structplace_t__generate = _libraries['FIXME_STUB'].structplace_t__generate
    structplace_t__generate.restype = ctypes.c_int32
    structplace_t__generate.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(qstrvec_t), ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(color_t), ctypes.POINTER(bgcolor_t), ctypes.POINTER(None), ctypes.c_int32]
    structplace_t__id = _libraries['FIXME_STUB'].structplace_t__id
    structplace_t__id.restype = ctypes.c_int32
    structplace_t__id.argtypes = [ctypes.POINTER(struct_structplace_t)]
    structplace_t__leave = _libraries['FIXME_STUB'].structplace_t__leave
    structplace_t__leave.restype = None
    structplace_t__leave.argtypes = [ctypes.POINTER(struct_structplace_t), uint32]
    structplace_t__makeplace = _libraries['FIXME_STUB'].structplace_t__makeplace
    structplace_t__makeplace.restype = ctypes.POINTER(struct_place_t)
    structplace_t__makeplace.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None), uval_t, ctypes.c_int32]
    structplace_t__name = _libraries['FIXME_STUB'].structplace_t__name
    structplace_t__name.restype = ctypes.c_char_p
    structplace_t__name.argtypes = [ctypes.POINTER(struct_structplace_t)]
    structplace_t__next = _libraries['FIXME_STUB'].structplace_t__next
    structplace_t__next.restype = ctypes.c_char
    structplace_t__next.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    structplace_t__prev = _libraries['FIXME_STUB'].structplace_t__prev
    structplace_t__prev.restype = ctypes.c_char
    structplace_t__prev.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    structplace_t__print = _libraries['FIXME_STUB'].structplace_t__print
    structplace_t__print.restype = None
    structplace_t__print.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(qstring), ctypes.POINTER(None)]
    structplace_t__rebase = _libraries['FIXME_STUB'].structplace_t__rebase
    structplace_t__rebase.restype = ctypes.c_char
    structplace_t__rebase.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(struct_segm_move_infos_t)]
    structplace_t__serialize = _libraries['FIXME_STUB'].structplace_t__serialize
    structplace_t__serialize.restype = None
    structplace_t__serialize.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(struct_bytevec_t)]
    structplace_t__toea = _libraries['FIXME_STUB'].structplace_t__toea
    structplace_t__toea.restype = ea_t
    structplace_t__toea.argtypes = [ctypes.POINTER(struct_structplace_t)]
    structplace_t__touval = _libraries['FIXME_STUB'].structplace_t__touval
    structplace_t__touval.restype = uval_t
    structplace_t__touval.argtypes = [ctypes.POINTER(struct_structplace_t), ctypes.POINTER(None)]
    swap128 = _libraries['FIXME_STUB'].swap128
    swap128.restype = None
    swap128.argtypes = [ctypes.POINTER(struct_uint128)]
    swap64 = _libraries['FIXME_STUB'].swap64
    swap64.restype = ulonglong
    swap64.argtypes = [ulonglong]
    swap_idcvs = _libraries['FIXME_STUB'].swap_idcvs
    swap_idcvs.restype = None
    swap_idcvs.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_idc_value_t)]
    swap_value = _libraries['FIXME_STUB'].swap_value
    swap_value.restype = None
    swap_value.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_int32]
    switch_dbctx = _libraries['FIXME_STUB'].switch_dbctx
    switch_dbctx.restype = ctypes.POINTER(struct_dbctx_t)
    switch_dbctx.argtypes = [size_t]
    tag_addr = _libraries['FIXME_STUB'].tag_addr
    tag_addr.restype = None
    tag_addr.argtypes = [ctypes.POINTER(qstring), ea_t, ctypes.c_char]
    tag_advance = _libraries['FIXME_STUB'].tag_advance
    tag_advance.restype = ctypes.c_char_p
    tag_advance.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    tag_remove = _libraries['FIXME_STUB'].tag_remove
    tag_remove.restype = ssize_t
    tag_remove.argtypes = [ctypes.POINTER(qstring), ctypes.c_char_p, ctypes.c_int32]
    tag_skipcode = _libraries['FIXME_STUB'].tag_skipcode
    tag_skipcode.restype = ctypes.c_char_p
    tag_skipcode.argtypes = [ctypes.c_char_p]
    tag_skipcodes = _libraries['FIXME_STUB'].tag_skipcodes
    tag_skipcodes.restype = ctypes.c_char_p
    tag_skipcodes.argtypes = [ctypes.c_char_p]
    tag_strlen = _libraries['FIXME_STUB'].tag_strlen
    tag_strlen.restype = ssize_t
    tag_strlen.argtypes = [ctypes.c_char_p]
    take_memory_snapshot = _libraries['FIXME_STUB'].take_memory_snapshot
    take_memory_snapshot.restype = ctypes.c_char
    take_memory_snapshot.argtypes = [ctypes.c_char]
    term_database = _libraries['FIXME_STUB'].term_database
    term_database.restype = None
    term_database.argtypes = []
    term_plugins = _libraries['FIXME_STUB'].term_plugins
    term_plugins.restype = None
    term_plugins.argtypes = [ctypes.c_int32]
    term_process = _libraries['FIXME_STUB'].term_process
    term_process.restype = ctypes.c_int32
    term_process.argtypes = [ctypes.POINTER(None)]
    throw_idc_exception = _libraries['FIXME_STUB'].throw_idc_exception
    throw_idc_exception.restype = error_t
    throw_idc_exception.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.c_char_p]
    toggle_bnot = _libraries['FIXME_STUB'].toggle_bnot
    toggle_bnot.restype = ctypes.c_char
    toggle_bnot.argtypes = [ea_t, ctypes.c_int32]
    toggle_sign = _libraries['FIXME_STUB'].toggle_sign
    toggle_sign.restype = ctypes.c_char
    toggle_sign.argtypes = [ea_t, ctypes.c_int32]
    track_value_until_address_jpt = _libraries['FIXME_STUB'].track_value_until_address_jpt
    track_value_until_address_jpt.restype = ctypes.c_char
    track_value_until_address_jpt.argtypes = [ctypes.POINTER(struct_jump_pattern_t), ctypes.POINTER(struct_op_t), ea_t]
    trim = _libraries['FIXME_STUB'].trim
    trim.restype = ctypes.c_char_p
    trim.argtypes = [ctypes.c_char_p]
    trim_jtable = _libraries['FIXME_STUB'].trim_jtable
    trim_jtable.restype = None
    trim_jtable.argtypes = [ctypes.POINTER(struct_switch_info_t), ea_t, ctypes.c_char]
    try_to_add_libfunc = _libraries['FIXME_STUB'].try_to_add_libfunc
    try_to_add_libfunc.restype = ctypes.c_int32
    try_to_add_libfunc.argtypes = [ea_t]
    under_debugger = ctypes_in_dll(ctypes.c_char, _libraries['FIXME_STUB'], 'under_debugger')
    unhook_event_listener = _libraries['FIXME_STUB'].unhook_event_listener
    unhook_event_listener.restype = ctypes.c_char
    unhook_event_listener.argtypes = [hook_type_t, ctypes.POINTER(struct_event_listener_t)]
    unhook_from_notification_point = _libraries['FIXME_STUB'].unhook_from_notification_point
    unhook_from_notification_point.restype = ctypes.c_int32
    unhook_from_notification_point.argtypes = [hook_type_t, ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.c_int32, va_list), ctypes.POINTER(None)]
    unlock_dbgmem_config = _libraries['FIXME_STUB'].unlock_dbgmem_config
    unlock_dbgmem_config.restype = None
    unlock_dbgmem_config.argtypes = []
    unmake_linput = _libraries['FIXME_STUB'].unmake_linput
    unmake_linput.restype = None
    unmake_linput.argtypes = [ctypes.POINTER(struct_linput_t)]
    unpack_dd = _libraries['FIXME_STUB'].unpack_dd
    unpack_dd.restype = uint32
    unpack_dd.argtypes = [ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    unpack_dq = _libraries['FIXME_STUB'].unpack_dq
    unpack_dq.restype = uint64
    unpack_dq.argtypes = [ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    unpack_ds = _libraries['FIXME_STUB'].unpack_ds
    unpack_ds.restype = ctypes.c_char_p
    unpack_ds.argtypes = [ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar), ctypes.c_char]
    unpack_dw = _libraries['FIXME_STUB'].unpack_dw
    unpack_dw.restype = ushort
    unpack_dw.argtypes = [ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    unpack_idcobj_from_bv = _libraries['FIXME_STUB'].unpack_idcobj_from_bv
    unpack_idcobj_from_bv.restype = error_t
    unpack_idcobj_from_bv.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ctypes.POINTER(struct_bytevec_t), ctypes.c_int32]
    unpack_idcobj_from_idb = _libraries['FIXME_STUB'].unpack_idcobj_from_idb
    unpack_idcobj_from_idb.restype = error_t
    unpack_idcobj_from_idb.argtypes = [ctypes.POINTER(struct_idc_value_t), ctypes.POINTER(struct_tinfo_t), ea_t, ctypes.POINTER(struct_bytevec_t), ctypes.c_int32]
    unpack_memory = _libraries['FIXME_STUB'].unpack_memory
    unpack_memory.restype = ctypes.c_char
    unpack_memory.argtypes = [ctypes.POINTER(None), size_t, ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    unpack_xleb128 = _libraries['FIXME_STUB'].unpack_xleb128
    unpack_xleb128.restype = ctypes.c_char
    unpack_xleb128.argtypes = [ctypes.POINTER(None), ctypes.c_int32, ctypes.c_char, ctypes.POINTER(ctypes.POINTER(uchar)), ctypes.POINTER(uchar)]
    unregister_custom_data_format = _libraries['FIXME_STUB'].unregister_custom_data_format
    unregister_custom_data_format.restype = ctypes.c_char
    unregister_custom_data_format.argtypes = [ctypes.c_int32]
    unregister_custom_data_type = _libraries['FIXME_STUB'].unregister_custom_data_type
    unregister_custom_data_type.restype = ctypes.c_char
    unregister_custom_data_type.argtypes = [ctypes.c_int32]
    unregister_custom_fixup = _libraries['FIXME_STUB'].unregister_custom_fixup
    unregister_custom_fixup.restype = ctypes.c_char
    unregister_custom_fixup.argtypes = [fixup_type_t]
    unregister_custom_refinfo = _libraries['FIXME_STUB'].unregister_custom_refinfo
    unregister_custom_refinfo.restype = ctypes.c_char
    unregister_custom_refinfo.argtypes = [ctypes.c_int32]
    unregister_post_event_visitor = _libraries['FIXME_STUB'].unregister_post_event_visitor
    unregister_post_event_visitor.restype = ctypes.c_char
    unregister_post_event_visitor.argtypes = [hook_type_t, ctypes.POINTER(struct_post_event_visitor_t)]
    upd_abits = _libraries['FIXME_STUB'].upd_abits
    upd_abits.restype = None
    upd_abits.argtypes = [ea_t, aflags_t, aflags_t]
    update_extra_cmt = _libraries['FIXME_STUB'].update_extra_cmt
    update_extra_cmt.restype = None
    update_extra_cmt.argtypes = [ea_t, ctypes.c_int32, ctypes.c_char_p]
    update_fpd = _libraries['FIXME_STUB'].update_fpd
    update_fpd.restype = ctypes.c_char
    update_fpd.argtypes = [ctypes.POINTER(struct_func_t), asize_t]
    update_func = _libraries['FIXME_STUB'].update_func
    update_func.restype = ctypes.c_char
    update_func.argtypes = [ctypes.POINTER(struct_func_t)]
    update_hidden_range = _libraries['FIXME_STUB'].update_hidden_range
    update_hidden_range.restype = ctypes.c_char
    update_hidden_range.argtypes = [ctypes.POINTER(struct_hidden_range_t)]
    update_segm = _libraries['FIXME_STUB'].update_segm
    update_segm.restype = ctypes.c_char
    update_segm.argtypes = [ctypes.POINTER(struct_segment_t)]
    update_snapshot_attributes = _libraries['FIXME_STUB'].update_snapshot_attributes
    update_snapshot_attributes.restype = ctypes.c_char
    update_snapshot_attributes.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct_snapshot_t), ctypes.POINTER(struct_snapshot_t), ctypes.c_int32]
    use_mapping = _libraries['FIXME_STUB'].use_mapping
    use_mapping.restype = ea_t
    use_mapping.argtypes = [ea_t]
    user2bin = _libraries['FIXME_STUB'].user2bin
    user2bin.restype = ctypes.c_int32
    user2bin.argtypes = [ctypes.POINTER(uchar), ctypes.POINTER(uchar), ea_t, ctypes.c_char_p, ctypes.c_int32, ctypes.c_char]
    user2qstr = _libraries['FIXME_STUB'].user2qstr
    user2qstr.restype = None
    user2qstr.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(qstring)]
    user2str = _libraries['FIXME_STUB'].user2str
    user2str.restype = ctypes.c_char_p
    user2str.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    utf16_utf8 = _libraries['FIXME_STUB'].utf16_utf8
    utf16_utf8.restype = ctypes.c_char
    utf16_utf8.argtypes = [ctypes.POINTER(qstring), ctypes.POINTER(wchar16_t), ctypes.c_int32]
    utf8_utf16 = _libraries['FIXME_STUB'].utf8_utf16
    utf8_utf16.restype = ctypes.c_char
    utf8_utf16.argtypes = [ctypes.POINTER(qwstring), ctypes.c_char_p, ctypes.c_int32]
    vadd_extra_line = _libraries['FIXME_STUB'].vadd_extra_line
    vadd_extra_line.restype = ctypes.c_char
    vadd_extra_line.argtypes = [ea_t, ctypes.c_int32, ctypes.c_char_p, va_list]
    validate_idb_names = _libraries['FIXME_STUB'].validate_idb_names
    validate_idb_names.restype = ctypes.c_int32
    validate_idb_names.argtypes = []
    validate_idb_names2 = _libraries['FIXME_STUB'].validate_idb_names2
    validate_idb_names2.restype = ctypes.c_int32
    validate_idb_names2.argtypes = [ctypes.c_char]
    validate_name = _libraries['FIXME_STUB'].validate_name
    validate_name.restype = ctypes.c_char
    validate_name.argtypes = [ctypes.POINTER(qstring), nametype_t, ctypes.c_int32]
    verify_argloc = _libraries['FIXME_STUB'].verify_argloc
    verify_argloc.restype = ctypes.c_int32
    verify_argloc.argtypes = [ctypes.POINTER(struct_argloc_t), ctypes.c_int32, ctypes.POINTER(struct_rangeset_t)]
    verify_tinfo = _libraries['FIXME_STUB'].verify_tinfo
    verify_tinfo.restype = ctypes.c_int32
    verify_tinfo.argtypes = [uint32]
    verror = _libraries['FIXME_STUB'].verror
    verror.restype = None
    verror.argtypes = [ctypes.c_char_p, va_list]
    visit_patched_bytes = _libraries['FIXME_STUB'].visit_patched_bytes
    visit_patched_bytes.restype = ctypes.c_int32
    visit_patched_bytes.argtypes = [ea_t, ea_t, ctypes.CFUNCTYPE(ctypes.c_int32, ea_t, int64, uint64, uint64, ctypes.POINTER(None)), ctypes.POINTER(None)]
    visit_snapshot_tree = _libraries['FIXME_STUB'].visit_snapshot_tree
    visit_snapshot_tree.restype = ctypes.c_int32
    visit_snapshot_tree.argtypes = [ctypes.POINTER(struct_snapshot_t), ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(struct_snapshot_t), ctypes.POINTER(None)), ctypes.POINTER(None)]
    visit_stroff_fields = _libraries['FIXME_STUB'].visit_stroff_fields
    visit_stroff_fields.restype = flags_t
    visit_stroff_fields.argtypes = [ctypes.POINTER(struct_struct_field_visitor_t), ctypes.POINTER(tid_t), ctypes.c_int32, ctypes.POINTER(adiff_t), ctypes.c_char]
    visit_subtypes = _libraries['FIXME_STUB'].visit_subtypes
    visit_subtypes.restype = ctypes.c_int32
    visit_subtypes.argtypes = [ctypes.POINTER(struct_tinfo_visitor_t), ctypes.POINTER(struct_type_mods_t), ctypes.POINTER(struct_tinfo_t), ctypes.c_char_p, ctypes.c_char_p]
    vloader_failure = _libraries['FIXME_STUB'].vloader_failure
    vloader_failure.restype = None
    vloader_failure.argtypes = [ctypes.c_char_p, va_list]
    vqmakepath = _libraries['FIXME_STUB'].vqmakepath
    vqmakepath.restype = ctypes.c_char_p
    vqmakepath.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    vqperror = _libraries['FIXME_STUB'].vqperror
    vqperror.restype = None
    vqperror.argtypes = [ctypes.c_char_p, va_list]
    vshow_hex = _libraries['FIXME_STUB'].vshow_hex
    vshow_hex.restype = None
    vshow_hex.argtypes = [ctypes.POINTER(None), size_t, ctypes.c_char_p, va_list]
    vshow_hex_file = _libraries['FIXME_STUB'].vshow_hex_file
    vshow_hex_file.restype = None
    vshow_hex_file.argtypes = [ctypes.POINTER(struct_linput_t), int64, size_t, ctypes.c_char_p, va_list]
    winerr = _libraries['FIXME_STUB'].winerr
    winerr.restype = ctypes.c_char_p
    winerr.argtypes = [ctypes.c_int32]
    write_struc_path = _libraries['FIXME_STUB'].write_struc_path
    write_struc_path.restype = None
    write_struc_path.argtypes = [ea_t, ctypes.c_int32, ctypes.POINTER(tid_t), ctypes.c_int32, adiff_t]
    write_tinfo_bitfield_value = _libraries['FIXME_STUB'].write_tinfo_bitfield_value
    write_tinfo_bitfield_value.restype = uint64
    write_tinfo_bitfield_value.argtypes = [uint32, uint64, uint64, ctypes.c_int32]
    writebytes = _libraries['FIXME_STUB'].writebytes
    writebytes.restype = ctypes.c_int32
    writebytes.argtypes = [ctypes.c_int32, uint32, ctypes.c_int32, ctypes.c_char]
    xrefblk_t_first_from = _libraries['FIXME_STUB'].xrefblk_t_first_from
    xrefblk_t_first_from.restype = ctypes.c_char
    xrefblk_t_first_from.argtypes = [ctypes.POINTER(struct_xrefblk_t), ea_t, ctypes.c_int32]
    xrefblk_t_first_to = _libraries['FIXME_STUB'].xrefblk_t_first_to
    xrefblk_t_first_to.restype = ctypes.c_char
    xrefblk_t_first_to.argtypes = [ctypes.POINTER(struct_xrefblk_t), ea_t, ctypes.c_int32]
    xrefblk_t_next_from = _libraries['FIXME_STUB'].xrefblk_t_next_from
    xrefblk_t_next_from.restype = ctypes.c_char
    xrefblk_t_next_from.argtypes = [ctypes.POINTER(struct_xrefblk_t)]
    xrefblk_t_next_to = _libraries['FIXME_STUB'].xrefblk_t_next_to
    xrefblk_t_next_to.restype = ctypes.c_char
    xrefblk_t_next_to.argtypes = [ctypes.POINTER(struct_xrefblk_t)]
    xrefchar = _libraries['FIXME_STUB'].xrefchar
    xrefchar.restype = ctypes.c_char
    xrefchar.argtypes = [ctypes.c_char]
    zip_deflate = _libraries['FIXME_STUB'].zip_deflate
    zip_deflate.restype = ctypes.c_int32
    zip_deflate.argtypes = [ctypes.POINTER(None), ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.POINTER(None), size_t), ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.POINTER(None), size_t)]
    zip_inflate = _libraries['FIXME_STUB'].zip_inflate
    zip_inflate.restype = ctypes.c_int32
    zip_inflate.argtypes = [ctypes.POINTER(None), ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.POINTER(None), size_t), ctypes.CFUNCTYPE(ssize_t, ctypes.POINTER(None), ctypes.POINTER(None), size_t)]
    __all__ = \
        ['AA_CHECKABLE', 'AA_CHECKED', 'AA_ICON', 'AA_LABEL', 'AA_NONE',
        'AA_SHORTCUT', 'AA_STATE', 'AA_TOOLTIP', 'AA_VISIBILITY',
        'ALL_CHANGED', 'ARGREGS_BY_SLOTS', 'ARGREGS_FP_CONSUME_GP',
        'ARGREGS_GP_ONLY', 'ARGREGS_INDEPENDENT', 'ARGREGS_MIPS_O32',
        'ARGREGS_POLICY_UNDEFINED', 'AST_DISABLE', 'AST_DISABLE_ALWAYS',
        'AST_DISABLE_FOR_IDB', 'AST_DISABLE_FOR_WIDGET', 'AST_ENABLE',
        'AST_ENABLE_ALWAYS', 'AST_ENABLE_FOR_IDB',
        'AST_ENABLE_FOR_WIDGET', 'BK_INVALIDADDR', 'BK_NOVALUE',
        'BK_VALID', 'BPLT_ABS', 'BPLT_REL', 'BPLT_SRC', 'BPLT_SYM',
        'BREAKPOINT', 'CB_CLOSE', 'CB_DESTROYING', 'CB_INIT',
        'CB_INVISIBLE', 'CB_YES', 'CDVH_LINES_ALIGNMENT',
        'CDVH_LINES_CLICK', 'CDVH_LINES_DBLCLICK', 'CDVH_LINES_DRAWICON',
        'CDVH_LINES_ICONMARGIN', 'CDVH_LINES_LINENUM', 'CDVH_LINES_POPUP',
        'CDVH_LINES_RADIX', 'CDVH_SRCVIEW', 'CDVH_USERDATA', 'CVH_CLICK',
        'CVH_CLOSE', 'CVH_CURPOS', 'CVH_DBLCLICK', 'CVH_HELP',
        'CVH_KEYDOWN', 'CVH_MOUSEMOVE', 'CVH_POPUP', 'CVH_QT_AWARE',
        'CVH_USERDATA', 'DEBNAME_EXACT', 'DEBNAME_LOWER', 'DEBNAME_NICE',
        'DEBNAME_UPPER', 'DEC_ERROR', 'DEC_NOTASK', 'DEC_TIMEOUT',
        'DIRTREE_BPTS', 'DIRTREE_END', 'DIRTREE_ENUMS',
        'DIRTREE_ENUMS_BOOKMARKS', 'DIRTREE_FUNCS',
        'DIRTREE_IDAPLACE_BOOKMARKS', 'DIRTREE_IMPORTS',
        'DIRTREE_LOCAL_TYPES', 'DIRTREE_NAMES', 'DIRTREE_STRUCTS',
        'DIRTREE_STRUCTS_BOOKMARKS', 'DQT_COMPILER', 'DQT_FULL',
        'DQT_NAME_TYPE', 'DQT_NPURGED_2', 'DQT_NPURGED_4',
        'DQT_NPURGED_8', 'DRC_CRC', 'DRC_ERROR', 'DRC_EVENTS',
        'DRC_FAILED', 'DRC_IDBSEG', 'DRC_NETERR', 'DRC_NOCHG',
        'DRC_NOFILE', 'DRC_NONE', 'DRC_NOPROC', 'DRC_OK',
        'DTE_ALREADY_EXISTS', 'DTE_BAD_PATH', 'DTE_CANT_RENAME',
        'DTE_LAST', 'DTE_MAX_DIR', 'DTE_NOT_DIRECTORY', 'DTE_NOT_EMPTY',
        'DTE_NOT_FOUND', 'DTE_OK', 'DTE_OWN_CHILD', 'DTN_DISPLAY_NAME',
        'DTN_FULL_NAME', 'EXCEPTION', 'FILE', 'FIND_EXTLANG_BY_EXT',
        'FIND_EXTLANG_BY_IDX', 'FIND_EXTLANG_BY_NAME', 'FMTFUNC_PRINTF',
        'FMTFUNC_SCANF', 'FMTFUNC_STRFMON', 'FMTFUNC_STRFTIME',
        'FPC_ARGS', 'FPC_LVARS', 'FPC_RETADDR', 'FPC_SAVREGS',
        'FPV_BADARG', 'FPV_NAN', 'FPV_NINF', 'FPV_NORM', 'FPV_PINF',
        'GDE_ERROR', 'GDE_MANY_EVENTS', 'GDE_NO_EVENT', 'GDE_ONE_EVENT',
        'GTD_CALC_ARGLOCS', 'GTD_CALC_LAYOUT', 'GTD_DEL_BITFLDS',
        'GTD_NO_ARGLOCS', 'GTD_NO_LAYOUT', 'GTS_BASECLASS', 'GTS_NESTED',
        'HF_COMMENT', 'HF_DEFAULT', 'HF_KEYWORD1', 'HF_KEYWORD2',
        'HF_KEYWORD3', 'HF_MAX', 'HF_NUMBER', 'HF_PREPROC', 'HF_STRING',
        'HT_DBG', 'HT_DEV', 'HT_GRAPH', 'HT_IDB', 'HT_IDD', 'HT_IDP',
        'HT_LAST', 'HT_OUTPUT', 'HT_UI', 'HT_VIEW', 'INFORMATION',
        'INF_ABIBITS', 'INF_ABINAME', 'INF_AF', 'INF_AF2',
        'INF_APPCALL_OPTIONS', 'INF_APPTYPE', 'INF_ARCHIVE_PATH',
        'INF_ASMTYPE', 'INF_BASEADDR', 'INF_BIN_PREFIX_SIZE', 'INF_CC',
        'INF_CC_CM', 'INF_CC_DEFALIGN', 'INF_CC_ID', 'INF_CC_SIZE_B',
        'INF_CC_SIZE_E', 'INF_CC_SIZE_I', 'INF_CC_SIZE_L',
        'INF_CC_SIZE_LDBL', 'INF_CC_SIZE_LL', 'INF_CC_SIZE_S',
        'INF_CMTFLG', 'INF_CMT_INDENT', 'INF_CRC32', 'INF_CTIME',
        'INF_C_MACROS', 'INF_DATABASE_CHANGE_COUNT', 'INF_DATATYPES',
        'INF_DBG_BINPATHS', 'INF_DEMNAMES', 'INF_DUALOP_GRAPH',
        'INF_DUALOP_TEXT', 'INF_ELAPSED', 'INF_FILETYPE',
        'INF_FILE_FORMAT_NAME', 'INF_FSIZE', 'INF_GENFLAGS', 'INF_GROUPS',
        'INF_HIGHOFF', 'INF_H_PATH', 'INF_IDA_VERSION', 'INF_IDSNODE',
        'INF_IMAGEBASE', 'INF_INCLUDE', 'INF_INDENT',
        'INF_INITIAL_VERSION', 'INF_INPUT_FILE_PATH', 'INF_LAST',
        'INF_LENXREF', 'INF_LFLAGS', 'INF_LIMITER', 'INF_LISTNAMES',
        'INF_LONG_DEMNAMES', 'INF_LOWOFF', 'INF_MAIN', 'INF_MARGIN',
        'INF_MAXREF', 'INF_MAX_AUTONAME_LEN', 'INF_MAX_EA', 'INF_MD5',
        'INF_MIN_EA', 'INF_NAMETYPE', 'INF_NETDELTA', 'INF_NOPENS',
        'INF_NOTEPAD', 'INF_OMAX_EA', 'INF_OMIN_EA', 'INF_OSTYPE',
        'INF_OUTFILEENC', 'INF_OUTFLAGS', 'INF_PREFFLAG', 'INF_PRIVRANGE',
        'INF_PRIVRANGE_END_EA', 'INF_PRIVRANGE_START_EA', 'INF_PROBLEMS',
        'INF_PROCNAME', 'INF_REFCMTNUM', 'INF_SELECTORS', 'INF_SHA256',
        'INF_SHORT_DEMNAMES', 'INF_SPECSEGS', 'INF_SRCDBG_PATHS',
        'INF_SRCDBG_UNDESIRED', 'INF_START_CS', 'INF_START_EA',
        'INF_START_IP', 'INF_START_SP', 'INF_START_SS',
        'INF_STRLIT_BREAK', 'INF_STRLIT_FLAGS', 'INF_STRLIT_PREF',
        'INF_STRLIT_SERNUM', 'INF_STRLIT_ZEROES', 'INF_STRTYPE',
        'INF_STR_ENCODINGS', 'INF_TYPE_XREFNUM', 'INF_VERSION',
        'INF_XREFFLAG', 'INF_XREFNUM', 'JT_ARR', 'JT_BOOL', 'JT_CALL',
        'JT_NONE', 'JT_NUM', 'JT_OBJ', 'JT_STR', 'JT_SWITCH',
        'JT_UNKNOWN', 'LECVT_CANCELED', 'LECVT_ERROR', 'LECVT_OK',
        'LIB_LOADED', 'LIB_UNLOADED', 'LINPUT_GENERIC', 'LINPUT_LOCAL',
        'LINPUT_NONE', 'LINPUT_PROCMEM', 'LINPUT_RFILE', 'LOC_CLOSE',
        'LOC_KEEP', 'LOC_UNMAKE', 'MD5Final', 'MD5Init', 'MD5Transform',
        'MD5Update', 'MOVBPT_BAD_TYPE', 'MOVBPT_DEST_BUSY',
        'MOVBPT_NOT_FOUND', 'MOVBPT_OK', 'NOTHING_CHANGED', 'NO_ACCESS',
        'NO_EVENT', 'OFILE_ASM', 'OFILE_DIF', 'OFILE_EXE', 'OFILE_IDC',
        'OFILE_LST', 'OFILE_MAP', 'PATH_TYPE_CMD', 'PATH_TYPE_ID0',
        'PATH_TYPE_IDB', 'PLUGIN', 'PROCESS_ATTACHED', 'PROCESS_DETACHED',
        'PROCESS_EXITED', 'PROCESS_STARTED', 'PROCESS_SUSPENDED',
        'QMOVE_CROSS_FS', 'QMOVE_OVERWRITE', 'QMOVE_OVR_RO',
        'RANGE_KIND_FUNC', 'RANGE_KIND_HIDDEN_RANGE',
        'RANGE_KIND_SEGMENT', 'RANGE_KIND_UNKNOWN', 'READ_ACCESS',
        'REAL_ERROR_BADDATA', 'REAL_ERROR_BADSTR', 'REAL_ERROR_FORMAT',
        'REAL_ERROR_FPOVER', 'REAL_ERROR_INTOVER', 'REAL_ERROR_OK',
        'REAL_ERROR_RANGE', 'REAL_ERROR_ZERODIV', 'REG_ASSERT',
        'REG_BADBR', 'REG_BADPAT', 'REG_BADRPT', 'REG_EBRACE',
        'REG_EBRACK', 'REG_ECOLLATE', 'REG_ECTYPE', 'REG_EESCAPE',
        'REG_EMPTY', 'REG_EPAREN', 'REG_ERANGE', 'REG_ESIZE',
        'REG_ESPACE', 'REG_ESUBREG', 'REG_INVARG', 'REG_NOMATCH',
        'RESMOD_HANDLE', 'RESMOD_INTO', 'RESMOD_MAX', 'RESMOD_NONE',
        'RESMOD_OUT', 'RESMOD_OVER', 'RESMOD_SRCINTO', 'RESMOD_SRCOUT',
        'RESMOD_SRCOVER', 'RESMOD_USER', 'RW_ACCESS', 'SAVE_ALL_VALUES',
        'SAVE_DIFF', 'SAVE_NONE', 'SELECTION_CHANGED', 'SETPROC_IDB',
        'SETPROC_LOADER', 'SETPROC_LOADER_NON_FATAL', 'SETPROC_USER',
        'SMT_ARRAY', 'SMT_BADARG', 'SMT_FAILED', 'SMT_KEEP',
        'SMT_NOCOMPAT', 'SMT_OK', 'SMT_OVERLAP', 'SMT_SIZE', 'SMT_WORSE',
        'SRCIT_EXPR', 'SRCIT_FUNC', 'SRCIT_LOCVAR', 'SRCIT_MODULE',
        'SRCIT_NONE', 'SRCIT_STMT', 'SRCIT_STTVAR', 'STEP', 'STI_ACCHAR',
        'STI_ACHAR', 'STI_ACUCHAR', 'STI_AEABI_LCMP', 'STI_AEABI_MEMCLR',
        'STI_AEABI_MEMCPY', 'STI_AEABI_MEMSET', 'STI_AEABI_ULCMP',
        'STI_AUCHAR', 'STI_COMPLEX128', 'STI_COMPLEX64', 'STI_DONT_USE',
        'STI_FDELOP', 'STI_FPURGING', 'STI_LAST', 'STI_MSGSEND',
        'STI_PBYTE', 'STI_PCCHAR', 'STI_PCHAR', 'STI_PCUCHAR',
        'STI_PCVOID', 'STI_PINT', 'STI_PPVOID', 'STI_PUCHAR', 'STI_PUINT',
        'STI_PVOID', 'STI_RTC_CHECK_2', 'STI_RTC_CHECK_4',
        'STI_RTC_CHECK_8', 'STI_SIZE_T', 'STI_SSIZE_T',
        'STRUC_ERROR_MEMBER_NAME', 'STRUC_ERROR_MEMBER_NESTED',
        'STRUC_ERROR_MEMBER_OFFSET', 'STRUC_ERROR_MEMBER_OK',
        'STRUC_ERROR_MEMBER_SIZE', 'STRUC_ERROR_MEMBER_STRUCT',
        'STRUC_ERROR_MEMBER_TINFO', 'STRUC_ERROR_MEMBER_UNIVAR',
        'STRUC_ERROR_MEMBER_VARLAST', 'STT_CUR', 'STT_DBG', 'STT_MM',
        'STT_VA', 'TCCPT_ENUMPLACE', 'TCCPT_IDAPLACE', 'TCCPT_INVALID',
        'TCCPT_PLACE', 'TCCPT_SIMPLELINE_PLACE', 'TCCPT_STRUCTPLACE',
        'TCCRT_FLAT', 'TCCRT_GRAPH', 'TCCRT_INVALID', 'TCCRT_PROXIMITY',
        'TCT_NOT_OWNER', 'TCT_OWNER', 'TCT_UNKNOWN', 'TERR_BADSYNC',
        'TERR_OK', 'TERR_SAVE', 'TERR_SERIALIZE', 'TERR_WRONGNAME',
        'THREAD_EXITED', 'THREAD_STARTED', 'TRACE_FULL', 'UCDR_MANGLED',
        'UCDR_NAME', 'UCDR_STRLIT', 'UCDR_TYPE', 'UTP_ENUM', 'UTP_STRUCT',
        'VME_LEFT_BUTTON', 'VME_MID_BUTTON', 'VME_RIGHT_BUTTON',
        'VME_UNKNOWN', 'VNT_IDENT', 'VNT_STRLIT', 'VNT_TYPE',
        'VNT_UDTMEM', 'VNT_VISIBLE', 'WRITE_ACCESS',
        '_0425F8F1A3AE8F87FA89CDE6305293FE',
        '_06ACCA0CDDC5718C62D5A4485E2E115D',
        '_0F4B5B224EF598EAC96C9D985A235D75',
        '_12B695DC843A94285F7310A143C8C434',
        '_13DEA147606768949B8709A1F27A1AE6',
        '_223DCB884574D5DE586AD2D6B7376847',
        '_2B5C0BD264F9291D6A7F6F791424403F',
        '_2C0E99206E7908236DCABCB2B91A8D4F',
        '_403A3450421E1FA417431FD6F5C6B815',
        '_40A15942B64B468D028A9EDC3BF273C3',
        '_47EB95A8857FB680635907AB7DCDCDE8',
        '_47FFB0B1AABFAE006217B68E4FFCB4B3',
        '_486A9EF9057A4F79C352527BA63EDFD3',
        '_492C834E753BED590AB0BAB80BEB78E7',
        '_5199E2C0DF2CA3E7E8DCA56464B8E928',
        '_53B156155FBE7E40597743DACE3276C6',
        '_5D6657710F2FD348305D4B59534642C3',
        '_5DBD8E863343736E5AD8CF23F5B72447',
        '_6748483DB9EEBDB64F2EA25B987191DF',
        '_7014156F94AE1B7FC5F5E3560392A8C4',
        '_7148FF134A2561D170DBC235C372E12B',
        '_77081ABAD94FC9A5EE14B650E0DBF110',
        '_776C644986E1218BAA015F499D7289A7',
        '_79278B08C9A02D276B5400213E6E8772',
        '_7A67CD558302B3EA29FC91F77D84E941',
        '_7C51D3F4B871613F1BA7F83DBEBC3FD5',
        '_94760D3F2768AB73DF4E13DC5B377508',
        '_94D4D585A38CDA12BD4A7F760DAFD340',
        '_9E76F4EBF8BA4D34546A573D2A95E8EF',
        '_9F642B09C10686E3843EA25A959506D5',
        '_A2117BA638E63C1EAFEA64D9666358AE',
        '_A32948CF266C727D9CC1D79F2B35CC28',
        '_A6F93F8BAFF0D1A2AF75D768A5FCB062',
        '_AF4ED28A64411848F4EED41572FA4CE1',
        '_B4F266B0568ADA5794EA29B6B9D8A3FE',
        '_B583FC0ED2D81EF34EE9B85011DA3455',
        '_BCFAB6CAE5EB6A58B72F2C0C12D28D2B',
        '_C09AF1331CFCFC509FB4233AA5230FB3',
        '_C7C212E52085C0E483DB7F2B4EDAB218',
        '_C9E14A82B8291B557AC92E2F5A452CE5',
        '_DB40683AED1FE27CD84662F2517C7BCC',
        '_EFB3D94CDC38BD29E337526787ABDBEA',
        '_F6359FE077454C49B917BFA4BFA37580',
        '_F6553CF4C635466D7A900A328CA0BFD3', '_Left', '_Right', '_Unused',
        '_qstring_char___const_iterator', '_qstring_char___iterator',
        '_qstring_unsigned_char___const_iterator',
        '_qstring_unsigned_char___iterator',
        '_qstring_wchar_t___const_iterator',
        '_qstring_wchar_t___iterator', '_source_file_iterator',
        '_source_item_iterator', 'abs_no', 'abs_t', 'abs_unk', 'abs_yes',
        'access_type_t', 'action_activation_ctx_t', 'action_attr_t',
        'action_state_t', 'action_update_ctx_t', 'add_auto_stkpnt',
        'add_base_tils', 'add_byte', 'add_cref', 'add_dref', 'add_dword',
        'add_encoding', 'add_entry', 'add_enum', 'add_enum_member',
        'add_frame', 'add_func_ex', 'add_hidden_range', 'add_idc_class',
        'add_idc_func', 'add_idc_gvar', 'add_mapping', 'add_qword',
        'add_refinfo_dref', 'add_regarg', 'add_regvar', 'add_segm',
        'add_segm_ex', 'add_segment_translation', 'add_sourcefile',
        'add_spaces', 'add_stkvar', 'add_struc', 'add_struc_member',
        'add_til', 'add_tryblk', 'add_user_stkpnt', 'add_word',
        'adding_segm', 'adiff_t', 'aflags_t', 'align_down_to_stack',
        'align_up_to_stack', 'alloc_type_ordinals', 'allocate_selector',
        'allsegs_moved', 'append_abi_opts', 'append_argloc', 'append_cmt',
        'append_disp', 'append_func_tail', 'append_snprintf',
        'append_struct_fields', 'append_tinfo_covered',
        'append_to_flowchart', 'apply_callee_tinfo', 'apply_cdecl',
        'apply_fixup', 'apply_idasgn_to', 'apply_named_type',
        'apply_once_tinfo_and_name', 'apply_startup_sig', 'apply_tinfo',
        'apply_tinfo_to_stkarg', 'argloc_t__biggest_t', 'argloc_type_t',
        'arglocs_t', 'argpartvec_t', 'argreg_policy_t',
        'array_of_intmap_t', 'array_of_intvec_t', 'array_of_node_set_t',
        'array_of_rangesets', 'asctoreal', 'ash', 'asize_t', 'atob32',
        'atob64', 'atoea', 'atos', 'attach_custom_data_format', 'atype_t',
        'auto_apply_tail', 'auto_apply_type', 'auto_cancel', 'auto_empty',
        'auto_empty_finally', 'auto_get', 'auto_is_ok', 'auto_make_step',
        'auto_mark_range', 'auto_recreate_insn', 'auto_unmark',
        'auto_wait', 'auto_wait_range', 'b2a32', 'b2a64', 'b2a_width',
        'back_char', 'backward_flow_iterator_t_State__Ctrl___visited_t',
        'backward_flow_iterator_t_no_regs_t__simple_bfi_t___waiting_t',
        'base2file', 'base64_decode', 'base64_encode', 'batch',
        'beep_default', 'beep_t', 'begin_type_updating', 'bgcolor_t',
        'bin_search', 'bin_search2', 'bin_search3', 'bitcount',
        'bitrange_t_extract_using_bitrange',
        'bitrange_t_inject_using_bitrange', 'blob_idx_t', 'bmask_t',
        'bookmark_changed', 'bookmarks_t_erase', 'bookmarks_t_find_index',
        'bookmarks_t_get', 'bookmarks_t_get_desc',
        'bookmarks_t_get_dirtree_id', 'bookmarks_t_mark',
        'bookmarks_t_set_desc', 'bookmarks_t_size', 'boolvec_t',
        'bpt_constptr_vec_t', 'bpt_loctype_t', 'bpt_vec_t', 'bpteas_t',
        'bptptr_vec_t', 'bpttype_t', 'bte_t', 'btoa128', 'btoa32',
        'btoa64', 'btoa_width', 'build_anon_type_name',
        'build_loaders_list', 'build_snapshot_tree', 'build_stkvar_name',
        'build_stkvar_xrefs', 'build_strlist', 'byte_patched',
        'calc_bg_color', 'calc_c_cpp_name', 'calc_crc32', 'calc_dataseg',
        'calc_def_align', 'calc_file_crc32', 'calc_fixup_size',
        'calc_func_size', 'calc_idasgn_state', 'calc_max_align',
        'calc_max_item_end', 'calc_min_align', 'calc_number_of_children',
        'calc_offset_base', 'calc_prefix_color',
        'calc_probable_base_by_value', 'calc_reference_data',
        'calc_stkvar_struc_offset', 'calc_switch_cases',
        'calc_thunk_func_target', 'calc_tinfo_gaps', 'call_idc_func',
        'call_system', 'callee_addr_changed', 'callui', 'can_be_off32',
        'can_define_item', 'casevec_t', 'catchvec_t', 'cb_id',
        'cfgopt_t__apply', 'cfgopt_t__apply2', 'cfgopt_t__apply3',
        'change_codepage', 'change_segment_status', 'change_storage_type',
        'changing_cmt', 'changing_enum_bf', 'changing_enum_cmt',
        'changing_op_ti', 'changing_op_type', 'changing_range_cmt',
        'changing_segm_class', 'changing_segm_end', 'changing_segm_name',
        'changing_segm_start', 'changing_struc_align',
        'changing_struc_cmt', 'changing_struc_member', 'changing_ti',
        'channel_redirs_t', 'check_flat_jump_table',
        'check_for_table_jump', 'check_process_exit', 'check_spoiled_jpt',
        'choose_ioport_device', 'choose_ioport_device2',
        'choose_local_tinfo', 'choose_local_tinfo_and_delta',
        'choose_named_type', 'choose_type_t', 'chooser_base_t__cbres_t',
        'chtype_entry', 'chtype_enum', 'chtype_enum_by_value',
        'chtype_enum_by_value_and_size', 'chtype_func', 'chtype_generic',
        'chtype_idasgn', 'chtype_idatil', 'chtype_name', 'chtype_segm',
        'chtype_srcp', 'chtype_stkvar_xref', 'chtype_strpath',
        'chtype_struc', 'chtype_xref', 'chunk_size', 'chunk_start',
        'cleanup_appcall', 'cleanup_argloc', 'cleanup_name',
        'clear_strlist', 'clear_tinfo_t', 'cliopt_handler_t',
        'cliopt_poly_handler_t', 'cliopts_t__usage_printer_t',
        'cliopts_t_add', 'cliopts_t_apply', 'cliopts_t_find_long',
        'cliopts_t_find_short', 'cliopts_t_usage', 'close_linput',
        'closebase', 'closing_comment', 'clr_abits', 'clr_lzero',
        'clr_module_data', 'clr_node_info', 'clr_op_type', 'cm_t',
        'cmt_changed', 'code_highlight_block', 'color_t',
        'combine_regs_jpt', 'comp_t', 'compact_numbered_types',
        'compact_til', 'compare_arglocs', 'compare_tinfo',
        'compile_idc_file', 'compile_idc_snippet', 'compile_idc_text',
        'compiled_binpat_vec_t', 'compiler_changed', 'compvec_t',
        'const_t', 'construct_macro', 'construct_macro2',
        'convert_encoding', 'copy_argloc', 'copy_debug_event',
        'copy_idcv', 'copy_named_type', 'copy_sreg_ranges',
        'copy_tinfo_t', 'create_16bit_data', 'create_32bit_data',
        'create_align', 'create_bytearray_linput', 'create_data',
        'create_dirtree', 'create_encoding_helper', 'create_filename_cmt',
        'create_generic_linput', 'create_idcv_ref', 'create_insn',
        'create_lexer', 'create_memory_linput',
        'create_multirange_qflow_chart', 'create_numbered_type_name',
        'create_outctx', 'create_qflow_chart', 'create_strlit',
        'create_switch_table', 'create_switch_xrefs', 'create_tinfo',
        'create_xrefs_from', 'create_zip_linput', 'cref_t',
        'custom_viewer_handler_id_t', 'dbg', 'dbg_appcall', 'dbg_bpt',
        'dbg_bpt_changed', 'dbg_event_code_t', 'dbg_exception',
        'dbg_finished_loading_bpts', 'dbg_get_input_path',
        'dbg_information', 'dbg_last', 'dbg_library_load',
        'dbg_library_unload', 'dbg_notification_t', 'dbg_null',
        'dbg_process_attach', 'dbg_process_detach', 'dbg_process_exit',
        'dbg_process_start', 'dbg_request_error', 'dbg_run_to',
        'dbg_started_loading_bpts', 'dbg_step_into', 'dbg_step_over',
        'dbg_step_until_ret', 'dbg_suspend_process', 'dbg_thread_exit',
        'dbg_thread_start', 'dbg_trace', 'dbgevt_vec_t', 'dbt_cancel',
        'dbt_no', 'dbt_yes', 'debug', 'debug_name_how_t',
        'debugger_t__event_t', 'decode_insn', 'decode_preceding_insn',
        'decode_prev_insn', 'decorate_name', 'deep_copy_idcv',
        'define_stkvar', 'del_aflags', 'del_cref', 'del_debug_names',
        'del_dref', 'del_encoding', 'del_enum', 'del_enum_member',
        'del_extra_cmt', 'del_fixup', 'del_frame', 'del_func',
        'del_hidden_range', 'del_idasgn', 'del_idc_func', 'del_idcv_attr',
        'del_item_color', 'del_items', 'del_mapping', 'del_member_tinfo',
        'del_named_type', 'del_node_info', 'del_numbered_type',
        'del_qatexit', 'del_refinfo', 'del_regvar', 'del_segm',
        'del_segment_translations', 'del_selector', 'del_source_linnum',
        'del_sourcefile', 'del_sreg_range', 'del_stkpnt', 'del_str_type',
        'del_struc', 'del_struc_member', 'del_struc_members',
        'del_switch_info', 'del_til', 'del_tinfo_attr', 'del_tryblks',
        'del_value', 'delete_all_xrefs_from', 'delete_dirtree',
        'delete_extra_cmts', 'delete_imports', 'delete_switch_table',
        'delete_unreferenced_stkvars', 'delete_wrong_stkvar_ops',
        'deleting_enum', 'deleting_enum_member', 'deleting_func',
        'deleting_func_tail', 'deleting_segm', 'deleting_struc',
        'deleting_struc_member', 'deleting_tryblks', 'delinf', 'demangle',
        'demangle_name', 'demreq_type_t', 'deref_idcv', 'deref_ptr',
        'deserialize_dynamic_register_set', 'deserialize_tinfo',
        'destroy_lexer', 'destroyed_items', 'detach_custom_data_format',
        'determine_rtl', 'determined_main', 'diffpos_t', 'direntry_vec_t',
        'diridx_t', 'dirtree_change_rank', 'dirtree_chdir',
        'dirtree_cursor_vec_t', 'dirtree_errstr', 'dirtree_find_entry',
        'dirtree_findfirst', 'dirtree_findnext',
        'dirtree_get_abspath_by_cursor', 'dirtree_get_abspath_by_relpath',
        'dirtree_get_dir_size', 'dirtree_get_entry_attrs',
        'dirtree_get_entry_name', 'dirtree_get_id',
        'dirtree_get_nodename', 'dirtree_get_parent_cursor',
        'dirtree_get_rank', 'dirtree_getcwd', 'dirtree_id_t',
        'dirtree_link', 'dirtree_link', 'dirtree_link_inode',
        'dirtree_mkdir', 'dirtree_mkdir', 'dirtree_move', 'dirtree_rank',
        'dirtree_rename', 'dirtree_resolve_cursor',
        'dirtree_resolve_path', 'dirtree_rmdir', 'dirtree_rmdir',
        'dirtree_rminode', 'dirtree_segm_moved', 'dirtree_set_id',
        'dirtree_set_nodename', 'dirtree_traverse', 'dirvec_t',
        'disable_flags', 'display_gdl', 'dk_addr_names', 'dk_addr_text',
        'dk_float', 'dk_int', 'dr_I', 'dr_O', 'dr_R', 'dr_S', 'dr_T',
        'dr_U', 'dr_W', 'drc_t', 'dref_t', 'dstr_tinfo', 'dterr_t',
        'dummy_name_ea', 'dump_func_type_data',
        'dynamic_register_set_t__const_char_vec_t', 'eNI', 'ea2node',
        'ea2str', 'ea64_t', 'ea_name_vec_t', 'ea_t', 'eadd', 'eavec_t',
        'echsize', 'eclose', 'ecmp', 'ecreate', 'edge_back', 'edge_cross',
        'edge_error', 'edge_forward', 'edge_subgraph', 'edge_tree',
        'edge_type_t', 'edgevec_t', 'ediv', 'eetol', 'eetol64',
        'eetol64u', 'eldexp', 'eltoe', 'eltoe64', 'eltoe64u', 'emdnorm',
        'emovi', 'emovo', 'emul', 'enable_auto', 'enable_flags',
        'enable_numbered_types', 'encoder_t__notify_recerr_t',
        'end_type_updating', 'enum_bf_changed', 'enum_cmt_changed',
        'enum_created', 'enum_deleted', 'enum_flag_changed',
        'enum_import_names', 'enum_member_created', 'enum_member_deleted',
        'enum_member_vec_t', 'enum_ordinal_changed', 'enum_renamed',
        'enum_t', 'enum_width_changed', 'enumerate_files',
        'enumerate_files2', 'enumerate_segments_with_selector',
        'enumerate_selectors', 'enumplace_t__adjust',
        'enumplace_t__beginning', 'enumplace_t__clone',
        'enumplace_t__compare', 'enumplace_t__compare2',
        'enumplace_t__copyfrom', 'enumplace_t__deserialize',
        'enumplace_t__ending', 'enumplace_t__enter',
        'enumplace_t__generate', 'enumplace_t__id', 'enumplace_t__leave',
        'enumplace_t__makeplace', 'enumplace_t__name',
        'enumplace_t__next', 'enumplace_t__prev', 'enumplace_t__print',
        'enumplace_t__rebase', 'enumplace_t__serialize',
        'enumplace_t__toea', 'enumplace_t__touval', 'equal_bytes',
        'eread', 'error_t', 'errorexit', 'eseek', 'eshift', 'ev_add_cref',
        'ev_add_dref', 'ev_adjust_argloc', 'ev_adjust_libfunc_ea',
        'ev_adjust_refinfo', 'ev_ana_insn', 'ev_analyze_prolog',
        'ev_appcall', 'ev_arch_changed', 'ev_arg_addrs_ready',
        'ev_asm_installed', 'ev_assemble', 'ev_attach_process',
        'ev_auto_queue_empty', 'ev_bin_search', 'ev_broadcast',
        'ev_calc_arglocs', 'ev_calc_cdecl_purged_bytes',
        'ev_calc_next_eas', 'ev_calc_purged_bytes', 'ev_calc_retloc',
        'ev_calc_spdelta', 'ev_calc_step_over', 'ev_calc_switch_cases',
        'ev_calc_varglocs', 'ev_calcrel', 'ev_can_have_type',
        'ev_check_bpt', 'ev_clean_tbit', 'ev_cleanup_appcall',
        'ev_close_file', 'ev_cmp_operands', 'ev_coagulate',
        'ev_coagulate_dref', 'ev_create_flat_group',
        'ev_create_func_frame', 'ev_create_merge_handlers',
        'ev_create_switch_xrefs', 'ev_creating_segm',
        'ev_dbg_enable_trace', 'ev_decorate_name', 'ev_del_cref',
        'ev_del_dref', 'ev_delay_slot_insn', 'ev_demangle_name',
        'ev_detach_process', 'ev_emu_insn', 'ev_endbinary',
        'ev_ending_undo', 'ev_equal_reglocs', 'ev_eval_lowcnd',
        'ev_exit_process', 'ev_extract_address', 'ev_find_op_value',
        'ev_find_reg_value', 'ev_func_bounds', 'ev_gen_asm_or_lst',
        'ev_gen_map_file', 'ev_gen_regvar_def', 'ev_gen_src_file_lnnum',
        'ev_gen_stkvar_def', 'ev_get_abi_info', 'ev_get_autocmt',
        'ev_get_bg_color', 'ev_get_cc_regs', 'ev_get_code16_mode',
        'ev_get_dbr_opnum', 'ev_get_debapp_attrs',
        'ev_get_debmod_extensions', 'ev_get_debug_event',
        'ev_get_default_enum_size', 'ev_get_frame_retsize',
        'ev_get_idd_opinfo', 'ev_get_macro_insn_head',
        'ev_get_memory_info', 'ev_get_operand_string', 'ev_get_processes',
        'ev_get_procmod', 'ev_get_reg_accesses', 'ev_get_reg_info',
        'ev_get_reg_name', 'ev_get_simd_types', 'ev_get_srcinfo_path',
        'ev_get_stkarg_area_info', 'ev_get_stkvar_scale_factor',
        'ev_getreg', 'ev_init', 'ev_init_debugger', 'ev_insn_reads_tbit',
        'ev_is_align_insn', 'ev_is_alloca_probe', 'ev_is_basic_block_end',
        'ev_is_call_insn', 'ev_is_cond_insn', 'ev_is_control_flow_guard',
        'ev_is_far_jump', 'ev_is_indirect_jump', 'ev_is_insn_table_jump',
        'ev_is_jump_func', 'ev_is_ret_insn', 'ev_is_sane_insn',
        'ev_is_sp_based', 'ev_is_switch', 'ev_is_tracing_enabled',
        'ev_last_cb_before_debugger', 'ev_last_cb_before_loader',
        'ev_last_cb_before_type_callbacks', 'ev_loader',
        'ev_loader_elf_machine', 'ev_lower_func_type', 'ev_map_address',
        'ev_max_ptr_size', 'ev_may_be_func', 'ev_may_show_sreg',
        'ev_moving_segm', 'ev_newasm', 'ev_newbinary', 'ev_newfile',
        'ev_newprc', 'ev_next_exec_insn', 'ev_obsolete1', 'ev_obsolete2',
        'ev_oldfile', 'ev_open_file', 'ev_out_assumes', 'ev_out_data',
        'ev_out_footer', 'ev_out_header', 'ev_out_insn', 'ev_out_label',
        'ev_out_mnem', 'ev_out_operand', 'ev_out_segend',
        'ev_out_segstart', 'ev_out_special_item', 'ev_privrange_changed',
        'ev_read_file', 'ev_read_memory', 'ev_read_registers',
        'ev_realcvt', 'ev_rebase_if_required_to', 'ev_rename',
        'ev_replaying_undo', 'ev_request_pause', 'ev_resume', 'ev_rexec',
        'ev_send_ioctl', 'ev_set_code16_mode', 'ev_set_exception_info',
        'ev_set_idp_options', 'ev_set_proc_options', 'ev_set_resume_mode',
        'ev_setup_til', 'ev_start_process', 'ev_str2reg', 'ev_suspended',
        'ev_term', 'ev_term_debugger', 'ev_thread_continue',
        'ev_thread_get_sreg_base', 'ev_thread_suspend',
        'ev_treat_hindering_item', 'ev_undefine', 'ev_update_bpts',
        'ev_update_call_stack', 'ev_update_call_stack',
        'ev_update_lowcnds', 'ev_use_arg_types', 'ev_use_regarg_type',
        'ev_use_stkarg_type', 'ev_validate_flirt_func',
        'ev_verify_noreturn', 'ev_verify_sp', 'ev_write_file',
        'ev_write_memory', 'ev_write_register', 'eval_expr',
        'eval_expr_long', 'eval_idc_expr', 'eval_idc_snippet',
        'event_id_t', 'ewrite', 'excvec_t', 'exec_system_script',
        'expand_struc', 'expanding_struc', 'extend_sign',
        'external_colorizers_t', 'external_ident_colorizers_t',
        'extlang_changed', 'extlang_object_t', 'extlangs_t',
        'extra_cmt_changed', 'extract_argloc',
        'extract_module_from_archive', 'extract_name', 'f_AIXAR',
        'f_AOUT', 'f_AR', 'f_BIN', 'f_COFF', 'f_COM', 'f_COM_old',
        'f_DRV', 'f_ELF', 'f_EXE', 'f_EXE_old', 'f_HEX', 'f_LE',
        'f_LOADER', 'f_LX', 'f_MACHO', 'f_MEX', 'f_NLM', 'f_OMF',
        'f_OMFLIB', 'f_PE', 'f_PRC', 'f_PSXOBJ', 'f_SREC', 'f_W32RUN',
        'f_WIN', 'f_ZIP', 'fc_block_type_t', 'fc_calc_block_type',
        'fcb_cndret', 'fcb_enoret', 'fcb_error', 'fcb_extern',
        'fcb_indjump', 'fcb_noret', 'fcb_normal', 'fcb_ret', 'file2base',
        'file_janitor_t', 'filetype_t', 'find_binary', 'find_byte',
        'find_byter', 'find_code', 'find_custom_data_format',
        'find_custom_data_type', 'find_custom_fixup',
        'find_custom_refinfo', 'find_data', 'find_defined',
        'find_defjump_from_table', 'find_error', 'find_extlang',
        'find_extlang_kind_t', 'find_free_selector', 'find_func_bounds',
        'find_idc_class', 'find_idc_func', 'find_idc_gvar', 'find_imm',
        'find_ioport', 'find_ioport_bit', 'find_jtable_size',
        'find_not_func', 'find_notype', 'find_plugin', 'find_reg_access',
        'find_regvar', 'find_selector', 'find_suspop', 'find_syseh',
        'find_text', 'find_tinfo_udt_member', 'find_unknown',
        'first_idcv_attr', 'first_named_type', 'fixup_type_t', 'fixups_t',
        'fl_CF', 'fl_CN', 'fl_F', 'fl_JF', 'fl_JN', 'fl_U',
        'fl_USobsolete', 'flags_t', 'flow_chart_created', 'flush_buffers',
        'fopenA', 'fopenM', 'fopenRB', 'fopenRT', 'fopenWB', 'fopenWT',
        'for_all_arglocs', 'for_all_enum_members', 'for_all_extlangs',
        'forget_problem', 'form_actions_t__dlgbtn_t', 'format_c_number',
        'format_cdata', 'format_charlit', 'format_functype_t',
        'fpvalue_error_t', 'fpvalue_kind_t', 'frame_deleted',
        'frame_part_t', 'freadbytes', 'free_chunk', 'free_debug_event',
        'free_dll', 'free_idcv', 'free_loaders_list', 'free_regarg',
        'free_regvar', 'free_til', 'func_added', 'func_deleted',
        'func_does_return', 'func_has_stkframe_hole',
        'func_item_iterator_decode_preceding_insn',
        'func_item_iterator_decode_prev_insn', 'func_item_iterator_next',
        'func_item_iterator_prev', 'func_item_iterator_succ',
        'func_noret_changed', 'func_parent_iterator_set',
        'func_tail_appended', 'func_tail_deleted',
        'func_tail_iterator_set', 'func_tail_iterator_set_ea',
        'func_updated', 'funcargvec_t', 'fwritebytes', 'gdecode_t',
        'gen_complex_call_chart', 'gen_decorate_name', 'gen_exe_file',
        'gen_file', 'gen_fix_fixups', 'gen_flow_graph', 'gen_gdl',
        'gen_rand_buf', 'gen_simple_call_chart', 'gen_use_arg_tinfos',
        'gen_use_arg_tinfos2', 'generate_disasm_line',
        'generate_disassembly', 'get_16bit', 'get_32bit', 'get_64bit',
        'get_8bit', 'get_abi_name', 'get_aflags', 'get_alias_target',
        'get_arg_addrs', 'get_array_parameters', 'get_ash',
        'get_auto_display', 'get_auto_state', 'get_basic_file_type',
        'get_best_fit_member', 'get_bmask_cmt', 'get_bmask_name',
        'get_byte', 'get_bytes', 'get_cmt', 'get_compiler_abbr',
        'get_compiler_name', 'get_compilers', 'get_cp_validity',
        'get_current_extlang', 'get_current_idasgn',
        'get_custom_data_format', 'get_custom_data_formats',
        'get_custom_data_type', 'get_custom_data_type_ids',
        'get_custom_data_types', 'get_custom_refinfo', 'get_data_elsize',
        'get_data_value', 'get_db_byte', 'get_dbctx_id', 'get_dbctx_qty',
        'get_dbg_byte', 'get_debug_name', 'get_debug_name_ea',
        'get_debug_names', 'get_debugger_plugins',
        'get_default_encoding_idx', 'get_default_radix',
        'get_default_reftype', 'get_dirty_infos', 'get_dtype_by_size',
        'get_dtype_flag', 'get_dtype_size', 'get_dword', 'get_ea_name',
        'get_effective_spd', 'get_elf_debug_file_directory',
        'get_encoding_bpu', 'get_encoding_bpu_by_name',
        'get_encoding_name', 'get_encoding_qty', 'get_entry',
        'get_entry_forwarder', 'get_entry_name', 'get_entry_ordinal',
        'get_entry_qty', 'get_enum', 'get_enum_cmt', 'get_enum_flag',
        'get_enum_id', 'get_enum_idx', 'get_enum_member',
        'get_enum_member_bmask', 'get_enum_member_by_name',
        'get_enum_member_cmt', 'get_enum_member_enum',
        'get_enum_member_expr', 'get_enum_member_name',
        'get_enum_member_serial', 'get_enum_member_value',
        'get_enum_name', 'get_enum_name2', 'get_enum_qty',
        'get_enum_size', 'get_enum_type_ordinal', 'get_enum_width',
        'get_errdesc', 'get_error_data', 'get_error_string',
        'get_extra_cmt', 'get_fchunk', 'get_fchunk_num', 'get_fchunk_qty',
        'get_file_ext', 'get_file_type_name', 'get_fileregion_ea',
        'get_fileregion_offset', 'get_first_bmask', 'get_first_cref_from',
        'get_first_cref_to', 'get_first_dref_from', 'get_first_dref_to',
        'get_first_enum_member', 'get_first_fcref_from',
        'get_first_fcref_to', 'get_first_fixup_ea',
        'get_first_free_extra_cmtidx', 'get_first_hidden_range',
        'get_first_seg', 'get_first_serial_enum_member',
        'get_first_struc_idx', 'get_fixup', 'get_fixup_desc',
        'get_fixup_handler', 'get_fixup_value', 'get_fixups',
        'get_flags_by_size', 'get_flags_ex', 'get_forced_operand',
        'get_fpvalue_kind', 'get_frame', 'get_frame_part',
        'get_frame_retsize', 'get_frame_size', 'get_free_disk_space',
        'get_func', 'get_func_bitness', 'get_func_by_frame',
        'get_func_chunknum', 'get_func_cmt', 'get_func_name',
        'get_func_num', 'get_func_qty', 'get_func_ranges',
        'get_group_selector', 'get_hexdsp', 'get_hidden_range',
        'get_hidden_range_num', 'get_hidden_range_qty', 'get_ida_subdirs',
        'get_idainfo_by_type', 'get_idasgn_desc',
        'get_idasgn_header_by_short_name', 'get_idasgn_qty',
        'get_idasgn_title', 'get_idati', 'get_idc_filename',
        'get_idcv_attr', 'get_idcv_class_name', 'get_idcv_slice',
        'get_idp_descs', 'get_idp_name', 'get_immvals',
        'get_import_module_name', 'get_import_module_qty',
        'get_innermost_member', 'get_item_color', 'get_item_end',
        'get_item_flag', 'get_jtable_target', 'get_last_bmask',
        'get_last_enum_member', 'get_last_hidden_range',
        'get_last_pfxlen', 'get_last_seg', 'get_last_serial_enum_member',
        'get_last_struc_idx', 'get_loader_name',
        'get_loader_name_from_dll', 'get_lookback',
        'get_mangled_name_type', 'get_manual_insn', 'get_mapping',
        'get_mappings_qty', 'get_max_strlit_length', 'get_member',
        'get_member_by_fullname', 'get_member_by_id',
        'get_member_by_name', 'get_member_fullname', 'get_member_name',
        'get_member_struc', 'get_member_tinfo', 'get_min_spd_ea',
        'get_module_data', 'get_name_base_ea', 'get_name_color',
        'get_name_ea', 'get_name_expr', 'get_name_value',
        'get_named_type', 'get_next_bmask', 'get_next_cref_from',
        'get_next_cref_to', 'get_next_dref_from', 'get_next_dref_to',
        'get_next_enum_member', 'get_next_fchunk', 'get_next_fcref_from',
        'get_next_fcref_to', 'get_next_fixup_ea', 'get_next_func',
        'get_next_func_addr', 'get_next_hidden_range',
        'get_next_member_idx', 'get_next_seg',
        'get_next_serial_enum_member', 'get_next_struc_idx',
        'get_nice_colored_name', 'get_nlist_ea', 'get_nlist_idx',
        'get_nlist_name', 'get_nlist_size', 'get_node_info',
        'get_nsec_stamp', 'get_numbered_type', 'get_numbered_type_name',
        'get_octet', 'get_offset_expr', 'get_offset_expression',
        'get_op_tinfo', 'get_opinfo', 'get_or_guess_member_tinfo',
        'get_ordinal_from_idb_type', 'get_ordinal_qty',
        'get_original_byte', 'get_original_dword', 'get_original_qword',
        'get_original_word', 'get_outfile_encoding_idx', 'get_path',
        'get_ph', 'get_place_class', 'get_place_class_id',
        'get_plugin_options', 'get_plugins', 'get_predef_insn_cmt',
        'get_prev_bmask', 'get_prev_enum_member', 'get_prev_fchunk',
        'get_prev_fixup_ea', 'get_prev_func', 'get_prev_func_addr',
        'get_prev_hidden_range', 'get_prev_member_idx', 'get_prev_seg',
        'get_prev_serial_enum_member', 'get_prev_sreg_range',
        'get_problem', 'get_problem_desc', 'get_problem_name',
        'get_qerrno', 'get_qword', 'get_radix', 'get_refinfo',
        'get_refinfo_descs', 'get_reftype_by_size', 'get_reg_name',
        'get_root_filename', 'get_scalar_bt', 'get_segm_base',
        'get_segm_by_name', 'get_segm_by_sel', 'get_segm_class',
        'get_segm_name', 'get_segm_num', 'get_segm_para', 'get_segm_qty',
        'get_segment_alignment', 'get_segment_cmt',
        'get_segment_combination', 'get_segment_translations',
        'get_selector_qty', 'get_source_linnum', 'get_sourcefile',
        'get_sp_delta', 'get_spd', 'get_special_folder',
        'get_spoiled_reg', 'get_sptr', 'get_sreg', 'get_sreg_range',
        'get_sreg_range_num', 'get_sreg_ranges_qty', 'get_std_dirtree',
        'get_stkvar', 'get_stock_tinfo', 'get_str_type', 'get_strid',
        'get_strlist_item', 'get_strlist_options', 'get_strlist_qty',
        'get_strlit_contents', 'get_stroff_path', 'get_struc',
        'get_struc_by_idx', 'get_struc_first_offset', 'get_struc_id',
        'get_struc_idx', 'get_struc_last_offset', 'get_struc_name',
        'get_struc_next_offset', 'get_struc_prev_offset', 'get_struc_qty',
        'get_struc_size', 'get_struct_operand', 'get_switch_info',
        'get_tinfo', 'get_tinfo_attr', 'get_tinfo_attrs',
        'get_tinfo_details', 'get_tinfo_pdata', 'get_tinfo_property',
        'get_tinfo_size', 'get_tryblks', 'get_type_ordinal',
        'get_user_idadir', 'get_utf8_char', 'get_vftable_ea',
        'get_vftable_ordinal', 'get_wide_byte', 'get_wide_dword',
        'get_wide_word', 'get_word', 'get_xrefpos', 'get_zero_ranges',
        'getinf', 'getinf_buf', 'getinf_flag', 'getinf_str', 'getn_enum',
        'getn_fchunk', 'getn_func', 'getn_hidden_range', 'getn_selector',
        'getn_sreg_range', 'getnseg', 'getseg', 'getsysfile', 'git_edge',
        'git_elp', 'git_node', 'git_none', 'git_text', 'git_tool',
        'graph_id_t', 'graph_item_type_t', 'graph_notification_t',
        'graph_row_info_t', 'graph_viewer_t', 'grcode_attach_menu_item',
        'grcode_calculating_layout', 'grcode_center_on',
        'grcode_change_group_visibility', 'grcode_changed_graph',
        'grcode_clear', 'grcode_clicked', 'grcode_create_circle_layout',
        'grcode_create_digraph_layout', 'grcode_create_disasm_graph1',
        'grcode_create_disasm_graph2', 'grcode_create_graph_viewer',
        'grcode_create_group', 'grcode_create_mutable_graph',
        'grcode_create_tree_layout', 'grcode_create_user_graph_place',
        'grcode_creating_group', 'grcode_dblclicked',
        'grcode_del_custom_layout', 'grcode_del_node_info',
        'grcode_delete_group', 'grcode_delete_mutable_graph',
        'grcode_deleting_group', 'grcode_destroyed',
        'grcode_edge_infos_wrapper_clear',
        'grcode_edge_infos_wrapper_copy', 'grcode_empty',
        'grcode_find_subgraph_node', 'grcode_fit_window',
        'grcode_get_curnode', 'grcode_get_custom_layout',
        'grcode_get_gli', 'grcode_get_graph_groups',
        'grcode_get_graph_viewer', 'grcode_get_node_info',
        'grcode_get_node_representative', 'grcode_get_selection',
        'grcode_get_viewer_graph', 'grcode_gotfocus',
        'grcode_group_visibility', 'grcode_is_visible_node',
        'grcode_layout_calculated', 'grcode_lostfocus', 'grcode_node_qty',
        'grcode_nrect', 'grcode_refresh_viewer', 'grcode_reserved',
        'grcode_reserved2', 'grcode_set_custom_layout', 'grcode_set_edge',
        'grcode_set_gli', 'grcode_set_graph_groups',
        'grcode_set_node_info', 'grcode_set_titlebar_height',
        'grcode_set_viewer_graph', 'grcode_user_draw', 'grcode_user_hint',
        'grcode_user_refresh', 'grcode_user_size', 'grcode_user_text',
        'grcode_user_title', 'grcode_viewer_create_groups',
        'grcode_viewer_create_groups_vec', 'grcode_viewer_delete_groups',
        'grcode_viewer_delete_groups_vec',
        'grcode_viewer_groups_visibility',
        'grcode_viewer_groups_visibility_vec', 'groups_crinfos_t',
        'gtd_func_t', 'gtd_udt_t', 'gts_code_t', 'guess_func_cc',
        'guess_tinfo', 'h2ti', 'handle_fixups_in_macro',
        'has_external_refs', 'has_insn_feature', 'help_t', 'hexdsp_t',
        'hexplace_gen_t__byte_kind_t', 'hexplace_gen_t__data_kind_t',
        'hexplace_gen_t__int_format_t', 'hexplace_t__adjust',
        'hexplace_t__beginning', 'hexplace_t__clone',
        'hexplace_t__compare', 'hexplace_t__compare2',
        'hexplace_t__copyfrom', 'hexplace_t__deserialize',
        'hexplace_t__ea2str', 'hexplace_t__ending', 'hexplace_t__enter',
        'hexplace_t__generate', 'hexplace_t__id', 'hexplace_t__leave',
        'hexplace_t__makeplace', 'hexplace_t__name', 'hexplace_t__next',
        'hexplace_t__out_one_item', 'hexplace_t__prev',
        'hexplace_t__print', 'hexplace_t__rebase',
        'hexplace_t__serialize', 'hexplace_t__toea', 'hexplace_t__touval',
        'hide_name', 'hook_event_listener', 'hook_to_notification_point',
        'hook_type_t', 'ida_checkmem',
        'ida_syntax_highlighter_t__keywords_t',
        'ida_syntax_highlighter_t__multicmtvec_t', 'idadir',
        'idaplace_t__adjust', 'idaplace_t__beginning',
        'idaplace_t__clone', 'idaplace_t__compare',
        'idaplace_t__compare2', 'idaplace_t__copyfrom',
        'idaplace_t__deserialize', 'idaplace_t__ending',
        'idaplace_t__enter', 'idaplace_t__generate', 'idaplace_t__id',
        'idaplace_t__leave', 'idaplace_t__makeplace', 'idaplace_t__name',
        'idaplace_t__next', 'idaplace_t__prev', 'idaplace_t__print',
        'idaplace_t__rebase', 'idaplace_t__serialize', 'idaplace_t__toea',
        'idaplace_t__touval', 'idasgn_loaded', 'idastate_t',
        'idb_event__event_code_t', 'idb_utf8', 'idc_vars_t', 'idcv_float',
        'idcv_int64', 'idcv_long', 'idcv_num', 'idcv_object',
        'idcv_string', 'idp_descs_t', 'idp_names_t', 'ieee_realcvt',
        'iek_key_press', 'iek_key_release', 'iek_mouse_button_press',
        'iek_mouse_button_release', 'iek_mouse_wheel', 'iek_shortcut',
        'iek_unknown', 'if_hex', 'if_signed', 'if_unsigned',
        'ignore_name_def_t', 'import_module', 'import_type', 'inf',
        'inftag_t', 'init_database', 'init_plugins', 'inode_t',
        'inodevec_t', 'input_event_kind_t', 'input_event_modifiers_t',
        'insn_add_cref', 'insn_add_dref', 'insn_add_off_drefs',
        'insn_create_op_data', 'insn_create_stkvar',
        'install_custom_argloc', 'install_extlang',
        'install_user_defined_prefix', 'int16', 'int32', 'int64', 'int8',
        'internal_register_place_class', 'interr', 'interr_should_throw',
        'intvec_t', 'invalidate_dbgmem_config',
        'invalidate_dbgmem_contents', 'invoke_callbacks', 'invoke_plugin',
        'ioport_bits_t', 'ioports_t', 'is_align_insn',
        'is_attached_custom_data_format', 'is_auto_enabled',
        'is_basic_block_end', 'is_bf', 'is_bnot', 'is_call_insn',
        'is_char', 'is_control_tty', 'is_cp_graphical', 'is_custfmt',
        'is_database_ext', 'is_database_flag', 'is_debugger_memory',
        'is_debugger_on', 'is_defarg', 'is_ea_tryblks', 'is_enum',
        'is_enum_fromtil', 'is_enum_hidden', 'is_fltnum',
        'is_forced_operand', 'is_func_locked', 'is_ghost_enum',
        'is_ida_kernel', 'is_ident', 'is_in_nlist',
        'is_indirect_jump_insn', 'is_invsign', 'is_loaded', 'is_lzero',
        'is_main_thread', 'is_manual', 'is_manual_insn', 'is_mapped',
        'is_member_id', 'is_miniidb', 'is_name_defined_locally',
        'is_numop', 'is_numop0', 'is_numop1', 'is_off', 'is_ordinal_name',
        'is_pattern_t', 'is_problem_present', 'is_public_name',
        'is_refresh_requested', 'is_ret_insn', 'is_seg', 'is_segm_locked',
        'is_spec_ea', 'is_spec_segm', 'is_special_member', 'is_stkvar',
        'is_stroff', 'is_suspop', 'is_trusted_idb', 'is_uname',
        'is_valid_cp', 'is_valid_typename', 'is_valid_utf8',
        'is_varmember', 'is_varsize_item', 'is_weak_name',
        'item_color_changed', 'iterate_func_chunks', 'itext', 'jtype_t',
        'jump_pattern_t__check_insn_t', 'jvalue_t_clear', 'jvalue_t_copy',
        'jvalues_t', 'kernel_config_loaded', 'l_compare', 'l_compare2',
        'last_idcv_attr', 'launch_process', 'layout_type_t',
        'lcr_auto_switch', 'lcr_goto', 'lcr_internal', 'lcr_jump',
        'lcr_navigate', 'lcr_scroll', 'lcr_unknown', 'lcr_user_switch',
        'leading_zero_important', 'lecvt_code_t', 'lex_define_macro',
        'lex_get_file_line', 'lex_get_token', 'lex_get_token2',
        'lex_init_file', 'lex_init_string', 'lex_print_token',
        'lex_set_options', 'lex_term_file', 'lex_undefine_macro',
        'lexcompare_tinfo', 'line_rendering_output_entries_refs_t',
        'linearray_t_beginning', 'linearray_t_ctr', 'linearray_t_down',
        'linearray_t_dtr', 'linearray_t_ending', 'linearray_t_set_place',
        'linearray_t_up', 'linput_close_code_t', 'linput_janitor_t',
        'linput_type_t', 'llong_scan', 'load_binary_file',
        'load_core_module', 'load_dirtree', 'load_ids_module',
        'load_nonbinary_file', 'load_til', 'load_til_header',
        'loader_finished', 'local_types_changed', 'locchange_reason_t',
        'lochist_entry_t_deserialize', 'lochist_entry_t_serialize',
        'lochist_entry_vec_t', 'lochist_t_back', 'lochist_t_clear',
        'lochist_t_current_index', 'lochist_t_deregister_live',
        'lochist_t_fwd', 'lochist_t_get', 'lochist_t_get_current',
        'lochist_t_init', 'lochist_t_jump', 'lochist_t_register_live',
        'lochist_t_save', 'lochist_t_seek', 'lochist_t_set',
        'lochist_t_size', 'lock_dbgmem_config', 'lock_func_range',
        'lock_segm', 'log2ceil', 'log2floor', 'longlong',
        'lookup_loc_converter2', 'lowcnd_vec_t', 'lower_type', 'lread',
        'lreadbytes', 'lx_parse_cast_t', 'lx_resolver_t', 'lxtype',
        'make_code', 'make_data', 'make_linput', 'make_name_auto',
        'make_name_non_public', 'make_name_non_weak', 'make_name_public',
        'make_name_user', 'make_name_weak', 'mangled_name_type_t',
        'map_code_ea', 'mark_switch_insns_jpt', 'match_jpt', 'mbox_error',
        'mbox_feedback', 'mbox_filestruct', 'mbox_hide', 'mbox_info',
        'mbox_internal', 'mbox_kind_t', 'mbox_nomem', 'mbox_readerror',
        'mbox_replace', 'mbox_wait', 'mbox_warning', 'mbox_writeerror',
        'mem2base', 'meminfo_vec_t', 'memreg_infos_t', 'memrev',
        'modinfovec_t', 'movbpt_code_t', 'movbpt_codes_t',
        'movbpt_infos_t', 'move_idcv', 'move_segm', 'move_segm_start',
        'msg_activated', 'msg_click', 'msg_closed', 'msg_dblclick',
        'msg_deactivated', 'msg_keydown', 'msg_notification_t',
        'mutable_graph_t__node_layout_t', 'name_requires_qualifier',
        'nametype_t', 'nat_auto', 'nat_cod', 'nat_cur', 'nat_dat',
        'nat_err', 'nat_ext', 'nat_fun', 'nat_gap', 'nat_hlo', 'nat_last',
        'nat_lib', 'nat_lum', 'nat_und', 'navaddr_type_t', 'nbits',
        'netnode_altadjust', 'netnode_altadjust2', 'netnode_altshift',
        'netnode_altval', 'netnode_altval_idx8', 'netnode_blobsize',
        'netnode_charshift', 'netnode_charval', 'netnode_charval_idx8',
        'netnode_check', 'netnode_copy', 'netnode_delblob',
        'netnode_delvalue', 'netnode_end', 'netnode_exist',
        'netnode_get_name', 'netnode_getblob', 'netnode_hashdel',
        'netnode_hashfirst', 'netnode_hashlast', 'netnode_hashnext',
        'netnode_hashprev', 'netnode_hashset', 'netnode_hashstr',
        'netnode_hashval', 'netnode_hashval_long', 'netnode_inited',
        'netnode_is_available', 'netnode_kill', 'netnode_lower_bound',
        'netnode_lower_bound_idx8', 'netnode_next', 'netnode_prev',
        'netnode_qgetblob', 'netnode_qhashfirst', 'netnode_qhashlast',
        'netnode_qhashnext', 'netnode_qhashprev', 'netnode_qhashstr',
        'netnode_qsupstr', 'netnode_qsupstr_idx8', 'netnode_qvalstr',
        'netnode_rename', 'netnode_set', 'netnode_setblob',
        'netnode_start', 'netnode_supdel', 'netnode_supdel_all',
        'netnode_supdel_idx8', 'netnode_supdel_range',
        'netnode_supdel_range_idx8', 'netnode_supfirst',
        'netnode_supfirst_idx8', 'netnode_suplast',
        'netnode_suplast_idx8', 'netnode_supnext', 'netnode_supnext_idx8',
        'netnode_supprev', 'netnode_supprev_idx8', 'netnode_supset',
        'netnode_supset_idx8', 'netnode_supshift', 'netnode_supstr',
        'netnode_supstr_idx8', 'netnode_supval', 'netnode_supval_idx8',
        'netnode_valobj', 'netnode_valstr', 'new_til', 'next_addr',
        'next_chunk', 'next_head', 'next_idcv_attr', 'next_named_type',
        'next_not_tail', 'next_that', 'next_visea', 'node2ea',
        'node_iterator_goup', 'nodeidx_t', 'notify_dirtree', 'nr_none',
        'nr_once', 'num_flag', 'numop2str', 'ofile_type_t',
        'op_adds_xrefs', 'op_custfmt', 'op_dtype_t', 'op_enum',
        'op_offset', 'op_offset_ex', 'op_seg', 'op_stkvar', 'op_stroff',
        'op_ti_changed', 'op_type_changed', 'openM', 'openR', 'openRT',
        'open_linput', 'optimize_argloc', 'optype_t', 'ordvec_t',
        'p_list', 'p_string', 'pack_dd', 'pack_dq', 'pack_ds', 'pack_dw',
        'pack_idcobj_to_bv', 'pack_idcobj_to_idb', 'parse_binpat_str',
        'parse_command_line', 'parse_config_value', 'parse_dbgopts',
        'parse_decl', 'parse_decls', 'parse_json', 'parse_json_string',
        'parse_reg_name', 'patch_byte', 'patch_bytes', 'patch_dword',
        'patch_fixup_value', 'patch_qword', 'patch_word', 'path_type_t',
        'peek_auto_queue', 'ph', 'pid_t', 'plan_and_wait',
        'plan_to_apply_idasgn', 'pointvec_t', 'prev_addr', 'prev_chunk',
        'prev_head', 'prev_idcv_attr', 'prev_not_tail', 'prev_that',
        'prev_utf8_char', 'prev_visea', 'print_argloc', 'print_cdata',
        'print_charlit', 'print_decls', 'print_fpval', 'print_idcv',
        'print_insn_mnem', 'print_operand', 'print_strlit_type',
        'print_tinfo', 'print_type', 'printer_t', 'problist_id_t',
        'process_archive', 'process_zip_linput', 'process_zipfile',
        'process_zipfile_entry', 'processor_t__event_t', 'procinfo_vec_t',
        'put_byte', 'put_bytes', 'put_dbg_byte', 'put_dword', 'put_qword',
        'put_utf8_char', 'put_word', 'qaccess', 'qalloc',
        'qalloc_or_throw', 'qatexit', 'qbasename', 'qcalloc', 'qchdir',
        'qchsize', 'qcleanline', 'qclose', 'qcontrol_tty', 'qcopyfile',
        'qcreate', 'qctime', 'qctime_utc', 'qdetach_tty', 'qdirname',
        'qdup', 'qerrcode', 'qerrstr', 'qexit', 'qfclose', 'qfgetc',
        'qfgets', 'qfileexist', 'qfilelength', 'qfilesize', 'qfindclose',
        'qfindfirst', 'qfindnext', 'qflow_chart_t__blocks_t', 'qflush',
        'qfopen', 'qfputc', 'qfputs', 'qfread', 'qfree', 'qfseek',
        'qfsize', 'qfstat', 'qfsync', 'qftell', 'qfwrite', 'qgetcwd',
        'qgetenv', 'qgetline', 'qgets', 'qgmtime', 'qhandle_t',
        'qisabspath', 'qisdir', 'qlfile', 'qlgetc', 'qlgets', 'qlgetz',
        'qlocaltime', 'qlread', 'qlseek', 'qlsize', 'qmake_full_path',
        'qmakefile', 'qmakepath', 'qmkdir', 'qmove', 'qmutex_create',
        'qmutex_free', 'qmutex_lock', 'qmutex_t', 'qmutex_unlock',
        'qopen', 'qopen_shared', 'qpipe_close', 'qpipe_create',
        'qpipe_read', 'qpipe_write', 'qread', 'qrealloc',
        'qrealloc_or_throw', 'qregcomp', 'qregerror', 'qregexec',
        'qregfree', 'qrename', 'qrmdir', 'qseek', 'qsem_create',
        'qsem_free', 'qsem_post', 'qsem_wait', 'qsemaphore_t', 'qsetenv',
        'qsleep', 'qsnprintf', 'qsplitfile', 'qsscanf', 'qstat',
        'qstpncpy', 'qstr2user', 'qstrchr', 'qstrcmp', 'qstrdup',
        'qstrerror', 'qstrftime', 'qstrftime64', 'qstring', 'qstrlen',
        'qstrlwr', 'qstrncat', 'qstrncpy', 'qstrrchr', 'qstrtok',
        'qstrupr', 'qstrvec_t', 'qtell', 'qthread_create',
        'qthread_equal', 'qthread_free', 'qthread_join', 'qthread_kill',
        'qthread_same', 'qthread_self', 'qthread_t', 'qtime32_t',
        'qtime64', 'qtime64_t', 'qtimegm', 'qtimer_t', 'qtmpfile',
        'qtmpnam', 'qtype', 'qunlink', 'quote_cmdline_arg', 'qustrlen',
        'qustrncpy', 'qvector__qstring_char____const_iterator',
        'qvector__qstring_char____iterator',
        'qvector__qstring_unsigned_char____const_iterator',
        'qvector__qstring_unsigned_char____iterator',
        'qvector__qstring_wchar_t____const_iterator',
        'qvector__qstring_wchar_t____iterator',
        'qvector_argloc_t___const_iterator',
        'qvector_argloc_t___iterator',
        'qvector_argpart_t___const_iterator',
        'qvector_argpart_t___iterator',
        'qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R____const_iterator',
        'qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R____iterator',
        'qvector_bool___const_iterator', 'qvector_bool___iterator',
        'qvector_bpt_t__P___const_iterator',
        'qvector_bpt_t__P___iterator', 'qvector_bpt_t___const_iterator',
        'qvector_bpt_t___iterator', 'qvector_bptaddrs_t___const_iterator',
        'qvector_bptaddrs_t___iterator',
        'qvector_call_stack_info_t___const_iterator',
        'qvector_call_stack_info_t___iterator',
        'qvector_catch_t___const_iterator', 'qvector_catch_t___iterator',
        'qvector_cfgopt_set_t___const_iterator',
        'qvector_cfgopt_set_t___iterator',
        'qvector_channel_redir_t___const_iterator',
        'qvector_channel_redir_t___iterator',
        'qvector_char___const_iterator', 'qvector_char___iterator',
        'qvector_cliopt_t___const_iterator',
        'qvector_cliopt_t___iterator',
        'qvector_compiled_binpat_t___const_iterator',
        'qvector_compiled_binpat_t___iterator',
        'qvector_const_bpt_t__P___const_iterator',
        'qvector_const_bpt_t__P___iterator',
        'qvector_const_char__P___const_iterator',
        'qvector_const_char__P___iterator',
        'qvector_const_rangeset_t__P___const_iterator',
        'qvector_const_rangeset_t__P___iterator',
        'qvector_const_twinline_t__P___const_iterator',
        'qvector_const_twinline_t__P___iterator',
        'qvector_debug_event_t___const_iterator',
        'qvector_debug_event_t___iterator',
        'qvector_direntry_t___const_iterator',
        'qvector_direntry_t___iterator',
        'qvector_dirtree_cursor_t___const_iterator',
        'qvector_dirtree_cursor_t___iterator',
        'qvector_ea_name_t___const_iterator',
        'qvector_ea_name_t___iterator', 'qvector_edge_t___const_iterator',
        'qvector_edge_t___iterator',
        'qvector_enum_member_t___const_iterator',
        'qvector_enum_member_t___iterator',
        'qvector_exception_info_t___const_iterator',
        'qvector_exception_info_t___iterator',
        'qvector_extlang_t__P___const_iterator',
        'qvector_extlang_t__P___iterator',
        'qvector_fixup_info_t___const_iterator',
        'qvector_fixup_info_t___iterator',
        'qvector_funcarg_t___const_iterator',
        'qvector_funcarg_t___iterator',
        'qvector_group_crinfo_t___const_iterator',
        'qvector_group_crinfo_t___iterator',
        'qvector_ida_syntax_highlighter_t__keywords_style_t___const_iterator',
        'qvector_ida_syntax_highlighter_t__keywords_style_t___iterator',
        'qvector_ida_syntax_highlighter_t__multicmt_t___const_iterator',
        'qvector_ida_syntax_highlighter_t__multicmt_t___iterator',
        'qvector_ida_syntax_highlighter_t__plain_char_ptr_t___const_iterator',
        'qvector_ida_syntax_highlighter_t__plain_char_ptr_t___iterator',
        'qvector_idc_global_t___const_iterator',
        'qvector_idc_global_t___iterator',
        'qvector_idp_desc_t___const_iterator',
        'qvector_idp_desc_t___iterator',
        'qvector_idp_name_t___const_iterator',
        'qvector_idp_name_t___iterator', 'qvector_int___const_iterator',
        'qvector_int___iterator', 'qvector_intmap_t___const_iterator',
        'qvector_intmap_t___iterator',
        'qvector_ioport_bit_t___const_iterator',
        'qvector_ioport_bit_t___iterator',
        'qvector_ioport_t___const_iterator',
        'qvector_ioport_t___iterator',
        'qvector_jvalue_t___const_iterator',
        'qvector_jvalue_t___iterator', 'qvector_kvp_t___const_iterator',
        'qvector_kvp_t___iterator',
        'qvector_line_rendering_output_entry_t__P___const_iterator',
        'qvector_line_rendering_output_entry_t__P___iterator',
        'qvector_lochist_entry_t___const_iterator',
        'qvector_lochist_entry_t___iterator',
        'qvector_long_long___P__syntax_highlight_style__P__const_char__P____const_iterator',
        'qvector_long_long___P__syntax_highlight_style__P__const_char__P____iterator',
        'qvector_long_long___const_iterator',
        'qvector_long_long___iterator',
        'qvector_lowcnd_t___const_iterator',
        'qvector_lowcnd_t___iterator',
        'qvector_memory_info_t___const_iterator',
        'qvector_memory_info_t___iterator',
        'qvector_memreg_info_t___const_iterator',
        'qvector_memreg_info_t___iterator',
        'qvector_modinfo_t___const_iterator',
        'qvector_modinfo_t___iterator',
        'qvector_movbpt_code_t___const_iterator',
        'qvector_movbpt_code_t___iterator',
        'qvector_movbpt_info_t___const_iterator',
        'qvector_movbpt_info_t___iterator',
        'qvector_node_set_t___const_iterator',
        'qvector_node_set_t___iterator', 'qvector_op_t___const_iterator',
        'qvector_op_t___iterator', 'qvector_point_t___const_iterator',
        'qvector_point_t___iterator',
        'qvector_process_info_t___const_iterator',
        'qvector_process_info_t___iterator',
        'qvector_qbasic_block_t___const_iterator',
        'qvector_qbasic_block_t___iterator',
        'qvector_qrefcnt_t_source_item_t____const_iterator',
        'qvector_qrefcnt_t_source_item_t____iterator',
        'qvector_qvector_const_char__P____const_iterator',
        'qvector_qvector_const_char__P____iterator',
        'qvector_qvector_const_twinline_t__P____const_iterator',
        'qvector_qvector_const_twinline_t__P____iterator',
        'qvector_qvector_int____const_iterator',
        'qvector_qvector_int____iterator',
        'qvector_qvector_long_long____const_iterator',
        'qvector_qvector_long_long____iterator',
        'qvector_range_t___const_iterator', 'qvector_range_t___iterator',
        'qvector_rangeset_t___const_iterator',
        'qvector_rangeset_t___iterator',
        'qvector_rect_t___const_iterator', 'qvector_rect_t___iterator',
        'qvector_refinfo_desc_t___const_iterator',
        'qvector_refinfo_desc_t___iterator',
        'qvector_reg_access_t___const_iterator',
        'qvector_reg_access_t___iterator',
        'qvector_reg_info_t___const_iterator',
        'qvector_reg_info_t___iterator',
        'qvector_register_info_t___const_iterator',
        'qvector_register_info_t___iterator',
        'qvector_regobj_t___const_iterator',
        'qvector_regobj_t___iterator',
        'qvector_regval_t___const_iterator',
        'qvector_regval_t___iterator', 'qvector_reserve',
        'qvector_row_info_t___const_iterator',
        'qvector_row_info_t___iterator',
        'qvector_scattered_segm_t___const_iterator',
        'qvector_scattered_segm_t___iterator',
        'qvector_segm_move_info_t___const_iterator',
        'qvector_segm_move_info_t___iterator',
        'qvector_selection_item_t___const_iterator',
        'qvector_selection_item_t___iterator',
        'qvector_simd_info_t___const_iterator',
        'qvector_simd_info_t___iterator',
        'qvector_simpleline_t___const_iterator',
        'qvector_simpleline_t___iterator',
        'qvector_snapshot_t__P___const_iterator',
        'qvector_snapshot_t__P___iterator',
        'qvector_stkpnt_t___const_iterator',
        'qvector_stkpnt_t___iterator',
        'qvector_sync_source_t___const_iterator',
        'qvector_sync_source_t___iterator',
        'qvector_tev_info_reg_t___const_iterator',
        'qvector_tev_info_reg_t___iterator',
        'qvector_tev_info_t___const_iterator',
        'qvector_tev_info_t___iterator',
        'qvector_tev_reg_value_t___const_iterator',
        'qvector_tev_reg_value_t___iterator',
        'qvector_thread_name_t___const_iterator',
        'qvector_thread_name_t___iterator',
        'qvector_tinfo_t___const_iterator', 'qvector_tinfo_t___iterator',
        'qvector_token_t___const_iterator', 'qvector_token_t___iterator',
        'qvector_tryblk_t___const_iterator',
        'qvector_tryblk_t___iterator',
        'qvector_twinline_t___const_iterator',
        'qvector_twinline_t___iterator',
        'qvector_type_attr_t___const_iterator',
        'qvector_type_attr_t___iterator',
        'qvector_udt_member_t___const_iterator',
        'qvector_udt_member_t___iterator',
        'qvector_unsigned_char___const_iterator',
        'qvector_unsigned_char___iterator',
        'qvector_unsigned_int___const_iterator',
        'qvector_unsigned_int___iterator',
        'qvector_unsigned_long_long___const_iterator',
        'qvector_unsigned_long_long___iterator',
        'qvector_update_bpt_info_t___const_iterator',
        'qvector_update_bpt_info_t___iterator',
        'qvector_valstr_t___const_iterator',
        'qvector_valstr_t___iterator', 'qvector_wchar_t___const_iterator',
        'qvector_wchar_t___iterator',
        'qvector_xreflist_entry_t___const_iterator',
        'qvector_xreflist_entry_t___iterator', 'qveprintf', 'qvfprintf',
        'qvfscanf', 'qvprintf', 'qvsnprintf', 'qvsscanf',
        'qwait_for_handles', 'qwait_timed', 'qwrite', 'qwstring',
        'qwstrvec_t', 'r50_to_asc', 'range_cmt_changed', 'range_kind_t',
        'range_t_print', 'rangeset_crefvec_t',
        'rangeset_t__const_iterator', 'rangeset_t__iterator',
        'rangeset_t_add', 'rangeset_t_add2', 'rangeset_t_contains',
        'rangeset_t_find_range', 'rangeset_t_has_common',
        'rangeset_t_has_common2', 'rangeset_t_intersect',
        'rangeset_t_lower_bound', 'rangeset_t_next_addr',
        'rangeset_t_next_range', 'rangeset_t_prev_addr',
        'rangeset_t_prev_range', 'rangeset_t_print', 'rangeset_t_sub',
        'rangeset_t_sub2', 'rangeset_t_swap', 'rangeset_t_upper_bound',
        'rangevec_base_t', 'read2bytes', 'read_config', 'read_config2',
        'read_ioports', 'read_ioports2', 'read_regargs',
        'read_struc_path', 'read_tinfo_bitfield_value', 'readbytes',
        'realtoasc', 'reanalyze_callers', 'reanalyze_function',
        'reanalyze_noret_flag', 'rebase_program', 'rebuild_nlist',
        'recalc_spd', 'refinfo_desc_vec_t', 'reftype_t',
        'reg_access_vec_t', 'reg_bin_op', 'reg_binary', 'reg_data_type',
        'reg_delete', 'reg_delete_subkey', 'reg_delete_tree', 'reg_dword',
        'reg_exists', 'reg_flush', 'reg_int_op', 'reg_load',
        'reg_read_strlist', 'reg_str_get', 'reg_str_set',
        'reg_subkey_children', 'reg_subkey_exists', 'reg_sz',
        'reg_unknown', 'reg_update_strlist', 'regcomp', 'regerror',
        'regex_cache_t__regex_cache_map_t', 'regex_match', 'regex_ptr_t',
        'regexec', 'regfree', 'reginfovec_t', 'register_class_t',
        'register_custom_data_format', 'register_custom_data_type',
        'register_custom_fixup', 'register_custom_refinfo',
        'register_info_vec_t', 'register_loc_converter2',
        'register_post_event_visitor', 'regobjvec_t', 'regoff_t',
        'regval_type_t', 'regvals_t', 'reload_file', 'reloc_value',
        'relocate_relobj', 'remember_problem', 'remove_abi_opts',
        'remove_custom_argloc', 'remove_event_listener', 'remove_extlang',
        'remove_func_tail', 'remove_tinfo_pointer', 'rename_encoding',
        'rename_entry', 'rename_regvar', 'renamed', 'renaming_enum',
        'renaming_struc', 'renaming_struc_member',
        'renderer_info_t__pos_t', 'reorder_dummy_names',
        'replace_ordinal_typerefs', 'replace_tabs', 'request_refresh',
        'resolve_typedef', 'resume_mode_t', 'retrieve_custom_argloc',
        'revert_byte', 'revert_ida_decisions', 'root_node', 'rotate_left',
        'round_down_power2', 'round_up_power2', 'run_plugin',
        'same_value_jpt', 'sanitize_file_name', 'save_database',
        'save_dirtree', 'save_reg_values_t', 'save_struc', 'save_tinfo',
        'savebase', 'sc_auto', 'sc_ext', 'sc_friend', 'sc_reg', 'sc_stat',
        'sc_type', 'sc_unk', 'sc_virt', 'scattered_image_t', 'sclass_t',
        'score_tinfo', 'screen_graph_selection_base_t', 'search',
        'search_path', 'section_lines_refs_t', 'sections_lines_refs_t',
        'segm_added', 'segm_adjust_diff', 'segm_adjust_ea',
        'segm_attrs_updated', 'segm_class_changed', 'segm_deleted',
        'segm_end_changed', 'segm_move_info_vec_t', 'segm_moved',
        'segm_name_changed', 'segm_start_changed', 'segtype', 'sel2para',
        'sel_t', 'select_extlang', 'serialize_dynamic_register_set',
        'serialize_json', 'serialize_tinfo', 'set_abits', 'set_aflags',
        'set_array_parameters', 'set_auto_state', 'set_bmask_cmt',
        'set_bmask_name', 'set_cmt', 'set_compiler',
        'set_compiler_string', 'set_cp_validity',
        'set_custom_data_type_ids', 'set_database_flag',
        'set_dbgmem_source', 'set_debug_event_code', 'set_debug_name',
        'set_debug_names', 'set_default_dataseg',
        'set_default_encoding_idx', 'set_default_sreg_value',
        'set_dummy_name', 'set_entry_forwarder', 'set_enum_bf',
        'set_enum_cmt', 'set_enum_flag', 'set_enum_fromtil',
        'set_enum_ghost', 'set_enum_hidden', 'set_enum_idx',
        'set_enum_member_name', 'set_enum_name', 'set_enum_type_ordinal',
        'set_enum_width', 'set_error_data', 'set_error_string',
        'set_file_ext', 'set_fixup', 'set_forced_operand',
        'set_frame_size', 'set_func_cmt', 'set_func_end',
        'set_func_name_if_jumpfunc', 'set_func_start',
        'set_group_selector', 'set_header_path', 'set_hexdsp',
        'set_ida_state', 'set_idc_dtor', 'set_idc_getattr',
        'set_idc_method', 'set_idc_setattr', 'set_idcv_attr',
        'set_idcv_slice', 'set_immd', 'set_import_name',
        'set_import_ordinal', 'set_item_color', 'set_lzero',
        'set_manual_insn', 'set_member_cmt', 'set_member_name',
        'set_member_tinfo', 'set_member_type', 'set_module_data',
        'set_moved_jpt', 'set_name', 'set_node_info', 'set_noret_insn',
        'set_notcode', 'set_numbered_type', 'set_op_tinfo', 'set_op_type',
        'set_opinfo', 'set_outfile_encoding_idx', 'set_path',
        'set_processor_type', 'set_purged', 'set_qerrno', 'set_refinfo',
        'set_refinfo_ex', 'set_regvar_cmt', 'set_segm_addressing',
        'set_segm_base', 'set_segm_class', 'set_segm_end',
        'set_segm_name', 'set_segm_start', 'set_segment_cmt',
        'set_segment_translations', 'set_selector', 'set_source_linnum',
        'set_sreg_at_next_code', 'set_str_type', 'set_struc_align',
        'set_struc_cmt', 'set_struc_hidden', 'set_struc_idx',
        'set_struc_listed', 'set_struc_name', 'set_switch_info',
        'set_tail_owner', 'set_target_assembler', 'set_tinfo',
        'set_tinfo_attr', 'set_tinfo_attrs', 'set_tinfo_property',
        'set_type_alias', 'set_user_defined_prefix', 'set_vftable_ea',
        'set_visible_func', 'set_visible_segm', 'set_xrefpos', 'setinf',
        'setinf_buf', 'setinf_flag', 'setproc_level_t',
        'setup_graph_subsystem', 'setup_lowcnd_regfuncs',
        'setup_selector', 'sgr_changed', 'sgr_deleted', 'show_auto',
        'show_name', 'simd_info_vec_t', 'simpleline_place_t__adjust',
        'simpleline_place_t__beginning', 'simpleline_place_t__clone',
        'simpleline_place_t__compare', 'simpleline_place_t__compare2',
        'simpleline_place_t__copyfrom', 'simpleline_place_t__deserialize',
        'simpleline_place_t__ending', 'simpleline_place_t__enter',
        'simpleline_place_t__generate', 'simpleline_place_t__id',
        'simpleline_place_t__leave', 'simpleline_place_t__makeplace',
        'simpleline_place_t__name', 'simpleline_place_t__next',
        'simpleline_place_t__prev', 'simpleline_place_t__print',
        'simpleline_place_t__rebase', 'simpleline_place_t__serialize',
        'simpleline_place_t__toea', 'simpleline_place_t__touval', 'sint8',
        'size_t', 'sizevec_t', 'skip_spaces', 'skip_utf8', 'smt_code_t',
        'snapshots_t', 'sort_til', 'source_file_iterator',
        'source_file_ptr', 'source_item_iterator', 'source_item_ptr',
        'source_items_t', 'split_sreg_range', 'src_item_kind_t',
        'ssize_t',
        'std___Default_allocator_traits_std__allocator_int____size_type',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_int__void__P_____pointer',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_int__void__P_____value_type',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_____pointer',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_____value_type',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_int__int___void__P_____pointer',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_int__int___void__P_____value_type',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_____pointer',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_____value_type',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_____pointer',
        'std___Default_allocator_traits_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_____value_type',
        'std___Default_allocator_traits_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______size_type',
        'std___Default_allocator_traits_std__allocator_std__pair_const_int__int_____size_type',
        'std___Default_allocator_traits_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____size_type',
        'std___Default_allocator_traits_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long_____size_type',
        'std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____',
        'std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'std___Iter_diff_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'std___Iter_diff_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____',
        'std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'std___Iter_ref_t_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'std___Iter_ref_t_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______pointer',
        'std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer',
        'std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer',
        'std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer',
        'std___Iterator_traits_base_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer',
        'std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer',
        'std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer',
        'std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer',
        'std___Iterator_traits_base_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer',
        'std___Rebind_pointer_t_void__P__std___Tree_node_int__void__P__',
        'std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P__',
        'std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_int__int___void__P__',
        'std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P__',
        'std___Rebind_pointer_t_void__P__std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P__',
        'std___Simple_types_int___const_pointer',
        'std___Simple_types_int___size_type',
        'std___Simple_types_int___value_type',
        'std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____const_pointer',
        'std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____pointer',
        'std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____size_type',
        'std___Simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____value_type',
        'std___Simple_types_std__pair_const_int__int____const_pointer',
        'std___Simple_types_std__pair_const_int__int____pointer',
        'std___Simple_types_std__pair_const_int__int____size_type',
        'std___Simple_types_std__pair_const_int__int____value_type',
        'std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____const_pointer',
        'std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____pointer',
        'std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____size_type',
        'std___Simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____value_type',
        'std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____const_pointer',
        'std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____pointer',
        'std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____size_type',
        'std___Simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____value_type',
        'std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___allocator_type',
        'std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___key_compare',
        'std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___key_type',
        'std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___value_type',
        'std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___allocator_type',
        'std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___key_compare',
        'std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___key_type',
        'std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___value_type',
        'std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___allocator_type',
        'std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___key_compare',
        'std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___key_type',
        'std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___value_type',
        'std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___allocator_type',
        'std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___key_compare',
        'std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___key_type',
        'std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___value_type',
        'std___Tree_child',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____pointer',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____reference',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____value_type',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference',
        'std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference',
        'std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type',
        'std___Tree_node_int__void__P____Nodeptr',
        'std___Tree_node_int__void__P___value_type',
        'std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____Nodeptr',
        'std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___value_type',
        'std___Tree_node_std__pair_const_int__int___void__P____Nodeptr',
        'std___Tree_node_std__pair_const_int__int___void__P___value_type',
        'std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____Nodeptr',
        'std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___value_type',
        'std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____Nodeptr',
        'std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___value_type',
        'std___Tree_simple_types_int____Node',
        'std___Tree_simple_types_int____Nodeptr',
        'std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______Node',
        'std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______Nodeptr',
        'std___Tree_simple_types_std__pair_const_int__int_____Node',
        'std___Tree_simple_types_std__pair_const_int__int_____Nodeptr',
        'std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____Node',
        'std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____Nodeptr',
        'std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____Node',
        'std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____Nodeptr',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Alnode',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Nodeptr',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Scary_val',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Unchecked_const_iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false_____Unchecked_iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____allocator_type',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____const_iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____const_reverse_iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____key_compare',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____key_type',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____reverse_iterator',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____size_type',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____value_compare',
        'std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false____value_type',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Alnode',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Nodeptr',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Scary_val',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Unchecked_const_iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false_____Unchecked_iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____allocator_type',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____const_iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____const_reverse_iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____key_compare',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____key_type',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____reverse_iterator',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____size_type',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____value_compare',
        'std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false____value_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Alnode',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Nodeptr',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Scary_val',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Unchecked_const_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false_____Unchecked_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____allocator_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____const_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____const_reverse_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____key_compare',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____key_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____reverse_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____size_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____value_compare',
        'std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false____value_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Alnode',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Nodeptr',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Scary_val',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Unchecked_const_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false_____Unchecked_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____allocator_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____const_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____const_reverse_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____key_compare',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____key_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____reverse_iterator',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____size_type',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____value_compare',
        'std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false____value_type',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Alnode',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Nodeptr',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Scary_val',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Unchecked_const_iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false_____Unchecked_iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____allocator_type',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____const_iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____const_reverse_iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____key_compare',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____key_type',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____reverse_iterator',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____size_type',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____value_compare',
        'std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false____value_type',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int______Nodeptr',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____pointer',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____reference',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int_____value_type',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________Nodeptr',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______Nodeptr',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______Nodeptr',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______Nodeptr',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference',
        'std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______pointer',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______reference',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______value_type',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______pointer',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______reference',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______value_type',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______pointer',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______reference',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______value_type',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______pointer',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______reference',
        'std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______value_type',
        'std___Tree_val_std___Tree_simple_types_int_____Nodeptr',
        'std___Tree_val_std___Tree_simple_types_int_____Unchecked_const_iterator',
        'std___Tree_val_std___Tree_simple_types_int____const_pointer',
        'std___Tree_val_std___Tree_simple_types_int____size_type',
        'std___Tree_val_std___Tree_simple_types_int____value_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______Nodeptr',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______Unchecked_const_iterator',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______const_pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______size_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______value_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______Nodeptr',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______Unchecked_const_iterator',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____const_pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____size_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____value_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______Nodeptr',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______Unchecked_const_iterator',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____const_pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____size_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____value_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______Nodeptr',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______Unchecked_const_iterator',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____const_pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____pointer',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____size_type',
        'std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____value_type',
        'std___Tset_traits_int__std__less_int___std__allocator_int___false___allocator_type',
        'std___Tset_traits_int__std__less_int___std__allocator_int___false___key_compare',
        'std___Tset_traits_int__std__less_int___std__allocator_int___false___key_type',
        'std___Tset_traits_int__std__less_int___std__allocator_int___false___value_compare',
        'std___Tset_traits_int__std__less_int___std__allocator_int___false___value_type',
        'std__allocator_std___Tree_node_int__void__P____value_type',
        'std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____value_type',
        'std__allocator_std___Tree_node_std__pair_const_int__int___void__P____value_type',
        'std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____value_type',
        'std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____value_type',
        'std__map__qstring_char___qrefcnt_t_refcnted_regex_t____allocator_type',
        'std__map__qstring_char___qrefcnt_t_refcnted_regex_t____key_compare',
        'std__map__qstring_char___qrefcnt_t_refcnted_regex_t____key_type',
        'std__map__qstring_char___qrefcnt_t_refcnted_regex_t____mapped_type',
        'std__map_int__int___allocator_type',
        'std__map_int__int___key_compare', 'std__map_int__int___key_type',
        'std__map_int__int___mapped_type',
        'std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___allocator_type',
        'std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___key_compare',
        'std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___key_type',
        'std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___mapped_type',
        'std__map_unsigned_long_long__unsigned_long_long___allocator_type',
        'std__map_unsigned_long_long__unsigned_long_long___key_compare',
        'std__map_unsigned_long_long__unsigned_long_long___key_type',
        'std__map_unsigned_long_long__unsigned_long_long___mapped_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______difference_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______pointer',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int______reference',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________difference_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________reference',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______difference_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______reference',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______difference_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______reference',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______difference_type',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer',
        'std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______reference',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________difference_type',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________pointer',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t________reference',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______difference_type',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______pointer',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_______reference',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______difference_type',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______pointer',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_______reference',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______difference_type',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______pointer',
        'std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_______reference',
        'std__set_int___allocator_type', 'std__set_int___key_compare',
        'std_out_segm_footer', 'stkpnts_changed', 'stoa',
        'stock_type_id_t', 'storage_type_t', 'store_til', 'str2ea',
        'str2ea_ex', 'str2reg', 'str2user', 'strarray', 'stristr',
        'strrpl', 'struc_align_changed', 'struc_cmt_changed',
        'struc_created', 'struc_deleted', 'struc_error_t',
        'struc_expanded', 'struc_member_changed', 'struc_member_created',
        'struc_member_deleted', 'struc_member_renamed', 'struc_renamed',
        'struct_MD5Context', 'struct_TPointDouble', 'struct_TPopupMenu',
        'struct_TWidget', 'struct__0B605D7B00AC5C12C153272CF5BD15AF',
        'struct__37EC8ECBAB39934116D1B12D6D12C693',
        'struct__C21FB2E1BAA97F44BFD298211C4C916B',
        'struct__EBE02DBEC342F8268AFE19180D75885B', 'struct___qmutex_t',
        'struct___qsemaphore_t', 'struct___qthread_t',
        'struct___qtimer_t', 'struct__iobuf', 'struct__qstring_char_',
        'struct__qstring_unsigned_char_', 'struct__qstring_wchar_t_',
        'struct_abstract_graph_t', 'struct_abstract_graph_t_vtbl',
        'struct_action_ctx_base_cur_sel_t', 'struct_action_ctx_base_t',
        'struct_action_desc_t', 'struct_action_handler_t',
        'struct_action_handler_t_vtbl', 'struct_addon_info_t',
        'struct_aloc_visitor_t', 'struct_aloc_visitor_t_vtbl',
        'struct_altadjust_visitor_t', 'struct_altadjust_visitor_t_vtbl',
        'struct_argloc_t', 'struct_argpart_t', 'struct_argtinfo_helper_t',
        'struct_argtinfo_helper_t_vtbl', 'struct_array_parameters_t',
        'struct_array_type_data_t', 'struct_asm_t',
        'struct_auto_display_t',
        'struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t_',
        'struct_backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t',
        'struct_bitfield_type_data_t', 'struct_bitrange_t',
        'struct_bookmarks_t', 'struct_bpt_location_t', 'struct_bpt_t',
        'struct_bpt_visitor_t', 'struct_bpt_visitor_t_vtbl',
        'struct_bptaddr_t', 'struct_bptaddrs_t', 'struct_bytes_t',
        'struct_bytevec_t', 'struct_call_stack_info_t',
        'struct_call_stack_t', 'struct_callregs_t',
        'struct_cancellable_graph_t', 'struct_cancellable_graph_t_vtbl',
        'struct_cast_t', 'struct_catch_t', 'struct_cfgopt_set_t',
        'struct_cfgopt_set_vec_t', 'struct_cfgopt_t',
        'struct_cfgopt_t__num_range_t', 'struct_cfgopt_t__params_t',
        'struct_channel_redir_t', 'struct_choose_ioport_parser_t',
        'struct_choose_ioport_parser_t_vtbl', 'struct_chooser_base_t',
        'struct_chooser_base_t_vtbl', 'struct_chooser_item_attrs_t',
        'struct_chooser_multi_t', 'struct_chooser_multi_t_vtbl',
        'struct_chooser_t', 'struct_chooser_t__cbret_t',
        'struct_chooser_t_vtbl', 'struct_cli_t', 'struct_cliopt_t',
        'struct_cliopts_t', 'struct_compiled_binpat_t',
        'struct_compiler_info_t', 'struct_const_aloc_visitor_t',
        'struct_const_aloc_visitor_t_vtbl', 'struct_custloc_desc_t',
        'struct_custom_data_type_ids_t',
        'struct_custom_refinfo_handler_t',
        'struct_custom_viewer_handlers_t', 'struct_data_format_t',
        'struct_data_type_t', 'struct_dbctx_t', 'struct_dbg_info_t',
        'struct_debapp_attrs_t', 'struct_debug_event_t',
        'struct_debugger_t', 'struct_depth_first_info_t',
        'struct_destset_t', 'struct_direntry_t', 'struct_dirspec_t',
        'struct_dirspec_t_vtbl', 'struct_dirtree_cursor_t',
        'struct_dirtree_impl_t', 'struct_dirtree_iterator_t',
        'struct_dirtree_selection_t', 'struct_dirtree_t',
        'struct_dirtree_visitor_t', 'struct_dirtree_visitor_t_vtbl',
        'struct_dynamic_register_set_t', 'struct_ea_name_t',
        'struct_edge_info_t', 'struct_edge_infos_t',
        'struct_edge_infos_wrapper_t', 'struct_edge_layout_point_t',
        'struct_edge_segment_t', 'struct_edge_segs_vec_t',
        'struct_edge_t', 'struct_edge_typer_t', 'struct_edgeset_t',
        'struct_elf_loader_t', 'struct_encoder_t',
        'struct_encoder_t_vtbl', 'struct_enum_const_t',
        'struct_enum_member_t', 'struct_enum_member_visitor_t',
        'struct_enum_member_visitor_t_vtbl', 'struct_enum_type_data_t',
        'struct_enumplace_t', 'struct_enumplace_t_vtbl',
        'struct_eval_ctx_t', 'struct_event_listener_t',
        'struct_event_listener_t_vtbl', 'struct_exception_info_t',
        'struct_excinfo_t', 'struct_exec_request_t',
        'struct_exec_request_t_vtbl', 'struct_exehdr',
        'struct_exehdr_full', 'struct_expanded_area_t',
        'struct_ext_idcfunc_t', 'struct_extlang_t',
        'struct_extlang_visitor_t', 'struct_extlang_visitor_t_vtbl',
        'struct_file_enumerator_t', 'struct_file_enumerator_t_vtbl',
        'struct_fixup_data_t', 'struct_fixup_handler_t',
        'struct_fixup_info_t', 'struct_form_actions_t',
        'struct_form_actions_t_vtbl', 'struct_format_data_info_t',
        'struct_fpvalue_t', 'struct_func_item_iterator_t',
        'struct_func_parent_iterator_t', 'struct_func_t',
        'struct_func_t_0_0', 'struct_func_t_0_1',
        'struct_func_t___C940058B2272AD9112E2141245617273_0',
        'struct_func_t___C940058B2272AD9112E2141245617273_1',
        'struct_func_tail_iterator_t', 'struct_func_type_data_t',
        'struct_funcarg_t', 'struct_gdl_graph_t',
        'struct_gdl_graph_t_vtbl', 'struct_generic_linput_t',
        'struct_generic_linput_t_vtbl', 'struct_getname_info_t',
        'struct_graph_item_t', 'struct_graph_location_info_t',
        'struct_graph_node_visitor_t', 'struct_graph_node_visitor_t_vtbl',
        'struct_graph_path_visitor_t', 'struct_graph_path_visitor_t_vtbl',
        'struct_graph_visitor_t', 'struct_graph_visitor_t_vtbl',
        'struct_group_crinfo_t', 'struct_hexplace_gen_t',
        'struct_hexplace_gen_t_vtbl', 'struct_hexplace_t',
        'struct_hexplace_t_vtbl', 'struct_hexview_t',
        'struct_hidden_range_t', 'struct_highlighter_cbs_t',
        'struct_highlighter_cbs_t_vtbl', 'struct_ida_lowertype_helper_t',
        'struct_ida_lowertype_helper_t_vtbl',
        'struct_ida_movable_type_argloc_t_',
        'struct_ida_movable_type_argpart_t_',
        'struct_ida_movable_type_array_type_data_t_',
        'struct_ida_movable_type_bitfield_type_data_t_',
        'struct_ida_movable_type_bpt_location_t_',
        'struct_ida_movable_type_bpt_t_',
        'struct_ida_movable_type_call_stack_info_t_',
        'struct_ida_movable_type_catch_t_',
        'struct_ida_movable_type_cliopt_t_',
        'struct_ida_movable_type_compiled_binpat_t_',
        'struct_ida_movable_type_dbg_info_t_',
        'struct_ida_movable_type_debug_event_t_',
        'struct_ida_movable_type_direntry_t_',
        'struct_ida_movable_type_dirtree_cursor_t_',
        'struct_ida_movable_type_ea_name_t_',
        'struct_ida_movable_type_edge_t_',
        'struct_ida_movable_type_enum_member_t_',
        'struct_ida_movable_type_enum_type_data_t_',
        'struct_ida_movable_type_exception_info_t_',
        'struct_ida_movable_type_fixup_info_t_',
        'struct_ida_movable_type_func_t_',
        'struct_ida_movable_type_funcarg_t_',
        'struct_ida_movable_type_idc_global_t_',
        'struct_ida_movable_type_idc_value_t_',
        'struct_ida_movable_type_idp_desc_t_',
        'struct_ida_movable_type_idp_name_t_',
        'struct_ida_movable_type_ioport_bit_t_',
        'struct_ida_movable_type_ioport_t_',
        'struct_ida_movable_type_jarr_t_',
        'struct_ida_movable_type_jobj_t_',
        'struct_ida_movable_type_jvalue_t_',
        'struct_ida_movable_type_kvp_t_',
        'struct_ida_movable_type_line_rendering_output_entry_t_',
        'struct_ida_movable_type_load_info_t_',
        'struct_ida_movable_type_locchange_md_t_',
        'struct_ida_movable_type_lochist_entry_t_',
        'struct_ida_movable_type_lochist_t_',
        'struct_ida_movable_type_memory_info_t_',
        'struct_ida_movable_type_memreg_info_t_',
        'struct_ida_movable_type_modinfo_t_',
        'struct_ida_movable_type_movbpt_info_t_',
        'struct_ida_movable_type_point_t_',
        'struct_ida_movable_type_process_info_t_',
        'struct_ida_movable_type_ptr_type_data_t_',
        'struct_ida_movable_type_range_t_',
        'struct_ida_movable_type_rangeset_t_',
        'struct_ida_movable_type_rect_t_',
        'struct_ida_movable_type_refinfo_desc_t_',
        'struct_ida_movable_type_reg_access_t_',
        'struct_ida_movable_type_reg_info_t_',
        'struct_ida_movable_type_regarg_t_',
        'struct_ida_movable_type_register_info_t_',
        'struct_ida_movable_type_regobj_t_',
        'struct_ida_movable_type_regval_t_',
        'struct_ida_movable_type_regvar_t_',
        'struct_ida_movable_type_scattered_aloc_t_',
        'struct_ida_movable_type_scattered_segm_t_',
        'struct_ida_movable_type_segm_move_info_t_',
        'struct_ida_movable_type_seh_t_',
        'struct_ida_movable_type_simd_info_t_',
        'struct_ida_movable_type_snapshot_t_',
        'struct_ida_movable_type_sreg_range_t_',
        'struct_ida_movable_type_stkpnt_t_',
        'struct_ida_movable_type_string_info_t_',
        'struct_ida_movable_type_sync_source_t_',
        'struct_ida_movable_type_tev_info_reg_t_',
        'struct_ida_movable_type_tev_reg_value_t_',
        'struct_ida_movable_type_til_symbol_t_',
        'struct_ida_movable_type_tinfo_t_',
        'struct_ida_movable_type_token_t_',
        'struct_ida_movable_type_try_handler_t_',
        'struct_ida_movable_type_tryblk_t_',
        'struct_ida_movable_type_twinline_t_',
        'struct_ida_movable_type_type_attr_t_',
        'struct_ida_movable_type_typedef_type_data_t_',
        'struct_ida_movable_type_udt_member_t_',
        'struct_ida_movable_type_udt_type_data_t_',
        'struct_ida_movable_type_update_bpt_info_t_',
        'struct_ida_movable_type_valinfo_t_',
        'struct_ida_movable_type_valstr_t_',
        'struct_ida_movable_type_xreflist_entry_t_',
        'struct_ida_syntax_highlighter_t',
        'struct_ida_syntax_highlighter_t__keywords_style_t',
        'struct_ida_syntax_highlighter_t__multicmt_t',
        'struct_ida_syntax_highlighter_t__plain_char_ptr_t',
        'struct_ida_syntax_highlighter_t_vtbl', 'struct_idadll_t',
        'struct_idainfo', 'struct_idaplace_t', 'struct_idaplace_t_vtbl',
        'struct_idasgn_t', 'struct_idc_class_t', 'struct_idc_global_t',
        'struct_idc_object_t', 'struct_idc_resolver_t',
        'struct_idc_resolver_t_vtbl', 'struct_idc_value_t',
        'struct_idcfuncs_t', 'struct_idd_opinfo_t', 'struct_idp_desc_t',
        'struct_idp_name_t', 'struct_ignore_micro_t', 'struct_impinfo_t',
        'struct_input_event_t',
        'struct_input_event_t__input_event_keyboard_data_t',
        'struct_input_event_t__input_event_mouse_data_t',
        'struct_input_event_t__input_event_shortcut_data_t',
        'struct_insn_t', 'struct_instant_dbgopts_t', 'struct_instruc_t',
        'struct_int128', 'struct_interr_exc_t',
        'struct_interr_exc_t_vtbl', 'struct_interval_t',
        'struct_intmap_t', 'struct_intset_t', 'struct_ioport_bit_t',
        'struct_ioport_t', 'struct_ioports_fallback_t',
        'struct_ioports_fallback_t_vtbl', 'struct_janitor_t__iobuf__P_',
        'struct_janitor_t_linput_t__P_', 'struct_jarr_t', 'struct_jobj_t',
        'struct_jump_pattern_t', 'struct_jump_pattern_t_vtbl',
        'struct_jvalue_t', 'struct_kvp_t',
        'struct_launch_process_params_t', 'struct_lex_value_t',
        'struct_lexer_t', 'struct_libfunc_t',
        'struct_line_rendering_output_entry_t', 'struct_linearray_t',
        'struct_lines_rendering_input_t',
        'struct_lines_rendering_output_t', 'struct_linput_buffer_t',
        'struct_linput_t', 'struct_llabel_t', 'struct_load_info_t',
        'struct_loader_t', 'struct_location_t', 'struct_locchange_md_t',
        'struct_lochist_entry_t', 'struct_lochist_t', 'struct_lock_func',
        'struct_lock_segment', 'struct_lowcnd_t',
        'struct_lowertype_helper_t', 'struct_lowertype_helper_t_vtbl',
        'struct_macro_constructor_t', 'struct_macro_constructor_t_vtbl',
        'struct_member_t', 'struct_memory_deserializer_t',
        'struct_memory_info_t', 'struct_memreg_info_t',
        'struct_merge_data_t', 'struct_minsn_t', 'struct_modinfo_t',
        'struct_movbpt_info_t', 'struct_mutable_graph_t',
        'struct_mutable_graph_t_vtbl', 'struct_netnode',
        'struct_no_regs_t', 'struct_node_info_t', 'struct_node_iterator',
        'struct_node_ordering_t', 'struct_node_set_t', 'struct_op_t',
        'struct_outctx_base_t', 'struct_outctx_base_t_vtbl',
        'struct_outctx_t', 'struct_outctx_t_vtbl', 'struct_place_t',
        'struct_place_t_vtbl', 'struct_plugin_info_t', 'struct_plugin_t',
        'struct_plugmod_t', 'struct_plugmod_t_vtbl', 'struct_point_t',
        'struct_pointseq_t', 'struct_post_event_visitor_t',
        'struct_post_event_visitor_t_vtbl', 'struct_predicate_t',
        'struct_predicate_t_vtbl', 'struct_printop_t',
        'struct_proc_def_t', 'struct_process_info_t',
        'struct_processor_t', 'struct_procmod_t', 'struct_procmod_t_vtbl',
        'struct_ptr_type_data_t', 'struct_qbasic_block_t',
        'struct_qffblk64_t', 'struct_qffblk_t', 'struct_qflow_chart_t',
        'struct_qflow_chart_t_vtbl',
        'struct_qiterator_qrefcnt_t_source_file_t__',
        'struct_qiterator_qrefcnt_t_source_file_t___vtbl',
        'struct_qiterator_qrefcnt_t_source_item_t__',
        'struct_qiterator_qrefcnt_t_source_item_t___vtbl',
        'struct_qlist_ui_request_t__P_',
        'struct_qlist_ui_request_t__P___const_iterator',
        'struct_qlist_ui_request_t__P___const_reverse_iterator',
        'struct_qlist_ui_request_t__P___iterator',
        'struct_qlist_ui_request_t__P___listnode_t',
        'struct_qlist_ui_request_t__P___reverse_iterator',
        'struct_qmutex_locker_t', 'struct_qrefcnt_obj_t',
        'struct_qrefcnt_obj_t_vtbl', 'struct_qrefcnt_t_extlang_t_',
        'struct_qrefcnt_t_qiterator_qrefcnt_t_source_file_t___',
        'struct_qrefcnt_t_qiterator_qrefcnt_t_source_item_t___',
        'struct_qrefcnt_t_refcnted_regex_t_',
        'struct_qrefcnt_t_source_file_t_',
        'struct_qrefcnt_t_source_item_t_', 'struct_qstack_token_t_',
        'struct_qstatbuf', 'struct_qvector__qstring_char__',
        'struct_qvector__qstring_unsigned_char__',
        'struct_qvector__qstring_wchar_t__', 'struct_qvector_argloc_t_',
        'struct_qvector_argpart_t_', 'struct_qvector_bool_',
        'struct_qvector_bool___P__syntax_highlight_style__P__const__qstring_char___R__',
        'struct_qvector_bpt_t_', 'struct_qvector_bpt_t__P_',
        'struct_qvector_bptaddrs_t_', 'struct_qvector_call_stack_info_t_',
        'struct_qvector_catch_t_', 'struct_qvector_cfgopt_set_t_',
        'struct_qvector_channel_redir_t_', 'struct_qvector_char_',
        'struct_qvector_cliopt_t_', 'struct_qvector_compiled_binpat_t_',
        'struct_qvector_const_bpt_t__P_', 'struct_qvector_const_char__P_',
        'struct_qvector_const_rangeset_t__P_',
        'struct_qvector_const_twinline_t__P_',
        'struct_qvector_debug_event_t_', 'struct_qvector_direntry_t_',
        'struct_qvector_dirtree_cursor_t_', 'struct_qvector_ea_name_t_',
        'struct_qvector_edge_t_', 'struct_qvector_enum_member_t_',
        'struct_qvector_exception_info_t_',
        'struct_qvector_extlang_t__P_', 'struct_qvector_fixup_info_t_',
        'struct_qvector_funcarg_t_', 'struct_qvector_group_crinfo_t_',
        'struct_qvector_ida_syntax_highlighter_t__keywords_style_t_',
        'struct_qvector_ida_syntax_highlighter_t__multicmt_t_',
        'struct_qvector_ida_syntax_highlighter_t__plain_char_ptr_t_',
        'struct_qvector_idc_global_t_', 'struct_qvector_idp_desc_t_',
        'struct_qvector_idp_name_t_', 'struct_qvector_int_',
        'struct_qvector_intmap_t_', 'struct_qvector_ioport_bit_t_',
        'struct_qvector_ioport_t_', 'struct_qvector_jvalue_t_',
        'struct_qvector_kvp_t_',
        'struct_qvector_line_rendering_output_entry_t__P_',
        'struct_qvector_lochist_entry_t_', 'struct_qvector_long_long_',
        'struct_qvector_long_long___P__syntax_highlight_style__P__const_char__P__',
        'struct_qvector_lowcnd_t_', 'struct_qvector_memory_info_t_',
        'struct_qvector_memreg_info_t_', 'struct_qvector_modinfo_t_',
        'struct_qvector_movbpt_code_t_', 'struct_qvector_movbpt_info_t_',
        'struct_qvector_node_set_t_', 'struct_qvector_op_t_',
        'struct_qvector_point_t_', 'struct_qvector_process_info_t_',
        'struct_qvector_qbasic_block_t_',
        'struct_qvector_qrefcnt_t_source_item_t__',
        'struct_qvector_qvector_const_char__P__',
        'struct_qvector_qvector_const_twinline_t__P__',
        'struct_qvector_qvector_int__',
        'struct_qvector_qvector_long_long__', 'struct_qvector_range_t_',
        'struct_qvector_rangeset_t_', 'struct_qvector_rect_t_',
        'struct_qvector_refinfo_desc_t_', 'struct_qvector_reg_access_t_',
        'struct_qvector_reg_info_t_', 'struct_qvector_register_info_t_',
        'struct_qvector_regobj_t_', 'struct_qvector_regval_t_',
        'struct_qvector_row_info_t_', 'struct_qvector_scattered_segm_t_',
        'struct_qvector_segm_move_info_t_',
        'struct_qvector_selection_item_t_', 'struct_qvector_simd_info_t_',
        'struct_qvector_simpleline_t_', 'struct_qvector_snapshot_t__P_',
        'struct_qvector_stkpnt_t_', 'struct_qvector_sync_source_t_',
        'struct_qvector_tev_info_reg_t_', 'struct_qvector_tev_info_t_',
        'struct_qvector_tev_reg_value_t_',
        'struct_qvector_thread_name_t_', 'struct_qvector_tinfo_t_',
        'struct_qvector_token_t_', 'struct_qvector_tryblk_t_',
        'struct_qvector_twinline_t_', 'struct_qvector_type_attr_t_',
        'struct_qvector_udt_member_t_', 'struct_qvector_unsigned_char_',
        'struct_qvector_unsigned_int_',
        'struct_qvector_unsigned_long_long_',
        'struct_qvector_update_bpt_info_t_', 'struct_qvector_valstr_t_',
        'struct_qvector_wchar_t_', 'struct_qvector_xreflist_entry_t_',
        'struct_range_marker_suspender_t', 'struct_range_t',
        'struct_rangeset_t', 'struct_rangevec_t', 'struct_reader_t',
        'struct_rect_t', 'struct_refcnted_regex_t',
        'struct_refcnted_regex_t_vtbl', 'struct_refinfo_desc_t',
        'struct_refinfo_t', 'struct_reg_access_t',
        'struct_reg_accesses_t', 'struct_reg_info_t', 'struct_regarg_t',
        'struct_regex_cache_t', 'struct_regex_t',
        'struct_register_info_t', 'struct_regmatch_t', 'struct_regobj_t',
        'struct_regobjs_t', 'struct_regval_t', 'struct_regvar_t',
        'struct_relobj_t', 'struct_reloc_info_t',
        'struct_renderer_info_pos_t', 'struct_renderer_info_t',
        'struct_renderer_pos_info_t', 'struct_row_info_t',
        'struct_rrel_t', 'struct_scattered_aloc_t',
        'struct_scattered_segm_t', 'struct_screen_graph_selection_t',
        'struct_segm_move_info_t', 'struct_segm_move_infos_t',
        'struct_segment_t', 'struct_seh_t', 'struct_selection_item_t',
        'struct_simd_info_t', 'struct_simple_bfi_t',
        'struct_simpleline_place_t', 'struct_simpleline_place_t_vtbl',
        'struct_simpleline_t', 'struct_snapshot_t',
        'struct_source_file_t', 'struct_source_file_t_vtbl',
        'struct_source_item_t', 'struct_source_item_t_vtbl',
        'struct_source_view_t', 'struct_srcinfo_provider_t',
        'struct_srcinfo_provider_t_vtbl', 'struct_sreg_range_t',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true_',
        'struct_std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true_',
        'struct_std___Compressed_pair_std__less__qstring_char____std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P____std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______true___true_',
        'struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_int__void__P____std___Tree_val_std___Tree_simple_types_int____true___true_',
        'struct_std___Compressed_pair_std__less_int___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_int__int___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____true___true_',
        'struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____true___true_',
        'struct_std___Compressed_pair_std__less_unsigned_long_long___std___Compressed_pair_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P____std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____true___true_',
        'struct_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false___value_compare',
        'struct_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false___value_compare',
        'struct_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false___value_compare',
        'struct_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false___value_compare',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int___',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____',
        'struct_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____',
        'struct_std___Tree_id_std___Tree_node_int__void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_const_int__int___void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P___P_',
        'struct_std___Tree_id_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P___P_',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____',
        'struct_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____',
        'struct_std___Tree_node_int__void__P_',
        'struct_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P_',
        'struct_std___Tree_node_std__pair_const_int__int___void__P_',
        'struct_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P_',
        'struct_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P_',
        'struct_std___Tree_std___Tmap_traits__qstring_char___qrefcnt_t_refcnted_regex_t___std__less__qstring_char____std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____false__',
        'struct_std___Tree_std___Tmap_traits_int__int__std__less_int___std__allocator_std__pair_const_int__int____false__',
        'struct_std___Tree_std___Tmap_traits_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____false__',
        'struct_std___Tree_std___Tmap_traits_unsigned_long_long__unsigned_long_long__std__less_unsigned_long_long___std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long____false__',
        'struct_std___Tree_std___Tset_traits_int__std__less_int___std__allocator_int___false__',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_int___',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____',
        'struct_std___Tree_unchecked_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_____',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int____',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t____',
        'struct_std___Tree_unchecked_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long____',
        'struct_std___Tree_val_std___Tree_simple_types_int__',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int___',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___',
        'struct_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long___',
        'struct_std__allocator_int_',
        'struct_std__allocator_std___Tree_node_int__void__P__',
        'struct_std__allocator_std___Tree_node_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t____void__P__',
        'struct_std__allocator_std___Tree_node_std__pair_const_int__int___void__P__',
        'struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t___void__P__',
        'struct_std__allocator_std___Tree_node_std__pair_const_unsigned_long_long__unsigned_long_long___void__P__',
        'struct_std__allocator_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___',
        'struct_std__allocator_std__pair_const_int__int__',
        'struct_std__allocator_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__',
        'struct_std__allocator_std__pair_const_unsigned_long_long__unsigned_long_long__',
        'struct_std__initializer_list_int_',
        'struct_std__initializer_list_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t___',
        'struct_std__initializer_list_std__pair_const_int__int__',
        'struct_std__initializer_list_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t__',
        'struct_std__initializer_list_std__pair_const_unsigned_long_long__unsigned_long_long__',
        'struct_std__less__qstring_char__', 'struct_std__less_int_',
        'struct_std__less_unsigned_long_long_',
        'struct_std__map__qstring_char___qrefcnt_t_refcnted_regex_t__',
        'struct_std__map_int__int_',
        'struct_std__map_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_',
        'struct_std__map_unsigned_long_long__unsigned_long_long_',
        'struct_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t__',
        'struct_std__pair_const_int__int_',
        'struct_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_',
        'struct_std__pair_const_unsigned_long_long__unsigned_long_long_',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int_____std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'struct_std__pair_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t_______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'struct_std__pair_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long______std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_int____',
        'struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'struct_std__reverse_iterator_std___Tree_const_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const__qstring_char___qrefcnt_t_refcnted_regex_t______',
        'struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_int__int_____',
        'struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__backward_flow_iterator_t_no_regs_t__simple_bfi_t___state_t_____',
        'struct_std__reverse_iterator_std___Tree_iterator_std___Tree_val_std___Tree_simple_types_std__pair_const_unsigned_long_long__unsigned_long_long_____',
        'struct_std__set_int_', 'struct_stkarg_area_info_t',
        'struct_stkpnt_t', 'struct_stkpnts_t', 'struct_strarray_t',
        'struct_string_info_t', 'struct_strpath_t', 'struct_struc_t',
        'struct_struct_field_visitor_t',
        'struct_struct_field_visitor_t_vtbl', 'struct_structplace_t',
        'struct_structplace_t_vtbl', 'struct_strwinsetup_t',
        'struct_switch_info_t', 'struct_sync_source_t',
        'struct_synced_group_t', 'struct_syntax_highlighter_t',
        'struct_syntax_highlighter_t_vtbl', 'struct_tev_info_reg_t',
        'struct_tev_info_t', 'struct_tev_reg_value_t',
        'struct_text_sink_t', 'struct_text_sink_t_vtbl',
        'struct_textctrl_info_t', 'struct_thread_name_t',
        'struct_til_bucket_t', 'struct_til_stream_t',
        'struct_til_symbol_t', 'struct_til_t', 'struct_tinfo_t',
        'struct_tinfo_visitor_t', 'struct_tinfo_visitor_t_vtbl',
        'struct_tm', 'struct_token_t', 'struct_try_handler_t',
        'struct_tryblk_t', 'struct_twinline_t', 'struct_twinpos_t',
        'struct_type_attr_t', 'struct_type_mods_t',
        'struct_typedef_type_data_t', 'struct_udt_member_t',
        'struct_udt_type_data_t', 'struct_udtmembervec_t',
        'struct_ui_request_t', 'struct_ui_request_t_vtbl',
        'struct_ui_requests_t', 'struct_uint128',
        'struct_update_bpt_info_t', 'struct_user_defined_prefix_t',
        'struct_user_defined_prefix_t_vtbl', 'struct_user_graph_place_t',
        'struct_user_graph_place_t_vtbl', 'struct_valinfo_t',
        'struct_valstr_t', 'struct_valstr_t__flatten_args_t',
        'struct_valstrs_t', 'struct_value_u__d128_t',
        'struct_value_u__dq_t', 'struct_value_u__dt_t',
        'struct_view_mouse_event_t', 'struct_xrefblk_t',
        'struct_xreflist_entry_t', 'struct_xrefpos_t',
        'structplace_t__adjust', 'structplace_t__beginning',
        'structplace_t__clone', 'structplace_t__compare',
        'structplace_t__compare2', 'structplace_t__copyfrom',
        'structplace_t__deserialize', 'structplace_t__ending',
        'structplace_t__enter', 'structplace_t__generate',
        'structplace_t__id', 'structplace_t__leave',
        'structplace_t__makeplace', 'structplace_t__name',
        'structplace_t__next', 'structplace_t__prev',
        'structplace_t__print', 'structplace_t__rebase',
        'structplace_t__serialize', 'structplace_t__toea',
        'structplace_t__touval', 'strvec_t', 'sval_t', 'svalvec_t',
        'swap128', 'swap64', 'swap_idcvs', 'swap_value', 'switch_dbctx',
        'sync_source_vec_t', 'syntax_highlight_style', 'table_checker_t',
        'tag_addr', 'tag_advance', 'tag_remove', 'tag_skipcode',
        'tag_skipcodes', 'tag_strlen', 'tail_owner_changed',
        'take_memory_snapshot', 'tcc_place_type_t', 'tcc_renderer_type_t',
        'term_database', 'term_plugins', 'term_process', 'tev_bpt',
        'tev_call', 'tev_event', 'tev_insn', 'tev_max', 'tev_mem',
        'tev_none', 'tev_reg_values_t', 'tev_ret', 'tev_type_t',
        'tevinfo_vec_t', 'tevinforeg_vec_t', 'text_t', 'thid_t',
        'thread_name_vec_t', 'throw_idc_exception', 'thunk_func_created',
        'ti_changed', 'tid_t', 'tinfo_code_t', 'tinfovec_t',
        'toggle_bnot', 'toggle_sign', 'tokenstack_t',
        'track_value_until_address_jpt', 'tracked_regs_t', 'trim',
        'trim_jtable', 'try_to_add_libfunc', 'tryblks_t',
        'tryblks_updated', 'tty_control_t', 'twidget_type_t',
        'type_attrs_t', 'type_sign_t', 'type_t', 'ucdr_kind_t', 'uchar',
        'ui_activate_widget', 'ui_add_idckey', 'ui_addons',
        'ui_analyzer_options', 'ui_ask_addr', 'ui_ask_buttons',
        'ui_ask_file', 'ui_ask_form', 'ui_ask_long', 'ui_ask_seg',
        'ui_ask_str', 'ui_ask_text', 'ui_attach_action_to_menu',
        'ui_attach_action_to_popup', 'ui_attach_action_to_toolbar',
        'ui_attach_dynamic_action_to_popup', 'ui_banner', 'ui_beep',
        'ui_broadcast', 'ui_cancel_exec_request',
        'ui_cancel_thread_exec_requests', 'ui_choose',
        'ui_choose_bookmark', 'ui_chooser_default_enter',
        'ui_close_chooser', 'ui_close_widget', 'ui_clr_cancelled',
        'ui_copywarn', 'ui_create_code_viewer', 'ui_create_custom_viewer',
        'ui_create_desktop_widget', 'ui_create_empty_widget',
        'ui_create_menu', 'ui_create_source_viewer', 'ui_create_toolbar',
        'ui_current_widget_changed', 'ui_custom_viewer_jump',
        'ui_custom_viewer_set_userdata', 'ui_database_closed',
        'ui_database_inited', 'ui_dbg_add_bpt', 'ui_dbg_add_bpt_tev',
        'ui_dbg_add_call_tev', 'ui_dbg_add_debug_event',
        'ui_dbg_add_insn_tev', 'ui_dbg_add_many_tevs',
        'ui_dbg_add_oldbpt', 'ui_dbg_add_path_mapping',
        'ui_dbg_add_ret_tev', 'ui_dbg_add_tev', 'ui_dbg_add_thread',
        'ui_dbg_add_vmod', 'ui_dbg_attach_process', 'ui_dbg_begin',
        'ui_dbg_bin_search', 'ui_dbg_bring_to_front',
        'ui_dbg_change_bptlocs', 'ui_dbg_check_bpt',
        'ui_dbg_choose_trace_file', 'ui_dbg_clear_requests_queue',
        'ui_dbg_clear_trace', 'ui_dbg_collect_stack_trace',
        'ui_dbg_compare_bpt_locs', 'ui_dbg_continue_process',
        'ui_dbg_define_exception', 'ui_dbg_del_bpt', 'ui_dbg_del_bptgrp',
        'ui_dbg_del_oldbpt', 'ui_dbg_del_thread', 'ui_dbg_del_vmod',
        'ui_dbg_detach_process', 'ui_dbg_diff_trace_file',
        'ui_dbg_edit_manual_regions', 'ui_dbg_enable_bblk_trace',
        'ui_dbg_enable_bpt', 'ui_dbg_enable_bptgrp',
        'ui_dbg_enable_func_trace', 'ui_dbg_enable_insn_trace',
        'ui_dbg_enable_manual_regions', 'ui_dbg_enable_oldbpt',
        'ui_dbg_enable_step_trace', 'ui_dbg_end', 'ui_dbg_exit_process',
        'ui_dbg_find_bpt', 'ui_dbg_for_all_bpts',
        'ui_dbg_get_bblk_trace_options', 'ui_dbg_get_bpt',
        'ui_dbg_get_bpt_group', 'ui_dbg_get_bpt_qty',
        'ui_dbg_get_bpt_tev_ea', 'ui_dbg_get_bptloc_string',
        'ui_dbg_get_call_tev_callee', 'ui_dbg_get_current_source_file',
        'ui_dbg_get_current_source_line', 'ui_dbg_get_current_thread',
        'ui_dbg_get_debug_event', 'ui_dbg_get_event_cond',
        'ui_dbg_get_first_module', 'ui_dbg_get_func_trace_options',
        'ui_dbg_get_global_var', 'ui_dbg_get_grp_bpts',
        'ui_dbg_get_insn_tev_reg_mem', 'ui_dbg_get_insn_tev_reg_result',
        'ui_dbg_get_insn_tev_reg_result_i', 'ui_dbg_get_insn_tev_reg_val',
        'ui_dbg_get_insn_tev_reg_val_i', 'ui_dbg_get_insn_trace_options',
        'ui_dbg_get_ip_val', 'ui_dbg_get_local_var',
        'ui_dbg_get_local_vars', 'ui_dbg_get_manual_regions',
        'ui_dbg_get_memory_info', 'ui_dbg_get_module_info',
        'ui_dbg_get_next_module', 'ui_dbg_get_process_options',
        'ui_dbg_get_process_state', 'ui_dbg_get_processes',
        'ui_dbg_get_reg_info', 'ui_dbg_get_reg_val',
        'ui_dbg_get_reg_val_i', 'ui_dbg_get_reg_value_type',
        'ui_dbg_get_ret_tev_return', 'ui_dbg_get_running_notification',
        'ui_dbg_get_running_request', 'ui_dbg_get_sp_val',
        'ui_dbg_get_srcinfo_provider', 'ui_dbg_get_step_trace_options',
        'ui_dbg_get_tev_ea', 'ui_dbg_get_tev_event',
        'ui_dbg_get_tev_info', 'ui_dbg_get_tev_memory_info',
        'ui_dbg_get_tev_qty', 'ui_dbg_get_tev_tid', 'ui_dbg_get_tev_type',
        'ui_dbg_get_thread_qty', 'ui_dbg_get_trace_base_address',
        'ui_dbg_get_trace_dynamic_register_set',
        'ui_dbg_get_trace_file_desc', 'ui_dbg_get_trace_platform',
        'ui_dbg_getn_bpt', 'ui_dbg_getn_thread',
        'ui_dbg_getn_thread_name', 'ui_dbg_graph_trace',
        'ui_dbg_handle_debug_event', 'ui_dbg_hide_all_bpts',
        'ui_dbg_internal_appcall', 'ui_dbg_internal_cleanup_appcall',
        'ui_dbg_internal_get_elang', 'ui_dbg_internal_get_sreg_base',
        'ui_dbg_internal_ioctl', 'ui_dbg_internal_set_elang',
        'ui_dbg_is_bblk_trace_enabled', 'ui_dbg_is_busy',
        'ui_dbg_is_func_trace_enabled', 'ui_dbg_is_insn_trace_enabled',
        'ui_dbg_is_step_trace_enabled', 'ui_dbg_is_valid_trace_file',
        'ui_dbg_list_bptgrps', 'ui_dbg_load_dbg_dbginfo',
        'ui_dbg_load_debugger', 'ui_dbg_load_trace_file',
        'ui_dbg_map_source_file_path', 'ui_dbg_map_source_path',
        'ui_dbg_modify_source_paths', 'ui_dbg_read_memory',
        'ui_dbg_read_registers', 'ui_dbg_register_provider',
        'ui_dbg_rename_bptgrp', 'ui_dbg_request_add_bpt',
        'ui_dbg_request_add_oldbpt', 'ui_dbg_request_attach_process',
        'ui_dbg_request_clear_trace', 'ui_dbg_request_continue_process',
        'ui_dbg_request_del_bpt', 'ui_dbg_request_del_oldbpt',
        'ui_dbg_request_detach_process',
        'ui_dbg_request_enable_bblk_trace', 'ui_dbg_request_enable_bpt',
        'ui_dbg_request_enable_func_trace',
        'ui_dbg_request_enable_insn_trace',
        'ui_dbg_request_enable_oldbpt',
        'ui_dbg_request_enable_step_trace', 'ui_dbg_request_exit_process',
        'ui_dbg_request_resume_thread', 'ui_dbg_request_run_to',
        'ui_dbg_request_select_thread',
        'ui_dbg_request_set_bblk_trace_options',
        'ui_dbg_request_set_func_trace_options',
        'ui_dbg_request_set_insn_trace_options',
        'ui_dbg_request_set_reg_val', 'ui_dbg_request_set_resume_mode',
        'ui_dbg_request_set_step_trace_options',
        'ui_dbg_request_start_process', 'ui_dbg_request_step_into',
        'ui_dbg_request_step_over', 'ui_dbg_request_step_until_ret',
        'ui_dbg_request_suspend_process', 'ui_dbg_request_suspend_thread',
        'ui_dbg_resume_thread', 'ui_dbg_retrieve_exceptions',
        'ui_dbg_run_requests', 'ui_dbg_run_to', 'ui_dbg_save_trace_file',
        'ui_dbg_select_thread', 'ui_dbg_set_bblk_trace_options',
        'ui_dbg_set_bpt_group', 'ui_dbg_set_bptloc_group',
        'ui_dbg_set_bptloc_string', 'ui_dbg_set_debugger_options',
        'ui_dbg_set_event_cond', 'ui_dbg_set_func_trace_options',
        'ui_dbg_set_highlight_trace_options',
        'ui_dbg_set_insn_trace_options', 'ui_dbg_set_manual_regions',
        'ui_dbg_set_process_options', 'ui_dbg_set_process_state',
        'ui_dbg_set_reg_val', 'ui_dbg_set_reg_val_i',
        'ui_dbg_set_remote_debugger', 'ui_dbg_set_resume_mode',
        'ui_dbg_set_step_trace_options', 'ui_dbg_set_trace_base_address',
        'ui_dbg_set_trace_dynamic_register_set',
        'ui_dbg_set_trace_file_desc', 'ui_dbg_set_trace_platform',
        'ui_dbg_set_trace_size', 'ui_dbg_srcdbg_request_step_into',
        'ui_dbg_srcdbg_request_step_over',
        'ui_dbg_srcdbg_request_step_until_ret', 'ui_dbg_srcdbg_step_into',
        'ui_dbg_srcdbg_step_over', 'ui_dbg_srcdbg_step_until_ret',
        'ui_dbg_start_process', 'ui_dbg_step_into', 'ui_dbg_step_over',
        'ui_dbg_step_until_ret', 'ui_dbg_store_exceptions',
        'ui_dbg_suspend_process', 'ui_dbg_suspend_thread',
        'ui_dbg_unregister_provider', 'ui_dbg_update_bpt',
        'ui_dbg_wait_for_next_event', 'ui_dbg_write_memory',
        'ui_dbg_write_register', 'ui_debugger_menu_change',
        'ui_delete_menu', 'ui_delete_toolbar', 'ui_desktop_applied',
        'ui_destroy_custom_viewer', 'ui_destroying_plugmod',
        'ui_destroying_procmod', 'ui_detach_action_from_menu',
        'ui_detach_action_from_popup', 'ui_detach_action_from_toolbar',
        'ui_display_widget', 'ui_ea_viewer_history_info',
        'ui_ea_viewer_history_push_and_jump',
        'ui_enable_chooser_item_attrs', 'ui_execute_sync',
        'ui_execute_ui_requests', 'ui_execute_ui_requests_list',
        'ui_find_widget', 'ui_finish_populating_widget_popup',
        'ui_free_custom_icon', 'ui_gen_disasm_text',
        'ui_gen_idanode_text', 'ui_genfile_callback',
        'ui_get_action_attr', 'ui_get_active_modal_widget',
        'ui_get_chooser_data', 'ui_get_chooser_item_attrs',
        'ui_get_chooser_obj', 'ui_get_curline', 'ui_get_curplace',
        'ui_get_current_viewer', 'ui_get_current_widget', 'ui_get_cursor',
        'ui_get_custom_viewer_curline', 'ui_get_custom_viewer_hint',
        'ui_get_custom_viewer_location',
        'ui_get_custom_viewer_place_xcoord', 'ui_get_ea_hint',
        'ui_get_highlight_2', 'ui_get_item_hint', 'ui_get_kernel_version',
        'ui_get_key_code', 'ui_get_lines_rendering_info', 'ui_get_opnum',
        'ui_get_output_curline', 'ui_get_output_cursor',
        'ui_get_output_selected_text', 'ui_get_range_marker',
        'ui_get_registered_actions', 'ui_get_renderer_type',
        'ui_get_synced_group', 'ui_get_tab_size',
        'ui_get_user_input_event', 'ui_get_viewer_place_type',
        'ui_get_viewer_user_data', 'ui_get_widget_config',
        'ui_get_widget_title', 'ui_get_widget_type', 'ui_get_window_id',
        'ui_hexdumpea', 'ui_idcstart', 'ui_idcstop',
        'ui_initing_database', 'ui_install_cli',
        'ui_install_custom_datatype_menu',
        'ui_install_custom_optype_menu', 'ui_is_idaq', 'ui_is_idaview',
        'ui_is_msg_inited', 'ui_jump_in_custom_viewer', 'ui_jumpto',
        'ui_last', 'ui_load_custom_icon', 'ui_load_custom_icon_file',
        'ui_load_file', 'ui_lock_range_refresh', 'ui_lookup_key_code',
        'ui_mbox', 'ui_msg', 'ui_msg_clear', 'ui_msg_get_lines',
        'ui_msg_save', 'ui_navband_ea', 'ui_navband_pixel', 'ui_noabort',
        'ui_notification_t', 'ui_null', 'ui_obsolete_dbg_save_bpts',
        'ui_obsolete_del_idckey', 'ui_obsolete_display_widget',
        'ui_obsolete_get_highlight',
        'ui_obsolete_get_user_strlist_options',
        'ui_obsolete_refresh_custom_code_viewer',
        'ui_obsolete_set_nav_colorizer', 'ui_open_builtin',
        'ui_open_form', 'ui_open_url', 'ui_plugin_loaded',
        'ui_plugin_unloading', 'ui_populating_widget_popup',
        'ui_postprocess_action', 'ui_preprocess_action',
        'ui_process_action', 'ui_range', 'ui_read_range_selection',
        'ui_read_selection', 'ui_ready_to_run', 'ui_refresh',
        'ui_refresh_chooser', 'ui_refresh_choosers',
        'ui_refresh_custom_viewer', 'ui_refresh_navband',
        'ui_refreshmarked', 'ui_register_action', 'ui_register_timer',
        'ui_repaint_qwidget', 'ui_restore_database_snapshot', 'ui_resume',
        'ui_run_dbg', 'ui_saved', 'ui_saving', 'ui_screen_ea_changed',
        'ui_screenea', 'ui_set_cancelled',
        'ui_set_code_viewer_line_handlers',
        'ui_set_custom_viewer_handler', 'ui_set_custom_viewer_handlers',
        'ui_set_custom_viewer_mode', 'ui_set_custom_viewer_range',
        'ui_set_dock_pos', 'ui_set_highlight', 'ui_set_mappings',
        'ui_set_nav_colorizer', 'ui_set_renderer_type',
        'ui_set_widget_config', 'ui_setidle', 'ui_setup_plugins_menu',
        'ui_show_rename_dialog', 'ui_strchoose', 'ui_suspend',
        'ui_sync_sources', 'ui_take_database_snapshot',
        'ui_test_cancelled', 'ui_unlock_range_refresh', 'ui_unmarksel',
        'ui_unrecognized_config_directive', 'ui_unregister_action',
        'ui_unregister_timer', 'ui_update_action_attr',
        'ui_update_file_history', 'ui_updated_actions',
        'ui_updating_actions', 'ui_widget_closing', 'ui_widget_invisible',
        'ui_widget_visible', 'uint', 'uint16', 'uint32', 'uint64',
        'uint8', 'ulonglong', 'under_debugger', 'unhook_event_listener',
        'unhook_from_notification_point',
        'union_action_ctx_base_source_t', 'union_argloc_t_0',
        'union_argloc_t___F4A6A313BC9EA9730D72EF3AFDF761E4',
        'union_callui_t', 'union_cfgopt_t_0', 'union_cfgopt_t_1',
        'union_cfgopt_t___072F956EBF1D0FA65345CBEA02E26438',
        'union_cfgopt_t___275FC9DDBA9D1187AC5032610B4D4F63',
        'union_func_t_0',
        'union_func_t___C940058B2272AD9112E2141245617273',
        'union_idc_value_t_0',
        'union_idc_value_t___D589224ACA3955A7C89073061DACDDE8',
        'union_input_event_t_0',
        'union_input_event_t___4953DA15226C435F033B39D89D558652',
        'union_insn_t_0',
        'union_insn_t___F4FA00FEEF275F329AD5381050035CF8',
        'union_jvalue_t_0',
        'union_jvalue_t___86FD308AB52B8F8AFE7E7C65068A43C3',
        'union_lex_value_t_0',
        'union_lex_value_t___6E94C03EE084EC1E8773E8F11C206FDC',
        'union_op_t_0', 'union_op_t_1', 'union_op_t_2', 'union_op_t_3',
        'union_op_t___03EE851906E7470B48652C42A8F5F22F',
        'union_op_t___1DAE607E75260845BFCA6DE571F2D359',
        'union_op_t___63479489C28A4014434636A3BFC4DC99',
        'union_op_t___9FE5DDDE6246481B3EE86C7EEB25DDF5', 'union_opinfo_t',
        'union_regval_t_0',
        'union_regval_t___E2461B07C1F03128F15079BB1FB5F381',
        'union_switch_info_t_0',
        'union_switch_info_t___76B1A80AA47B7214ED24D33A3285D956',
        'union_token_t_0', 'union_token_t_1',
        'union_token_t___8299423771E115C2E8FEC5C7170C0424',
        'union_token_t___EFD300335D00E904D0DC340AFA3DF967',
        'union_typedef_type_data_t_0',
        'union_typedef_type_data_t___F773DD8B4C420A056648FD7EB1349F55',
        'union_value_u', 'union_view_mouse_event_location_t',
        'unlock_dbgmem_config', 'unmake_linput', 'unpack_dd', 'unpack_dq',
        'unpack_ds', 'unpack_dw', 'unpack_idcobj_from_bv',
        'unpack_idcobj_from_idb', 'unpack_memory', 'unpack_xleb128',
        'unregister_custom_data_format', 'unregister_custom_data_type',
        'unregister_custom_fixup', 'unregister_custom_refinfo',
        'unregister_post_event_visitor', 'upd_abits', 'update_bpt_vec_t',
        'update_extra_cmt', 'update_fpd', 'update_func',
        'update_hidden_range', 'update_segm',
        'update_snapshot_attributes', 'update_type_t', 'updating_tryblks',
        'upgraded', 'use_mapping', 'user2bin', 'user2qstr', 'user2str',
        'ushort', 'utf16_utf8', 'utf8_utf16', 'uval_t', 'uvalvec_t',
        'va_list', 'vadd_extra_line', 'validate_idb_names',
        'validate_idb_names2', 'validate_name', 'valstrvec_t',
        'verify_argloc', 'verify_tinfo', 'verror', 'view_activated',
        'view_click', 'view_close', 'view_created', 'view_curpos',
        'view_dblclick', 'view_deactivated', 'view_event_state_t',
        'view_keydown', 'view_loc_changed',
        'view_mouse_event_t__location_t', 'view_mouse_moved',
        'view_mouse_over', 'view_notification_t', 'view_switched',
        'visit_patched_bytes', 'visit_snapshot_tree',
        'visit_stroff_fields', 'visit_subtypes', 'vloader_failure',
        'vme_button_t', 'vqmakepath', 'vqperror', 'vshow_hex',
        'vshow_hex_file', 'wchar16_t', 'wchar32_t', 'winerr',
        'write_struc_path', 'write_tinfo_bitfield_value', 'writebytes',
        'xrefblk_t_first_from', 'xrefblk_t_first_to',
        'xrefblk_t_next_from', 'xrefblk_t_next_to', 'xrefchar',
        'xreflist_t', 'zip_deflate', 'zip_inflate']
    
    return locals()
