import os, re
from openai import OpenAI
import config

# Client OpenAI configuré avec la clé d’API (via variable d’environnement)
_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Instructions système en anglais pour l’IA :
# → 3–4 paragraphes concis
# → pas de salutations ni de formules de politesse
SYS_EN = (
    "Write a motivation letter in 3–4 paragraphs.\n"
    "Base it ONLY on my CV and the job posting I give you.\n"
    "Do NOT summarize the job description.\n"
    "Focus only on: my motivation for the role, my relevant experiences, my skills, and why I fit.\n"
    "Do NOT invent degrees or jobs. Do NOT copy sentences from the job description.\n"
    "Plain text only, no greetings or closings."
)



# Instructions système en français pour l’IA :
# → même logique, mais adapté au français
SYS_FR = (
    "Rédige une lettre de motivation en 3–4 paragraphes.\n"
    "Base-toi UNIQUEMENT sur mon CV et l’offre fournie.\n"
    "N’écris PAS de résumé de l’offre.\n"
    "Concentre-toi uniquement sur : ma motivation, mes expériences pertinentes, mes compétences, et pourquoi je corresponds au poste.\n"
    "N’invente aucun diplôme ni expérience. N’utilise pas de phrases copiées de l’annonce.\n"
    "Texte brut uniquement, sans formule de politesse ni salutation."
)



# ————— Normalisation du texte (nettoyage avant traitement) —————
NBSP = "\u00A0"   # espace insécable
ZWS  = "\u200B"   # espace de largeur zéro

# Expressions régulières pour détecter une salutation en début de texte (FR/EN)
GREET_RX = re.compile(
    r"^\s*(dear(\s+hiring\s+(team|manager))?|bonjour|madame|monsieur|a\s+l'attention|à\s+l'attention)\b[^\n]*?,?\s*",
    re.IGNORECASE,
)

# Expressions régulières pour détecter les formules de politesse de fin (FR/EN)
CLOSE_RX = re.compile(
    r"\b(yours\s+sincerely|kind\s+regards|best\s+regards|cordialement)\b.*$",
    re.IGNORECASE,
)

def _normalize_ws(s: str) -> str:
    """Nettoie les espaces spéciaux et les puces/traits en début de ligne."""
    s = (s or "").replace(NBSP, " ").replace(ZWS, " ")
    s = s.strip()
    # Supprime une éventuelle puce ou tiret en tout début
    s = re.sub(r"^[\u2022>\-\*\•\s]+", "", s)
    return s

def _strip_greetings_text(text: str) -> str:
    """Enlève toute salutation au début + toute formule de politesse à la fin, garde uniquement le contenu."""
    t = _normalize_ws(text)

    # Si le texte commence directement par "Dear …", on enlève la ligne entière
    t = re.sub(r"^\s*(dear[^\n]{0,120})\n+", "", t, flags=re.IGNORECASE)

    # Supprime une salutation résiduelle en tête de texte
    t = GREET_RX.sub("", t)

    # Retire les formules de fin (ex. "Kind regards") ainsi que les lignes suivantes
    lines = t.splitlines()
    while lines and CLOSE_RX.search(_normalize_ws(lines[-1])):
        lines.pop()
    return "\n".join(lines).strip()

def _paragraphize(text: str) -> list[str]:
    """Découpe le texte propre en paragraphes (max 4), en ignorant toute salutation ou closing restants."""
    t = _strip_greetings_text(text)
    # On coupe sur les doubles sauts de ligne
    parts = [p for p in re.split(r"\n\s*\n+", t) if _normalize_ws(p)]
    cleaned = []
    for p in parts:
        p = _normalize_ws(p)
        # On retire une salutation résiduelle en début de paragraphe
        p = GREET_RX.sub("", p)
        # On ignore un paragraphe qui n’est en fait qu’une formule de politesse
        if CLOSE_RX.search(p):
            continue
        if p:
            cleaned.append(p)
    # On limite à 4 paragraphes max (standard pour une lettre de motivation)
    return cleaned[:4]

def generate_body_paragraphs(bank: str, position: str, offer: str, lang: str = "EN") -> list[str]:
    """Appelle l’API OpenAI pour générer 3–4 paragraphes de lettre de motivation adaptés à l’offre."""
    # On choisit le prompt système selon la langue
    system = SYS_EN if lang.upper() == "EN" else SYS_FR

    # Prompt utilisateur = contexte (banque, poste, description)
    user = (
        f"Bank/Company: {bank}\nRole: {position}\nJob description:\n{offer}\n\n"
        "Write 3–4 paragraphs aligned to the role, outcome-oriented, and tailored to the description. "
        "No greeting, no closing."
        if lang.upper() == "EN" else
        f"Banque/Entreprise : {bank}\nPoste : {position}\nAnnonce :\n{offer}\n\n"
        "Rédige 3–4 paragraphes pertinents alignés sur l’annonce, orientés résultats. "
        "Aucune salutation ni formule finale."
    )

    # Appel à l’API (chat.completions) avec modèle défini dans config.py
    resp = _client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.6,
    )

    # On récupère le texte brut renvoyé par l’IA
    raw = (resp.choices[0].message.content or "").strip()

    # On découpe et nettoie en paragraphes exploitables
    return _paragraphize(raw)
