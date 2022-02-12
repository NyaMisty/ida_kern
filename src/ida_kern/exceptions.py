class IDAKernException(Exception):
    pass

class IDAKernCtypesException(IDAKernException):
    pass

class UnknownArchitecture(IDAKernCtypesException):
    pass