def extreu_ranking(font, sortida):
    """
    Donat un fitxer games.csv que conte a la 5a columna
    un ID de joc a la BGG, fa una crida a la API de BGG
    per cada ID i retorna el corresponent average_ranking.
    El resultat s'extreu en el fitxer rankings.csv
    
    Attributes
	----------
	font: str       fitxer csv amb les dades d'entrada
	sortida: str    fitxer csv amb les dades de sortida
	
	Returns: none
    """
    import csv
    from urllib.request import urlopen

    # Extreu els id de BGG del fitxer games.csv
    with open(font, encoding='latin1') as csv_file, open(sortida, 'w') as r:
        csv_reader = csv.reader(csv_file, delimiter=';')
        output = []
        urlapi = []
        rows = []
        headers = next(csv_reader)
        for row in csv_reader:
            ranking = -1
            if row[4].strip() != '':
                # per cada un dels id obtinguts, crea una url per la api
                urlapi = 'https://boardgamegeek.com/xmlapi2/thing?stats=1&id='+row[4]
                # Fer una crida a la API per cada url
                with urlopen(urlapi) as u:                         
                    data=[x.decode().strip() for x in u.readlines()]
                # afegir [id, ranking] la llista 'rows'
                for linia in data:
                    if "<average value" in linia:
                        ranking=linia.split('"')[1]
                        break
            output.append(list(row) + [ranking])

    # escriu un fitxer csv amb els id i el ranking corresponent
    with open(sortida, 'w') as r:
        write = csv.writer(r)
        write.writerow(list(headers) + ['ranking'])
        write.writerows(output)

if __name__ = '__main__':
    font = 'games.csv'
    sortida = 'games2.csv'
    extreu_ranking(font, sortida)

