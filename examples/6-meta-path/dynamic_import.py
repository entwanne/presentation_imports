import importlib
import importlib.abc
import importlib.util
import sys


class DynamicLoader(importlib.abc.Loader):
    def __init__(self, attributes):
        self.attributes = attributes

    def exec_module(self, module):
        module.__dict__.update(self.attributes)


class DynamicFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith('dynamic__'):
            parts = fullname.split('__')[1:]
            attributes = dict(part.split('_') for part in parts)
            return importlib.util.spec_from_loader(
                fullname,
                DynamicLoader(attributes)
            )

sys.meta_path.append(DynamicFinder())

import dynamic__foo_bar__toto_tata as mod
print(mod)
print(mod.foo)
print(mod.toto)
