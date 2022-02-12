TIL_NAME = idasdk_linux
TIL_DESC = "IDA SDK headers for x64 linux"
INPUT_FILE = ../idasdk.h
GCC_VERSION = $(shell expr `gcc -dumpversion | cut -f1 -d.`)
CLANG_ARGV = -target x86_64-pc-linux                                      \
             -x c++                                                       \
             -I/usr/lib/gcc/x86_64-linux-gnu/$(GCC_VERSION)/include       \
             -I/usr/local/include                                         \
             -I/usr/lib/gcc/x86_64-linux-gnu/$(GCC_VERSION)/include-fixed \
             -I/usr/include/x86_64-linux-gnu                              \
             -I/usr/include                                               \
             -I$(IDASDK)/include/                                        \
             -D__LINUX__                                                  \
             -D__EA64__                                                   \
             -Wno-nullability-completeness

include ../idaclang.mak
