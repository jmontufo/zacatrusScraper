from urllib.request import Request, urlopen, URLError, re, urlparse
import datetime
import time
from bs4 import BeautifulSoup

class BoardGame:
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
        
    def __str__(self):
        return self.name + "," + str(self.price) + "," + self.availability


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
        
def title_meta(tag):
    return tag.name == 'meta' and tag.has_attr('property') and tag['property'] == 'og:title'

def price_meta(tag):
    return tag.name == 'meta' and tag.has_attr('property') and tag['property'] == 'product:price:amount'

def availability_span(tag):
    return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'stock' and tag['class'][1] == 'available'
    
        
def scrap(html):
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())
    attributes_table = soup.find(id="product-attribute-specs-table")
    
    if attributes_table is not None:
        title_container = soup.find(title_meta)
        title = title_container['content']
        
        price_container = soup.find(price_meta)
        price = price_container['content']
        
        bg = BoardGame(title, price)        
        
        availability_container = soup.find(availability_span)
        bg.availability = availability_container.find('span').string
        
        print (bg)
    
        #falta obtenir totes les dades de attributes_table
        
def link_crawler(seed_url, link_regex, delay = 5, max_depth=2, max_downloaded_pages = 1000000):
    """Crawl from the given seed URL following links matched by link_regex
    """    
    crawl_queue = [seed_url]
    seen = {}
    seen[seed_url] = 0
    downloaded_pages = 0
    throttle = Throttle(delay)

    while crawl_queue and downloaded_pages < max_downloaded_pages:
        url = crawl_queue.pop()
        
        depth = seen[url]
        if depth != max_depth:
        
            throttle.wait(url)
            html = download(url)
            
            scrap(html)
            
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

link_crawler('https://zacatrus.es/juegos-de-mesa.html', 'https://zacatrus\.es/[^/]*\.html$', 5, 3, 3)

# if re.match('https://www.zacatrus.es/*', 'https://zacatrus.es/juegos-de-mesa/para_2.html'):
#     print('holi')
