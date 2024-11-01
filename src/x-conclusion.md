# Conclusion

## L'import en bref

- Vue d'ensemble des étapes lors d'un import :
    1. Résolution du nom du module
    2. Recherche du module dans le cache (court-circuit si trouvé)
    3. Résolution des modules parents dans le cas d'un paquet
    4. Identification de la spécification du module (_finder_)
    5. Chargement du module (_loader_)
    6. Stockage dans le cache
    7. Exécution du code du module (_loader_)

- <https://docs.python.org/3/library/importlib.html#approximating-importlib-import-module>

## Conclusion

- Le mécanisme d'imports est paramétrable à de multiples niveaux
- Et permet de tordre Python comme on le veut

## Liens utiles

- Quelques liens utiles
    - <https://peps.python.org/pep-0302/>
    - <https://peps.python.org/pep-0451/>
    - <https://docs.python.org/3/reference/import.html>
    - <https://docs.python.org/3/library/importlib.html>

---

- Et retrouvez les sources de cette présentation
    - <https://github.com/entwanne/presentation_imports>

## Questions ?
