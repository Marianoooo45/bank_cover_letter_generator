from typing import List
import json
import os
from pathlib import Path
import config

try:
    from openai import OpenAI
except Exception as e:
    raise RuntimeError("Installe le SDK OpenAI: pip install openai") from e


def _client() -> "OpenAI":
    if config.OPENAI_API_BASE:
        return OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_API_BASE)
    return OpenAI(api_key=config.OPENAI_API_KEY)


def _app_dir() -> Path:
    """Répertoire de l'app (compatible exécutable PyInstaller)."""
    import sys
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def _read_cv_text() -> str:
    """
    Lit le CV texte brut. Ordre de recherche :
    1) Variable d'env CV_PATH (si définie)
    2) ./cv.txt à côté des sources
    3) ./cv.txt dans le dossier courant
    Si introuvable, retourne une chaîne vide (le LLM se débrouille avec le reste).
    """
    env_path = os.getenv("CV_PATH")
    if env_path and Path(env_path).is_file():
        return Path(env_path).read_text(encoding="utf-8", errors="ignore")

    p1 = _app_dir() / "cv.txt"
    if p1.is_file():
        return p1.read_text(encoding="utf-8", errors="ignore")

    p2 = Path.cwd() / "cv.txt"
    if p2.is_file():
        return p2.read_text(encoding="utf-8", errors="ignore")

    return ""


SYS_PROMPT = """You write professional cover letters for banking and markets roles.
Output ONLY valid JSON:
{"paragraphs":["...", "...", "...", "..."]}

Guidelines:
- 3 to 4 concise paragraphs, no bullets, no markdown.
- Use the candidate resume ('cv') to tailor achievements and skills.
- Use the job description and the company name to align motivation and fit.
- If language=FR, write fluent French; if EN, write fluent English.
- Keep a professional, confident tone; avoid repetition and generic claims.
"""


def generate_body_paragraphs(bank: str, position: str, offer_text: str, language: str = "EN") -> List[str]:
    cl = _client()
    cv_text = _read_cv_text()

    payload = {
        "bank": bank,
        "position": position,
        "language": language,
        "job_description": (offer_text or "")[:6000],
        "cv": cv_text[:8000],  # on injecte le contenu de cv.txt
        # fallback minimal si jamais cv.txt est absent
        "identity_fallback": {"name": config.NOM, "email": config.EMAIL},
    }

    resp = cl.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=0.6,
        max_tokens=700,
    )

    content = resp.choices[0].message.content.strip()
    s, e = content.find("{"), content.rfind("}")
    if s == -1 or e == -1 or e <= s:
        raise RuntimeError("Réponse LLM non JSON.")
    data = json.loads(content[s:e + 1])
    paras = [p.strip() for p in data.get("paragraphs", []) if isinstance(p, str) and p.strip()]
    if not paras:
        raise RuntimeError("Aucun paragraphe généré.")
    return paras[:4]
