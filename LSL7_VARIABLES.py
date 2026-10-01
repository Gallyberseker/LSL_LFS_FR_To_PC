"""Chemins et tailles des ressources françaises de référence."""
from pathlib import Path
BASE = Path(__file__).resolve().parent
BACKUP = BASE / 'PC_VERSION'
TEMP = BASE / 'PC_VERSION_EDIT_TEMPS'
FINI = BASE / 'PC_VERSION_EDIT_FINI'
STEAM = r'E:\SteamLibrary\steamapps\common\Larry7'
SOURCE_FR = 'F:\\'
RESSOURCES = {'RESSCI.000': 66964472, 'RESMAP.000': 8206,
              'RESMDT.000': 8206, 'RESOURCE.AUD': 345764571,
              'RESOURCE.SFX': 32072347}
