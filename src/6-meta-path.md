# Découvrir des modules ailleurs que dans les fichiers

## Découvrir des modules ailleurs que dans les fichiers

- On a jusqu'ici utilisé `FileFinder` pour découvrir nos modules
- Celui-ci s'appuie sur des répertoires (ou apparentés) sur le système de fichiers pour les localiser
    - Ils reposent pour cela sur `PathEntryFinder`

---

- Mais il est possible d'imaginer d'autres manières de découvrir des modules

## Meta-path

- `sys.meta_path` liste les _meta finders_ utilisés par Python pour rechercher un module
    - Ceux-ci implémentent l'interface de `MetaPathFinder`
    - Très proche de `PathEntryFinder`, elle demande une méthode `find_spec` recevant le nom du module et son chemin

```python
sys.meta_path
```

---

- On remarque que `PathFinder` (et donc les mécanismes liés à `sys.path` et `sys.meta_path`) est lui aussi une entrée _meta path_

## Imports installables

- On peut imaginer un mécanisme d'import s'assurant qu'un paquet est installé
- Pour cela le _finder_ peut faire appel à `pip` afin d'installer un paquet manquant

---

```python
import subprocess


class PipFinder(importlib.abc.MetaPathFinder):
    def __init__(self, *allowed_modules):
        self.allowed_modules = set(allowed_modules)

    def find_spec(self, fullname, path, target=None):
        if fullname not in self.allowed_modules:
            return None

        subprocess.run(['pip', 'install', fullname])

        return importlib.util.find_spec(fullname)
```

## Imports installables

- On ajoute ensuite le _finder_ au _meta-path_ pour le rendre accessible

```python
sys.meta_path.append(PipFinder('requests'))

import requests
print(requests.get('https://pycon.fr'))
```

## Imports réseau

- Si on s'abstrait du système de fichiers, on peut aussi envisager des imports via le réseau
- En disposant par exemple d'un serveur HTTP exposant des modules

---

```python
import http.server
import threading


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

## Imports réseau

- Que l'on lancerait ici dans un _thread_ dédié, mais qu'on pourrait imaginer sur un serveur distant (RPC)

```python
server = http.server.HTTPServer(('', 8080), ServerHandler)
thr = threading.Thread(target=server.serve_forever)
thr.start()
```

## Imports réseau

- On utilise alors un _finder_ simple s'appuyant sur un _loader_ pour la partie réseau

```python
class NetworkFinder(importlib.abc.MetaPathFinder):
    def __init__(self, baseurl):
        self.loader = NetworkLoader(baseurl)

    def find_spec(self, fullname, path, target=None):
        if self.loader.exists(fullname):
            return importlib.util.spec_from_loader(fullname, self.loader)
```

## Imports réseau

- Le _loader_ interroge le serveur configuré pour obtenir le code source des modules

```python
import urllib


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

## Imports réseau

- Il suffit alors de créer une entrée pour notre serveur précédemment instancié

```python
sys.meta_path.append(NetworkFinder('http://localhost:8080'))

import remote
remote.test()
```

## Imports dynamiques

- Enfin on peut exploiter le mécanisme des _loaders_ pour charger le code du module à la volée
- Par exemple un module qui définirait ses attributs en fonction de son nom

```python
class DynamicFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname.startswith('dynamic__'):
            parts = fullname.split('__')[1:]
            attributes = dict(part.split('_') for part in parts)
            return importlib.util.spec_from_loader(
                fullname,
                DynamicLoader(attributes)
            )
```

## Imports dynamiques

- Avec le _loader_ associé

```python
class DynamicLoader(importlib.abc.Loader):
    def __init__(self, attributes):
        self.attributes = attributes

    def exec_module(self, module):
        module.__dict__.update(self.attributes)
```

```python
sys.meta_path.append(DynamicFinder())

import dynamic__foo_bar__toto_tata as mod
print(mod)
print(mod.foo)
print(mod.toto)
```

## Autres exemples

- L'ensemble des exemples précédents (_path hooks_, extensions particulières) peuvent être réécrits à l'aide de _meta finders_
    - Mais ils nécessitent alors que chaque élément se charge de parcourir `sys.path` pour itérer sur les répertoires
- On peut aussi imaginer d'autres manières de générer du code à la volée
    - Import _copilot_ : <https://pypi.org/project/copilot-import/>
