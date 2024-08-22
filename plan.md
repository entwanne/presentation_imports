- Que se passe-t-il quand on fait un `import foo`
- __import__ / importlib.import_module

- Vérification de la présence du module dans le cache sys.modules
- Nettoyer / falsifier le cache

- Exploration du sys.path pour trouver des répertoires à importer
- Modifier sys.path pour ajouter des répertoires particuliers
- -> préférer laisser Python gérer ça et utiliser pip pour placer les paquets dans les répertoires d'installation

- Mécanisme des finders et loaders
- sys.path_hooks pour ajouter de nouveaux finders
- SourceLoader / PathEntryFinder
- Exemples :
    - Transformer le texte lu (ROT13, chiffrement)
    - Étendre la syntaxe de Python (opérateur d'incrémentation)
    - Compiler depuis d'autres langages (Brainfuck)

- Autres finders dans sys.meta_path
- MetaPathFinder
- Exemples :
    - Importer des modules depuis le réseau (HTTP, RPC)
    - Création de modules à la volée (nom du module qui correspond lui-même à des instructions)

- Vue d'ensemble : étapes lors d'un import