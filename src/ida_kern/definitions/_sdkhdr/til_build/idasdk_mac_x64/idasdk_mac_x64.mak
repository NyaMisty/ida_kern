TIL_NAME = idasdk_mac_x64
TIL_DESC = "IDA SDK headers for MacOSX"
INPUT_FILE = ../idasdk.h
SDK = /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.15.sdk
TOOLCHAIN = /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain
CLANG_ARGV = -target x86_64-apple-darwin                 \
             -x objective-c++                            \
             -isysroot $(SDK)                            \
             -I$(TOOLCHAIN)/usr/include/c++/v1           \
             -I$(TOOLCHAIN)/usr/lib/clang/11.0.3/include \
             -I$(IDASDK)/include/                       \
             -D__MAC__                                   \
             -D__EA64__                                  \
             -Wno-nullability-completeness

include ../idaclang.mak
