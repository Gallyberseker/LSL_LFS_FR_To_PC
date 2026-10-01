"""Orchestration des services depuis l'interface."""
from LSL7_SOURCE_FR import ouvrir
import LSL7_MOTEUR as M
from LSL7_CONSTRUCTION import LSL7_Construction
from LSL7_INJECTIONS import LSL7_Injections

class LSL7_Controleur:
    """Relie les actions utilisateur aux services."""
    def __init__(self, jeu, fr, progression):
        """Configure les deux services avec les mêmes chemins."""
        self.construction = LSL7_Construction(jeu, fr, progression)
        self.injections = LSL7_Injections(jeu, fr, progression)

    def recuperer_moteur(self):
        """Récupère le moteur dès la sélection de la source FR."""
        with ouvrir(self.construction.fr, self.construction.afficher) as dossier:
            M.recuperer(dossier, self.construction.afficher)

    def construire(self, injecter_automatiquement=True):
        """Prépare la version française."""
        with ouvrir(self.construction.fr, self.construction.afficher) as dossier:
            M.recuperer(dossier, self.construction.afficher)
            LSL7_Construction(self.construction.jeu, str(dossier),
                              self.construction.afficher).construire()
        if injecter_automatiquement:
            self.injections.injecter()

    def injecter(self):
        """Installe la version finie."""
        self.injections.injecter()

    def restaurer(self):
        """Rétablit les ressources Steam originales."""
        self.injections.restaurer()
