# Leisure Suit Larry 7 — Drague en haute mer — FR pour Steam

Outil Python modulaire développé par **Gallyberseker** pour installer les ressources de la version **PC française** de *Leisure Suit Larry 7: Love for Sail!* dans la version **Steam**.

Le projet utilise les textes, les voix et le moteur de la version française fournie par l’utilisateur. Il ne réalise pas de traduction automatique et ne fournit aucun fichier du jeu.

## Fonctionnalités

- **Source française** : sélection d’un dossier ou d’un ISO, recherche des ressources dans les sous-dossiers.
- **Moteur FR** : récupération de `SIER.EXE` depuis la source sélectionnée, vérification de son empreinte et copie dans `MOTEUR_FR`.
- **Sauvegarde** : copie complète de la version Steam originale dans `PC_VERSION`.
- **Construction** : suppression des anciens dossiers Temp et Fini après validation, préparation dans Temp, puis création de Fini.
- **Installation** : copie automatique vers Steam après une construction réussie, ou injection manuelle de Fini.
- **Vérification** : contrôle des tailles attendues et des copies par SHA-256.
- **Restauration** : remise des fichiers Steam remplacés depuis le backup, sans remplacer les sauvegardes de parties.
- **Interface** : fenêtres de sélection, progression et message informatif si aucune sauvegarde n’est disponible.

## Installation et lancement

Prévoir **Windows**, **Python 3.10 ou supérieur avec Tkinter**, une version Steam et une version PC française contenant les cinq ressources attendues et `SIER.EXE`.

```powershell
git clone https://github.com/Gallyberseker/LSL_LFS_FR_To_PC.git
cd LSL_LFS_FR_To_PC
code .
```

Dans **VS Code**, ouvre `Larry7_FR_Steam.py` et clique sur **Exécuter le fichier Python**. Place le projet hors du dossier Steam.

## Utilisation

1. Sélectionne le dossier Steam, par exemple `E:\SteamLibrary\steamapps\common\Larry7`.
2. Sélectionne la source française avec **Parcourir** ou **Choisir ISO**. Le moteur FR est récupéré à cette sélection ; il l’est également lors de la construction si le chemin est saisi manuellement.
3. Ferme Larry 7 et DOSBox.
4. Clique sur **Construire la version FR**.
5. Après installation, lance une **nouvelle partie depuis Steam** et vérifie les textes, menus, accents et voix.

La case **Copier automatiquement dans Steam après construction réussie** est cochée par défaut. Décoche-la pour préparer Fini sans installer. Le bouton **Injecter** installe une version Fini déjà construite.

**Construire efface les anciens dossiers Temp et Fini, y compris leurs modifications manuelles.** Le backup original est conservé. Si la validation de la source ou du backup échoue, ces dossiers ne sont pas supprimés.

## Source française et ISO

Les cinq ressources attendues sont `RESSCI.000`, `RESMAP.000`, `RESMDT.000`, `RESOURCE.AUD` et `RESOURCE.SFX`. La source doit également fournir le moteur français `SIER.EXE` correspondant à l’empreinte reconnue par l’outil.

Sous Windows, l’ISO est monté temporairement à l’aide de PowerShell. Les fichiers nécessaires sont copiés avant le démontage. Un ISO déjà monté reste monté. Si Windows refuse le montage, monte ou extrais l’ISO puis sélectionne le dossier des fichiers.

## Dossiers principaux

| Élément | Rôle |
| --- | --- |
| `PC_VERSION` | Sauvegarde complète originale de Steam |
| `sauvegarde.json` | Chemin Steam et empreintes des fichiers sauvegardés |
| `PC_VERSION_EDIT_TEMPS` | Préparation temporaire |
| `PC_VERSION_EDIT_FINI` | Version française prête à installer |
| `MOTEUR_FR/SIER.EXE` | Moteur récupéré depuis la source française |

Conserve **PC_VERSION et sauvegarde.json** ensemble, à côté des modules Python. Prévoir l’espace nécessaire pour deux copies complètes du jeu en plus de l’installation Steam.

## Restauration et contrôles

Ferme le jeu et DOSBox, puis clique sur **Restaurer Steam**. L’outil restaure les ressources remplacées, `RESOURCE.CFG`, `VERSION` et `SIER.EXE`. Sans backup ou sans `sauvegarde.json`, il affiche un message informatif.

Pendant l’installation française, les correctifs anglais restent présents mais sont désactivés par une configuration pointant vers le dossier vide `PATCHES_FR_TEST`. Une erreur pendant les copies d’injection déclenche une tentative de restauration des fichiers originaux.

La réussite des contrôles de fichiers ne garantit pas la compatibilité en jeu. Le moteur FR est utilisé avec ses ressources pour traiter le problème de contrôle de version rencontré avec le moteur Steam ; le résultat doit être vérifié sur le PC de l’utilisateur.

## Architecture

| Module | Rôle |
| --- | --- |
| `Larry7_FR_Steam.py` | Démarrage |
| `LSL7_MENU.py` | Interface graphique |
| `LSL7_CONTROLEUR.py` | Orchestration |
| `LSL7_VARIABLES.py` | Chemins et constantes |
| `LSL7_CONTEXTE.py` | Paramètres partagés |
| `LSL7_SOURCE_FR.py` | Dossiers et montage ISO |
| `LSL7_MOTEUR.py` | Récupération et contrôle du moteur |
| `LSL7_CONSTRUCTION.py` | Backup, Temp et Fini |
| `LSL7_INJECTIONS.py` | Installation et restauration |
| `LSL7_CONFIGURATION.py` | Langue et correctifs |
| `LSL7_FICHIERS.py` | Copies et empreintes |

## Licence et droits des tiers

**Copyright © 2026 Gallyberseker. Tous droits réservés sur ses contributions originales.** Voir le fichier [licence](licence).

L’utilisation personnelle de l’outil est gratuite. Sous réserve des droits impératifs prévus par la loi et des conditions de la plateforme d’hébergement, la modification, la redistribution, la publication de versions modifiées et la réutilisation du code nécessitent l’autorisation écrite préalable de l’auteur. La consultation publique du code ne constitue pas une licence générale de réutilisation.

**Leisure Suit Larry**, **Love for Sail!**, **Drague en haute mer**, **Sierra** et les noms, logos, personnages et ressources associés restent soumis aux droits de leurs titulaires respectifs. Steam est une marque de Valve Corporation. Les outils et bibliothèques tiers conservent leurs propres licences.

Ce projet est indépendant et n’est ni affilié, ni approuvé, ni sponsorisé par les ayants droit du jeu ou par Valve.

## Ressources et distribution

Le dépôt fournit uniquement le code de l’outil. Les exécutables, images disque, archives propriétaires et versions reconstruites contenant des ressources du jeu ne doivent pas être publiés ou redistribués sans les autorisations requises.

`PC_VERSION`, `PC_VERSION_EDIT_TEMPS`, `PC_VERSION_EDIT_FINI`, `MOTEUR_FR`, `sauvegarde.json` et les ISO doivent rester exclus de Git.

Les données doivent provenir de copies obtenues légalement. La possession du jeu et l’usage personnel n’accordent pas, à eux seuls, une autorisation générale d’adaptation ou de redistribution.

Le logiciel est fourni en l’état, sans garantie de fonctionnement ou de compatibilité, dans les limites permises par la loi. Conserve les données originales avant tout traitement.

## Auteur

**Gallyberseker** — [GitHub](https://github.com/Gallyberseker/LSL_LFS_FR_To_PC)
