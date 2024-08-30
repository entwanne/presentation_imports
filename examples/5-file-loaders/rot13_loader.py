import codecs
import importlib.abc
import sys
from importlib.machinery import FileFinder, SourceFileLoader


class Rot13Loader(importlib.abc.FileLoader):
    def get_source(self, fullname):
        data = self.get_data(self.get_filename(fullname))
        return codecs.encode(data.decode(), 'rot_13')


path_hook = FileFinder.path_hook(
    (SourceFileLoader, ['.py']),
    (Rot13Loader, ['.pyr']),
)
sys.path_hooks.insert(0, path_hook)
sys.path_importer_cache.clear()

import secret
print(secret.toto())
import secret2
print(secret2.toto())

sys.path_hooks.remove(path_hook)
sys.path_importer_cache.clear()
