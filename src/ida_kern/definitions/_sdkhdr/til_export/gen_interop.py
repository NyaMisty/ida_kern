# Generate inter-op wrappers of ctypes structs we used
import re
import subprocess

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

def rewrite_ida_header(hdrLoc, outLoc):
    with open(hdrLoc, 'r') as f:
        content = f.read()
    
    # remove vft
    content = re.sub(r'struct /\*VFT\*/ (.*?_vtbl\n{\n[\S\s]+?\n};\n)', '/*struct \\1*/\n', content)
    
    BLACKLIST = ['procmod_t', '__m128i']

    for strucName in BLACKLIST:
        content = re.sub(r'(\n(struct|enum|union) .*?' + strucName + '.*?\n{\n[\s\S]+?\n};\n)', '/*\\1*/\n', content)

    TYPEDEF_BLACKLIST = ['_Mbstatet']
    for typeName in TYPEDEF_BLACKLIST:
        content = re.sub(r'\n(typedef .*? ' + typeName + ';)\n', '\n//\\1\n', content)

    # remove coments
    #content = remove_comments(content)
    
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
    
    content = content.replace('~', '_del_')
    
    replaceList = []
    
    identifier = r'\w\d_'
    typename = r'[%s][%s<>_ ,*]+?[%s>]' % (identifier, identifier, identifier)

    for strucName in re.findall(r'\nstruct (%s);\n' % typename, content):
        replaceList.append((strucName, cleanName(strucName)))
    
    for strucName in re.findall(r'\n  struct (%s) \*[a-zA-Z_]+?;\n' % typename, content):
        replaceList.append((strucName, cleanName(strucName)))
    
    #for strucName, _, strucBase in re.findall(r'struct __cppobj (.*?)( : (.*?)|)\n', content):
    for _, _, _, _, strucName, _, strucBase in re.findall(r'\nstruct( __[^ ]+?|)( __[^ ]+?|)( __[^ ]+?|)( __[^ ]+?|) (%s)( : (%s)|)\n' % (typename, typename), content):
        replaceList.append((strucName, cleanName(strucName)))
        replaceList.append((strucBase, cleanName(strucBase)))
    
    templateArg = r'[^<>]*?'
    templatePat = []
    def genTemplatePat(level):
        if level == 1:
            ret = r'<(%s)>' % templateArg
            templatePat.append(ret)
        else:
            genTemplatePat(level - 1)
            for pat in templatePat[:]:
                ret = r'<(%s%s+?%s)+?>' % (templateArg, '(%s)' % '|'.join(templatePat), templateArg)
                templatePat.append(ret)

        return
    
    genTemplatePat(4)
    
    for pat in templatePat:
        for match in re.finditer(pat, content):
            tmplArg = match.group(0)
            if tmplArg == '*':
                print(pat, match)
                sys.exit(1)
            replaceList.append((tmplArg, cleanName(tmplArg)))

    
    content = content.replace('\nconst struct', '\nstruct')
    
    #for strucName in re.findall(r'^typedef struct (.*?);\n', content):
    #    replaceList.append((strucName, cleanName(strucName)))
    
    replaceList = list(set(replaceList))
    replaceList.sort(key=lambda x: len(x[0]), reverse=True)
    
    for a, b in replaceList[:]:
        print(a, b)
        content = content.replace(a, b)
        if 'struct_std__nested_exception_vtbl' in content:
            break
    
    content = re.sub(r'\nenum ([%s]+?) : __int32\n' % identifier, '\nenum \\1 : unsigned __int32\n', content)
    
    with open(outLoc, 'w') as f:
        f.write('#include "../common.h"\n\n')
        f.write(content)

def gen_ctypes(hdrLoc, outLoc):
    outCpp = hdrLoc.replace('.h', '.cpp')
    rewrite_ida_header(hdrLoc, outCpp)
    out = subprocess.check_output(['clang2py', '--verbose', outCpp])
    with open(outLoc, 'wb') as f:
        f.write(out)


def main():
    import sys
    gen_ctypes('_ida64_win/idasdk.h', '_ida64_win/_idasdk.py')

if __name__ == '__main__':
    main()