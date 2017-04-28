----

## Rapport de projet : Bentley Ottmann

### Rigondaud Baptiste et Burrer Yann
#### 1A Ensimag, Avril 2017

----

#### Vue générale

Le projet Bentley Ottmann consiste en premier lieu à implémenter l'algorithme de Bentley Ottmann qui permet de calculer efficacement des intersections de segments dans un plan, en comparaison avec un algorithme "naïf" qui comparerait les segments deux à deux.

Dans la suite de ce rapport sont détaillés les choix techniques faits afin d'implémenter cet algorithme, une prise de performance sur des exemples fournis, une discussion autour de la compléxité de l'algorithme ainsi qu'un retour d'expérience.

L'objectif principal, qui est d'implémenter l'algorithme de Bentley Ottmann n'est cependant pas complètement atteint puisque certaines intersections ne sont pas calculées. Ce point sera détaillé plus longuement dans le retour d'expérience.

----

#### Rapport technique

###### Structures de données

- L'algorithme repose premièrement sur une gestion d'évènements, qui permettent, à l'aide d'une ligne de balayage virtuelle, de calculer les intersections. Afin de stocker ces évènements deux objets sont utilisés:

    - Event: représente un évènement
    - Events: contient la liste des évènements, qui est une SortedListWithKey, provenant du module SortedContainers.

- Cette liste des évènements permet de remplacer la structure d'arbre pour stocker les évènements, en utilisant pour clé les coordonnées de ceux-ci. Cette liste permet donc d'effectuer des opérations dichotomiques de recherche et d'insertion.

- Un point important de l'algorithme est la gestion des "segments en vie". Il représentent les segments pouvant effectuer une intersection. Afin de les stocker, nous avons utilisé une SortedList, du module SortedContainers, afin de remplacer une structure d'arbre. Cette structure est couplée avec une fonction de calcul de clé, qui est appelée à chaque opération sur la liste des segments vivants.


- Enfin, l'objet Solution permet en outre de stocker la solution, mais permet aussi d'effectuer divers tracés. Cela permet notamment lors du débogage, de tracer l'algorithme étape par étape, en visualisant les segments en vie, le point courant, et les intrsections au fur et à mesure de l'avancement de l'algorithme.

###### Prise de performance
