#!/usr/bin/env python3
"""Writes jem_sync_task.py: the copy of jem_sync.py embedded in the scheduled task's prompt (limit 64 KB).
It drops comments, docstrings and the in-session-only commands (approve, relink). Run after every change to jem_sync.py,
then put jem_sync_task.py in the task prompt with its MD5 (see README)."""
import ast, hashlib, io, os, re, tokenize
here = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(here, 'jem_sync.py'), encoding='utf-8').read()
src = re.sub(r'# >>> in-session only.*?# <<< in-session only\n', '', src, flags=re.S)
lines = src.split('\n')
# blank out docstrings (module and function), then comments
for node in ast.walk(ast.parse(src)):
    if isinstance(node, (ast.Module, ast.FunctionDef)) and node.body and isinstance(node.body[0], ast.Expr) \
            and isinstance(getattr(node.body[0], 'value', None), ast.Constant) and isinstance(node.body[0].value.value, str):
        d = node.body[0]
        for i in range(d.lineno - 1, d.end_lineno): lines[i] = ''
src = '\n'.join(lines)
chars = [list(l) for l in src.split('\n')]
for t in tokenize.generate_tokens(io.StringIO(src).readline):
    if t.type == tokenize.COMMENT:
        (r, c), (_, c2) = t.start, t.end
        for i in range(c, c2): chars[r - 1][i] = ''
out = [''.join(l).rstrip() for l in chars]
out = [l for l in out if l.strip()]
code = '\n'.join(out) + '\n'
compile(code, 'jem_sync_task.py', 'exec')
open(os.path.join(here, 'jem_sync_task.py'), 'w', encoding='utf-8').write(code)
print(f'jem_sync_task.py: {len(code.encode())} bytes, md5 {hashlib.md5(code.encode()).hexdigest()}')
