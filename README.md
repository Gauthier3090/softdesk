# Softdesk

![](https://camo.githubusercontent.com/7c691d06ed3e830244e052e43bb63780a25f0be9c7446cd4bea9f638dae92c99/68747470733a2f2f6f6e617465737465706f7572746f692e636f6d2f77702d636f6e74656e742f75706c6f6164732f323032302f30322f4c6f676f5f6f70656e636c617373726f6f6d735f6f6e617465737465706f7572746f692e6a7067)

# Résumé du projet

Une application de suivi des problèmes pour les trois plateformes (site web, applications Android et iOS).

L'application permettra essentiellement aux utilisateurs de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.

Pour plus de détails sur le fonctionnement de cette API, se référer à sa [documentation](https://documenter.getpostman.com/view/19366183/UzJHQHqX) (Postman).

# Configurer un environnement virtuel Python et lancer le projet Django

## Récupération du projet

````Bash
git clone https://github.com/Gauthier3090/softdesk.git p10_django
cd p10_django
````
## Windows

La création d'environnements virtuels est faite en exécutant la commande venv :

````Bash
python -m venv \path\to\new\virtual\venv
````

Pour commencer à utiliser l’environnement virtuel, il doit être activé :

````Bash
.\venv\Scripts\activate.bat
pip install -r requirements.txt
````

Pour lancer le projet Django:

````Bash
cd .\src
py .\manage.py runserver
````

## Unix

La création d'environnements virtuels est faite en exécutant la commande venv :

````Bash
python3 -m venv \path\to\new\virtual\venv
````

Pour commencer à utiliser l’environnement virtuel, il doit être activé :

````Bash
source venv/bin/activate
pip install -r requirements.txt
````

Pour lancer le projet Django:

````Bash
cd .\src
python3 .\manage.py runserver
````

### Vous pouvez naviguer sur l'API grâce aux commandes cURL ou Postman.