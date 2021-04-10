from urllib.request import Request, urlopen, URLError, re, urlparse
import datetime
import time
from bs4 import BeautifulSoup
import csv



class BoardGame:
   	"""
	This is a class to represent a Board Game.

	Attributes
	----------
	name : str
		name of the item
	price : int
		price at the moment of the download of the data from 			Zacatrus.es, in Euro
	availability : str
		tells if the game is avaiable for purchase at the website or not
	autor : str
		creator of the game
        BGG : int
		id of the game in BGG database
        tematica : str
		topics that appear in the game, as culture, trade, etc. Can have multiple values
        sibuscas : str
		tags to find the game e.g. family, party, etc. Can have multiple values
        edad : str
		recommended players' age, grouped in intervals. Can have multiple values
        num_jugadores : str
		minimum and maximum number of players
        tiempo : str
		average duration of a game
        medidas : str
		size of the packaging
        complejidad : str
		tells if the game is easy, medium or difficult to play
        editorial : str
		publisher of the game
        dependencia_idioma : str
		tells if it is necessary to know the laguage of the game to play, ranked in: not necessary / only instructions / highly necessary
        mecanica : str
		game's mechanism (e.g. question-answer, crawler, etc.). Can have multiple values
        idioma : str
		language of the game
    		
	"""
    
    def __init__(self, name, price):
	"""
	Constructs all the necessarty attributes for the BoardGame object
	
	Parameters
	----------
		name: str
			name of the game
		price: int
			price of the game
	Returns
	-------
	None
	"""

        self.name = name
        self.price = price
        self.availability = ''
        self.autor = ''
        self.BGG = ''
        self.tematica = ''
        self.sibuscas = ''
        self.edad = ''
        self.num_jugadores = ''
        self.tiempo = ''
        self.medidas = ''
        self.complejidad = ''
        self.editorial = ''
        self.dependencia_idioma = ''
        self.mecanica = ''
        self.idioma = ''
        
    def __str__(self):
	"""
	Creates a string with all the attributes separated by commas.

	Returns
	-------
	toreturn: string that contains all the attributes of a BoardGame
	"""

        toreturn = self.name
        toreturn = toreturn + "," + str(self.price)
        toreturn = toreturn + "," + self.availability
        toreturn = toreturn + "," + self.autor
        toreturn = toreturn + "," + self.BGG 
        toreturn = toreturn + "," + self.tematica 
        toreturn = toreturn + "," + self.sibuscas 
        toreturn = toreturn + "," + self.edad 
        toreturn = toreturn + "," + self.num_jugadores 
        toreturn = toreturn + "," + self.tiempo 
        toreturn = toreturn + "," + self.medidas 
        toreturn = toreturn + "," + self.complejidad 
        toreturn = toreturn + "," + self.editorial 
        toreturn = toreturn + "," + self.dependencia_idioma 
        toreturn = toreturn + "," + self.mecanica 
        toreturn = toreturn + "," + self.idioma
        
        return toreturn
    
    def to_array(self):
 	"""
	Creates an array with all the attributes.

	Returns
	-------
	toreturn: array that contains all the attributes of a BoardGame
	"""       
        toreturn = []
        toreturn.append(self.name)
        toreturn.append(self.price)
        toreturn.append(self.availability)
        toreturn.append(self.autor)
        toreturn.append(self.BGG)
        toreturn.append(self.tematica)
        toreturn.append(self.sibuscas)
        toreturn.append(self.edad)
        toreturn.append(self.num_jugadores)
        toreturn.append(self.tiempo)
        toreturn.append(self.medidas)
        toreturn.append(self.complejidad)
        toreturn.append(self.editorial)
        toreturn.append(self.dependencia_idioma)
        toreturn.append(self.mecanica)
        toreturn.append(self.idioma)
        
        return toreturn
    
    def build_header():
  	"""
	Creates a heather with all the attributes.

	Returns
	-------
	toreturn: array that contains all the attributes of a BoardGame
	"""       
       
        toreturn = []
        toreturn.append('Nombre')
        toreturn.append('Precio')
        toreturn.append('Disponibilidad')
        toreturn.append('Autor')
        toreturn.append('BGG')
        toreturn.append('Temática')
        toreturn.append('Si Buscas...')
        toreturn.append('Edad')
        toreturn.append('Núm. jugadores')
        toreturn.append('Tiempo de juego')
        toreturn.append('Medidas')
        toreturn.append('Complejidad')
        toreturn.append('Editorial')
        toreturn.append('Dependencia del idioma')
        toreturn.append('Mecánica')
        toreturn.append('Idioma')
        
        return toreturn

    def add_attribute(self, attribute, value):
 	"""
	Sets the value for a given attribute.

	Parameters
	----------
	attribute : str
		attribute of the game
	value : str
		value for the given attribute

	Returns
	-------
	None
	"""       

        if attribute == 'Autor':
            self.autor = value
        elif attribute == 'BGG':
            self.BGG = value
        elif attribute == 'Temática':
            self.tematica = value
        elif attribute == 'Si buscas...':
            self.sibuscas = value
        elif attribute == 'Edad':
            self.edad = value
        elif attribute == 'Núm. jugadores':
            self.num_jugadores = value
        elif attribute == 'Tiempo de juego':
            self.tiempo = value
        elif attribute == 'Medidas':
            self.medidas = value
        elif attribute == 'Complejidad':
            self.complejidad = value
        elif attribute == 'Editorial':
            self.editorial = value
        elif attribute == 'Dependencia del idioma':
            self.dependencia_idioma = value
        elif attribute == 'Mecánica':
            self.mecanica = value
        elif attribute == 'Idioma':
            self.idioma = value
        else:
            print(attribute)
        
        
class Throttle:
 	"""
	Adds a delay between downloads to the same domain
 	"""

    def __init__(self, delay):
	"""
	Sets the delay between downloads for each domain.
	Creates a dictionary called 'domains' that contains the timestamp when a domain was last accessed.
	Parameters
	----------
	delay : int
		number of seconds

	Returns
	-------
	None
	"""        
	# amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
    
    def wait(self, url):
 	"""
	Given a certain delay, tells if the request to an url needs to wait. If not, updates last_accessed time.

	Parameters
	----------
	url : str
		url addres to parse

	Returns
	-------
	None
	"""

        domain = urlparse(url).netloc
        last_accessed = self.domains.get(domain)
        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                # domain has been accessed recently
                # so need to sleep
                time.sleep(sleep_secs)
        # update the last accessed time
        self.domains[domain] = datetime.datetime.now()
 
def download(url, user_agent='PracticaUOC/jmontufo', num_retries=2):
 	"""
	Downloads a webpage using given user.

	Parameters
	----------
	url : str
		url addres to download
	user_agent: str
		url user
	num_retries: int
		number of times to retry the download in case it fails

	Returns
	-------
	html code
	"""

    print('Downloading:', url)
    headers = {'User-agent': user_agent}
    request = Request(url, headers=headers)
    try:
        html = urlopen(request).read()
        html = html.decode('utf-8')
    except URLError as e:
        print('Download error:', e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, user_agent, num_retries-1)
    return html

def crawl_sitemap(url, max_downloaded_pages = 1000000):
 	"""
	Downloads the sitemap file, extracts the links, downloads them.

	Parameters
	----------
	url : str
		url addres of the sitemap
	max_downloaded_pages: int
		max number of pages to download

	Returns
	-------
	none
	"""
    downloaded_pages = 0
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    # download each link
    for link in links:
        if downloaded_pages > max_downloaded_pages:
            return
        print(download(link))
        downloaded_pages = downloaded_pages + 1
        
def availability_span(tag):
 	"""
    Checks if 'tag' is a div of class 'stock'

	Parameters
	----------
	tag : str
        tag to perform the test on
        
	Returns
	-------
	Bool with test result
	"""
  
    return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'stock'    
        
def scrap(html):
 	"""
    Scraps all the information for one game

	Parameters
	----------
	html : str
        html page for one game
        
	Returns
	-------
	Object of class 'bg' with all the information for the game, or None.
	"""
    soup = BeautifulSoup(html, 'html.parser')
    
    description = soup.find("div", class_="cn_product_visited")
    
    if description is None:
        return None
    
    
    categories = description.find_all("span",class_="category")
    is_board_game = False
    
    for category in categories:
        if category.string == '/Juegos de mesa':
            is_board_game = True
    
    if not is_board_game:
        return None
    
    attributes_table = soup.find(id="product-attribute-specs-table")
    
    if attributes_table is not None:
        # title_container = soup.find(title_meta)
        # title = title_container['content']
        
        title_container = soup.find("meta",  property="og:title")
        title = title_container['content']
        
        price_container = soup.find("meta",  property="product:price:amount")
        price = price_container['content']
        
        bg = BoardGame(title, price)        
        
        availability_container = soup.find(availability_span)
        bg.availability = availability_container.find('span').string
        
        for attribute_row in attributes_table.tbody.find_all("tr"):
            attribute_cell = attribute_row.td
            attribute_name = attribute_cell['data-th']
            attribute_value = attribute_cell.string
            
            bg.add_attribute(attribute_name, attribute_value)
        
        return bg
    
    return None
        
def link_crawler(seed_url, link_regex, delay = 5, max_depth=2, max_downloaded_pages = 1000000):
    """Crawl from the given seed URL following links matched by link_regex.
    
    Parameters
	----------
	seed_url : str
        base url for the site
    link_regex: str
        regex to match the links to crawl
    delay: int
        delay between downloads
    max_depth: int
        do not follow links above this depth
    max_downloaded_pages: int
        max number of pages to download
    
    Returns
	-------
	None
    """    
    crawl_queue = [seed_url]
    seen = {}
    seen[seed_url] = 0
    downloaded_pages = 0
    throttle = Throttle(delay)
    with open('games.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(BoardGame.build_header())
    
        while crawl_queue and downloaded_pages < max_downloaded_pages:
            url = crawl_queue.pop()
            
            depth = seen[url]
            if depth != max_depth:
            
                throttle.wait(url)
                html = download(url)
                
                game = scrap(html)
                
                if game is not None:
                    spamwriter.writerow(game.to_array())
                
                downloaded_pages = downloaded_pages + 1
                
                # filter for links matching our regular expression
                for link in get_links(html):
                    if re.match(link_regex, link):
                        # check if have already seen this link
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
                
def get_links(html):
    """Return a list of links from html.
        
    Parameters
	----------
    html: str
        html code for the page where links have to be found
        
    Returns
	-------
	List with all links found
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

#print(download('http://www.zacatrus.com'))
#crawl_sitemap('https://zacatrus.es/pub/media/sitemap.xml',10)

link_crawler('https://zacatrus.es/juegos-de-mesa', 'https://zacatrus\.es/[^/]*\.html$', 5, 3, 50)

# if re.match('https://www.zacatrus.es/*', 'https://zacatrus.es/juegos-de-mesa/para_2.html'):
#     print('holi')
