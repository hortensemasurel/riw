# Recherche d'information

Par Alexandre Lainé, Hortense Masurel et Anne-Laurène Harmel de CentraleSupélec

Ce projet consiste à créer un moteur de recherche sur un corpus de texte de Stanford (CS276).
Notre algorithme de recherche utilise le système de poids TF-IDF.

## Installation du projet

Nous recommandons la création d'un environnement virtuel afin d'isoler les dépendances requises pour 
ce projet des autres dépendances du système.


#### Installation des packages
Les packages requis peuvent être installés en exécutant la commande suivante.

```
(venv) $ pip install -r requirements.txt
```

#### Installation de la bibliothèque NLTK
Nous utilisons la bibliotèque NLTK dans notre projet et il faut donc installer certains éléments 
grâce à la commande suivante.

```
(venv) $ python -m nltk.downloader stopwords wordnet
```

#### Installation des données
Ce moteur de recherche est adapté pour les données CS276 de Stanford Education.
Les données sont présentes à cet [endroit](http://web.stanford.edu/class/cs276/pa/pa1-data.zip) et pour le bon fonctionnement du projet
, elles doivent être installées dans le dossier ./data/cs276.

Pour ce faire, la commande suivante doit être exécutée : 

```
python data_download.py
```

Une fois la commande effectuée, la structure du projet sera la suivante :
```
projet
└───models
└───data
│   └───cs276
|       └───0
|       |   |   3dradiology.stanford.edu_
|       |   |   ...
|       └───1
|        ...
```

#### Lancement d'une requête
Pour lancer une requête, il faut exécuter le fichier main.py avec la commande suivante:
```
python main.py
```


## Description technique

#### Modèles
Nous avons choisi de représenter les documents, la collection, les requêtes et le moteur de recherche 
par des classes séparées définies respectivement dans les fichiers document.py, collection.py, 
query.py, search_engine.py.

#### Traitement des données
Après avoir téléchargé les données, elles sont triées et rangées dans le dossier data.
Nous allons ensuite les traiter à travers une pipeline. D'abord, nous allons conserver uniquement
les caractères alphabétiques, ensuite, nous enlèverons les stopwords (ceux listés dans la bibliothèque NLTK) 
et enfin nous retiendrons la racine des mots (étape de lemmatisation) grâce au réseau WordNet.
Les requêtes suivent la même pipeline de traitement.

Nous construisons ensuite l'index inversé dans le fichier collection.py afin de représenter la collection.

#### Modèle de poids choisi
Pour construire notre algorithme de recherche, nous avons choisi d'utiliser le modèle TF-IDF.
Pour traduire la pertinence d'un mot dans un document, nous allons donc observer deux mesures :
- la fréquence du terme (TF) dans le document qui nous indique à quel point le terme décrit le document.
- l'inverse document frequency (IDF), qui mesure la répartition du terme dans la collection.

Nous avons normalisé la fréquence du terme (TF) car la pertinence d'un terme ne croît pas proportionellement avec sa fréquence.
Nous considérons donc le poids normalisé suivant : 1 + log(TF).

Pour l'IDF nous avons pris la formule vue en cours : log (N / dft).

Le poids final s'obtient en multipliant les deux quantités. Ainsi, un terme apparaissant fréquemment dans le document mais
rarement dans le reste de la collection aura un poids élevé. Cela signifie que le document sera très pertinent par rapport à une
requête comprenant ce terme.
