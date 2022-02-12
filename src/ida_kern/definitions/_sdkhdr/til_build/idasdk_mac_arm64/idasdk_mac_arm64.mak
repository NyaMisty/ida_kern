TIL_NAME = idasdk_mac_arm64
TIL_DESC = "IDA SDK headers for arm64 macOS 12"
INPUT_FILE = ../idasdk.h
SDK = /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX12.0.sdk
TOOLCHAIN = /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain
CLANG_ARGV = -target arm64-apple-darwin                  \
             -x objective-c++                            \
             -isysroot $(SDK)                            \
             -I$(TOOLCHAIN)/usr/lib/clang/13.0.0/include \
             -I$(IDASDK)/include/                       \
             -D__MAC__                                   \
             -D__EA64__                                  \
             -D__ARM__                                   \
             -Wno-nullability-completeness

include ../idaclang.mak
