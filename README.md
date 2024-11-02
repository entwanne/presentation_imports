# La mécanique des imports

Conférence présentée à la PyConFr 2024.

> Voyage au cœur du mécanisme des imports en Python afin de comprendre comment ils fonctionnent et comment nous pouvons agir sur leur comportement, à travers l'écriture de finders et de loaders personnalisés.

Le support est disponible à l'adresse <https://entwanne.github.io/presentation_imports/>.

## Support de présentation

Le support de présentation utilise [`lucina`](https://pypi.org/project/lucina/), un outil permettant de générer un notebook Jupyter à partir de fichiers Markdown.
C'est ensuite le plugin rise qui est utilisé pour rendre une présentation Reveal.js à partir de ce notebook, afin d'avoir une présentation interactive.

L'environnement de travail peut alors être installé à l'aide de la commande shell `pip install -r requirements`.

`make run` permet ensuite de générer et démarrer la présentation.

Différents exports (notebook, reveal, PDF) sont présentés sur la branche [exports](https://github.com/entwanne/presentation_imports/tree/exports).
