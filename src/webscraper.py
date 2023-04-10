import requests
from bs4 import BeautifulSoup
    
def get_soup(url):
    page = requests.get(url)
    if page.status_code == 200: 
        return BeautifulSoup(page.content, 'html.parser')
    else: raise Exception("HTML Error")
