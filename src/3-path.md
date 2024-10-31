# Recherche de modules

## Recherche de modules

- Pour trouver les modules à importer, Python parcourt la liste `sys.path`

```python
sys.path
```

## Ajouter un répertoire

- On peut ainsi ajouter des répertoires dans `sys.path` pour permettre à Python de trouver les modules qui s'y trouvent

```python
import dir_example
```

```python
sys.path.append('subdirectory')

import dir_example
dir_example.hello('PyConFR')
```

---

- Mais on préférera laisser Python gérer ça par lui-même et utiliser les répertoires d'installation pour rendre nos modules et paquets accessibles

## Ajouter un fichier zip

- De la même manière, Python est en mesure d'importer des modules depuis une archive zip

```shell
%%sh
zipinfo -1 packages.zip
zcat packages.zip
```

```python
sys.path.append('packages.zip')

import zip_example
zip_example.hello('PyConFR')
```

## Ajouter un fichier zip

- Ce mécanisme permet aussi de distribuer un paquet comme un zip

```shell
%%sh
zipinfo calc_program.zip
```

```shell
%%sh
X=3 Y=4 python calc_program.zip
```
