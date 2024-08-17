import codecs
import importlib
import importlib.abc
import importlib.util
import pathlib
import sys


class Rot13Loader(importlib.abc.SourceLoader):
    def __init__(self, basepath):
        self.basepath = basepath

    def get_path(self, fullname):
        return (self.basepath / fullname).with_suffix('.pyr')

    def get_data(self, path):
        with open(path) as f:
            content = f.read()
            return codecs.encode(content, 'rot_13')

    def get_filename(self, name):
        return str(self.get_path(name))


class Rot13Finder(importlib.abc.PathEntryFinder):
    def __init__(self, dirpath, default_finder=None):
        self.path = pathlib.Path(dirpath)
        self.loader = Rot13Loader(self.path)
        self.default_finder = default_finder

    def find_spec(self, fullname, path):
        path = self.loader.get_path(fullname)
        if path.exists():
            return importlib.util.spec_from_loader(fullname, self.loader)
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
