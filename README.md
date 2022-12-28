# OWS - Projet Transports

### Arthur BENARD - Guillaume DUFAU

# Cahier des charges fonctionnel

Le projet a été réalisé à l’aide de [flask](https://flask.palletsprojects.com/en/2.2.x/quickstart/), un framework python pour le web, en utilisant le moteur de template [Jinja2](https://jinja.palletsprojects.com/en/2.10.x/) pour le rendu HTML dynamique ainsi que [Bulma](https://bulma.io/), un framework CSS qui nous a permis de ne pas avoir à créer de CSS pour notre application et ainsi de gagner du temps.

Afin de pouvoir utiliser l’application, il est nécessaire d’installer flask (Windows ou Unix) :

[Installation - Flask Documentation (2.2.x)](https://flask.palletsprojects.com/en/2.2.x/installation/)

Nous utilisons également la bibliothèque python [RDFLib](https://rdflib.readthedocs.io/en/stable/) afin de lire et d’exécuter du SPARQL sur notre graphe RDF (en turtle).

In est donc nécessaire de l’installer afin que le projet puisse fonctionner correctement :

```bash
$ pip install rdflib
```

Notre application compte un menu (en haut à gauche de l’écran) avec deux catégories : 

- une catégorie individus (statique) avec un sous-menu permettant d’afficher la liste des véhicules, personnes, lieux et trajets
- une catégorie recherche (dynamique) ou il est possible d’effectuer des recherches dans le graphe des transports et sur DBPedia

Voici un lien vers le démonstrateur vidéo :  

[[M2 VMI] OWS Projet Transports - Démonstrateur](https://www.youtube.com/watch?v=uHY3OcXcgMU)