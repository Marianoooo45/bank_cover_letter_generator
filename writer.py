import os, re, sys
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_LINE_SPACING
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import config

def app_dir() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def _cfg(name, default):
    return getattr(config, name, default)

def _apply_font_to_run(run, bold=False):
    run.bold = bool(bold)
    run.font.name = _cfg("POLICE", "Aptos (Body)")
    run.font.size = Pt(_cfg("TAILLE_PT", 11))
    r = run._element
    rPr = r.find(qn("w:rPr")) or OxmlElement("w:rPr"); r.append(rPr) if r.find(qn("w:rPr")) is None else None
    rFonts = rPr.find(qn("w:rFonts")) or OxmlElement("w:rFonts"); rPr.append(rFonts) if rPr.find(qn("w:rFonts")) is None else None
    font_name = _cfg("POLICE", "Aptos (Body)")
    rFonts.set(qn("w:ascii"), font_name); rFonts.set(qn("w:hAnsi"), font_name); rFonts.set(qn("w:cs"), font_name)

def _add_text(p, text, bold=False):
    r = p.add_run(text)
    _apply_font_to_run(r, bold=bold)
    return r

def _mailto(paragraph, email: str):
    part = paragraph.part
    r_id = part.relate_to(f"mailto:{email}", RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement("w:hyperlink"); hyperlink.set(qn("r:id"), r_id)
    run = OxmlElement("w:r"); rPr = OxmlElement("w:rPr")
    rStyle = OxmlElement("w:rStyle"); rStyle.set(qn("w:val"), "Hyperlink"); rPr.append(rStyle)
    u = OxmlElement("w:u"); u.set(qn("w:val"), "single"); rPr.append(u)
    rFonts = OxmlElement("w:rFonts"); font_name = _cfg("POLICE", "Aptos (Body)")
    rFonts.set(qn("w:ascii"), font_name); rFonts.set(qn("w:hAnsi"), font_name); rFonts.set(qn("w:cs"), font_name)
    rPr.append(rFonts)
    sz = OxmlElement("w:sz"); sz.set(qn("w:val"), str(int(_cfg("TAILLE_PT", 11) * 2)))
    szCs = OxmlElement("w:szCs"); szCs.set(qn("w:val"), str(int(_cfg("TAILLE_PT", 11) * 2)))
    rPr.append(sz); rPr.append(szCs)
    color = OxmlElement("w:color"); color.set(qn("w:val"), "0563C1"); rPr.append(color)
    run.append(rPr); t = OxmlElement("w:t"); t.text = email; run.append(t)
    hyperlink.append(run); paragraph._p.append(hyperlink)

def _clean(text: str) -> str:
    text = re.sub(r"[\*_\`]+", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()

def _pf(p, after_pt=0, before_pt=0):
    pf = p.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = _cfg("LINE_SPACING", 1.22)
    pf.space_before = Pt(before_pt)
    pf.space_after  = Pt(after_pt)

def build_letter_doc(bank: str, position: str, body_paragraphs: list[str]) -> Document:
    doc = Document()
    top, bottom, left, right = _cfg("MARGES_INCH", (1.00, 0.60, 1.10, 1.10))
    for s in doc.sections:
        s.top_margin = Inches(top); s.bottom_margin = Inches(bottom)
        s.left_margin = Inches(left); s.right_margin = Inches(right)
    st = doc.styles["Normal"]
    st.font.name = _cfg("POLICE", "Aptos (Body)")
    st.font.size = Pt(_cfg("TAILLE_PT", 12))
    st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    st.paragraph_format.line_spacing = _cfg("LINE_SPACING", 1.22)
    st.paragraph_format.space_before = Pt(0); st.paragraph_format.space_after = Pt(0)

    after_email     = _cfg("ESP_APRES_EMAIL_PT",     12)
    after_subject   = _cfg("ESP_APRES_SUJET_PT",     12)
    after_salut     = _cfg("ESP_APRES_SALUT_PT",     12)
    after_par       = _cfg("ESP_APRES_PAR_PT",        6)
    after_signature = _cfg("ESP_APRES_SIGNATURE_PT", 12)

    p = doc.add_paragraph()
    _add_text(p, config.NOM, bold=True); _add_text(p, "\n")
    _add_text(p, config.ADRESSE); _add_text(p, "\n")
    _add_text(p, config.VILLE_PAYS); _add_text(p, "\n")
    _add_text(p, config.TEL); _pf(p, after_pt=0)

    p_mail = doc.add_paragraph(); _mailto(p_mail, config.EMAIL); _pf(p_mail, after_pt=after_email)

    p_subj = doc.add_paragraph()
    _add_text(p_subj, f"Subject: Application – {position}", bold=True); _pf(p_subj, after_pt=after_subject)

    p_greet = doc.add_paragraph()
    _add_text(p_greet, "Dear Hiring Team,"); _pf(p_greet, after_pt=after_salut)

    for para in body_paragraphs[:4]:
        pb = doc.add_paragraph(); _add_text(pb, _clean(para)); _pf(pb, after_pt=after_par)

    ps1 = doc.add_paragraph(); _add_text(ps1, "Yours sincerely,"); _pf(ps1, after_pt=after_signature)
    ps2 = doc.add_paragraph(); _add_text(ps2, config.NOM, bold=True); _pf(ps2, after_pt=0)
    return doc

def save_letter(bank: str, position: str, body_paragraphs: list[str]) -> str:
    doc = build_letter_doc(bank, position, body_paragraphs)
    out_root = os.path.join(app_dir(), _cfg("OUT_DIR", "generated_letters"))
    out_dir = os.path.join(out_root, bank)
    os.makedirs(out_dir, exist_ok=True)
    filename = f"Cover Letter - {bank} - {position.replace(' ', '_')}.docx"
    path = os.path.join(out_dir, filename)
    base, ext = os.path.splitext(path); n = 1
    while True:
        try:
            doc.save(path); break
        except PermissionError:
            path = f"{base} ({n}){ext}"; n += 1
    return path
