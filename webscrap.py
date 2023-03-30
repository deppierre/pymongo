import requests
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url="", group=""):
        self.url = url
        self.group = group
        self.groups = {
            "NSWNP": "https://www.nationalparks.nsw.gov.au/conservation-and-heritage/national-parks"
        }
        self.locations = []
        
        if not self.group and not self.url:
            raise Exception("You need to provide either an url or a group")

        if self.group: 
            self.url = self.groups[self.group]
    
    def get_soup(self):
        page = requests.get(self.url)
        if page.status_code == 200: return BeautifulSoup(page.content, 'html.parser')
        else: raise Exception("HTML Error")
