# Qu'est-ce qu'un import ?

## Qu'est-ce qu'un import ?

- Que se passe-t-il quand on fait un `import my_module` ?

```python
import my_module
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

## Import de paquets et sous-modules

- Résolution/import des paquets parents
    - `import abc.def.ghi` -> `import abc` + `import abc.def` + `import abc.def.ghi`
    - Exécution des modules `__init__` de chaque paquet

- Imports relatifs dans des paquets

## Étapes de l'import

- Résolution du nom
    - Pour résoudre les imports relatifs
    - `importlib.util.resolve_name`
- Imports des paquets parents
- Chargement du module
- Stockage dans le cache
- Exécution du code du module

## Conseils

- Différence `import abc` / `import abc.def` / `from abc import def`
    - imports circulaires
