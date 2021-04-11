# Web Scraper per a l'obtenció de jocs de taula de la botiga online Zacatrus


## Autors

- Marta Montclus 
- Jose Montufo

## Descripció del contingut

- codi/zacatrusScraper.py --> Codi que realitza la tasca de scraping al lloc web de Zacatrus.es per realitzar un dataset amb el seu catàleg.
- codi/get_avg_rating.py --> Codi que afegeix una columna al dataset amb la valoració dels usuaris a la base de dades de la BoardGameGeek, si la valoració es troba disponible.
- codi/Throttle.py --> Classe que permet afegir una espera entre crides a un mateix domini, per tal de no saturar el lloc web al qual es fa web scraping.
- PRA1_montufo_montclus.pdf --> Documentació de la pràctica 
- games.csv --> Dataset obtingut després de fer web scraping a Zacatrus.es
- games_with_ratings.csv --> Dataset obtingut a partir d'afegir la valoració de la BGG al jocs obtinguts de Zacatrus.es

