# Découverte et chargement de modules

## Découverte et chargement de modules

- Mécanisme des finders et loaders
- `sys.path_hooks` pour ajouter de nouveaux finders
- principe des finders et loaders
    - méthodes requires
    - `SourceLoader` / `PathEntryFinder`
- Exemples :
    - Charger du code depuis une archive `.tar.gz`

## Découverte et chargement de modules

- `sys.path` ne contient pas que des répertoires
- Chaque entrée est associée à un _path hook_
- Un _path hook_ est présent pour les répertoires, un autre pour les archives .zip

## Importer des `.tar.gz`

- Similaire à l'import de zip

```shell
%%sh
tar -xzvOf packages.tar.gz
```

```python
import tar_example
tar_example.hello('PyConFR')
```

```python
import importlib
import importlib.abc
import importlib.util
import sys
import tarfile
```

```python
class ArchiveFinder(importlib.abc.PathEntryFinder):
    def __init__(self, path):
        self.loader = ArchiveLoader(path)

    def find_spec(self, fullname, path):
        if fullname in self.loader.filenames:
            return importlib.util.spec_from_loader(fullname, self.loader)
```

```python
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
```

```python
def archive_path_hook(archive_path):
    if archive_path.endswith('.tar.gz'):
        return ArchiveFinder(archive_path)
    raise ImportError

sys.path_hooks.append(archive_path_hook)
sys.path.append('packages.tar.gz')
sys.path_importer_cache.clear()
```

```python
import tar_example
tar_example.hello('PyConFR')
```

## Importer des modules distants

```python
import remote
remote.test()
```

```python
import codecs
import http.client
import http.server
import importlib
import importlib.abc
import importlib.util
import sys
import threading
import urllib.request
```

```python
class ServerHandler(http.server.BaseHTTPRequestHandler):
    files = {
        'remote.py': b'def test():\n    print("Hello")'
    }

    def do_GET(self):
        filename = self.path[1:]
        content = self.files.get(filename)
        if content is None:
            self.send_error(404)
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(content)

    def do_HEAD(self):
        filename = self.path[1:]
        if filename in self.files:
            self.send_response(200)
            self.end_headers()
        else:
            self.send_error(404)
```

```python
server = http.server.HTTPServer(('', 8080), ServerHandler)
thr = threading.Thread(target=server.serve_forever)
thr.start()
```

```python
class NetworkLoader(importlib.abc.SourceLoader):
    def __init__(self, baseurl):
        self.baseurl = baseurl

    def get_url(self, fullname):
        return f'{self.baseurl}/{fullname}.py'

    def get_data(self, url):
        with urllib.request.urlopen(url) as f:
            return f.read()

    def get_filename(self, name):
        return f'{self.get_url(name)}'

    def exists(self, name):
        req = urllib.request.Request(self.get_url(name), method='HEAD')
        try:
            with urllib.request.urlopen(req) as f:
                pass
        except:
            return False
        return f.status == 200
```

```python
class NetworkFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self.loader = NetworkLoader(baseurl)

    def find_spec(self, fullname, path, target=None):
        if self.loader.exists(fullname):
            return importlib.util.spec_from_loader(fullname, self.loader)
```

```python
def network_path_hook(path):
    if path.startswith('http://') or path.startswith('https://'):
        return NetworkFinder(path)
    raise ImportError

sys.path_hooks.append(network_path_hook)
sys.path.append('http://localhost:8080')
sys.path_importer_cache.clear()
```

```python
import remote
remote.test()
```

```python
sys.path_hooks.remove(network_path_hook)
sys.path_importer_cache.clear()
server.shutdown()
thr.join()
```
