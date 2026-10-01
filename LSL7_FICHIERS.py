"""Copies vérifiées par SHA-256."""
import hashlib
import shutil

def sha(path):
    """Calcule l'empreinte d'un fichier par blocs."""
    h = hashlib.sha256()
    with path.open('rb') as flux:
        for bloc in iter(lambda: flux.read(1024 * 1024), b''):
            h.update(bloc)
    return h.hexdigest()

def copie(source, cible):
    """Copie et vérifie les octets transférés."""
    shutil.copyfile(source, cible)
    if sha(source) != sha(cible):
        raise RuntimeError(f'Copie incorrecte : {cible.name}')
