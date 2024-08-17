import importlib
import importlib.abc
import importlib.util
import sys


class DummyLoader(importlib.abc.Loader):
    def exec_module(self, module):
        module.foo = 'bar'


class DummyPathFinder(importlib.abc.PathEntryFinder):
    def __init__(self, dirpath):
        pass

    def find_spec(self, fullname, target=None):
        if fullname == 'pouet':
            return importlib.util.spec_from_loader(fullname, DummyLoader())


class DummyMetaFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == 'metapouet':
            return importlib.util.spec_from_loader(fullname, DummyLoader())

sys.path_hooks.insert(0, DummyPathFinder)
sys.path_importer_cache.clear()
sys.meta_path.append(DummyMetaFinder())

import pouet
print(pouet)
print(pouet.foo)
print(pouet.__spec__)

import metapouet
print(metapouet)
print(metapouet.foo)
print(metapouet.__spec__)
