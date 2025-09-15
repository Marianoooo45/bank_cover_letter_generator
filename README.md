# Bank Cover Letter Generator

Bank Cover Letter Generator is a Python tool that automatically generates personalized cover letters for banks and financial institutions. Based on a job description and your CV, the app writes a professional, structured letter and formats it into a Word document (DOCX) with optional PDF export.

--------------------------------------------------------------------------------

![Interface – Dark Mode](docs/screenshot-ui.png)

--------------------------------------------------------------------------------

Features
- GUI built with CustomTkinter (dark-mode friendly)
- Pre-filled list of banks and financial institutions with integrated search
- AI-powered generation of 3–4 tailored paragraphs via OpenAI API (gpt-3.5-turbo: cost-effective and fast)
- Supports English and French
- Automated Word formatting (contact details, fonts, margins, spacing)
- Automatic PDF export via Microsoft Word or LibreOffice
- Output organized per bank under: generated_letters/

--------------------------------------------------------------------------------

Installation & Setup

1) Clone the repo
   git clone https://github.com/Marianoooo45/bank_cover_letter_generator.git
   cd bank_cover_letter_generator

2) Create a virtual environment and install dependencies
   python -m venv .venv
   .venv\Scripts\activate          # Windows
   # or
   source .venv/bin/activate       # Linux / macOS
   pip install -r requirements.txt

3) Create your environment file
   cp .env.example .env

4) Open .env and fill in the following (example)
   OPENAI_API_KEY=sk-xxxxxxx
   USER_FULLNAME=Your Name
   USER_ADDRESS=Your Address
   USER_CITY_COUNTRY=City – Country
   USER_PHONE=+33 6 00 00 00 00
   USER_EMAIL=email@example.com
   # Optional if your CV is stored elsewhere:
   # CV_PATH=/absolute/path/to/cv.txt

--------------------------------------------------------------------------------

Local CV (important)

The app reads a local text CV (cv.txt) to personalize the letter and avoid random details.

Search order:
  1. Path defined by CV_PATH in .env (optional)
  2. ./cv.txt at the project root
  3. cv.txt in the current working directory

A cv.example.txt is provided in the repo as a template. Create your own cv.txt locally (same structure) and do not commit it.

--------------------------------------------------------------------------------

Usage

Run the app:
  python app.py

Steps:
  1. Select a bank
  2. Enter the job title
  3. Paste the job description
  4. Choose the language (EN / FR)
  5. Generate → DOCX and PDF files are created in:
       generated_letters/<BankName>/

--------------------------------------------------------------------------------

Project Structure

bank_cover_letter_generator/
├─ app.py              # GUI
├─ config.py           # Env/config loader
├─ llm_body.py         # AI generation (reads cv.txt if present)
├─ writer.py           # DOCX creation
├─ export_pdf.py       # DOCX → PDF conversion
├─ requirements.txt    # Python dependencies
├─ .env.example        # Example env file
├─ cv.example.txt      # Example CV text (cv.txt stays local)
├─ .gitignore          # Excludes cv.txt, .env, etc.
└─ README.md           # Documentation

--------------------------------------------------------------------------------

Security

- Never publish your .env or your cv.txt
- Keep your OpenAI API key private (only in local env variables)
- .gitignore is configured to prevent accidental commits

Quick sanity check before pushing:
  git grep -n "sk-" -- .

--------------------------------------------------------------------------------

License

MIT License.
