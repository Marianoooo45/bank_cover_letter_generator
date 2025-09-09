import os, threading, inspect
import customtkinter as ctk
from tkinter import messagebox

import config
import llm_body
import writer
import export_pdf as pdfmod

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cover Letter Generator")
        self.geometry("900x680"); self.minsize(860, 640)

        main = ctk.CTkFrame(self, corner_radius=12)
        main.pack(expand=True, fill="both", padx=16, pady=16)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(main, text="Générateur de lettres de motivation",
                     font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(12, 6))

        # Banque
        ctk.CTkLabel(main, text="Banque").grid(row=1, column=0, sticky="e", padx=12, pady=6)
        self.search_entry = ctk.CTkEntry(main, placeholder_text="Rechercher une banque…")
        self.search_entry.grid(row=1, column=1, sticky="we", padx=12, pady=6)
        self.search_entry.bind("<KeyRelease>", self._filter_banks)

        self.bank_combo = ctk.CTkComboBox(main, values=config.BANQUES, state="readonly")
        self.bank_combo.grid(row=2, column=1, sticky="we", padx=12, pady=(0, 10))
        self.bank_combo.set(config.BANQUES[0])

        # Poste
        ctk.CTkLabel(main, text="Poste").grid(row=3, column=0, sticky="e", padx=12, pady=6)
        self.position_entry = ctk.CTkEntry(main, placeholder_text="ex: AVP USD Structured Rates Trading")
        self.position_entry.grid(row=3, column=1, sticky="we", padx=12, pady=6)

        # Langue
        ctk.CTkLabel(main, text="Langue").grid(row=4, column=0, sticky="e", padx=12, pady=6)
        self.lang_var = ctk.StringVar(value="EN")
        lf = ctk.CTkFrame(main, fg_color="transparent"); lf.grid(row=4, column=1, sticky="w", padx=12, pady=6)
        ctk.CTkRadioButton(lf, text="English", variable=self.lang_var, value="EN").grid(row=0, column=0, padx=(0, 12))
        ctk.CTkRadioButton(lf, text="Français", variable=self.lang_var, value="FR").grid(row=0, column=1)

        # Annonce
        ctk.CTkLabel(main, text="Annonce / Description").grid(row=5, column=0, sticky="ne", padx=12, pady=6)
        self.offer_text = ctk.CTkTextbox(main, width=720, height=360)
        self.offer_text.grid(row=5, column=1, sticky="nsew", padx=12, pady=6)

        # Bouton
        self.generate_btn = ctk.CTkButton(main, text="Générer la lettre", command=self._on_generate)
        self.generate_btn.grid(row=6, column=1, sticky="e", padx=12, pady=(8, 0))

        # Statut + progress
        self.status = ctk.CTkLabel(
            main,
            text=f"Prêt. (writer={os.path.basename(inspect.getfile(writer))}, pdf={os.path.basename(inspect.getfile(pdfmod))})",
            text_color=("gray80","gray80"),
        )
        self.status.grid(row=7, column=0, columnspan=2, sticky="w", padx=12, pady=(8, 2))
        self.progress = ctk.CTkProgressBar(main); self.progress.set(0)
        self.progress.grid(row=8, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))

    def _filter_banks(self, _e=None):
        q = self.search_entry.get().lower()
        vals = [b for b in config.BANQUES if q in b.lower()] or config.BANQUES
        self.bank_combo.configure(values=vals)
        if self.bank_combo.get() not in vals:
            self.bank_combo.set(vals[0])

    def _on_generate(self):
        bank = self.bank_combo.get().strip()
        position = self.position_entry.get().strip()
        offer = self.offer_text.get("1.0", "end").strip()
        lang = self.lang_var.get()

        if not bank or not position or not offer:
            messagebox.showwarning("Champs manquants", "Merci de remplir banque, poste et annonce.")
            return

        self.generate_btn.configure(state="disabled")
        self._set_status("Envoi à GPT…")
        self._progress_start()
        threading.Thread(target=self._worker, args=(bank, position, offer, lang), daemon=True).start()

    def _worker(self, bank, position, offer, lang):
        try:
            body = llm_body.generate_body_paragraphs(bank, position, offer, lang)
            self._set_status("Création du Word…")
            docx_path = writer.save_letter(bank, position, body)

            self._set_status("Export PDF…")
            try:
                pdf_path = pdfmod.docx_to_pdf(docx_path)
                self._set_status("Terminé. DOCX et PDF prêts.")
                messagebox.showinfo("Succès", f"DOCX :\n{docx_path}\n\nPDF :\n{pdf_path}")
            except Exception as e:
                self._set_status("DOCX OK. Export PDF a échoué.")
                messagebox.showwarning("Partiel", f"DOCX OK :\n{docx_path}\n\nPDF échec : {e}")
        except Exception as e:
            self._set_status("Erreur.")
            messagebox.showerror("Erreur", str(e))
        finally:
            self._progress_stop()
            self.generate_btn.configure(state="normal")

    def _set_status(self, t): self.status.after(0, lambda: self.status.configure(text=t))
    def _progress_start(self): self.progress.after(0, lambda: (self.progress.configure(mode="indeterminate"), self.progress.start()))
    def _progress_stop(self): self.progress.after(0, lambda: (self.progress.stop(), self.progress.configure(mode="determinate"), self.progress.set(0)))

if __name__ == "__main__":
    App().mainloop()
