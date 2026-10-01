"""Paramètres communs aux services du projet."""
from LSL7_CONFIGURATION import LSL7_Configuration

class LSL7_Contexte(LSL7_Configuration):
    """Transmet les chemins et les messages de progression."""
    def __init__(self, jeu, fr, progression=print):
        """Initialise les sources et le rappel de progression."""
        self.jeu = jeu
        self.fr = fr
        self.afficher = progression
