"""Sauvegarde originale, préparation temporaire et version finie."""
from pathlib import Path
import json
import shutil
import LSL7_VARIABLES as V
import LSL7_MOTEUR as M
from LSL7_FICHIERS import sha, copie
from LSL7_CONTEXTE import LSL7_Contexte

class LSL7_Construction(LSL7_Contexte):
    """Construit la version française sans modifier Steam."""
    def construire(self):
        """Sauvegarde Steam une fois puis construit la version française."""
        jeu, fr = Path(self.jeu).resolve(), Path(self.fr).resolve()
        M.source()
        if jeu == fr or V.BASE == jeu or V.BASE.is_relative_to(jeu):
            raise RuntimeError('Place cet outil hors du dossier Steam ; sources distinctes requises.')
        if jeu == V.BASE or jeu.is_relative_to(V.BASE) or fr == V.BASE or fr.is_relative_to(V.BASE):
            raise RuntimeError('Les sources doivent être hors du dossier de cet outil.')
        for nom in ['SIER.EXE', 'RESOURCE.CFG', 'RESSCI.000', 'RESMAP.000']:
            if not (jeu / nom).is_file():
                raise RuntimeError(f'Fichier Steam absent : {nom}')
        for nom, taille in V.RESSOURCES.items():
            if not (fr / nom).is_file() or (fr / nom).stat().st_size != taille:
                raise RuntimeError(f'Ressource FR absente ou taille inattendue : {nom}')
        marqueur = V.BASE / 'sauvegarde.json'
        if V.BACKUP.exists():
            etat = json.loads(marqueur.read_text(encoding='utf-8'))
            if etat['steam'] != str(jeu):
                raise RuntimeError('Cette sauvegarde correspond à un autre dossier Steam.')
        else:
            self.configuration((jeu / 'RESOURCE.CFG').read_bytes())
            if (jeu / 'PATCHES_FR_TEST').exists():
                raise RuntimeError('PATCHES_FR_TEST existe déjà dans Steam.')
            self.afficher('Sauvegarde complète Steam vers PC_VERSION…')
            shutil.copytree(jeu, V.BACKUP)
            etat = {'steam': str(jeu), 'hashes': {n: sha(V.BACKUP / n)
                    for n in list(V.RESSOURCES) + ['RESOURCE.CFG', 'VERSION', 'SIER.EXE']}}
            marqueur.write_text(json.dumps(etat, indent=2), encoding='utf-8')
        M.sauvegarde_moteur(etat)
        for nom, attendu in etat['hashes'].items():
            if sha(V.BACKUP / nom) != attendu:
                raise RuntimeError(f'Sauvegarde modifiée : {nom}')
        cfg = self.configuration((V.BACKUP / 'RESOURCE.CFG').read_bytes())
        for dossier in (V.TEMP, V.FINI):
            if dossier.is_symlink():
                raise RuntimeError(f'Dossier de travail lié : {dossier}. Supprime le lien manuellement.')
            if dossier.exists() and not dossier.is_dir():
                raise RuntimeError(f'Le chemin de travail n’est pas un dossier : {dossier}')
        for dossier in (V.TEMP, V.FINI):
            if dossier.exists():
                self.afficher(f'Suppression de l’ancienne préparation : {dossier.name}')
                shutil.rmtree(dossier)
        self.afficher('Préparation dans PC_VERSION_EDIT_TEMPS…')
        shutil.copytree(V.BACKUP, V.TEMP)
        for nom in V.RESSOURCES:
            self.afficher(f'Copie FR et vérification : {nom}')
            copie(fr / nom, V.TEMP / nom)
        M.preparer(V.TEMP)
        (V.TEMP / 'RESOURCE.CFG').write_bytes(cfg)
        (V.TEMP / 'VERSION').write_bytes(b'1.05f\r\n')
        (V.TEMP / 'PATCHES_FR_TEST').mkdir()
        V.TEMP.rename(V.FINI)
        self.afficher('Version FR construite dans PC_VERSION_EDIT_FINI. Steam inchangé.')
