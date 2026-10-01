"""Injection des ressources et restauration de Steam."""
from pathlib import Path
import json
import shutil
import LSL7_VARIABLES as V
import LSL7_MOTEUR as M
from LSL7_FICHIERS import sha, copie
from LSL7_CONTEXTE import LSL7_Contexte

class LSL7_Injections(LSL7_Contexte):
    """Gère les modifications réversibles de Steam."""
    def verifier_cible(self):
        """Vérifie que la sauvegarde appartient au dossier Steam choisi."""
        jeu = Path(self.jeu).resolve()
        etat = json.loads((V.BASE / 'sauvegarde.json').read_text(encoding='utf-8'))
        if etat['steam'] != str(jeu):
            raise RuntimeError('Le dossier Steam ne correspond pas à la sauvegarde.')
        M.sauvegarde_moteur(etat)
        for nom, attendu in etat['hashes'].items():
            if sha(V.BACKUP / nom) != attendu:
                raise RuntimeError(f'Sauvegarde modifiée : {nom}')
        return jeu
    def injecter(self):
        """Injecte uniquement les ressources FR et la configuration préparée."""
        jeu = self.verifier_cible()
        for nom, taille in V.RESSOURCES.items():
            if (V.FINI / nom).stat().st_size != taille:
                raise RuntimeError(f'Version finie incorrecte : {nom}')
        M.preparer(V.FINI)
        self.afficher('Moteur FR préparé pour les ressources françaises.')
        try:
            (jeu / 'PATCHES_FR_TEST').mkdir(exist_ok=True)
            if any((jeu / 'PATCHES_FR_TEST').iterdir()):
                raise RuntimeError('Le dossier PATCHES_FR_TEST doit être vide.')
            for nom in list(V.RESSOURCES) + ['RESOURCE.CFG', 'VERSION', 'SIER.EXE']:
                self.afficher(f'Injection : {nom}')
                copie(V.FINI / nom, jeu / nom)
        except Exception:
            self.restaurer()
            raise
        self.afficher('Injection terminée. Lance une NOUVELLE PARTIE depuis Steam.')
    def restaurer(self):
        """Restaure les fichiers remplacés sans toucher aux sauvegardes de parties."""
        jeu = self.verifier_cible()
        for nom in list(V.RESSOURCES) + ['RESOURCE.CFG', 'VERSION', 'SIER.EXE']:
            self.afficher(f'Restauration : {nom}')
            copie(V.BACKUP / nom, jeu / nom)
        patches = jeu / 'PATCHES_FR_TEST'
        if patches.exists() and not any(patches.iterdir()):
            patches.rmdir()
        self.afficher('Steam restauré. Backup, Temp et Fini conservés.')
