import importlib
import importlib.abc
import importlib.util
import pathlib
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
            case _:
                yield from stack
                stack.clear()
                yield token


class BetterPythonLoader(importlib.abc.SourceLoader):
    def __init__(self, basepath):
        self.basepath = basepath

    def get_path(self, fullname):
        return (self.basepath / fullname).with_suffix('.bpy')

    def get_data(self, path):
        with open(path, 'rb') as f:
            tokens = list(tokenize.tokenize(f.readline))
        tokens = transform(tokens)
        return tokenize.untokenize(tokens)

    def get_filename(self, name):
        return str(self.get_path(name))


class BetterPythonFinder(importlib.abc.PathEntryFinder):
    def __init__(self, dirpath, default_finder=None):
        self.path = pathlib.Path(dirpath)
        self.loader = BetterPythonLoader(self.path)
        self.default_finder = default_finder

    def find_spec(self, fullname, path):
        path = self.loader.get_path(fullname)
        if path.exists():
            return importlib.util.spec_from_loader(fullname, self.loader)
        if self.default_finder:
            return self.default_finder.find_spec(fullname, path)


filefinder_path_hook = sys.path_hooks[1]


def bpython_path_hook(dirpath):
    default_finder = filefinder_path_hook(dirpath)
    return BetterPythonFinder(dirpath, default_finder)


sys.path_hooks[1] = bpython_path_hook
sys.path_importer_cache.clear()

import increment
increment.test(4)
