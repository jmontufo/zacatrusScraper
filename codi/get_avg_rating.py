import Throttle

def extreu_ranking(font, sortida):
    """
    Donat un fitxer 'font' que conte a la 5a columna
    un ID de joc a la BGG, fa una crida a la API de BGG
    per cada ID i retorna el corresponent average_ranking.
    El resultat s'extreu en el fitxer 'sortida'.
    
    Attributes
	----------
	font: str       fitxer csv amb les dades d'entrada
	sortida: str    fitxer csv amb les dades de sortida
	
	Returns: none
    """
    import csv
    from urllib.request import urlopen

    # Extreu els id de BGG del fitxer games.csv
    with open(font) as csv_file, open(sortida, 'w', newline='') as r:
        csv_reader = csv.reader(csv_file, delimiter=';')
        output = []
        urlapi = []
        headers = next(csv_reader)
        
        throttle = Throttle.Throttle(2)
    
        for row in csv_reader:
            
            print('Obtain ranquing for ', row[0])

            try:
                ranking = None
                if row[5].strip() != '':
                    # per cada un dels id obtinguts, crea una url per la api
                    urlapi = 'https://boardgamegeek.com/xmlapi2/thing?stats=1&id='+row[5]
                    # Fer una crida a la API per cada url                             
                    throttle.wait(urlapi)
                    with urlopen(urlapi) as u:                         
                        data=[x.decode().strip() for x in u.readlines()]
                    # afegir [id, ranking] la llista 'rows'
                    for linia in data:
                        if "<average value" in linia:
                            ranking=linia.split('"')[1]
                            ranking = ranking.replace('.', ',')
                            break
                output.append(list(row) + [ranking])
            except:
                print('Exception obtaining rating for id ', row[0])

    # escriu un fitxer csv amb els id i el ranking corresponent
    with open(sortida, 'w') as r:
        write = csv.writer(r, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        write.writerow(list(headers) + ['ranking'])
        write.writerows(output)

# if __name__ = '__main__':
font = 'games.csv'
sortida = 'games_wih_rating.csv'
extreu_ranking(font, sortida)
