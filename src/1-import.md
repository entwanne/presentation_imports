# Qu'est-ce qu'un import ?

## Qu'est-ce qu'un import ?

- Que se passe-t-il quand on fait un `import my_module` ?

```python
import my_module
my_module
```

---

- Cela équivaut à un appel à la fonction `__import__` avec le nom du module en argument
- Dont le retour est stocké dans le nom indiqué

```python
my_module = __import__('my_module')
my_module
```

## `importlib`

- L'usage de la fonction `__import__` est cependant découragé
- `import_module` d'`importlib` offre une interface plus claire, notamment dans le cas de paquets
- On préférera alors cette fonction pour un « import programmatique »

```python
import importlib

my_module = importlib.import_module('my_module')
my_module
```

## Exécution du module

- L'import ne fait pas que charger le module
- Il en exécute aussi le contenu

---

```python
%%writefile my_other_module.py
print('Coucou')
```

```python
import my_other_module
```

## Import de paquets et sous-modules

- Le mécanisme d'import se charge de résoudre et d'importer les paquets parents
    - Ainsi importer `foo.spam.eggs` équivaut à importer `foo` puis `foo.spam` et enfin `foo.spam.eggs`
    - Le module `__init__` de chaque paquet est chargé et exécuté

## Import de paquets et sous-modules

- Par exemple ici avec une hiérarchie sur 3 niveaux

```python
%%writefile foo/__init__.py
print('Import foo')
```

```python
%%writefile foo/spam/__init__.py
print('Import foo.spam')
```

```python
%%writefile foo/spam/eggs.py
print('Import foo.spam.eggs')
```

```python
import foo.spam.eggs
```

## Import de paquets et sous-modules

- Les imports relatifs (`.`, `..`, etc.) sont aussi résolus par ce mécanisme

---

```python
%%writefile foo/spam/increment.py
def increment(x):
    return x + 1
```

```python
%%writefile foo/spam/relative.py
from .increment import increment

print(increment(5))
```

```python
import foo.spam.relative
```

## Étapes de l'import

- Pour résumer, l'import se déroule en plusieurs étapes :
    1. Résolution du nom
        - Pour résoudre les imports relatifs
        - `importlib.util.resolve_name`
    2. Imports récursifs des paquets parents
    3. Chargement du module
    4. Exécution du code du module
