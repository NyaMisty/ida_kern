#include <stdlib.h>     /* size_t, nullptr, memory */
#include <stdarg.h>
#include <stddef.h>
#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include <ctype.h>
#include <time.h>
#ifdef __cplusplus
#include <new>
#include <string>
#endif
#if defined(__NT__)
#  include <malloc.h>
#endif

/// \def{WIN32_LEAN_AND_MEAN, compile faster}
#if defined(_MSC_VER)
#  define WIN32_LEAN_AND_MEAN
#  include <string.h>
#  include <io.h>
#  include <direct.h>
#else
#  include <wchar.h>
#  include <string.h>
#  include <unistd.h>
#  include <sys/stat.h>
#  include <errno.h>
#endif
#ifdef __cplusplus
#  include <set>
#  include <map>
#  include <algorithm>
#endif
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
