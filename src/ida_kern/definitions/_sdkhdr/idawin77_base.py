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
    
    class struct_std___Compressed_pair_std__allocator_char16_t___std___String_val_std___Simple_types_char16_t____true_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char16_t__(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char16_t_____Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char16_t_____Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char16_t_____Bxty._fields_ = [
        ('_Buf', ctypes.c_int16 * 8),
        ('_Ptr', ctypes.POINTER(ctypes.c_int16)),
        ('_Alias', ctypes.c_char * 8),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std___String_val_std___Simple_types_char16_t__._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char16_t__._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char16_t_____Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char16_t___std___String_val_std___Simple_types_char16_t____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char16_t___std___String_val_std___Simple_types_char16_t____true_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char16_t__),
    ]
    
    class struct_std___Compressed_pair_std__allocator_char32_t___std___String_val_std___Simple_types_char32_t____true_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char32_t__(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char32_t_____Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char32_t_____Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char32_t_____Bxty._fields_ = [
        ('_Buf', ctypes.c_int32 * 4),
        ('_Ptr', ctypes.POINTER(ctypes.c_int32)),
        ('_Alias', ctypes.c_char * 4),
        ('PADDING_0', ctypes.c_ubyte * 12),
    ]
    
    struct_std___String_val_std___Simple_types_char32_t__._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char32_t__._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char32_t_____Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char32_t___std___String_val_std___Simple_types_char32_t____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char32_t___std___String_val_std___Simple_types_char32_t____true_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char32_t__),
    ]
    
    class struct_std___Compressed_pair_std__allocator_wchar_t___std___String_val_std___Simple_types_wchar_t____true_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_wchar_t__(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_wchar_t_____Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_wchar_t_____Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_wchar_t_____Bxty._fields_ = [
        ('_Buf', ctypes.c_int16 * 8),
        ('_Ptr', ctypes.POINTER(ctypes.c_int16)),
        ('_Alias', ctypes.c_char * 8),
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std___String_val_std___Simple_types_wchar_t__._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_wchar_t__._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_wchar_t_____Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_wchar_t___std___String_val_std___Simple_types_wchar_t____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_wchar_t___std___String_val_std___Simple_types_wchar_t____true_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_wchar_t__),
    ]
    
    class struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____(Structure):
        pass
    
    class struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___(Structure):
        pass
    
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___._pack_ = 1 # source:False
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___._fields_ = [
        ('_Ptr', ctypes.POINTER(ctypes.c_int16)),
    ]
    
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____._fields_ = [
        ('current', struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____(Structure):
        pass
    
    class struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___(Structure):
        pass
    
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___._pack_ = 1 # source:False
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___._fields_ = [
        ('_Ptr', ctypes.POINTER(ctypes.c_int32)),
    ]
    
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____._fields_ = [
        ('current', struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____(Structure):
        pass
    
    class struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___(Structure):
        pass
    
    struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___._pack_ = 1 # source:False
    struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___._fields_ = [
        ('_Ptr', ctypes.POINTER(ctypes.c_int16)),
    ]
    
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____._fields_ = [
        ('current', struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char____(Structure):
        pass
    
    class struct_std___String_const_iterator_std___String_val_std___Simple_types_char___(Structure):
        pass
    
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char___._pack_ = 1 # source:False
    struct_std___String_const_iterator_std___String_val_std___Simple_types_char___._fields_ = [
        ('_Ptr', ctypes.c_char_p),
    ]
    
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char____._fields_ = [
        ('current', struct_std___String_const_iterator_std___String_val_std___Simple_types_char___),
    ]
    
    class struct_std___Compressed_pair_std__allocator_char___std___String_val_std___Simple_types_char____true_(Structure):
        pass
    
    class struct_std___String_val_std___Simple_types_char__(Structure):
        pass
    
    class union_std___String_val_std___Simple_types_char_____Bxty(Union):
        pass
    
    union_std___String_val_std___Simple_types_char_____Bxty._pack_ = 1 # source:False
    union_std___String_val_std___Simple_types_char_____Bxty._fields_ = [
        ('_Buf', ctypes.c_char * 16),
        ('_Ptr', ctypes.c_char_p),
        ('_Alias', ctypes.c_char * 16),
    ]
    
    struct_std___String_val_std___Simple_types_char__._pack_ = 1 # source:False
    struct_std___String_val_std___Simple_types_char__._fields_ = [
        ('_Bx', union_std___String_val_std___Simple_types_char_____Bxty),
        ('_Mysize', ctypes.c_uint64),
        ('_Myres', ctypes.c_uint64),
    ]
    
    struct_std___Compressed_pair_std__allocator_char___std___String_val_std___Simple_types_char____true_._pack_ = 1 # source:False
    struct_std___Compressed_pair_std__allocator_char___std___String_val_std___Simple_types_char____true_._fields_ = [
        ('_Myval2', struct_std___String_val_std___Simple_types_char__),
    ]
    
    class struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t____(Structure):
        pass
    
    class struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___(Structure):
        pass
    
    struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___._pack_ = 1 # source:False
    struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t____._fields_ = [
        ('current', struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t____(Structure):
        pass
    
    class struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___(Structure):
        pass
    
    struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___._pack_ = 1 # source:False
    struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t____._fields_ = [
        ('current', struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t____(Structure):
        pass
    
    class struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___(Structure):
        pass
    
    struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___._pack_ = 1 # source:False
    struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t____._fields_ = [
        ('current', struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___),
    ]
    
    class struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char____(Structure):
        pass
    
    class struct_std___String_iterator_std___String_val_std___Simple_types_char___(Structure):
        pass
    
    struct_std___String_iterator_std___String_val_std___Simple_types_char___._pack_ = 1 # source:False
    struct_std___String_iterator_std___String_val_std___Simple_types_char___._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 8),
    ]
    
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char____._pack_ = 1 # source:False
    struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char____._fields_ = [
        ('current', struct_std___String_iterator_std___String_val_std___Simple_types_char___),
    ]
    
    class struct_std___Char_traits_unsigned_short__unsigned_short_(Structure):
        pass
    
    class struct_std___String_constructor_rvalue_allocator_tag(Structure):
        pass
    
    class struct_std__integral_constant_unsigned_long_long__0_(Structure):
        pass
    
    class struct_std___Char_traits_char16_t__unsigned_short_(Structure):
        pass
    
    class struct_std___Char_traits_wchar_t__unsigned_short_(Structure):
        pass
    
    class struct_std___Char_traits_char32_t__unsigned_int_(Structure):
        pass
    
    class struct_std___Floating_type_traits_long_double_(Structure):
        pass
    
    class struct_std__numeric_limits_unsigned_long_long_(Structure):
        pass
    
    class struct_std___Narrow_char_traits_char__int_(Structure):
        pass
    
    class struct_std___String_constructor_concat_tag(Structure):
        pass
    
    class struct_std__integral_constant_bool__false_(Structure):
        pass
    
    class struct_std__numeric_limits_unsigned_short_(Structure):
        pass
    
    class struct__Combined_type_float__long_double_(Structure):
        pass
    
    class struct_std___Floating_type_traits_double_(Structure):
        pass
    
    class struct_std___WChar_traits_unsigned_short_(Structure):
        pass
    
    class struct_std__integral_constant_bool__true_(Structure):
        pass
    
    class struct_std__numeric_limits_unsigned_char_(Structure):
        pass
    
    class struct_std__numeric_limits_unsigned_long_(Structure):
        pass
    
    class struct_std___Basic_container_proxy_ptr12(Structure):
        pass
    
    class struct_std___Container_proxy(Structure):
        pass
    
    struct_std___Basic_container_proxy_ptr12._pack_ = 1 # source:False
    struct_std___Basic_container_proxy_ptr12._fields_ = [
        ('_Ptr', ctypes.POINTER(struct_std___Container_proxy)),
    ]
    
    class struct_std___Floating_type_traits_float_(Structure):
        pass
    
    class struct_std___Is_character_unsigned_char_(Structure):
        pass
    
    class struct_std__basic_istringstream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_ostringstream_wchar_t_(Structure):
        pass
    
    class struct_std__numeric_limits_unsigned_int_(Structure):
        pass
    
    class struct_std___Is_character_or_bool_bool_(Structure):
        pass
    
    class struct_std__basic_stringstream_wchar_t_(Structure):
        pass
    
    class struct_std__char_traits_unsigned_short_(Structure):
        pass
    
    class struct_std__numeric_limits_long_double_(Structure):
        pass
    
    class struct_std__numeric_limits_signed_char_(Structure):
        pass
    
    class struct_std___Is_character_signed_char_(Structure):
        pass
    
    class struct_std___Zero_then_variadic_args_t(Structure):
        pass
    
    class struct_std__bidirectional_iterator_tag(Structure):
        pass
    
    class struct_std__initializer_list_char16_t_(Structure):
        pass
    
    struct_std__initializer_list_char16_t_._pack_ = 1 # source:False
    struct_std__initializer_list_char16_t_._fields_ = [
        ('_First', ctypes.POINTER(ctypes.c_int16)),
        ('_Last', ctypes.POINTER(ctypes.c_int16)),
    ]
    
    class struct_std__initializer_list_char32_t_(Structure):
        pass
    
    struct_std__initializer_list_char32_t_._pack_ = 1 # source:False
    struct_std__initializer_list_char32_t_._fields_ = [
        ('_First', ctypes.POINTER(ctypes.c_int32)),
        ('_Last', ctypes.POINTER(ctypes.c_int32)),
    ]
    
    class struct_std__random_access_iterator_tag(Structure):
        pass
    
    class struct_std___One_then_variadic_args_t(Structure):
        pass
    
    class struct_std__bad_array_new_length_vtbl(Structure):
        pass
    
    class struct_std__basic_istringstream_char_(Structure):
        pass
    
    class struct_std__basic_ostringstream_char_(Structure):
        pass
    
    class struct_std__initializer_list_wchar_t_(Structure):
        pass
    
    struct_std__initializer_list_wchar_t_._pack_ = 1 # source:False
    struct_std__initializer_list_wchar_t_._fields_ = [
        ('_First', ctypes.POINTER(ctypes.c_int16)),
        ('_Last', ctypes.POINTER(ctypes.c_int16)),
    ]
    
    class struct_std__numeric_limits_long_long_(Structure):
        pass
    
    class struct__Combined_type_float__double_(Structure):
        pass
    
    class struct__Real_widened_double__double_(Structure):
        pass
    
    class struct_std___Default_allocate_traits(Structure):
        pass
    
    class struct_std__basic_streambuf_wchar_t_(Structure):
        pass
    
    class struct_std__basic_stringbuf_wchar_t_(Structure):
        pass
    
    class struct_std__basic_stringstream_char_(Structure):
        pass
    
    class struct_std__numeric_limits_char16_t_(Structure):
        pass
    
    class struct_std__numeric_limits_char32_t_(Structure):
        pass
    
    class struct__Real_widened_double__float_(Structure):
        pass
    
    class struct__Real_widened_float__double_(Structure):
        pass
    
    class struct_std___Char_traits_char__int_(Structure):
        pass
    
    class struct_std___WChar_traits_char16_t_(Structure):
        pass
    
    class struct_std__basic_ifstream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_iostream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_ofstream_wchar_t_(Structure):
        pass
    
    class struct_std__numeric_limits_wchar_t_(Structure):
        pass
    
    class struct__Real_widened_float__float_(Structure):
        pass
    
    class struct_std___Nontrivial_dummy_type(Structure):
        pass
    
    class struct_std___WChar_traits_wchar_t_(Structure):
        pass
    
    class struct_std__basic_filebuf_wchar_t_(Structure):
        pass
    
    class struct_std__basic_fstream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_istream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_ostream_wchar_t_(Structure):
        pass
    
    class struct_std__basic_string_char16_t_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char16_t___std___String_val_std___Simple_types_char16_t____true_),
         ]
    
    class struct_std__basic_string_char32_t_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char32_t___std___String_val_std___Simple_types_char32_t____true_),
         ]
    
    class struct_std__initializer_list_char_(Structure):
        pass
    
    struct_std__initializer_list_char_._pack_ = 1 # source:False
    struct_std__initializer_list_char_._fields_ = [
        ('_First', ctypes.c_char_p),
        ('_Last', ctypes.c_char_p),
    ]
    
    class struct_std__numeric_limits_double_(Structure):
        pass
    
    class struct_std___Alloc_unpack_tuple_t(Structure):
        pass
    
    class struct_std__basic_streambuf_char_(Structure):
        pass
    
    class struct_std__basic_string_wchar_t_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_wchar_t___std___String_val_std___Simple_types_wchar_t____true_),
         ]
    
    class struct_std__basic_stringbuf_char_(Structure):
        pass
    
    class struct_std__char_traits_char16_t_(Structure):
        pass
    
    class struct_std__char_traits_char32_t_(Structure):
        pass
    
    class struct_std__nested_exception_vtbl(Structure):
        pass
    
    class struct_std__numeric_limits_float_(Structure):
        pass
    
    class struct_std__numeric_limits_short_(Structure):
        pass
    
    class struct_std__piecewise_construct_t(Structure):
        pass
    
    class struct_std___Fake_proxy_ptr_impl(Structure):
        pass
    
    class struct_std___Invoker_pmd_pointer(Structure):
        pass
    
    class struct_std___Invoker_pmd_refwrap(Structure):
        pass
    
    class struct_std___Invoker_pmf_pointer(Structure):
        pass
    
    class struct_std___Invoker_pmf_refwrap(Structure):
        pass
    
    class struct_std___Leave_proxy_unbound(Structure):
        pass
    
    class struct_std___Rand_urng_from_func(Structure):
        pass
    
    class struct_std__bad_array_new_length(Structure):
        pass
    
    struct_std__bad_array_new_length._pack_ = 1 # source:False
    struct_std__bad_array_new_length._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_std__basic_ifstream_char_(Structure):
        pass
    
    class struct_std__basic_iostream_char_(Structure):
        pass
    
    class struct_std__basic_ofstream_char_(Structure):
        pass
    
    class struct_std__char_traits_wchar_t_(Structure):
        pass
    
    class struct_std__forward_iterator_tag(Structure):
        pass
    
    class struct_std__hash_std__nullptr_t_(Structure):
        pass
    
    class struct_std__numeric_limits_bool_(Structure):
        pass
    
    class struct_std__numeric_limits_char_(Structure):
        pass
    
    class struct_std__numeric_limits_long_(Structure):
        pass
    
    class struct___crt_locale_data_public(Structure):
        pass
    
    struct___crt_locale_data_public._pack_ = 1 # source:False
    struct___crt_locale_data_public._fields_ = [
        ('_locale_pctype', ctypes.POINTER(ctypes.c_uint16)),
        ('_locale_mb_cur_max', ctypes.c_int32),
        ('_locale_lc_codepage', ctypes.c_uint32),
    ]
    
    class struct_std___Alloc_exact_args_t(Structure):
        pass
    
    class struct_std___Invoker_pmd_object(Structure):
        pass
    
    class struct_std___Invoker_pmf_object(Structure):
        pass
    
    class struct_std___Is_character_char_(Structure):
        pass
    
    class struct_std___Move_allocator_tag(Structure):
        pass
    
    class struct_std__allocator_char16_t_(Structure):
        pass
    
    class struct_std__allocator_char32_t_(Structure):
        pass
    
    class struct_std__basic_filebuf_char_(Structure):
        pass
    
    class struct_std__basic_fstream_char_(Structure):
        pass
    
    class struct_std__basic_istream_char_(Structure):
        pass
    
    class struct_std__basic_ostream_char_(Structure):
        pass
    
    class struct_std__greater_equal_void_(Structure):
        pass
    
    class struct_std__numeric_limits_int_(Structure):
        pass
    
    class struct_std__output_iterator_tag(Structure):
        pass
    
    class struct__Real_type_long_double_(Structure):
        pass
    
    class struct_std___Make_unsigned2_1_(Structure):
        pass
    
    class struct_std___Make_unsigned2_2_(Structure):
        pass
    
    class struct_std___Make_unsigned2_4_(Structure):
        pass
    
    class struct_std___Make_unsigned2_8_(Structure):
        pass
    
    class struct_std__allocator_wchar_t_(Structure):
        pass
    
    class struct_std__bad_exception_vtbl(Structure):
        pass
    
    class struct_std__basic_ios_wchar_t_(Structure):
        pass
    
    class struct_std__basic_string_char_(Structure):
        _pack_ = 1 # source:False
        _fields_ = [
        ('_Mypair', struct_std___Compressed_pair_std__allocator_char___std___String_val_std___Simple_types_char____true_),
         ]
    
    class struct_std__input_iterator_tag(Structure):
        pass
    
    class struct_std__not_equal_to_void_(Structure):
        pass
    
    class struct_std___Container_base12(Structure):
        pass
    
    struct_std___Container_base12._pack_ = 1 # source:False
    struct_std___Container_base12._fields_ = [
        ('_Myproxy', ctypes.POINTER(struct_std___Container_proxy)),
    ]
    
    class struct_std___Default_sentinel(Structure):
        pass
    
    class struct_std___Distance_unknown(Structure):
        pass
    
    class struct_std___Equal_allocators(Structure):
        pass
    
    class struct_std___Unused_parameter(Structure):
        pass
    
    class struct_std__char_traits_char_(Structure):
        pass
    
    class struct_std__hash_long_double_(Structure):
        pass
    
    class struct___crt_locale_pointers(Structure):
        pass
    
    class struct___crt_multibyte_data(Structure):
        pass
    
    class struct___crt_locale_data(Structure):
        pass
    
    struct___crt_locale_pointers._pack_ = 1 # source:False
    struct___crt_locale_pointers._fields_ = [
        ('locinfo', ctypes.POINTER(struct___crt_locale_data)),
        ('mbcinfo', ctypes.POINTER(struct___crt_multibyte_data)),
    ]
    
    class struct_std___Container_base0(Structure):
        pass
    
    class struct_std___Iterator_base12(Structure):
        pass
    
    struct_std___Container_proxy._pack_ = 1 # source:False
    struct_std___Container_proxy._fields_ = [
        ('_Mycont', ctypes.POINTER(struct_std___Container_base12)),
        ('_Myfirstiter', ctypes.POINTER(struct_std___Iterator_base12)),
    ]
    
    class struct_std___Invoker_functor(Structure):
        pass
    
    struct_std___Iterator_base12._pack_ = 1 # source:False
    struct_std___Iterator_base12._fields_ = [
        ('_Myproxy', ctypes.POINTER(struct_std___Container_proxy)),
        ('_Mynextiter', ctypes.POINTER(struct_std___Iterator_base12)),
    ]
    
    class struct_std___Make_signed2_1_(Structure):
        pass
    
    class struct_std___Make_signed2_2_(Structure):
        pass
    
    class struct_std___Make_signed2_4_(Structure):
        pass
    
    class struct_std___Make_signed2_8_(Structure):
        pass
    
    class struct_std__less_equal_void_(Structure):
        pass
    
    class struct_std__multiplies_void_(Structure):
        pass
    
    class struct_std__nested_exception(Structure):
        pass
    
    class struct_std__exception_ptr(Structure):
        pass
    
    struct_std__exception_ptr._pack_ = 1 # source:False
    struct_std__exception_ptr._fields_ = [
        ('_Data1', ctypes.POINTER(None)),
        ('_Data2', ctypes.POINTER(None)),
    ]
    
    struct_std__nested_exception._pack_ = 1 # source:False
    struct_std__nested_exception._fields_ = [
        ('__vftable', ctypes.POINTER(struct_std__nested_exception_vtbl)),
        ('_Exc', struct_std__exception_ptr),
    ]
    
    class struct___std_exception_data(Structure):
        pass
    
    struct___std_exception_data._pack_ = 1 # source:False
    struct___std_exception_data._fields_ = [
        ('_What', ctypes.c_char_p),
        ('_DoFree', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct_std___Fake_allocator(Structure):
        pass
    
    class struct_std___False_copy_cat(Structure):
        pass
    
    class struct_std___Iterator_base0(Structure):
        pass
    
    class struct_std___Num_float_base(Structure):
        pass
    
    class struct_std___Unpack_tuple_t(Structure):
        pass
    
    class struct_std__allocator_char_(Structure):
        pass
    
    class struct_std__allocator_void_(Structure):
        pass
    
    class struct_std__allocator_arg_t(Structure):
        pass
    
    class struct_std__basic_ios_char_(Structure):
        pass
    
    class struct_std__fpos__Mbstatet_(Structure):
        pass
    
    struct_std__fpos__Mbstatet_._pack_ = 1 # source:False
    struct_std__fpos__Mbstatet_._fields_ = [
        ('_Myoff', ctypes.c_int64),
        ('_Fpos', ctypes.c_int64),
        ('_Mystate', ctypes.c_char),
        ('PADDING_0', ctypes.c_ubyte * 7),
    ]
    
    class struct__EXCEPTION_POINTERS(Structure):
        pass
    
    class struct_std___Select_false_(Structure):
        pass
    
    class struct_std__bad_alloc_vtbl(Structure):
        pass
    
    class struct_std__equal_to_void_(Structure):
        pass
    
    class struct_std__exception_vtbl(Structure):
        pass
    
    class struct__CrtMemBlockHeader(Structure):
        pass
    
    class struct_std___Exact_args_t(Structure):
        pass
    
    class struct_std___Num_int_base(Structure):
        pass
    
    class struct_std__bad_exception(Structure):
        pass
    
    struct_std__bad_exception._pack_ = 1 # source:False
    struct_std__bad_exception._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_std__common_type__(Structure):
        pass
    
    class struct_std__greater_void_(Structure):
        pass
    
    class struct__Real_type_float_(Structure):
        pass
    
    class struct__wfinddata32i64_t(Structure):
        pass
    
    struct__wfinddata32i64_t._pack_ = 1 # source:False
    struct__wfinddata32i64_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('time_create', ctypes.c_int32),
        ('time_access', ctypes.c_int32),
        ('time_write', ctypes.c_int32),
        ('size', ctypes.c_int64),
        ('name', ctypes.c_int16 * 260),
    ]
    
    class struct__wfinddata64i32_t(Structure):
        pass
    
    struct__wfinddata64i32_t._pack_ = 1 # source:False
    struct__wfinddata64i32_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('time_create', ctypes.c_int64),
        ('time_access', ctypes.c_int64),
        ('time_write', ctypes.c_int64),
        ('size', ctypes.c_uint32),
        ('name', ctypes.c_int16 * 260),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct_std__hash_double_(Structure):
        pass
    
    class struct__finddata32i64_t(Structure):
        pass
    
    struct__finddata32i64_t._pack_ = 1 # source:False
    struct__finddata32i64_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('time_create', ctypes.c_int32),
        ('time_access', ctypes.c_int32),
        ('time_write', ctypes.c_int32),
        ('size', ctypes.c_int64),
        ('name', ctypes.c_char * 260),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct__finddata64i32_t(Structure):
        pass
    
    struct__finddata64i32_t._pack_ = 1 # source:False
    struct__finddata64i32_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('time_create', ctypes.c_int64),
        ('time_access', ctypes.c_int64),
        ('time_write', ctypes.c_int64),
        ('size', ctypes.c_uint32),
        ('name', ctypes.c_char * 260),
    ]
    
    class struct_std___Init_locks(Structure):
        pass
    
    class struct_std__hash_float_(Structure):
        pass
    
    class struct_std__minus_void_(Structure):
        pass
    
    class struct_std___Maximum__(Structure):
        pass
    
    class struct_std__less_void_(Structure):
        pass
    
    class struct_std__plus_void_(Structure):
        pass
    
    class struct___finddata64_t(Structure):
        pass
    
    struct___finddata64_t._pack_ = 1 # source:False
    struct___finddata64_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('time_create', ctypes.c_int64),
        ('time_access', ctypes.c_int64),
        ('time_write', ctypes.c_int64),
        ('size', ctypes.c_int64),
        ('name', ctypes.c_char * 260),
        ('PADDING_1', ctypes.c_ubyte * 4),
    ]
    
    class struct__wfinddata32_t(Structure):
        pass
    
    struct__wfinddata32_t._pack_ = 1 # source:False
    struct__wfinddata32_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('time_create', ctypes.c_int32),
        ('time_access', ctypes.c_int32),
        ('time_write', ctypes.c_int32),
        ('size', ctypes.c_uint32),
        ('name', ctypes.c_int16 * 260),
    ]
    
    class struct__wfinddata64_t(Structure):
        pass
    
    struct__wfinddata64_t._pack_ = 1 # source:False
    struct__wfinddata64_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('time_create', ctypes.c_int64),
        ('time_access', ctypes.c_int64),
        ('time_write', ctypes.c_int64),
        ('size', ctypes.c_int64),
        ('name', ctypes.c_int16 * 260),
    ]
    
    class struct_std___Num_base(Structure):
        pass
    
    class struct_std__bad_alloc(Structure):
        pass
    
    struct_std__bad_alloc._pack_ = 1 # source:False
    struct_std__bad_alloc._fields_ = [
        ('PADDING_0', ctypes.c_ubyte * 24),
    ]
    
    class struct_std__exception(Structure):
        pass
    
    struct_std__exception._pack_ = 1 # source:False
    struct_std__exception._fields_ = [
        ('__vftable', ctypes.POINTER(struct_std__exception_vtbl)),
        ('_Data', struct___std_exception_data),
    ]
    
    class struct_std__nothrow_t(Structure):
        pass
    
    class struct__finddata32_t(Structure):
        pass
    
    struct__finddata32_t._pack_ = 1 # source:False
    struct__finddata32_t._fields_ = [
        ('attrib', ctypes.c_uint32),
        ('time_create', ctypes.c_int32),
        ('time_access', ctypes.c_int32),
        ('time_write', ctypes.c_int32),
        ('size', ctypes.c_uint32),
        ('name', ctypes.c_char * 260),
    ]
    
    class struct_std__ios_base(Structure):
        pass
    
    class struct__CrtMemState(Structure):
        pass
    
    struct__CrtMemState._pack_ = 1 # source:False
    struct__CrtMemState._fields_ = [
        ('pBlockHeader', ctypes.POINTER(struct__CrtMemBlockHeader)),
        ('lCounts', ctypes.c_uint64 * 5),
        ('lSizes', ctypes.c_uint64 * 5),
        ('lHighWaterCount', ctypes.c_uint64),
        ('lTotalCount', ctypes.c_uint64),
    ]
    
    class struct_std___Ignore(Structure):
        pass
    
    class struct_std___Lockit(Structure):
        pass
    
    struct_std___Lockit._pack_ = 1 # source:False
    struct_std___Lockit._fields_ = [
        ('_Locktype', ctypes.c_int32),
    ]
    
    class struct_std__tuple__(Structure):
        pass
    
    class struct__CRT_DOUBLE(Structure):
        pass
    
    struct__CRT_DOUBLE._pack_ = 1 # source:False
    struct__CRT_DOUBLE._fields_ = [
        ('x', ctypes.c_double),
    ]
    
    class struct__LONGDOUBLE(Structure):
        pass
    
    struct__LONGDOUBLE._pack_ = 1 # source:False
    struct__LONGDOUBLE._fields_ = [
        ('x', ctypes.c_double),
    ]
    
    class struct__diskfree_t(Structure):
        pass
    
    struct__diskfree_t._pack_ = 1 # source:False
    struct__diskfree_t._fields_ = [
        ('total_clusters', ctypes.c_uint32),
        ('avail_clusters', ctypes.c_uint32),
        ('sectors_per_cluster', ctypes.c_uint32),
        ('bytes_per_sector', ctypes.c_uint32),
    ]
    
    class struct__timespec32(Structure):
        pass
    
    struct__timespec32._pack_ = 1 # source:False
    struct__timespec32._fields_ = [
        ('tv_sec', ctypes.c_int32),
        ('tv_nsec', ctypes.c_int32),
    ]
    
    class struct__timespec64(Structure):
        pass
    
    struct__timespec64._pack_ = 1 # source:False
    struct__timespec64._fields_ = [
        ('tv_sec', ctypes.c_int64),
        ('tv_nsec', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_std__locale(Structure):
        pass
    
    class struct__CRT_FLOAT(Structure):
        pass
    
    struct__CRT_FLOAT._pack_ = 1 # source:False
    struct__CRT_FLOAT._fields_ = [
        ('f', ctypes.c_float),
    ]
    
    class struct__exception(Structure):
        pass
    
    struct__exception._pack_ = 1 # source:False
    struct__exception._fields_ = [
        ('type', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
        ('name', ctypes.c_char_p),
        ('arg1', ctypes.c_double),
        ('arg2', ctypes.c_double),
        ('retval', ctypes.c_double),
    ]
    
    class struct__stat32i64(Structure):
        pass
    
    struct__stat32i64._pack_ = 1 # source:False
    struct__stat32i64._fields_ = [
        ('st_dev', ctypes.c_uint32),
        ('st_ino', ctypes.c_uint16),
        ('st_mode', ctypes.c_uint16),
        ('st_nlink', ctypes.c_int16),
        ('st_uid', ctypes.c_int16),
        ('st_gid', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('st_rdev', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('st_size', ctypes.c_int64),
        ('st_atime', ctypes.c_int32),
        ('st_mtime', ctypes.c_int32),
        ('st_ctime', ctypes.c_int32),
        ('PADDING_2', ctypes.c_ubyte * 4),
    ]
    
    class struct__stat64i32(Structure):
        pass
    
    struct__stat64i32._pack_ = 1 # source:False
    struct__stat64i32._fields_ = [
        ('st_dev', ctypes.c_uint32),
        ('st_ino', ctypes.c_uint16),
        ('st_mode', ctypes.c_uint16),
        ('st_nlink', ctypes.c_int16),
        ('st_uid', ctypes.c_int16),
        ('st_gid', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('st_rdev', ctypes.c_uint32),
        ('st_size', ctypes.c_int32),
        ('st_atime', ctypes.c_int64),
        ('st_mtime', ctypes.c_int64),
        ('st_ctime', ctypes.c_int64),
    ]
    
    class struct__heapinfo(Structure):
        pass
    
    struct__heapinfo._pack_ = 1 # source:False
    struct__heapinfo._fields_ = [
        ('_pentry', ctypes.POINTER(ctypes.c_int32)),
        ('_size', ctypes.c_uint64),
        ('_useflag', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct_type_info(Structure):
        pass
    
    class struct__LDOUBLE(Structure):
        pass
    
    struct__LDOUBLE._pack_ = 1 # source:False
    struct__LDOUBLE._fields_ = [
        ('ld', ctypes.c_ubyte * 10),
    ]
    
    class struct__complex(Structure):
        pass
    
    struct__complex._pack_ = 1 # source:False
    struct__complex._fields_ = [
        ('x', ctypes.c_double),
        ('y', ctypes.c_double),
    ]
    
    class struct__lldiv_t(Structure):
        pass
    
    struct__lldiv_t._pack_ = 1 # source:False
    struct__lldiv_t._fields_ = [
        ('quot', ctypes.c_int64),
        ('rem', ctypes.c_int64),
    ]
    
    class struct_timespec(Structure):
        pass
    
    struct_timespec._pack_ = 1 # source:False
    struct_timespec._fields_ = [
        ('tv_sec', ctypes.c_int64),
        ('tv_nsec', ctypes.c_int32),
        ('PADDING_0', ctypes.c_ubyte * 4),
    ]
    
    class struct__LDBL12(Structure):
        pass
    
    struct__LDBL12._pack_ = 1 # source:False
    struct__LDBL12._fields_ = [
        ('ld12', ctypes.c_ubyte * 12),
    ]
    
    class struct__ldiv_t(Structure):
        pass
    
    struct__ldiv_t._pack_ = 1 # source:False
    struct__ldiv_t._fields_ = [
        ('quot', ctypes.c_int32),
        ('rem', ctypes.c_int32),
    ]
    
    class struct__stat32(Structure):
        pass
    
    struct__stat32._pack_ = 1 # source:False
    struct__stat32._fields_ = [
        ('st_dev', ctypes.c_uint32),
        ('st_ino', ctypes.c_uint16),
        ('st_mode', ctypes.c_uint16),
        ('st_nlink', ctypes.c_int16),
        ('st_uid', ctypes.c_int16),
        ('st_gid', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('st_rdev', ctypes.c_uint32),
        ('st_size', ctypes.c_int32),
        ('st_atime', ctypes.c_int32),
        ('st_mtime', ctypes.c_int32),
        ('st_ctime', ctypes.c_int32),
    ]
    
    class struct__stat64(Structure):
        pass
    
    struct__stat64._pack_ = 1 # source:False
    struct__stat64._fields_ = [
        ('st_dev', ctypes.c_uint32),
        ('st_ino', ctypes.c_uint16),
        ('st_mode', ctypes.c_uint16),
        ('st_nlink', ctypes.c_int16),
        ('st_uid', ctypes.c_int16),
        ('st_gid', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('st_rdev', ctypes.c_uint32),
        ('PADDING_1', ctypes.c_ubyte * 4),
        ('st_size', ctypes.c_int64),
        ('st_atime', ctypes.c_int64),
        ('st_mtime', ctypes.c_int64),
        ('st_ctime', ctypes.c_int64),
    ]
    
    class struct__div_t(Structure):
        pass
    
    struct__div_t._pack_ = 1 # source:False
    struct__div_t._fields_ = [
        ('quot', ctypes.c_int32),
        ('rem', ctypes.c_int32),
    ]
    
    class struct__iobuf(Structure):
        pass
    
    struct__iobuf._pack_ = 1 # source:False
    struct__iobuf._fields_ = [
        ('_Placeholder', ctypes.POINTER(None)),
    ]
    
    class struct_stat(Structure):
        pass
    
    struct_stat._pack_ = 1 # source:False
    struct_stat._fields_ = [
        ('st_dev', ctypes.c_uint32),
        ('st_ino', ctypes.c_uint16),
        ('st_mode', ctypes.c_uint16),
        ('st_nlink', ctypes.c_int16),
        ('st_uid', ctypes.c_int16),
        ('st_gid', ctypes.c_int16),
        ('PADDING_0', ctypes.c_ubyte * 2),
        ('st_rdev', ctypes.c_uint32),
        ('st_size', ctypes.c_int32),
        ('st_atime', ctypes.c_int64),
        ('st_mtime', ctypes.c_int64),
        ('st_ctime', ctypes.c_int64),
    ]
    
    class struct_tm(Structure):
        pass
    
    struct_tm._pack_ = 1 # source:False
    struct_tm._fields_ = [
        ('tm_sec', ctypes.c_int32),
        ('tm_min', ctypes.c_int32),
        ('tm_hour', ctypes.c_int32),
        ('tm_mday', ctypes.c_int32),
        ('tm_mon', ctypes.c_int32),
        ('tm_year', ctypes.c_int32),
        ('tm_wday', ctypes.c_int32),
        ('tm_yday', ctypes.c_int32),
        ('tm_isdst', ctypes.c_int32),
    ]
    
    std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____ = ctypes.c_int64
    std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____ = ctypes.c_int64
    std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____ = ctypes.c_int64
    std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____ = ctypes.POINTER(ctypes.c_int16)
    std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____ = ctypes.POINTER(ctypes.c_int32)
    std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____ = ctypes.POINTER(ctypes.c_int16)
    std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char____ = ctypes.c_int64
    std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char____ = ctypes.c_char_p
    std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char16_t____ = ctypes.c_int64
    std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char32_t____ = ctypes.c_int64
    std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_wchar_t____ = ctypes.c_int64
    std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char16_t____ = ctypes.POINTER(ctypes.c_int16)
    std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char32_t____ = ctypes.POINTER(ctypes.c_int32)
    std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_wchar_t____ = ctypes.POINTER(ctypes.c_int16)
    std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char____ = ctypes.c_int64
    std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char____ = ctypes.c_char_p
    std___Char_traits_unsigned_short__unsigned_short___int_type = ctypes.c_uint16
    std__integral_constant_unsigned_long_long__0___value_type = ctypes.c_uint64
    std___Char_traits_char16_t__unsigned_short___int_type = ctypes.c_uint16
    std___Char_traits_wchar_t__unsigned_short___int_type = ctypes.c_uint16
    std___Char_traits_char32_t__unsigned_int___int_type = ctypes.c_uint32
    std__integral_constant_bool__false___value_type = ctypes.c_char
    std__integral_constant_bool__true___value_type = ctypes.c_char
    std___Narrow_char_traits_char__int___int_type = ctypes.c_int32
    std___WChar_traits_unsigned_short___int_type = ctypes.c_uint16
    _CoreCrtNonSecureSearchSortCompareFunction = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None))
    std___Simple_types_char16_t___value_type = ctypes.c_int16
    std___Simple_types_char32_t___value_type = ctypes.c_int32
    _CoreCrtSecureSearchSortCompareFunction = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None))
    std___Simple_types_wchar_t___value_type = ctypes.c_int16
    std__basic_string_char16_t___value_type = ctypes.c_int16
    std__basic_string_char32_t___value_type = ctypes.c_int32
    std___Char_traits_char__int___int_type = ctypes.c_int32
    std___Rand_urng_from_func__result_type = ctypes.c_uint32
    std___WChar_traits_char16_t___int_type = ctypes.c_uint16
    std__basic_string_wchar_t___value_type = ctypes.c_int16
    std___WChar_traits_wchar_t___int_type = ctypes.c_uint16
    std___Simple_types_char___value_type = ctypes.c_char
    std___WChar_traits__Elem___int_type = ctypes.c_uint16
    std__basic_string_char___value_type = ctypes.c_char
    _se_translator_function = ctypes.CFUNCTYPE(None, ctypes.c_uint32, ctypes.POINTER(struct__EXCEPTION_POINTERS))
    
    # values for enumeration 'std__float_denorm_style'
    std__float_denorm_style__enumvalues = {
        4294967295: 'denorm_indeterminate',
        0: 'denorm_absent',
        1: 'denorm_present',
    }
    denorm_indeterminate = 4294967295
    denorm_absent = 0
    denorm_present = 1
    std__float_denorm_style = ctypes.c_uint32 # enum
    std___Atomic_counter_t = ctypes.c_uint32
    
    # values for enumeration 'std___Invoker_strategy'
    std___Invoker_strategy__enumvalues = {
        0: '_Functor',
        1: '_Pmf_object',
        2: '_Pmf_refwrap',
        3: '_Pmf_pointer',
        4: '_Pmd_object',
        5: '_Pmd_refwrap',
        6: '_Pmd_pointer',
    }
    _Functor = 0
    _Pmf_object = 1
    _Pmf_refwrap = 2
    _Pmf_pointer = 3
    _Pmd_object = 4
    _Pmd_refwrap = 5
    _Pmd_pointer = 6
    std___Invoker_strategy = ctypes.c_uint32 # enum
    
    # values for enumeration 'std__float_round_style'
    std__float_round_style__enumvalues = {
        4294967295: 'round_indeterminate',
        0: 'round_toward_zero',
        1: 'round_to_nearest',
        2: 'round_toward_infinity',
        3: 'round_toward_neg_infinity',
    }
    round_indeterminate = 4294967295
    round_toward_zero = 0
    round_to_nearest = 1
    round_toward_infinity = 2
    round_toward_neg_infinity = 3
    std__float_round_style = ctypes.c_uint32 # enum
    
    # values for enumeration 'std___Uninitialized'
    std___Uninitialized__enumvalues = {
        0: '_Noinit',
    }
    _Noinit = 0
    std___Uninitialized = ctypes.c_uint32 # enum
    unexpected_function = ctypes.CFUNCTYPE(None)
    terminate_function = ctypes.CFUNCTYPE(None)
    unexpected_handler = ctypes.CFUNCTYPE(None)
    _CRT_REPORT_HOOKW = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int32))
    _purecall_handler = ctypes.CFUNCTYPE(None)
    
    # values for enumeration 'std__memory_order'
    std__memory_order__enumvalues = {
        0: 'memory_order_relaxed',
        1: 'memory_order_consume',
        2: 'memory_order_acquire',
        3: 'memory_order_release',
        4: 'memory_order_acq_rel',
        5: 'memory_order_seq_cst',
    }
    memory_order_relaxed = 0
    memory_order_consume = 1
    memory_order_acquire = 2
    memory_order_release = 3
    memory_order_acq_rel = 4
    memory_order_seq_cst = 5
    std__memory_order = ctypes.c_uint32 # enum
    terminate_handler = ctypes.CFUNCTYPE(None)
    
    # values for enumeration 'ISA_AVAILABILITY'
    ISA_AVAILABILITY__enumvalues = {
        0: '__ISA_AVAILABLE_X86',
        1: '__ISA_AVAILABLE_SSE2',
        2: '__ISA_AVAILABLE_SSE42',
        3: '__ISA_AVAILABLE_AVX',
        4: '__ISA_AVAILABLE_ENFSTRG',
        5: '__ISA_AVAILABLE_AVX2',
        6: '__ISA_AVAILABLE_AVX512',
        0: '__ISA_AVAILABLE_ARMNT',
        1: '__ISA_AVAILABLE_NEON',
        2: '__ISA_AVAILABLE_NEON_ARM64',
    }
    __ISA_AVAILABLE_X86 = 0
    __ISA_AVAILABLE_SSE2 = 1
    __ISA_AVAILABLE_SSE42 = 2
    __ISA_AVAILABLE_AVX = 3
    __ISA_AVAILABLE_ENFSTRG = 4
    __ISA_AVAILABLE_AVX2 = 5
    __ISA_AVAILABLE_AVX512 = 6
    __ISA_AVAILABLE_ARMNT = 0
    __ISA_AVAILABLE_NEON = 1
    __ISA_AVAILABLE_NEON_ARM64 = 2
    ISA_AVAILABILITY = ctypes.c_uint32 # enum
    _CRT_REPORT_HOOK = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32))
    
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
    std__max_align_t = ctypes.c_double
    std__new_handler = ctypes.CFUNCTYPE(None)
    std__streamsize = ctypes.c_int64
    std__nullptr_t = ctypes.c_int64
    std__streamoff = ctypes.c_int64
    uint_least16_t = ctypes.c_uint16
    uint_least32_t = ctypes.c_uint32
    uint_least64_t = ctypes.c_uint64
    int_least16_t = ctypes.c_int16
    int_least32_t = ctypes.c_int32
    int_least64_t = ctypes.c_int64
    uint_fast16_t = ctypes.c_uint32
    uint_fast32_t = ctypes.c_uint32
    uint_fast64_t = ctypes.c_uint64
    uint_least8_t = ctypes.c_ubyte
    class union__float_const(Union):
        pass
    
    union__float_const._pack_ = 1 # source:False
    union__float_const._fields_ = [
        ('_Word', ctypes.c_uint16 * 4),
        ('_Float', ctypes.c_float),
        ('_Double', ctypes.c_double),
        ('_Long_double', ctypes.c_double),
    ]
    
    class union__ldouble_val(Union):
        pass
    
    union__ldouble_val._pack_ = 1 # source:False
    union__ldouble_val._fields_ = [
        ('_Sh', ctypes.c_uint16 * 4),
        ('_Val', ctypes.c_double),
    ]
    
    int_fast16_t = ctypes.c_int32
    int_fast32_t = ctypes.c_int32
    int_fast64_t = ctypes.c_int64
    int_least8_t = ctypes.c_char
    uint_fast8_t = ctypes.c_ubyte
    __vcrt_bool = ctypes.c_char
    class union__double_val(Union):
        pass
    
    union__double_val._pack_ = 1 # source:False
    union__double_val._fields_ = [
        ('_Sh', ctypes.c_uint16 * 4),
        ('_Val', ctypes.c_double),
    ]
    
    int_fast8_t = ctypes.c_char
    __crt_bool = ctypes.c_char
    __time32_t = ctypes.c_int32
    __time64_t = ctypes.c_int64
    class union__float_val(Union):
        pass
    
    union__float_val._pack_ = 1 # source:False
    union__float_val._fields_ = [
        ('_Sh', ctypes.c_uint16 * 2),
        ('_Val', ctypes.c_float),
    ]
    
    _locale_t = ctypes.POINTER(struct___crt_locale_pointers)
    _onexit_t = ctypes.CFUNCTYPE(ctypes.c_int32)
    mbstate_t = ctypes.c_char
    ptrdiff_t = ctypes.c_int64
    uintmax_t = ctypes.c_uint64
    uintptr_t = ctypes.c_uint64
    _fsize_t = ctypes.c_uint32
    double_t = ctypes.c_double
    intmax_t = ctypes.c_int64
    intptr_t = ctypes.c_int64
    wctype_t = ctypes.c_uint16
    _Wint_t = ctypes.c_int16
    clock_t = ctypes.c_int32
    errno_t = ctypes.c_int32
    float_t = ctypes.c_float
    int16_t = ctypes.c_int16
    int32_t = ctypes.c_int32
    int64_t = ctypes.c_int64
    _HFILE = ctypes.POINTER(None)
    _dev_t = ctypes.c_uint32
    _ino_t = ctypes.c_uint16
    _off_t = ctypes.c_int32
    fpos_t = ctypes.c_int64
    int8_t = ctypes.c_int8
    size_t = ctypes.c_uint64
    wint_t = ctypes.c_uint16
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______reference = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______reference = ctypes.POINTER(ctypes.c_int32)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______reference = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______reference = ctypes.c_char_p
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______difference_type = ctypes.c_int64
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______reference = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______reference = ctypes.POINTER(ctypes.c_int32)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______reference = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______reference = ctypes.c_char_p
    std___Default_allocator_traits_std__allocator_char16_t____size_type = ctypes.c_uint64
    std___Default_allocator_traits_std__allocator_char32_t____size_type = ctypes.c_uint64
    std___Default_allocator_traits_std__allocator_wchar_t____size_type = ctypes.c_uint64
    std___Default_allocator_traits_std__allocator_char____size_type = ctypes.c_uint64
    std___String_val_std___Simple_types_char16_t____value_type = ctypes.c_int16
    std___String_val_std___Simple_types_char32_t____value_type = ctypes.c_int32
    std___String_val_std___Simple_types_wchar_t____value_type = ctypes.c_int16
    std___String_val_std___Simple_types_char____value_type = ctypes.c_char
    std___Simple_types_char16_t___difference_type = ctypes.c_int64
    std___Simple_types_char32_t___difference_type = ctypes.c_int64
    std___Simple_types_wchar_t___difference_type = ctypes.c_int64
    std__basic_string_char16_t___const_reference = ctypes.POINTER(ctypes.c_int16)
    std__basic_string_char32_t___const_reference = ctypes.POINTER(ctypes.c_int32)
    std___Simple_types_char16_t___const_pointer = ctypes.POINTER(ctypes.c_int16)
    std___Simple_types_char32_t___const_pointer = ctypes.POINTER(ctypes.c_int32)
    std__basic_string_char16_t___allocator_type = struct_std__allocator_char16_t_
    std__basic_string_char32_t___allocator_type = struct_std__allocator_char32_t_
    std__basic_string_wchar_t___const_reference = ctypes.POINTER(ctypes.c_int16)
    std___Simple_types_wchar_t___const_pointer = ctypes.POINTER(ctypes.c_int16)
    std__basic_string_wchar_t___allocator_type = struct_std__allocator_wchar_t_
    std___Simple_types_char___difference_type = ctypes.c_int64
    std__basic_string_char___const_reference = ctypes.c_char_p
    std___Simple_types_char16_t___size_type = ctypes.c_uint64
    std___Simple_types_char32_t___size_type = ctypes.c_uint64
    std___Simple_types_char___const_pointer = ctypes.c_char_p
    std__basic_string_char___allocator_type = struct_std__allocator_char_
    std___Simple_types_wchar_t___size_type = ctypes.c_uint64
    std__basic_string_char16_t___reference = ctypes.POINTER(ctypes.c_int16)
    std__basic_string_char16_t___size_type = ctypes.c_uint64
    std__basic_string_char32_t___reference = ctypes.POINTER(ctypes.c_int32)
    std__basic_string_char32_t___size_type = ctypes.c_uint64
    std___Simple_types_char16_t___pointer = ctypes.POINTER(ctypes.c_int16)
    std___Simple_types_char32_t___pointer = ctypes.POINTER(ctypes.c_int32)
    std__basic_string_wchar_t___reference = ctypes.POINTER(ctypes.c_int16)
    std__basic_string_wchar_t___size_type = ctypes.c_uint64
    std___Simple_types_wchar_t___pointer = ctypes.POINTER(ctypes.c_int16)
    std___Simple_types_char___size_type = ctypes.c_uint64
    std__basic_string_char16_t____Alty = struct_std__allocator_char16_t_
    std__basic_string_char32_t____Alty = struct_std__allocator_char32_t_
    std__basic_string_char___reference = ctypes.c_char_p
    std__basic_string_char___size_type = ctypes.c_uint64
    std___Simple_types_char___pointer = ctypes.c_char_p
    std__basic_string_wchar_t____Alty = struct_std__allocator_wchar_t_
    std__basic_string_char____Alty = struct_std__allocator_char_
    _invalid_parameter_handler = ctypes.CFUNCTYPE(None, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.c_uint32, ctypes.c_uint64)
    std___Container_base = struct_std___Container_base0
    std___Iterator_base = struct_std___Iterator_base0
    std__wistringstream = struct_std__basic_istringstream_wchar_t_
    std__wostringstream = struct_std__basic_ostringstream_wchar_t_
    std__istringstream = struct_std__basic_istringstream_char_
    std__ostringstream = struct_std__basic_ostringstream_char_
    std__wstringstream = struct_std__basic_stringstream_wchar_t_
    std__stringstream = struct_std__basic_stringstream_char_
    _CRT_DUMP_CLIENT = ctypes.CFUNCTYPE(None, ctypes.POINTER(None), ctypes.c_uint64)
    _CRT_ALLOC_HOOK = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(None), ctypes.c_uint64, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int32)
    std__false_type = struct_std__integral_constant_bool__false_
    std__wstreambuf = struct_std__basic_streambuf_wchar_t_
    std__wstringbuf = struct_std__basic_stringbuf_wchar_t_
    std__streambuf = struct_std__basic_streambuf_char_
    std__stringbuf = struct_std__basic_stringbuf_char_
    std__true_type = struct_std__integral_constant_bool__true_
    std__wifstream = struct_std__basic_ifstream_wchar_t_
    std__wiostream = struct_std__basic_iostream_wchar_t_
    std__wofstream = struct_std__basic_ofstream_wchar_t_
    std___Any_tag = struct_std___Unused_parameter
    std__ifstream = struct_std__basic_ifstream_char_
    std__iostream = struct_std__basic_iostream_char_
    std__ofstream = struct_std__basic_ofstream_char_
    std__wfilebuf = struct_std__basic_filebuf_wchar_t_
    std__wfstream = struct_std__basic_fstream_wchar_t_
    std__wistream = struct_std__basic_istream_wchar_t_
    std__wostream = struct_std__basic_ostream_wchar_t_
    std__filebuf = struct_std__basic_filebuf_char_
    std__fstream = struct_std__basic_fstream_char_
    std__istream = struct_std__basic_istream_char_
    std__ostream = struct_std__basic_ostream_char_
    std__wios = struct_std__basic_ios_wchar_t_
    std__ios = struct_std__basic_ios_char_
    lldiv_t = struct__lldiv_t
    rsize_t = ctypes.c_uint64
    ldiv_t = struct__ldiv_t
    time_t = ctypes.c_int64
    dev_t = ctypes.c_uint32
    div_t = struct__div_t
    ino_t = ctypes.c_uint16
    off_t = ctypes.c_int32
    FILE = struct__iobuf
    std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____value_type = ctypes.c_int16
    std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____value_type = ctypes.c_int32
    std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____reference = ctypes.POINTER(ctypes.c_int16)
    std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____reference = ctypes.POINTER(ctypes.c_int32)
    std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____value_type = ctypes.c_int16
    std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____reference = ctypes.POINTER(ctypes.c_int16)
    std___String_const_iterator_std___String_val_std___Simple_types_char_____value_type = ctypes.c_char
    std___String_const_iterator_std___String_val_std___Simple_types_char_____reference = ctypes.c_char_p
    std___String_iterator_std___String_val_std___Simple_types_char16_t_____value_type = ctypes.c_int16
    std___String_iterator_std___String_val_std___Simple_types_char32_t_____value_type = ctypes.c_int32
    std___String_iterator_std___String_val_std___Simple_types_char16_t_____reference = ctypes.POINTER(ctypes.c_int16)
    std___String_iterator_std___String_val_std___Simple_types_char32_t_____reference = ctypes.POINTER(ctypes.c_int32)
    std___String_iterator_std___String_val_std___Simple_types_wchar_t_____value_type = ctypes.c_int16
    std___String_iterator_std___String_val_std___Simple_types_wchar_t_____reference = ctypes.POINTER(ctypes.c_int16)
    std___String_iterator_std___String_val_std___Simple_types_char_____value_type = ctypes.c_char
    std___String_iterator_std___String_val_std___Simple_types_char_____reference = ctypes.c_char_p
    std___String_val_std___Simple_types_char16_t____difference_type = ctypes.c_int64
    std___String_val_std___Simple_types_char32_t____difference_type = ctypes.c_int64
    std___String_val_std___Simple_types_wchar_t____difference_type = ctypes.c_int64
    std___String_val_std___Simple_types_char16_t____const_pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_val_std___Simple_types_char32_t____const_pointer = ctypes.POINTER(ctypes.c_int32)
    std___String_val_std___Simple_types_wchar_t____const_pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_val_std___Simple_types_char____difference_type = ctypes.c_int64
    std___String_val_std___Simple_types_char16_t____size_type = ctypes.c_uint64
    std___String_val_std___Simple_types_char32_t____size_type = ctypes.c_uint64
    std___String_val_std___Simple_types_char____const_pointer = ctypes.c_char_p
    std___String_val_std___Simple_types_wchar_t____size_type = ctypes.c_uint64
    std___String_val_std___Simple_types_char16_t____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_val_std___Simple_types_char32_t____pointer = ctypes.POINTER(ctypes.c_int32)
    std___String_val_std___Simple_types_wchar_t____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_val_std___Simple_types_char____size_type = ctypes.c_uint64
    std___String_val_std___Simple_types_char____pointer = ctypes.c_char_p
    std___No_propagate_allocators = struct_std__integral_constant_bool__false_
    std___Propagate_allocators = struct_std__integral_constant_bool__true_
    std__streampos = struct_std__fpos__Mbstatet_
    _HEAPINFO = struct__heapinfo
    std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____difference_type = ctypes.c_int64
    std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____difference_type = ctypes.c_int64
    std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____difference_type = ctypes.c_int64
    std___String_const_iterator_std___String_val_std___Simple_types_char_____difference_type = ctypes.c_int64
    std___String_iterator_std___String_val_std___Simple_types_char16_t_____difference_type = ctypes.c_int64
    std___String_iterator_std___String_val_std___Simple_types_char32_t_____difference_type = ctypes.c_int64
    std___String_iterator_std___String_val_std___Simple_types_wchar_t_____difference_type = ctypes.c_int64
    std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____pointer = ctypes.POINTER(ctypes.c_int32)
    std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_iterator_std___String_val_std___Simple_types_char_____difference_type = ctypes.c_int64
    std___String_const_iterator_std___String_val_std___Simple_types_char_____pointer = ctypes.c_char_p
    std___String_iterator_std___String_val_std___Simple_types_char16_t_____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_iterator_std___String_val_std___Simple_types_char32_t_____pointer = ctypes.POINTER(ctypes.c_int32)
    std___String_iterator_std___String_val_std___Simple_types_wchar_t_____pointer = ctypes.POINTER(ctypes.c_int16)
    std___String_iterator_std___String_val_std___Simple_types_char_____pointer = ctypes.c_char_p
    std__basic_string_char16_t____Scary_val = struct_std___String_val_std___Simple_types_char16_t__
    std__basic_string_char32_t____Scary_val = struct_std___String_val_std___Simple_types_char32_t__
    std__basic_string_wchar_t____Scary_val = struct_std___String_val_std___Simple_types_wchar_t__
    std__basic_string_char____Scary_val = struct_std___String_val_std___Simple_types_char__
    std__u16streampos = struct_std__fpos__Mbstatet_
    std__u32streampos = struct_std__fpos__Mbstatet_
    std__wstreampos = struct_std__fpos__Mbstatet_
    std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______pointer = ctypes.POINTER(ctypes.c_int32)
    std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char______pointer = ctypes.c_char_p
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______pointer = ctypes.POINTER(ctypes.c_int32)
    std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char16_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char32_t______pointer = ctypes.POINTER(ctypes.c_int32)
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_wchar_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______pointer = ctypes.c_char_p
    std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char______pointer = ctypes.c_char_p
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______pointer = ctypes.POINTER(ctypes.c_int32)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______pointer = ctypes.POINTER(ctypes.c_int16)
    std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______pointer = ctypes.c_char_p
    std__basic_string_char16_t___const_reverse_iterator = struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____
    std__basic_string_char32_t___const_reverse_iterator = struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____
    std__basic_string_wchar_t___const_reverse_iterator = struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____
    std__basic_string_char___const_reverse_iterator = struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char____
    std__basic_string_char16_t___const_iterator = struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___
    std__basic_string_char32_t___const_iterator = struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___
    std__basic_string_wchar_t___const_iterator = struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___
    std__basic_string_char___const_iterator = struct_std___String_const_iterator_std___String_val_std___Simple_types_char___
    std__basic_string_char16_t___iterator = struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___
    std__basic_string_char32_t___iterator = struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___
    std__basic_string_wchar_t___iterator = struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___
    std__basic_string_char___iterator = struct_std___String_iterator_std___String_val_std___Simple_types_char___
    std__u16string = struct_std__basic_string_char16_t_
    std__u32string = struct_std__basic_string_char32_t_
    std__wstring = struct_std__basic_string_wchar_t_
    std__string = struct_std__basic_string_char_
    std__basic_string_char16_t___reverse_iterator = struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t____
    std__basic_string_char32_t___reverse_iterator = struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t____
    std__basic_string_wchar_t___reverse_iterator = struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t____
    std__basic_string_char___reverse_iterator = struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char____
    BitScanForward = _libraries['FIXME_STUB'].BitScanForward
    BitScanForward.restype = ctypes.c_ubyte
    BitScanForward.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
    BitScanForward64 = _libraries['FIXME_STUB'].BitScanForward64
    BitScanForward64.restype = ctypes.c_ubyte
    BitScanForward64.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint64]
    BitScanReverse = _libraries['FIXME_STUB'].BitScanReverse
    BitScanReverse.restype = ctypes.c_ubyte
    BitScanReverse.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32]
    BitScanReverse64 = _libraries['FIXME_STUB'].BitScanReverse64
    BitScanReverse64.restype = ctypes.c_ubyte
    BitScanReverse64.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint64]
    Denorm_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Denorm_C')
    Eps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Eps_C')
    Exit = _libraries['FIXME_STUB'].Exit
    Exit.restype = None
    Exit.argtypes = [ctypes.c_int32]
    FDenorm_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FDenorm_C')
    FEps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FEps_C')
    FInf_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FInf_C')
    FNan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FNan_C')
    FRteps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FRteps_C')
    FSnan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'FSnan_C')
    FXbig_C = ctypes_in_dll(ctypes.c_float, _libraries['FIXME_STUB'], 'FXbig_C')
    FZero_C = ctypes_in_dll(ctypes.c_float, _libraries['FIXME_STUB'], 'FZero_C')
    Hugeval_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Hugeval_C')
    Inf_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Inf_C')
    InterlockedAnd = _libraries['FIXME_STUB'].InterlockedAnd
    InterlockedAnd.restype = ctypes.c_int32
    InterlockedAnd.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    InterlockedAnd16 = _libraries['FIXME_STUB'].InterlockedAnd16
    InterlockedAnd16.restype = ctypes.c_int16
    InterlockedAnd16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    InterlockedAnd64 = _libraries['FIXME_STUB'].InterlockedAnd64
    InterlockedAnd64.restype = ctypes.c_int64
    InterlockedAnd64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    InterlockedAnd8 = _libraries['FIXME_STUB'].InterlockedAnd8
    InterlockedAnd8.restype = ctypes.c_char
    InterlockedAnd8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    InterlockedCompareExchange = _libraries['FIXME_STUB'].InterlockedCompareExchange
    InterlockedCompareExchange.restype = ctypes.c_int32
    InterlockedCompareExchange.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32, ctypes.c_int32]
    InterlockedCompareExchange128 = _libraries['FIXME_STUB'].InterlockedCompareExchange128
    InterlockedCompareExchange128.restype = ctypes.c_ubyte
    InterlockedCompareExchange128.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64, ctypes.c_int64, ctypes.POINTER(ctypes.c_int64)]
    InterlockedCompareExchange16 = _libraries['FIXME_STUB'].InterlockedCompareExchange16
    InterlockedCompareExchange16.restype = ctypes.c_int16
    InterlockedCompareExchange16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16, ctypes.c_int16]
    InterlockedCompareExchange64 = _libraries['FIXME_STUB'].InterlockedCompareExchange64
    InterlockedCompareExchange64.restype = ctypes.c_int64
    InterlockedCompareExchange64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64, ctypes.c_int64]
    InterlockedCompareExchange8 = _libraries['FIXME_STUB'].InterlockedCompareExchange8
    InterlockedCompareExchange8.restype = ctypes.c_char
    InterlockedCompareExchange8.argtypes = [ctypes.c_char_p, ctypes.c_char, ctypes.c_char]
    InterlockedDecrement = _libraries['FIXME_STUB'].InterlockedDecrement
    InterlockedDecrement.restype = ctypes.c_int32
    InterlockedDecrement.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    InterlockedDecrement16 = _libraries['FIXME_STUB'].InterlockedDecrement16
    InterlockedDecrement16.restype = ctypes.c_int16
    InterlockedDecrement16.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    InterlockedDecrement64 = _libraries['FIXME_STUB'].InterlockedDecrement64
    InterlockedDecrement64.restype = ctypes.c_int64
    InterlockedDecrement64.argtypes = [ctypes.POINTER(ctypes.c_int64)]
    InterlockedExchange = _libraries['FIXME_STUB'].InterlockedExchange
    InterlockedExchange.restype = ctypes.c_int32
    InterlockedExchange.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    InterlockedExchange16 = _libraries['FIXME_STUB'].InterlockedExchange16
    InterlockedExchange16.restype = ctypes.c_int16
    InterlockedExchange16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    InterlockedExchange64 = _libraries['FIXME_STUB'].InterlockedExchange64
    InterlockedExchange64.restype = ctypes.c_int64
    InterlockedExchange64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    InterlockedExchange8 = _libraries['FIXME_STUB'].InterlockedExchange8
    InterlockedExchange8.restype = ctypes.c_char
    InterlockedExchange8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    InterlockedExchangeAdd = _libraries['FIXME_STUB'].InterlockedExchangeAdd
    InterlockedExchangeAdd.restype = ctypes.c_int32
    InterlockedExchangeAdd.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    InterlockedExchangeAdd16 = _libraries['FIXME_STUB'].InterlockedExchangeAdd16
    InterlockedExchangeAdd16.restype = ctypes.c_int16
    InterlockedExchangeAdd16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    InterlockedExchangeAdd64 = _libraries['FIXME_STUB'].InterlockedExchangeAdd64
    InterlockedExchangeAdd64.restype = ctypes.c_int64
    InterlockedExchangeAdd64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    InterlockedExchangeAdd8 = _libraries['FIXME_STUB'].InterlockedExchangeAdd8
    InterlockedExchangeAdd8.restype = ctypes.c_char
    InterlockedExchangeAdd8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    InterlockedIncrement = _libraries['FIXME_STUB'].InterlockedIncrement
    InterlockedIncrement.restype = ctypes.c_int32
    InterlockedIncrement.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    InterlockedIncrement16 = _libraries['FIXME_STUB'].InterlockedIncrement16
    InterlockedIncrement16.restype = ctypes.c_int16
    InterlockedIncrement16.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    InterlockedIncrement64 = _libraries['FIXME_STUB'].InterlockedIncrement64
    InterlockedIncrement64.restype = ctypes.c_int64
    InterlockedIncrement64.argtypes = [ctypes.POINTER(ctypes.c_int64)]
    InterlockedOr = _libraries['FIXME_STUB'].InterlockedOr
    InterlockedOr.restype = ctypes.c_int32
    InterlockedOr.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    InterlockedOr16 = _libraries['FIXME_STUB'].InterlockedOr16
    InterlockedOr16.restype = ctypes.c_int16
    InterlockedOr16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    InterlockedOr64 = _libraries['FIXME_STUB'].InterlockedOr64
    InterlockedOr64.restype = ctypes.c_int64
    InterlockedOr64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    InterlockedOr8 = _libraries['FIXME_STUB'].InterlockedOr8
    InterlockedOr8.restype = ctypes.c_char
    InterlockedOr8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    InterlockedXor = _libraries['FIXME_STUB'].InterlockedXor
    InterlockedXor.restype = ctypes.c_int32
    InterlockedXor.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    InterlockedXor16 = _libraries['FIXME_STUB'].InterlockedXor16
    InterlockedXor16.restype = ctypes.c_int16
    InterlockedXor16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    InterlockedXor64 = _libraries['FIXME_STUB'].InterlockedXor64
    InterlockedXor64.restype = ctypes.c_int64
    InterlockedXor64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    InterlockedXor8 = _libraries['FIXME_STUB'].InterlockedXor8
    InterlockedXor8.restype = ctypes.c_char
    InterlockedXor8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    LDenorm_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LDenorm_C')
    LEps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LEps_C')
    LInf_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LInf_C')
    LNan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LNan_C')
    LRteps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LRteps_C')
    LSnan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'LSnan_C')
    LXbig_C = ctypes_in_dll(ctypes.c_double, _libraries['FIXME_STUB'], 'LXbig_C')
    LZero_C = ctypes_in_dll(ctypes.c_double, _libraries['FIXME_STUB'], 'LZero_C')
    MallocaComputeSize = _libraries['FIXME_STUB'].MallocaComputeSize
    MallocaComputeSize.restype = size_t
    MallocaComputeSize.argtypes = [size_t]
    MarkAllocaS = _libraries['FIXME_STUB'].MarkAllocaS
    MarkAllocaS.restype = ctypes.POINTER(None)
    MarkAllocaS.argtypes = [ctypes.POINTER(None), ctypes.c_uint32]
    Nan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Nan_C')
    ReadWriteBarrier = _libraries['FIXME_STUB'].ReadWriteBarrier
    ReadWriteBarrier.restype = None
    ReadWriteBarrier.argtypes = []
    Rteps_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Rteps_C')
    Snan_C = ctypes_in_dll(union__float_const, _libraries['FIXME_STUB'], 'Snan_C')
    Xbig_C = ctypes_in_dll(ctypes.c_double, _libraries['FIXME_STUB'], 'Xbig_C')
    Zero_C = ctypes_in_dll(ctypes.c_double, _libraries['FIXME_STUB'], 'Zero_C')
    __mb_cur_max_func = _libraries['FIXME_STUB'].__mb_cur_max_func
    __mb_cur_max_func.restype = ctypes.c_int32
    __mb_cur_max_func.argtypes = []
    __mb_cur_max_l_func = _libraries['FIXME_STUB'].__mb_cur_max_l_func
    __mb_cur_max_l_func.restype = ctypes.c_int32
    __mb_cur_max_l_func.argtypes = [_locale_t]
    _acrt_get_locale_data_prefix = _libraries['FIXME_STUB']._acrt_get_locale_data_prefix
    _acrt_get_locale_data_prefix.restype = ctypes.POINTER(struct___crt_locale_data_public)
    _acrt_get_locale_data_prefix.argtypes = [ctypes.POINTER(None)]
    _acrt_iob_func = _libraries['FIXME_STUB']._acrt_iob_func
    _acrt_iob_func.restype = ctypes.POINTER(FILE)
    _acrt_iob_func.argtypes = [ctypes.c_uint32]
    _acrt_locale_get_ctype_array_value = _libraries['FIXME_STUB']._acrt_locale_get_ctype_array_value
    _acrt_locale_get_ctype_array_value.restype = ctypes.c_int32
    _acrt_locale_get_ctype_array_value.argtypes = [ctypes.POINTER(ctypes.c_uint16), ctypes.c_int32, ctypes.c_int32]
    _ascii_iswalpha = _libraries['FIXME_STUB']._ascii_iswalpha
    _ascii_iswalpha.restype = ctypes.c_int32
    _ascii_iswalpha.argtypes = [ctypes.c_int32]
    _ascii_iswdigit = _libraries['FIXME_STUB']._ascii_iswdigit
    _ascii_iswdigit.restype = ctypes.c_int32
    _ascii_iswdigit.argtypes = [ctypes.c_int32]
    _ascii_tolower = _libraries['FIXME_STUB']._ascii_tolower
    _ascii_tolower.restype = ctypes.c_int32
    _ascii_tolower.argtypes = [ctypes.c_int32]
    _ascii_toupper = _libraries['FIXME_STUB']._ascii_toupper
    _ascii_toupper.restype = ctypes.c_int32
    _ascii_toupper.argtypes = [ctypes.c_int32]
    _ascii_towlower = _libraries['FIXME_STUB']._ascii_towlower
    _ascii_towlower.restype = ctypes.c_int32
    _ascii_towlower.argtypes = [ctypes.c_int32]
    _ascii_towupper = _libraries['FIXME_STUB']._ascii_towupper
    _ascii_towupper.restype = ctypes.c_int32
    _ascii_towupper.argtypes = [ctypes.c_int32]
    _builtin_assume_aligned = _libraries['FIXME_STUB']._builtin_assume_aligned
    _builtin_assume_aligned.restype = ctypes.POINTER(None)
    _builtin_assume_aligned.argtypes = [ctypes.POINTER(None), size_t]
    _ceil = _libraries['FIXME_STUB']._ceil
    _ceil.restype = ctypes.c_double
    _ceil.argtypes = [ctypes.c_double]
    _ceilf = _libraries['FIXME_STUB']._ceilf
    _ceilf.restype = ctypes.c_float
    _ceilf.argtypes = [ctypes.c_float]
    va_list = ctypes.POINTER(ctypes.POINTER(None))
    _conio_common_vcwprintf = _libraries['FIXME_STUB']._conio_common_vcwprintf
    _conio_common_vcwprintf.restype = ctypes.c_int32
    _conio_common_vcwprintf.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _conio_common_vcwprintf_p = _libraries['FIXME_STUB']._conio_common_vcwprintf_p
    _conio_common_vcwprintf_p.restype = ctypes.c_int32
    _conio_common_vcwprintf_p.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _conio_common_vcwprintf_s = _libraries['FIXME_STUB']._conio_common_vcwprintf_s
    _conio_common_vcwprintf_s.restype = ctypes.c_int32
    _conio_common_vcwprintf_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _conio_common_vcwscanf = _libraries['FIXME_STUB']._conio_common_vcwscanf
    _conio_common_vcwscanf.restype = ctypes.c_int32
    _conio_common_vcwscanf.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _copysign = _libraries['FIXME_STUB']._copysign
    _copysign.restype = ctypes.c_double
    _copysign.argtypes = [ctypes.c_double, ctypes.c_double]
    _copysignf = _libraries['FIXME_STUB']._copysignf
    _copysignf.restype = ctypes.c_float
    _copysignf.argtypes = [ctypes.c_float, ctypes.c_float]
    _daylight = _libraries['FIXME_STUB']._daylight
    _daylight.restype = ctypes.POINTER(ctypes.c_int32)
    _daylight.argtypes = []
    _doserrno = _libraries['FIXME_STUB']._doserrno
    _doserrno.restype = ctypes.POINTER(ctypes.c_uint32)
    _doserrno.argtypes = []
    _dstbias = _libraries['FIXME_STUB']._dstbias
    _dstbias.restype = ctypes.POINTER(ctypes.c_int32)
    _dstbias.argtypes = []
    _floor = _libraries['FIXME_STUB']._floor
    _floor.restype = ctypes.c_double
    _floor.argtypes = [ctypes.c_double]
    _floorf = _libraries['FIXME_STUB']._floorf
    _floorf.restype = ctypes.c_float
    _floorf.argtypes = [ctypes.c_float]
    _fpe_flt_rounds = _libraries['FIXME_STUB']._fpe_flt_rounds
    _fpe_flt_rounds.restype = ctypes.c_int32
    _fpe_flt_rounds.argtypes = []
    _fpecode = _libraries['FIXME_STUB']._fpecode
    _fpecode.restype = ctypes.POINTER(ctypes.c_int32)
    _fpecode.argtypes = []
    _isa_available = ctypes_in_dll(ctypes.c_int32, _libraries['FIXME_STUB'], '_isa_available')
    _isascii = _libraries['FIXME_STUB']._isascii
    _isascii.restype = ctypes.c_int32
    _isascii.argtypes = [ctypes.c_int32]
    _iscsym = _libraries['FIXME_STUB']._iscsym
    _iscsym.restype = ctypes.c_int32
    _iscsym.argtypes = [ctypes.c_int32]
    _iscsymf = _libraries['FIXME_STUB']._iscsymf
    _iscsymf.restype = ctypes.c_int32
    _iscsymf.argtypes = [ctypes.c_int32]
    _iso_volatile_load16 = _libraries['FIXME_STUB']._iso_volatile_load16
    _iso_volatile_load16.restype = ctypes.c_int16
    _iso_volatile_load16.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    _iso_volatile_load32 = _libraries['FIXME_STUB']._iso_volatile_load32
    _iso_volatile_load32.restype = ctypes.c_int32
    _iso_volatile_load32.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    _iso_volatile_load64 = _libraries['FIXME_STUB']._iso_volatile_load64
    _iso_volatile_load64.restype = ctypes.c_int64
    _iso_volatile_load64.argtypes = [ctypes.POINTER(ctypes.c_int64)]
    _iso_volatile_load8 = _libraries['FIXME_STUB']._iso_volatile_load8
    _iso_volatile_load8.restype = ctypes.c_char
    _iso_volatile_load8.argtypes = [ctypes.c_char_p]
    _iso_volatile_store16 = _libraries['FIXME_STUB']._iso_volatile_store16
    _iso_volatile_store16.restype = None
    _iso_volatile_store16.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    _iso_volatile_store32 = _libraries['FIXME_STUB']._iso_volatile_store32
    _iso_volatile_store32.restype = None
    _iso_volatile_store32.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    _iso_volatile_store64 = _libraries['FIXME_STUB']._iso_volatile_store64
    _iso_volatile_store64.restype = None
    _iso_volatile_store64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    _iso_volatile_store8 = _libraries['FIXME_STUB']._iso_volatile_store8
    _iso_volatile_store8.restype = None
    _iso_volatile_store8.argtypes = [ctypes.c_char_p, ctypes.c_char]
    _iswcsym = _libraries['FIXME_STUB']._iswcsym
    _iswcsym.restype = ctypes.c_int32
    _iswcsym.argtypes = [wint_t]
    _iswcsymf = _libraries['FIXME_STUB']._iswcsymf
    _iswcsymf.restype = ctypes.c_int32
    _iswcsymf.argtypes = [wint_t]
    _local_stdio_printf_options = _libraries['FIXME_STUB']._local_stdio_printf_options
    _local_stdio_printf_options.restype = ctypes.POINTER(ctypes.c_uint64)
    _local_stdio_printf_options.argtypes = []
    _local_stdio_scanf_options = _libraries['FIXME_STUB']._local_stdio_scanf_options
    _local_stdio_scanf_options.restype = ctypes.POINTER(ctypes.c_uint64)
    _local_stdio_scanf_options.argtypes = []
    _lzcnt = _libraries['FIXME_STUB']._lzcnt
    _lzcnt.restype = ctypes.c_uint32
    _lzcnt.argtypes = [ctypes.c_uint32]
    _lzcnt16 = _libraries['FIXME_STUB']._lzcnt16
    _lzcnt16.restype = ctypes.c_uint16
    _lzcnt16.argtypes = [ctypes.c_uint16]
    _lzcnt64 = _libraries['FIXME_STUB']._lzcnt64
    _lzcnt64.restype = ctypes.c_uint64
    _lzcnt64.argtypes = [ctypes.c_uint64]
    _p___argc = _libraries['FIXME_STUB']._p___argc
    _p___argc.restype = ctypes.POINTER(ctypes.c_int32)
    _p___argc.argtypes = []
    _p___argv = _libraries['FIXME_STUB']._p___argv
    _p___argv.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p))
    _p___argv.argtypes = []
    _p___wargv = _libraries['FIXME_STUB']._p___wargv
    _p___wargv.restype = ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)))
    _p___wargv.argtypes = []
    _p__commode = _libraries['FIXME_STUB']._p__commode
    _p__commode.restype = ctypes.POINTER(ctypes.c_int32)
    _p__commode.argtypes = []
    _p__environ = _libraries['FIXME_STUB']._p__environ
    _p__environ.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p))
    _p__environ.argtypes = []
    _p__fmode = _libraries['FIXME_STUB']._p__fmode
    _p__fmode.restype = ctypes.POINTER(ctypes.c_int32)
    _p__fmode.argtypes = []
    _p__pgmptr = _libraries['FIXME_STUB']._p__pgmptr
    _p__pgmptr.restype = ctypes.POINTER(ctypes.c_char_p)
    _p__pgmptr.argtypes = []
    _p__wenviron = _libraries['FIXME_STUB']._p__wenviron
    _p__wenviron.restype = ctypes.POINTER(ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)))
    _p__wenviron.argtypes = []
    _p__wpgmptr = _libraries['FIXME_STUB']._p__wpgmptr
    _p__wpgmptr.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))
    _p__wpgmptr.argtypes = []
    _pctype_func = _libraries['FIXME_STUB']._pctype_func
    _pctype_func.restype = ctypes.POINTER(ctypes.c_uint16)
    _pctype_func.argtypes = []
    _popcnt = _libraries['FIXME_STUB']._popcnt
    _popcnt.restype = ctypes.c_uint32
    _popcnt.argtypes = [ctypes.c_uint32]
    _popcnt16 = _libraries['FIXME_STUB']._popcnt16
    _popcnt16.restype = ctypes.c_uint16
    _popcnt16.argtypes = [ctypes.c_uint16]
    _popcnt64 = _libraries['FIXME_STUB']._popcnt64
    _popcnt64.restype = ctypes.c_uint64
    _popcnt64.argtypes = [ctypes.c_uint64]
    _pwctype_func = _libraries['FIXME_STUB']._pwctype_func
    _pwctype_func.restype = ctypes.POINTER(wctype_t)
    _pwctype_func.argtypes = []
    _report_gsfailure = _libraries['FIXME_STUB']._report_gsfailure
    _report_gsfailure.restype = None
    _report_gsfailure.argtypes = [uintptr_t]
    _round = _libraries['FIXME_STUB']._round
    _round.restype = ctypes.c_double
    _round.argtypes = [ctypes.c_double]
    _roundf = _libraries['FIXME_STUB']._roundf
    _roundf.restype = ctypes.c_float
    _roundf.argtypes = [ctypes.c_float]
    _security_check_cookie = _libraries['FIXME_STUB']._security_check_cookie
    _security_check_cookie.restype = None
    _security_check_cookie.argtypes = [uintptr_t]
    _security_cookie = ctypes_in_dll(ctypes.c_uint64, _libraries['FIXME_STUB'], '_security_cookie')
    _security_init_cookie = _libraries['FIXME_STUB']._security_init_cookie
    _security_init_cookie.restype = None
    _security_init_cookie.argtypes = []
    _shiftright128 = _libraries['FIXME_STUB']._shiftright128
    _shiftright128.restype = ctypes.c_uint64
    _shiftright128.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_ubyte]
    _signbitvalue = _libraries['FIXME_STUB']._signbitvalue
    _signbitvalue.restype = ctypes.c_uint32
    _signbitvalue.argtypes = [ctypes.c_double]
    _signbitvaluef = _libraries['FIXME_STUB']._signbitvaluef
    _signbitvaluef.restype = ctypes.c_uint32
    _signbitvaluef.argtypes = [ctypes.c_float]
    _std_exception_copy = _libraries['FIXME_STUB']._std_exception_copy
    _std_exception_copy.restype = None
    _std_exception_copy.argtypes = [ctypes.POINTER(struct___std_exception_data), ctypes.POINTER(struct___std_exception_data)]
    _std_exception_destroy = _libraries['FIXME_STUB']._std_exception_destroy
    _std_exception_destroy.restype = None
    _std_exception_destroy.argtypes = [ctypes.POINTER(struct___std_exception_data)]
    _std_reverse_copy_trivially_copyable_1 = _libraries['FIXME_STUB']._std_reverse_copy_trivially_copyable_1
    _std_reverse_copy_trivially_copyable_1.restype = None
    _std_reverse_copy_trivially_copyable_1.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_copy_trivially_copyable_2 = _libraries['FIXME_STUB']._std_reverse_copy_trivially_copyable_2
    _std_reverse_copy_trivially_copyable_2.restype = None
    _std_reverse_copy_trivially_copyable_2.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_copy_trivially_copyable_4 = _libraries['FIXME_STUB']._std_reverse_copy_trivially_copyable_4
    _std_reverse_copy_trivially_copyable_4.restype = None
    _std_reverse_copy_trivially_copyable_4.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_copy_trivially_copyable_8 = _libraries['FIXME_STUB']._std_reverse_copy_trivially_copyable_8
    _std_reverse_copy_trivially_copyable_8.restype = None
    _std_reverse_copy_trivially_copyable_8.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_trivially_swappable_1 = _libraries['FIXME_STUB']._std_reverse_trivially_swappable_1
    _std_reverse_trivially_swappable_1.restype = None
    _std_reverse_trivially_swappable_1.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_trivially_swappable_2 = _libraries['FIXME_STUB']._std_reverse_trivially_swappable_2
    _std_reverse_trivially_swappable_2.restype = None
    _std_reverse_trivially_swappable_2.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_trivially_swappable_4 = _libraries['FIXME_STUB']._std_reverse_trivially_swappable_4
    _std_reverse_trivially_swappable_4.restype = None
    _std_reverse_trivially_swappable_4.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_reverse_trivially_swappable_8 = _libraries['FIXME_STUB']._std_reverse_trivially_swappable_8
    _std_reverse_trivially_swappable_8.restype = None
    _std_reverse_trivially_swappable_8.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None)]
    _std_swap_ranges_trivially_swappable_noalias = _libraries['FIXME_STUB']._std_swap_ranges_trivially_swappable_noalias
    _std_swap_ranges_trivially_swappable_noalias.restype = None
    _std_swap_ranges_trivially_swappable_noalias.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(None)]
    _stdio_common_vfprintf = _libraries['FIXME_STUB']._stdio_common_vfprintf
    _stdio_common_vfprintf.restype = ctypes.c_int32
    _stdio_common_vfprintf.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vfprintf_p = _libraries['FIXME_STUB']._stdio_common_vfprintf_p
    _stdio_common_vfprintf_p.restype = ctypes.c_int32
    _stdio_common_vfprintf_p.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vfprintf_s = _libraries['FIXME_STUB']._stdio_common_vfprintf_s
    _stdio_common_vfprintf_s.restype = ctypes.c_int32
    _stdio_common_vfprintf_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vfscanf = _libraries['FIXME_STUB']._stdio_common_vfscanf
    _stdio_common_vfscanf.restype = ctypes.c_int32
    _stdio_common_vfscanf.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vfwprintf = _libraries['FIXME_STUB']._stdio_common_vfwprintf
    _stdio_common_vfwprintf.restype = ctypes.c_int32
    _stdio_common_vfwprintf.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vfwprintf_p = _libraries['FIXME_STUB']._stdio_common_vfwprintf_p
    _stdio_common_vfwprintf_p.restype = ctypes.c_int32
    _stdio_common_vfwprintf_p.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vfwprintf_s = _libraries['FIXME_STUB']._stdio_common_vfwprintf_s
    _stdio_common_vfwprintf_s.restype = ctypes.c_int32
    _stdio_common_vfwprintf_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vfwscanf = _libraries['FIXME_STUB']._stdio_common_vfwscanf
    _stdio_common_vfwscanf.restype = ctypes.c_int32
    _stdio_common_vfwscanf.argtypes = [ctypes.c_uint64, ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vsnprintf_s = _libraries['FIXME_STUB']._stdio_common_vsnprintf_s
    _stdio_common_vsnprintf_s.restype = ctypes.c_int32
    _stdio_common_vsnprintf_s.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, size_t, ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vsnwprintf_s = _libraries['FIXME_STUB']._stdio_common_vsnwprintf_s
    _stdio_common_vsnwprintf_s.restype = ctypes.c_int32
    _stdio_common_vsnwprintf_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vsprintf = _libraries['FIXME_STUB']._stdio_common_vsprintf
    _stdio_common_vsprintf.restype = ctypes.c_int32
    _stdio_common_vsprintf.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vsprintf_p = _libraries['FIXME_STUB']._stdio_common_vsprintf_p
    _stdio_common_vsprintf_p.restype = ctypes.c_int32
    _stdio_common_vsprintf_p.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vsprintf_s = _libraries['FIXME_STUB']._stdio_common_vsprintf_s
    _stdio_common_vsprintf_s.restype = ctypes.c_int32
    _stdio_common_vsprintf_s.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vsscanf = _libraries['FIXME_STUB']._stdio_common_vsscanf
    _stdio_common_vsscanf.restype = ctypes.c_int32
    _stdio_common_vsscanf.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    _stdio_common_vswprintf = _libraries['FIXME_STUB']._stdio_common_vswprintf
    _stdio_common_vswprintf.restype = ctypes.c_int32
    _stdio_common_vswprintf.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vswprintf_p = _libraries['FIXME_STUB']._stdio_common_vswprintf_p
    _stdio_common_vswprintf_p.restype = ctypes.c_int32
    _stdio_common_vswprintf_p.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vswprintf_s = _libraries['FIXME_STUB']._stdio_common_vswprintf_s
    _stdio_common_vswprintf_s.restype = ctypes.c_int32
    _stdio_common_vswprintf_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _stdio_common_vswscanf = _libraries['FIXME_STUB']._stdio_common_vswscanf
    _stdio_common_vswscanf.restype = ctypes.c_int32
    _stdio_common_vswscanf.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _strncnt = _libraries['FIXME_STUB']._strncnt
    _strncnt.restype = size_t
    _strncnt.argtypes = [ctypes.c_char_p, size_t]
    _swprintf_l = _libraries['FIXME_STUB']._swprintf_l
    _swprintf_l.restype = ctypes.c_int32
    _swprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    _sys_errlist = _libraries['FIXME_STUB']._sys_errlist
    _sys_errlist.restype = ctypes.POINTER(ctypes.c_char_p)
    _sys_errlist.argtypes = []
    _sys_nerr = _libraries['FIXME_STUB']._sys_nerr
    _sys_nerr.restype = ctypes.POINTER(ctypes.c_int32)
    _sys_nerr.argtypes = []
    _threadhandle = _libraries['FIXME_STUB']._threadhandle
    _threadhandle.restype = uintptr_t
    _threadhandle.argtypes = []
    _threadid = _libraries['FIXME_STUB']._threadid
    _threadid.restype = ctypes.c_uint32
    _threadid.argtypes = []
    _timezone = _libraries['FIXME_STUB']._timezone
    _timezone.restype = ctypes.POINTER(ctypes.c_int32)
    _timezone.argtypes = []
    _toascii = _libraries['FIXME_STUB']._toascii
    _toascii.restype = ctypes.c_int32
    _toascii.argtypes = [ctypes.c_int32]
    _trunc = _libraries['FIXME_STUB']._trunc
    _trunc.restype = ctypes.c_double
    _trunc.argtypes = [ctypes.c_double]
    _truncf = _libraries['FIXME_STUB']._truncf
    _truncf.restype = ctypes.c_float
    _truncf.argtypes = [ctypes.c_float]
    _tzname = _libraries['FIXME_STUB']._tzname
    _tzname.restype = ctypes.POINTER(ctypes.c_char_p)
    _tzname.argtypes = []
    _uncaught_exception = _libraries['FIXME_STUB']._uncaught_exception
    _uncaught_exception.restype = ctypes.c_char
    _uncaught_exception.argtypes = []
    _uncaught_exceptions = _libraries['FIXME_STUB']._uncaught_exceptions
    _uncaught_exceptions.restype = ctypes.c_int32
    _uncaught_exceptions.argtypes = []
    _va_start = _libraries['FIXME_STUB']._va_start
    _va_start.restype = None
    _va_start.argtypes = [ctypes.POINTER(va_list)]
    _vswprintf_l = _libraries['FIXME_STUB']._vswprintf_l
    _vswprintf_l.restype = ctypes.c_int32
    _vswprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    _wcserror = _libraries['FIXME_STUB']._wcserror
    _wcserror.restype = ctypes.POINTER(ctypes.c_int16)
    _wcserror.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    _wcserror_s = _libraries['FIXME_STUB']._wcserror_s
    _wcserror_s.restype = errno_t
    _wcserror_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    abs64 = _libraries['FIXME_STUB'].abs64
    abs64.restype = ctypes.c_int64
    abs64.argtypes = [ctypes.c_int64]
    access = _libraries['FIXME_STUB'].access
    access.restype = ctypes.c_int32
    access.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    access_s = _libraries['FIXME_STUB'].access_s
    access_s.restype = errno_t
    access_s.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    aligned_free = _libraries['FIXME_STUB'].aligned_free
    aligned_free.restype = None
    aligned_free.argtypes = [ctypes.POINTER(None)]
    aligned_malloc = _libraries['FIXME_STUB'].aligned_malloc
    aligned_malloc.restype = ctypes.POINTER(None)
    aligned_malloc.argtypes = [size_t, size_t]
    aligned_msize = _libraries['FIXME_STUB'].aligned_msize
    aligned_msize.restype = size_t
    aligned_msize.argtypes = [ctypes.POINTER(None), size_t, size_t]
    aligned_offset_malloc = _libraries['FIXME_STUB'].aligned_offset_malloc
    aligned_offset_malloc.restype = ctypes.POINTER(None)
    aligned_offset_malloc.argtypes = [size_t, size_t, size_t]
    aligned_offset_realloc = _libraries['FIXME_STUB'].aligned_offset_realloc
    aligned_offset_realloc.restype = ctypes.POINTER(None)
    aligned_offset_realloc.argtypes = [ctypes.POINTER(None), size_t, size_t, size_t]
    aligned_offset_recalloc = _libraries['FIXME_STUB'].aligned_offset_recalloc
    aligned_offset_recalloc.restype = ctypes.POINTER(None)
    aligned_offset_recalloc.argtypes = [ctypes.POINTER(None), size_t, size_t, size_t, size_t]
    aligned_realloc = _libraries['FIXME_STUB'].aligned_realloc
    aligned_realloc.restype = ctypes.POINTER(None)
    aligned_realloc.argtypes = [ctypes.POINTER(None), size_t, size_t]
    aligned_recalloc = _libraries['FIXME_STUB'].aligned_recalloc
    aligned_recalloc.restype = ctypes.POINTER(None)
    aligned_recalloc.argtypes = [ctypes.POINTER(None), size_t, size_t, size_t]
    alloca = _libraries['FIXME_STUB'].alloca
    alloca.restype = ctypes.POINTER(None)
    alloca.argtypes = [size_t]
    atodbl = _libraries['FIXME_STUB'].atodbl
    atodbl.restype = ctypes.c_int32
    atodbl.argtypes = [ctypes.POINTER(struct__CRT_DOUBLE), ctypes.c_char_p]
    atodbl_l = _libraries['FIXME_STUB'].atodbl_l
    atodbl_l.restype = ctypes.c_int32
    atodbl_l.argtypes = [ctypes.POINTER(struct__CRT_DOUBLE), ctypes.c_char_p, _locale_t]
    atof_l = _libraries['FIXME_STUB'].atof_l
    atof_l.restype = ctypes.c_double
    atof_l.argtypes = [ctypes.c_char_p, _locale_t]
    atoflt = _libraries['FIXME_STUB'].atoflt
    atoflt.restype = ctypes.c_int32
    atoflt.argtypes = [ctypes.POINTER(struct__CRT_FLOAT), ctypes.c_char_p]
    atoflt_l = _libraries['FIXME_STUB'].atoflt_l
    atoflt_l.restype = ctypes.c_int32
    atoflt_l.argtypes = [ctypes.POINTER(struct__CRT_FLOAT), ctypes.c_char_p, _locale_t]
    atoi64 = _libraries['FIXME_STUB'].atoi64
    atoi64.restype = ctypes.c_int64
    atoi64.argtypes = [ctypes.c_char_p]
    atoi64_l = _libraries['FIXME_STUB'].atoi64_l
    atoi64_l.restype = ctypes.c_int64
    atoi64_l.argtypes = [ctypes.c_char_p, _locale_t]
    atoi_l = _libraries['FIXME_STUB'].atoi_l
    atoi_l.restype = ctypes.c_int32
    atoi_l.argtypes = [ctypes.c_char_p, _locale_t]
    atol_l = _libraries['FIXME_STUB'].atol_l
    atol_l.restype = ctypes.c_int32
    atol_l.argtypes = [ctypes.c_char_p, _locale_t]
    atoldbl = _libraries['FIXME_STUB'].atoldbl
    atoldbl.restype = ctypes.c_int32
    atoldbl.argtypes = [ctypes.POINTER(struct__LDOUBLE), ctypes.c_char_p]
    atoldbl_l = _libraries['FIXME_STUB'].atoldbl_l
    atoldbl_l.restype = ctypes.c_int32
    atoldbl_l.argtypes = [ctypes.POINTER(struct__LDOUBLE), ctypes.c_char_p, _locale_t]
    atoll_l = _libraries['FIXME_STUB'].atoll_l
    atoll_l.restype = ctypes.c_int64
    atoll_l.argtypes = [ctypes.c_char_p, _locale_t]
    beep = _libraries['FIXME_STUB'].beep
    beep.restype = None
    beep.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    bittest = _libraries['FIXME_STUB'].bittest
    bittest.restype = ctypes.c_ubyte
    bittest.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    byteswap_uint64 = _libraries['FIXME_STUB'].byteswap_uint64
    byteswap_uint64.restype = ctypes.c_uint64
    byteswap_uint64.argtypes = [ctypes.c_uint64]
    byteswap_ulong = _libraries['FIXME_STUB'].byteswap_ulong
    byteswap_ulong.restype = ctypes.c_uint32
    byteswap_ulong.argtypes = [ctypes.c_uint32]
    byteswap_ushort = _libraries['FIXME_STUB'].byteswap_ushort
    byteswap_ushort.restype = ctypes.c_uint16
    byteswap_ushort.argtypes = [ctypes.c_uint16]
    cabs = _libraries['FIXME_STUB'].cabs
    cabs.restype = ctypes.c_double
    cabs.argtypes = [struct__complex]
    callnewh = _libraries['FIXME_STUB'].callnewh
    callnewh.restype = ctypes.c_int32
    callnewh.argtypes = [size_t]
    calloc_base = _libraries['FIXME_STUB'].calloc_base
    calloc_base.restype = ctypes.POINTER(None)
    calloc_base.argtypes = [size_t, size_t]
    cgetws_s = _libraries['FIXME_STUB'].cgetws_s
    cgetws_s.restype = errno_t
    cgetws_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(size_t)]
    chdir = _libraries['FIXME_STUB'].chdir
    chdir.restype = ctypes.c_int32
    chdir.argtypes = [ctypes.c_char_p]
    chdrive = _libraries['FIXME_STUB'].chdrive
    chdrive.restype = ctypes.c_int32
    chdrive.argtypes = [ctypes.c_int32]
    chgsign = _libraries['FIXME_STUB'].chgsign
    chgsign.restype = ctypes.c_double
    chgsign.argtypes = [ctypes.c_double]
    chgsignf = _libraries['FIXME_STUB'].chgsignf
    chgsignf.restype = ctypes.c_float
    chgsignf.argtypes = [ctypes.c_float]
    chgsignl = _libraries['FIXME_STUB'].chgsignl
    chgsignl.restype = ctypes.c_double
    chgsignl.argtypes = [ctypes.c_double]
    chmod = _libraries['FIXME_STUB'].chmod
    chmod.restype = ctypes.c_int32
    chmod.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    chsize = _libraries['FIXME_STUB'].chsize
    chsize.restype = ctypes.c_int32
    chsize.argtypes = [ctypes.c_int32, ctypes.c_int32]
    chsize_s = _libraries['FIXME_STUB'].chsize_s
    chsize_s.restype = errno_t
    chsize_s.argtypes = [ctypes.c_int32, ctypes.c_int64]
    chvalidchk_l = _libraries['FIXME_STUB'].chvalidchk_l
    chvalidchk_l.restype = ctypes.c_int32
    chvalidchk_l.argtypes = [ctypes.c_int32, ctypes.c_int32, _locale_t]
    clearfp = _libraries['FIXME_STUB'].clearfp
    clearfp.restype = ctypes.c_uint32
    clearfp.argtypes = []
    close = _libraries['FIXME_STUB'].close
    close.restype = ctypes.c_int32
    close.argtypes = [ctypes.c_int32]
    commit = _libraries['FIXME_STUB'].commit
    commit.restype = ctypes.c_int32
    commit.argtypes = [ctypes.c_int32]
    control87 = _libraries['FIXME_STUB'].control87
    control87.restype = ctypes.c_uint32
    control87.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    controlfp = _libraries['FIXME_STUB'].controlfp
    controlfp.restype = ctypes.c_uint32
    controlfp.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    controlfp_s = _libraries['FIXME_STUB'].controlfp_s
    controlfp_s.restype = errno_t
    controlfp_s.argtypes = [ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, ctypes.c_uint32]
    copysign = _libraries['FIXME_STUB'].copysign
    copysign.restype = ctypes.c_double
    copysign.argtypes = [ctypes.c_double, ctypes.c_double]
    copysignf = _libraries['FIXME_STUB'].copysignf
    copysignf.restype = ctypes.c_float
    copysignf.argtypes = [ctypes.c_float, ctypes.c_float]
    copysignl = _libraries['FIXME_STUB'].copysignl
    copysignl.restype = ctypes.c_double
    copysignl.argtypes = [ctypes.c_double, ctypes.c_double]
    cputws = _libraries['FIXME_STUB'].cputws
    cputws.restype = ctypes.c_int32
    cputws.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    creat = _libraries['FIXME_STUB'].creat
    creat.restype = ctypes.c_int32
    creat.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    ctime32 = _libraries['FIXME_STUB'].ctime32
    ctime32.restype = ctypes.c_char_p
    ctime32.argtypes = [ctypes.POINTER(__time32_t)]
    ctime32_s = _libraries['FIXME_STUB'].ctime32_s
    ctime32_s.restype = errno_t
    ctime32_s.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(__time32_t)]
    ctime64 = _libraries['FIXME_STUB'].ctime64
    ctime64.restype = ctypes.c_char_p
    ctime64.argtypes = [ctypes.POINTER(__time64_t)]
    ctime64_s = _libraries['FIXME_STUB'].ctime64_s
    ctime64_s.restype = errno_t
    ctime64_s.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(__time64_t)]
    cvt_dtoi_sat = _libraries['FIXME_STUB'].cvt_dtoi_sat
    cvt_dtoi_sat.restype = ctypes.c_int32
    cvt_dtoi_sat.argtypes = [ctypes.c_double]
    cvt_dtoi_sent = _libraries['FIXME_STUB'].cvt_dtoi_sent
    cvt_dtoi_sent.restype = ctypes.c_int32
    cvt_dtoi_sent.argtypes = [ctypes.c_double]
    cvt_dtoll_sat = _libraries['FIXME_STUB'].cvt_dtoll_sat
    cvt_dtoll_sat.restype = ctypes.c_int64
    cvt_dtoll_sat.argtypes = [ctypes.c_double]
    cvt_dtoll_sent = _libraries['FIXME_STUB'].cvt_dtoll_sent
    cvt_dtoll_sent.restype = ctypes.c_int64
    cvt_dtoll_sent.argtypes = [ctypes.c_double]
    cvt_dtoui_sat = _libraries['FIXME_STUB'].cvt_dtoui_sat
    cvt_dtoui_sat.restype = ctypes.c_uint32
    cvt_dtoui_sat.argtypes = [ctypes.c_double]
    cvt_dtoui_sent = _libraries['FIXME_STUB'].cvt_dtoui_sent
    cvt_dtoui_sent.restype = ctypes.c_uint32
    cvt_dtoui_sent.argtypes = [ctypes.c_double]
    cvt_dtoull_sat = _libraries['FIXME_STUB'].cvt_dtoull_sat
    cvt_dtoull_sat.restype = ctypes.c_uint64
    cvt_dtoull_sat.argtypes = [ctypes.c_double]
    cvt_dtoull_sent = _libraries['FIXME_STUB'].cvt_dtoull_sent
    cvt_dtoull_sent.restype = ctypes.c_uint64
    cvt_dtoull_sent.argtypes = [ctypes.c_double]
    cvt_ftoi_sat = _libraries['FIXME_STUB'].cvt_ftoi_sat
    cvt_ftoi_sat.restype = ctypes.c_int32
    cvt_ftoi_sat.argtypes = [ctypes.c_float]
    cvt_ftoi_sent = _libraries['FIXME_STUB'].cvt_ftoi_sent
    cvt_ftoi_sent.restype = ctypes.c_int32
    cvt_ftoi_sent.argtypes = [ctypes.c_float]
    cvt_ftoll_sat = _libraries['FIXME_STUB'].cvt_ftoll_sat
    cvt_ftoll_sat.restype = ctypes.c_int64
    cvt_ftoll_sat.argtypes = [ctypes.c_float]
    cvt_ftoll_sent = _libraries['FIXME_STUB'].cvt_ftoll_sent
    cvt_ftoll_sent.restype = ctypes.c_int64
    cvt_ftoll_sent.argtypes = [ctypes.c_float]
    cvt_ftoui_sat = _libraries['FIXME_STUB'].cvt_ftoui_sat
    cvt_ftoui_sat.restype = ctypes.c_uint32
    cvt_ftoui_sat.argtypes = [ctypes.c_float]
    cvt_ftoui_sent = _libraries['FIXME_STUB'].cvt_ftoui_sent
    cvt_ftoui_sent.restype = ctypes.c_uint32
    cvt_ftoui_sent.argtypes = [ctypes.c_float]
    cvt_ftoull_sat = _libraries['FIXME_STUB'].cvt_ftoull_sat
    cvt_ftoull_sat.restype = ctypes.c_uint64
    cvt_ftoull_sat.argtypes = [ctypes.c_float]
    cvt_ftoull_sent = _libraries['FIXME_STUB'].cvt_ftoull_sent
    cvt_ftoull_sent.restype = ctypes.c_uint64
    cvt_ftoull_sent.argtypes = [ctypes.c_float]
    cwprintf = _libraries['FIXME_STUB'].cwprintf
    cwprintf.restype = ctypes.c_int32
    cwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    cwprintf_l = _libraries['FIXME_STUB'].cwprintf_l
    cwprintf_l.restype = ctypes.c_int32
    cwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    cwprintf_p = _libraries['FIXME_STUB'].cwprintf_p
    cwprintf_p.restype = ctypes.c_int32
    cwprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    cwprintf_p_l = _libraries['FIXME_STUB'].cwprintf_p_l
    cwprintf_p_l.restype = ctypes.c_int32
    cwprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    cwprintf_s = _libraries['FIXME_STUB'].cwprintf_s
    cwprintf_s.restype = ctypes.c_int32
    cwprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    cwprintf_s_l = _libraries['FIXME_STUB'].cwprintf_s_l
    cwprintf_s_l.restype = ctypes.c_int32
    cwprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    cwscanf = _libraries['FIXME_STUB'].cwscanf
    cwscanf.restype = ctypes.c_int32
    cwscanf.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    cwscanf_l = _libraries['FIXME_STUB'].cwscanf_l
    cwscanf_l.restype = ctypes.c_int32
    cwscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    cwscanf_s = _libraries['FIXME_STUB'].cwscanf_s
    cwscanf_s.restype = ctypes.c_int32
    cwscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    cwscanf_s_l = _libraries['FIXME_STUB'].cwscanf_s_l
    cwscanf_s_l.restype = ctypes.c_int32
    cwscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    d_int = _libraries['FIXME_STUB'].d_int
    d_int.restype = ctypes.c_int16
    d_int.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int16]
    dclass = _libraries['FIXME_STUB'].dclass
    dclass.restype = ctypes.c_int16
    dclass.argtypes = [ctypes.c_double]
    dexp = _libraries['FIXME_STUB'].dexp
    dexp.restype = ctypes.c_int16
    dexp.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_int32]
    difftime32 = _libraries['FIXME_STUB'].difftime32
    difftime32.restype = ctypes.c_double
    difftime32.argtypes = [__time32_t, __time32_t]
    difftime64 = _libraries['FIXME_STUB'].difftime64
    difftime64.restype = ctypes.c_double
    difftime64.argtypes = [__time64_t, __time64_t]
    dlog = _libraries['FIXME_STUB'].dlog
    dlog.restype = ctypes.c_double
    dlog.argtypes = [ctypes.c_double, ctypes.c_int32]
    dnorm = _libraries['FIXME_STUB'].dnorm
    dnorm.restype = ctypes.c_int16
    dnorm.argtypes = [ctypes.POINTER(ctypes.c_uint16)]
    dpcomp = _libraries['FIXME_STUB'].dpcomp
    dpcomp.restype = ctypes.c_int32
    dpcomp.argtypes = [ctypes.c_double, ctypes.c_double]
    dpoly = _libraries['FIXME_STUB'].dpoly
    dpoly.restype = ctypes.c_double
    dpoly.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int32]
    dscale = _libraries['FIXME_STUB'].dscale
    dscale.restype = ctypes.c_int16
    dscale.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int32]
    dsign = _libraries['FIXME_STUB'].dsign
    dsign.restype = ctypes.c_int32
    dsign.argtypes = [ctypes.c_double]
    dsin = _libraries['FIXME_STUB'].dsin
    dsin.restype = ctypes.c_double
    dsin.argtypes = [ctypes.c_double, ctypes.c_uint32]
    dtest = _libraries['FIXME_STUB'].dtest
    dtest.restype = ctypes.c_int16
    dtest.argtypes = [ctypes.POINTER(ctypes.c_double)]
    dunscale = _libraries['FIXME_STUB'].dunscale
    dunscale.restype = ctypes.c_int16
    dunscale.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_double)]
    dup = _libraries['FIXME_STUB'].dup
    dup.restype = ctypes.c_int32
    dup.argtypes = [ctypes.c_int32]
    dup2 = _libraries['FIXME_STUB'].dup2
    dup2.restype = ctypes.c_int32
    dup2.argtypes = [ctypes.c_int32, ctypes.c_int32]
    dupenv_s = _libraries['FIXME_STUB'].dupenv_s
    dupenv_s.restype = errno_t
    dupenv_s.argtypes = [ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(size_t), ctypes.c_char_p]
    ecvt = _libraries['FIXME_STUB'].ecvt
    ecvt.restype = ctypes.c_char_p
    ecvt.argtypes = [ctypes.c_double, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    ecvt_s = _libraries['FIXME_STUB'].ecvt_s
    ecvt_s.restype = errno_t
    ecvt_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_double, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    eof = _libraries['FIXME_STUB'].eof
    eof.restype = ctypes.c_int32
    eof.argtypes = [ctypes.c_int32]
    errno = _libraries['FIXME_STUB'].errno
    errno.restype = ctypes.POINTER(ctypes.c_int32)
    errno.argtypes = []
    exit = _libraries['FIXME_STUB'].exit
    exit.restype = None
    exit.argtypes = [ctypes.c_int32]
    expand = _libraries['FIXME_STUB'].expand
    expand.restype = ctypes.POINTER(None)
    expand.argtypes = [ctypes.POINTER(None), size_t]
    fclose_nolock = _libraries['FIXME_STUB'].fclose_nolock
    fclose_nolock.restype = ctypes.c_int32
    fclose_nolock.argtypes = [ctypes.POINTER(FILE)]
    fcloseall = _libraries['FIXME_STUB'].fcloseall
    fcloseall.restype = ctypes.c_int32
    fcloseall.argtypes = []
    fcvt = _libraries['FIXME_STUB'].fcvt
    fcvt.restype = ctypes.c_char_p
    fcvt.argtypes = [ctypes.c_double, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    fcvt_s = _libraries['FIXME_STUB'].fcvt_s
    fcvt_s.restype = errno_t
    fcvt_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_double, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32)]
    fd_int = _libraries['FIXME_STUB'].fd_int
    fd_int.restype = ctypes.c_int16
    fd_int.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int16]
    fdclass = _libraries['FIXME_STUB'].fdclass
    fdclass.restype = ctypes.c_int16
    fdclass.argtypes = [ctypes.c_float]
    fdexp = _libraries['FIXME_STUB'].fdexp
    fdexp.restype = ctypes.c_int16
    fdexp.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_float, ctypes.c_int32]
    fdlog = _libraries['FIXME_STUB'].fdlog
    fdlog.restype = ctypes.c_float
    fdlog.argtypes = [ctypes.c_float, ctypes.c_int32]
    fdnorm = _libraries['FIXME_STUB'].fdnorm
    fdnorm.restype = ctypes.c_int16
    fdnorm.argtypes = [ctypes.POINTER(ctypes.c_uint16)]
    fdopen = _libraries['FIXME_STUB'].fdopen
    fdopen.restype = ctypes.POINTER(FILE)
    fdopen.argtypes = [ctypes.c_int32, ctypes.c_char_p]
    fdpcomp = _libraries['FIXME_STUB'].fdpcomp
    fdpcomp.restype = ctypes.c_int32
    fdpcomp.argtypes = [ctypes.c_float, ctypes.c_float]
    fdpoly = _libraries['FIXME_STUB'].fdpoly
    fdpoly.restype = ctypes.c_float
    fdpoly.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_float), ctypes.c_int32]
    fdscale = _libraries['FIXME_STUB'].fdscale
    fdscale.restype = ctypes.c_int16
    fdscale.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int32]
    fdsign = _libraries['FIXME_STUB'].fdsign
    fdsign.restype = ctypes.c_int32
    fdsign.argtypes = [ctypes.c_float]
    fdsin = _libraries['FIXME_STUB'].fdsin
    fdsin.restype = ctypes.c_float
    fdsin.argtypes = [ctypes.c_float, ctypes.c_uint32]
    fdtest = _libraries['FIXME_STUB'].fdtest
    fdtest.restype = ctypes.c_int16
    fdtest.argtypes = [ctypes.POINTER(ctypes.c_float)]
    fdunscale = _libraries['FIXME_STUB'].fdunscale
    fdunscale.restype = ctypes.c_int16
    fdunscale.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_float)]
    fflush_nolock = _libraries['FIXME_STUB'].fflush_nolock
    fflush_nolock.restype = ctypes.c_int32
    fflush_nolock.argtypes = [ctypes.POINTER(FILE)]
    fgetc_nolock = _libraries['FIXME_STUB'].fgetc_nolock
    fgetc_nolock.restype = ctypes.c_int32
    fgetc_nolock.argtypes = [ctypes.POINTER(FILE)]
    fgetchar = _libraries['FIXME_STUB'].fgetchar
    fgetchar.restype = ctypes.c_int32
    fgetchar.argtypes = []
    fgetwc_nolock = _libraries['FIXME_STUB'].fgetwc_nolock
    fgetwc_nolock.restype = wint_t
    fgetwc_nolock.argtypes = [ctypes.POINTER(FILE)]
    fgetwchar = _libraries['FIXME_STUB'].fgetwchar
    fgetwchar.restype = wint_t
    fgetwchar.argtypes = []
    filelength = _libraries['FIXME_STUB'].filelength
    filelength.restype = ctypes.c_int32
    filelength.argtypes = [ctypes.c_int32]
    filelengthi64 = _libraries['FIXME_STUB'].filelengthi64
    filelengthi64.restype = ctypes.c_int64
    filelengthi64.argtypes = [ctypes.c_int32]
    fileno = _libraries['FIXME_STUB'].fileno
    fileno.restype = ctypes.c_int32
    fileno.argtypes = [ctypes.POINTER(FILE)]
    findclose = _libraries['FIXME_STUB'].findclose
    findclose.restype = ctypes.c_int32
    findclose.argtypes = [intptr_t]
    findfirst32 = _libraries['FIXME_STUB'].findfirst32
    findfirst32.restype = intptr_t
    findfirst32.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__finddata32_t)]
    findfirst32i64 = _libraries['FIXME_STUB'].findfirst32i64
    findfirst32i64.restype = intptr_t
    findfirst32i64.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__finddata32i64_t)]
    findfirst64 = _libraries['FIXME_STUB'].findfirst64
    findfirst64.restype = intptr_t
    findfirst64.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct___finddata64_t)]
    findfirst64i32 = _libraries['FIXME_STUB'].findfirst64i32
    findfirst64i32.restype = intptr_t
    findfirst64i32.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__finddata64i32_t)]
    findnext32 = _libraries['FIXME_STUB'].findnext32
    findnext32.restype = ctypes.c_int32
    findnext32.argtypes = [intptr_t, ctypes.POINTER(struct__finddata32_t)]
    findnext32i64 = _libraries['FIXME_STUB'].findnext32i64
    findnext32i64.restype = ctypes.c_int32
    findnext32i64.argtypes = [intptr_t, ctypes.POINTER(struct__finddata32i64_t)]
    findnext64 = _libraries['FIXME_STUB'].findnext64
    findnext64.restype = ctypes.c_int32
    findnext64.argtypes = [intptr_t, ctypes.POINTER(struct___finddata64_t)]
    findnext64i32 = _libraries['FIXME_STUB'].findnext64i32
    findnext64i32.restype = ctypes.c_int32
    findnext64i32.argtypes = [intptr_t, ctypes.POINTER(struct__finddata64i32_t)]
    finite = _libraries['FIXME_STUB'].finite
    finite.restype = ctypes.c_int32
    finite.argtypes = [ctypes.c_double]
    finitef = _libraries['FIXME_STUB'].finitef
    finitef.restype = ctypes.c_int32
    finitef.argtypes = [ctypes.c_float]
    flushall = _libraries['FIXME_STUB'].flushall
    flushall.restype = ctypes.c_int32
    flushall.argtypes = []
    fpclass = _libraries['FIXME_STUB'].fpclass
    fpclass.restype = ctypes.c_int32
    fpclass.argtypes = [ctypes.c_double]
    fpclassf = _libraries['FIXME_STUB'].fpclassf
    fpclassf.restype = ctypes.c_int32
    fpclassf.argtypes = [ctypes.c_float]
    fperrraise = _libraries['FIXME_STUB'].fperrraise
    fperrraise.restype = None
    fperrraise.argtypes = [ctypes.c_int32]
    fpreset = _libraries['FIXME_STUB'].fpreset
    fpreset.restype = None
    fpreset.argtypes = []
    fprintf_l = _libraries['FIXME_STUB'].fprintf_l
    fprintf_l.restype = ctypes.c_int32
    fprintf_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t]
    fprintf_p = _libraries['FIXME_STUB'].fprintf_p
    fprintf_p.restype = ctypes.c_int32
    fprintf_p.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    fprintf_p_l = _libraries['FIXME_STUB'].fprintf_p_l
    fprintf_p_l.restype = ctypes.c_int32
    fprintf_p_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t]
    fprintf_s_l = _libraries['FIXME_STUB'].fprintf_s_l
    fprintf_s_l.restype = ctypes.c_int32
    fprintf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t]
    fputc_nolock = _libraries['FIXME_STUB'].fputc_nolock
    fputc_nolock.restype = ctypes.c_int32
    fputc_nolock.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    fputchar = _libraries['FIXME_STUB'].fputchar
    fputchar.restype = ctypes.c_int32
    fputchar.argtypes = [ctypes.c_int32]
    fputwc_nolock = _libraries['FIXME_STUB'].fputwc_nolock
    fputwc_nolock.restype = wint_t
    fputwc_nolock.argtypes = [ctypes.c_int16, ctypes.POINTER(FILE)]
    fputwchar = _libraries['FIXME_STUB'].fputwchar
    fputwchar.restype = wint_t
    fputwchar.argtypes = [ctypes.c_int16]
    fread_nolock = _libraries['FIXME_STUB'].fread_nolock
    fread_nolock.restype = size_t
    fread_nolock.argtypes = [ctypes.POINTER(None), size_t, size_t, ctypes.POINTER(FILE)]
    fread_nolock_s = _libraries['FIXME_STUB'].fread_nolock_s
    fread_nolock_s.restype = size_t
    fread_nolock_s.argtypes = [ctypes.POINTER(None), size_t, size_t, size_t, ctypes.POINTER(FILE)]
    free_base = _libraries['FIXME_STUB'].free_base
    free_base.restype = None
    free_base.argtypes = [ctypes.POINTER(None)]
    freea = _libraries['FIXME_STUB'].freea
    freea.restype = None
    freea.argtypes = [ctypes.POINTER(None)]
    fscanf_l = _libraries['FIXME_STUB'].fscanf_l
    fscanf_l.restype = ctypes.c_int32
    fscanf_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t]
    fscanf_s_l = _libraries['FIXME_STUB'].fscanf_s_l
    fscanf_s_l.restype = ctypes.c_int32
    fscanf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t]
    fseek_nolock = _libraries['FIXME_STUB'].fseek_nolock
    fseek_nolock.restype = ctypes.c_int32
    fseek_nolock.argtypes = [ctypes.POINTER(FILE), ctypes.c_int32, ctypes.c_int32]
    fseeki64 = _libraries['FIXME_STUB'].fseeki64
    fseeki64.restype = ctypes.c_int32
    fseeki64.argtypes = [ctypes.POINTER(FILE), ctypes.c_int64, ctypes.c_int32]
    fseeki64_nolock = _libraries['FIXME_STUB'].fseeki64_nolock
    fseeki64_nolock.restype = ctypes.c_int32
    fseeki64_nolock.argtypes = [ctypes.POINTER(FILE), ctypes.c_int64, ctypes.c_int32]
    fsopen = _libraries['FIXME_STUB'].fsopen
    fsopen.restype = ctypes.POINTER(FILE)
    fsopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]
    fstat32 = _libraries['FIXME_STUB'].fstat32
    fstat32.restype = ctypes.c_int32
    fstat32.argtypes = [ctypes.c_int32, ctypes.POINTER(struct__stat32)]
    fstat32i64 = _libraries['FIXME_STUB'].fstat32i64
    fstat32i64.restype = ctypes.c_int32
    fstat32i64.argtypes = [ctypes.c_int32, ctypes.POINTER(struct__stat32i64)]
    fstat64 = _libraries['FIXME_STUB'].fstat64
    fstat64.restype = ctypes.c_int32
    fstat64.argtypes = [ctypes.c_int32, ctypes.POINTER(struct__stat64)]
    fstat64i32 = _libraries['FIXME_STUB'].fstat64i32
    fstat64i32.restype = ctypes.c_int32
    fstat64i32.argtypes = [ctypes.c_int32, ctypes.POINTER(struct__stat64i32)]
    ftell_nolock = _libraries['FIXME_STUB'].ftell_nolock
    ftell_nolock.restype = ctypes.c_int32
    ftell_nolock.argtypes = [ctypes.POINTER(FILE)]
    ftelli64 = _libraries['FIXME_STUB'].ftelli64
    ftelli64.restype = ctypes.c_int64
    ftelli64.argtypes = [ctypes.POINTER(FILE)]
    ftelli64_nolock = _libraries['FIXME_STUB'].ftelli64_nolock
    ftelli64_nolock.restype = ctypes.c_int64
    ftelli64_nolock.argtypes = [ctypes.POINTER(FILE)]
    fullpath = _libraries['FIXME_STUB'].fullpath
    fullpath.restype = ctypes.c_char_p
    fullpath.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    fwprintf_l = _libraries['FIXME_STUB'].fwprintf_l
    fwprintf_l.restype = ctypes.c_int32
    fwprintf_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t]
    fwprintf_p = _libraries['FIXME_STUB'].fwprintf_p
    fwprintf_p.restype = ctypes.c_int32
    fwprintf_p.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16)]
    fwprintf_p_l = _libraries['FIXME_STUB'].fwprintf_p_l
    fwprintf_p_l.restype = ctypes.c_int32
    fwprintf_p_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t]
    fwprintf_s_l = _libraries['FIXME_STUB'].fwprintf_s_l
    fwprintf_s_l.restype = ctypes.c_int32
    fwprintf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t]
    fwrite_nolock = _libraries['FIXME_STUB'].fwrite_nolock
    fwrite_nolock.restype = size_t
    fwrite_nolock.argtypes = [ctypes.POINTER(None), size_t, size_t, ctypes.POINTER(FILE)]
    fwscanf_l = _libraries['FIXME_STUB'].fwscanf_l
    fwscanf_l.restype = ctypes.c_int32
    fwscanf_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t]
    fwscanf_s_l = _libraries['FIXME_STUB'].fwscanf_s_l
    fwscanf_s_l.restype = ctypes.c_int32
    fwscanf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t]
    gcvt = _libraries['FIXME_STUB'].gcvt
    gcvt.restype = ctypes.c_char_p
    gcvt.argtypes = [ctypes.c_double, ctypes.c_int32, ctypes.c_char_p]
    gcvt_s = _libraries['FIXME_STUB'].gcvt_s
    gcvt_s.restype = errno_t
    gcvt_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_double, ctypes.c_int32]
    get_FMA3_enable = _libraries['FIXME_STUB'].get_FMA3_enable
    get_FMA3_enable.restype = ctypes.c_int32
    get_FMA3_enable.argtypes = []
    get_daylight = _libraries['FIXME_STUB'].get_daylight
    get_daylight.restype = errno_t
    get_daylight.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    get_doserrno = _libraries['FIXME_STUB'].get_doserrno
    get_doserrno.restype = errno_t
    get_doserrno.argtypes = [ctypes.POINTER(ctypes.c_uint32)]
    get_dstbias = _libraries['FIXME_STUB'].get_dstbias
    get_dstbias.restype = errno_t
    get_dstbias.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    get_errno = _libraries['FIXME_STUB'].get_errno
    get_errno.restype = errno_t
    get_errno.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    get_fmode = _libraries['FIXME_STUB'].get_fmode
    get_fmode.restype = errno_t
    get_fmode.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    get_heap_handle = _libraries['FIXME_STUB'].get_heap_handle
    get_heap_handle.restype = intptr_t
    get_heap_handle.argtypes = []
    get_invalid_parameter_handler = _libraries['FIXME_STUB'].get_invalid_parameter_handler
    get_invalid_parameter_handler.restype = _invalid_parameter_handler
    get_invalid_parameter_handler.argtypes = []
    get_osfhandle = _libraries['FIXME_STUB'].get_osfhandle
    get_osfhandle.restype = intptr_t
    get_osfhandle.argtypes = [ctypes.c_int32]
    get_pgmptr = _libraries['FIXME_STUB'].get_pgmptr
    get_pgmptr.restype = errno_t
    get_pgmptr.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
    get_printf_count_output = _libraries['FIXME_STUB'].get_printf_count_output
    get_printf_count_output.restype = ctypes.c_int32
    get_printf_count_output.argtypes = []
    get_purecall_handler = _libraries['FIXME_STUB'].get_purecall_handler
    get_purecall_handler.restype = _purecall_handler
    get_purecall_handler.argtypes = []
    get_stream_buffer_pointers = _libraries['FIXME_STUB'].get_stream_buffer_pointers
    get_stream_buffer_pointers.restype = errno_t
    get_stream_buffer_pointers.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.POINTER(ctypes.c_char_p)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int32))]
    get_terminate = _libraries['FIXME_STUB'].get_terminate
    get_terminate.restype = terminate_handler
    get_terminate.argtypes = []
    get_thread_local_invalid_parameter_handler = _libraries['FIXME_STUB'].get_thread_local_invalid_parameter_handler
    get_thread_local_invalid_parameter_handler.restype = _invalid_parameter_handler
    get_thread_local_invalid_parameter_handler.argtypes = []
    get_timezone = _libraries['FIXME_STUB'].get_timezone
    get_timezone.restype = errno_t
    get_timezone.argtypes = [ctypes.POINTER(ctypes.c_int32)]
    get_tzname = _libraries['FIXME_STUB'].get_tzname
    get_tzname.restype = errno_t
    get_tzname.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, size_t, ctypes.c_int32]
    get_unexpected = _libraries['FIXME_STUB'].get_unexpected
    get_unexpected.restype = unexpected_handler
    get_unexpected.argtypes = []
    get_wpgmptr = _libraries['FIXME_STUB'].get_wpgmptr
    get_wpgmptr.restype = errno_t
    get_wpgmptr.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    getc_nolock = _libraries['FIXME_STUB'].getc_nolock
    getc_nolock.restype = ctypes.c_int32
    getc_nolock.argtypes = [ctypes.POINTER(FILE)]
    getcwd = _libraries['FIXME_STUB'].getcwd
    getcwd.restype = ctypes.c_char_p
    getcwd.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    getdcwd = _libraries['FIXME_STUB'].getdcwd
    getdcwd.restype = ctypes.c_char_p
    getdcwd.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32]
    getdiskfree = _libraries['FIXME_STUB'].getdiskfree
    getdiskfree.restype = ctypes.c_uint32
    getdiskfree.argtypes = [ctypes.c_uint32, ctypes.POINTER(struct__diskfree_t)]
    getdrive = _libraries['FIXME_STUB'].getdrive
    getdrive.restype = ctypes.c_int32
    getdrive.argtypes = []
    getdrives = _libraries['FIXME_STUB'].getdrives
    getdrives.restype = ctypes.c_uint32
    getdrives.argtypes = []
    getmaxstdio = _libraries['FIXME_STUB'].getmaxstdio
    getmaxstdio.restype = ctypes.c_int32
    getmaxstdio.argtypes = []
    getsystime = _libraries['FIXME_STUB'].getsystime
    getsystime.restype = ctypes.c_uint32
    getsystime.argtypes = [ctypes.POINTER(struct_tm)]
    getw = _libraries['FIXME_STUB'].getw
    getw.restype = ctypes.c_int32
    getw.argtypes = [ctypes.POINTER(FILE)]
    getwc_nolock = _libraries['FIXME_STUB'].getwc_nolock
    getwc_nolock.restype = wint_t
    getwc_nolock.argtypes = [ctypes.POINTER(FILE)]
    getwch = _libraries['FIXME_STUB'].getwch
    getwch.restype = wint_t
    getwch.argtypes = []
    getwch_nolock = _libraries['FIXME_STUB'].getwch_nolock
    getwch_nolock.restype = wint_t
    getwch_nolock.argtypes = []
    getwche = _libraries['FIXME_STUB'].getwche
    getwche.restype = wint_t
    getwche.argtypes = []
    getwche_nolock = _libraries['FIXME_STUB'].getwche_nolock
    getwche_nolock.restype = wint_t
    getwche_nolock.argtypes = []
    getws_s = _libraries['FIXME_STUB'].getws_s
    getws_s.restype = ctypes.POINTER(ctypes.c_int16)
    getws_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    gmtime32 = _libraries['FIXME_STUB'].gmtime32
    gmtime32.restype = ctypes.POINTER(struct_tm)
    gmtime32.argtypes = [ctypes.POINTER(__time32_t)]
    gmtime32_s = _libraries['FIXME_STUB'].gmtime32_s
    gmtime32_s.restype = errno_t
    gmtime32_s.argtypes = [ctypes.POINTER(struct_tm), ctypes.POINTER(__time32_t)]
    gmtime64 = _libraries['FIXME_STUB'].gmtime64
    gmtime64.restype = ctypes.POINTER(struct_tm)
    gmtime64.argtypes = [ctypes.POINTER(__time64_t)]
    gmtime64_s = _libraries['FIXME_STUB'].gmtime64_s
    gmtime64_s.restype = errno_t
    gmtime64_s.argtypes = [ctypes.POINTER(struct_tm), ctypes.POINTER(__time64_t)]
    heapchk = _libraries['FIXME_STUB'].heapchk
    heapchk.restype = ctypes.c_int32
    heapchk.argtypes = []
    heapmin = _libraries['FIXME_STUB'].heapmin
    heapmin.restype = ctypes.c_int32
    heapmin.argtypes = []
    heapwalk = _libraries['FIXME_STUB'].heapwalk
    heapwalk.restype = ctypes.c_int32
    heapwalk.argtypes = [ctypes.POINTER(_HEAPINFO)]
    hypot = _libraries['FIXME_STUB'].hypot
    hypot.restype = ctypes.c_double
    hypot.argtypes = [ctypes.c_double, ctypes.c_double]
    hypotf = _libraries['FIXME_STUB'].hypotf
    hypotf.restype = ctypes.c_float
    hypotf.argtypes = [ctypes.c_float, ctypes.c_float]
    hypotl = _libraries['FIXME_STUB'].hypotl
    hypotl.restype = ctypes.c_double
    hypotl.argtypes = [ctypes.c_double, ctypes.c_double]
    i64toa = _libraries['FIXME_STUB'].i64toa
    i64toa.restype = ctypes.c_char_p
    i64toa.argtypes = [ctypes.c_int64, ctypes.c_char_p, ctypes.c_int32]
    i64toa_s = _libraries['FIXME_STUB'].i64toa_s
    i64toa_s.restype = errno_t
    i64toa_s.argtypes = [ctypes.c_int64, ctypes.c_char_p, size_t, ctypes.c_int32]
    i64tow = _libraries['FIXME_STUB'].i64tow
    i64tow.restype = ctypes.POINTER(ctypes.c_int16)
    i64tow.argtypes = [ctypes.c_int64, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    i64tow_s = _libraries['FIXME_STUB'].i64tow_s
    i64tow_s.restype = errno_t
    i64tow_s.argtypes = [ctypes.c_int64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    interlockedand64 = _libraries['FIXME_STUB'].interlockedand64
    interlockedand64.restype = ctypes.c_int64
    interlockedand64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    interlockedbittestandset = _libraries['FIXME_STUB'].interlockedbittestandset
    interlockedbittestandset.restype = ctypes.c_ubyte
    interlockedbittestandset.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    interlockeddecrement64 = _libraries['FIXME_STUB'].interlockeddecrement64
    interlockeddecrement64.restype = ctypes.c_int64
    interlockeddecrement64.argtypes = [ctypes.POINTER(ctypes.c_int64)]
    interlockedexchange64 = _libraries['FIXME_STUB'].interlockedexchange64
    interlockedexchange64.restype = ctypes.c_int64
    interlockedexchange64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    interlockedexchangeadd64 = _libraries['FIXME_STUB'].interlockedexchangeadd64
    interlockedexchangeadd64.restype = ctypes.c_int64
    interlockedexchangeadd64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    interlockedincrement64 = _libraries['FIXME_STUB'].interlockedincrement64
    interlockedincrement64.restype = ctypes.c_int64
    interlockedincrement64.argtypes = [ctypes.POINTER(ctypes.c_int64)]
    interlockedor64 = _libraries['FIXME_STUB'].interlockedor64
    interlockedor64.restype = ctypes.c_int64
    interlockedor64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    interlockedxor64 = _libraries['FIXME_STUB'].interlockedxor64
    interlockedxor64.restype = ctypes.c_int64
    interlockedxor64.argtypes = [ctypes.POINTER(ctypes.c_int64), ctypes.c_int64]
    invalid_parameter_noinfo = _libraries['FIXME_STUB'].invalid_parameter_noinfo
    invalid_parameter_noinfo.restype = None
    invalid_parameter_noinfo.argtypes = []
    invalid_parameter_noinfo_noreturn = _libraries['FIXME_STUB'].invalid_parameter_noinfo_noreturn
    invalid_parameter_noinfo_noreturn.restype = None
    invalid_parameter_noinfo_noreturn.argtypes = []
    invoke_watson = _libraries['FIXME_STUB'].invoke_watson
    invoke_watson.restype = None
    invoke_watson.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.c_uint32, uintptr_t]
    is_exception_typeof = _libraries['FIXME_STUB'].is_exception_typeof
    is_exception_typeof.restype = ctypes.c_int32
    is_exception_typeof.argtypes = [ctypes.POINTER(struct_type_info), ctypes.POINTER(struct__EXCEPTION_POINTERS)]
    isalnum_l = _libraries['FIXME_STUB'].isalnum_l
    isalnum_l.restype = ctypes.c_int32
    isalnum_l.argtypes = [ctypes.c_int32, _locale_t]
    isalpha_l = _libraries['FIXME_STUB'].isalpha_l
    isalpha_l.restype = ctypes.c_int32
    isalpha_l.argtypes = [ctypes.c_int32, _locale_t]
    isatty = _libraries['FIXME_STUB'].isatty
    isatty.restype = ctypes.c_int32
    isatty.argtypes = [ctypes.c_int32]
    isblank_l = _libraries['FIXME_STUB'].isblank_l
    isblank_l.restype = ctypes.c_int32
    isblank_l.argtypes = [ctypes.c_int32, _locale_t]
    ischartype_l = _libraries['FIXME_STUB'].ischartype_l
    ischartype_l.restype = ctypes.c_int32
    ischartype_l.argtypes = [ctypes.c_int32, ctypes.c_int32, _locale_t]
    iscntrl_l = _libraries['FIXME_STUB'].iscntrl_l
    iscntrl_l.restype = ctypes.c_int32
    iscntrl_l.argtypes = [ctypes.c_int32, _locale_t]
    isctype = _libraries['FIXME_STUB'].isctype
    isctype.restype = ctypes.c_int32
    isctype.argtypes = [ctypes.c_int32, ctypes.c_int32]
    isctype_l = _libraries['FIXME_STUB'].isctype_l
    isctype_l.restype = ctypes.c_int32
    isctype_l.argtypes = [ctypes.c_int32, ctypes.c_int32, _locale_t]
    isdigit_l = _libraries['FIXME_STUB'].isdigit_l
    isdigit_l.restype = ctypes.c_int32
    isdigit_l.argtypes = [ctypes.c_int32, _locale_t]
    isgraph_l = _libraries['FIXME_STUB'].isgraph_l
    isgraph_l.restype = ctypes.c_int32
    isgraph_l.argtypes = [ctypes.c_int32, _locale_t]
    isleadbyte_l = _libraries['FIXME_STUB'].isleadbyte_l
    isleadbyte_l.restype = ctypes.c_int32
    isleadbyte_l.argtypes = [ctypes.c_int32, _locale_t]
    islower_l = _libraries['FIXME_STUB'].islower_l
    islower_l.restype = ctypes.c_int32
    islower_l.argtypes = [ctypes.c_int32, _locale_t]
    isnan = _libraries['FIXME_STUB'].isnan
    isnan.restype = ctypes.c_int32
    isnan.argtypes = [ctypes.c_double]
    isnanf = _libraries['FIXME_STUB'].isnanf
    isnanf.restype = ctypes.c_int32
    isnanf.argtypes = [ctypes.c_float]
    isprint_l = _libraries['FIXME_STUB'].isprint_l
    isprint_l.restype = ctypes.c_int32
    isprint_l.argtypes = [ctypes.c_int32, _locale_t]
    ispunct_l = _libraries['FIXME_STUB'].ispunct_l
    ispunct_l.restype = ctypes.c_int32
    ispunct_l.argtypes = [ctypes.c_int32, _locale_t]
    isspace_l = _libraries['FIXME_STUB'].isspace_l
    isspace_l.restype = ctypes.c_int32
    isspace_l.argtypes = [ctypes.c_int32, _locale_t]
    isupper_l = _libraries['FIXME_STUB'].isupper_l
    isupper_l.restype = ctypes.c_int32
    isupper_l.argtypes = [ctypes.c_int32, _locale_t]
    iswalnum_l = _libraries['FIXME_STUB'].iswalnum_l
    iswalnum_l.restype = ctypes.c_int32
    iswalnum_l.argtypes = [wint_t, _locale_t]
    iswalpha_l = _libraries['FIXME_STUB'].iswalpha_l
    iswalpha_l.restype = ctypes.c_int32
    iswalpha_l.argtypes = [wint_t, _locale_t]
    iswblank_l = _libraries['FIXME_STUB'].iswblank_l
    iswblank_l.restype = ctypes.c_int32
    iswblank_l.argtypes = [wint_t, _locale_t]
    iswcntrl_l = _libraries['FIXME_STUB'].iswcntrl_l
    iswcntrl_l.restype = ctypes.c_int32
    iswcntrl_l.argtypes = [wint_t, _locale_t]
    iswcsym_l = _libraries['FIXME_STUB'].iswcsym_l
    iswcsym_l.restype = ctypes.c_int32
    iswcsym_l.argtypes = [wint_t, _locale_t]
    iswcsymf_l = _libraries['FIXME_STUB'].iswcsymf_l
    iswcsymf_l.restype = ctypes.c_int32
    iswcsymf_l.argtypes = [wint_t, _locale_t]
    iswctype_l = _libraries['FIXME_STUB'].iswctype_l
    iswctype_l.restype = ctypes.c_int32
    iswctype_l.argtypes = [wint_t, wctype_t, _locale_t]
    iswdigit_l = _libraries['FIXME_STUB'].iswdigit_l
    iswdigit_l.restype = ctypes.c_int32
    iswdigit_l.argtypes = [wint_t, _locale_t]
    iswgraph_l = _libraries['FIXME_STUB'].iswgraph_l
    iswgraph_l.restype = ctypes.c_int32
    iswgraph_l.argtypes = [wint_t, _locale_t]
    iswlower_l = _libraries['FIXME_STUB'].iswlower_l
    iswlower_l.restype = ctypes.c_int32
    iswlower_l.argtypes = [wint_t, _locale_t]
    iswprint_l = _libraries['FIXME_STUB'].iswprint_l
    iswprint_l.restype = ctypes.c_int32
    iswprint_l.argtypes = [wint_t, _locale_t]
    iswpunct_l = _libraries['FIXME_STUB'].iswpunct_l
    iswpunct_l.restype = ctypes.c_int32
    iswpunct_l.argtypes = [wint_t, _locale_t]
    iswspace_l = _libraries['FIXME_STUB'].iswspace_l
    iswspace_l.restype = ctypes.c_int32
    iswspace_l.argtypes = [wint_t, _locale_t]
    iswupper_l = _libraries['FIXME_STUB'].iswupper_l
    iswupper_l.restype = ctypes.c_int32
    iswupper_l.argtypes = [wint_t, _locale_t]
    iswxdigit_l = _libraries['FIXME_STUB'].iswxdigit_l
    iswxdigit_l.restype = ctypes.c_int32
    iswxdigit_l.argtypes = [wint_t, _locale_t]
    isxdigit_l = _libraries['FIXME_STUB'].isxdigit_l
    isxdigit_l.restype = ctypes.c_int32
    isxdigit_l.argtypes = [ctypes.c_int32, _locale_t]
    itoa = _libraries['FIXME_STUB'].itoa
    itoa.restype = ctypes.c_char_p
    itoa.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32]
    itoa_s = _libraries['FIXME_STUB'].itoa_s
    itoa_s.restype = errno_t
    itoa_s.argtypes = [ctypes.c_int32, ctypes.c_char_p, size_t, ctypes.c_int32]
    itow = _libraries['FIXME_STUB'].itow
    itow.restype = ctypes.POINTER(ctypes.c_int16)
    itow.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    itow_s = _libraries['FIXME_STUB'].itow_s
    itow_s.restype = errno_t
    itow_s.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    j0 = _libraries['FIXME_STUB'].j0
    j0.restype = ctypes.c_double
    j0.argtypes = [ctypes.c_double]
    j1 = _libraries['FIXME_STUB'].j1
    j1.restype = ctypes.c_double
    j1.argtypes = [ctypes.c_double]
    jn = _libraries['FIXME_STUB'].jn
    jn.restype = ctypes.c_double
    jn.argtypes = [ctypes.c_int32, ctypes.c_double]
    ld_int = _libraries['FIXME_STUB'].ld_int
    ld_int.restype = ctypes.c_int16
    ld_int.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int16]
    ldclass = _libraries['FIXME_STUB'].ldclass
    ldclass.restype = ctypes.c_int16
    ldclass.argtypes = [ctypes.c_double]
    ldexp = _libraries['FIXME_STUB'].ldexp
    ldexp.restype = ctypes.c_int16
    ldexp.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double, ctypes.c_int32]
    ldlog = _libraries['FIXME_STUB'].ldlog
    ldlog.restype = ctypes.c_double
    ldlog.argtypes = [ctypes.c_double, ctypes.c_int32]
    ldpcomp = _libraries['FIXME_STUB'].ldpcomp
    ldpcomp.restype = ctypes.c_int32
    ldpcomp.argtypes = [ctypes.c_double, ctypes.c_double]
    ldpoly = _libraries['FIXME_STUB'].ldpoly
    ldpoly.restype = ctypes.c_double
    ldpoly.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int32]
    ldscale = _libraries['FIXME_STUB'].ldscale
    ldscale.restype = ctypes.c_int16
    ldscale.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int32]
    ldsign = _libraries['FIXME_STUB'].ldsign
    ldsign.restype = ctypes.c_int32
    ldsign.argtypes = [ctypes.c_double]
    ldsin = _libraries['FIXME_STUB'].ldsin
    ldsin.restype = ctypes.c_double
    ldsin.argtypes = [ctypes.c_double, ctypes.c_uint32]
    ldtest = _libraries['FIXME_STUB'].ldtest
    ldtest.restype = ctypes.c_int16
    ldtest.argtypes = [ctypes.POINTER(ctypes.c_double)]
    ldunscale = _libraries['FIXME_STUB'].ldunscale
    ldunscale.restype = ctypes.c_int16
    ldunscale.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_double)]
    lfind = _libraries['FIXME_STUB'].lfind
    lfind.restype = ctypes.POINTER(None)
    lfind.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, _CoreCrtNonSecureSearchSortCompareFunction]
    lfind_s = _libraries['FIXME_STUB'].lfind_s
    lfind_s.restype = ctypes.POINTER(None)
    lfind_s.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(ctypes.c_uint32), size_t, _CoreCrtSecureSearchSortCompareFunction, ctypes.POINTER(None)]
    localtime32 = _libraries['FIXME_STUB'].localtime32
    localtime32.restype = ctypes.POINTER(struct_tm)
    localtime32.argtypes = [ctypes.POINTER(__time32_t)]
    localtime32_s = _libraries['FIXME_STUB'].localtime32_s
    localtime32_s.restype = errno_t
    localtime32_s.argtypes = [ctypes.POINTER(struct_tm), ctypes.POINTER(__time32_t)]
    localtime64 = _libraries['FIXME_STUB'].localtime64
    localtime64.restype = ctypes.POINTER(struct_tm)
    localtime64.argtypes = [ctypes.POINTER(__time64_t)]
    localtime64_s = _libraries['FIXME_STUB'].localtime64_s
    localtime64_s.restype = errno_t
    localtime64_s.argtypes = [ctypes.POINTER(struct_tm), ctypes.POINTER(__time64_t)]
    lock_file = _libraries['FIXME_STUB'].lock_file
    lock_file.restype = None
    lock_file.argtypes = [ctypes.POINTER(FILE)]
    locking = _libraries['FIXME_STUB'].locking
    locking.restype = ctypes.c_int32
    locking.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    logb = _libraries['FIXME_STUB'].logb
    logb.restype = ctypes.c_double
    logb.argtypes = [ctypes.c_double]
    logbf = _libraries['FIXME_STUB'].logbf
    logbf.restype = ctypes.c_float
    logbf.argtypes = [ctypes.c_float]
    lrotl = _libraries['FIXME_STUB'].lrotl
    lrotl.restype = ctypes.c_uint32
    lrotl.argtypes = [ctypes.c_uint32, ctypes.c_int32]
    lrotr = _libraries['FIXME_STUB'].lrotr
    lrotr.restype = ctypes.c_uint32
    lrotr.argtypes = [ctypes.c_uint32, ctypes.c_int32]
    lsearch = _libraries['FIXME_STUB'].lsearch
    lsearch.restype = ctypes.POINTER(None)
    lsearch.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(ctypes.c_uint32), ctypes.c_uint32, _CoreCrtNonSecureSearchSortCompareFunction]
    lsearch_s = _libraries['FIXME_STUB'].lsearch_s
    lsearch_s.restype = ctypes.POINTER(None)
    lsearch_s.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.POINTER(ctypes.c_uint32), size_t, _CoreCrtSecureSearchSortCompareFunction, ctypes.POINTER(None)]
    lseek = _libraries['FIXME_STUB'].lseek
    lseek.restype = ctypes.c_int32
    lseek.argtypes = [ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    lseeki64 = _libraries['FIXME_STUB'].lseeki64
    lseeki64.restype = ctypes.c_int64
    lseeki64.argtypes = [ctypes.c_int32, ctypes.c_int64, ctypes.c_int32]
    ltoa = _libraries['FIXME_STUB'].ltoa
    ltoa.restype = ctypes.c_char_p
    ltoa.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.c_int32]
    ltoa_s = _libraries['FIXME_STUB'].ltoa_s
    ltoa_s.restype = errno_t
    ltoa_s.argtypes = [ctypes.c_int32, ctypes.c_char_p, size_t, ctypes.c_int32]
    ltow = _libraries['FIXME_STUB'].ltow
    ltow.restype = ctypes.POINTER(ctypes.c_int16)
    ltow.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    ltow_s = _libraries['FIXME_STUB'].ltow_s
    ltow_s.restype = errno_t
    ltow_s.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    makepath = _libraries['FIXME_STUB'].makepath
    makepath.restype = None
    makepath.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    makepath_s = _libraries['FIXME_STUB'].makepath_s
    makepath_s.restype = errno_t
    makepath_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    malloc_base = _libraries['FIXME_STUB'].malloc_base
    malloc_base.restype = ctypes.POINTER(None)
    malloc_base.argtypes = [size_t]
    matherr = _libraries['FIXME_STUB'].matherr
    matherr.restype = ctypes.c_int32
    matherr.argtypes = [ctypes.POINTER(struct__exception)]
    mblen_l = _libraries['FIXME_STUB'].mblen_l
    mblen_l.restype = ctypes.c_int32
    mblen_l.argtypes = [ctypes.c_char_p, size_t, _locale_t]
    mbstowcs_l = _libraries['FIXME_STUB'].mbstowcs_l
    mbstowcs_l.restype = size_t
    mbstowcs_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_char_p, size_t, _locale_t]
    mbstowcs_s_l = _libraries['FIXME_STUB'].mbstowcs_s_l
    mbstowcs_s_l.restype = errno_t
    mbstowcs_s_l.argtypes = [ctypes.POINTER(size_t), ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_char_p, size_t, _locale_t]
    mbstrlen = _libraries['FIXME_STUB'].mbstrlen
    mbstrlen.restype = size_t
    mbstrlen.argtypes = [ctypes.c_char_p]
    mbstrlen_l = _libraries['FIXME_STUB'].mbstrlen_l
    mbstrlen_l.restype = size_t
    mbstrlen_l.argtypes = [ctypes.c_char_p, _locale_t]
    mbstrnlen = _libraries['FIXME_STUB'].mbstrnlen
    mbstrnlen.restype = size_t
    mbstrnlen.argtypes = [ctypes.c_char_p, size_t]
    mbstrnlen_l = _libraries['FIXME_STUB'].mbstrnlen_l
    mbstrnlen_l.restype = size_t
    mbstrnlen_l.argtypes = [ctypes.c_char_p, size_t, _locale_t]
    mbtowc_l = _libraries['FIXME_STUB'].mbtowc_l
    mbtowc_l.restype = ctypes.c_int32
    mbtowc_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_char_p, size_t, _locale_t]
    memccpy = _libraries['FIXME_STUB'].memccpy
    memccpy.restype = ctypes.POINTER(None)
    memccpy.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), ctypes.c_int32, size_t]
    memicmp = _libraries['FIXME_STUB'].memicmp
    memicmp.restype = ctypes.c_int32
    memicmp.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t]
    memicmp_l = _libraries['FIXME_STUB'].memicmp_l
    memicmp_l.restype = ctypes.c_int32
    memicmp_l.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t, _locale_t]
    mkdir = _libraries['FIXME_STUB'].mkdir
    mkdir.restype = ctypes.c_int32
    mkdir.argtypes = [ctypes.c_char_p]
    mkgmtime32 = _libraries['FIXME_STUB'].mkgmtime32
    mkgmtime32.restype = __time32_t
    mkgmtime32.argtypes = [ctypes.POINTER(struct_tm)]
    mkgmtime64 = _libraries['FIXME_STUB'].mkgmtime64
    mkgmtime64.restype = __time64_t
    mkgmtime64.argtypes = [ctypes.POINTER(struct_tm)]
    mktemp = _libraries['FIXME_STUB'].mktemp
    mktemp.restype = ctypes.c_char_p
    mktemp.argtypes = [ctypes.c_char_p]
    mktemp_s = _libraries['FIXME_STUB'].mktemp_s
    mktemp_s.restype = errno_t
    mktemp_s.argtypes = [ctypes.c_char_p, size_t]
    mktime32 = _libraries['FIXME_STUB'].mktime32
    mktime32.restype = __time32_t
    mktime32.argtypes = [ctypes.POINTER(struct_tm)]
    mktime64 = _libraries['FIXME_STUB'].mktime64
    mktime64.restype = __time64_t
    mktime64.argtypes = [ctypes.POINTER(struct_tm)]
    mm_pause = _libraries['FIXME_STUB'].mm_pause
    mm_pause.restype = None
    mm_pause.argtypes = []
    msize = _libraries['FIXME_STUB'].msize
    msize.restype = size_t
    msize.argtypes = [ctypes.POINTER(None)]
    msize_base = _libraries['FIXME_STUB'].msize_base
    msize_base.restype = size_t
    msize_base.argtypes = [ctypes.POINTER(None)]
    nextafter = _libraries['FIXME_STUB'].nextafter
    nextafter.restype = ctypes.c_double
    nextafter.argtypes = [ctypes.c_double, ctypes.c_double]
    nextafterf = _libraries['FIXME_STUB'].nextafterf
    nextafterf.restype = ctypes.c_float
    nextafterf.argtypes = [ctypes.c_float, ctypes.c_float]
    onexit = _libraries['FIXME_STUB'].onexit
    onexit.restype = _onexit_t
    onexit.argtypes = [_onexit_t]
    open_osfhandle = _libraries['FIXME_STUB'].open_osfhandle
    open_osfhandle.restype = ctypes.c_int32
    open_osfhandle.argtypes = [intptr_t, ctypes.c_int32]
    pclose = _libraries['FIXME_STUB'].pclose
    pclose.restype = ctypes.c_int32
    pclose.argtypes = [ctypes.POINTER(FILE)]
    pipe = _libraries['FIXME_STUB'].pipe
    pipe.restype = ctypes.c_int32
    pipe.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_uint32, ctypes.c_int32]
    popen = _libraries['FIXME_STUB'].popen
    popen.restype = ctypes.POINTER(FILE)
    popen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    printf_l = _libraries['FIXME_STUB'].printf_l
    printf_l.restype = ctypes.c_int32
    printf_l.argtypes = [ctypes.c_char_p, _locale_t]
    printf_p = _libraries['FIXME_STUB'].printf_p
    printf_p.restype = ctypes.c_int32
    printf_p.argtypes = [ctypes.c_char_p]
    printf_p_l = _libraries['FIXME_STUB'].printf_p_l
    printf_p_l.restype = ctypes.c_int32
    printf_p_l.argtypes = [ctypes.c_char_p, _locale_t]
    printf_s_l = _libraries['FIXME_STUB'].printf_s_l
    printf_s_l.restype = ctypes.c_int32
    printf_s_l.argtypes = [ctypes.c_char_p, _locale_t]
    putc_nolock = _libraries['FIXME_STUB'].putc_nolock
    putc_nolock.restype = ctypes.c_int32
    putc_nolock.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    putenv = _libraries['FIXME_STUB'].putenv
    putenv.restype = ctypes.c_int32
    putenv.argtypes = [ctypes.c_char_p]
    putenv_s = _libraries['FIXME_STUB'].putenv_s
    putenv_s.restype = errno_t
    putenv_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    putw = _libraries['FIXME_STUB'].putw
    putw.restype = ctypes.c_int32
    putw.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    putwc_nolock = _libraries['FIXME_STUB'].putwc_nolock
    putwc_nolock.restype = wint_t
    putwc_nolock.argtypes = [ctypes.c_int16, ctypes.POINTER(FILE)]
    putwch = _libraries['FIXME_STUB'].putwch
    putwch.restype = wint_t
    putwch.argtypes = [ctypes.c_int16]
    putwch_nolock = _libraries['FIXME_STUB'].putwch_nolock
    putwch_nolock.restype = wint_t
    putwch_nolock.argtypes = [ctypes.c_int16]
    putws = _libraries['FIXME_STUB'].putws
    putws.restype = ctypes.c_int32
    putws.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    read = _libraries['FIXME_STUB'].read
    read.restype = ctypes.c_int32
    read.argtypes = [ctypes.c_int32, ctypes.POINTER(None), ctypes.c_uint32]
    realloc_base = _libraries['FIXME_STUB'].realloc_base
    realloc_base.restype = ctypes.POINTER(None)
    realloc_base.argtypes = [ctypes.POINTER(None), size_t]
    recalloc = _libraries['FIXME_STUB'].recalloc
    recalloc.restype = ctypes.POINTER(None)
    recalloc.argtypes = [ctypes.POINTER(None), size_t, size_t]
    recalloc_base = _libraries['FIXME_STUB'].recalloc_base
    recalloc_base.restype = ctypes.POINTER(None)
    recalloc_base.argtypes = [ctypes.POINTER(None), size_t, size_t]
    resetstkoflw = _libraries['FIXME_STUB'].resetstkoflw
    resetstkoflw.restype = ctypes.c_int32
    resetstkoflw.argtypes = []
    rmdir = _libraries['FIXME_STUB'].rmdir
    rmdir.restype = ctypes.c_int32
    rmdir.argtypes = [ctypes.c_char_p]
    rmtmp = _libraries['FIXME_STUB'].rmtmp
    rmtmp.restype = ctypes.c_int32
    rmtmp.argtypes = []
    rotl = _libraries['FIXME_STUB'].rotl
    rotl.restype = ctypes.c_uint32
    rotl.argtypes = [ctypes.c_uint32, ctypes.c_int32]
    rotl64 = _libraries['FIXME_STUB'].rotl64
    rotl64.restype = ctypes.c_uint64
    rotl64.argtypes = [ctypes.c_uint64, ctypes.c_int32]
    rotr = _libraries['FIXME_STUB'].rotr
    rotr.restype = ctypes.c_uint32
    rotr.argtypes = [ctypes.c_uint32, ctypes.c_int32]
    rotr64 = _libraries['FIXME_STUB'].rotr64
    rotr64.restype = ctypes.c_uint64
    rotr64.argtypes = [ctypes.c_uint64, ctypes.c_int32]
    scalb = _libraries['FIXME_STUB'].scalb
    scalb.restype = ctypes.c_double
    scalb.argtypes = [ctypes.c_double, ctypes.c_int32]
    scalbf = _libraries['FIXME_STUB'].scalbf
    scalbf.restype = ctypes.c_float
    scalbf.argtypes = [ctypes.c_float, ctypes.c_int32]
    scanf_l = _libraries['FIXME_STUB'].scanf_l
    scanf_l.restype = ctypes.c_int32
    scanf_l.argtypes = [ctypes.c_char_p, _locale_t]
    scanf_s_l = _libraries['FIXME_STUB'].scanf_s_l
    scanf_s_l.restype = ctypes.c_int32
    scanf_s_l.argtypes = [ctypes.c_char_p, _locale_t]
    scprintf = _libraries['FIXME_STUB'].scprintf
    scprintf.restype = ctypes.c_int32
    scprintf.argtypes = [ctypes.c_char_p]
    scprintf_l = _libraries['FIXME_STUB'].scprintf_l
    scprintf_l.restype = ctypes.c_int32
    scprintf_l.argtypes = [ctypes.c_char_p, _locale_t]
    scprintf_p = _libraries['FIXME_STUB'].scprintf_p
    scprintf_p.restype = ctypes.c_int32
    scprintf_p.argtypes = [ctypes.c_char_p]
    scprintf_p_l = _libraries['FIXME_STUB'].scprintf_p_l
    scprintf_p_l.restype = ctypes.c_int32
    scprintf_p_l.argtypes = [ctypes.c_char_p, _locale_t]
    scwprintf = _libraries['FIXME_STUB'].scwprintf
    scwprintf.restype = ctypes.c_int32
    scwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    scwprintf_l = _libraries['FIXME_STUB'].scwprintf_l
    scwprintf_l.restype = ctypes.c_int32
    scwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    scwprintf_p = _libraries['FIXME_STUB'].scwprintf_p
    scwprintf_p.restype = ctypes.c_int32
    scwprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    scwprintf_p_l = _libraries['FIXME_STUB'].scwprintf_p_l
    scwprintf_p_l.restype = ctypes.c_int32
    scwprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    searchenv = _libraries['FIXME_STUB'].searchenv
    searchenv.restype = None
    searchenv.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    searchenv_s = _libraries['FIXME_STUB'].searchenv_s
    searchenv_s.restype = errno_t
    searchenv_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, size_t]
    set_FMA3_enable = _libraries['FIXME_STUB'].set_FMA3_enable
    set_FMA3_enable.restype = ctypes.c_int32
    set_FMA3_enable.argtypes = [ctypes.c_int32]
    set_abort_behavior = _libraries['FIXME_STUB'].set_abort_behavior
    set_abort_behavior.restype = ctypes.c_uint32
    set_abort_behavior.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    set_controlfp = _libraries['FIXME_STUB'].set_controlfp
    set_controlfp.restype = None
    set_controlfp.argtypes = [ctypes.c_uint32, ctypes.c_uint32]
    set_doserrno = _libraries['FIXME_STUB'].set_doserrno
    set_doserrno.restype = errno_t
    set_doserrno.argtypes = [ctypes.c_uint32]
    set_errno = _libraries['FIXME_STUB'].set_errno
    set_errno.restype = errno_t
    set_errno.argtypes = [ctypes.c_int32]
    set_error_mode = _libraries['FIXME_STUB'].set_error_mode
    set_error_mode.restype = ctypes.c_int32
    set_error_mode.argtypes = [ctypes.c_int32]
    set_fmode = _libraries['FIXME_STUB'].set_fmode
    set_fmode.restype = errno_t
    set_fmode.argtypes = [ctypes.c_int32]
    set_invalid_parameter_handler = _libraries['FIXME_STUB'].set_invalid_parameter_handler
    set_invalid_parameter_handler.restype = _invalid_parameter_handler
    set_invalid_parameter_handler.argtypes = [_invalid_parameter_handler]
    set_printf_count_output = _libraries['FIXME_STUB'].set_printf_count_output
    set_printf_count_output.restype = ctypes.c_int32
    set_printf_count_output.argtypes = [ctypes.c_int32]
    set_purecall_handler = _libraries['FIXME_STUB'].set_purecall_handler
    set_purecall_handler.restype = _purecall_handler
    set_purecall_handler.argtypes = [_purecall_handler]
    set_se_translator = _libraries['FIXME_STUB'].set_se_translator
    set_se_translator.restype = _se_translator_function
    set_se_translator.argtypes = [_se_translator_function]
    set_thread_local_invalid_parameter_handler = _libraries['FIXME_STUB'].set_thread_local_invalid_parameter_handler
    set_thread_local_invalid_parameter_handler.restype = _invalid_parameter_handler
    set_thread_local_invalid_parameter_handler.argtypes = [_invalid_parameter_handler]
    seterrormode = _libraries['FIXME_STUB'].seterrormode
    seterrormode.restype = None
    seterrormode.argtypes = [ctypes.c_int32]
    setmaxstdio = _libraries['FIXME_STUB'].setmaxstdio
    setmaxstdio.restype = ctypes.c_int32
    setmaxstdio.argtypes = [ctypes.c_int32]
    setmode = _libraries['FIXME_STUB'].setmode
    setmode.restype = ctypes.c_int32
    setmode.argtypes = [ctypes.c_int32, ctypes.c_int32]
    setsystime = _libraries['FIXME_STUB'].setsystime
    setsystime.restype = ctypes.c_uint32
    setsystime.argtypes = [ctypes.POINTER(struct_tm), ctypes.c_uint32]
    sleep = _libraries['FIXME_STUB'].sleep
    sleep.restype = None
    sleep.argtypes = [ctypes.c_uint32]
    snprintf = _libraries['FIXME_STUB'].snprintf
    snprintf.restype = ctypes.c_int32
    snprintf.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    snprintf_c = _libraries['FIXME_STUB'].snprintf_c
    snprintf_c.restype = ctypes.c_int32
    snprintf_c.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    snprintf_c_l = _libraries['FIXME_STUB'].snprintf_c_l
    snprintf_c_l.restype = ctypes.c_int32
    snprintf_c_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    snprintf_l = _libraries['FIXME_STUB'].snprintf_l
    snprintf_l.restype = ctypes.c_int32
    snprintf_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    snprintf_s = _libraries['FIXME_STUB'].snprintf_s
    snprintf_s.restype = ctypes.c_int32
    snprintf_s.argtypes = [ctypes.c_char_p, size_t, size_t, ctypes.c_char_p]
    snprintf_s_l = _libraries['FIXME_STUB'].snprintf_s_l
    snprintf_s_l.restype = ctypes.c_int32
    snprintf_s_l.argtypes = [ctypes.c_char_p, size_t, size_t, ctypes.c_char_p, _locale_t]
    snscanf = _libraries['FIXME_STUB'].snscanf
    snscanf.restype = ctypes.c_int32
    snscanf.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    snscanf_l = _libraries['FIXME_STUB'].snscanf_l
    snscanf_l.restype = ctypes.c_int32
    snscanf_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    snscanf_s = _libraries['FIXME_STUB'].snscanf_s
    snscanf_s.restype = ctypes.c_int32
    snscanf_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    snscanf_s_l = _libraries['FIXME_STUB'].snscanf_s_l
    snscanf_s_l.restype = ctypes.c_int32
    snscanf_s_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    snwprintf = _libraries['FIXME_STUB'].snwprintf
    snwprintf.restype = ctypes.c_int32
    snwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    snwprintf_l = _libraries['FIXME_STUB'].snwprintf_l
    snwprintf_l.restype = ctypes.c_int32
    snwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    snwprintf_s = _libraries['FIXME_STUB'].snwprintf_s
    snwprintf_s.restype = ctypes.c_int32
    snwprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, size_t, ctypes.POINTER(ctypes.c_int16)]
    snwprintf_s_l = _libraries['FIXME_STUB'].snwprintf_s_l
    snwprintf_s_l.restype = ctypes.c_int32
    snwprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    snwscanf = _libraries['FIXME_STUB'].snwscanf
    snwscanf.restype = ctypes.c_int32
    snwscanf.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    snwscanf_l = _libraries['FIXME_STUB'].snwscanf_l
    snwscanf_l.restype = ctypes.c_int32
    snwscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    snwscanf_s = _libraries['FIXME_STUB'].snwscanf_s
    snwscanf_s.restype = ctypes.c_int32
    snwscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    snwscanf_s_l = _libraries['FIXME_STUB'].snwscanf_s_l
    snwscanf_s_l.restype = ctypes.c_int32
    snwscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    sopen_dispatch = _libraries['FIXME_STUB'].sopen_dispatch
    sopen_dispatch.restype = errno_t
    sopen_dispatch.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    sopen_s = _libraries['FIXME_STUB'].sopen_s
    sopen_s.restype = errno_t
    sopen_s.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    sopen_s_nolock = _libraries['FIXME_STUB'].sopen_s_nolock
    sopen_s_nolock.restype = errno_t
    sopen_s_nolock.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    splitpath = _libraries['FIXME_STUB'].splitpath
    splitpath.restype = None
    splitpath.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
    splitpath_s = _libraries['FIXME_STUB'].splitpath_s
    splitpath_s.restype = errno_t
    splitpath_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, ctypes.c_char_p, size_t, ctypes.c_char_p, size_t, ctypes.c_char_p, size_t]
    sprintf_l = _libraries['FIXME_STUB'].sprintf_l
    sprintf_l.restype = ctypes.c_int32
    sprintf_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    sprintf_p = _libraries['FIXME_STUB'].sprintf_p
    sprintf_p.restype = ctypes.c_int32
    sprintf_p.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    sprintf_p_l = _libraries['FIXME_STUB'].sprintf_p_l
    sprintf_p_l.restype = ctypes.c_int32
    sprintf_p_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    sprintf_s_l = _libraries['FIXME_STUB'].sprintf_s_l
    sprintf_s_l.restype = ctypes.c_int32
    sprintf_s_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t]
    sscanf_l = _libraries['FIXME_STUB'].sscanf_l
    sscanf_l.restype = ctypes.c_int32
    sscanf_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    sscanf_s_l = _libraries['FIXME_STUB'].sscanf_s_l
    sscanf_s_l.restype = ctypes.c_int32
    sscanf_s_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    stat32 = _libraries['FIXME_STUB'].stat32
    stat32.restype = ctypes.c_int32
    stat32.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__stat32)]
    stat32i64 = _libraries['FIXME_STUB'].stat32i64
    stat32i64.restype = ctypes.c_int32
    stat32i64.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__stat32i64)]
    stat64 = _libraries['FIXME_STUB'].stat64
    stat64.restype = ctypes.c_int32
    stat64.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__stat64)]
    stat64i32 = _libraries['FIXME_STUB'].stat64i32
    stat64i32.restype = ctypes.c_int32
    stat64i32.argtypes = [ctypes.c_char_p, ctypes.POINTER(struct__stat64i32)]
    statusfp = _libraries['FIXME_STUB'].statusfp
    statusfp.restype = ctypes.c_uint32
    statusfp.argtypes = []
    strcmpi = _libraries['FIXME_STUB'].strcmpi
    strcmpi.restype = ctypes.c_int32
    strcmpi.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcoll_l = _libraries['FIXME_STUB'].strcoll_l
    strcoll_l.restype = ctypes.c_int32
    strcoll_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    strdate = _libraries['FIXME_STUB'].strdate
    strdate.restype = ctypes.c_char_p
    strdate.argtypes = [ctypes.c_char_p]
    strdate_s = _libraries['FIXME_STUB'].strdate_s
    strdate_s.restype = errno_t
    strdate_s.argtypes = [ctypes.c_char_p, size_t]
    strdup = _libraries['FIXME_STUB'].strdup
    strdup.restype = ctypes.c_char_p
    strdup.argtypes = [ctypes.c_char_p]
    strerror = _libraries['FIXME_STUB'].strerror
    strerror.restype = ctypes.c_char_p
    strerror.argtypes = [ctypes.c_char_p]
    strerror_s = _libraries['FIXME_STUB'].strerror_s
    strerror_s.restype = errno_t
    strerror_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    strftime_l = _libraries['FIXME_STUB'].strftime_l
    strftime_l.restype = size_t
    strftime_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.POINTER(struct_tm), _locale_t]
    stricmp = _libraries['FIXME_STUB'].stricmp
    stricmp.restype = ctypes.c_int32
    stricmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    stricmp_l = _libraries['FIXME_STUB'].stricmp_l
    stricmp_l.restype = ctypes.c_int32
    stricmp_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    stricoll = _libraries['FIXME_STUB'].stricoll
    stricoll.restype = ctypes.c_int32
    stricoll.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    stricoll_l = _libraries['FIXME_STUB'].stricoll_l
    stricoll_l.restype = ctypes.c_int32
    stricoll_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t]
    strlwr = _libraries['FIXME_STUB'].strlwr
    strlwr.restype = ctypes.c_char_p
    strlwr.argtypes = [ctypes.c_char_p]
    strlwr_l = _libraries['FIXME_STUB'].strlwr_l
    strlwr_l.restype = ctypes.c_char_p
    strlwr_l.argtypes = [ctypes.c_char_p, _locale_t]
    strlwr_s = _libraries['FIXME_STUB'].strlwr_s
    strlwr_s.restype = errno_t
    strlwr_s.argtypes = [ctypes.c_char_p, size_t]
    strlwr_s_l = _libraries['FIXME_STUB'].strlwr_s_l
    strlwr_s_l.restype = errno_t
    strlwr_s_l.argtypes = [ctypes.c_char_p, size_t, _locale_t]
    strncoll = _libraries['FIXME_STUB'].strncoll
    strncoll.restype = ctypes.c_int32
    strncoll.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strncoll_l = _libraries['FIXME_STUB'].strncoll_l
    strncoll_l.restype = ctypes.c_int32
    strncoll_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, _locale_t]
    strnicmp = _libraries['FIXME_STUB'].strnicmp
    strnicmp.restype = ctypes.c_int32
    strnicmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strnicmp_l = _libraries['FIXME_STUB'].strnicmp_l
    strnicmp_l.restype = ctypes.c_int32
    strnicmp_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, _locale_t]
    strnicoll = _libraries['FIXME_STUB'].strnicoll
    strnicoll.restype = ctypes.c_int32
    strnicoll.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strnicoll_l = _libraries['FIXME_STUB'].strnicoll_l
    strnicoll_l.restype = ctypes.c_int32
    strnicoll_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, _locale_t]
    strnset = _libraries['FIXME_STUB'].strnset
    strnset.restype = ctypes.c_char_p
    strnset.argtypes = [ctypes.c_char_p, ctypes.c_int32, size_t]
    strnset_s = _libraries['FIXME_STUB'].strnset_s
    strnset_s.restype = errno_t
    strnset_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_int32, size_t]
    strrev = _libraries['FIXME_STUB'].strrev
    strrev.restype = ctypes.c_char_p
    strrev.argtypes = [ctypes.c_char_p]
    strset = _libraries['FIXME_STUB'].strset
    strset.restype = ctypes.c_char_p
    strset.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    strset_s = _libraries['FIXME_STUB'].strset_s
    strset_s.restype = errno_t
    strset_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_int32]
    strtime = _libraries['FIXME_STUB'].strtime
    strtime.restype = ctypes.c_char_p
    strtime.argtypes = [ctypes.c_char_p]
    strtime_s = _libraries['FIXME_STUB'].strtime_s
    strtime_s.restype = errno_t
    strtime_s.argtypes = [ctypes.c_char_p, size_t]
    strtod_l = _libraries['FIXME_STUB'].strtod_l
    strtod_l.restype = ctypes.c_double
    strtod_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), _locale_t]
    strtof_l = _libraries['FIXME_STUB'].strtof_l
    strtof_l.restype = ctypes.c_float
    strtof_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), _locale_t]
    strtoi64 = _libraries['FIXME_STUB'].strtoi64
    strtoi64.restype = ctypes.c_int64
    strtoi64.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strtoi64_l = _libraries['FIXME_STUB'].strtoi64_l
    strtoi64_l.restype = ctypes.c_int64
    strtoi64_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strtol_l = _libraries['FIXME_STUB'].strtol_l
    strtol_l.restype = ctypes.c_int32
    strtol_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strtold_l = _libraries['FIXME_STUB'].strtold_l
    strtold_l.restype = ctypes.c_double
    strtold_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), _locale_t]
    strtoll_l = _libraries['FIXME_STUB'].strtoll_l
    strtoll_l.restype = ctypes.c_int64
    strtoll_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strtoui64 = _libraries['FIXME_STUB'].strtoui64
    strtoui64.restype = ctypes.c_uint64
    strtoui64.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strtoui64_l = _libraries['FIXME_STUB'].strtoui64_l
    strtoui64_l.restype = ctypes.c_uint64
    strtoui64_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strtoul_l = _libraries['FIXME_STUB'].strtoul_l
    strtoul_l.restype = ctypes.c_uint32
    strtoul_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strtoull_l = _libraries['FIXME_STUB'].strtoull_l
    strtoull_l.restype = ctypes.c_uint64
    strtoull_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32, _locale_t]
    strupr = _libraries['FIXME_STUB'].strupr
    strupr.restype = ctypes.c_char_p
    strupr.argtypes = [ctypes.c_char_p]
    strupr_l = _libraries['FIXME_STUB'].strupr_l
    strupr_l.restype = ctypes.c_char_p
    strupr_l.argtypes = [ctypes.c_char_p, _locale_t]
    strupr_s = _libraries['FIXME_STUB'].strupr_s
    strupr_s.restype = errno_t
    strupr_s.argtypes = [ctypes.c_char_p, size_t]
    strupr_s_l = _libraries['FIXME_STUB'].strupr_s_l
    strupr_s_l.restype = errno_t
    strupr_s_l.argtypes = [ctypes.c_char_p, size_t, _locale_t]
    strxfrm_l = _libraries['FIXME_STUB'].strxfrm_l
    strxfrm_l.restype = size_t
    strxfrm_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t, _locale_t]
    swab = _libraries['FIXME_STUB'].swab
    swab.restype = None
    swab.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int32]
    swprintf = _libraries['FIXME_STUB'].swprintf
    swprintf.restype = ctypes.c_int32
    swprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    swprintf_c = _libraries['FIXME_STUB'].swprintf_c
    swprintf_c.restype = ctypes.c_int32
    swprintf_c.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    swprintf_c_l = _libraries['FIXME_STUB'].swprintf_c_l
    swprintf_c_l.restype = ctypes.c_int32
    swprintf_c_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    swprintf_l = _libraries['FIXME_STUB'].swprintf_l
    swprintf_l.restype = ctypes.c_int32
    swprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    swprintf_p = _libraries['FIXME_STUB'].swprintf_p
    swprintf_p.restype = ctypes.c_int32
    swprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    swprintf_p_l = _libraries['FIXME_STUB'].swprintf_p_l
    swprintf_p_l.restype = ctypes.c_int32
    swprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    swprintf_s_l = _libraries['FIXME_STUB'].swprintf_s_l
    swprintf_s_l.restype = ctypes.c_int32
    swprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t]
    swscanf_l = _libraries['FIXME_STUB'].swscanf_l
    swscanf_l.restype = ctypes.c_int32
    swscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    swscanf_s_l = _libraries['FIXME_STUB'].swscanf_s_l
    swscanf_s_l.restype = ctypes.c_int32
    swscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    tell = _libraries['FIXME_STUB'].tell
    tell.restype = ctypes.c_int32
    tell.argtypes = [ctypes.c_int32]
    telli64 = _libraries['FIXME_STUB'].telli64
    telli64.restype = ctypes.c_int64
    telli64.argtypes = [ctypes.c_int32]
    tempnam = _libraries['FIXME_STUB'].tempnam
    tempnam.restype = ctypes.c_char_p
    tempnam.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    time32 = _libraries['FIXME_STUB'].time32
    time32.restype = __time32_t
    time32.argtypes = [ctypes.POINTER(__time32_t)]
    time64 = _libraries['FIXME_STUB'].time64
    time64.restype = __time64_t
    time64.argtypes = [ctypes.POINTER(__time64_t)]
    timespec32_get = _libraries['FIXME_STUB'].timespec32_get
    timespec32_get.restype = ctypes.c_int32
    timespec32_get.argtypes = [ctypes.POINTER(struct__timespec32), ctypes.c_int32]
    timespec64_get = _libraries['FIXME_STUB'].timespec64_get
    timespec64_get.restype = ctypes.c_int32
    timespec64_get.argtypes = [ctypes.POINTER(struct__timespec64), ctypes.c_int32]
    tolower = _libraries['FIXME_STUB'].tolower
    tolower.restype = ctypes.c_int32
    tolower.argtypes = [ctypes.c_int32]
    tolower_l = _libraries['FIXME_STUB'].tolower_l
    tolower_l.restype = ctypes.c_int32
    tolower_l.argtypes = [ctypes.c_int32, _locale_t]
    toupper = _libraries['FIXME_STUB'].toupper
    toupper.restype = ctypes.c_int32
    toupper.argtypes = [ctypes.c_int32]
    toupper_l = _libraries['FIXME_STUB'].toupper_l
    toupper_l.restype = ctypes.c_int32
    toupper_l.argtypes = [ctypes.c_int32, _locale_t]
    towlower_l = _libraries['FIXME_STUB'].towlower_l
    towlower_l.restype = wint_t
    towlower_l.argtypes = [wint_t, _locale_t]
    towupper_l = _libraries['FIXME_STUB'].towupper_l
    towupper_l.restype = wint_t
    towupper_l.argtypes = [wint_t, _locale_t]
    tzset = _libraries['FIXME_STUB'].tzset
    tzset.restype = None
    tzset.argtypes = []
    ui64toa = _libraries['FIXME_STUB'].ui64toa
    ui64toa.restype = ctypes.c_char_p
    ui64toa.argtypes = [ctypes.c_uint64, ctypes.c_char_p, ctypes.c_int32]
    ui64toa_s = _libraries['FIXME_STUB'].ui64toa_s
    ui64toa_s.restype = errno_t
    ui64toa_s.argtypes = [ctypes.c_uint64, ctypes.c_char_p, size_t, ctypes.c_int32]
    ui64tow = _libraries['FIXME_STUB'].ui64tow
    ui64tow.restype = ctypes.POINTER(ctypes.c_int16)
    ui64tow.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    ui64tow_s = _libraries['FIXME_STUB'].ui64tow_s
    ui64tow_s.restype = errno_t
    ui64tow_s.argtypes = [ctypes.c_uint64, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    ultoa = _libraries['FIXME_STUB'].ultoa
    ultoa.restype = ctypes.c_char_p
    ultoa.argtypes = [ctypes.c_uint32, ctypes.c_char_p, ctypes.c_int32]
    ultoa_s = _libraries['FIXME_STUB'].ultoa_s
    ultoa_s.restype = errno_t
    ultoa_s.argtypes = [ctypes.c_uint32, ctypes.c_char_p, size_t, ctypes.c_int32]
    ultow = _libraries['FIXME_STUB'].ultow
    ultow.restype = ctypes.POINTER(ctypes.c_int16)
    ultow.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    ultow_s = _libraries['FIXME_STUB'].ultow_s
    ultow_s.restype = errno_t
    ultow_s.argtypes = [ctypes.c_uint32, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    umask = _libraries['FIXME_STUB'].umask
    umask.restype = ctypes.c_int32
    umask.argtypes = [ctypes.c_int32]
    umask_s = _libraries['FIXME_STUB'].umask_s
    umask_s.restype = errno_t
    umask_s.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
    umul128 = _libraries['FIXME_STUB'].umul128
    umul128.restype = ctypes.c_uint64
    umul128.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.POINTER(ctypes.c_uint64)]
    ungetc_nolock = _libraries['FIXME_STUB'].ungetc_nolock
    ungetc_nolock.restype = ctypes.c_int32
    ungetc_nolock.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    ungetwc_nolock = _libraries['FIXME_STUB'].ungetwc_nolock
    ungetwc_nolock.restype = wint_t
    ungetwc_nolock.argtypes = [wint_t, ctypes.POINTER(FILE)]
    ungetwch = _libraries['FIXME_STUB'].ungetwch
    ungetwch.restype = wint_t
    ungetwch.argtypes = [wint_t]
    ungetwch_nolock = _libraries['FIXME_STUB'].ungetwch_nolock
    ungetwch_nolock.restype = wint_t
    ungetwch_nolock.argtypes = [wint_t]
    unlink = _libraries['FIXME_STUB'].unlink
    unlink.restype = ctypes.c_int32
    unlink.argtypes = [ctypes.c_char_p]
    unlock_file = _libraries['FIXME_STUB'].unlock_file
    unlock_file.restype = None
    unlock_file.argtypes = [ctypes.POINTER(FILE)]
    vcwprintf = _libraries['FIXME_STUB'].vcwprintf
    vcwprintf.restype = ctypes.c_int32
    vcwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vcwprintf_l = _libraries['FIXME_STUB'].vcwprintf_l
    vcwprintf_l.restype = ctypes.c_int32
    vcwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vcwprintf_p = _libraries['FIXME_STUB'].vcwprintf_p
    vcwprintf_p.restype = ctypes.c_int32
    vcwprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vcwprintf_p_l = _libraries['FIXME_STUB'].vcwprintf_p_l
    vcwprintf_p_l.restype = ctypes.c_int32
    vcwprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vcwprintf_s = _libraries['FIXME_STUB'].vcwprintf_s
    vcwprintf_s.restype = ctypes.c_int32
    vcwprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vcwprintf_s_l = _libraries['FIXME_STUB'].vcwprintf_s_l
    vcwprintf_s_l.restype = ctypes.c_int32
    vcwprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vcwscanf = _libraries['FIXME_STUB'].vcwscanf
    vcwscanf.restype = ctypes.c_int32
    vcwscanf.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vcwscanf_l = _libraries['FIXME_STUB'].vcwscanf_l
    vcwscanf_l.restype = ctypes.c_int32
    vcwscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vcwscanf_s = _libraries['FIXME_STUB'].vcwscanf_s
    vcwscanf_s.restype = ctypes.c_int32
    vcwscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vcwscanf_s_l = _libraries['FIXME_STUB'].vcwscanf_s_l
    vcwscanf_s_l.restype = ctypes.c_int32
    vcwscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vfprintf_l = _libraries['FIXME_STUB'].vfprintf_l
    vfprintf_l.restype = ctypes.c_int32
    vfprintf_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    vfprintf_p = _libraries['FIXME_STUB'].vfprintf_p
    vfprintf_p.restype = ctypes.c_int32
    vfprintf_p.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    vfprintf_p_l = _libraries['FIXME_STUB'].vfprintf_p_l
    vfprintf_p_l.restype = ctypes.c_int32
    vfprintf_p_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    vfprintf_s_l = _libraries['FIXME_STUB'].vfprintf_s_l
    vfprintf_s_l.restype = ctypes.c_int32
    vfprintf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    vfscanf_l = _libraries['FIXME_STUB'].vfscanf_l
    vfscanf_l.restype = ctypes.c_int32
    vfscanf_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    vfscanf_s_l = _libraries['FIXME_STUB'].vfscanf_s_l
    vfscanf_s_l.restype = ctypes.c_int32
    vfscanf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, _locale_t, va_list]
    vfwprintf_l = _libraries['FIXME_STUB'].vfwprintf_l
    vfwprintf_l.restype = ctypes.c_int32
    vfwprintf_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vfwprintf_p = _libraries['FIXME_STUB'].vfwprintf_p
    vfwprintf_p.restype = ctypes.c_int32
    vfwprintf_p.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), va_list]
    vfwprintf_p_l = _libraries['FIXME_STUB'].vfwprintf_p_l
    vfwprintf_p_l.restype = ctypes.c_int32
    vfwprintf_p_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vfwprintf_s_l = _libraries['FIXME_STUB'].vfwprintf_s_l
    vfwprintf_s_l.restype = ctypes.c_int32
    vfwprintf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vfwscanf_l = _libraries['FIXME_STUB'].vfwscanf_l
    vfwscanf_l.restype = ctypes.c_int32
    vfwscanf_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vfwscanf_s_l = _libraries['FIXME_STUB'].vfwscanf_s_l
    vfwscanf_s_l.restype = ctypes.c_int32
    vfwscanf_s_l.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vprintf_l = _libraries['FIXME_STUB'].vprintf_l
    vprintf_l.restype = ctypes.c_int32
    vprintf_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vprintf_p = _libraries['FIXME_STUB'].vprintf_p
    vprintf_p.restype = ctypes.c_int32
    vprintf_p.argtypes = [ctypes.c_char_p, va_list]
    vprintf_p_l = _libraries['FIXME_STUB'].vprintf_p_l
    vprintf_p_l.restype = ctypes.c_int32
    vprintf_p_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vprintf_s_l = _libraries['FIXME_STUB'].vprintf_s_l
    vprintf_s_l.restype = ctypes.c_int32
    vprintf_s_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vscanf_l = _libraries['FIXME_STUB'].vscanf_l
    vscanf_l.restype = ctypes.c_int32
    vscanf_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vscanf_s_l = _libraries['FIXME_STUB'].vscanf_s_l
    vscanf_s_l.restype = ctypes.c_int32
    vscanf_s_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vscprintf = _libraries['FIXME_STUB'].vscprintf
    vscprintf.restype = ctypes.c_int32
    vscprintf.argtypes = [ctypes.c_char_p, va_list]
    vscprintf_l = _libraries['FIXME_STUB'].vscprintf_l
    vscprintf_l.restype = ctypes.c_int32
    vscprintf_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vscprintf_p = _libraries['FIXME_STUB'].vscprintf_p
    vscprintf_p.restype = ctypes.c_int32
    vscprintf_p.argtypes = [ctypes.c_char_p, va_list]
    vscprintf_p_l = _libraries['FIXME_STUB'].vscprintf_p_l
    vscprintf_p_l.restype = ctypes.c_int32
    vscprintf_p_l.argtypes = [ctypes.c_char_p, _locale_t, va_list]
    vscwprintf = _libraries['FIXME_STUB'].vscwprintf
    vscwprintf.restype = ctypes.c_int32
    vscwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vscwprintf_l = _libraries['FIXME_STUB'].vscwprintf_l
    vscwprintf_l.restype = ctypes.c_int32
    vscwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vscwprintf_p = _libraries['FIXME_STUB'].vscwprintf_p
    vscwprintf_p.restype = ctypes.c_int32
    vscwprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vscwprintf_p_l = _libraries['FIXME_STUB'].vscwprintf_p_l
    vscwprintf_p_l.restype = ctypes.c_int32
    vscwprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vsnprintf = _libraries['FIXME_STUB'].vsnprintf
    vsnprintf.restype = ctypes.c_int32
    vsnprintf.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    vsnprintf_c = _libraries['FIXME_STUB'].vsnprintf_c
    vsnprintf_c.restype = ctypes.c_int32
    vsnprintf_c.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    vsnprintf_c_l = _libraries['FIXME_STUB'].vsnprintf_c_l
    vsnprintf_c_l.restype = ctypes.c_int32
    vsnprintf_c_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    vsnprintf_l = _libraries['FIXME_STUB'].vsnprintf_l
    vsnprintf_l.restype = ctypes.c_int32
    vsnprintf_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    vsnprintf_s = _libraries['FIXME_STUB'].vsnprintf_s
    vsnprintf_s.restype = ctypes.c_int32
    vsnprintf_s.argtypes = [ctypes.c_char_p, size_t, size_t, ctypes.c_char_p, va_list]
    vsnprintf_s_l = _libraries['FIXME_STUB'].vsnprintf_s_l
    vsnprintf_s_l.restype = ctypes.c_int32
    vsnprintf_s_l.argtypes = [ctypes.c_char_p, size_t, size_t, ctypes.c_char_p, _locale_t, va_list]
    vsnwprintf = _libraries['FIXME_STUB'].vsnwprintf
    vsnwprintf.restype = ctypes.c_int32
    vsnwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), va_list]
    vsnwprintf_l = _libraries['FIXME_STUB'].vsnwprintf_l
    vsnwprintf_l.restype = ctypes.c_int32
    vsnwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vsnwprintf_s = _libraries['FIXME_STUB'].vsnwprintf_s
    vsnwprintf_s.restype = ctypes.c_int32
    vsnwprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, size_t, ctypes.POINTER(ctypes.c_int16), va_list]
    vsnwprintf_s_l = _libraries['FIXME_STUB'].vsnwprintf_s_l
    vsnwprintf_s_l.restype = ctypes.c_int32
    vsnwprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vsnwscanf_l = _libraries['FIXME_STUB'].vsnwscanf_l
    vsnwscanf_l.restype = ctypes.c_int32
    vsnwscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vsnwscanf_s_l = _libraries['FIXME_STUB'].vsnwscanf_s_l
    vsnwscanf_s_l.restype = ctypes.c_int32
    vsnwscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vsprintf_l = _libraries['FIXME_STUB'].vsprintf_l
    vsprintf_l.restype = ctypes.c_int32
    vsprintf_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t, va_list]
    vsprintf_p = _libraries['FIXME_STUB'].vsprintf_p
    vsprintf_p.restype = ctypes.c_int32
    vsprintf_p.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    vsprintf_p_l = _libraries['FIXME_STUB'].vsprintf_p_l
    vsprintf_p_l.restype = ctypes.c_int32
    vsprintf_p_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    vsprintf_s_l = _libraries['FIXME_STUB'].vsprintf_s_l
    vsprintf_s_l.restype = ctypes.c_int32
    vsprintf_s_l.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, _locale_t, va_list]
    vsscanf_l = _libraries['FIXME_STUB'].vsscanf_l
    vsscanf_l.restype = ctypes.c_int32
    vsscanf_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t, va_list]
    vsscanf_s_l = _libraries['FIXME_STUB'].vsscanf_s_l
    vsscanf_s_l.restype = ctypes.c_int32
    vsscanf_s_l.argtypes = [ctypes.c_char_p, ctypes.c_char_p, _locale_t, va_list]
    vswprintf = _libraries['FIXME_STUB'].vswprintf
    vswprintf.restype = ctypes.c_int32
    vswprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), va_list]
    vswprintf_c = _libraries['FIXME_STUB'].vswprintf_c
    vswprintf_c.restype = ctypes.c_int32
    vswprintf_c.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), va_list]
    vswprintf_c_l = _libraries['FIXME_STUB'].vswprintf_c_l
    vswprintf_c_l.restype = ctypes.c_int32
    vswprintf_c_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vswprintf_l = _libraries['FIXME_STUB'].vswprintf_l
    vswprintf_l.restype = ctypes.c_int32
    vswprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vswprintf_p = _libraries['FIXME_STUB'].vswprintf_p
    vswprintf_p.restype = ctypes.c_int32
    vswprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), va_list]
    vswprintf_p_l = _libraries['FIXME_STUB'].vswprintf_p_l
    vswprintf_p_l.restype = ctypes.c_int32
    vswprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vswprintf_s_l = _libraries['FIXME_STUB'].vswprintf_s_l
    vswprintf_s_l.restype = ctypes.c_int32
    vswprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vswscanf_l = _libraries['FIXME_STUB'].vswscanf_l
    vswscanf_l.restype = ctypes.c_int32
    vswscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vswscanf_s_l = _libraries['FIXME_STUB'].vswscanf_s_l
    vswscanf_s_l.restype = ctypes.c_int32
    vswscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vwprintf_l = _libraries['FIXME_STUB'].vwprintf_l
    vwprintf_l.restype = ctypes.c_int32
    vwprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vwprintf_p = _libraries['FIXME_STUB'].vwprintf_p
    vwprintf_p.restype = ctypes.c_int32
    vwprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vwprintf_p_l = _libraries['FIXME_STUB'].vwprintf_p_l
    vwprintf_p_l.restype = ctypes.c_int32
    vwprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vwprintf_s_l = _libraries['FIXME_STUB'].vwprintf_s_l
    vwprintf_s_l.restype = ctypes.c_int32
    vwprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vwscanf_l = _libraries['FIXME_STUB'].vwscanf_l
    vwscanf_l.restype = ctypes.c_int32
    vwscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    vwscanf_s_l = _libraries['FIXME_STUB'].vwscanf_s_l
    vwscanf_s_l.restype = ctypes.c_int32
    vwscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t, va_list]
    waccess = _libraries['FIXME_STUB'].waccess
    waccess.restype = ctypes.c_int32
    waccess.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    waccess_s = _libraries['FIXME_STUB'].waccess_s
    waccess_s.restype = errno_t
    waccess_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wasctime = _libraries['FIXME_STUB'].wasctime
    wasctime.restype = ctypes.POINTER(ctypes.c_int16)
    wasctime.argtypes = [ctypes.POINTER(struct_tm)]
    wasctime_s = _libraries['FIXME_STUB'].wasctime_s
    wasctime_s.restype = errno_t
    wasctime_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(struct_tm)]
    wassert = _libraries['FIXME_STUB'].wassert
    wassert.restype = None
    wassert.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.c_uint32]
    wchdir = _libraries['FIXME_STUB'].wchdir
    wchdir.restype = ctypes.c_int32
    wchdir.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wchmod = _libraries['FIXME_STUB'].wchmod
    wchmod.restype = ctypes.c_int32
    wchmod.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wcreat = _libraries['FIXME_STUB'].wcreat
    wcreat.restype = ctypes.c_int32
    wcreat.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wcreate_locale = _libraries['FIXME_STUB'].wcreate_locale
    wcreate_locale.restype = _locale_t
    wcreate_locale.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16)]
    wcscoll_l = _libraries['FIXME_STUB'].wcscoll_l
    wcscoll_l.restype = ctypes.c_int32
    wcscoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    wcsdup = _libraries['FIXME_STUB'].wcsdup
    wcsdup.restype = ctypes.POINTER(ctypes.c_int16)
    wcsdup.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wcserror = _libraries['FIXME_STUB'].wcserror
    wcserror.restype = ctypes.POINTER(ctypes.c_int16)
    wcserror.argtypes = [ctypes.c_int32]
    wcserror_s = _libraries['FIXME_STUB'].wcserror_s
    wcserror_s.restype = errno_t
    wcserror_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int32]
    wcsftime_l = _libraries['FIXME_STUB'].wcsftime_l
    wcsftime_l.restype = size_t
    wcsftime_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct_tm), _locale_t]
    wcsicmp = _libraries['FIXME_STUB'].wcsicmp
    wcsicmp.restype = ctypes.c_int32
    wcsicmp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcsicmp_l = _libraries['FIXME_STUB'].wcsicmp_l
    wcsicmp_l.restype = ctypes.c_int32
    wcsicmp_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    wcsicoll = _libraries['FIXME_STUB'].wcsicoll
    wcsicoll.restype = ctypes.c_int32
    wcsicoll.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcsicoll_l = _libraries['FIXME_STUB'].wcsicoll_l
    wcsicoll_l.restype = ctypes.c_int32
    wcsicoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), _locale_t]
    wcslwr = _libraries['FIXME_STUB'].wcslwr
    wcslwr.restype = ctypes.POINTER(ctypes.c_int16)
    wcslwr.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wcslwr_l = _libraries['FIXME_STUB'].wcslwr_l
    wcslwr_l.restype = ctypes.POINTER(ctypes.c_int16)
    wcslwr_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wcslwr_s = _libraries['FIXME_STUB'].wcslwr_s
    wcslwr_s.restype = errno_t
    wcslwr_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wcslwr_s_l = _libraries['FIXME_STUB'].wcslwr_s_l
    wcslwr_s_l.restype = errno_t
    wcslwr_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcsncoll = _libraries['FIXME_STUB'].wcsncoll
    wcsncoll.restype = ctypes.c_int32
    wcsncoll.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsncoll_l = _libraries['FIXME_STUB'].wcsncoll_l
    wcsncoll_l.restype = ctypes.c_int32
    wcsncoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcsnicmp = _libraries['FIXME_STUB'].wcsnicmp
    wcsnicmp.restype = ctypes.c_int32
    wcsnicmp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsnicmp_l = _libraries['FIXME_STUB'].wcsnicmp_l
    wcsnicmp_l.restype = ctypes.c_int32
    wcsnicmp_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcsnicoll = _libraries['FIXME_STUB'].wcsnicoll
    wcsnicoll.restype = ctypes.c_int32
    wcsnicoll.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsnicoll_l = _libraries['FIXME_STUB'].wcsnicoll_l
    wcsnicoll_l.restype = ctypes.c_int32
    wcsnicoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcsnset = _libraries['FIXME_STUB'].wcsnset
    wcsnset.restype = ctypes.POINTER(ctypes.c_int16)
    wcsnset.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16, size_t]
    wcsnset_s = _libraries['FIXME_STUB'].wcsnset_s
    wcsnset_s.restype = errno_t
    wcsnset_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int16, size_t]
    wcsrev = _libraries['FIXME_STUB'].wcsrev
    wcsrev.restype = ctypes.POINTER(ctypes.c_int16)
    wcsrev.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wcsset = _libraries['FIXME_STUB'].wcsset
    wcsset.restype = ctypes.POINTER(ctypes.c_int16)
    wcsset.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    wcsset_s = _libraries['FIXME_STUB'].wcsset_s
    wcsset_s.restype = errno_t
    wcsset_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_int16]
    wcstod_l = _libraries['FIXME_STUB'].wcstod_l
    wcstod_l.restype = ctypes.c_double
    wcstod_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), _locale_t]
    wcstof_l = _libraries['FIXME_STUB'].wcstof_l
    wcstof_l.restype = ctypes.c_float
    wcstof_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), _locale_t]
    wcstoi64 = _libraries['FIXME_STUB'].wcstoi64
    wcstoi64.restype = ctypes.c_int64
    wcstoi64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcstoi64_l = _libraries['FIXME_STUB'].wcstoi64_l
    wcstoi64_l.restype = ctypes.c_int64
    wcstoi64_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcstol_l = _libraries['FIXME_STUB'].wcstol_l
    wcstol_l.restype = ctypes.c_int32
    wcstol_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcstold_l = _libraries['FIXME_STUB'].wcstold_l
    wcstold_l.restype = ctypes.c_double
    wcstold_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), _locale_t]
    wcstoll_l = _libraries['FIXME_STUB'].wcstoll_l
    wcstoll_l.restype = ctypes.c_int64
    wcstoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcstombs_l = _libraries['FIXME_STUB'].wcstombs_l
    wcstombs_l.restype = size_t
    wcstombs_l.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcstombs_s_l = _libraries['FIXME_STUB'].wcstombs_s_l
    wcstombs_s_l.restype = errno_t
    wcstombs_s_l.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, size_t, ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcstoui64 = _libraries['FIXME_STUB'].wcstoui64
    wcstoui64.restype = ctypes.c_uint64
    wcstoui64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcstoui64_l = _libraries['FIXME_STUB'].wcstoui64_l
    wcstoui64_l.restype = ctypes.c_uint64
    wcstoui64_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcstoul_l = _libraries['FIXME_STUB'].wcstoul_l
    wcstoul_l.restype = ctypes.c_uint32
    wcstoul_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcstoull_l = _libraries['FIXME_STUB'].wcstoull_l
    wcstoull_l.restype = ctypes.c_uint64
    wcstoull_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32, _locale_t]
    wcsupr = _libraries['FIXME_STUB'].wcsupr
    wcsupr.restype = ctypes.POINTER(ctypes.c_int16)
    wcsupr.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wcsupr_l = _libraries['FIXME_STUB'].wcsupr_l
    wcsupr_l.restype = ctypes.POINTER(ctypes.c_int16)
    wcsupr_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wcsupr_s = _libraries['FIXME_STUB'].wcsupr_s
    wcsupr_s.restype = errno_t
    wcsupr_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wcsupr_s_l = _libraries['FIXME_STUB'].wcsupr_s_l
    wcsupr_s_l.restype = errno_t
    wcsupr_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wcsxfrm_l = _libraries['FIXME_STUB'].wcsxfrm_l
    wcsxfrm_l.restype = size_t
    wcsxfrm_l.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t, _locale_t]
    wctime32 = _libraries['FIXME_STUB'].wctime32
    wctime32.restype = ctypes.POINTER(ctypes.c_int16)
    wctime32.argtypes = [ctypes.POINTER(__time32_t)]
    wctime32_s = _libraries['FIXME_STUB'].wctime32_s
    wctime32_s.restype = errno_t
    wctime32_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(__time32_t)]
    wctime64 = _libraries['FIXME_STUB'].wctime64
    wctime64.restype = ctypes.POINTER(ctypes.c_int16)
    wctime64.argtypes = [ctypes.POINTER(__time64_t)]
    wctime64_s = _libraries['FIXME_STUB'].wctime64_s
    wctime64_s.restype = errno_t
    wctime64_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(__time64_t)]
    wctomb_l = _libraries['FIXME_STUB'].wctomb_l
    wctomb_l.restype = ctypes.c_int32
    wctomb_l.argtypes = [ctypes.c_char_p, ctypes.c_int16, _locale_t]
    wctomb_s_l = _libraries['FIXME_STUB'].wctomb_s_l
    wctomb_s_l.restype = errno_t
    wctomb_s_l.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, size_t, ctypes.c_int16, _locale_t]
    wdupenv_s = _libraries['FIXME_STUB'].wdupenv_s
    wdupenv_s.restype = errno_t
    wdupenv_s.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.POINTER(size_t), ctypes.POINTER(ctypes.c_int16)]
    wexecl = _libraries['FIXME_STUB'].wexecl
    wexecl.restype = intptr_t
    wexecl.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wexecle = _libraries['FIXME_STUB'].wexecle
    wexecle.restype = intptr_t
    wexecle.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wexeclp = _libraries['FIXME_STUB'].wexeclp
    wexeclp.restype = intptr_t
    wexeclp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wexeclpe = _libraries['FIXME_STUB'].wexeclpe
    wexeclpe.restype = intptr_t
    wexeclpe.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wexecv = _libraries['FIXME_STUB'].wexecv
    wexecv.restype = intptr_t
    wexecv.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wexecve = _libraries['FIXME_STUB'].wexecve
    wexecve.restype = intptr_t
    wexecve.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wexecvp = _libraries['FIXME_STUB'].wexecvp
    wexecvp.restype = intptr_t
    wexecvp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wexecvpe = _libraries['FIXME_STUB'].wexecvpe
    wexecvpe.restype = intptr_t
    wexecvpe.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wfdopen = _libraries['FIXME_STUB'].wfdopen
    wfdopen.restype = ctypes.POINTER(FILE)
    wfdopen.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16)]
    wfindfirst32 = _libraries['FIXME_STUB'].wfindfirst32
    wfindfirst32.restype = intptr_t
    wfindfirst32.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__wfinddata32_t)]
    wfindfirst32i64 = _libraries['FIXME_STUB'].wfindfirst32i64
    wfindfirst32i64.restype = intptr_t
    wfindfirst32i64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__wfinddata32i64_t)]
    wfindfirst64 = _libraries['FIXME_STUB'].wfindfirst64
    wfindfirst64.restype = intptr_t
    wfindfirst64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__wfinddata64_t)]
    wfindfirst64i32 = _libraries['FIXME_STUB'].wfindfirst64i32
    wfindfirst64i32.restype = intptr_t
    wfindfirst64i32.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__wfinddata64i32_t)]
    wfindnext32 = _libraries['FIXME_STUB'].wfindnext32
    wfindnext32.restype = ctypes.c_int32
    wfindnext32.argtypes = [intptr_t, ctypes.POINTER(struct__wfinddata32_t)]
    wfindnext32i64 = _libraries['FIXME_STUB'].wfindnext32i64
    wfindnext32i64.restype = ctypes.c_int32
    wfindnext32i64.argtypes = [intptr_t, ctypes.POINTER(struct__wfinddata32i64_t)]
    wfindnext64 = _libraries['FIXME_STUB'].wfindnext64
    wfindnext64.restype = ctypes.c_int32
    wfindnext64.argtypes = [intptr_t, ctypes.POINTER(struct__wfinddata64_t)]
    wfindnext64i32 = _libraries['FIXME_STUB'].wfindnext64i32
    wfindnext64i32.restype = ctypes.c_int32
    wfindnext64i32.argtypes = [intptr_t, ctypes.POINTER(struct__wfinddata64i32_t)]
    wfopen = _libraries['FIXME_STUB'].wfopen
    wfopen.restype = ctypes.POINTER(FILE)
    wfopen.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wfopen_s = _libraries['FIXME_STUB'].wfopen_s
    wfopen_s.restype = errno_t
    wfopen_s.argtypes = [ctypes.POINTER(ctypes.POINTER(FILE)), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wfreopen = _libraries['FIXME_STUB'].wfreopen
    wfreopen.restype = ctypes.POINTER(FILE)
    wfreopen.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(FILE)]
    wfreopen_s = _libraries['FIXME_STUB'].wfreopen_s
    wfreopen_s.restype = errno_t
    wfreopen_s.argtypes = [ctypes.POINTER(ctypes.POINTER(FILE)), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(FILE)]
    wfsopen = _libraries['FIXME_STUB'].wfsopen
    wfsopen.restype = ctypes.POINTER(FILE)
    wfsopen.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wfullpath = _libraries['FIXME_STUB'].wfullpath
    wfullpath.restype = ctypes.POINTER(ctypes.c_int16)
    wfullpath.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wgetcwd = _libraries['FIXME_STUB'].wgetcwd
    wgetcwd.restype = ctypes.POINTER(ctypes.c_int16)
    wgetcwd.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wgetdcwd = _libraries['FIXME_STUB'].wgetdcwd
    wgetdcwd.restype = ctypes.POINTER(ctypes.c_int16)
    wgetdcwd.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.c_int32]
    wgetenv = _libraries['FIXME_STUB'].wgetenv
    wgetenv.restype = ctypes.POINTER(ctypes.c_int16)
    wgetenv.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wgetenv_s = _libraries['FIXME_STUB'].wgetenv_s
    wgetenv_s.restype = errno_t
    wgetenv_s.argtypes = [ctypes.POINTER(size_t), ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    wmakepath = _libraries['FIXME_STUB'].wmakepath
    wmakepath.restype = None
    wmakepath.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wmakepath_s = _libraries['FIXME_STUB'].wmakepath_s
    wmakepath_s.restype = errno_t
    wmakepath_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wmkdir = _libraries['FIXME_STUB'].wmkdir
    wmkdir.restype = ctypes.c_int32
    wmkdir.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wmktemp = _libraries['FIXME_STUB'].wmktemp
    wmktemp.restype = ctypes.POINTER(ctypes.c_int16)
    wmktemp.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wmktemp_s = _libraries['FIXME_STUB'].wmktemp_s
    wmktemp_s.restype = errno_t
    wmktemp_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wperror = _libraries['FIXME_STUB'].wperror
    wperror.restype = None
    wperror.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wpopen = _libraries['FIXME_STUB'].wpopen
    wpopen.restype = ctypes.POINTER(FILE)
    wpopen.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wprintf_l = _libraries['FIXME_STUB'].wprintf_l
    wprintf_l.restype = ctypes.c_int32
    wprintf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wprintf_p = _libraries['FIXME_STUB'].wprintf_p
    wprintf_p.restype = ctypes.c_int32
    wprintf_p.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wprintf_p_l = _libraries['FIXME_STUB'].wprintf_p_l
    wprintf_p_l.restype = ctypes.c_int32
    wprintf_p_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wprintf_s_l = _libraries['FIXME_STUB'].wprintf_s_l
    wprintf_s_l.restype = ctypes.c_int32
    wprintf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wputenv = _libraries['FIXME_STUB'].wputenv
    wputenv.restype = ctypes.c_int32
    wputenv.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wputenv_s = _libraries['FIXME_STUB'].wputenv_s
    wputenv_s.restype = errno_t
    wputenv_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wremove = _libraries['FIXME_STUB'].wremove
    wremove.restype = ctypes.c_int32
    wremove.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wrename = _libraries['FIXME_STUB'].wrename
    wrename.restype = ctypes.c_int32
    wrename.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    write = _libraries['FIXME_STUB'].write
    write.restype = ctypes.c_int32
    write.argtypes = [ctypes.c_int32, ctypes.POINTER(None), ctypes.c_uint32]
    wrmdir = _libraries['FIXME_STUB'].wrmdir
    wrmdir.restype = ctypes.c_int32
    wrmdir.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wscanf_l = _libraries['FIXME_STUB'].wscanf_l
    wscanf_l.restype = ctypes.c_int32
    wscanf_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wscanf_s_l = _libraries['FIXME_STUB'].wscanf_s_l
    wscanf_s_l.restype = ctypes.c_int32
    wscanf_s_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wsearchenv = _libraries['FIXME_STUB'].wsearchenv
    wsearchenv.restype = None
    wsearchenv.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wsearchenv_s = _libraries['FIXME_STUB'].wsearchenv_s
    wsearchenv_s.restype = errno_t
    wsearchenv_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wsetlocale = _libraries['FIXME_STUB'].wsetlocale
    wsetlocale.restype = ctypes.POINTER(ctypes.c_int16)
    wsetlocale.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16)]
    wsopen_dispatch = _libraries['FIXME_STUB'].wsopen_dispatch
    wsopen_dispatch.restype = errno_t
    wsopen_dispatch.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32, ctypes.POINTER(ctypes.c_int32), ctypes.c_int32]
    wsopen_s = _libraries['FIXME_STUB'].wsopen_s
    wsopen_s.restype = errno_t
    wsopen_s.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int16), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32]
    wspawnl = _libraries['FIXME_STUB'].wspawnl
    wspawnl.restype = intptr_t
    wspawnl.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wspawnle = _libraries['FIXME_STUB'].wspawnle
    wspawnle.restype = intptr_t
    wspawnle.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wspawnlp = _libraries['FIXME_STUB'].wspawnlp
    wspawnlp.restype = intptr_t
    wspawnlp.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wspawnlpe = _libraries['FIXME_STUB'].wspawnlpe
    wspawnlpe.restype = intptr_t
    wspawnlpe.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wspawnv = _libraries['FIXME_STUB'].wspawnv
    wspawnv.restype = intptr_t
    wspawnv.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wspawnve = _libraries['FIXME_STUB'].wspawnve
    wspawnve.restype = intptr_t
    wspawnve.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wspawnvp = _libraries['FIXME_STUB'].wspawnvp
    wspawnvp.restype = intptr_t
    wspawnvp.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wspawnvpe = _libraries['FIXME_STUB'].wspawnvpe
    wspawnvpe.restype = intptr_t
    wspawnvpe.argtypes = [ctypes.c_int32, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wsplitpath = _libraries['FIXME_STUB'].wsplitpath
    wsplitpath.restype = None
    wsplitpath.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wsplitpath_s = _libraries['FIXME_STUB'].wsplitpath_s
    wsplitpath_s.restype = errno_t
    wsplitpath_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), size_t]
    wstat32 = _libraries['FIXME_STUB'].wstat32
    wstat32.restype = ctypes.c_int32
    wstat32.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__stat32)]
    wstat32i64 = _libraries['FIXME_STUB'].wstat32i64
    wstat32i64.restype = ctypes.c_int32
    wstat32i64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__stat32i64)]
    wstat64 = _libraries['FIXME_STUB'].wstat64
    wstat64.restype = ctypes.c_int32
    wstat64.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__stat64)]
    wstat64i32 = _libraries['FIXME_STUB'].wstat64i32
    wstat64i32.restype = ctypes.c_int32
    wstat64i32.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct__stat64i32)]
    wstrdate = _libraries['FIXME_STUB'].wstrdate
    wstrdate.restype = ctypes.POINTER(ctypes.c_int16)
    wstrdate.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wstrdate_s = _libraries['FIXME_STUB'].wstrdate_s
    wstrdate_s.restype = errno_t
    wstrdate_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wstrtime = _libraries['FIXME_STUB'].wstrtime
    wstrtime.restype = ctypes.POINTER(ctypes.c_int16)
    wstrtime.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wstrtime_s = _libraries['FIXME_STUB'].wstrtime_s
    wstrtime_s.restype = errno_t
    wstrtime_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wsystem = _libraries['FIXME_STUB'].wsystem
    wsystem.restype = ctypes.c_int32
    wsystem.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtempnam = _libraries['FIXME_STUB'].wtempnam
    wtempnam.restype = ctypes.POINTER(ctypes.c_int16)
    wtempnam.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wtmpnam = _libraries['FIXME_STUB'].wtmpnam
    wtmpnam.restype = ctypes.POINTER(ctypes.c_int16)
    wtmpnam.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtmpnam_s = _libraries['FIXME_STUB'].wtmpnam_s
    wtmpnam_s.restype = errno_t
    wtmpnam_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wtof = _libraries['FIXME_STUB'].wtof
    wtof.restype = ctypes.c_double
    wtof.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtof_l = _libraries['FIXME_STUB'].wtof_l
    wtof_l.restype = ctypes.c_double
    wtof_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wtoi = _libraries['FIXME_STUB'].wtoi
    wtoi.restype = ctypes.c_int32
    wtoi.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtoi64 = _libraries['FIXME_STUB'].wtoi64
    wtoi64.restype = ctypes.c_int64
    wtoi64.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtoi64_l = _libraries['FIXME_STUB'].wtoi64_l
    wtoi64_l.restype = ctypes.c_int64
    wtoi64_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wtoi_l = _libraries['FIXME_STUB'].wtoi_l
    wtoi_l.restype = ctypes.c_int32
    wtoi_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wtol = _libraries['FIXME_STUB'].wtol
    wtol.restype = ctypes.c_int32
    wtol.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtol_l = _libraries['FIXME_STUB'].wtol_l
    wtol_l.restype = ctypes.c_int32
    wtol_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wtoll = _libraries['FIXME_STUB'].wtoll
    wtoll.restype = ctypes.c_int64
    wtoll.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wtoll_l = _libraries['FIXME_STUB'].wtoll_l
    wtoll_l.restype = ctypes.c_int64
    wtoll_l.argtypes = [ctypes.POINTER(ctypes.c_int16), _locale_t]
    wunlink = _libraries['FIXME_STUB'].wunlink
    wunlink.restype = ctypes.c_int32
    wunlink.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    y0 = _libraries['FIXME_STUB'].y0
    y0.restype = ctypes.c_double
    y0.argtypes = [ctypes.c_double]
    y1 = _libraries['FIXME_STUB'].y1
    y1.restype = ctypes.c_double
    y1.argtypes = [ctypes.c_double]
    yn = _libraries['FIXME_STUB'].yn
    yn.restype = ctypes.c_double
    yn.argtypes = [ctypes.c_int32, ctypes.c_double]
    abort = _libraries['FIXME_STUB'].abort
    abort.restype = None
    abort.argtypes = []
    abs = _libraries['FIXME_STUB'].abs
    abs.restype = ctypes.c_int32
    abs.argtypes = [ctypes.c_int32]
    acos = _libraries['FIXME_STUB'].acos
    acos.restype = ctypes.c_double
    acos.argtypes = [ctypes.c_double]
    acosf = _libraries['FIXME_STUB'].acosf
    acosf.restype = ctypes.c_float
    acosf.argtypes = [ctypes.c_float]
    acosh = _libraries['FIXME_STUB'].acosh
    acosh.restype = ctypes.c_double
    acosh.argtypes = [ctypes.c_double]
    acoshf = _libraries['FIXME_STUB'].acoshf
    acoshf.restype = ctypes.c_float
    acoshf.argtypes = [ctypes.c_float]
    acoshl = _libraries['FIXME_STUB'].acoshl
    acoshl.restype = ctypes.c_double
    acoshl.argtypes = [ctypes.c_double]
    acosl = _libraries['FIXME_STUB'].acosl
    acosl.restype = ctypes.c_double
    acosl.argtypes = [ctypes.c_double]
    asctime = _libraries['FIXME_STUB'].asctime
    asctime.restype = ctypes.c_char_p
    asctime.argtypes = [ctypes.POINTER(struct_tm)]
    asctime_s = _libraries['FIXME_STUB'].asctime_s
    asctime_s.restype = errno_t
    asctime_s.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(struct_tm)]
    asin = _libraries['FIXME_STUB'].asin
    asin.restype = ctypes.c_double
    asin.argtypes = [ctypes.c_double]
    asinf = _libraries['FIXME_STUB'].asinf
    asinf.restype = ctypes.c_float
    asinf.argtypes = [ctypes.c_float]
    asinh = _libraries['FIXME_STUB'].asinh
    asinh.restype = ctypes.c_double
    asinh.argtypes = [ctypes.c_double]
    asinhf = _libraries['FIXME_STUB'].asinhf
    asinhf.restype = ctypes.c_float
    asinhf.argtypes = [ctypes.c_float]
    asinhl = _libraries['FIXME_STUB'].asinhl
    asinhl.restype = ctypes.c_double
    asinhl.argtypes = [ctypes.c_double]
    asinl = _libraries['FIXME_STUB'].asinl
    asinl.restype = ctypes.c_double
    asinl.argtypes = [ctypes.c_double]
    at_quick_exit = _libraries['FIXME_STUB'].at_quick_exit
    at_quick_exit.restype = ctypes.c_int32
    at_quick_exit.argtypes = [ctypes.CFUNCTYPE(None)]
    atan = _libraries['FIXME_STUB'].atan
    atan.restype = ctypes.c_double
    atan.argtypes = [ctypes.c_double]
    atan2 = _libraries['FIXME_STUB'].atan2
    atan2.restype = ctypes.c_double
    atan2.argtypes = [ctypes.c_double, ctypes.c_double]
    atan2f = _libraries['FIXME_STUB'].atan2f
    atan2f.restype = ctypes.c_float
    atan2f.argtypes = [ctypes.c_float, ctypes.c_float]
    atan2l = _libraries['FIXME_STUB'].atan2l
    atan2l.restype = ctypes.c_double
    atan2l.argtypes = [ctypes.c_double, ctypes.c_double]
    atanf = _libraries['FIXME_STUB'].atanf
    atanf.restype = ctypes.c_float
    atanf.argtypes = [ctypes.c_float]
    atanh = _libraries['FIXME_STUB'].atanh
    atanh.restype = ctypes.c_double
    atanh.argtypes = [ctypes.c_double]
    atanhf = _libraries['FIXME_STUB'].atanhf
    atanhf.restype = ctypes.c_float
    atanhf.argtypes = [ctypes.c_float]
    atanhl = _libraries['FIXME_STUB'].atanhl
    atanhl.restype = ctypes.c_double
    atanhl.argtypes = [ctypes.c_double]
    atanl = _libraries['FIXME_STUB'].atanl
    atanl.restype = ctypes.c_double
    atanl.argtypes = [ctypes.c_double]
    atexit = _libraries['FIXME_STUB'].atexit
    atexit.restype = ctypes.c_int32
    atexit.argtypes = [ctypes.CFUNCTYPE(None)]
    atof = _libraries['FIXME_STUB'].atof
    atof.restype = ctypes.c_double
    atof.argtypes = [ctypes.c_char_p]
    atoi = _libraries['FIXME_STUB'].atoi
    atoi.restype = ctypes.c_int32
    atoi.argtypes = [ctypes.c_char_p]
    atol = _libraries['FIXME_STUB'].atol
    atol.restype = ctypes.c_int32
    atol.argtypes = [ctypes.c_char_p]
    atoll = _libraries['FIXME_STUB'].atoll
    atoll.restype = ctypes.c_int64
    atoll.argtypes = [ctypes.c_char_p]
    bsearch = _libraries['FIXME_STUB'].bsearch
    bsearch.restype = ctypes.POINTER(None)
    bsearch.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t, size_t, _CoreCrtNonSecureSearchSortCompareFunction]
    bsearch_s = _libraries['FIXME_STUB'].bsearch_s
    bsearch_s.restype = ctypes.POINTER(None)
    bsearch_s.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), rsize_t, rsize_t, _CoreCrtSecureSearchSortCompareFunction, ctypes.POINTER(None)]
    btowc = _libraries['FIXME_STUB'].btowc
    btowc.restype = wint_t
    btowc.argtypes = [ctypes.c_int32]
    calloc = _libraries['FIXME_STUB'].calloc
    calloc.restype = ctypes.POINTER(None)
    calloc.argtypes = [size_t, size_t]
    cbrt = _libraries['FIXME_STUB'].cbrt
    cbrt.restype = ctypes.c_double
    cbrt.argtypes = [ctypes.c_double]
    cbrtf = _libraries['FIXME_STUB'].cbrtf
    cbrtf.restype = ctypes.c_float
    cbrtf.argtypes = [ctypes.c_float]
    cbrtl = _libraries['FIXME_STUB'].cbrtl
    cbrtl.restype = ctypes.c_double
    cbrtl.argtypes = [ctypes.c_double]
    ceil = _libraries['FIXME_STUB'].ceil
    ceil.restype = ctypes.c_double
    ceil.argtypes = [ctypes.c_double]
    ceilf = _libraries['FIXME_STUB'].ceilf
    ceilf.restype = ctypes.c_float
    ceilf.argtypes = [ctypes.c_float]
    ceill = _libraries['FIXME_STUB'].ceill
    ceill.restype = ctypes.c_double
    ceill.argtypes = [ctypes.c_double]
    clearerr = _libraries['FIXME_STUB'].clearerr
    clearerr.restype = None
    clearerr.argtypes = [ctypes.POINTER(FILE)]
    clearerr_s = _libraries['FIXME_STUB'].clearerr_s
    clearerr_s.restype = errno_t
    clearerr_s.argtypes = [ctypes.POINTER(FILE)]
    clock = _libraries['FIXME_STUB'].clock
    clock.restype = clock_t
    clock.argtypes = []
    cos = _libraries['FIXME_STUB'].cos
    cos.restype = ctypes.c_double
    cos.argtypes = [ctypes.c_double]
    cosf = _libraries['FIXME_STUB'].cosf
    cosf.restype = ctypes.c_float
    cosf.argtypes = [ctypes.c_float]
    cosh = _libraries['FIXME_STUB'].cosh
    cosh.restype = ctypes.c_double
    cosh.argtypes = [ctypes.c_double]
    coshf = _libraries['FIXME_STUB'].coshf
    coshf.restype = ctypes.c_float
    coshf.argtypes = [ctypes.c_float]
    coshl = _libraries['FIXME_STUB'].coshl
    coshl.restype = ctypes.c_double
    coshl.argtypes = [ctypes.c_double]
    cosl = _libraries['FIXME_STUB'].cosl
    cosl.restype = ctypes.c_double
    cosl.argtypes = [ctypes.c_double]
    div = _libraries['FIXME_STUB'].div
    div.restype = div_t
    div.argtypes = [ctypes.c_int32, ctypes.c_int32]
    erf = _libraries['FIXME_STUB'].erf
    erf.restype = ctypes.c_double
    erf.argtypes = [ctypes.c_double]
    erfc = _libraries['FIXME_STUB'].erfc
    erfc.restype = ctypes.c_double
    erfc.argtypes = [ctypes.c_double]
    erfcf = _libraries['FIXME_STUB'].erfcf
    erfcf.restype = ctypes.c_float
    erfcf.argtypes = [ctypes.c_float]
    erfcl = _libraries['FIXME_STUB'].erfcl
    erfcl.restype = ctypes.c_double
    erfcl.argtypes = [ctypes.c_double]
    erff = _libraries['FIXME_STUB'].erff
    erff.restype = ctypes.c_float
    erff.argtypes = [ctypes.c_float]
    erfl = _libraries['FIXME_STUB'].erfl
    erfl.restype = ctypes.c_double
    erfl.argtypes = [ctypes.c_double]
    exp = _libraries['FIXME_STUB'].exp
    exp.restype = ctypes.c_double
    exp.argtypes = [ctypes.c_double]
    exp2 = _libraries['FIXME_STUB'].exp2
    exp2.restype = ctypes.c_double
    exp2.argtypes = [ctypes.c_double]
    exp2f = _libraries['FIXME_STUB'].exp2f
    exp2f.restype = ctypes.c_float
    exp2f.argtypes = [ctypes.c_float]
    exp2l = _libraries['FIXME_STUB'].exp2l
    exp2l.restype = ctypes.c_double
    exp2l.argtypes = [ctypes.c_double]
    expf = _libraries['FIXME_STUB'].expf
    expf.restype = ctypes.c_float
    expf.argtypes = [ctypes.c_float]
    expl = _libraries['FIXME_STUB'].expl
    expl.restype = ctypes.c_double
    expl.argtypes = [ctypes.c_double]
    expm1 = _libraries['FIXME_STUB'].expm1
    expm1.restype = ctypes.c_double
    expm1.argtypes = [ctypes.c_double]
    expm1f = _libraries['FIXME_STUB'].expm1f
    expm1f.restype = ctypes.c_float
    expm1f.argtypes = [ctypes.c_float]
    expm1l = _libraries['FIXME_STUB'].expm1l
    expm1l.restype = ctypes.c_double
    expm1l.argtypes = [ctypes.c_double]
    fabs = _libraries['FIXME_STUB'].fabs
    fabs.restype = ctypes.c_double
    fabs.argtypes = [ctypes.c_double]
    fabsf = _libraries['FIXME_STUB'].fabsf
    fabsf.restype = ctypes.c_float
    fabsf.argtypes = [ctypes.c_float]
    fabsl = _libraries['FIXME_STUB'].fabsl
    fabsl.restype = ctypes.c_double
    fabsl.argtypes = [ctypes.c_double]
    fclose = _libraries['FIXME_STUB'].fclose
    fclose.restype = ctypes.c_int32
    fclose.argtypes = [ctypes.POINTER(FILE)]
    fdim = _libraries['FIXME_STUB'].fdim
    fdim.restype = ctypes.c_double
    fdim.argtypes = [ctypes.c_double, ctypes.c_double]
    fdimf = _libraries['FIXME_STUB'].fdimf
    fdimf.restype = ctypes.c_float
    fdimf.argtypes = [ctypes.c_float, ctypes.c_float]
    fdiml = _libraries['FIXME_STUB'].fdiml
    fdiml.restype = ctypes.c_double
    fdiml.argtypes = [ctypes.c_double, ctypes.c_double]
    feof = _libraries['FIXME_STUB'].feof
    feof.restype = ctypes.c_int32
    feof.argtypes = [ctypes.POINTER(FILE)]
    ferror = _libraries['FIXME_STUB'].ferror
    ferror.restype = ctypes.c_int32
    ferror.argtypes = [ctypes.POINTER(FILE)]
    fflush = _libraries['FIXME_STUB'].fflush
    fflush.restype = ctypes.c_int32
    fflush.argtypes = [ctypes.POINTER(FILE)]
    fgetc = _libraries['FIXME_STUB'].fgetc
    fgetc.restype = ctypes.c_int32
    fgetc.argtypes = [ctypes.POINTER(FILE)]
    fgetpos = _libraries['FIXME_STUB'].fgetpos
    fgetpos.restype = ctypes.c_int32
    fgetpos.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(fpos_t)]
    fgets = _libraries['FIXME_STUB'].fgets
    fgets.restype = ctypes.c_char_p
    fgets.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.POINTER(FILE)]
    fgetwc = _libraries['FIXME_STUB'].fgetwc
    fgetwc.restype = wint_t
    fgetwc.argtypes = [ctypes.POINTER(FILE)]
    fgetws = _libraries['FIXME_STUB'].fgetws
    fgetws.restype = ctypes.POINTER(ctypes.c_int16)
    fgetws.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int32, ctypes.POINTER(FILE)]
    floor = _libraries['FIXME_STUB'].floor
    floor.restype = ctypes.c_double
    floor.argtypes = [ctypes.c_double]
    floorf = _libraries['FIXME_STUB'].floorf
    floorf.restype = ctypes.c_float
    floorf.argtypes = [ctypes.c_float]
    floorl = _libraries['FIXME_STUB'].floorl
    floorl.restype = ctypes.c_double
    floorl.argtypes = [ctypes.c_double]
    fma = _libraries['FIXME_STUB'].fma
    fma.restype = ctypes.c_double
    fma.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    fmaf = _libraries['FIXME_STUB'].fmaf
    fmaf.restype = ctypes.c_float
    fmaf.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.c_float]
    fmal = _libraries['FIXME_STUB'].fmal
    fmal.restype = ctypes.c_double
    fmal.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    fmax = _libraries['FIXME_STUB'].fmax
    fmax.restype = ctypes.c_double
    fmax.argtypes = [ctypes.c_double, ctypes.c_double]
    fmaxf = _libraries['FIXME_STUB'].fmaxf
    fmaxf.restype = ctypes.c_float
    fmaxf.argtypes = [ctypes.c_float, ctypes.c_float]
    fmaxl = _libraries['FIXME_STUB'].fmaxl
    fmaxl.restype = ctypes.c_double
    fmaxl.argtypes = [ctypes.c_double, ctypes.c_double]
    fmin = _libraries['FIXME_STUB'].fmin
    fmin.restype = ctypes.c_double
    fmin.argtypes = [ctypes.c_double, ctypes.c_double]
    fminf = _libraries['FIXME_STUB'].fminf
    fminf.restype = ctypes.c_float
    fminf.argtypes = [ctypes.c_float, ctypes.c_float]
    fminl = _libraries['FIXME_STUB'].fminl
    fminl.restype = ctypes.c_double
    fminl.argtypes = [ctypes.c_double, ctypes.c_double]
    fmod = _libraries['FIXME_STUB'].fmod
    fmod.restype = ctypes.c_double
    fmod.argtypes = [ctypes.c_double, ctypes.c_double]
    fmodf = _libraries['FIXME_STUB'].fmodf
    fmodf.restype = ctypes.c_float
    fmodf.argtypes = [ctypes.c_float, ctypes.c_float]
    fmodl = _libraries['FIXME_STUB'].fmodl
    fmodl.restype = ctypes.c_double
    fmodl.argtypes = [ctypes.c_double, ctypes.c_double]
    fopen = _libraries['FIXME_STUB'].fopen
    fopen.restype = ctypes.POINTER(FILE)
    fopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    fopen_s = _libraries['FIXME_STUB'].fopen_s
    fopen_s.restype = errno_t
    fopen_s.argtypes = [ctypes.POINTER(ctypes.POINTER(FILE)), ctypes.c_char_p, ctypes.c_char_p]
    fprintf = _libraries['FIXME_STUB'].fprintf
    fprintf.restype = ctypes.c_int32
    fprintf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    fprintf_s = _libraries['FIXME_STUB'].fprintf_s
    fprintf_s.restype = ctypes.c_int32
    fprintf_s.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    fputc = _libraries['FIXME_STUB'].fputc
    fputc.restype = ctypes.c_int32
    fputc.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    fputs = _libraries['FIXME_STUB'].fputs
    fputs.restype = ctypes.c_int32
    fputs.argtypes = [ctypes.c_char_p, ctypes.POINTER(FILE)]
    fputwc = _libraries['FIXME_STUB'].fputwc
    fputwc.restype = wint_t
    fputwc.argtypes = [ctypes.c_int16, ctypes.POINTER(FILE)]
    fputws = _libraries['FIXME_STUB'].fputws
    fputws.restype = ctypes.c_int32
    fputws.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(FILE)]
    fread = _libraries['FIXME_STUB'].fread
    fread.restype = size_t
    fread.argtypes = [ctypes.POINTER(None), size_t, size_t, ctypes.POINTER(FILE)]
    fread_s = _libraries['FIXME_STUB'].fread_s
    fread_s.restype = size_t
    fread_s.argtypes = [ctypes.POINTER(None), size_t, size_t, size_t, ctypes.POINTER(FILE)]
    free = _libraries['FIXME_STUB'].free
    free.restype = None
    free.argtypes = [ctypes.POINTER(None)]
    freopen = _libraries['FIXME_STUB'].freopen
    freopen.restype = ctypes.POINTER(FILE)
    freopen.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(FILE)]
    freopen_s = _libraries['FIXME_STUB'].freopen_s
    freopen_s.restype = errno_t
    freopen_s.argtypes = [ctypes.POINTER(ctypes.POINTER(FILE)), ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(FILE)]
    frexp = _libraries['FIXME_STUB'].frexp
    frexp.restype = ctypes.c_double
    frexp.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_int32)]
    frexpf = _libraries['FIXME_STUB'].frexpf
    frexpf.restype = ctypes.c_float
    frexpf.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_int32)]
    frexpl = _libraries['FIXME_STUB'].frexpl
    frexpl.restype = ctypes.c_double
    frexpl.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_int32)]
    fscanf = _libraries['FIXME_STUB'].fscanf
    fscanf.restype = ctypes.c_int32
    fscanf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    fscanf_s = _libraries['FIXME_STUB'].fscanf_s
    fscanf_s.restype = ctypes.c_int32
    fscanf_s.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    fseek = _libraries['FIXME_STUB'].fseek
    fseek.restype = ctypes.c_int32
    fseek.argtypes = [ctypes.POINTER(FILE), ctypes.c_int32, ctypes.c_int32]
    fsetpos = _libraries['FIXME_STUB'].fsetpos
    fsetpos.restype = ctypes.c_int32
    fsetpos.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(fpos_t)]
    ftell = _libraries['FIXME_STUB'].ftell
    ftell.restype = ctypes.c_int32
    ftell.argtypes = [ctypes.POINTER(FILE)]
    fwide = _libraries['FIXME_STUB'].fwide
    fwide.restype = ctypes.c_int32
    fwide.argtypes = [ctypes.POINTER(FILE), ctypes.c_int32]
    fwprintf = _libraries['FIXME_STUB'].fwprintf
    fwprintf.restype = ctypes.c_int32
    fwprintf.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16)]
    fwprintf_s = _libraries['FIXME_STUB'].fwprintf_s
    fwprintf_s.restype = ctypes.c_int32
    fwprintf_s.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16)]
    fwrite = _libraries['FIXME_STUB'].fwrite
    fwrite.restype = size_t
    fwrite.argtypes = [ctypes.POINTER(None), size_t, size_t, ctypes.POINTER(FILE)]
    fwscanf = _libraries['FIXME_STUB'].fwscanf
    fwscanf.restype = ctypes.c_int32
    fwscanf.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16)]
    fwscanf_s = _libraries['FIXME_STUB'].fwscanf_s
    fwscanf_s.restype = ctypes.c_int32
    fwscanf_s.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16)]
    getc = _libraries['FIXME_STUB'].getc
    getc.restype = ctypes.c_int32
    getc.argtypes = [ctypes.POINTER(FILE)]
    getchar = _libraries['FIXME_STUB'].getchar
    getchar.restype = ctypes.c_int32
    getchar.argtypes = []
    getenv = _libraries['FIXME_STUB'].getenv
    getenv.restype = ctypes.c_char_p
    getenv.argtypes = [ctypes.c_char_p]
    getenv_s = _libraries['FIXME_STUB'].getenv_s
    getenv_s.restype = errno_t
    getenv_s.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, rsize_t, ctypes.c_char_p]
    gets_s = _libraries['FIXME_STUB'].gets_s
    gets_s.restype = ctypes.c_char_p
    gets_s.argtypes = [ctypes.c_char_p, rsize_t]
    getwc = _libraries['FIXME_STUB'].getwc
    getwc.restype = wint_t
    getwc.argtypes = [ctypes.POINTER(FILE)]
    getwchar = _libraries['FIXME_STUB'].getwchar
    getwchar.restype = wint_t
    getwchar.argtypes = []
    ilogb = _libraries['FIXME_STUB'].ilogb
    ilogb.restype = ctypes.c_int32
    ilogb.argtypes = [ctypes.c_double]
    ilogbf = _libraries['FIXME_STUB'].ilogbf
    ilogbf.restype = ctypes.c_int32
    ilogbf.argtypes = [ctypes.c_float]
    ilogbl = _libraries['FIXME_STUB'].ilogbl
    ilogbl.restype = ctypes.c_int32
    ilogbl.argtypes = [ctypes.c_double]
    is_wctype = _libraries['FIXME_STUB'].is_wctype
    is_wctype.restype = ctypes.c_int32
    is_wctype.argtypes = [wint_t, wctype_t]
    isalnum = _libraries['FIXME_STUB'].isalnum
    isalnum.restype = ctypes.c_int32
    isalnum.argtypes = [ctypes.c_int32]
    isalpha = _libraries['FIXME_STUB'].isalpha
    isalpha.restype = ctypes.c_int32
    isalpha.argtypes = [ctypes.c_int32]
    isblank = _libraries['FIXME_STUB'].isblank
    isblank.restype = ctypes.c_int32
    isblank.argtypes = [ctypes.c_int32]
    iscntrl = _libraries['FIXME_STUB'].iscntrl
    iscntrl.restype = ctypes.c_int32
    iscntrl.argtypes = [ctypes.c_int32]
    isdigit = _libraries['FIXME_STUB'].isdigit
    isdigit.restype = ctypes.c_int32
    isdigit.argtypes = [ctypes.c_int32]
    isgraph = _libraries['FIXME_STUB'].isgraph
    isgraph.restype = ctypes.c_int32
    isgraph.argtypes = [ctypes.c_int32]
    isleadbyte = _libraries['FIXME_STUB'].isleadbyte
    isleadbyte.restype = ctypes.c_int32
    isleadbyte.argtypes = [ctypes.c_int32]
    islower = _libraries['FIXME_STUB'].islower
    islower.restype = ctypes.c_int32
    islower.argtypes = [ctypes.c_int32]
    isprint = _libraries['FIXME_STUB'].isprint
    isprint.restype = ctypes.c_int32
    isprint.argtypes = [ctypes.c_int32]
    ispunct = _libraries['FIXME_STUB'].ispunct
    ispunct.restype = ctypes.c_int32
    ispunct.argtypes = [ctypes.c_int32]
    isspace = _libraries['FIXME_STUB'].isspace
    isspace.restype = ctypes.c_int32
    isspace.argtypes = [ctypes.c_int32]
    isupper = _libraries['FIXME_STUB'].isupper
    isupper.restype = ctypes.c_int32
    isupper.argtypes = [ctypes.c_int32]
    iswalnum = _libraries['FIXME_STUB'].iswalnum
    iswalnum.restype = ctypes.c_int32
    iswalnum.argtypes = [wint_t]
    iswalpha = _libraries['FIXME_STUB'].iswalpha
    iswalpha.restype = ctypes.c_int32
    iswalpha.argtypes = [wint_t]
    iswascii = _libraries['FIXME_STUB'].iswascii
    iswascii.restype = ctypes.c_int32
    iswascii.argtypes = [wint_t]
    iswblank = _libraries['FIXME_STUB'].iswblank
    iswblank.restype = ctypes.c_int32
    iswblank.argtypes = [wint_t]
    iswcntrl = _libraries['FIXME_STUB'].iswcntrl
    iswcntrl.restype = ctypes.c_int32
    iswcntrl.argtypes = [wint_t]
    iswctype = _libraries['FIXME_STUB'].iswctype
    iswctype.restype = ctypes.c_int32
    iswctype.argtypes = [wint_t, wctype_t]
    iswdigit = _libraries['FIXME_STUB'].iswdigit
    iswdigit.restype = ctypes.c_int32
    iswdigit.argtypes = [wint_t]
    iswgraph = _libraries['FIXME_STUB'].iswgraph
    iswgraph.restype = ctypes.c_int32
    iswgraph.argtypes = [wint_t]
    iswlower = _libraries['FIXME_STUB'].iswlower
    iswlower.restype = ctypes.c_int32
    iswlower.argtypes = [wint_t]
    iswprint = _libraries['FIXME_STUB'].iswprint
    iswprint.restype = ctypes.c_int32
    iswprint.argtypes = [wint_t]
    iswpunct = _libraries['FIXME_STUB'].iswpunct
    iswpunct.restype = ctypes.c_int32
    iswpunct.argtypes = [wint_t]
    iswspace = _libraries['FIXME_STUB'].iswspace
    iswspace.restype = ctypes.c_int32
    iswspace.argtypes = [wint_t]
    iswupper = _libraries['FIXME_STUB'].iswupper
    iswupper.restype = ctypes.c_int32
    iswupper.argtypes = [wint_t]
    iswxdigit = _libraries['FIXME_STUB'].iswxdigit
    iswxdigit.restype = ctypes.c_int32
    iswxdigit.argtypes = [wint_t]
    isxdigit = _libraries['FIXME_STUB'].isxdigit
    isxdigit.restype = ctypes.c_int32
    isxdigit.argtypes = [ctypes.c_int32]
    labs = _libraries['FIXME_STUB'].labs
    labs.restype = ctypes.c_int32
    labs.argtypes = [ctypes.c_int32]
    ldexpf = _libraries['FIXME_STUB'].ldexpf
    ldexpf.restype = ctypes.c_float
    ldexpf.argtypes = [ctypes.c_float, ctypes.c_int32]
    ldexpl = _libraries['FIXME_STUB'].ldexpl
    ldexpl.restype = ctypes.c_double
    ldexpl.argtypes = [ctypes.c_double, ctypes.c_int32]
    ldiv = _libraries['FIXME_STUB'].ldiv
    ldiv.restype = ldiv_t
    ldiv.argtypes = [ctypes.c_int32, ctypes.c_int32]
    lgamma = _libraries['FIXME_STUB'].lgamma
    lgamma.restype = ctypes.c_double
    lgamma.argtypes = [ctypes.c_double]
    lgammaf = _libraries['FIXME_STUB'].lgammaf
    lgammaf.restype = ctypes.c_float
    lgammaf.argtypes = [ctypes.c_float]
    lgammal = _libraries['FIXME_STUB'].lgammal
    lgammal.restype = ctypes.c_double
    lgammal.argtypes = [ctypes.c_double]
    llabs = _libraries['FIXME_STUB'].llabs
    llabs.restype = ctypes.c_int64
    llabs.argtypes = [ctypes.c_int64]
    lldiv = _libraries['FIXME_STUB'].lldiv
    lldiv.restype = lldiv_t
    lldiv.argtypes = [ctypes.c_int64, ctypes.c_int64]
    llrint = _libraries['FIXME_STUB'].llrint
    llrint.restype = ctypes.c_int64
    llrint.argtypes = [ctypes.c_double]
    llrintf = _libraries['FIXME_STUB'].llrintf
    llrintf.restype = ctypes.c_int64
    llrintf.argtypes = [ctypes.c_float]
    llrintl = _libraries['FIXME_STUB'].llrintl
    llrintl.restype = ctypes.c_int64
    llrintl.argtypes = [ctypes.c_double]
    llround = _libraries['FIXME_STUB'].llround
    llround.restype = ctypes.c_int64
    llround.argtypes = [ctypes.c_double]
    llroundf = _libraries['FIXME_STUB'].llroundf
    llroundf.restype = ctypes.c_int64
    llroundf.argtypes = [ctypes.c_float]
    llroundl = _libraries['FIXME_STUB'].llroundl
    llroundl.restype = ctypes.c_int64
    llroundl.argtypes = [ctypes.c_double]
    log = _libraries['FIXME_STUB'].log
    log.restype = ctypes.c_double
    log.argtypes = [ctypes.c_double]
    log10 = _libraries['FIXME_STUB'].log10
    log10.restype = ctypes.c_double
    log10.argtypes = [ctypes.c_double]
    log10f = _libraries['FIXME_STUB'].log10f
    log10f.restype = ctypes.c_float
    log10f.argtypes = [ctypes.c_float]
    log10l = _libraries['FIXME_STUB'].log10l
    log10l.restype = ctypes.c_double
    log10l.argtypes = [ctypes.c_double]
    log1p = _libraries['FIXME_STUB'].log1p
    log1p.restype = ctypes.c_double
    log1p.argtypes = [ctypes.c_double]
    log1pf = _libraries['FIXME_STUB'].log1pf
    log1pf.restype = ctypes.c_float
    log1pf.argtypes = [ctypes.c_float]
    log1pl = _libraries['FIXME_STUB'].log1pl
    log1pl.restype = ctypes.c_double
    log1pl.argtypes = [ctypes.c_double]
    log2 = _libraries['FIXME_STUB'].log2
    log2.restype = ctypes.c_double
    log2.argtypes = [ctypes.c_double]
    log2f = _libraries['FIXME_STUB'].log2f
    log2f.restype = ctypes.c_float
    log2f.argtypes = [ctypes.c_float]
    log2l = _libraries['FIXME_STUB'].log2l
    log2l.restype = ctypes.c_double
    log2l.argtypes = [ctypes.c_double]
    logbl = _libraries['FIXME_STUB'].logbl
    logbl.restype = ctypes.c_double
    logbl.argtypes = [ctypes.c_double]
    logf = _libraries['FIXME_STUB'].logf
    logf.restype = ctypes.c_float
    logf.argtypes = [ctypes.c_float]
    logl = _libraries['FIXME_STUB'].logl
    logl.restype = ctypes.c_double
    logl.argtypes = [ctypes.c_double]
    lrint = _libraries['FIXME_STUB'].lrint
    lrint.restype = ctypes.c_int32
    lrint.argtypes = [ctypes.c_double]
    lrintf = _libraries['FIXME_STUB'].lrintf
    lrintf.restype = ctypes.c_int32
    lrintf.argtypes = [ctypes.c_float]
    lrintl = _libraries['FIXME_STUB'].lrintl
    lrintl.restype = ctypes.c_int32
    lrintl.argtypes = [ctypes.c_double]
    lround = _libraries['FIXME_STUB'].lround
    lround.restype = ctypes.c_int32
    lround.argtypes = [ctypes.c_double]
    lroundf = _libraries['FIXME_STUB'].lroundf
    lroundf.restype = ctypes.c_int32
    lroundf.argtypes = [ctypes.c_float]
    lroundl = _libraries['FIXME_STUB'].lroundl
    lroundl.restype = ctypes.c_int32
    lroundl.argtypes = [ctypes.c_double]
    malloc = _libraries['FIXME_STUB'].malloc
    malloc.restype = ctypes.POINTER(None)
    malloc.argtypes = [size_t]
    mblen = _libraries['FIXME_STUB'].mblen
    mblen.restype = ctypes.c_int32
    mblen.argtypes = [ctypes.c_char_p, size_t]
    mbrlen = _libraries['FIXME_STUB'].mbrlen
    mbrlen.restype = size_t
    mbrlen.argtypes = [ctypes.c_char_p, size_t, ctypes.POINTER(mbstate_t)]
    mbrtowc = _libraries['FIXME_STUB'].mbrtowc
    mbrtowc.restype = size_t
    mbrtowc.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_char_p, size_t, ctypes.POINTER(mbstate_t)]
    mbsinit = _libraries['FIXME_STUB'].mbsinit
    mbsinit.restype = ctypes.c_int32
    mbsinit.argtypes = [ctypes.POINTER(mbstate_t)]
    mbsrtowcs = _libraries['FIXME_STUB'].mbsrtowcs
    mbsrtowcs.restype = size_t
    mbsrtowcs.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_char_p), size_t, ctypes.POINTER(mbstate_t)]
    mbsrtowcs_s = _libraries['FIXME_STUB'].mbsrtowcs_s
    mbsrtowcs_s.restype = errno_t
    mbsrtowcs_s.argtypes = [ctypes.POINTER(size_t), ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_char_p), size_t, ctypes.POINTER(mbstate_t)]
    mbstowcs = _libraries['FIXME_STUB'].mbstowcs
    mbstowcs.restype = size_t
    mbstowcs.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_char_p, size_t]
    mbstowcs_s = _libraries['FIXME_STUB'].mbstowcs_s
    mbstowcs_s.restype = errno_t
    mbstowcs_s.argtypes = [ctypes.POINTER(size_t), ctypes.POINTER(ctypes.c_int16), size_t, ctypes.c_char_p, size_t]
    mbtowc = _libraries['FIXME_STUB'].mbtowc
    mbtowc.restype = ctypes.c_int32
    mbtowc.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_char_p, size_t]
    memchr = _libraries['FIXME_STUB'].memchr
    memchr.restype = ctypes.POINTER(None)
    memchr.argtypes = [ctypes.POINTER(None), ctypes.c_int32, size_t]
    memcmp = _libraries['FIXME_STUB'].memcmp
    memcmp.restype = ctypes.c_int32
    memcmp.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t]
    memcpy = _libraries['FIXME_STUB'].memcpy
    memcpy.restype = ctypes.POINTER(None)
    memcpy.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t]
    memmove = _libraries['FIXME_STUB'].memmove
    memmove.restype = ctypes.POINTER(None)
    memmove.argtypes = [ctypes.POINTER(None), ctypes.POINTER(None), size_t]
    memset = _libraries['FIXME_STUB'].memset
    memset.restype = ctypes.POINTER(None)
    memset.argtypes = [ctypes.POINTER(None), ctypes.c_int32, size_t]
    modf = _libraries['FIXME_STUB'].modf
    modf.restype = ctypes.c_double
    modf.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
    modff = _libraries['FIXME_STUB'].modff
    modff.restype = ctypes.c_float
    modff.argtypes = [ctypes.c_float, ctypes.POINTER(ctypes.c_float)]
    modfl = _libraries['FIXME_STUB'].modfl
    modfl.restype = ctypes.c_double
    modfl.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double)]
    nan = _libraries['FIXME_STUB'].nan
    nan.restype = ctypes.c_double
    nan.argtypes = [ctypes.c_char_p]
    nanf = _libraries['FIXME_STUB'].nanf
    nanf.restype = ctypes.c_float
    nanf.argtypes = [ctypes.c_char_p]
    nanl = _libraries['FIXME_STUB'].nanl
    nanl.restype = ctypes.c_double
    nanl.argtypes = [ctypes.c_char_p]
    nearbyint = _libraries['FIXME_STUB'].nearbyint
    nearbyint.restype = ctypes.c_double
    nearbyint.argtypes = [ctypes.c_double]
    nearbyintf = _libraries['FIXME_STUB'].nearbyintf
    nearbyintf.restype = ctypes.c_float
    nearbyintf.argtypes = [ctypes.c_float]
    nearbyintl = _libraries['FIXME_STUB'].nearbyintl
    nearbyintl.restype = ctypes.c_double
    nearbyintl.argtypes = [ctypes.c_double]
    nextafterl = _libraries['FIXME_STUB'].nextafterl
    nextafterl.restype = ctypes.c_double
    nextafterl.argtypes = [ctypes.c_double, ctypes.c_double]
    nexttoward = _libraries['FIXME_STUB'].nexttoward
    nexttoward.restype = ctypes.c_double
    nexttoward.argtypes = [ctypes.c_double, ctypes.c_double]
    nexttowardf = _libraries['FIXME_STUB'].nexttowardf
    nexttowardf.restype = ctypes.c_float
    nexttowardf.argtypes = [ctypes.c_float, ctypes.c_double]
    nexttowardl = _libraries['FIXME_STUB'].nexttowardl
    nexttowardl.restype = ctypes.c_double
    nexttowardl.argtypes = [ctypes.c_double, ctypes.c_double]
    open = _libraries['FIXME_STUB'].open
    open.restype = ctypes.c_int32
    open.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    perror = _libraries['FIXME_STUB'].perror
    perror.restype = None
    perror.argtypes = [ctypes.c_char_p]
    pow = _libraries['FIXME_STUB'].pow
    pow.restype = ctypes.c_double
    pow.argtypes = [ctypes.c_double, ctypes.c_double]
    powf = _libraries['FIXME_STUB'].powf
    powf.restype = ctypes.c_float
    powf.argtypes = [ctypes.c_float, ctypes.c_float]
    powl = _libraries['FIXME_STUB'].powl
    powl.restype = ctypes.c_double
    powl.argtypes = [ctypes.c_double, ctypes.c_double]
    printf = _libraries['FIXME_STUB'].printf
    printf.restype = ctypes.c_int32
    printf.argtypes = [ctypes.c_char_p]
    printf_s = _libraries['FIXME_STUB'].printf_s
    printf_s.restype = ctypes.c_int32
    printf_s.argtypes = [ctypes.c_char_p]
    putc = _libraries['FIXME_STUB'].putc
    putc.restype = ctypes.c_int32
    putc.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    putchar = _libraries['FIXME_STUB'].putchar
    putchar.restype = ctypes.c_int32
    putchar.argtypes = [ctypes.c_int32]
    puts = _libraries['FIXME_STUB'].puts
    puts.restype = ctypes.c_int32
    puts.argtypes = [ctypes.c_char_p]
    putwc = _libraries['FIXME_STUB'].putwc
    putwc.restype = wint_t
    putwc.argtypes = [ctypes.c_int16, ctypes.POINTER(FILE)]
    putwchar = _libraries['FIXME_STUB'].putwchar
    putwchar.restype = wint_t
    putwchar.argtypes = [ctypes.c_int16]
    qsort = _libraries['FIXME_STUB'].qsort
    qsort.restype = None
    qsort.argtypes = [ctypes.POINTER(None), size_t, size_t, _CoreCrtNonSecureSearchSortCompareFunction]
    qsort_s = _libraries['FIXME_STUB'].qsort_s
    qsort_s.restype = None
    qsort_s.argtypes = [ctypes.POINTER(None), rsize_t, rsize_t, _CoreCrtSecureSearchSortCompareFunction, ctypes.POINTER(None)]
    quick_exit = _libraries['FIXME_STUB'].quick_exit
    quick_exit.restype = None
    quick_exit.argtypes = [ctypes.c_int32]
    rand = _libraries['FIXME_STUB'].rand
    rand.restype = ctypes.c_int32
    rand.argtypes = []
    realloc = _libraries['FIXME_STUB'].realloc
    realloc.restype = ctypes.POINTER(None)
    realloc.argtypes = [ctypes.POINTER(None), size_t]
    remainder = _libraries['FIXME_STUB'].remainder
    remainder.restype = ctypes.c_double
    remainder.argtypes = [ctypes.c_double, ctypes.c_double]
    remainderf = _libraries['FIXME_STUB'].remainderf
    remainderf.restype = ctypes.c_float
    remainderf.argtypes = [ctypes.c_float, ctypes.c_float]
    remainderl = _libraries['FIXME_STUB'].remainderl
    remainderl.restype = ctypes.c_double
    remainderl.argtypes = [ctypes.c_double, ctypes.c_double]
    remove = _libraries['FIXME_STUB'].remove
    remove.restype = ctypes.c_int32
    remove.argtypes = [ctypes.c_char_p]
    remquo = _libraries['FIXME_STUB'].remquo
    remquo.restype = ctypes.c_double
    remquo.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int32)]
    remquof = _libraries['FIXME_STUB'].remquof
    remquof.restype = ctypes.c_float
    remquof.argtypes = [ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_int32)]
    remquol = _libraries['FIXME_STUB'].remquol
    remquol.restype = ctypes.c_double
    remquol.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.POINTER(ctypes.c_int32)]
    rename = _libraries['FIXME_STUB'].rename
    rename.restype = ctypes.c_int32
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    rewind = _libraries['FIXME_STUB'].rewind
    rewind.restype = None
    rewind.argtypes = [ctypes.POINTER(FILE)]
    rint = _libraries['FIXME_STUB'].rint
    rint.restype = ctypes.c_double
    rint.argtypes = [ctypes.c_double]
    rintf = _libraries['FIXME_STUB'].rintf
    rintf.restype = ctypes.c_float
    rintf.argtypes = [ctypes.c_float]
    rintl = _libraries['FIXME_STUB'].rintl
    rintl.restype = ctypes.c_double
    rintl.argtypes = [ctypes.c_double]
    round = _libraries['FIXME_STUB'].round
    round.restype = ctypes.c_double
    round.argtypes = [ctypes.c_double]
    roundf = _libraries['FIXME_STUB'].roundf
    roundf.restype = ctypes.c_float
    roundf.argtypes = [ctypes.c_float]
    roundl = _libraries['FIXME_STUB'].roundl
    roundl.restype = ctypes.c_double
    roundl.argtypes = [ctypes.c_double]
    scalbln = _libraries['FIXME_STUB'].scalbln
    scalbln.restype = ctypes.c_double
    scalbln.argtypes = [ctypes.c_double, ctypes.c_int32]
    scalblnf = _libraries['FIXME_STUB'].scalblnf
    scalblnf.restype = ctypes.c_float
    scalblnf.argtypes = [ctypes.c_float, ctypes.c_int32]
    scalblnl = _libraries['FIXME_STUB'].scalblnl
    scalblnl.restype = ctypes.c_double
    scalblnl.argtypes = [ctypes.c_double, ctypes.c_int32]
    scalbn = _libraries['FIXME_STUB'].scalbn
    scalbn.restype = ctypes.c_double
    scalbn.argtypes = [ctypes.c_double, ctypes.c_int32]
    scalbnf = _libraries['FIXME_STUB'].scalbnf
    scalbnf.restype = ctypes.c_float
    scalbnf.argtypes = [ctypes.c_float, ctypes.c_int32]
    scalbnl = _libraries['FIXME_STUB'].scalbnl
    scalbnl.restype = ctypes.c_double
    scalbnl.argtypes = [ctypes.c_double, ctypes.c_int32]
    scanf = _libraries['FIXME_STUB'].scanf
    scanf.restype = ctypes.c_int32
    scanf.argtypes = [ctypes.c_char_p]
    scanf_s = _libraries['FIXME_STUB'].scanf_s
    scanf_s.restype = ctypes.c_int32
    scanf_s.argtypes = [ctypes.c_char_p]
    set_terminate = _libraries['FIXME_STUB'].set_terminate
    set_terminate.restype = terminate_handler
    set_terminate.argtypes = [terminate_handler]
    set_unexpected = _libraries['FIXME_STUB'].set_unexpected
    set_unexpected.restype = unexpected_handler
    set_unexpected.argtypes = [unexpected_handler]
    setbuf = _libraries['FIXME_STUB'].setbuf
    setbuf.restype = None
    setbuf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p]
    setvbuf = _libraries['FIXME_STUB'].setvbuf
    setvbuf.restype = ctypes.c_int32
    setvbuf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, ctypes.c_int32, size_t]
    sin = _libraries['FIXME_STUB'].sin
    sin.restype = ctypes.c_double
    sin.argtypes = [ctypes.c_double]
    sinf = _libraries['FIXME_STUB'].sinf
    sinf.restype = ctypes.c_float
    sinf.argtypes = [ctypes.c_float]
    sinh = _libraries['FIXME_STUB'].sinh
    sinh.restype = ctypes.c_double
    sinh.argtypes = [ctypes.c_double]
    sinhf = _libraries['FIXME_STUB'].sinhf
    sinhf.restype = ctypes.c_float
    sinhf.argtypes = [ctypes.c_float]
    sinhl = _libraries['FIXME_STUB'].sinhl
    sinhl.restype = ctypes.c_double
    sinhl.argtypes = [ctypes.c_double]
    sinl = _libraries['FIXME_STUB'].sinl
    sinl.restype = ctypes.c_double
    sinl.argtypes = [ctypes.c_double]
    sopen = _libraries['FIXME_STUB'].sopen
    sopen.restype = ctypes.c_int32
    sopen.argtypes = [ctypes.c_char_p, ctypes.c_int32, ctypes.c_int32]
    sprintf = _libraries['FIXME_STUB'].sprintf
    sprintf.restype = ctypes.c_int32
    sprintf.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    sprintf_s = _libraries['FIXME_STUB'].sprintf_s
    sprintf_s.restype = ctypes.c_int32
    sprintf_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p]
    sqrt = _libraries['FIXME_STUB'].sqrt
    sqrt.restype = ctypes.c_double
    sqrt.argtypes = [ctypes.c_double]
    sqrtf = _libraries['FIXME_STUB'].sqrtf
    sqrtf.restype = ctypes.c_float
    sqrtf.argtypes = [ctypes.c_float]
    sqrtl = _libraries['FIXME_STUB'].sqrtl
    sqrtl.restype = ctypes.c_double
    sqrtl.argtypes = [ctypes.c_double]
    srand = _libraries['FIXME_STUB'].srand
    srand.restype = None
    srand.argtypes = [ctypes.c_uint32]
    sscanf = _libraries['FIXME_STUB'].sscanf
    sscanf.restype = ctypes.c_int32
    sscanf.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    sscanf_s = _libraries['FIXME_STUB'].sscanf_s
    sscanf_s.restype = ctypes.c_int32
    sscanf_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcat = _libraries['FIXME_STUB'].strcat
    strcat.restype = ctypes.c_char_p
    strcat.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcat_s = _libraries['FIXME_STUB'].strcat_s
    strcat_s.restype = errno_t
    strcat_s.argtypes = [ctypes.c_char_p, rsize_t, ctypes.c_char_p]
    strchr = _libraries['FIXME_STUB'].strchr
    strchr.restype = ctypes.c_char_p
    strchr.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    strcmp = _libraries['FIXME_STUB'].strcmp
    strcmp.restype = ctypes.c_int32
    strcmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcoll = _libraries['FIXME_STUB'].strcoll
    strcoll.restype = ctypes.c_int32
    strcoll.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcpy = _libraries['FIXME_STUB'].strcpy
    strcpy.restype = ctypes.c_char_p
    strcpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strcpy_s = _libraries['FIXME_STUB'].strcpy_s
    strcpy_s.restype = errno_t
    strcpy_s.argtypes = [ctypes.c_char_p, rsize_t, ctypes.c_char_p]
    strcspn = _libraries['FIXME_STUB'].strcspn
    strcspn.restype = size_t
    strcspn.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strftime = _libraries['FIXME_STUB'].strftime
    strftime.restype = size_t
    strftime.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, ctypes.POINTER(struct_tm)]
    strlen = _libraries['FIXME_STUB'].strlen
    strlen.restype = size_t
    strlen.argtypes = [ctypes.c_char_p]
    strncat = _libraries['FIXME_STUB'].strncat
    strncat.restype = ctypes.c_char_p
    strncat.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strncat_s = _libraries['FIXME_STUB'].strncat_s
    strncat_s.restype = errno_t
    strncat_s.argtypes = [ctypes.c_char_p, rsize_t, ctypes.c_char_p, rsize_t]
    strncmp = _libraries['FIXME_STUB'].strncmp
    strncmp.restype = ctypes.c_int32
    strncmp.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strncpy = _libraries['FIXME_STUB'].strncpy
    strncpy.restype = ctypes.c_char_p
    strncpy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    strncpy_s = _libraries['FIXME_STUB'].strncpy_s
    strncpy_s.restype = errno_t
    strncpy_s.argtypes = [ctypes.c_char_p, rsize_t, ctypes.c_char_p, rsize_t]
    strnlen = _libraries['FIXME_STUB'].strnlen
    strnlen.restype = size_t
    strnlen.argtypes = [ctypes.c_char_p, size_t]
    strpbrk = _libraries['FIXME_STUB'].strpbrk
    strpbrk.restype = ctypes.c_char_p
    strpbrk.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strrchr = _libraries['FIXME_STUB'].strrchr
    strrchr.restype = ctypes.c_char_p
    strrchr.argtypes = [ctypes.c_char_p, ctypes.c_int32]
    strspn = _libraries['FIXME_STUB'].strspn
    strspn.restype = size_t
    strspn.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strstr = _libraries['FIXME_STUB'].strstr
    strstr.restype = ctypes.c_char_p
    strstr.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strtod = _libraries['FIXME_STUB'].strtod
    strtod.restype = ctypes.c_double
    strtod.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
    strtof = _libraries['FIXME_STUB'].strtof
    strtof.restype = ctypes.c_float
    strtof.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
    strtok = _libraries['FIXME_STUB'].strtok
    strtok.restype = ctypes.c_char_p
    strtok.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    strtok_s = _libraries['FIXME_STUB'].strtok_s
    strtok_s.restype = ctypes.c_char_p
    strtok_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
    strtol = _libraries['FIXME_STUB'].strtol
    strtol.restype = ctypes.c_int32
    strtol.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strtold = _libraries['FIXME_STUB'].strtold
    strtold.restype = ctypes.c_double
    strtold.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p)]
    strtoll = _libraries['FIXME_STUB'].strtoll
    strtoll.restype = ctypes.c_int64
    strtoll.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strtoul = _libraries['FIXME_STUB'].strtoul
    strtoul.restype = ctypes.c_uint32
    strtoul.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strtoull = _libraries['FIXME_STUB'].strtoull
    strtoull.restype = ctypes.c_uint64
    strtoull.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.c_int32]
    strxfrm = _libraries['FIXME_STUB'].strxfrm
    strxfrm.restype = size_t
    strxfrm.argtypes = [ctypes.c_char_p, ctypes.c_char_p, size_t]
    swprintf_s = _libraries['FIXME_STUB'].swprintf_s
    swprintf_s.restype = ctypes.c_int32
    swprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16)]
    swscanf = _libraries['FIXME_STUB'].swscanf
    swscanf.restype = ctypes.c_int32
    swscanf.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    swscanf_s = _libraries['FIXME_STUB'].swscanf_s
    swscanf_s.restype = ctypes.c_int32
    swscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    system = _libraries['FIXME_STUB'].system
    system.restype = ctypes.c_int32
    system.argtypes = [ctypes.c_char_p]
    tan = _libraries['FIXME_STUB'].tan
    tan.restype = ctypes.c_double
    tan.argtypes = [ctypes.c_double]
    tanf = _libraries['FIXME_STUB'].tanf
    tanf.restype = ctypes.c_float
    tanf.argtypes = [ctypes.c_float]
    tanh = _libraries['FIXME_STUB'].tanh
    tanh.restype = ctypes.c_double
    tanh.argtypes = [ctypes.c_double]
    tanhf = _libraries['FIXME_STUB'].tanhf
    tanhf.restype = ctypes.c_float
    tanhf.argtypes = [ctypes.c_float]
    tanhl = _libraries['FIXME_STUB'].tanhl
    tanhl.restype = ctypes.c_double
    tanhl.argtypes = [ctypes.c_double]
    tanl = _libraries['FIXME_STUB'].tanl
    tanl.restype = ctypes.c_double
    tanl.argtypes = [ctypes.c_double]
    terminate = _libraries['FIXME_STUB'].terminate
    terminate.restype = None
    terminate.argtypes = []
    tgamma = _libraries['FIXME_STUB'].tgamma
    tgamma.restype = ctypes.c_double
    tgamma.argtypes = [ctypes.c_double]
    tgammaf = _libraries['FIXME_STUB'].tgammaf
    tgammaf.restype = ctypes.c_float
    tgammaf.argtypes = [ctypes.c_float]
    tgammal = _libraries['FIXME_STUB'].tgammal
    tgammal.restype = ctypes.c_double
    tgammal.argtypes = [ctypes.c_double]
    tmpfile = _libraries['FIXME_STUB'].tmpfile
    tmpfile.restype = ctypes.POINTER(FILE)
    tmpfile.argtypes = []
    tmpfile_s = _libraries['FIXME_STUB'].tmpfile_s
    tmpfile_s.restype = errno_t
    tmpfile_s.argtypes = [ctypes.POINTER(ctypes.POINTER(FILE))]
    tmpnam = _libraries['FIXME_STUB'].tmpnam
    tmpnam.restype = ctypes.c_char_p
    tmpnam.argtypes = [ctypes.c_char_p]
    tmpnam_s = _libraries['FIXME_STUB'].tmpnam_s
    tmpnam_s.restype = errno_t
    tmpnam_s.argtypes = [ctypes.c_char_p, rsize_t]
    towlower = _libraries['FIXME_STUB'].towlower
    towlower.restype = wint_t
    towlower.argtypes = [wint_t]
    towupper = _libraries['FIXME_STUB'].towupper
    towupper.restype = wint_t
    towupper.argtypes = [wint_t]
    trunc = _libraries['FIXME_STUB'].trunc
    trunc.restype = ctypes.c_double
    trunc.argtypes = [ctypes.c_double]
    truncf = _libraries['FIXME_STUB'].truncf
    truncf.restype = ctypes.c_float
    truncf.argtypes = [ctypes.c_float]
    truncl = _libraries['FIXME_STUB'].truncl
    truncl.restype = ctypes.c_double
    truncl.argtypes = [ctypes.c_double]
    unexpected = _libraries['FIXME_STUB'].unexpected
    unexpected.restype = None
    unexpected.argtypes = []
    ungetc = _libraries['FIXME_STUB'].ungetc
    ungetc.restype = ctypes.c_int32
    ungetc.argtypes = [ctypes.c_int32, ctypes.POINTER(FILE)]
    ungetwc = _libraries['FIXME_STUB'].ungetwc
    ungetwc.restype = wint_t
    ungetwc.argtypes = [wint_t, ctypes.POINTER(FILE)]
    vfprintf = _libraries['FIXME_STUB'].vfprintf
    vfprintf.restype = ctypes.c_int32
    vfprintf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    vfprintf_s = _libraries['FIXME_STUB'].vfprintf_s
    vfprintf_s.restype = ctypes.c_int32
    vfprintf_s.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    vfscanf = _libraries['FIXME_STUB'].vfscanf
    vfscanf.restype = ctypes.c_int32
    vfscanf.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    vfscanf_s = _libraries['FIXME_STUB'].vfscanf_s
    vfscanf_s.restype = ctypes.c_int32
    vfscanf_s.argtypes = [ctypes.POINTER(FILE), ctypes.c_char_p, va_list]
    vfwprintf = _libraries['FIXME_STUB'].vfwprintf
    vfwprintf.restype = ctypes.c_int32
    vfwprintf.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), va_list]
    vfwprintf_s = _libraries['FIXME_STUB'].vfwprintf_s
    vfwprintf_s.restype = ctypes.c_int32
    vfwprintf_s.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), va_list]
    vfwscanf = _libraries['FIXME_STUB'].vfwscanf
    vfwscanf.restype = ctypes.c_int32
    vfwscanf.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), va_list]
    vfwscanf_s = _libraries['FIXME_STUB'].vfwscanf_s
    vfwscanf_s.restype = ctypes.c_int32
    vfwscanf_s.argtypes = [ctypes.POINTER(FILE), ctypes.POINTER(ctypes.c_int16), va_list]
    vprintf = _libraries['FIXME_STUB'].vprintf
    vprintf.restype = ctypes.c_int32
    vprintf.argtypes = [ctypes.c_char_p, va_list]
    vprintf_s = _libraries['FIXME_STUB'].vprintf_s
    vprintf_s.restype = ctypes.c_int32
    vprintf_s.argtypes = [ctypes.c_char_p, va_list]
    vscanf = _libraries['FIXME_STUB'].vscanf
    vscanf.restype = ctypes.c_int32
    vscanf.argtypes = [ctypes.c_char_p, va_list]
    vscanf_s = _libraries['FIXME_STUB'].vscanf_s
    vscanf_s.restype = ctypes.c_int32
    vscanf_s.argtypes = [ctypes.c_char_p, va_list]
    vsprintf = _libraries['FIXME_STUB'].vsprintf
    vsprintf.restype = ctypes.c_int32
    vsprintf.argtypes = [ctypes.c_char_p, ctypes.c_char_p, va_list]
    vsprintf_s = _libraries['FIXME_STUB'].vsprintf_s
    vsprintf_s.restype = ctypes.c_int32
    vsprintf_s.argtypes = [ctypes.c_char_p, size_t, ctypes.c_char_p, va_list]
    vsscanf = _libraries['FIXME_STUB'].vsscanf
    vsscanf.restype = ctypes.c_int32
    vsscanf.argtypes = [ctypes.c_char_p, ctypes.c_char_p, va_list]
    vsscanf_s = _libraries['FIXME_STUB'].vsscanf_s
    vsscanf_s.restype = ctypes.c_int32
    vsscanf_s.argtypes = [ctypes.c_char_p, ctypes.c_char_p, va_list]
    vswprintf_s = _libraries['FIXME_STUB'].vswprintf_s
    vswprintf_s.restype = ctypes.c_int32
    vswprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), va_list]
    vswscanf = _libraries['FIXME_STUB'].vswscanf
    vswscanf.restype = ctypes.c_int32
    vswscanf.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), va_list]
    vswscanf_s = _libraries['FIXME_STUB'].vswscanf_s
    vswscanf_s.restype = ctypes.c_int32
    vswscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), va_list]
    vwprintf = _libraries['FIXME_STUB'].vwprintf
    vwprintf.restype = ctypes.c_int32
    vwprintf.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vwprintf_s = _libraries['FIXME_STUB'].vwprintf_s
    vwprintf_s.restype = ctypes.c_int32
    vwprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vwscanf = _libraries['FIXME_STUB'].vwscanf
    vwscanf.restype = ctypes.c_int32
    vwscanf.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    vwscanf_s = _libraries['FIXME_STUB'].vwscanf_s
    vwscanf_s.restype = ctypes.c_int32
    vwscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16), va_list]
    wcrtomb = _libraries['FIXME_STUB'].wcrtomb
    wcrtomb.restype = size_t
    wcrtomb.argtypes = [ctypes.c_char_p, ctypes.c_int16, ctypes.POINTER(mbstate_t)]
    wcrtomb_s = _libraries['FIXME_STUB'].wcrtomb_s
    wcrtomb_s.restype = errno_t
    wcrtomb_s.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, size_t, ctypes.c_int16, ctypes.POINTER(mbstate_t)]
    wcscat = _libraries['FIXME_STUB'].wcscat
    wcscat.restype = ctypes.POINTER(ctypes.c_int16)
    wcscat.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcscat_s = _libraries['FIXME_STUB'].wcscat_s
    wcscat_s.restype = errno_t
    wcscat_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16)]
    wcschr = _libraries['FIXME_STUB'].wcschr
    wcschr.restype = ctypes.POINTER(ctypes.c_int16)
    wcschr.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    wcscmp = _libraries['FIXME_STUB'].wcscmp
    wcscmp.restype = ctypes.c_int32
    wcscmp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcscoll = _libraries['FIXME_STUB'].wcscoll
    wcscoll.restype = ctypes.c_int32
    wcscoll.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcscpy = _libraries['FIXME_STUB'].wcscpy
    wcscpy.restype = ctypes.POINTER(ctypes.c_int16)
    wcscpy.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcscpy_s = _libraries['FIXME_STUB'].wcscpy_s
    wcscpy_s.restype = errno_t
    wcscpy_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16)]
    wcscspn = _libraries['FIXME_STUB'].wcscspn
    wcscspn.restype = size_t
    wcscspn.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcsftime = _libraries['FIXME_STUB'].wcsftime
    wcsftime.restype = size_t
    wcsftime.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t, ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(struct_tm)]
    wcslen = _libraries['FIXME_STUB'].wcslen
    wcslen.restype = size_t
    wcslen.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wcsncat = _libraries['FIXME_STUB'].wcsncat
    wcsncat.restype = ctypes.POINTER(ctypes.c_int16)
    wcsncat.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsncat_s = _libraries['FIXME_STUB'].wcsncat_s
    wcsncat_s.restype = errno_t
    wcsncat_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16), rsize_t]
    wcsncmp = _libraries['FIXME_STUB'].wcsncmp
    wcsncmp.restype = ctypes.c_int32
    wcsncmp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsncpy = _libraries['FIXME_STUB'].wcsncpy
    wcsncpy.restype = ctypes.POINTER(ctypes.c_int16)
    wcsncpy.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wcsncpy_s = _libraries['FIXME_STUB'].wcsncpy_s
    wcsncpy_s.restype = errno_t
    wcsncpy_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16), rsize_t]
    wcsnlen = _libraries['FIXME_STUB'].wcsnlen
    wcsnlen.restype = size_t
    wcsnlen.argtypes = [ctypes.POINTER(ctypes.c_int16), size_t]
    wcspbrk = _libraries['FIXME_STUB'].wcspbrk
    wcspbrk.restype = ctypes.POINTER(ctypes.c_int16)
    wcspbrk.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcsrchr = _libraries['FIXME_STUB'].wcsrchr
    wcsrchr.restype = ctypes.POINTER(ctypes.c_int16)
    wcsrchr.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16]
    wcsrtombs = _libraries['FIXME_STUB'].wcsrtombs
    wcsrtombs.restype = size_t
    wcsrtombs.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), size_t, ctypes.POINTER(mbstate_t)]
    wcsrtombs_s = _libraries['FIXME_STUB'].wcsrtombs_s
    wcsrtombs_s.restype = errno_t
    wcsrtombs_s.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, size_t, ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), size_t, ctypes.POINTER(mbstate_t)]
    wcsspn = _libraries['FIXME_STUB'].wcsspn
    wcsspn.restype = size_t
    wcsspn.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcsstr = _libraries['FIXME_STUB'].wcsstr
    wcsstr.restype = ctypes.POINTER(ctypes.c_int16)
    wcsstr.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16)]
    wcstod = _libraries['FIXME_STUB'].wcstod
    wcstod.restype = ctypes.c_double
    wcstod.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wcstof = _libraries['FIXME_STUB'].wcstof
    wcstof.restype = ctypes.c_float
    wcstof.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wcstok = _libraries['FIXME_STUB'].wcstok
    wcstok.restype = ctypes.POINTER(ctypes.c_int16)
    wcstok.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wcstok_s = _libraries['FIXME_STUB'].wcstok_s
    wcstok_s.restype = ctypes.POINTER(ctypes.c_int16)
    wcstok_s.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wcstol = _libraries['FIXME_STUB'].wcstol
    wcstol.restype = ctypes.c_int32
    wcstol.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcstold = _libraries['FIXME_STUB'].wcstold
    wcstold.restype = ctypes.c_double
    wcstold.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16))]
    wcstoll = _libraries['FIXME_STUB'].wcstoll
    wcstoll.restype = ctypes.c_int64
    wcstoll.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcstombs = _libraries['FIXME_STUB'].wcstombs
    wcstombs.restype = size_t
    wcstombs.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int16), size_t]
    wcstombs_s = _libraries['FIXME_STUB'].wcstombs_s
    wcstombs_s.restype = errno_t
    wcstombs_s.argtypes = [ctypes.POINTER(size_t), ctypes.c_char_p, size_t, ctypes.POINTER(ctypes.c_int16), size_t]
    wcstoul = _libraries['FIXME_STUB'].wcstoul
    wcstoul.restype = ctypes.c_uint32
    wcstoul.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcstoull = _libraries['FIXME_STUB'].wcstoull
    wcstoull.restype = ctypes.c_uint64
    wcstoull.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.POINTER(ctypes.c_int16)), ctypes.c_int32]
    wcsxfrm = _libraries['FIXME_STUB'].wcsxfrm
    wcsxfrm.restype = size_t
    wcsxfrm.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wctob = _libraries['FIXME_STUB'].wctob
    wctob.restype = ctypes.c_int32
    wctob.argtypes = [wint_t]
    wctomb = _libraries['FIXME_STUB'].wctomb
    wctomb.restype = ctypes.c_int32
    wctomb.argtypes = [ctypes.c_char_p, ctypes.c_int16]
    wctomb_s = _libraries['FIXME_STUB'].wctomb_s
    wctomb_s.restype = errno_t
    wctomb_s.argtypes = [ctypes.POINTER(ctypes.c_int32), ctypes.c_char_p, rsize_t, ctypes.c_int16]
    wmemchr = _libraries['FIXME_STUB'].wmemchr
    wmemchr.restype = ctypes.POINTER(ctypes.c_int16)
    wmemchr.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16, size_t]
    wmemcmp = _libraries['FIXME_STUB'].wmemcmp
    wmemcmp.restype = ctypes.c_int32
    wmemcmp.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wmemcpy = _libraries['FIXME_STUB'].wmemcpy
    wmemcpy.restype = ctypes.POINTER(ctypes.c_int16)
    wmemcpy.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wmemcpy_s = _libraries['FIXME_STUB'].wmemcpy_s
    wmemcpy_s.restype = errno_t
    wmemcpy_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16), rsize_t]
    wmemmove = _libraries['FIXME_STUB'].wmemmove
    wmemmove.restype = ctypes.POINTER(ctypes.c_int16)
    wmemmove.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.POINTER(ctypes.c_int16), size_t]
    wmemmove_s = _libraries['FIXME_STUB'].wmemmove_s
    wmemmove_s.restype = errno_t
    wmemmove_s.argtypes = [ctypes.POINTER(ctypes.c_int16), rsize_t, ctypes.POINTER(ctypes.c_int16), rsize_t]
    wmemset = _libraries['FIXME_STUB'].wmemset
    wmemset.restype = ctypes.POINTER(ctypes.c_int16)
    wmemset.argtypes = [ctypes.POINTER(ctypes.c_int16), ctypes.c_int16, size_t]
    wprintf = _libraries['FIXME_STUB'].wprintf
    wprintf.restype = ctypes.c_int32
    wprintf.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wprintf_s = _libraries['FIXME_STUB'].wprintf_s
    wprintf_s.restype = ctypes.c_int32
    wprintf_s.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wscanf = _libraries['FIXME_STUB'].wscanf
    wscanf.restype = ctypes.c_int32
    wscanf.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    wscanf_s = _libraries['FIXME_STUB'].wscanf_s
    wscanf_s.restype = ctypes.c_int32
    wscanf_s.argtypes = [ctypes.POINTER(ctypes.c_int16)]
    __all__ = \
        ['BitScanForward', 'BitScanForward64', 'BitScanReverse',
        'BitScanReverse64', 'Denorm_C', 'Eps_C', 'Exit', 'FDenorm_C',
        'FEps_C', 'FILE', 'FInf_C', 'FNan_C', 'FRteps_C', 'FSnan_C',
        'FXbig_C', 'FZero_C', 'Hugeval_C', 'ISA_AVAILABILITY', 'Inf_C',
        'InterlockedAnd', 'InterlockedAnd16', 'InterlockedAnd64',
        'InterlockedAnd8', 'InterlockedCompareExchange',
        'InterlockedCompareExchange128', 'InterlockedCompareExchange16',
        'InterlockedCompareExchange64', 'InterlockedCompareExchange8',
        'InterlockedDecrement', 'InterlockedDecrement16',
        'InterlockedDecrement64', 'InterlockedExchange',
        'InterlockedExchange16', 'InterlockedExchange64',
        'InterlockedExchange8', 'InterlockedExchangeAdd',
        'InterlockedExchangeAdd16', 'InterlockedExchangeAdd64',
        'InterlockedExchangeAdd8', 'InterlockedIncrement',
        'InterlockedIncrement16', 'InterlockedIncrement64',
        'InterlockedOr', 'InterlockedOr16', 'InterlockedOr64',
        'InterlockedOr8', 'InterlockedXor', 'InterlockedXor16',
        'InterlockedXor64', 'InterlockedXor8', 'LDenorm_C', 'LEps_C',
        'LInf_C', 'LNan_C', 'LRteps_C', 'LSnan_C', 'LXbig_C', 'LZero_C',
        'MallocaComputeSize', 'MarkAllocaS', 'Nan_C', 'ReadWriteBarrier',
        'Rteps_C', 'Snan_C', 'Xbig_C', 'Zero_C', '_CRT_ALLOC_HOOK',
        '_CRT_DUMP_CLIENT', '_CRT_REPORT_HOOK', '_CRT_REPORT_HOOKW',
        '_CoreCrtNonSecureSearchSortCompareFunction',
        '_CoreCrtSecureSearchSortCompareFunction', '_Functor',
        '_HEAPINFO', '_HFILE', '_Left', '_Noinit', '_Pmd_object',
        '_Pmd_pointer', '_Pmd_refwrap', '_Pmf_object', '_Pmf_pointer',
        '_Pmf_refwrap', '_Right', '_Unused', '_Wint_t',
        '__ISA_AVAILABLE_ARMNT', '__ISA_AVAILABLE_AVX',
        '__ISA_AVAILABLE_AVX2', '__ISA_AVAILABLE_AVX512',
        '__ISA_AVAILABLE_ENFSTRG', '__ISA_AVAILABLE_NEON',
        '__ISA_AVAILABLE_NEON_ARM64', '__ISA_AVAILABLE_SSE2',
        '__ISA_AVAILABLE_SSE42', '__ISA_AVAILABLE_X86', '__crt_bool',
        '__mb_cur_max_func', '__mb_cur_max_l_func', '__time32_t',
        '__time64_t', '__vcrt_bool', '_acrt_get_locale_data_prefix',
        '_acrt_iob_func', '_acrt_locale_get_ctype_array_value',
        '_ascii_iswalpha', '_ascii_iswdigit', '_ascii_tolower',
        '_ascii_toupper', '_ascii_towlower', '_ascii_towupper',
        '_builtin_assume_aligned', '_ceil', '_ceilf',
        '_conio_common_vcwprintf', '_conio_common_vcwprintf_p',
        '_conio_common_vcwprintf_s', '_conio_common_vcwscanf',
        '_copysign', '_copysignf', '_daylight', '_dev_t', '_doserrno',
        '_dstbias', '_floor', '_floorf', '_fpe_flt_rounds', '_fpecode',
        '_fsize_t', '_ino_t', '_invalid_parameter_handler',
        '_isa_available', '_isascii', '_iscsym', '_iscsymf',
        '_iso_volatile_load16', '_iso_volatile_load32',
        '_iso_volatile_load64', '_iso_volatile_load8',
        '_iso_volatile_store16', '_iso_volatile_store32',
        '_iso_volatile_store64', '_iso_volatile_store8', '_iswcsym',
        '_iswcsymf', '_local_stdio_printf_options',
        '_local_stdio_scanf_options', '_locale_t', '_lzcnt', '_lzcnt16',
        '_lzcnt64', '_off_t', '_onexit_t', '_p___argc', '_p___argv',
        '_p___wargv', '_p__commode', '_p__environ', '_p__fmode',
        '_p__pgmptr', '_p__wenviron', '_p__wpgmptr', '_pctype_func',
        '_popcnt', '_popcnt16', '_popcnt64', '_purecall_handler',
        '_pwctype_func', '_report_gsfailure', '_round', '_roundf',
        '_se_translator_function', '_security_check_cookie',
        '_security_cookie', '_security_init_cookie', '_shiftright128',
        '_signbitvalue', '_signbitvaluef', '_std_exception_copy',
        '_std_exception_destroy',
        '_std_reverse_copy_trivially_copyable_1',
        '_std_reverse_copy_trivially_copyable_2',
        '_std_reverse_copy_trivially_copyable_4',
        '_std_reverse_copy_trivially_copyable_8',
        '_std_reverse_trivially_swappable_1',
        '_std_reverse_trivially_swappable_2',
        '_std_reverse_trivially_swappable_4',
        '_std_reverse_trivially_swappable_8',
        '_std_swap_ranges_trivially_swappable_noalias',
        '_stdio_common_vfprintf', '_stdio_common_vfprintf_p',
        '_stdio_common_vfprintf_s', '_stdio_common_vfscanf',
        '_stdio_common_vfwprintf', '_stdio_common_vfwprintf_p',
        '_stdio_common_vfwprintf_s', '_stdio_common_vfwscanf',
        '_stdio_common_vsnprintf_s', '_stdio_common_vsnwprintf_s',
        '_stdio_common_vsprintf', '_stdio_common_vsprintf_p',
        '_stdio_common_vsprintf_s', '_stdio_common_vsscanf',
        '_stdio_common_vswprintf', '_stdio_common_vswprintf_p',
        '_stdio_common_vswprintf_s', '_stdio_common_vswscanf', '_strncnt',
        '_swprintf_l', '_sys_errlist', '_sys_nerr', '_threadhandle',
        '_threadid', '_timezone', '_toascii', '_trunc', '_truncf',
        '_tzname', '_uncaught_exception', '_uncaught_exceptions',
        '_va_start', '_vswprintf_l', '_wcserror', '_wcserror_s', 'abort',
        'abs', 'abs64', 'access', 'access_s', 'acos', 'acosf', 'acosh',
        'acoshf', 'acoshl', 'acosl', 'aligned_free', 'aligned_malloc',
        'aligned_msize', 'aligned_offset_malloc',
        'aligned_offset_realloc', 'aligned_offset_recalloc',
        'aligned_realloc', 'aligned_recalloc', 'alloca', 'asctime',
        'asctime_s', 'asin', 'asinf', 'asinh', 'asinhf', 'asinhl',
        'asinl', 'at_quick_exit', 'atan', 'atan2', 'atan2f', 'atan2l',
        'atanf', 'atanh', 'atanhf', 'atanhl', 'atanl', 'atexit', 'atodbl',
        'atodbl_l', 'atof', 'atof_l', 'atoflt', 'atoflt_l', 'atoi',
        'atoi64', 'atoi64_l', 'atoi_l', 'atol', 'atol_l', 'atoldbl',
        'atoldbl_l', 'atoll', 'atoll_l', 'beep', 'bittest', 'bsearch',
        'bsearch_s', 'btowc', 'byteswap_uint64', 'byteswap_ulong',
        'byteswap_ushort', 'cabs', 'callnewh', 'calloc', 'calloc_base',
        'cbrt', 'cbrtf', 'cbrtl', 'ceil', 'ceilf', 'ceill', 'cgetws_s',
        'chdir', 'chdrive', 'chgsign', 'chgsignf', 'chgsignl', 'chmod',
        'chsize', 'chsize_s', 'chvalidchk_l', 'clearerr', 'clearerr_s',
        'clearfp', 'clock', 'clock_t', 'close', 'commit', 'control87',
        'controlfp', 'controlfp_s', 'copysign', 'copysignf', 'copysignl',
        'cos', 'cosf', 'cosh', 'coshf', 'coshl', 'cosl', 'cputws',
        'creat', 'ctime32', 'ctime32_s', 'ctime64', 'ctime64_s',
        'cvt_dtoi_sat', 'cvt_dtoi_sent', 'cvt_dtoll_sat',
        'cvt_dtoll_sent', 'cvt_dtoui_sat', 'cvt_dtoui_sent',
        'cvt_dtoull_sat', 'cvt_dtoull_sent', 'cvt_ftoi_sat',
        'cvt_ftoi_sent', 'cvt_ftoll_sat', 'cvt_ftoll_sent',
        'cvt_ftoui_sat', 'cvt_ftoui_sent', 'cvt_ftoull_sat',
        'cvt_ftoull_sent', 'cwprintf', 'cwprintf_l', 'cwprintf_p',
        'cwprintf_p_l', 'cwprintf_s', 'cwprintf_s_l', 'cwscanf',
        'cwscanf_l', 'cwscanf_s', 'cwscanf_s_l', 'd_int', 'dclass',
        'denorm_absent', 'denorm_indeterminate', 'denorm_present',
        'dev_t', 'dexp', 'difftime32', 'difftime64', 'div', 'div_t',
        'dlog', 'dnorm', 'double_t', 'dpcomp', 'dpoly', 'dscale', 'dsign',
        'dsin', 'dtest', 'dunscale', 'dup', 'dup2', 'dupenv_s', 'ecvt',
        'ecvt_s', 'eof', 'erf', 'erfc', 'erfcf', 'erfcl', 'erff', 'erfl',
        'errno', 'errno_t', 'exit', 'exp', 'exp2', 'exp2f', 'exp2l',
        'expand', 'expf', 'expl', 'expm1', 'expm1f', 'expm1l', 'fabs',
        'fabsf', 'fabsl', 'fclose', 'fclose_nolock', 'fcloseall', 'fcvt',
        'fcvt_s', 'fd_int', 'fdclass', 'fdexp', 'fdim', 'fdimf', 'fdiml',
        'fdlog', 'fdnorm', 'fdopen', 'fdpcomp', 'fdpoly', 'fdscale',
        'fdsign', 'fdsin', 'fdtest', 'fdunscale', 'feof', 'ferror',
        'fflush', 'fflush_nolock', 'fgetc', 'fgetc_nolock', 'fgetchar',
        'fgetpos', 'fgets', 'fgetwc', 'fgetwc_nolock', 'fgetwchar',
        'fgetws', 'filelength', 'filelengthi64', 'fileno', 'findclose',
        'findfirst32', 'findfirst32i64', 'findfirst64', 'findfirst64i32',
        'findnext32', 'findnext32i64', 'findnext64', 'findnext64i32',
        'finite', 'finitef', 'float_t', 'floor', 'floorf', 'floorl',
        'flushall', 'fma', 'fmaf', 'fmal', 'fmax', 'fmaxf', 'fmaxl',
        'fmin', 'fminf', 'fminl', 'fmod', 'fmodf', 'fmodl', 'fopen',
        'fopen_s', 'fpclass', 'fpclassf', 'fperrraise', 'fpos_t',
        'fpreset', 'fprintf', 'fprintf_l', 'fprintf_p', 'fprintf_p_l',
        'fprintf_s', 'fprintf_s_l', 'fputc', 'fputc_nolock', 'fputchar',
        'fputs', 'fputwc', 'fputwc_nolock', 'fputwchar', 'fputws',
        'fread', 'fread_nolock', 'fread_nolock_s', 'fread_s', 'free',
        'free_base', 'freea', 'freopen', 'freopen_s', 'frexp', 'frexpf',
        'frexpl', 'fscanf', 'fscanf_l', 'fscanf_s', 'fscanf_s_l', 'fseek',
        'fseek_nolock', 'fseeki64', 'fseeki64_nolock', 'fsetpos',
        'fsopen', 'fstat32', 'fstat32i64', 'fstat64', 'fstat64i32',
        'ftell', 'ftell_nolock', 'ftelli64', 'ftelli64_nolock',
        'fullpath', 'fwide', 'fwprintf', 'fwprintf_l', 'fwprintf_p',
        'fwprintf_p_l', 'fwprintf_s', 'fwprintf_s_l', 'fwrite',
        'fwrite_nolock', 'fwscanf', 'fwscanf_l', 'fwscanf_s',
        'fwscanf_s_l', 'gcvt', 'gcvt_s', 'get_FMA3_enable',
        'get_daylight', 'get_doserrno', 'get_dstbias', 'get_errno',
        'get_fmode', 'get_heap_handle', 'get_invalid_parameter_handler',
        'get_osfhandle', 'get_pgmptr', 'get_printf_count_output',
        'get_purecall_handler', 'get_stream_buffer_pointers',
        'get_terminate', 'get_thread_local_invalid_parameter_handler',
        'get_timezone', 'get_tzname', 'get_unexpected', 'get_wpgmptr',
        'getc', 'getc_nolock', 'getchar', 'getcwd', 'getdcwd',
        'getdiskfree', 'getdrive', 'getdrives', 'getenv', 'getenv_s',
        'getmaxstdio', 'gets_s', 'getsystime', 'getw', 'getwc',
        'getwc_nolock', 'getwch', 'getwch_nolock', 'getwchar', 'getwche',
        'getwche_nolock', 'getws_s', 'gmtime32', 'gmtime32_s', 'gmtime64',
        'gmtime64_s', 'heapchk', 'heapmin', 'heapwalk', 'hypot', 'hypotf',
        'hypotl', 'i64toa', 'i64toa_s', 'i64tow', 'i64tow_s', 'ilogb',
        'ilogbf', 'ilogbl', 'ino_t', 'int16_t', 'int32_t', 'int64_t',
        'int8_t', 'int_fast16_t', 'int_fast32_t', 'int_fast64_t',
        'int_fast8_t', 'int_least16_t', 'int_least32_t', 'int_least64_t',
        'int_least8_t', 'interlockedand64', 'interlockedbittestandset',
        'interlockeddecrement64', 'interlockedexchange64',
        'interlockedexchangeadd64', 'interlockedincrement64',
        'interlockedor64', 'interlockedxor64', 'intmax_t', 'intptr_t',
        'invalid_parameter_noinfo', 'invalid_parameter_noinfo_noreturn',
        'invoke_watson', 'is_exception_typeof', 'is_wctype', 'isalnum',
        'isalnum_l', 'isalpha', 'isalpha_l', 'isatty', 'isblank',
        'isblank_l', 'ischartype_l', 'iscntrl', 'iscntrl_l', 'isctype',
        'isctype_l', 'isdigit', 'isdigit_l', 'isgraph', 'isgraph_l',
        'isleadbyte', 'isleadbyte_l', 'islower', 'islower_l', 'isnan',
        'isnanf', 'isprint', 'isprint_l', 'ispunct', 'ispunct_l',
        'isspace', 'isspace_l', 'isupper', 'isupper_l', 'iswalnum',
        'iswalnum_l', 'iswalpha', 'iswalpha_l', 'iswascii', 'iswblank',
        'iswblank_l', 'iswcntrl', 'iswcntrl_l', 'iswcsym_l', 'iswcsymf_l',
        'iswctype', 'iswctype_l', 'iswdigit', 'iswdigit_l', 'iswgraph',
        'iswgraph_l', 'iswlower', 'iswlower_l', 'iswprint', 'iswprint_l',
        'iswpunct', 'iswpunct_l', 'iswspace', 'iswspace_l', 'iswupper',
        'iswupper_l', 'iswxdigit', 'iswxdigit_l', 'isxdigit',
        'isxdigit_l', 'itoa', 'itoa_s', 'itow', 'itow_s', 'j0', 'j1',
        'jn', 'labs', 'ld_int', 'ldclass', 'ldexp', 'ldexpf', 'ldexpl',
        'ldiv', 'ldiv_t', 'ldlog', 'ldpcomp', 'ldpoly', 'ldscale',
        'ldsign', 'ldsin', 'ldtest', 'ldunscale', 'lfind', 'lfind_s',
        'lgamma', 'lgammaf', 'lgammal', 'llabs', 'lldiv', 'lldiv_t',
        'llrint', 'llrintf', 'llrintl', 'llround', 'llroundf', 'llroundl',
        'localtime32', 'localtime32_s', 'localtime64', 'localtime64_s',
        'lock_file', 'locking', 'log', 'log10', 'log10f', 'log10l',
        'log1p', 'log1pf', 'log1pl', 'log2', 'log2f', 'log2l', 'logb',
        'logbf', 'logbl', 'logf', 'logl', 'lrint', 'lrintf', 'lrintl',
        'lrotl', 'lrotr', 'lround', 'lroundf', 'lroundl', 'lsearch',
        'lsearch_s', 'lseek', 'lseeki64', 'ltoa', 'ltoa_s', 'ltow',
        'ltow_s', 'makepath', 'makepath_s', 'malloc', 'malloc_base',
        'matherr', 'mblen', 'mblen_l', 'mbrlen', 'mbrtowc', 'mbsinit',
        'mbsrtowcs', 'mbsrtowcs_s', 'mbstate_t', 'mbstowcs', 'mbstowcs_l',
        'mbstowcs_s', 'mbstowcs_s_l', 'mbstrlen', 'mbstrlen_l',
        'mbstrnlen', 'mbstrnlen_l', 'mbtowc', 'mbtowc_l', 'memccpy',
        'memchr', 'memcmp', 'memcpy', 'memicmp', 'memicmp_l', 'memmove',
        'memory_order_acq_rel', 'memory_order_acquire',
        'memory_order_consume', 'memory_order_relaxed',
        'memory_order_release', 'memory_order_seq_cst', 'memset', 'mkdir',
        'mkgmtime32', 'mkgmtime64', 'mktemp', 'mktemp_s', 'mktime32',
        'mktime64', 'mm_pause', 'modf', 'modff', 'modfl', 'msize',
        'msize_base', 'nan', 'nanf', 'nanl', 'nearbyint', 'nearbyintf',
        'nearbyintl', 'nextafter', 'nextafterf', 'nextafterl',
        'nexttoward', 'nexttowardf', 'nexttowardl', 'off_t', 'onexit',
        'open', 'open_osfhandle', 'pclose', 'perror', 'pipe', 'popen',
        'pow', 'powf', 'powl', 'printf', 'printf_l', 'printf_p',
        'printf_p_l', 'printf_s', 'printf_s_l', 'ptrdiff_t', 'putc',
        'putc_nolock', 'putchar', 'putenv', 'putenv_s', 'puts', 'putw',
        'putwc', 'putwc_nolock', 'putwch', 'putwch_nolock', 'putwchar',
        'putws', 'qsort', 'qsort_s', 'quick_exit', 'rand', 'read',
        'realloc', 'realloc_base', 'recalloc', 'recalloc_base',
        'remainder', 'remainderf', 'remainderl', 'remove', 'remquo',
        'remquof', 'remquol', 'rename', 'resetstkoflw', 'rewind', 'rint',
        'rintf', 'rintl', 'rmdir', 'rmtmp', 'rotl', 'rotl64', 'rotr',
        'rotr64', 'round', 'round_indeterminate', 'round_to_nearest',
        'round_toward_infinity', 'round_toward_neg_infinity',
        'round_toward_zero', 'roundf', 'roundl', 'rsize_t', 'scalb',
        'scalbf', 'scalbln', 'scalblnf', 'scalblnl', 'scalbn', 'scalbnf',
        'scalbnl', 'scanf', 'scanf_l', 'scanf_s', 'scanf_s_l', 'scprintf',
        'scprintf_l', 'scprintf_p', 'scprintf_p_l', 'scwprintf',
        'scwprintf_l', 'scwprintf_p', 'scwprintf_p_l', 'searchenv',
        'searchenv_s', 'set_FMA3_enable', 'set_abort_behavior',
        'set_controlfp', 'set_doserrno', 'set_errno', 'set_error_mode',
        'set_fmode', 'set_invalid_parameter_handler',
        'set_printf_count_output', 'set_purecall_handler',
        'set_se_translator', 'set_terminate',
        'set_thread_local_invalid_parameter_handler', 'set_unexpected',
        'setbuf', 'seterrormode', 'setmaxstdio', 'setmode', 'setsystime',
        'setvbuf', 'sin', 'sinf', 'sinh', 'sinhf', 'sinhl', 'sinl',
        'size_t', 'sleep', 'snprintf', 'snprintf_c', 'snprintf_c_l',
        'snprintf_l', 'snprintf_s', 'snprintf_s_l', 'snscanf',
        'snscanf_l', 'snscanf_s', 'snscanf_s_l', 'snwprintf',
        'snwprintf_l', 'snwprintf_s', 'snwprintf_s_l', 'snwscanf',
        'snwscanf_l', 'snwscanf_s', 'snwscanf_s_l', 'sopen',
        'sopen_dispatch', 'sopen_s', 'sopen_s_nolock', 'splitpath',
        'splitpath_s', 'sprintf', 'sprintf_l', 'sprintf_p', 'sprintf_p_l',
        'sprintf_s', 'sprintf_s_l', 'sqrt', 'sqrtf', 'sqrtl', 'srand',
        'sscanf', 'sscanf_l', 'sscanf_s', 'sscanf_s_l', 'stat32',
        'stat32i64', 'stat64', 'stat64i32', 'statusfp', 'std___Any_tag',
        'std___Atomic_counter_t',
        'std___Char_traits_char16_t__unsigned_short___int_type',
        'std___Char_traits_char32_t__unsigned_int___int_type',
        'std___Char_traits_char__int___int_type',
        'std___Char_traits_unsigned_short__unsigned_short___int_type',
        'std___Char_traits_wchar_t__unsigned_short___int_type',
        'std___Container_base',
        'std___Default_allocator_traits_std__allocator_char16_t____size_type',
        'std___Default_allocator_traits_std__allocator_char32_t____size_type',
        'std___Default_allocator_traits_std__allocator_char____size_type',
        'std___Default_allocator_traits_std__allocator_wchar_t____size_type',
        'std___Invoker_strategy',
        'std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____',
        'std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____',
        'std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_char____',
        'std___Iter_diff_t_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____',
        'std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char16_t____',
        'std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char32_t____',
        'std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_char____',
        'std___Iter_diff_t_std___String_iterator_std___String_val_std___Simple_types_wchar_t____',
        'std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____',
        'std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____',
        'std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_char____',
        'std___Iter_ref_t_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____',
        'std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char16_t____',
        'std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char32_t____',
        'std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_char____',
        'std___Iter_ref_t_std___String_iterator_std___String_val_std___Simple_types_wchar_t____',
        'std___Iterator_base',
        'std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______pointer',
        'std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______pointer',
        'std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_char______pointer',
        'std___Iterator_traits_base_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______pointer',
        'std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char16_t______pointer',
        'std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char32_t______pointer',
        'std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_char______pointer',
        'std___Iterator_traits_base_std___String_iterator_std___String_val_std___Simple_types_wchar_t______pointer',
        'std___Narrow_char_traits_char__int___int_type',
        'std___No_propagate_allocators', 'std___Propagate_allocators',
        'std___Rand_urng_from_func__result_type',
        'std___Simple_types_char16_t___const_pointer',
        'std___Simple_types_char16_t___difference_type',
        'std___Simple_types_char16_t___pointer',
        'std___Simple_types_char16_t___size_type',
        'std___Simple_types_char16_t___value_type',
        'std___Simple_types_char32_t___const_pointer',
        'std___Simple_types_char32_t___difference_type',
        'std___Simple_types_char32_t___pointer',
        'std___Simple_types_char32_t___size_type',
        'std___Simple_types_char32_t___value_type',
        'std___Simple_types_char___const_pointer',
        'std___Simple_types_char___difference_type',
        'std___Simple_types_char___pointer',
        'std___Simple_types_char___size_type',
        'std___Simple_types_char___value_type',
        'std___Simple_types_wchar_t___const_pointer',
        'std___Simple_types_wchar_t___difference_type',
        'std___Simple_types_wchar_t___pointer',
        'std___Simple_types_wchar_t___size_type',
        'std___Simple_types_wchar_t___value_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____difference_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____pointer',
        'std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____reference',
        'std___String_const_iterator_std___String_val_std___Simple_types_char16_t_____value_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____difference_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____pointer',
        'std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____reference',
        'std___String_const_iterator_std___String_val_std___Simple_types_char32_t_____value_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char_____difference_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_char_____pointer',
        'std___String_const_iterator_std___String_val_std___Simple_types_char_____reference',
        'std___String_const_iterator_std___String_val_std___Simple_types_char_____value_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____difference_type',
        'std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____pointer',
        'std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____reference',
        'std___String_const_iterator_std___String_val_std___Simple_types_wchar_t_____value_type',
        'std___String_iterator_std___String_val_std___Simple_types_char16_t_____difference_type',
        'std___String_iterator_std___String_val_std___Simple_types_char16_t_____pointer',
        'std___String_iterator_std___String_val_std___Simple_types_char16_t_____reference',
        'std___String_iterator_std___String_val_std___Simple_types_char16_t_____value_type',
        'std___String_iterator_std___String_val_std___Simple_types_char32_t_____difference_type',
        'std___String_iterator_std___String_val_std___Simple_types_char32_t_____pointer',
        'std___String_iterator_std___String_val_std___Simple_types_char32_t_____reference',
        'std___String_iterator_std___String_val_std___Simple_types_char32_t_____value_type',
        'std___String_iterator_std___String_val_std___Simple_types_char_____difference_type',
        'std___String_iterator_std___String_val_std___Simple_types_char_____pointer',
        'std___String_iterator_std___String_val_std___Simple_types_char_____reference',
        'std___String_iterator_std___String_val_std___Simple_types_char_____value_type',
        'std___String_iterator_std___String_val_std___Simple_types_wchar_t_____difference_type',
        'std___String_iterator_std___String_val_std___Simple_types_wchar_t_____pointer',
        'std___String_iterator_std___String_val_std___Simple_types_wchar_t_____reference',
        'std___String_iterator_std___String_val_std___Simple_types_wchar_t_____value_type',
        'std___String_val_std___Simple_types_char16_t____const_pointer',
        'std___String_val_std___Simple_types_char16_t____difference_type',
        'std___String_val_std___Simple_types_char16_t____pointer',
        'std___String_val_std___Simple_types_char16_t____size_type',
        'std___String_val_std___Simple_types_char16_t____value_type',
        'std___String_val_std___Simple_types_char32_t____const_pointer',
        'std___String_val_std___Simple_types_char32_t____difference_type',
        'std___String_val_std___Simple_types_char32_t____pointer',
        'std___String_val_std___Simple_types_char32_t____size_type',
        'std___String_val_std___Simple_types_char32_t____value_type',
        'std___String_val_std___Simple_types_char____const_pointer',
        'std___String_val_std___Simple_types_char____difference_type',
        'std___String_val_std___Simple_types_char____pointer',
        'std___String_val_std___Simple_types_char____size_type',
        'std___String_val_std___Simple_types_char____value_type',
        'std___String_val_std___Simple_types_wchar_t____const_pointer',
        'std___String_val_std___Simple_types_wchar_t____difference_type',
        'std___String_val_std___Simple_types_wchar_t____pointer',
        'std___String_val_std___Simple_types_wchar_t____size_type',
        'std___String_val_std___Simple_types_wchar_t____value_type',
        'std___Tree_child', 'std___Uninitialized',
        'std___WChar_traits__Elem___int_type',
        'std___WChar_traits_char16_t___int_type',
        'std___WChar_traits_unsigned_short___int_type',
        'std___WChar_traits_wchar_t___int_type',
        'std__basic_string_char16_t____Alty',
        'std__basic_string_char16_t____Scary_val',
        'std__basic_string_char16_t___allocator_type',
        'std__basic_string_char16_t___const_iterator',
        'std__basic_string_char16_t___const_reference',
        'std__basic_string_char16_t___const_reverse_iterator',
        'std__basic_string_char16_t___iterator',
        'std__basic_string_char16_t___reference',
        'std__basic_string_char16_t___reverse_iterator',
        'std__basic_string_char16_t___size_type',
        'std__basic_string_char16_t___value_type',
        'std__basic_string_char32_t____Alty',
        'std__basic_string_char32_t____Scary_val',
        'std__basic_string_char32_t___allocator_type',
        'std__basic_string_char32_t___const_iterator',
        'std__basic_string_char32_t___const_reference',
        'std__basic_string_char32_t___const_reverse_iterator',
        'std__basic_string_char32_t___iterator',
        'std__basic_string_char32_t___reference',
        'std__basic_string_char32_t___reverse_iterator',
        'std__basic_string_char32_t___size_type',
        'std__basic_string_char32_t___value_type',
        'std__basic_string_char____Alty',
        'std__basic_string_char____Scary_val',
        'std__basic_string_char___allocator_type',
        'std__basic_string_char___const_iterator',
        'std__basic_string_char___const_reference',
        'std__basic_string_char___const_reverse_iterator',
        'std__basic_string_char___iterator',
        'std__basic_string_char___reference',
        'std__basic_string_char___reverse_iterator',
        'std__basic_string_char___size_type',
        'std__basic_string_char___value_type',
        'std__basic_string_wchar_t____Alty',
        'std__basic_string_wchar_t____Scary_val',
        'std__basic_string_wchar_t___allocator_type',
        'std__basic_string_wchar_t___const_iterator',
        'std__basic_string_wchar_t___const_reference',
        'std__basic_string_wchar_t___const_reverse_iterator',
        'std__basic_string_wchar_t___iterator',
        'std__basic_string_wchar_t___reference',
        'std__basic_string_wchar_t___reverse_iterator',
        'std__basic_string_wchar_t___size_type',
        'std__basic_string_wchar_t___value_type', 'std__false_type',
        'std__filebuf', 'std__float_denorm_style',
        'std__float_round_style', 'std__fstream', 'std__ifstream',
        'std__integral_constant_bool__false___value_type',
        'std__integral_constant_bool__true___value_type',
        'std__integral_constant_unsigned_long_long__0___value_type',
        'std__ios', 'std__iostream', 'std__istream', 'std__istringstream',
        'std__max_align_t', 'std__memory_order', 'std__new_handler',
        'std__nullptr_t', 'std__ofstream', 'std__ostream',
        'std__ostringstream',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______difference_type',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______pointer',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t______reference',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______difference_type',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______pointer',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t______reference',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______difference_type',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______pointer',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char______reference',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______difference_type',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______pointer',
        'std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t______reference',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______difference_type',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______pointer',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t______reference',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______difference_type',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______pointer',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t______reference',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______difference_type',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______pointer',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char______reference',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______difference_type',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______pointer',
        'std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t______reference',
        'std__streambuf', 'std__streamoff', 'std__streampos',
        'std__streamsize', 'std__string', 'std__stringbuf',
        'std__stringstream', 'std__true_type', 'std__u16streampos',
        'std__u16string', 'std__u32streampos', 'std__u32string',
        'std__wfilebuf', 'std__wfstream', 'std__wifstream', 'std__wios',
        'std__wiostream', 'std__wistream', 'std__wistringstream',
        'std__wofstream', 'std__wostream', 'std__wostringstream',
        'std__wstreambuf', 'std__wstreampos', 'std__wstring',
        'std__wstringbuf', 'std__wstringstream', 'strcat', 'strcat_s',
        'strchr', 'strcmp', 'strcmpi', 'strcoll', 'strcoll_l', 'strcpy',
        'strcpy_s', 'strcspn', 'strdate', 'strdate_s', 'strdup',
        'strerror', 'strerror_s', 'strftime', 'strftime_l', 'stricmp',
        'stricmp_l', 'stricoll', 'stricoll_l', 'strlen', 'strlwr',
        'strlwr_l', 'strlwr_s', 'strlwr_s_l', 'strncat', 'strncat_s',
        'strncmp', 'strncoll', 'strncoll_l', 'strncpy', 'strncpy_s',
        'strnicmp', 'strnicmp_l', 'strnicoll', 'strnicoll_l', 'strnlen',
        'strnset', 'strnset_s', 'strpbrk', 'strrchr', 'strrev', 'strset',
        'strset_s', 'strspn', 'strstr', 'strtime', 'strtime_s', 'strtod',
        'strtod_l', 'strtof', 'strtof_l', 'strtoi64', 'strtoi64_l',
        'strtok', 'strtok_s', 'strtol', 'strtol_l', 'strtold',
        'strtold_l', 'strtoll', 'strtoll_l', 'strtoui64', 'strtoui64_l',
        'strtoul', 'strtoul_l', 'strtoull', 'strtoull_l',
        'struct__CRT_DOUBLE', 'struct__CRT_FLOAT',
        'struct__Combined_type_float__double_',
        'struct__Combined_type_float__long_double_',
        'struct__CrtMemBlockHeader', 'struct__CrtMemState',
        'struct__EXCEPTION_POINTERS', 'struct__LDBL12', 'struct__LDOUBLE',
        'struct__LONGDOUBLE', 'struct__Real_type_float_',
        'struct__Real_type_long_double_',
        'struct__Real_widened_double__double_',
        'struct__Real_widened_double__float_',
        'struct__Real_widened_float__double_',
        'struct__Real_widened_float__float_', 'struct___crt_locale_data',
        'struct___crt_locale_data_public', 'struct___crt_locale_pointers',
        'struct___crt_multibyte_data', 'struct___finddata64_t',
        'struct___std_exception_data', 'struct__complex',
        'struct__diskfree_t', 'struct__div_t', 'struct__exception',
        'struct__finddata32_t', 'struct__finddata32i64_t',
        'struct__finddata64i32_t', 'struct__heapinfo', 'struct__iobuf',
        'struct__ldiv_t', 'struct__lldiv_t', 'struct__stat32',
        'struct__stat32i64', 'struct__stat64', 'struct__stat64i32',
        'struct__timespec32', 'struct__timespec64',
        'struct__wfinddata32_t', 'struct__wfinddata32i64_t',
        'struct__wfinddata64_t', 'struct__wfinddata64i32_t',
        'struct_stat', 'struct_std___Alloc_exact_args_t',
        'struct_std___Alloc_unpack_tuple_t',
        'struct_std___Basic_container_proxy_ptr12',
        'struct_std___Char_traits_char16_t__unsigned_short_',
        'struct_std___Char_traits_char32_t__unsigned_int_',
        'struct_std___Char_traits_char__int_',
        'struct_std___Char_traits_unsigned_short__unsigned_short_',
        'struct_std___Char_traits_wchar_t__unsigned_short_',
        'struct_std___Compressed_pair_std__allocator_char16_t___std___String_val_std___Simple_types_char16_t____true_',
        'struct_std___Compressed_pair_std__allocator_char32_t___std___String_val_std___Simple_types_char32_t____true_',
        'struct_std___Compressed_pair_std__allocator_char___std___String_val_std___Simple_types_char____true_',
        'struct_std___Compressed_pair_std__allocator_wchar_t___std___String_val_std___Simple_types_wchar_t____true_',
        'struct_std___Container_base0', 'struct_std___Container_base12',
        'struct_std___Container_proxy',
        'struct_std___Default_allocate_traits',
        'struct_std___Default_sentinel', 'struct_std___Distance_unknown',
        'struct_std___Equal_allocators', 'struct_std___Exact_args_t',
        'struct_std___Fake_allocator', 'struct_std___Fake_proxy_ptr_impl',
        'struct_std___False_copy_cat',
        'struct_std___Floating_type_traits_double_',
        'struct_std___Floating_type_traits_float_',
        'struct_std___Floating_type_traits_long_double_',
        'struct_std___Ignore', 'struct_std___Init_locks',
        'struct_std___Invoker_functor', 'struct_std___Invoker_pmd_object',
        'struct_std___Invoker_pmd_pointer',
        'struct_std___Invoker_pmd_refwrap',
        'struct_std___Invoker_pmf_object',
        'struct_std___Invoker_pmf_pointer',
        'struct_std___Invoker_pmf_refwrap',
        'struct_std___Is_character_char_',
        'struct_std___Is_character_or_bool_bool_',
        'struct_std___Is_character_signed_char_',
        'struct_std___Is_character_unsigned_char_',
        'struct_std___Iterator_base0', 'struct_std___Iterator_base12',
        'struct_std___Leave_proxy_unbound', 'struct_std___Lockit',
        'struct_std___Make_signed2_1_', 'struct_std___Make_signed2_2_',
        'struct_std___Make_signed2_4_', 'struct_std___Make_signed2_8_',
        'struct_std___Make_unsigned2_1_',
        'struct_std___Make_unsigned2_2_',
        'struct_std___Make_unsigned2_4_',
        'struct_std___Make_unsigned2_8_', 'struct_std___Maximum__',
        'struct_std___Move_allocator_tag',
        'struct_std___Narrow_char_traits_char__int_',
        'struct_std___Nontrivial_dummy_type', 'struct_std___Num_base',
        'struct_std___Num_float_base', 'struct_std___Num_int_base',
        'struct_std___One_then_variadic_args_t',
        'struct_std___Rand_urng_from_func', 'struct_std___Select_false_',
        'struct_std___String_const_iterator_std___String_val_std___Simple_types_char16_t___',
        'struct_std___String_const_iterator_std___String_val_std___Simple_types_char32_t___',
        'struct_std___String_const_iterator_std___String_val_std___Simple_types_char___',
        'struct_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t___',
        'struct_std___String_constructor_concat_tag',
        'struct_std___String_constructor_rvalue_allocator_tag',
        'struct_std___String_iterator_std___String_val_std___Simple_types_char16_t___',
        'struct_std___String_iterator_std___String_val_std___Simple_types_char32_t___',
        'struct_std___String_iterator_std___String_val_std___Simple_types_char___',
        'struct_std___String_iterator_std___String_val_std___Simple_types_wchar_t___',
        'struct_std___String_val_std___Simple_types_char16_t__',
        'struct_std___String_val_std___Simple_types_char32_t__',
        'struct_std___String_val_std___Simple_types_char__',
        'struct_std___String_val_std___Simple_types_wchar_t__',
        'struct_std___Unpack_tuple_t', 'struct_std___Unused_parameter',
        'struct_std___WChar_traits_char16_t_',
        'struct_std___WChar_traits_unsigned_short_',
        'struct_std___WChar_traits_wchar_t_',
        'struct_std___Zero_then_variadic_args_t',
        'struct_std__allocator_arg_t', 'struct_std__allocator_char16_t_',
        'struct_std__allocator_char32_t_', 'struct_std__allocator_char_',
        'struct_std__allocator_void_', 'struct_std__allocator_wchar_t_',
        'struct_std__bad_alloc', 'struct_std__bad_alloc_vtbl',
        'struct_std__bad_array_new_length',
        'struct_std__bad_array_new_length_vtbl',
        'struct_std__bad_exception', 'struct_std__bad_exception_vtbl',
        'struct_std__basic_filebuf_char_',
        'struct_std__basic_filebuf_wchar_t_',
        'struct_std__basic_fstream_char_',
        'struct_std__basic_fstream_wchar_t_',
        'struct_std__basic_ifstream_char_',
        'struct_std__basic_ifstream_wchar_t_',
        'struct_std__basic_ios_char_', 'struct_std__basic_ios_wchar_t_',
        'struct_std__basic_iostream_char_',
        'struct_std__basic_iostream_wchar_t_',
        'struct_std__basic_istream_char_',
        'struct_std__basic_istream_wchar_t_',
        'struct_std__basic_istringstream_char_',
        'struct_std__basic_istringstream_wchar_t_',
        'struct_std__basic_ofstream_char_',
        'struct_std__basic_ofstream_wchar_t_',
        'struct_std__basic_ostream_char_',
        'struct_std__basic_ostream_wchar_t_',
        'struct_std__basic_ostringstream_char_',
        'struct_std__basic_ostringstream_wchar_t_',
        'struct_std__basic_streambuf_char_',
        'struct_std__basic_streambuf_wchar_t_',
        'struct_std__basic_string_char16_t_',
        'struct_std__basic_string_char32_t_',
        'struct_std__basic_string_char_',
        'struct_std__basic_string_wchar_t_',
        'struct_std__basic_stringbuf_char_',
        'struct_std__basic_stringbuf_wchar_t_',
        'struct_std__basic_stringstream_char_',
        'struct_std__basic_stringstream_wchar_t_',
        'struct_std__bidirectional_iterator_tag',
        'struct_std__char_traits_char16_t_',
        'struct_std__char_traits_char32_t_',
        'struct_std__char_traits_char_',
        'struct_std__char_traits_unsigned_short_',
        'struct_std__char_traits_wchar_t_', 'struct_std__common_type__',
        'struct_std__equal_to_void_', 'struct_std__exception',
        'struct_std__exception_ptr', 'struct_std__exception_vtbl',
        'struct_std__forward_iterator_tag', 'struct_std__fpos__Mbstatet_',
        'struct_std__greater_equal_void_', 'struct_std__greater_void_',
        'struct_std__hash_double_', 'struct_std__hash_float_',
        'struct_std__hash_long_double_',
        'struct_std__hash_std__nullptr_t_',
        'struct_std__initializer_list_char16_t_',
        'struct_std__initializer_list_char32_t_',
        'struct_std__initializer_list_char_',
        'struct_std__initializer_list_wchar_t_',
        'struct_std__input_iterator_tag',
        'struct_std__integral_constant_bool__false_',
        'struct_std__integral_constant_bool__true_',
        'struct_std__integral_constant_unsigned_long_long__0_',
        'struct_std__ios_base', 'struct_std__less_equal_void_',
        'struct_std__less_void_', 'struct_std__locale',
        'struct_std__minus_void_', 'struct_std__multiplies_void_',
        'struct_std__nested_exception',
        'struct_std__nested_exception_vtbl',
        'struct_std__not_equal_to_void_', 'struct_std__nothrow_t',
        'struct_std__numeric_limits_bool_',
        'struct_std__numeric_limits_char16_t_',
        'struct_std__numeric_limits_char32_t_',
        'struct_std__numeric_limits_char_',
        'struct_std__numeric_limits_double_',
        'struct_std__numeric_limits_float_',
        'struct_std__numeric_limits_int_',
        'struct_std__numeric_limits_long_',
        'struct_std__numeric_limits_long_double_',
        'struct_std__numeric_limits_long_long_',
        'struct_std__numeric_limits_short_',
        'struct_std__numeric_limits_signed_char_',
        'struct_std__numeric_limits_unsigned_char_',
        'struct_std__numeric_limits_unsigned_int_',
        'struct_std__numeric_limits_unsigned_long_',
        'struct_std__numeric_limits_unsigned_long_long_',
        'struct_std__numeric_limits_unsigned_short_',
        'struct_std__numeric_limits_wchar_t_',
        'struct_std__output_iterator_tag',
        'struct_std__piecewise_construct_t', 'struct_std__plus_void_',
        'struct_std__random_access_iterator_tag',
        'struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char16_t____',
        'struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char32_t____',
        'struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_char____',
        'struct_std__reverse_iterator_std___String_const_iterator_std___String_val_std___Simple_types_wchar_t____',
        'struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char16_t____',
        'struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char32_t____',
        'struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_char____',
        'struct_std__reverse_iterator_std___String_iterator_std___String_val_std___Simple_types_wchar_t____',
        'struct_std__tuple__', 'struct_timespec', 'struct_tm',
        'struct_type_info', 'strupr', 'strupr_l', 'strupr_s',
        'strupr_s_l', 'strxfrm', 'strxfrm_l', 'swab', 'swprintf',
        'swprintf_c', 'swprintf_c_l', 'swprintf_l', 'swprintf_p',
        'swprintf_p_l', 'swprintf_s', 'swprintf_s_l', 'swscanf',
        'swscanf_l', 'swscanf_s', 'swscanf_s_l', 'system', 'tan', 'tanf',
        'tanh', 'tanhf', 'tanhl', 'tanl', 'tell', 'telli64', 'tempnam',
        'terminate', 'terminate_function', 'terminate_handler', 'tgamma',
        'tgammaf', 'tgammal', 'time32', 'time64', 'time_t',
        'timespec32_get', 'timespec64_get', 'tmpfile', 'tmpfile_s',
        'tmpnam', 'tmpnam_s', 'tolower', 'tolower_l', 'toupper',
        'toupper_l', 'towlower', 'towlower_l', 'towupper', 'towupper_l',
        'trunc', 'truncf', 'truncl', 'tzset', 'ui64toa', 'ui64toa_s',
        'ui64tow', 'ui64tow_s', 'uint_fast16_t', 'uint_fast32_t',
        'uint_fast64_t', 'uint_fast8_t', 'uint_least16_t',
        'uint_least32_t', 'uint_least64_t', 'uint_least8_t', 'uintmax_t',
        'uintptr_t', 'ultoa', 'ultoa_s', 'ultow', 'ultow_s', 'umask',
        'umask_s', 'umul128', 'unexpected', 'unexpected_function',
        'unexpected_handler', 'ungetc', 'ungetc_nolock', 'ungetwc',
        'ungetwc_nolock', 'ungetwch', 'ungetwch_nolock',
        'union__double_val', 'union__float_const', 'union__float_val',
        'union__ldouble_val',
        'union_std___String_val_std___Simple_types_char16_t_____Bxty',
        'union_std___String_val_std___Simple_types_char32_t_____Bxty',
        'union_std___String_val_std___Simple_types_char_____Bxty',
        'union_std___String_val_std___Simple_types_wchar_t_____Bxty',
        'unlink', 'unlock_file', 'va_list', 'vcwprintf', 'vcwprintf_l',
        'vcwprintf_p', 'vcwprintf_p_l', 'vcwprintf_s', 'vcwprintf_s_l',
        'vcwscanf', 'vcwscanf_l', 'vcwscanf_s', 'vcwscanf_s_l',
        'vfprintf', 'vfprintf_l', 'vfprintf_p', 'vfprintf_p_l',
        'vfprintf_s', 'vfprintf_s_l', 'vfscanf', 'vfscanf_l', 'vfscanf_s',
        'vfscanf_s_l', 'vfwprintf', 'vfwprintf_l', 'vfwprintf_p',
        'vfwprintf_p_l', 'vfwprintf_s', 'vfwprintf_s_l', 'vfwscanf',
        'vfwscanf_l', 'vfwscanf_s', 'vfwscanf_s_l', 'vprintf',
        'vprintf_l', 'vprintf_p', 'vprintf_p_l', 'vprintf_s',
        'vprintf_s_l', 'vscanf', 'vscanf_l', 'vscanf_s', 'vscanf_s_l',
        'vscprintf', 'vscprintf_l', 'vscprintf_p', 'vscprintf_p_l',
        'vscwprintf', 'vscwprintf_l', 'vscwprintf_p', 'vscwprintf_p_l',
        'vsnprintf', 'vsnprintf_c', 'vsnprintf_c_l', 'vsnprintf_l',
        'vsnprintf_s', 'vsnprintf_s_l', 'vsnwprintf', 'vsnwprintf_l',
        'vsnwprintf_s', 'vsnwprintf_s_l', 'vsnwscanf_l', 'vsnwscanf_s_l',
        'vsprintf', 'vsprintf_l', 'vsprintf_p', 'vsprintf_p_l',
        'vsprintf_s', 'vsprintf_s_l', 'vsscanf', 'vsscanf_l', 'vsscanf_s',
        'vsscanf_s_l', 'vswprintf', 'vswprintf_c', 'vswprintf_c_l',
        'vswprintf_l', 'vswprintf_p', 'vswprintf_p_l', 'vswprintf_s',
        'vswprintf_s_l', 'vswscanf', 'vswscanf_l', 'vswscanf_s',
        'vswscanf_s_l', 'vwprintf', 'vwprintf_l', 'vwprintf_p',
        'vwprintf_p_l', 'vwprintf_s', 'vwprintf_s_l', 'vwscanf',
        'vwscanf_l', 'vwscanf_s', 'vwscanf_s_l', 'waccess', 'waccess_s',
        'wasctime', 'wasctime_s', 'wassert', 'wchdir', 'wchmod', 'wcreat',
        'wcreate_locale', 'wcrtomb', 'wcrtomb_s', 'wcscat', 'wcscat_s',
        'wcschr', 'wcscmp', 'wcscoll', 'wcscoll_l', 'wcscpy', 'wcscpy_s',
        'wcscspn', 'wcsdup', 'wcserror', 'wcserror_s', 'wcsftime',
        'wcsftime_l', 'wcsicmp', 'wcsicmp_l', 'wcsicoll', 'wcsicoll_l',
        'wcslen', 'wcslwr', 'wcslwr_l', 'wcslwr_s', 'wcslwr_s_l',
        'wcsncat', 'wcsncat_s', 'wcsncmp', 'wcsncoll', 'wcsncoll_l',
        'wcsncpy', 'wcsncpy_s', 'wcsnicmp', 'wcsnicmp_l', 'wcsnicoll',
        'wcsnicoll_l', 'wcsnlen', 'wcsnset', 'wcsnset_s', 'wcspbrk',
        'wcsrchr', 'wcsrev', 'wcsrtombs', 'wcsrtombs_s', 'wcsset',
        'wcsset_s', 'wcsspn', 'wcsstr', 'wcstod', 'wcstod_l', 'wcstof',
        'wcstof_l', 'wcstoi64', 'wcstoi64_l', 'wcstok', 'wcstok_s',
        'wcstol', 'wcstol_l', 'wcstold', 'wcstold_l', 'wcstoll',
        'wcstoll_l', 'wcstombs', 'wcstombs_l', 'wcstombs_s',
        'wcstombs_s_l', 'wcstoui64', 'wcstoui64_l', 'wcstoul',
        'wcstoul_l', 'wcstoull', 'wcstoull_l', 'wcsupr', 'wcsupr_l',
        'wcsupr_s', 'wcsupr_s_l', 'wcsxfrm', 'wcsxfrm_l', 'wctime32',
        'wctime32_s', 'wctime64', 'wctime64_s', 'wctob', 'wctomb',
        'wctomb_l', 'wctomb_s', 'wctomb_s_l', 'wctype_t', 'wdupenv_s',
        'wexecl', 'wexecle', 'wexeclp', 'wexeclpe', 'wexecv', 'wexecve',
        'wexecvp', 'wexecvpe', 'wfdopen', 'wfindfirst32',
        'wfindfirst32i64', 'wfindfirst64', 'wfindfirst64i32',
        'wfindnext32', 'wfindnext32i64', 'wfindnext64', 'wfindnext64i32',
        'wfopen', 'wfopen_s', 'wfreopen', 'wfreopen_s', 'wfsopen',
        'wfullpath', 'wgetcwd', 'wgetdcwd', 'wgetenv', 'wgetenv_s',
        'wint_t', 'wmakepath', 'wmakepath_s', 'wmemchr', 'wmemcmp',
        'wmemcpy', 'wmemcpy_s', 'wmemmove', 'wmemmove_s', 'wmemset',
        'wmkdir', 'wmktemp', 'wmktemp_s', 'wperror', 'wpopen', 'wprintf',
        'wprintf_l', 'wprintf_p', 'wprintf_p_l', 'wprintf_s',
        'wprintf_s_l', 'wputenv', 'wputenv_s', 'wremove', 'wrename',
        'write', 'wrmdir', 'wscanf', 'wscanf_l', 'wscanf_s', 'wscanf_s_l',
        'wsearchenv', 'wsearchenv_s', 'wsetlocale', 'wsopen_dispatch',
        'wsopen_s', 'wspawnl', 'wspawnle', 'wspawnlp', 'wspawnlpe',
        'wspawnv', 'wspawnve', 'wspawnvp', 'wspawnvpe', 'wsplitpath',
        'wsplitpath_s', 'wstat32', 'wstat32i64', 'wstat64', 'wstat64i32',
        'wstrdate', 'wstrdate_s', 'wstrtime', 'wstrtime_s', 'wsystem',
        'wtempnam', 'wtmpnam', 'wtmpnam_s', 'wtof', 'wtof_l', 'wtoi',
        'wtoi64', 'wtoi64_l', 'wtoi_l', 'wtol', 'wtol_l', 'wtoll',
        'wtoll_l', 'wunlink', 'y0', 'y1', 'yn']
    
    return locals()
