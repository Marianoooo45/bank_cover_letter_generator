import os, re
from openai import OpenAI
import config

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYS_EN = (
    "You are a cover-letter assistant. Return 3–4 concise paragraphs ONLY, plain text.\n"
    "Do NOT include greeting or closing (no 'Dear…', no 'Yours…'). Start directly with content."
)
SYS_FR = (
    "Tu es un assistant de lettre de motivation. Rends UNIQUEMENT 3–4 paragraphes concis, en texte brut.\n"
    "N’inclus NI salutation NI formule de politesse. Commence directement par le contenu."
)

# ---------- Normalisation / Nettoyage ----------
NBSP = "\u00A0"
ZWS  = "\u200B"

# salutations communes (EN/FR)
GREET_RX = re.compile(
    r"^\s*(dear(\s+hiring\s+(team|manager))?|bonjour|madame|monsieur|a\s+l'attention|à\s+l'attention)\b[^\n]*?,?\s*",
    re.IGNORECASE,
)
# closings communes
CLOSE_RX = re.compile(
    r"\b(yours\s+sincerely|kind\s+regards|best\s+regards|cordialement)\b.*$",
    re.IGNORECASE,
)

def _normalize_ws(s: str) -> str:
    # remplace NBSP/ZWS, nettoie bullets/ponctuation parasite en tête
    s = (s or "").replace(NBSP, " ").replace(ZWS, " ")
    s = s.strip()
    # retire puces/traits en tout début de ligne
    s = re.sub(r"^[\u2022>\-\*\•\s]+", "", s)
    return s

def _strip_greetings_text(text: str) -> str:
    """Enlève une salutation tout en haut + closing en bas, conserve le reste."""
    t = _normalize_ws(text)

    # 1) si le texte commence par une salut, supprime la ligne de salut
    t = re.sub(r"^\s*(dear[^\n]{0,120})\n+", "", t, flags=re.IGNORECASE)

    # 2) supprime toute salut au tout début même si non suivie d'un saut de ligne
    t = GREET_RX.sub("", t)

    # 3) supprime les closings à la fin (et lignes qui suivent)
    lines = t.splitlines()
    while lines and CLOSE_RX.search(_normalize_ws(lines[-1])):
        lines.pop()
    return "\n".join(lines).strip()

def _paragraphize(text: str) -> list[str]:
    """Nettoie (salut/closing) puis découpe en paragraphes; retire salut résiduels par paragraphe."""
    t = _strip_greetings_text(text)
    parts = [p for p in re.split(r"\n\s*\n+", t) if _normalize_ws(p)]
    cleaned = []
    for p in parts:
        p = _normalize_ws(p)
        # retire une éventuelle salut restante au début du paragraphe mais garde le contenu
        p = GREET_RX.sub("", p)
        # ignore un paragraphe qui n'est qu'une formule de politesse
        if CLOSE_RX.search(p):
            continue
        if p:
            cleaned.append(p)
    return cleaned[:4]

def generate_body_paragraphs(bank: str, position: str, offer: str, lang: str = "EN") -> list[str]:
    system = SYS_EN if lang.upper() == "EN" else SYS_FR
    user = (
        f"Bank/Company: {bank}\nRole: {position}\nJob description:\n{offer}\n\n"
        "Write 3–4 paragraphs aligned to the role, outcome-oriented, and tailored to the description. "
        "No greeting, no closing."
        if lang.upper() == "EN" else
        f"Banque/Entreprise : {bank}\nPoste : {position}\nAnnonce :\n{offer}\n\n"
        "Rédige 3–4 paragraphes pertinents alignés sur l’annonce, orientés résultats. "
        "Aucune salutation ni formule finale."
    )
    resp = _client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.6,
    )
    raw = (resp.choices[0].message.content or "").strip()
    return _paragraphize(raw)
