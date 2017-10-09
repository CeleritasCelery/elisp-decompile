"""Scanner for ELISP decompiler

We take input from ELISP disassembly
"""
import re
from eldecompile.tok import Token
from collections import namedtuple

FuncDef = namedtuple('FuncDef', ['name', 'args', 'opt_args',
                                 'docstring', 'interactive', 'fn_type'])

def fn_scanner(fp, show_tokens=False):
    tokens = []
    lines = fp.readlines()
    line = lines[0]
    fn_type = 'defun'
    interactive = None
    m = re.match("^byte code for macro (\S+):$", line)
    if m:
        fn_type = 'defmacro'
        name = m.group(1)
    else:
        m = re.match("^byte code for (\S+):$", line)
        if m:
            name = m.group(1)
        elif re.match("^byte code:$", line):
            fn_type = 'file'
            name = None
        else:
            name = 'unknown'

    line = lines[1]
    if line.startswith('  doc:  '):
        docstring = '\n  "%s"\n' % line[len('  doc:  '):].rstrip("\n")
        start_adjust = 1
    elif line.startswith('  doc-start '):
        m = re.match('^  doc-start (\d+):  (.*)$', line)
        if m:
            tot_len = int(m.group(1))
            docstring = '\n  "' + m.group(2) + '\n'
            l = len(m.group(2))
            start_adjust = 1
            while l < tot_len:
                line = lines[1 + start_adjust]
                l += len(line)
                docstring += line
                start_adjust += 1
                pass
            docstring = docstring.rstrip("\n")
            docstring += '"'
            pass
    else:
        docstring = ''
        start_adjust = 0

    line = lines[1+start_adjust]
    m = re.match("^  args: (\([^)]*\))", line)
    if m:
        args = m.group(1)
    elif re.match("^  args: nil", line):
        args = '()'
    else:
        args = '(?)'
    start_adjust += 1

    line = lines[1+start_adjust]
    if line.startswith(' interactive: '):
        interactive = line[len(' interactive: '):].rstrip("\n")
        start_adjust += 1
        line = lines[1+start_adjust]

    fn_def = FuncDef(name, args, None, docstring,
                     interactive, fn_type)
    customize = {}

    for i, line in enumerate(lines[1+start_adjust:]):
        fields = line.split()
        offset = fields[0]
        colon_point = offset.find(':')
        if colon_point >= 0:
            label = offset[colon_point:]
            offset = offset[:colon_point]
            tokens.append(Token('LABEL', label, offset))
        offset, opname = fields[:2]
        if opname == 'constant':
            attr = line[line.index(' '):].strip()
            tokens.append(Token('CONSTANT', attr, offset.strip()))
        elif opname[:-1] in ('list', 'concat', 'cal'):
            if opname.startswith('call'):
                count = int(fields[2]) + 1
                opname = "%s_%d" % (opname, count)
            elif opname[-1] == 'N':
                count = int(fields[2])
                opname = "%s_%d" % (opname, count)
            else:
                count = int(opname[-1])
                opname = "%s_%d" % (opname[:-1], count)
            opname = opname.upper().strip()
            tokens.append(Token(opname, count, offset.strip()))
            customize[opname] = int(count)
        elif len(fields) == 3:
            offset, opname, attr = fields
            tokens.append(Token(opname.upper().strip(), attr.strip(),
                                offset.strip()))
        elif len(fields) == 2:
            offset, opname = fields
            tokens.append(Token(opname.upper().strip(), None, offset.strip()))
            pass
        else:
            print("Can't handle line %d:\n\t%s" % (i, line))
        pass

    if show_tokens:
        print('\n'.join([str(t) for t in tokens]))
    return fn_def, tokens, customize
