# Bank Cover Letter Generator

Bank Cover Letter Generator est un outil Python qui génère automatiquement des lettres de motivation personnalisées pour des banques et institutions financières.  
À partir d’une description de poste et de votre CV, l’application crée un texte professionnel structuré puis le met en forme dans un document Word (DOCX) et l’exporte en PDF.

## Aperçu

![Interface – Dark Mode](docs/screenshot-ui.png)
---

## Fonctionnalités

- Interface graphique avec CustomTkinter  
- Liste pré-remplie de banques et institutions financieres avec recherche intégrée  
- Génération de 3 à 4 paragraphes adaptés à l’offre grâce à l’API OpenAI (modèle 3.5 turbo car pas cher et efficace) 
- Support de l’anglais et du français  
- Mise en page Word automatisée (coordonnées, police, marges, espacements)  
- Export automatique en PDF via Microsoft Word ou LibreOffice  
- Organisation des fichiers par banque dans le dossier `generated_letters/`

---

## Installation

Cloner le dépôt :
~~~bash
git clone https://github.com/Marianoooo45/bank_cover_letter_generator.git
cd bank_cover_letter_generator
~~~

Créer un environnement virtuel et installer les dépendances :
~~~bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
~~~

Configurer les variables d’environnement :
~~~bash
cp .env.example .env
~~~

Éditer `.env` pour ajouter la clé OpenAI et vos informations personnelles :
~~~dotenv
OPENAI_API_KEY=sk-xxxxxxx
USER_FULLNAME=Votre Nom
USER_ADDRESS=Votre Adresse
USER_CITY_COUNTRY=Votre Ville – Pays
USER_PHONE=+33 6 00 00 00 00
USER_EMAIL=adresse@email.com

# Optionnel : si vous stockez le CV ailleurs que dans la racine du projet
# CV_PATH=C:\chemin\vers\cv.txt
~~~

---

## CV local (important)

L’application lit un fichier **`cv.txt`** pour personnaliser la lettre et éviter les informations aléatoires.

Ordre de recherche :
1. Chemin défini par la variable d’environnement `CV_PATH` (optionnel)  
2. `./cv.txt` à la racine du projet  
3. `cv.txt` dans le dossier courant

Dans le dépôt public, un **`cv.example.txt`** est fourni comme modèle.  
Créez votre `cv.txt` localement (même structure) et **ne le committez pas**.

---

## Utilisation

Lancer l’application :
~~~bash
python app.py
~~~

Étapes :
1. Sélectionner une banque  
2. Indiquer le nom du poste  
3. Coller la description de l’offre  
4. Choisir la langue (EN / FR)  
5. Générer la lettre → fichiers DOCX et PDF créés dans `generated_letters/<Nom Banque>/`

---

## Structure du projet

~~~text
bank_cover_letter_generator/
├── app.py              # Interface graphique
├── config.py           # Chargement des variables d’environnement
├── llm_body.py         # Génération du contenu (lit cv.txt si présent)
├── writer.py           # Création du document Word
├── export_pdf.py       # Conversion DOCX → PDF
├── requirements.txt    # Dépendances Python
├── .env.example        # Exemple de configuration
├── cv.example.txt      # Exemple de CV texte (cv.txt reste local)
├── .gitignore          # Fichiers exclus du repo (inclut cv.txt et .env)
└── README.md           # Documentation
~~~

---

## Sécurité

- Ne jamais publier votre fichier `.env` ni votre `cv.txt`.  
- La clé API doit rester privée et être stockée uniquement dans vos variables d’environnement.  
- `.gitignore` protège contre les commits accidentels.  
- Vérification rapide avant un push :
~~~bash
git grep -n "sk-" -- .
~~~

---

## Licence

Projet distribué sous licence MIT.
