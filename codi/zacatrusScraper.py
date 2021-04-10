from urllib.request import Request, urlopen, URLError, re, urlparse
import datetime
import time
from bs4 import BeautifulSoup
import csv
import requests
import json
import os


class BoardGame:
    
    """
	
    This is a class to represent a Board Game.
    
    Class Attributes
    ---------------
    
      last_id_used : int
          identifier of the last board game created
	
    Attributes
    ----------
    	name : str
    		name of the item
	   price : int
    		price at the moment of the download of the data from Zacatrus.es, in Euro
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
    
    last_id_used = 0
    
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
        
        BoardGame.last_id_used = BoardGame.last_id_used + 1
        
        self.num_id = BoardGame.last_id_used
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
          to_return: string that contains all the attributes of a BoardGame
        
        """

        to_return = str(self.num_id)
        to_return += "," + self.name
        to_return += "," + str(self.price)
        to_return += "," + self.availability
        to_return += "," + self.autor
        to_return += "," + self.BGG 
        to_return += "," + self.tematica 
        to_return += "," + self.sibuscas 
        to_return += "," + self.edad 
        to_return += "," + self.num_jugadores 
        to_return += "," + self.tiempo 
        to_return += "," + self.medidas 
        to_return += "," + self.complejidad 
        to_return += "," + self.editorial 
        to_return += "," + self.dependencia_idioma 
        to_return += "," + self.mecanica 
        to_return += "," + self.idioma
        
        return to_return
    
    def to_array(self):
        
        """
        
        Creates an array with all the attributes.
            
        Returns
        -------
          to_return: array that contains all the attributes of a BoardGame
              
        """
        
        to_return = []
        to_return.append(self.num_id)
        to_return.append(self.name)
        to_return.append(self.price)
        to_return.append(self.availability)
        to_return.append(self.autor)
        to_return.append(self.BGG)
        to_return.append(self.tematica)
        to_return.append(self.sibuscas)
        to_return.append(self.edad)
        to_return.append(self.num_jugadores)
        to_return.append(self.tiempo)
        to_return.append(self.medidas)
        to_return.append(self.complejidad)
        to_return.append(self.editorial)
        to_return.append(self.dependencia_idioma)
        to_return.append(self.mecanica)
        to_return.append(self.idioma)
        
        return to_return
    
    def build_header():
        
        """       
        
        Creates a heather with all the attributes.
            
        Returns
        -------
          to_return: array that contains all the attributes of a BoardGame
              
        """       
       
        to_return = []
        to_return.append('Num. Id')
        to_return.append('Nombre')
        to_return.append('Precio')
        to_return.append('Disponibilidad')
        to_return.append('Autor')
        to_return.append('BGG')
        to_return.append('Temática')
        to_return.append('Si Buscas...')
        to_return.append('Edad')
        to_return.append('Núm. jugadores')
        to_return.append('Tiempo de juego')
        to_return.append('Medidas')
        to_return.append('Complejidad')
        to_return.append('Editorial')
        to_return.append('Dependencia del idioma')
        to_return.append('Mecánica')
        to_return.append('Idioma')
        
        return to_return

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
        # else:
        #     print(attribute)
        
        
class Throttle:    
    
    """
	
    Class that manages the delay between downloads to the same domain
    
    Attributes
    ----------
    	delay : int
    		amount of delay between downloads for each domain
	   domains : dict
    		timestamp of when a domain was last accessed    
	
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
        
        self.delay = delay
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
                # domain has been accessed recently so need to sleep
                time.sleep(sleep_secs)
                
        # update the last accessed time
        self.domains[domain] = datetime.datetime.now()
 
def download(url, user_agent='PracticaUOC/jmontufo', num_retries=2):
    
    """
    
    Downloads a webpage using given user.
    
    Parameters
    ----------
      url : str
          url address to download
      user_agent: str
          user agent that will identify the origin of the downloads
      num_retries: int
          number of times to retry the download in case it fails
          
    Returns
    -------
        html code of the downloaded page
        
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

        
def availability_div(tag):
    
    """
    
    Function used to find the availability div with beautiful soup
	
    Parameters
    ----------
      tag : str
          tag to perform the test on
          
    Returns
    -------
        Bool with test result
        
    """
 
    return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'stock'  

def download_image(source_url, directory):
    
    """
    
    Downloads an image from a server
	
    Parameters
    ----------
      source_url : str
          Address of the image to download
      directory : str
          Directory where the image is saved
          
    Returns
    -------
        None
        
    """
    response = requests.get(source_url, stream = True)
    
    if response.status_code == 200:
        
        aSplit = source_url.split('/')
        filename = directory + aSplit[len(aSplit)-1]
        
        output = open(filename,"wb")
        
        for chunk in response:
            output.write(chunk)
            
        output.close()
        
def is_a_board_game(soup):
    
    """
    
    Determines whether the content of the page corresponds to a board game
	
    Parameters
    ----------
      soup : BeautifulSoup
          Html of the page transformed in soup
          
    Returns
    -------
        True if the pages corresponds to a board game, False otherwise
        
    """
    
    description_container = soup.find("div", class_="cn_product_visited")
    
    if description_container is None:
        return False    
    
    categories = description_container.find_all("span",class_="category")
    is_board_game = False
    
    for category in categories:
        if category.string == '/Juegos de mesa' or category.string == '/Productos/Juegos de mesa':
            is_board_game = True
    
    return is_board_game    
              
def scrap(html, download_images = False):
    
    """
    
    Scraps all the information for one game
    
    Parameters
    ----------
      html : str
          html page for one game
      download_images : boolean
          whether the images of the board game are downloaded or not
          
    Returns
    -------
        BoardGame with all the information for the game, or None if the html
        doesn't belong to a board game page.
        
    """
    
    soup = BeautifulSoup(html, 'html.parser')
    
    if is_a_board_game(soup):
                
        title_container = soup.find("meta",  property="og:title")
        
        if title_container is None:
            return None
        
        title = title_container['content']
        
        price_container = soup.find("meta",  property="product:price:amount")
        
        if price_container is None:
            return None
        
        price = price_container['content']
        
        bg = BoardGame(title, price)        
        
        availability_container = soup.find(availability_div)
        
        if availability_container is not None:
            bg.availability = availability_container.find('span').string        
        
        # Obtain the attributes from the table
        attributes_table = soup.find(id="product-attribute-specs-table")
        
        if attributes_table is not None:            
            for attribute_row in attributes_table.tbody.find_all("tr"):
                attribute_cell = attribute_row.td
                attribute_name = attribute_cell['data-th']
                attribute_value = attribute_cell.string
                
                bg.add_attribute(attribute_name, attribute_value)    
        
        if download_images:            
            # Download the images of the board game
            for script in soup.find_all("script"):
                
                script_content = script.string
                
                if script_content is not None and "mage/gallery/gallery" in script_content:
                    
                    directory = "./Pictures/" + str(bg.num_id) + "/"
                    os.mkdir(directory)
                    
                    script_in_dict = json.loads(script_content)
                    images_in_dict = script_in_dict["[data-gallery-role=gallery-placeholder]"]["mage/gallery/gallery"]["data"]
                    
                    for image_in_dict in images_in_dict:
                        if image_in_dict["type"] == "image":
                            image_url = image_in_dict["full"]
                            download_image(image_url, directory)
    
        return bg
    
    else:
        return None
        
def link_crawler(seed_url, link_regex, delay = 5, max_depth=2, max_downloaded_pages = 1000000, max_downloaded_images = 0):
    
    """
    
    Crawl from the given seed URL following links matched by link_regex.
    
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
      max_downloaded_images: int
          max number of games whose images will be downloaded
          
    Returns
    -------
      None
      
    """    
    
    crawl_queue = [seed_url]
    seen = {}
    seen[seed_url] = 0
    downloaded_pages = 0
    download_images = True
    throttle = Throttle(delay)
    
    with open('games.csv', 'w', newline='') as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(BoardGame.build_header())
    
        while crawl_queue and downloaded_pages < max_downloaded_pages:
                        
            if BoardGame.last_id_used >= max_downloaded_images:
                download_images = False
                
            url = crawl_queue.pop()
            
            depth = seen[url]
            
            if depth != max_depth:            
                throttle.wait(url)
                html = download(url)
                
                board_game = scrap(html, download_images)
                
                if board_game is not None:
                    spamwriter.writerow(board_game.to_array())
                
                downloaded_pages = downloaded_pages + 1
                
                # filter for links matching our regular expression
                for link in get_links(html):
                    if re.match(link_regex, link):
                        # check if have already seen this link
                        if link not in seen:
                            seen[link] = depth + 1
                            crawl_queue.append(link)
                
def get_links(html):
    
    """
    
    Return a list of links from html.
    
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


link_crawler('https://zacatrus.es/nemo-s-war.html', 'https://zacatrus\.es/[^/]*\.html$', 5, 3, 50, 20)
