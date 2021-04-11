from urllib.request import urlparse
import datetime
import time

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
        self.domains[domain] = datetime.datetime.now()# -*- coding: utf-8 -*-

