# SNT-webservijer
Ur servijer Web simpl evit an SNT el lise Diwan

## Installation
 * Créer une arborescence pour stocker les pages web : un dossier racine et un sous-dossier par groupe dans le dossier racine.
 * Définir où les pages des élèves seront stockées en modifiant la variable ROOT_FOLDER du fichier update_index.py
 * Pour chaque sous-dossier du dossier ROOT_FOLDER, définir un script pour lancer un server de fichier droopy avec un numéro de port différent.
 * Modifier le dictionnaire UPLOAD_SERVERS DU FICHIER du fichier update_index pour indiquer le numéro de port de chaque serveur droopy.

## Utilisation
 * Executer le script "update_index.py" si des modifications ont étés apportés aux pages sans avoir été téléversées par droopy.
 * Ajouter (manuellement) le tag <meta name="author" content="Jeanne & Jean"> à chaque page
 * Lancer le script "prizian.py" pour générer la page où sera listé qui note quel groupe (ce script n'est a lancer qu'une fois, lorsque toutes les pages auront été marquées avec le tag d'auteur).

## Variable NOTES_FILE
(à définir dans update_index.py)
Permet d'afficher des remarques dans la colonne de diagnostique
