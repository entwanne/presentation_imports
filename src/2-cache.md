# Système de cache

## Système de cache

- Mais recharger / réexécuter le module à chaque import serait coûteux
- Python utilise alors un cache pour se souvenir des modules précédemment importés
- L'import d'un module déjà présent dans le cache peut alors court-circuiter toute la procédure d'import

---

- `import_module` stocke aussi son résultat dans le cache
- Ce cache est accessible via `sys.modules`

```python
import sys
sys.modules
```

## Système de cache

- Changer le code d'un module à la volée ne permet alors pas de le réimporter
- À moins d'utiliser `importlib.reload`

```python
%%writefile rewrite.py
def version():
    return 1
```

```python
import rewrite
print('before', rewrite.version())

with open('rewrite.py', 'w') as f:
    print("def version():\n    return 2", file=f)

import rewrite
print('after', rewrite.version())

importlib.reload(rewrite)
print('reload', rewrite.version())
```

## Système de cache

- Ce système de cache nous permet aussi de :
    - Simplement vérifier qu'un module a déjà été importé
        - En vérifiant s'il existe dans `sys.modules`
    - Nettoyer et/ou falsifier le cache en ajoutant des modules à la volée

        ```python
        del sys.modules[...]
        importlib.reload(...)
        sys.modules[...] = ...
        ```

## Système de cache

- Dans le cadre de la présentation, le cache est nettoyé après chaque bloc de code
