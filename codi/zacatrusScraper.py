from urllib.request import Request, urlopen, URLError, re, urlparse
import datetime
import time
from bs4 import BeautifulSoup
import csv
import requests
import json
import os


class BoardGame:
    
    num_id = 0
    
    def __init__(self, name, price):
        
        BoardGame.num_id = BoardGame.num_id + 1
        
        self.num_id = BoardGame.num_id
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
        toreturn = str(self.num_id)
        toreturn = toreturn + "," + self.name
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
        
        toreturn = []
        toreturn.append(self.num_id)
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
        
        toreturn = []
        toreturn.append('Num. Id')
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
    """Add a delay between downloads to the same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}
    
    def wait(self, url):
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
    return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'stock'  

def load_requests(source_url, folder):
    r = requests.get(source_url, stream = True)
    if r.status_code == 200:
        aSplit = source_url.split('/')
        ruta = folder + aSplit[len(aSplit)-1]
        print(ruta)
        output = open(ruta,"wb")
        for chunk in r:
            output.write(chunk)
        output.close()
      
        
def scrap(html):
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
    
        # Main image, usually a video, so it's not the main image of the game
        # image = soup.find("img", alt="main product photo")
        # load_requests(image.get('src'))
        
        
        for script in soup.find_all("script"):
            script_content = script.string
            if script_content is not None and "mage/gallery/gallery" in script_content:
                
                folder = "./Pictures/" + str(bg.num_id) + "/"
                os.mkdir(folder)
                
                script_in_dict = json.loads(script_content)
                images_in_dict = script_in_dict["[data-gallery-role=gallery-placeholder]"]["mage/gallery/gallery"]["data"]
                
                for image_in_dict in images_in_dict:
                    if image_in_dict["type"] == "image":
                        image_url = image_in_dict["full"]
                        load_requests(image_url, folder)
    
        return bg
    
    return None
        
def link_crawler(seed_url, link_regex, delay = 5, max_depth=2, max_downloaded_pages = 1000000):
    """Crawl from the given seed URL following links matched by link_regex
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
    """Return a list of links from html
    """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)

#print(download('http://www.zacatrus.com'))
#crawl_sitemap('https://zacatrus.es/pub/media/sitemap.xml',10)

link_crawler('https://zacatrus.es/juegos-de-mesa', 'https://zacatrus\.es/[^/]*\.html$', 5, 3, 50)
