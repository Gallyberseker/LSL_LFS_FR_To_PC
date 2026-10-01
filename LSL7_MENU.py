"""Interface graphique ; aucune copie de fichier dans ce module."""
import tkinter as tk
from tkinter import filedialog, messagebox
import LSL7_VARIABLES as V
from LSL7_CONTROLEUR import LSL7_Controleur

class LSL7_Menu:
    """Présente les chemins et les trois opérations."""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Larry 7 FR — Backup / Temp / Fini')
        self.root.geometry('760x520')
        self.jeu = tk.StringVar(value=V.STEAM)
        self.fr = tk.StringVar(value=V.SOURCE_FR)
        for titre, variable in [('Dossier Steam', self.jeu), ('Source PC française : dossier ou ISO', self.fr)]:
            tk.Label(self.root, text=titre).pack(anchor='w', padx=18, pady=(12, 2))
            ligne = tk.Frame(self.root)
            ligne.pack(fill='x', padx=18)
            tk.Entry(ligne, textvariable=variable).pack(side='left', fill='x', expand=True)
            tk.Button(ligne, text='Parcourir', command=lambda v=variable: self.choisir(v)).pack(side='right')
            if variable is self.fr:
                tk.Button(ligne, text='Choisir ISO', command=self.choisir_iso).pack(side='right')
        tk.Label(self.root, text='PC_VERSION : copie Steam originale\n'
                 'PC_VERSION_EDIT_TEMPS : préparation FR\n'
                 'PC_VERSION_EDIT_FINI : version prête à injecter\n'
                 'Ferme Larry 7 et DOSBox avant injection ou restauration.').pack(pady=12)
        self.injection_auto = tk.BooleanVar(value=True)
        tk.Checkbutton(self.root, text='Copier automatiquement dans Steam après construction réussie',
                       variable=self.injection_auto).pack(pady=5)
        for titre, fonction in [('1 — Construire la version FR', 'construire'),
                                ('2 — Injecter la version finie dans Steam', 'injecter'),
                                ('3 — Restaurer Steam', 'restaurer')]:
            tk.Button(self.root, text=titre, command=lambda f=fonction: self.action(f)).pack(pady=5)
        self.statut = tk.StringVar(value='Essai : compatibilité en jeu à confirmer.')
        tk.Label(self.root, textvariable=self.statut, wraplength=710).pack(pady=12)

    def choisir(self, variable):
        """Sélectionne un dossier."""
        dossier = filedialog.askdirectory()
        if dossier:
            variable.set(dossier)
            if variable is self.fr:
                self.action('recuperer_moteur')

    def choisir_iso(self):
        """Sélectionne une image disque française."""
        iso = filedialog.askopenfilename(title='ISO PC français Larry 7',
                                         filetypes=[('Image ISO', '*.iso')])
        if iso:
            self.fr.set(iso)
            self.action('recuperer_moteur')

    def afficher(self, texte):
        """Affiche la progression."""
        self.statut.set(texte)
        self.root.update_idletasks()

    def action(self, fonction):
        """Présente les erreurs sans fermer l'interface."""
        if fonction == 'restaurer' and (not V.BACKUP.is_dir() or
                                         not (V.BASE / 'sauvegarde.json').is_file()):
            messagebox.showinfo(
                'Aucune sauvegarde à restaurer',
                'Aucune sauvegarde Steam n’est disponible dans ce dossier.\n\n'
                'Elle sera créée lors de la première construction de la version FR.\n'
                'Si tu as déplacé le projet, remets PC_VERSION et sauvegarde.json '
                'à côté des fichiers Python.')
            return
        try:
            controleur = LSL7_Controleur(self.jeu.get(), self.fr.get(), self.afficher)
            if fonction == 'construire':
                controleur.construire(self.injection_auto.get())
            else:
                getattr(controleur, fonction)()
        except Exception as erreur:
            messagebox.showerror('Opération interrompue', str(erreur))

