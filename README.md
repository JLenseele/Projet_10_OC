#SOFTDESK API

## Requirements

+ [Python v3+](https://www.python.org/downloads/)

## Installation & Get Started

#### Récuperer le projet sur GitHub

    git clone https://github.com/JLenseele/Project_10_OC
    cd Project_10_OC

#### Créer l'environement virtuel

    python -m venv env
    env\Scripts\activate
    pip install -r requierments.txt
    
#### (Optionnel - rapport Flake8)  
Il est possible de générer un nouveau rapport via la commande suivante :  
Le rapport sera disponible dans ./flake-report/index.html

    flake8 --format=html --htmldir=flake-report
    
#### Lancer le serveur

    python softdesk\manage.py runserver
