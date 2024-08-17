Voyage au cœur du mécanisme des imports en Python afin de comprendre comment ils fonctionnent et comment nous pouvons agir sur leur comportement, à travers l'écriture de _finders_ et de _loaders_ personnalisés.

Il s'agirait de passer en revue :
- `__import__` / `importlib.import_module`
- `sys.modules`
- `sys.path`
- `sys.path_hooks`
- `sys.meta_path`

Avec différents exemples :
- Importer des modules Python-ROT13
- Importer des modules depuis le réseau
- Importer des modules écrits en brainfuck
- Étendre la grammaire de Python
