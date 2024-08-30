import atexit
import importlib
import importlib.abc
import importlib.util
import subprocess
import sys


class PipFinder(importlib.abc.MetaPathFinder):
    def __init__(self, *allowed_modules):
        self.allowed_modules = set(allowed_modules)

    def find_spec(self, fullname, path, target=None):
        if fullname not in self.allowed_modules:
            return None

        subprocess.run(['pip', 'install', fullname])
        atexit.register(subprocess.run, ['pip', 'uninstall', fullname])

        return importlib.util.find_spec(fullname)


sys.meta_path.append(PipFinder('requests'))

import requests
print(requests.get('https://pycon.fr'))
