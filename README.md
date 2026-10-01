LARRY 7 — LOCALISATION FRANÇAISE POUR STEAM

Outil Python modulaire pour installer les ressources et le moteur de la
version PC française de Leisure Suit Larry 7 dans la version Steam.

UTILISATION
Python 3.10 ou supérieur avec Tkinter.
Place le projet hors du dossier Steam, puis ouvre Larry7_FR_Steam.py
dans VS Code et exécute le fichier.

1. Sélectionne le dossier du jeu Steam.
2. Sélectionne un dossier ou un ISO contenant la version PC française.
   Le moteur SIER.EXE est vérifié et copié dans MOTEUR_FR.
3. Ferme Larry 7 et DOSBox, puis clique Construire.

CONSTRUCTION ET INSTALLATION
L’outil conserve une sauvegarde complète dans PC_VERSION.
Il supprime les anciens dossiers Temp et Fini, prépare la version française
dans PC_VERSION_EDIT_TEMPS, puis la finalise dans PC_VERSION_EDIT_FINI.

La copie vers Steam est automatique après une construction réussie.
Décoche cette option pour préparer la version sans l’installer.
Le bouton Injecter permet d’installer une version Fini déjà construite.
Les copies sont vérifiées par SHA-256.

SOURCE FRANÇAISE
La source doit contenir les cinq ressources FR et le moteur SIER.EXE.
Les ISO sont montés temporairement sous Windows, puis démontés.
Un ISO déjà monté reste monté.

RESTAURATION
Restaurer remet les fichiers Steam originaux depuis PC_VERSION.
Sans sauvegarde disponible, un message informatif est affiché.
Les sauvegardes de parties sont conservées.

À CONSERVER
PC_VERSION et sauvegarde.json constituent la sauvegarde originale.
Les modifications manuelles dans Temp et Fini sont effacées à chaque
reconstruction.

Aucun fichier du jeu n’est fourni avec le projet.
MOTEUR_FR, les copies du jeu et les ISO sont exclus de Git.
Prévoir l’espace nécessaire pour deux copies complètes du jeu.

Les vérifications de fichiers ne remplacent pas un test en jeu.
Après installation, lance une nouvelle partie depuis Steam.