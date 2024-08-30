import importlib.abc
import importlib.machinery
import sys
import tokenize


def transform(tokens):
    stack = []
    for token in tokens:
        match token.type:
            case tokenize.NAME if not stack:
                stack.append(token)
            case tokenize.OP if stack and token.string == '+':
                if len(stack) < 2:
                    stack.append(token)
                else:
                    yield from increment_token(token, stack)
            case _:
                yield from stack
                stack.clear()
                yield token


def increment_token(token, stack):
    name_token = stack.pop(0)
    stack.clear()

    start = name_token.start
    end = token.end
    line = name_token.line

    yield tokenize.TokenInfo(type=tokenize.OP, string='(', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=':=', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string='+', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NUMBER, string='1', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=')', start=start, end=end, line=line)


class BetterPythonLoader(importlib.abc.FileLoader):
    def get_source(self, fullname):
        path = self.get_filename(fullname)
        with open(path, 'rb') as f:
            tokens = list(tokenize.tokenize(f.readline))
        tokens = transform(tokens)
        return tokenize.untokenize(tokens)


path_hook = importlib.machinery.FileFinder.path_hook(
    (importlib.machinery.SourceFileLoader, ['.py']),
    (BetterPythonLoader, ['.bpy']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()

import increment
increment.test(4)

sys.path_hooks.remove(path_hook)
sys.path_importer_cache.clear()
