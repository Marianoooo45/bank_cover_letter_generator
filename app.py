# app.py 

import os
import platform
import threading
import customtkinter as ctk
<<<<<<< HEAD
from tkinter import messagebox  # fallback
=======
from tkinter import messagebox  # fallback si besoin
>>>>>>> 482caf2 (final version)

import config
import llm_body
import writer
import export_pdf as pdfmod

<<<<<<< HEAD

=======
>>>>>>> 482caf2 (final version)
# ===================== Palette =====================
C = {
    "bg":        "#000000",
    "card":      "#000000",
    "surface":   "#12161b",
    "stroke":    "#2a3139",
    "stroke2":   "#37414c",
    "text":      "#eef2f7",
    "muted":     "#a0aab6",
    "primary":   "#14e3ff",
    "primaryH":  "#3eeaff",
    "pink":      "#ff5fc1",
    "pinkH":     "#ff80cf",
    "success":   "#34d399",
    "danger":    "#ef4444",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.05)

<<<<<<< HEAD

# ===================== Utils =====================
def open_in_file_manager(path: str):
    if not path: return
=======
# ===================== Utils =====================
def open_in_file_manager(path: str):
    if not path:
        return
>>>>>>> 482caf2 (final version)
    folder = os.path.dirname(path) if os.path.isfile(path) else path
    try:
        if platform.system() == "Windows":
            os.startfile(folder)  # type: ignore
        elif platform.system() == "Darwin":
            import subprocess; subprocess.Popen(["open", folder])
        else:
            import subprocess; subprocess.Popen(["xdg-open", folder])
    except Exception:
        pass

<<<<<<< HEAD

=======
>>>>>>> 482caf2 (final version)
def _ring(widget, on=True):
    try:
        widget.configure(border_color=C["primary"] if on else C["stroke"])
    except Exception:
        pass

<<<<<<< HEAD

# ===================== Toaster & Dialog =====================
class Toast(ctk.CTkToplevel):
    def __init__(self, master, message, kind="info", timeout_ms=1800):
        super().__init__(master)
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(fg_color=C["card"])
        color = {"info": C["primary"], "success": C["success"], "error": C["danger"], "warn": C["pink"]}.get(kind, C["primary"])
        wrap = ctk.CTkFrame(self, corner_radius=10, fg_color=C["card"], border_width=2, border_color=C["stroke2"])
        wrap.pack(expand=True, fill="both")
        bar = ctk.CTkFrame(wrap, width=6, fg_color=color, corner_radius=8)
        bar.pack(side="left", fill="y", padx=(8, 0), pady=8)
        ctk.CTkLabel(wrap, text=message, text_color=C["text"], font=ctk.CTkFont(size=12)).pack(side="left", padx=12, pady=10)
        self.update_idletasks()
        x = master.winfo_rootx() + master.winfo_width() - self.winfo_width() - 24
        y = master.winfo_rooty() + master.winfo_height() - self.winfo_height() - 24
        self.geometry(f"+{x}+{y}")
        self.after(timeout_ms, self.destroy)


=======
# ===================== Dialog (compact, scrollable, redimensionnable) =====================
>>>>>>> 482caf2 (final version)
class Dialog(ctk.CTkToplevel):
    def __init__(self, master, title, message, kind="info"):
        super().__init__(master)
        self.title(title)
        self.configure(fg_color=C["card"])
<<<<<<< HEAD
        self.resizable(False, False)
        self.attributes("-topmost", True)
        color = {"info": C["primary"], "success": C["success"], "error": C["danger"], "warn": C["pink"]}.get(kind, C["primary"])
        wrap = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"], border_width=2, border_color=C["stroke2"])
        wrap.pack(expand=True, fill="both", padx=12, pady=12)
        bar = ctk.CTkFrame(wrap, width=8, fg_color=color, corner_radius=8)
        bar.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(8, 12), pady=12)
        ctk.CTkLabel(wrap, text=title, text_color=C["text"], font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1, sticky="w", pady=(12, 4))
        msg = ctk.CTkTextbox(wrap, fg_color=C["card"], text_color=C["text"], height=120, width=480, wrap="word", border_width=0)
        msg.grid(row=1, column=1, sticky="ew", pady=(0, 8))
        msg.insert("1.0", message); msg.configure(state="disabled")
        btn = ctk.CTkButton(wrap, text="OK", fg_color=color, hover_color=color, text_color=C["bg"], corner_radius=8, command=self.destroy)
        btn.grid(row=2, column=1, sticky="e", pady=(0, 12))
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = master.winfo_rootx() + (master.winfo_width() - w) // 2
        y = master.winfo_rooty() + (master.winfo_height() - h) // 2
=======
        self.attributes("-topmost", True)
        self.resizable(True, True)

        # Taille cible : ~72% de la fenêtre parente (bornée), avec minsize
        master.update_idletasks()
        mw = max(1, master.winfo_width())
        mh = max(1, master.winfo_height())
        sw, sh = master.winfo_screenwidth(), master.winfo_screenheight()

        target_w = max(720, min(int((mw or sw) * 0.72), 1280))
        target_h = max(480, min(int((mh or sh) * 0.75), 900))

        # Couleur d’accent
        color = {
            "info": C["primary"], "success": C["success"],
            "error": C["danger"],  "warn": C["pink"]
        }.get(kind, C["primary"])

        # Conteneur
        wrap = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"],
                            border_width=2, border_color=C["stroke2"])
        wrap.pack(expand=True, fill="both", padx=12, pady=12)
        wrap.grid_columnconfigure(1, weight=1)
        wrap.grid_rowconfigure(1, weight=1)

        # Barre d’accent
        bar = ctk.CTkFrame(wrap, width=10, fg_color=color, corner_radius=8)
        bar.grid(row=0, column=0, rowspan=3, sticky="ns", padx=(8, 12), pady=12)

        DLabel(wrap, title, size=16, weight="bold").grid(row=0, column=1, sticky="w", pady=(12, 6))

        # Zone de message large et scrollable (s’agrandit avec la fenêtre)
        msg = ctk.CTkTextbox(
            wrap, fg_color=C["card"], text_color=C["text"],
            border_width=0, wrap="word",
            width=target_w - 220, height=target_h - 200
        )
        msg.grid(row=1, column=1, sticky="nsew", pady=(0, 10))
        msg.insert("1.0", message)
        msg.configure(state="disabled")

        # Boutons
        def _copy():
            try:
                self.clipboard_clear(); self.clipboard_append(message)
            except Exception:
                pass

        btns = ctk.CTkFrame(wrap, fg_color="transparent")
        btns.grid(row=2, column=1, sticky="e", pady=(0, 12))
        ctk.CTkButton(btns, text="Copier", fg_color=C["surface"], hover_color="#1a222c",
                      text_color=C["text"], corner_radius=8, command=_copy).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btns, text="OK", fg_color=color, hover_color=color,
                      text_color=C["bg"], corner_radius=8, command=self.destroy).pack(side="left")

        # Taille mini et centrage
        self.minsize(680, 420)
        self.update_idletasks()
        w, h = target_w, target_h
        x = master.winfo_rootx() + max(0, (mw - w) // 2)
        y = master.winfo_rooty() + max(0, (mh - h) // 2)
>>>>>>> 482caf2 (final version)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.grab_set()


# ===================== Widgets de base =====================
class DButton(ctk.CTkButton):
    def __init__(self, master, text, variant="filled", accent="primary", **kw):
        col = C.get(accent, C["primary"])
        if variant == "filled":
            kw.setdefault("fg_color", col); kw.setdefault("hover_color", C["primaryH"] if accent == "primary" else col)
            kw.setdefault("text_color", C["bg"]); kw.setdefault("border_width", 0)
        elif variant == "outline":
            kw.setdefault("fg_color", C["surface"]); kw.setdefault("hover_color", "#1a222c")
            kw.setdefault("text_color", col); kw.setdefault("border_width", 2); kw.setdefault("border_color", col)
        else:
            kw.setdefault("fg_color", C["surface"]); kw.setdefault("hover_color", "#1a222c")
            kw.setdefault("text_color", C["text"]); kw.setdefault("border_width", 0)
        kw.setdefault("corner_radius", 10); kw.setdefault("height", 38)
        super().__init__(master, text=text, **kw)
        self.configure(text_color_disabled=C["muted"])

<<<<<<< HEAD

=======
>>>>>>> 482caf2 (final version)
class DEntry(ctk.CTkEntry):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", C["surface"]); kw.setdefault("text_color", C["text"])
        kw.setdefault("placeholder_text_color", C["muted"]); kw.setdefault("border_color", C["stroke"])
        kw.setdefault("border_width", 2); kw.setdefault("corner_radius", 10)
<<<<<<< HEAD
        super().__init__(master, **kw); self.bind("<FocusIn>", lambda _e: _ring(self, True)); self.bind("<FocusOut>", lambda _e: _ring(self, False))

=======
        super().__init__(master, **kw)
        self.bind("<FocusIn>", lambda _e: _ring(self, True))
        self.bind("<FocusOut>", lambda _e: _ring(self, False))
>>>>>>> 482caf2 (final version)

class DTextbox(ctk.CTkTextbox):
    def __init__(self, master, **kw):
        kw.setdefault("fg_color", C["surface"]); kw.setdefault("text_color", C["text"])
        kw.setdefault("border_color", C["stroke"]); kw.setdefault("border_width", 2); kw.setdefault("corner_radius", 12)
<<<<<<< HEAD
        super().__init__(master, **kw); self.bind("<FocusIn>", lambda _e: _ring(self, True)); self.bind("<FocusOut>", lambda _e: _ring(self, False))


class DLabel(ctk.CTkLabel):
    def __init__(self, master, text, size=13, weight="normal", color="text", **kw):
        kw.setdefault("text_color", C.get(color, C["text"])); kw.setdefault("font", ctk.CTkFont(size=size, weight=weight))
        super().__init__(master, text=text, **kw)


=======
        super().__init__(master, **kw)
        self.bind("<FocusIn>", lambda _e: _ring(self, True))
        self.bind("<FocusOut>", lambda _e: _ring(self, False))

class DLabel(ctk.CTkLabel):
    def __init__(self, master, text, size=13, weight="normal", color="text", **kw):
        kw.setdefault("text_color", C.get(color, C["text"]))
        kw.setdefault("font", ctk.CTkFont(size=size, weight=weight))
        super().__init__(master, text=text, **kw)

>>>>>>> 482caf2 (final version)
# ===================== Application =====================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cover Letter Generator — Dark Anthracite Neon")
        self.geometry("1120x720"); self.minsize(980, 680)
        self.configure(fg_color=C["bg"])

        # root grid : header | accent | main (weight 1) | footer
        self.grid_rowconfigure(2, weight=1); self.grid_columnconfigure(0, weight=1)

        # ----- Header -----
        header = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"])
        header.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        DLabel(header, "⚡ Générateur de lettres de motivation", size=22, weight="bold").pack(anchor="w", padx=14, pady=(12, 2))
        badges = ctk.CTkFrame(header, fg_color="transparent"); badges.pack(anchor="w", padx=14, pady=(0, 12))
        ctk.CTkLabel(badges, text=f"🧠  {getattr(config, 'MODEL','N/A')}", fg_color="#18323a", text_color=C["primary"], corner_radius=8, padx=10, pady=4).pack(side="left", padx=(0,8))
        ctk.CTkLabel(badges, text=f"📁  {getattr(config,'OUT_DIR','generated_letters')}", fg_color="#361b2b", text_color=C["pink"], corner_radius=8, padx=10, pady=4).pack(side="left")

        ctk.CTkFrame(self, height=2, fg_color=C["primary"]).grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 0))

        # ----- Main -----
        main = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"])
        main.grid(row=2, column=0, sticky="nsew", padx=16, pady=8)
        main.grid_columnconfigure(1, weight=1); main.grid_rowconfigure(0, weight=1)

        # LEFT
        left = ctk.CTkFrame(main, corner_radius=12, fg_color=C["surface"])
        left.grid(row=0, column=0, sticky="nsw", padx=12, pady=12)
        for r in range(20): left.grid_rowconfigure(r, weight=0)

        DLabel(left, "Banque", size=14, weight="bold").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        # filtre + combo (chevron natif)
<<<<<<< HEAD
        row_f = ctk.CTkFrame(left, fg_color="transparent"); row_f.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        row_f.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row_f, text="🔎", width=22, text_color=C["muted"]).grid(row=0, column=0, sticky="w")
        self.quick = DEntry(row_f, placeholder_text="Filtrer rapidement (ex: BNP, SocGen, RBC…)", width=260)
        self.quick.grid(row=0, column=1, sticky="ew"); self.quick.bind("<KeyRelease>", self._on_quick_filter)
=======
        row_f = ctk.CTkFrame(left, fg_color="transparent")
        row_f.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 6))
        row_f.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(row_f, text="🔎", width=22, text_color=C["muted"]).grid(row=0, column=0, sticky="w")
        self.quick = DEntry(row_f, placeholder_text="Filtrer rapidement (ex: BNP, SocGen, RBC…)", width=260)
        self.quick.grid(row=0, column=1, sticky="ew")
        self.quick.bind("<KeyRelease>", self._on_quick_filter)
>>>>>>> 482caf2 (final version)

        self.bank_combo = ctk.CTkComboBox(
            left, values=config.BANQUES, state="readonly", width=360,
            fg_color=C["surface"], text_color=C["text"], button_color=C["pink"], button_hover_color=C["pinkH"],
            dropdown_fg_color=C["card"], dropdown_text_color=C["text"], border_color=C["stroke2"], border_width=2, corner_radius=10
        )
        self.bank_combo.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 14))
        self.bank_combo.set(config.BANQUES[0])

        # Poste
        DLabel(left, "Poste", size=14, weight="bold").grid(row=3, column=0, sticky="w", padx=12, pady=(0, 6))
        self.position_entry = DEntry(left, placeholder_text="ex: AVP USD Structured Rates Trading")
        self.position_entry.grid(row=4, column=0, sticky="ew", padx=12, pady=(0, 12))

        # Langue
        DLabel(left, "Langue", size=14, weight="bold").grid(row=5, column=0, sticky="w", padx=12, pady=(0, 6))
        self.lang = ctk.StringVar(value="EN")
        self.lang_seg = ctk.CTkSegmentedButton(
            left, values=["EN","FR"], variable=self.lang, corner_radius=8,
            fg_color=C["surface"], selected_color="#134e58", selected_hover_color="#196b7a",
            unselected_color=C["stroke2"], unselected_hover_color="#232a32", text_color=C["text"]
        )
        self.lang_seg.grid(row=6, column=0, sticky="ew", padx=12, pady=(0, 12))

        # Switch PDF (track gris OFF, fill cyan ON)
        self.export_pdf = ctk.BooleanVar(value=True)
        self.pdf_switch = ctk.CTkSwitch(
            left, text="Exporter également en PDF", variable=self.export_pdf,
            fg_color=C["stroke2"], progress_color=C["primary"], button_color=C["card"], text_color=C["text"]
        )
        self.pdf_switch.grid(row=7, column=0, sticky="w", padx=12, pady=(0, 12))

        # Utils
        util = ctk.CTkFrame(left, fg_color="transparent")
        util.grid(row=8, column=0, sticky="ew", padx=12, pady=(4, 12))
        util.grid_columnconfigure((0,1), weight=1)
        self.btn_clear = DButton(util, "🧹  Vider (Ctrl+L)", variant="outline", accent="primary", command=self._clear_form)
        self.btn_clear.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.btn_open = DButton(util, "📂  Ouvrir dossier de sortie", variant="outline", accent="pink", command=self._open_output_dir)
        self.btn_open.grid(row=0, column=1, sticky="ew", padx=(6, 0))

        # RIGHT
        right = ctk.CTkFrame(main, corner_radius=12, fg_color=C["surface"])
        right.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)
        right.grid_rowconfigure(2, weight=1); right.grid_columnconfigure(0, weight=1)

        DLabel(right, "Annonce / Description", size=14, weight="bold").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

<<<<<<< HEAD
        tb = ctk.CTkFrame(right, fg_color="transparent"); tb.grid(row=1, column=0, sticky="ew", padx=12, pady=(0,6))
=======
        tb = ctk.CTkFrame(right, fg_color="transparent")
        tb.grid(row=1, column=0, sticky="ew", padx=12, pady=(0,6))
>>>>>>> 482caf2 (final version)
        tb.grid_columnconfigure(1, weight=1)
        self.btn_paste = DButton(tb, "📋  Coller (Ctrl+V)", variant="outline", accent="primary", command=self._paste_from_clipboard)
        self.btn_paste.grid(row=0, column=0, sticky="w")
        self.counter_var = ctk.StringVar(value="0 mots • 0 caractères")
        ctk.CTkLabel(tb, textvariable=self.counter_var, text_color=C["muted"]).grid(row=0, column=1, sticky="e")

        self.offer_text = DTextbox(right, height=420)
        self.offer_text.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.offer_text.bind("<<Modified>>", self._on_offer_modified)

        # ----- Footer (toujours visible) -----
        footer = ctk.CTkFrame(self, corner_radius=12, fg_color=C["card"])
        footer.grid(row=3, column=0, sticky="ew", padx=16, pady=(8, 16))
        footer.grid_columnconfigure(0, weight=1); footer.grid_columnconfigure(1, weight=0)

<<<<<<< HEAD
        status = ctk.CTkFrame(footer, fg_color="transparent"); status.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
=======
        status = ctk.CTkFrame(footer, fg_color="transparent")
        status.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
>>>>>>> 482caf2 (final version)
        status.grid_columnconfigure(1, weight=1)
        self.status = ctk.CTkLabel(status, text="Prêt.", text_color=C["muted"], font=ctk.CTkFont(size=12))
        self.status.grid(row=0, column=0, sticky="w", padx=(0, 12))
        self.progress = ctk.CTkProgressBar(status, height=10, progress_color=C["primary"])
        self.progress.grid(row=0, column=1, sticky="ew"); self.progress.set(0)

        self.btn_generate = DButton(footer, "⚡  Générer la lettre (Ctrl+Entrée)", variant="filled", accent="primary", command=self._on_generate)
        self.btn_generate.grid(row=0, column=1, sticky="e", padx=12, pady=12)
        self.btn_generate.configure(state="disabled", fg_color=C["stroke2"], hover_color=C["stroke2"], text_color_disabled=C["muted"])

        # Raccourcis
        self.bind_all("<Control-Return>", lambda _e: self._on_generate())
        self.bind_all("<Control-l>", lambda _e: self._clear_form())
        self.bind_all("<Control-L>", lambda _e: self._clear_form())
        self.bind_all("<Control-v>", lambda _e: self._paste_from_clipboard())
        self.bind_all("<Control-V>", lambda _e: self._paste_from_clipboard())

        self._validate_form()

    # ===================== Events =====================
    def _on_quick_filter(self, _e=None):
        q = self.quick.get().strip().lower()
        vals = [b for b in config.BANQUES if q in b.lower()] or config.BANQUES
        self.bank_combo.configure(values=vals)
        if self.bank_combo.get() not in vals:
            self.bank_combo.set(vals[0])
        self._validate_form()

    def _on_offer_modified(self, _e=None):
<<<<<<< HEAD
        try: self.offer_text.edit_modified(False)
        except Exception: pass
=======
        try:
            self.offer_text.edit_modified(False)
        except Exception:
            pass
>>>>>>> 482caf2 (final version)
        txt = self.offer_text.get("1.0", "end").strip()
        words = len([w for w in txt.split() if w.strip()])
        self.counter_var.set(f"{words} mots • {len(txt)} caractères")
        self._validate_form()

    # ===================== Actions =====================
    def _clear_form(self):
        self.quick.delete(0, "end"); self.bank_combo.set(config.BANQUES[0])
        self.position_entry.delete(0, "end")
        self.offer_text.delete("1.0", "end")
        self.counter_var.set("0 mots • 0 caractères")
        self._set_status("Formulaire réinitialisé.")
<<<<<<< HEAD
        Toast(self, "Formulaire vidé", "info", 1400)
=======
>>>>>>> 482caf2 (final version)
        self._validate_form()

    def _paste_from_clipboard(self):
        try:
            txt = self.clipboard_get()
            if txt:
<<<<<<< HEAD
                self.offer_text.insert("end", txt); self._on_offer_modified()
                self._set_status("Annonce collée."); Toast(self, "Texte collé", "success", 1200)
        except Exception:
            Toast(self, "Impossible de coller", "error", 1600)
=======
                self.offer_text.insert("end", txt)
                self._on_offer_modified()
                self._set_status("Annonce collée.")
        except Exception:
            self._set_status("Impossible de coller.")
>>>>>>> 482caf2 (final version)

    def _open_output_dir(self):
        out_root = os.path.join(self._app_dir(), getattr(config, "OUT_DIR", "generated_letters"))
        os.makedirs(out_root, exist_ok=True)
<<<<<<< HEAD
        open_in_file_manager(out_root); Toast(self, "Dossier de sortie ouvert", "info", 1400)
=======
        open_in_file_manager(out_root)
        self._set_status("Dossier de sortie ouvert.")
>>>>>>> 482caf2 (final version)

    def _validate_form(self):
        ok = all([
            (self.bank_combo.get() or "").strip(),
            (self.position_entry.get() or "").strip(),
            (self.offer_text.get("1.0", "end") or "").strip()
        ])
        self.btn_generate.configure(
            state=("normal" if ok else "disabled"),
            fg_color=(C["primary"] if ok else C["stroke2"]),
            hover_color=(C["primaryH"] if ok else C["stroke2"]),
        )
        return ok

    def _on_generate(self):
        if not self._validate_form():
<<<<<<< HEAD
            Dialog(self, "Champs manquants", "Merci de remplir banque, poste et annonce.", "warn"); return
=======
            Dialog(self, "Champs manquants", "Merci de remplir banque, poste et annonce.", "warn")
            return
>>>>>>> 482caf2 (final version)
        bank = self.bank_combo.get().strip()
        position = self.position_entry.get().strip()
        offer = self.offer_text.get("1.0", "end").strip()
        lang = self.lang.get()
<<<<<<< HEAD
        self._set_status("Envoi à GPT…"); self._progress_start(); self._toggle_controls(False)
        threading.Thread(target=self._worker, args=(bank, position, offer, lang, self.export_pdf.get()), daemon=True).start()

    def _worker(self, bank, position, offer, lang, do_pdf):
        docx_path = pdf_path = None; err = None
=======
        self._set_status("Envoi à GPT…")
        self._progress_start()
        self._toggle_controls(False)
        threading.Thread(target=self._worker, args=(bank, position, offer, lang, self.export_pdf.get()), daemon=True).start()

    def _worker(self, bank, position, offer, lang, do_pdf):
        docx_path = pdf_path = None
        err = None
>>>>>>> 482caf2 (final version)
        try:
            body = llm_body.generate_body_paragraphs(bank, position, offer, lang)
            self._set_status("Création du DOCX…")
            docx_path = writer.save_letter(bank, position, body)
            if do_pdf:
                self._set_status("Export PDF…")
<<<<<<< HEAD
                try: pdf_path = pdfmod.docx_to_pdf(docx_path)
                except Exception as e: err = f"DOCX OK. Export PDF a échoué : {e}"
        except Exception as e:
            err = str(e)

        def done():
            self._progress_stop(); self._toggle_controls(True)
            if err:
                self._set_status("Erreur."); Dialog(self, "Erreur", err, "error")
            else:
                self._set_status("Terminé.")
                msg = f"DOCX :\n{docx_path}" + (f"\n\nPDF :\n{pdf_path}" if pdf_path else "")
                Dialog(self, "Succès", msg, "success")
        self.after(0, done)

    # ===================== UI helpers =====================
    def _set_status(self, t): 
        try: self.status.configure(text=t)
        except Exception: pass

    def _progress_start(self):
        self.progress.configure(mode="indeterminate"); self.progress.start()

    def _progress_stop(self):
        self.progress.stop(); self.progress.configure(mode="determinate"); self.progress.set(0)

    def _toggle_controls(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for w in [self.quick, self.bank_combo, self.position_entry, self.lang_seg, self.pdf_switch, self.offer_text, self.btn_clear, self.btn_open, self.btn_paste, self.btn_generate]:
            try: w.configure(state=state)
            except Exception: pass

    @staticmethod
    def _app_dir() -> str:
        import sys
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))

=======
                try:
                    pdf_path = pdfmod.docx_to_pdf(docx_path)
                except Exception as e:
                    err = f"DOCX OK. Export PDF a échoué : {e}"
        except Exception as e:
            err = str(e)

        def done():
            self._progress_stop()
            self._toggle_controls(True)
            if err:
                self._set_status("Erreur.")
                Dialog(self, "Erreur", err, "error")
            else:
                self._set_status("Terminé.")
                msg = f"DOCX :\n{docx_path}" + (f"\n\nPDF :\n{pdf_path}" if pdf_path else "")
                Dialog(self, "Succès", msg, "success")
        self.after(0, done)

    # ===================== UI helpers =====================
    def _set_status(self, t):
        try:
            self.status.configure(text=t)
        except Exception:
            pass

    def _progress_start(self):
        self.progress.configure(mode="indeterminate")
        self.progress.start()

    def _progress_stop(self):
        self.progress.stop()
        self.progress.configure(mode="determinate")
        self.progress.set(0)

    def _toggle_controls(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for w in [
            self.quick, self.bank_combo, self.position_entry, self.lang_seg,
            self.pdf_switch, self.offer_text, self.btn_clear, self.btn_open,
            self.btn_paste, self.btn_generate,
        ]:
            try:
                w.configure(state=state)
            except Exception:
                pass

    @staticmethod
    def _app_dir() -> str:
        import sys
        if getattr(sys, "frozen", False):
            return os.path.dirname(sys.executable)
        return os.path.dirname(os.path.abspath(__file__))
>>>>>>> 482caf2 (final version)

if __name__ == "__main__":
    App().mainloop()
