# Bank Cover Letter Generator

Bank Cover Letter Generator est un outil Python qui génère automatiquement des lettres de motivation personnalisées pour des banques et institutions financières.  
À partir d’une description de poste, l’application crée un texte professionnel structuré puis le met en forme dans un document Word (DOCX) et l’exporte en PDF.

---

## Fonctionnalités

- Interface graphique moderne avec CustomTkinter  
- Liste pré-remplie de banques avec recherche intégrée  
- Génération de 3 à 4 paragraphes adaptés à l’offre grâce à l’API OpenAI  
- Support de l’anglais et du français  
- Mise en page Word automatisée (coordonnées, police, marges, espacements)  
- Export automatique en PDF via Microsoft Word ou LibreOffice  
- Organisation des fichiers par banque dans le dossier `generated_letters/`

---

## Installation

Cloner le dépôt :
```bash
git clone https://github.com/Marianoooo45/bank_cover_letter_generator.git
cd bank_cover_letter_generator
Créer un environnement virtuel et installer les dépendances :

bash
Copy code
python -m venv .venv
.venv\Scripts\activate  # Windows
# ou
source .venv/bin/activate  # Linux / macOS

pip install -r requirements.txt
Configurer les variables d’environnement :

bash
Copy code
cp .env.example .env
Éditer .env pour ajouter la clé OpenAI et vos informations personnelles :

dotenv
Copy code
OPENAI_API_KEY=sk-xxxxxxx
USER_FULLNAME=Votre Nom
USER_ADDRESS=Votre Adresse
USER_CITY_COUNTRY=Votre Ville – Pays
USER_PHONE=+33 6 00 00 00 00
USER_EMAIL=adresse@email.com
Utilisation
Lancer l’application :

bash
Copy code
python app.py
Étapes :

Sélectionner une banque

Indiquer le poste visé

Coller la description de l’offre

Choisir la langue (EN / FR)

Générer la lettre → fichiers DOCX et PDF créés dans generated_letters/<Nom Banque>/

Structure du projet
pgsql
Copy code
bank_cover_letter_generator/
├── app.py              # Interface graphique
├── config.py           # Chargement des variables d’environnement
├── llm_body.py         # Génération du contenu avec OpenAI
├── writer.py           # Création du document Word
├── export_pdf.py       # Conversion DOCX → PDF
├── requirements.txt    # Dépendances Python
├── .env.example        # Exemple de configuration
├── .gitignore          # Fichiers exclus du repo
└── README.md           # Documentation
Sécurité
Ne jamais publier votre fichier .env

La clé API doit rester privée et être stockée uniquement dans vos variables d’environnement

.gitignore protège contre les commits accidentels

Vérification rapide avant un push :

bash
Copy code
git grep -n "sk-" -- .
