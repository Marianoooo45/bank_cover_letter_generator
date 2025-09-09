# export_pdf.py — Conversion DOCX -> PDF
# Tente d’abord avec Microsoft Word (via COM sur Windows).
# Si échec, bascule sur LibreOffice (mode headless).
import os, time, subprocess

def _ensure_dir(path):
    """Crée le dossier cible si nécessaire (par ex. pour accueillir le PDF)."""
    d = os.path.dirname(path)
    if d and not os.path.isdir(d):
        os.makedirs(d, exist_ok=True)

def docx_to_pdf(docx_path: str) -> str:
    """Convertit un fichier DOCX en PDF.
    - Si Word est dispo (Windows), on l’utilise via COM.
    - Sinon, fallback LibreOffice en mode ligne de commande.
    """
    if not os.path.isfile(docx_path):
        raise FileNotFoundError(docx_path)

    abs_docx = os.path.abspath(docx_path)
    base, _ = os.path.splitext(abs_docx)
    pdf_path = base + ".pdf"
    _ensure_dir(pdf_path)

    # Tentative 1 : Microsoft Word (COM Windows)
    try:
        import win32com.client
        from win32com.client import gencache, constants

        try:
            # Initialise le cache COM proprement (utile si première utilisation)
            gencache.EnsureDispatch("Word.Application")
            word = win32com.client.Dispatch("Word.Application")
        except Exception:
            # Si EnsureDispatch échoue, on tente un Dispatch direct
            word = win32com.client.Dispatch("Word.Application")

        # On garde Word invisible et silencieux
        word.Visible = False
        word.DisplayAlerts = 0

        # Ouverture du DOCX et export direct en PDF
        doc = word.Documents.Open(abs_docx)
        doc.SaveAs(pdf_path, FileFormat=constants.wdFormatPDF)
        doc.Close(False)
        word.Quit()
        time.sleep(0.2)  # petit délai pour laisser Word finir son boulot

        if not os.path.isfile(pdf_path):
            raise RuntimeError("Word a terminé sans produire de PDF.")

        return pdf_path

    # Si Word n’est pas dispo ou plante, on passe à LibreOffice
    except Exception as e_word:
        soffice = _find_soffice()
        if soffice is None:
            raise RuntimeError(f"Impossible de convertir : Word a échoué ({e_word}) et LibreOffice est introuvable.")

        out_dir = os.path.dirname(base)
        cmd = [soffice, "--headless", "--convert-to", "pdf", "--outdir", out_dir, abs_docx]
        proc = subprocess.run(cmd, capture_output=True, text=True)

        if proc.returncode != 0:
            raise RuntimeError(f"LibreOffice a échoué: {proc.stderr.strip() or proc.stdout.strip()}")

        if not os.path.isfile(pdf_path):
            raise RuntimeError("LibreOffice n'a pas produit de PDF.")

        return pdf_path

def _find_soffice():
    """Cherche l’exécutable LibreOffice (soffice.exe) dans les chemins connus + le PATH."""
    candidates = [
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    for p in os.environ.get("PATH", "").split(os.pathsep):
        exe = os.path.join(p, "soffice.exe")
        if os.path.isfile(exe):
            return exe
    return None
