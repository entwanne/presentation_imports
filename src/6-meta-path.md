# Découvrir des modules ailleurs que dans les fichiers

## Découvrir des modules ailleurs que dans les fichiers

- Autres finders dans `sys.meta_path`
- `MetaPathFinder`
- Exemples :
    - Les exemples précédents peuvent être réécrits à l'aide d'une entrée dans le meta_path
        - Nécessitant alors de reparcourir les répertoires de sys.path
    - Création de modules à la volée (nom du module qui correspond lui-même à des instructions)
    - Importer des modules depuis le réseau (HTTP, RPC)
    - Recherche & installation de modules sur pip

## Étendre la syntaxe Python

```python
%%writefile increment.bpy
def test(x=0):
    for _ in range(10):
        print(x++)
```

```python
from increment import test
test(1)
```

## Étendre la syntaxe Python

```python
import importlib
import importlib.abc
import importlib.util
import pathlib
import sys
import tokenize
```

## Étendre la syntaxe Python

```python
def transform(tokens):
    stack = []
    for token in tokens:
        match token.type:
            case tokenize.NAME if not stack:
                stack.append(token)
            case tokenize.OP if stack and token.string == '+':
                if len(stack) < 2:
                    stack.append(token)
                else:
                    yield from increment_token(token, stack)
            case _:
                yield from stack
                stack.clear()
                yield token
```

## Étendre la syntaxe Python

```python
def increment_token(token, stack):
    name_token = stack.pop(0)
    stack.clear()

    start = name_token.start
    end = token.end
    line = name_token.line

    yield tokenize.TokenInfo(type=tokenize.OP, string='(', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=':=', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NAME, string=name_token.string, start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string='+', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.NUMBER, string='1', start=start, end=start, line=line)
    yield tokenize.TokenInfo(type=tokenize.OP, string=')', start=start, end=end, line=line)
```

## Étendre la syntaxe Python

```python
class BetterPythonLoader(importlib.abc.FileLoader):
    def __init__(self, basepath):
        self.basepath = pathlib.Path(basepath)

    def _get_path(self, fullname):
        return (self.basepath / fullname).with_suffix('.bpy')

    def get_data(self, path):
        with open(path, 'rb') as f:
            tokens = list(tokenize.tokenize(f.readline))
        tokens = transform(tokens)
        return tokenize.untokenize(tokens)

    def get_filename(self, name):
        return str(self._get_path(name))
```

## Étendre la syntaxe Python

```python
class BetterPythonFinder(importlib.abc.PathEntryFinder):
    def __init__(self):
        self.loaders = [BetterPythonLoader(basepath) for basepath in sys.path]

    def find_spec(self, fullname, path, target=None):
        for loader in self.loaders:
            path = loader.get_path(fullname)
            if path.exists():
                return importlib.util.spec_from_loader(fullname, loader)
```

## Étendre la syntaxe Python

```python
sys.meta_path.append(BetterPythonFinder())
```

## Étendre la syntaxe Python

```python
from increment import test
test(1)
```
