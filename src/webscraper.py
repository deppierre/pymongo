import requests
from bs4 import BeautifulSoup
    
def get_soup(url):

    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    page = requests.get(url, headers=headers)
    if page.status_code == 200: 
        return BeautifulSoup(page.content, 'html.parser')
    else: raise Exception("HTML Error")
