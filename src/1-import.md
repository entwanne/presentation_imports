# Qu'est-ce qu'un import

## Qu'est-ce qu'un import

- Que se passe-t-il quand on fait un `import foo`
- `__import__` / `importlib.import_module`

- Résolution/import des paquets parents
    - `import abc.def.ghi` -> `import abc` + `import abc.def` + `import abc.def.ghi`
    - Exécution des modules `__init__`

- Différence `import abc` / `import abc.def` / `from abc import def`
    - imports circulaires
