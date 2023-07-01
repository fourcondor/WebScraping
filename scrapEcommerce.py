import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
import scraping
import time





def ricerca_e_commerce(item):
    # INIT
    API_KEY = 'AIzaSyCJEQcHyw6u1llI678mO5BlsKCNAYr7kGQ'
    service = build('customsearch', 'v1', developerKey=API_KEY)
    CUSTOM_SEARCH_ENGINE_ID = '85f179deb03424abc'
    # FINE INIT
    e_commerces = []
    print("--------INIZIO RICERCA E-COMMERCE------------")
    query = f"{item} -site:amazon.it -site:ebay.it -site:trovaprezzi.it -site:collistar.it -site:amazon.com -site:idealo.it -inurl:\"category/sponsored-post\""
    result = service.cse().list(q=query, cx=CUSTOM_SEARCH_ENGINE_ID, num=10).execute()
    oggetti = result['items']
    for oggetto in oggetti:
        print('Title: {}'.format(oggetto['title']))
        print('Link: {}'.format(oggetto['link']))
        e_commerces.append(oggetto['link'])
        print('---')
    print(f"Fine ITEM {item}")
    print("------FINE---------")
    return e_commerces[:]
