# Générateur d'attestation numérique python pour le confinement de fin 2020

Ceci est un programme CLI (command line interface) qui permet de générer des attestations numériques.

## Disclaimer

Ce générateur n'est pas officiel et pourrait contenir des données obsolètes ou incorrectes.
Vous pouvez me faire part de différences que vous voyez avec l'officiel.

## Features
Il est possible d'enregistrer des profils où seront inscrits les données fixes (nom, adresse, date de naissance,...). Ils seront enregistrés dans le dossier **profils**. 
Vous pourrez alors sélectionner ces profils et ne remplir que les informations qui changent (date, heure et motifs de la sortie).

## Installation
```bash
# Création de l'environment python
python3 -m virtualenv .venv --python=/usr/bin/python3

# Installation des dépendances
.venv/bin/pip install -r requirements.txt
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

## Changements entre le premier confinement et le reconfinement de Novembre

Deux motifs ont été ajouté : 
- Accompagnement de personnes en situation de handicap
- Accompagnement des enfants à l'école ou pour activité périscolaire

Le texte de l'attestation à quelque peut changé. Cf la branche ancien-confinement pour retrouver l'ancienne attestation (input-page1.png)

J'ai remarqué dans le code du gouv que le pdf possédait des metadata. Je ne sais pas si c'était le cas auparavant.
``` javascript
  // set pdf metadata
  pdfDoc.setTitle('COVID-19 - Déclaration de déplacement')
  pdfDoc.setSubject('Attestation de déplacement dérogatoire')
  pdfDoc.setKeywords([
    'covid19',
    'covid-19',
    'attestation',
    'déclaration',
    'déplacement',
    'officielle',
    'gouvernement',
  ])
  pdfDoc.setProducer('DNUM/SDIT')
  pdfDoc.setCreator('')
  pdfDoc.setAuthor("Ministère de l'intérieur")
```

```
> pdfinfo attestation_officielle.pdf
Title:          COVID-19 - Déclaration de déplacement
Subject:        Attestation de déplacement dérogatoire
Keywords:       covid19 covid-19 attestation déclaration déplacement officielle gouvernement
Author:         Ministère de l'intérieur
Creator:        
Producer:       DNUM/SDIT
CreationDate:   Thu Oct 29 18:27:05 2020 CET
ModDate:        Fri Oct 30 09:44:03 2020 CET
Tagged:         no
UserProperties: no
Suspects:       no
Form:           none
JavaScript:     no
Pages:          2
Encrypted:      no
Page size:      595 x 842 pts (A4)
Page rot:       0
File size:      42052 bytes
Optimized:      no
PDF version:    1.7
```

```
> pdfinfo attestation_generee_par_ce_logiciel.pdf
Title:          COVID-19 - Déclaration de déplacement
Subject:        Attestation de déplacement dérogatoire
Keywords:       covid19 covid-19 attestation déclaration déplacement officielle gouvernement
Author:         Ministère de l'intérieur
Creator:        
Producer:       DNUM/SDIT
Tagged:         no
UserProperties: no
Suspects:       no
Form:           none
JavaScript:     no
Pages:          2
Encrypted:      no
Page size:      892.8 x 1263.6 pts
Page rot:       0
File size:      335004 bytes
Optimized:      no
PDF version:    1.3
```

Il manque donc les metadata `CreationDate` & `ModDate`, et la version du PDF, la taille & le poids sont différents.

La police utilisée pour remplir le formulaire est Helvetica sur le générateur du gouvernement. J'ai gardé Arial pour ce programme, vous pouvez faire un fork et changer dans `generate_pdf.py`:

``` python
FONT = "Arial.ttf"
SMALL_LETTER_FONT = "arial.ttf"
# Deviendra
FONT = "Helevetica.ttf"
SMALL_LETTER_FONT = "helvetica.ttf"
```

## Modifications futures

- Je vais rajouter dans le prompt une vérification pour "la ville où vous êtes actuellement".
- J'aimerai aussi pouvoir ajouter un serveur mail afin de pouvoir envoyer directement l'output plutôt que de devoir se l'envoyer à chaque fois...



## CRÉDITS
Ceci est un fork de tdopierre qui a créé le générateur pdf.
https://github.com/tdopierre/AttestationNumeriqueCOVID-19
