# Découverte et chargement de modules

## Découverte et chargement de modules

- Python utilise des _finders_ pour découvrir les modules et des _loaders_ pour les charger
- `sys.path_hooks` est une liste de callables créant un _finder_ pour chaque entrée de `sys.path`

```python
sys.path_hooks
```

## Découverte et chargement de modules

- Un _finder_ est un objet possédant une méthode `find_spec`
    - Cette méthode prend en argument le nom complet du module
    - Elle renvoie une « spécification de module » (`ModuleSpec`), ou `None` si le module n'est pas trouvé

```python
finder = sys.path_hooks[-1]('.') # Finder sur le répertoire courant
finder.find_spec('my_module')
```

```python
finder.find_spec('not_found')
```

## Découverte et chargement de modules

- La spécification contient des attributs décrivant le module (`name`, `origin`)

```python
spec = finder.find_spec('my_module')
spec.name, spec.origin
```

- et un attribut `loader` renvoyant le _loader_ associé à ce type de fichier

```python
spec.loader
```

## Découverte et chargement de modules

- On peut initialiser un module vide à partir de la spec
    - cela utilise la méthode `create_module` du _loader_ si elle est définie

```python
import importlib.util

module = importlib.util.module_from_spec(spec)
module.__dict__.keys()
```
- Et charger le module via la méthode `exec_module` du _loader_

```python
spec.loader.exec_module(module)
module.__dict__.keys()
```

```python
>>> module.my_function()
```

## Découverte et chargement de modules

- Python propose des utilitaires pour gérer différents types de _finders_ et _loaders_
- `PathEntryFinder` est un _finder_ dédié pour les entrées de `sys.path`

- `SourceLoader` est un _loader_ offrant de facilités pour importer un fichier source
    - Un _source loader_ a juste à implémenter des méthodes `get_filename` et `get_data` (qui renvoie le contenu du module sous forme de _bytes_)

## Importer des `.tar.gz`

- On peut par exemple ajouter un _loader_ pour gérer les archives `.tar.gz`
    - fonctionnant sur le même principe que l'import d'archives `.zip`

```shell
%%sh
tar -xzvOf packages.tar.gz
```

```python
sys.path.append('packages.tar.gz')

import tar_example
tar_example.hello('PyConFR')
```

## Importer des `.tar.gz`

- Le _finder_ est un `PathEntryFinder` classique

```python
import importlib.abc
import tarfile


class ArchiveFinder(importlib.abc.PathEntryFinder):
    def __init__(self, path):
        self.loader = ArchiveLoader(path)

    def find_spec(self, fullname, target=None):
        if fullname in self.loader.filenames:
            return importlib.util.spec_from_loader(fullname, self.loader)
```

## Importer des `.tar.gz`

- Le _loader_ s'occupe d'ouvrir l'archive, de localiser le module et d'en renvoyer la source

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
        return fobj.read()

    def get_filename(self, name):
        return self.filenames[name]
```

## Importer des `.tar.gz`

- Il suffit ensuite de le brancher aux `sys.path_hooks`
- Python garde en cache les _hooks_ existants et il faut donc penser à nettoyer le cache

```python
def archive_path_hook(archive_path):
    if archive_path.endswith('.tar.gz'):
        return ArchiveFinder(archive_path)
    raise ImportError

sys.path_hooks.append(archive_path_hook)
sys.path_importer_cache.clear()
```

```python
import tar_example
tar_example.hello('PyConFR')
```

## Autres exemples

- On peut imaginer d'autres exemples de _path hooks_
    - Import depuis tout type d'archive, ou tout ce qui prend la forme d'une collection de fichiers
    - Import depuis le réseau (on y reviendra plus tard)
