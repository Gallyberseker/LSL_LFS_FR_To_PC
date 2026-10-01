"""Résout un dossier FR ou monte temporairement un ISO sous Windows."""
from contextlib import contextmanager
from pathlib import Path
import os
import subprocess
import json
import LSL7_VARIABLES as V


def trouver(racines):
    """Trouve un unique dossier contenant toutes les ressources FR."""
    candidats = set()
    for racine in racines:
        racine = Path(racine)
        dossiers = [racine]
        dossiers.extend(f.parent for f in racine.rglob('RESSCI.000'))
        for dossier in dossiers:
            if all((dossier / n).is_file() and (dossier / n).stat().st_size == t
                   for n, t in V.RESSOURCES.items()):
                candidats.add(dossier.resolve())
    if not candidats:
        raise RuntimeError('Aucun dossier ne contient les cinq ressources FR attendues.')
    if len(candidats) != 1:
        raise RuntimeError('Plusieurs versions FR trouvées : sélectionne directement le dossier voulu.')
    return candidats.pop()


def powershell(script, iso):
    """Transmet le chemin ISO comme donnée, sans interpolation de commande."""
    environnement = os.environ.copy()
    environnement['LSL7_ISO_SOURCE'] = str(iso)
    resultat = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive',
                               '-Command', script], env=environnement,
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace')
    if resultat.returncode:
        raise RuntimeError('Montage ISO Windows : ' + (resultat.stderr.strip() or resultat.stdout.strip()))
    return resultat.stdout.strip()


@contextmanager
def ouvrir(source, afficher=print):
    """Garde l'ISO monté pendant la construction et libère notre montage."""
    chemin = Path(source).expanduser().resolve()
    if chemin.is_dir():
        yield trouver([chemin])
        return
    if not chemin.is_file() or chemin.suffix.lower() != '.iso':
        raise RuntimeError('Choisis un dossier FR ou un fichier .iso existant.')
    if os.name != 'nt':
        raise RuntimeError('Le montage ISO intégré nécessite Windows ; utilise un dossier extrait.')
    prefixe = "$ErrorActionPreference='Stop'; [Console]::OutputEncoding=[Text.UTF8Encoding]::new(); "
    deja = powershell(prefixe + '(Get-DiskImage -ImagePath $env:LSL7_ISO_SOURCE).Attached', chemin).lower() == 'true'
    try:
        if not deja:
            afficher('Montage temporaire de l’ISO français…')
            powershell(prefixe + 'Mount-DiskImage -ImagePath $env:LSL7_ISO_SOURCE | Out-Null', chemin)
        sortie = powershell(prefixe + "ConvertTo-Json -Compress -InputObject @((Get-DiskImage -ImagePath $env:LSL7_ISO_SOURCE | Get-Volume | Where-Object DriveLetter | ForEach-Object { $_.DriveLetter.ToString() + ':\\' }))", chemin)
        racines = json.loads(sortie)
        if not racines:
            raise RuntimeError('ISO monté sans lettre de lecteur accessible.')
        yield trouver(racines)
    finally:
        if not deja:
            powershell(prefixe + 'Dismount-DiskImage -ImagePath $env:LSL7_ISO_SOURCE', chemin)
