# IDAKern

An IDAPython wrapper for IDA Pro's kernel dll.

## Why?

Many useful and low level API aren't exposed by IDAPython's SWIG wrapper. 

Although those API are documented and exported in SDK, IDAPython still cannot easily use them due to lack of structure.

## Usage

```
import sys
sys.path.append(r'C:\ida_kern\src')

import ida_kern
k = ida_kern.IDAKern()
print(k.idadir(None))
```

~Loading takes 3-5 seconds currently, be patient ;)~

Now only takes 0.5 seconds to load!

Examples can be found in `examples/` folder:
- hook_to_notification_point example usage (HT_UI hook as example)
- qstring manipulation
- tinfo_t manipulation
- (more!)

## How does it work?

With these tools we can now generate raw ctypes API binding for IDA SDK:
- IDAClang: can export all types & symbols in headers to til
- Tilib (in SDK): export types in til to C header
- My Tool: sanitize tilib's output & generate compilable source code
- ctypeslib: generate bindings from C/simple C++ source file (need to use my fork to fix some bugs)
