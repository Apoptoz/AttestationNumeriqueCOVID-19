# AttestationNumeriqueCOVID-19
Générateur d'attestation numérique dérogatoire pour le confinement dû au Covid-19

## Features
Il est possible d'enregistrer des profils où seront inscrits les données fixes (nom, adresse, date de naissance,...). Ils seront enregistrés dans le dossier **profils**. 
Vous pourrez alors sélectionner ces profils et ne remplir que les informations qui changent (date, heure et motifs de la sortie).

## Installation
```bash
# Création de l'environment python
python3 -m virtualenv .venv --python=/usr/bin/python3

# Installation des dépendances
.venv/bin/pip install -r requirements 
```

## Utilisation

### Avec prompt
```bash
python register_info.py
```

Puis suivez les instructions.

### Sans prompt
```bash
.venv/bin/python generate_pdf.py \
	--first-name John \
	--last-name Doe \
	--birth-date 01/01/1900 \
	--birth-city Paname \
	--address "12 GRANDE RUE 75666 Paname" \
	--current-city Paname \
	--leave-date 06/04/2020 \
	--leave-hour 15:00 \
	--motifs travail-courses-sante-famille-sport-judiciaire-missions
```

L'attestation est ensuite disponible dans le fichier `output.pdf`.


## CRÉDITS
Ceci est un fork de tdopierre qui a créé le générateur pdf.
https://github.com/tdopierre/AttestationNumeriqueCOVID-19
