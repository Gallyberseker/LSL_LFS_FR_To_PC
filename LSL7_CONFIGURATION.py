"""Configuration française et sélection des correctifs."""
import re

class LSL7_Configuration:
    def configuration(self, data):
        """Active le français et un dossier de correctifs vide dédié."""
        texte = data.decode('cp1252')
        texte, n = re.subn(r'(?im)^(\s*language\s*=\s*)\d+', r'\g<1>33', texte)
        if n != 1:
            raise RuntimeError('Réglage language absent ou ambigu.')
        texte, n = re.subn(r'(?im)^\s*patchDir\s*=.*$',
                           lambda _: 'patchDir=.\\PATCHES_FR_TEST', texte)
        if n != 1:
            raise RuntimeError('Réglage patchDir absent ou ambigu.')
        return texte.encode('cp1252')
