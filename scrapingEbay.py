import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests
import re
import html
import unicodedata
import scraping

# Crea il dizionario con gli attributi
azienda = {
    'EAN': None,
    'MPN': None,
    'Vetrina': None,
    'Marca': None,
    'Nome prodotto': None,
    'Prezzo': None,
    'Colore': None,
    'Tipo': None,
    'Nome azienda:': None,
    'N. Feed Back': None,
    'Numero Partita IVA:': '',
    'Informazioni sul venditore professionale': '',
    'Emails': []
}


# COOKIE
cookie_value = 'BAQAAAYhF58hiAAaAADMABmZR5lkxMDExQUEAygAgaDMZ2TU4MjQ5YTYwMTg4MGEyYTU0NTk0MTIwMmZmZGRkNDUxAMsAAmRwueE0OLh6sarD+aIa8rO7kTBc1CmxGyWy'

URL = "https://www.ebay.it/n/all-categories"

HEADERS = ({
    'User-Agent': scraping.generate_random_user_agent(),
    'Accept-Language': 'en-US, en;q=0.5'})
# VARIABILI
group_by_IVA = []
file_name = ''
# Creazione di un DataFrame vuoto
df = pd.DataFrame(columns=azienda.keys())

# ----------------------METHODS------------------------------------
def is_solo_numero(variabile):
    try:
        numero = int(variabile)
        return True
    except ValueError:
        return False


def menu():
    global file_name
    print("HELLO MR. Scraper")
    print("Connecting to eBay.it ...")
    ebay = requests.get(URL, headers=HEADERS,
                        cookies={'nonsession': cookie_value})
    categories = BeautifulSoup(ebay.content, "html.parser")
    categories_links = categories.find_all("a", attrs={'class': "cat-url"})
    i = 1
    for categorie in categories_links:
        print(f"Press {i} for {categorie.text}")
        i += 1
    choice = input()
    while not (is_solo_numero(choice) and 0 < int(choice) < i):
        print("WHAT ARE YOU DOING!")
        choice = input()
    lista = list(categories_links)
    print(f"Connecting to {lista[int(choice)-1].get('href')}")
    file_name = lista[int(choice)-1].text
    return lista[int(choice)-1].get('href')


def cerca_elemento(elemento, lista):
    if (elemento in lista) or len(elemento) == 0:
        return True
    else:
        return False


def tronca_stringa(s):
    pattern = r'^(\D{0,3}\d+).*'
    match = re.match(pattern, s)
    if match:
        return match.group(1)
    else:
        return None


if __name__ == '__main__':
    print(f"---------------------------------CATGEGORIA {file_name}--------------------------------------------------")
    URL = menu()
    while True:
        try:
            webpage = requests.get(URL, headers=HEADERS,
                                   cookies={'nonsession': cookie_value})

            # Parsing HTML
            soup = BeautifulSoup(webpage.content, "html.parser")
            # Parsing di tutti i link presenti nella pagina principale dei prodotti
            links = soup.find_all("a", attrs={'class': "s-item__link"})
            for link_i in links:
                link = link_i.get('href')
                product_link = link
                print(product_link)
                # pagina web del prodotto i-esimo
                product_webpage = requests.get(product_link, headers=HEADERS,
                                               cookies={'session-token': cookie_value})
                new_soup = BeautifulSoup(product_webpage.content, "html.parser")
                # estrazione dei dati presenti nell pagina
                # ESTRAZIONE INFORMAZIONI DEL PRODOTTO
                # Trova il contenitore della tabella
                try:
                    container = new_soup.find(class_='ux-layout-section-evo__item--table-view')

                    # Estrai le etichette delle colonne e i valori
                    labels = [label.text.strip() for label in container.find_all(class_='ux-labels-values__labels-content')]
                    values = [value.text.strip() for value in container.find_all(class_='ux-labels-values__values-content')]

                    # Crea un dizionario delle coppie etichetta-valore
                    table_data = dict(zip(labels, values))
                except AttributeError as ae:
                    table_data = None

                azienda = dict.fromkeys(azienda.keys(), None)
                # Stampa il dizionario
                azienda = {k: v if k not in table_data else table_data[k] for k, v in azienda.items()}
                print(table_data)
                # ESTRAZIONE Nome prodotto
                nome_prodotto = new_soup.find("h1", attrs={"class": "x-item-title__mainTitle"}).text.strip()
                print(nome_prodotto)
                azienda['Nome prodotto'] = nome_prodotto
                # ESTRAZIONE prezzo prodotto
                prezzo_prodotto = new_soup.find("span", attrs={"itemprop": "price"}).get('content')
                print(prezzo_prodotto)
                azienda['Prezzo'] = prezzo_prodotto
                # ESTRAZIONE nome venditore e vetrina
                try:
                    seller_link = new_soup.find("div", attrs={"class": "ux-seller-section__item--seller"}).find('a')
                    azienda['Nome azienda:'] = seller_link.text.strip()
                    azienda['Vetrina'] = seller_link.get('href')
                except AttributeError as ae:
                    azienda['Nome azienda:'] = None
                    azienda['Vetrina'] = None
                # ESTRAZIONE N. Feed Back venditore
                try:
                    num_feed_back = new_soup.find("div", attrs={"class": "ux-seller-section__item--seller"}). \
                        find('a', attrs={'href': "#LISTING_FRAME_MODULE"}). \
                        find('span', attrs={'class', 'ux-textspans ux-textspans--PSEUDOLINK'}).text
                    azienda['N. Feed Back'] = num_feed_back
                except AttributeError as ae:
                    azienda['N. Feed Back'] = None
                # ESTRAZIONE INFO VENDITORE
                try:
                    info_venditore = new_soup.find("div", attrs={'class': 'vim d-business-seller'}).text
                    print(info_venditore)

                    delimitatori = {
                        "Informazioni sul venditore professionale": "Mostra Informazioni di contatto:",
                        "Mostra Informazioni di contatto:": "Numero Partita IVA:",
                        "Numero Partita IVA:": ""
                    }

                    result = {}

                    start_index = 0

                    for delimitatore, next_delimitatore in delimitatori.items():
                        start_index = info_venditore.find(delimitatore, start_index)
                        if start_index == -1:
                            break
                        start_index += len(delimitatore)
                        if next_delimitatore:
                            end_index = info_venditore.find(next_delimitatore, start_index)
                        else:
                            end_index = len(info_venditore)
                        value = info_venditore[start_index:end_index].strip()
                        result[delimitatore] = value if value else None

                    # TRONCARE CAMPO PARTITA IVA
                    try:
                        azienda = {k: v if k not in result else result[k] for k, v in azienda.items()}
                        azienda['Numero Partita IVA:'] = tronca_stringa(azienda['Numero Partita IVA:']) \
                            .strip().replace(" ", "")
                        if cerca_elemento(azienda['Numero Partita IVA:'], group_by_IVA) or \
                                azienda['Numero Partita IVA:'] is None:
                            continue
                        print(
                            f"PARTITA IVA {azienda['Numero Partita IVA:']}, Lunghezza {len(azienda['Numero Partita IVA:'])}")
                        group_by_IVA.append(azienda['Numero Partita IVA:'])
                        print(f"PARTITA IVA TRONCATA {azienda['Numero Partita IVA:']}")
                    except TypeError as te:
                        continue
                except AttributeError as ae:
                    print("NO Info venditore disponibile")
                    continue

                print("-------TROVO EMAIL----------")
                html_content = new_soup.text

                # Decodifica il testo HTML
                decoded_html = html.unescape(html_content)
                # Utilizza un'espressione regolare per trovare gli indirizzi email nel testo
                email_regex = r'\b[-\s]?[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
                azienda['Emails'] = re.findall(email_regex, decoded_html)
                azienda['Emails'] = list(dict.fromkeys(azienda['Emails']))
                print(azienda)

                # Creazione di un DataFrame temporaneo con il dizionario azienda come riga
                df_temp = pd.DataFrame([azienda])

                # Concatenazione del DataFrame temporaneo con il DataFrame principale
                df = pd.concat([df, df_temp], ignore_index=True)

                # Aggiungi il contenuto del dizionario al file CSV
                filename = './reportEbay.csv'  # Sostituisci con il nome del file desiderato

                with open(filename, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=azienda.keys())

                    if file.tell() == 0:  # Se il file è vuoto, scrivi l'intestazione
                        writer.writeheader()

                    writer.writerow(azienda)  # Scrivi i dati del dizionario

                print(f"Il contenuto del dizionario è stato aggiunto al file '{filename}' in formato CSV.")
        except KeyboardInterrupt as ki:
            break

        print("EXIT")
        try:
            new_URL = soup.find("a", attrs={'class': "pagination__next icon-link"})
            URL = new_URL.get('href')
        except AttributeError as ae:
            break
    file_name = file_name.replace(" ", "_")
    df.to_excel(f'reportEbay{file_name}.xlsx', index=False)
    print(f"Aggiornamento file EXCEL...reportEbay{file_name}.xlsx")
    scraping.formatta_file_excel(f'reportEbay{file_name}.xlsx')
    print("-------------DONE-----------------")
