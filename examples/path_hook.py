import codecs
import importlib
import importlib.abc
import importlib.util
import pathlib
import sys


class Rot13Loader(importlib.abc.Loader):
    def __init__(self, path):
        self.path = path

    def exec_module(self, module):
        content = self.path.read_text()
        content = codecs.encode(content, 'rot_13')
        exec(content, module.__dict__)


class Rot13Finder(importlib.abc.PathEntryFinder):
    def __init__(self, dirpath, default_finder=None):
        self.path = pathlib.Path(dirpath)
        self.default_finder = default_finder

    def find_spec(self, fullname, path):
        path = (self.path / fullname).with_suffix('.pyr')
        if path.exists():
            return importlib.util.spec_from_loader(fullname, Rot13Loader(path))
        if self.default_finder:
            return self.default_finder.find_spec(fullname, path)


filefinder_path_hook = sys.path_hooks[1]


def rot13_path_hook(dirpath):
    default_finder = filefinder_path_hook(dirpath)
    return Rot13Finder(dirpath, default_finder)


sys.path_hooks[1] = rot13_path_hook
sys.path_importer_cache.clear()

import secret
print(secret.toto())
import secret2
print(secret2.toto())
