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
    - https://pypi.org/project/copilot-import/
