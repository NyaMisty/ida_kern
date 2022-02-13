# Generate inter-op wrappers of ctypes structs we used
import re
import subprocess
from collections import OrderedDict

# https://stackoverflow.com/questions/2319019/using-regex-to-remove-comments-from-source-files
def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)


IDENTIFIER = r'\w\d_'

def replaceTemplateArgs(content):
    def cleanName(nam):
        nam_map = {}
        for c in ' :<>,-()':
            nam_map[c] = '_'
        nam_map['&'] = '_R'
        nam_map['*'] = '_P'
        for c, v in nam_map.items():
            nam = nam.replace(c,v)
        return nam
    
    content = content.replace('::', '__')

    content = content.replace('$', '_')
    
    content = content.replace('?', '_')
    
    content = content.replace('~', '_del_')
    
    replaceList = set()
    
    typename = r'[%s][%s<>_ ,*]+?[%s>]' % (IDENTIFIER, IDENTIFIER, IDENTIFIER)

    #for strucName in re.findall(r'\nstruct (%s);\n' % typename, content):
    #    replaceList.append((strucName, cleanName(strucName)))
    
    #for strucName in re.findall(r'\n  struct (%s) \*[a-zA-Z_]+?;\n' % typename, content):
    #    replaceList.append((strucName, cleanName(strucName)))
    
    #for strucName, _, strucBase in re.findall(r'struct __cppobj (.*?)( : (.*?)|)\n', content):
    #for _, _, _, _, strucName, _, strucBase in re.findall(r'\nstruct( __[^ ]+?|)( __[^ ]+?|)( __[^ ]+?|)( __[^ ]+?|) (%s)( : (%s)|)\n' % (typename, typename), content):
    #    replaceList.append((strucName, cleanName(strucName)))
    #    replaceList.append((strucBase, cleanName(strucBase)))
    
    templateArgChars = r'A-z0-9_ :,\-()?*&'
    templateArg_ = r'[%s]+?' % templateArgChars
    templateArg = r'[%s]*?' % templateArgChars
    templatePat = []
    def genTemplatePat(level):
        if level == 1:
            ret = r'<(%s)>' % templateArg
            templatePat.append(ret)
        else:
            genTemplatePat(level - 1)
            for pat in templatePat[:]:
                ret = r'<(%s%s+?%s)+?>' % (templateArg_, '(%s)' % '|'.join(templatePat), templateArg)
                templatePat.append(ret)

        return
    
    genTemplatePat(4)
    
    for i, pat in enumerate(templatePat):
        #print("Finding matchs on pattern %d: %s" % (i, pat))
        for match in re.finditer(pat, content):
            tmplArg = match.group(0)
            if tmplArg == '*':
                print(pat, match)
                sys.exit(1)
            replaceList.add(tmplArg)
            #print(match.start(), tmplArg)

    
    content = content.replace('\nconst struct', '\nstruct')
    
    #for strucName in re.findall(r'^typedef struct (.*?);\n', content):
    #    replaceList.append((strucName, cleanName(strucName)))
    
    replaceList = list(set(replaceList))
    #replaceList.sort(key=lambda x: len(x[0]), reverse=True)
    replaceList.sort(key=lambda x: len(x), reverse=True)
    
    for a in replaceList[:]:
        print(a)
        content = content.replace(a, cleanName(a))
        if 'struct_std__nested_exception_vtbl' in content:
            break
    return content

class TypeDecl(object):
    def __init__(self, typClass, typName, typDef):
        self.typClass = typClass
        self.typName = typName
        self.typDef = typDef
    
    def __repr__(self):
        return '<%s %s: %s>' % (self.typClass, self.typName, self.typDef)
    
    def __str__(self):
        return self.typDef

def parseDecls(types):
    # find all defined types' identifiers
    identifierPat = '[%s]+' % IDENTIFIER
    type_defs = {}
    def add_type(cls, t, line):
        #print(t, line[:100])
        if t in type_defs:
            print("Offending decl: %s" % type_defs[t])
        assert not t in type_defs
        type_defs[t] = TypeDecl(cls, t, line)
    for line in types.splitlines():
        line = line.replace('__cdecl ', '').replace('__cppobj ', '')
        if line.startswith('/*'):
            continue
        
        if line.startswith('enum '):
            matches = re.findall(r'enum (%s) :' % identifierPat, line)
            if not matches:
                print(line)
            match = matches[0]
            #identifiers.append('enum ' + match)
            add_type('enum', match, line)
        elif line.startswith('union '):
            match = re.findall(r'union (%s) ' % identifierPat, line)[0]
            #identifiers.append('union ' + match)
            add_type('union', match, line)
        elif line.startswith('struct '):
            matches = []
            matches += re.findall(r'struct (%s) : (%s|, )+? {' % (identifierPat, identifierPat), line)
            matches += re.findall(r'struct (%s) {' % identifierPat, line)
            matches += re.findall(r'struct (%s);' % identifierPat, line)
            for m in matches:
                if not isinstance(m, tuple):
                    m = [m]
                add_type('struct', m[0], line)
        elif line.startswith('typedef '):
            matches = []
            matches += re.findall(r'typedef .*?(%s);' % identifierPat, line)
            matches += re.findall(r'typedef .*?(%s)\(.*?\);' % identifierPat, line)
            matches += re.findall(r'typedef .*?(%s)\)\(.*?\);' % identifierPat, line)
            matches += re.findall(r'typedef .*?(%s)\[.*?\];' % identifierPat, line)
            if not matches:
                print(line)
            #identifiers.append(matches[0])
            add_type('typedef', matches[0], line)
        else:
            assert False
    return type_defs
    

def rewrite_ida_header(hdrLoc, outLoc):
    with open(hdrLoc, 'r') as f:
        content = f.read()
    
    #content = content.replace(';', ';\n').replace('{', '{\n').replace('}', '}\n')
    
    #BLACKLIST = ['procmod_t', '__m128i']

    #for strucName in BLACKLIST:
    #    content = re.sub(r'(\n(struct|enum|union) .*?' + strucName + '.*?\n{\n[\s\S]+?\n};\n)', '/*\\1*/\n', content)

    types, _, symbols = content.partition('\n\n')
    symbols = '\n'.join([c for c in symbols.splitlines() if '?' not in c])
    content = types + '\n\n' + symbols

    TYPEDEF_BLACKLIST = ['_Mbstatet']
    for typeName in TYPEDEF_BLACKLIST:
        content = re.sub(r'\n(typedef .*? ' + typeName + ';)\n', '\n/*\\1*/\n', content)

    # remove vft
    content = re.sub(r'\nstruct /\*VFT\*/ ((.*?_vtbl) {.*?};)\n', '\nstruct \\2; /* \\1*/\n', content)

    # remove coments
    #content = remove_comments(content)
    content = replaceTemplateArgs(content)
    
    content = re.sub(r'\nenum ([%s]+?) : __int32 ' % IDENTIFIER, '\nenum \\1 : unsigned __int32 ', content)
    
    types, _, symbols = content.partition('\n\n')
    
    type_defs = parseDecls(types)
    assert 'procmod_t' in type_defs
    
    #assert len(type_defs) == len(types.splitlines())
    
    # analyse the type hierarchy
    type_defs_sorted = OrderedDict(sorted(type_defs.items(), key=lambda x: len(x[0]), reverse=True))
    typeDefDeps = {}
    for typName, typInfo in type_defs_sorted.items():
        typeDefDeps[typName] = []
        otherTyps = [t for t in type_defs_sorted if t != typName]
        typDef = typInfo.typDef
        for otherTyp in otherTyps:
            if otherTyp in typDef and re.search(r'[ ;*(){},]%s[ ;*(){},]' % (otherTyp), typDef):
                isDepend = True
                if re.search(r'[ ;*(){},]%s *\*' % (otherTyp), typDef): # is Pointer
                    if type_defs_sorted[otherTyp].typClass == 'struct':
                        if typInfo.typClass == 'struct':
                            # ignored pointer in struct
                            isDepend = False
                        if typInfo.typClass == 'typedef':
                            isDepend = False
                if isDepend:    
                    typeDefDeps[typName].append(otherTyp)
                # masking cur type
                typDef = typDef.replace(otherTyp, '$$$$')
                
        #print("%s -> %s" % (typName, typeDefDeps[typName]))
    
    typeDefDeps_sorted = OrderedDict(sorted(typeDefDeps.items(), key=lambda x: len(x[1])))

    print("Type hierarchy analysis finished:")
    for t in typeDefDeps_sorted:
        print("%s -> %s" % (t, typeDefDeps_sorted[t]))

    # BFS the dependency tree
    typeLines = []
    typKnown = []
    while typeDefDeps_sorted:
        has_change = False
        for k, v in list(typeDefDeps_sorted.items()):
            if all((t in typKnown for t in v)):
                typeDefDeps_sorted.pop(k)
                typeLines.append(type_defs_sorted[k])
                typKnown.append(k)
                has_change = True
        if not has_change:
            raise Exception("Dependency loop!\n  curKnown: %s,\n  remaining: %s\n" % (
                    typKnown, 
                    '\n'.join(['%s -> %s' % (k,v) for k,v in typeDefDeps_sorted.items()])
                    ))

    symbolLines = []
    for symLine in symbols.splitlines():
        if symLine.startswith('#error '):
            continue
        
        BLACKLIST_SYMS = ['operator delete', 'operator delete[]', 'operator new', 'operator new[]', 'operator""s', 'operator&', 'operator+', 'operator-', 'operator<', 'operator^', 'operator|']
        if any(c in symLine for c in BLACKLIST_SYMS):
            continue
        
        # for: int __cdecl _stat32(const char *_FileName, _stat32 *_Stat);
        symLine = symLine.replace('_stat32 *', 'struct _stat32 *').replace('_stat32i64 *', 'struct _stat32i64 *').replace('_stat64 *', 'struct _stat64 *').replace('_stat64i32 *', 'struct _stat64i32 *')
        
        if symLine.endswith('[];'): # const char regkey_history[];
            continue
        parts = symLine.split(' ')
        t = parts[0]
        if len(parts) == 2 and t in type_defs_sorted and type_defs_sorted[t].typClass == 'enum':
            symLine = '// ' + symLine
        symbolLines.append(symLine)
    
    with open(outLoc, 'w') as f:
        f.write('#include "../common.h"\n\n')
        
        f.write('\n'.join('struct %s;' % n for n,t in type_defs_sorted.items() if t.typClass == 'struct'))
        f.write('\n\n')
        f.write('\n'.join(c.typDef for c in typeLines))
        f.write('\n\n')
        f.write('namespace SymbolsNamespace {\n')
        f.write('\n'.join(c for c in symbolLines))
        f.write('\n\n}')

def gen_ctypes(hdrLoc, outLoc):
    outCpp = hdrLoc.replace('.h', '.cpp')
    rewrite_ida_header(hdrLoc, outCpp)
    out = subprocess.check_output(['clang2py', '--verbose', outCpp], encoding='utf-8')
    wraps, sep, defs = out.partition("_libraries = {}\n_libraries['FIXME_STUB'] = FunctionFactoryStub() #  ctypes.CDLL('FIXME_STUB')\n")
    def_patched = defs.replace('\n', '\n    ').replace('ctypes.POINTER(ctypes.c_char)', 'ctypes.c_char_p')
    newdef = '\n\n'
    newdef += 'def ctypeslib_define():'
    newdef += def_patched
    newdef += '\n    return locals()'
    newdef += '\n'
    with open(outLoc, 'w') as f:
        f.write(wraps + sep + newdef)


def main(args):
    if not args:
        gen_ctypes('idasdk_win/idasdk_win.h', 'idasdk_win/idasdk_win.py')
    else:
        gen_ctypes(args[0], args[1])

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])