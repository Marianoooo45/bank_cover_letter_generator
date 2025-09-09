# config.py — public safe config (commit OK)
import os
from pathlib import Path

# Charge .env en dev (sans l'exiger en prod/CI)
try:
    from dotenv import load_dotenv
    for p in (Path(__file__).with_name(".env"), Path.cwd() / ".env"):
        if p.exists():
            load_dotenv(p, override=False)
            break
except Exception:
    pass

# --- Secrets / API ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "") or None
MODEL = os.getenv("MODEL", "gpt-4o-mini")

if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY manquant. Définis la variable d'environnement ou crée un .env local."
    )

# --- Coordonnées (placeholder par défaut) ---
NOM = os.getenv("USER_FULLNAME", "Your Name")
ADRESSE = os.getenv("USER_ADDRESS", "Street & Number")
VILLE_PAYS = os.getenv("USER_CITY_COUNTRY", "City – Country")
TEL = os.getenv("USER_PHONE", "+00 0 00 00 00 00")
EMAIL = os.getenv("USER_EMAIL", "your.email@example.com")

# --- Style docx ---
POLICE = os.getenv("DOC_FONT", "Aptos (Body)")
TAILLE_PT = int(os.getenv("DOC_FONT_SIZE_PT", "12"))
LINE_SPACING = float(os.getenv("DOC_LINE_SPACING", "1.22"))

# Marges: top, bottom, left, right (en pouces)
MARGES_INCH = tuple(map(float, os.getenv("DOC_MARGINS_INCH", "1.00,0.60,1.10,1.10").split(",")))

# Espacements (points)
ESP_APRES_EMAIL_PT = int(os.getenv("DOC_SPACE_AFTER_EMAIL_PT", "12"))
ESP_APRES_SUJET_PT = int(os.getenv("DOC_SPACE_AFTER_SUBJECT_PT", "12"))
ESP_APRES_SALUT_PT = int(os.getenv("DOC_SPACE_AFTER_SALUT_PT", "12"))
ESP_APRES_PAR_PT = int(os.getenv("DOC_SPACE_AFTER_PAR_PT", "6"))
ESP_APRES_SIGNATURE_PT = int(os.getenv("DOC_SPACE_AFTER_SIGNATURE_PT", "12"))

# Dossier de sortie
OUT_DIR = os.getenv("OUTPUT_DIR", "generated_letters")

# Banques (public)
BANQUES = sorted([
    "ADM","BP Trading","Bunge","Cargill","EDF Trading","Engie Global Markets","Glencore","Gunvor",
    "Louis Dreyfus Company","Mabanaft","Mercuria","Shell Trading","TotalEnergies","Trafigura","Vitol",
    "Airbus Finance","Air Liquide Finance","LVMH Finance","Sanofi Finance",
    "Amundi","Axa IM","BlackRock","DNCA","Fidelity","LFDE","PIMCO","Sycomore","Wellington",
    "Bloomberg","CME Group","Euronext","LSEG","Murex","SIX",
    "AG2R La Mondiale","Generali","Scor",
    "BGC Partners","Flow Traders","GFI Securities","IMC Trading","Jane Street","Kepler Cheuvreux",
    "Marex","Optiver","SMBC Nikko","Stifel","Susquehanna","TP Icap",
    "Edmond de Rothschild","Julius Baer","Lombard Odier","Mirabaud","Pictet","Rothschild & Co","Vontobel",
    "Alantra","Banco Do Brasil","Barclays","BBVA","Berenberg","BNP Paribas","Bank of America",
    "Bank of China","Groupe BPCE","Bryan Garnier","Crédit Agricole","Caixa Bank","CIC","Citi",
    "Deutsche Bank","DZ Bank","Goldman Sachs","HSBC","ICBC","ING","Intesa Sanpaolo","Jefferies",
    "JP Morgan","KfW Bank","La Banque Postale","Morgan Stanley","Mizuho","MUFG","Natixis","Nomura",
    "Oddo BHF","Rabobank","RBC","Santander","Société Générale","Standard Chartered","UBS","UniCredit",
    "Wells Fargo"
])
