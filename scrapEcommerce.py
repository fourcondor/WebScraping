import requests
from bs4 import BeautifulSoup
import re
import csv

lista_item = []
what_cms = "https://whatcms.org/?s="


# def leggi_file_csv(nome_file):
#     dati = []
#     with open(nome_file, 'r') as file_csv:
#         lettore = csv.reader(file_csv)
#         for riga in lettore:
#             dati.append(riga)
#     return dati


# Esempio di utilizzo
# nome_file_csv = 'reportAmazon.csv'
# dati_csv = leggi_file_csv(nome_file_csv)
# for riga in dati_csv:
#     if riga[7] == 'Amazon':
#         print(riga[3])
#         lista_item.append(riga[3])


def ricerca_e_commerce(item):
    e_commerces = []
    print("--------INIZIO RICERCA E-COMMERCE------------")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    query = {'q': f"{item} -site:amazon.it"}
    google_url = 'https://www.google.com/search'
    html = requests.get(google_url, headers=headers, params=query)
    soup = BeautifulSoup(html.content, 'html.parser')
    links = soup.find_all("div", attrs={'class': "yuRUbf"})
    e_commerces.append(item)
    for link_i in links:
        href = link_i.a.get('href')
        print(href)
        e_commerces.append(href)
    print(f"Fine ITEM {item}")
    print("------FINE---------")
    return e_commerces[1:]
