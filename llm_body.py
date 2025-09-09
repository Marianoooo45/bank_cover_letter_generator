# llm_body.py — appelle l'API pour produire 3–4 paragraphes
from typing import List
import json
import config

try:
    from openai import OpenAI
except Exception as e:
    raise RuntimeError("Installe le SDK OpenAI: pip install openai") from e

def _client() -> "OpenAI":
    if config.OPENAI_API_BASE:
        return OpenAI(api_key=config.OPENAI_API_KEY, base_url=config.OPENAI_API_BASE)
    return OpenAI(api_key=config.OPENAI_API_KEY)

SYS_PROMPT = """You are a precise assistant writing professional cover letters.
Return ONLY JSON:
{"paragraphs": ["...", "...", "...", "..."]}

Rules:
- 3 to 4 concise paragraphs.
- No bullets, no markdown.
- Formal, energetic, tailored to the role and company.
- If language=FR write French; if EN write English.
"""

def generate_body_paragraphs(bank: str, position: str, offer_text: str, language: str = "EN") -> List[str]:
    cl = _client()
    payload = {
        "bank": bank,
        "position": position,
        "language": language,
        "job_description": offer_text[:6000],
    }
    resp = cl.chat.completions.create(
        model=config.MODEL,
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        temperature=0.6,
        max_tokens=600,
    )
    content = resp.choices[0].message.content.strip()
    s, e = content.find("{"), content.rfind("}")
    if s == -1 or e == -1 or e <= s:
        raise RuntimeError("Réponse LLM non JSON.")
    data = json.loads(content[s:e+1])
    paras = [p.strip() for p in data.get("paragraphs", []) if isinstance(p, str) and p.strip()]
    if not paras:
        raise RuntimeError("Aucun paragraphe généré.")
    return paras[:4]
