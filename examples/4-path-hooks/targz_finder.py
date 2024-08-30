import importlib
import importlib.abc
import importlib.util
import sys
import tarfile


class ArchiveFinder(importlib.abc.PathEntryFinder):
    def __init__(self, path):
        self.loader = ArchiveLoader(path)

    def find_spec(self, fullname, path):
        if fullname in self.loader.filenames:
            return importlib.util.spec_from_loader(fullname, self.loader)


class ArchiveLoader(importlib.abc.SourceLoader):
    def __init__(self, path):
        self.archive = tarfile.open(path, mode='r:gz')
        self.filenames = {
            name.removesuffix('.py'): name
            for name in self.archive.getnames()
            if name.endswith('.py')
        }

    def get_data(self, name):
        member = self.archive.getmember(name)
        fobj = self.archive.extractfile(member)
        return fobj.read().decode()

    def get_filename(self, name):
        return self.filenames[name]


def archive_path_hook(archive_path):
    if archive_path.endswith('.tar.gz'):
        return ArchiveFinder(archive_path)
    raise ImportError


sys.path_hooks.append(archive_path_hook)
sys.path.append('packages.tar.gz')
sys.path_importer_cache.clear()


import tar_example
tar_example.hello('PyConFR')
