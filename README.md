# SOFTDESK API

## Requirements

+ [Python v3+](https://www.python.org/downloads/)

## Installation & Get Started

#### Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Projet_10_OC.git
    cd Projet_10_OC

#### Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requirements.txt
    
#### (Optionnel - rapport Flake8)  
Il est possible de générer un nouveau rapport via la commande suivante :  
Le rapport sera disponible dans ./flake-report/index.html

    flake8 --format=html --htmldir=flake-report
    
#### Lancer le serveur

    python softdesk\manage.py runserver

## Documentation POSTMAN

Vous trouverez sur le lien suivant, la documentation complète des différents EndPoints de l'API  
    
    https://documenter.getpostman.com/view/24506495/2s93Y2QgKY
