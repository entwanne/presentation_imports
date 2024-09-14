# Système de cache

## Système de cache

- Comme indiqué précédemment, le module importé est mise en cache
- Cela lui évite d'être rechargé / ré-exécuté à chaque import

---

- Ce cache est accessible via `sys.modules`

```python
import sys
sys.modules
```

## Système de cache

- `import_module` stocke aussi son résultat dans le cache
- Changer le code d'un module à la volée ne permet alors pas de le réimporter

```python
```

---

- À moins d'utiliser `importlib.reload`

```python
```

## Système de cache

- Vérification de la présence du module dans le cache `sys.modules`
- Nettoyer / falsifier le cache
    - `del sys.modules[...]`
    - `importlib.reload`
    - `sys.modules[...] = ...`

## Système de cache

- Dans le cadre de la présentation, le cache est nettoyé après chaque bloc de code
