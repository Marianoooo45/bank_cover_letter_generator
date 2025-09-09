# Cover Letter Generator (safe public)

Génère une lettre de motivation (DOCX + PDF) à partir d'une description de poste via l'API OpenAI.

## Setup
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# édite .env et renseigne OPENAI_API_KEY + tes infos perso
python app.py
