"""Moteur français et protection du moteur Steam sauvegardé."""
import json
from pathlib import Path
import LSL7_VARIABLES as V
from LSL7_FICHIERS import sha, copie
FR_SHA = '7990057003f7326097120eacf3bee2b137e41813b22f7a8f2cf8cc5049374ecf'
STEAM_SHA = '380142ae618bf9b7c5fcebc2d6e2703ee1f64588cf84bcb017c9ae67ab740284'

def source():
    moteur = V.BASE / 'MOTEUR_FR' / 'SIER.EXE'
    if not moteur.is_file() or sha(moteur) != FR_SHA:
        raise RuntimeError('Moteur FR absent ou modifié dans MOTEUR_FR.')
    return moteur

def sauvegarde_moteur(etat):
    moteur = V.BACKUP / 'SIER.EXE'
    attendu = etat['hashes'].get('SIER.EXE')
    actuel = sha(moteur)
    if attendu is None:
        if actuel != STEAM_SHA:
            raise RuntimeError('Ancien backup : moteur Steam différent de celui fourni. Backup conservé.')
        etat['hashes']['SIER.EXE'] = actuel
        (V.BASE / 'sauvegarde.json').write_text(json.dumps(etat, indent=2), encoding='utf-8')
    elif actuel != attendu:
        raise RuntimeError('Moteur du backup modifié.')

def preparer(dossier):
    copie(source(), dossier / 'SIER.EXE')


def recuperer(dossier, afficher=print):
    """Copie le moteur vérifié depuis les fichiers PC français sélectionnés."""
    dossier = Path(dossier)
    candidats = [dossier / 'SIER.EXE']
    candidats.extend(dossier.rglob('SIER.EXE'))
    moteur = next((f for f in candidats if f.is_file() and sha(f) == FR_SHA), None)
    if moteur is None:
        raise RuntimeError('SIER.EXE français attendu introuvable dans la source sélectionnée.')
    destination = V.BASE / 'MOTEUR_FR'
    destination.mkdir(exist_ok=True)
    temporaire = destination / 'SIER.EXE.tmp'
    try:
        copie(moteur, temporaire)
        temporaire.replace(destination / 'SIER.EXE')
    finally:
        temporaire.unlink(missing_ok=True)
    afficher('SIER.EXE récupéré depuis la version FR dans MOTEUR_FR.')
