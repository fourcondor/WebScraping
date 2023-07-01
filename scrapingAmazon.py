import time
import pandas as pd
from bs4 import BeautifulSoup
import csv
import requests
import re
import html
import unicodedata
import scraping

url_categorie = {
    'Bellezza': "https://www.amazon.it/s?rh=n%3A6306897031&fs=true&ref=lp_6306897031_sar",
    'Fai da te': "https://www.amazon.it/s?rh=n%3A2454160031&fs=true&ref=lp_2454160031_sar",
    'Cura della casa': "https://www.amazon.it/s?rh=n%3A6394759031&fs=true&ref=lp_6394759031_sar",
    'Sport e tempo libero': "https://www.amazon.it/s?bbn=524012031&rh=n%3A26039477031&fs=true&ref=lp_26039477031_sar",
    'Pulizie': "https://www.amazon.it/s?rh=n%3A6571987031&fs=true&ref=lp_6571987031_sar",
    'Lavorazione': "https://www.amazon.it/s?rh=n%3A6306897031&fs=true&ref=lp_6306897031_sar",
    'Attrezzatura': "https://www.amazon.it/s?rh=n%3A2565863031&fs=true&ref=lp_2565863031_sar",
    'Creme': "https://www.amazon.it/s?k=creme&rh=n%3A6306897031&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss",
    'Siero': "https://www.amazon.it/s?k=siero&rh=n%3A6306897031&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss",
    'Brazz': "https://www.amazon.it/s?k=bracciolo+universale&rh=p_n_sb_certificate_id%3A75628273031&dc&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2N5HP5O7ZN1AH&qid=1688054828&rnid=75628272031&sprefix=bracciolo+universale%2Caps%2C106&ref=sr_nr_p_n_sb_certificate_id_1&ds=v1%3ATjYd6U8pAuRbXfWk8kA6ptMQbawBmJS1zfyZqssvjjM"
}
# Crea il dizionario con gli attributi
azienda = {
    'ASIN': None,
    'Vetrina': None,
    'Num prodotti vetrina': None,
    'Marca': None,
    'Nome prodotto': None,
    'Prezzo': None,
    'Sconto': None,
    'Prezzo consigliato': None,
    'Nome azienda:': None,
    'N. Feed Back': None,
    'Tipo di attività:': None,
    'Numero di iscrizione al registro delle imprese:': None,
    'Numero di partita IVA:': '',
    'Numero di telefono:': '',
    'Indirizzo Servizio clienti:': '',
    'Indirizzo aziendale:': '',
    'Emails': [],
}

# COOKIE
cookies = {
    'csm-hit': 'tb:DFTKCNYKNH7A2VW3120N+s-DK2WVNN5SW86915YRB1E|1687968488201&t:1687968488201&adb:adblk_no',
    'i18n-prefs': 'EUR',
    'session-id': '257-6672538-7538018',
    'session-id-time': '2082787201l',
    'session-token': '"Y2CGecnFCiS9oTLHtZcVAFAVOn3RkjSsl4oVfVleDVNG48iCFmPm7r4eGhfWxwgOvxPgkd6ZbdrCjs3q5CzicB7Ty5weKrRMukumgONCkm8O08c6D6GlqkmebLLoQqtM2CBS6VUuw76vS6P8ZIiA8VBFiAKlS0gn0F7MoxfMAu2NvhLyTlylYU/2LM1hjuFpSkAYKf9qyLRGXj6M0ENl3nO+JcCzdqHK1z8xSFHN51Y="',
    'ubid-acbit': '262-9912553-6719151'
}

URL = "https://www.amazon.it/b?ie=UTF8&node=13773664031"

HEADERS = ({
    'User-Agent': scraping.generate_random_user_agent(),
    'Cookie': '; '.join([f'{name}={value}' for name, value in cookies.items()]),
    'Accept-Language': 'en-US, en;q=0.5'})

group_by_IVA = []
group_by_vetrina = []


# ----------------METHODS------------------
def is_solo_numero(variabile):
    try:
        numero = int(variabile)
        return True
    except ValueError:
        return False


def estrazioneNumProdotti(link_vetrina):
    num_links = 0
    new_link_vetrina = link_vetrina
    print("Conteggio numero prodotti venduti dal venditore")
    while True:
        try:
            link_v = "https://amazon.it" + new_link_vetrina
            time.sleep(5)
            vetrina = requests.get(link_v, headers=HEADERS)
            prodotti_vetrina = BeautifulSoup(vetrina.content, "html.parser")
            num_links_tmp = prodotti_vetrina.find_all("a", attrs={
                'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            num_links += len(num_links_tmp)
            print(num_links)
            new_url_link_vetrina = prodotti_vetrina.find("a", attrs={
                'class': "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"})
            new_link_vetrina = new_url_link_vetrina.get('href')
        except AttributeError as ae:
            break
    print(f"NUMERO PRODOTTI VETRINA {num_links}")
    return str(num_links)


# Creazione di un DataFrame vuoto
df = pd.DataFrame(columns=azienda.keys())

file_name = ''


def menu():
    global file_name
    print("HELLO MR. Scraper")
    print("Connecting to Amazon.it ...")

    i = 1
    for categoria in url_categorie.keys():
        print(f"Press {i} for {categoria}")
        i += 1
    choice = input()
    while not (is_solo_numero(choice) and 0 < int(choice) < i):
        print("WHAT ARE YOU DOING!")
        choice = input()
    campi = url_categorie.keys()
    result = url_categorie[list(campi)[int(choice) - 1]]
    print(f"Connecting to {result}")
    file_name = list(campi)[int(choice) - 1]
    print(f"File generato reportAmazon{file_name}.xlsx")
    return result


def cerca_elemento(elemento, lista):
    if (elemento in lista):
        return True
    else:
        return False


if __name__ == '__main__':
    URL = menu()
    print(f"---------------------------------CATGEGORIA {file_name}--------------------------------------------------")
    num_records = 0
    while True:
        try:
            if num_records > 100:
                num_records = 0
                print("Attendere qualche minuto ...")
                time.sleep(500)
            webpage = requests.get(URL, headers=HEADERS)

            # Parsing HTML
            soup = BeautifulSoup(webpage.content, "html.parser")

            # Parsing di tutti i link presenti nella pagina principale dei prodotti
            links = soup.find_all("a", attrs={
                'class': "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
            for link_i in links:
                link = link_i.get('href')
                product_link = "https://amazon.it" + link
                print(product_link)
                # pagina web del prodotto i-esimo
                time.sleep(8)
                print("Attendere...")

                product_webpage = requests.get(product_link, headers=HEADERS)
                new_soup = BeautifulSoup(product_webpage.content, "html.parser")
                num_records += 1
                # estrazione dei dati presenti nell pagina
                # ESTRAZIONE ASIN
                try:
                    table = new_soup.find('table', id='productDetails_techSpec_section_1')

                    # Trova tutte le righe della tabella
                    rows = table.find_all('tr')

                    asin = None

                    # Cerca l'ASIN nelle righe della tabella
                    for row in rows:
                        th = row.find('th')
                        td = row.find('td')
                        if th and td and th.get_text(strip=True) == 'ASIN':
                            codice = td.get_text(strip=True)
                            asin = html.unescape(codice)
                            break
                except AttributeError as ae:
                    asin = None

                # ESTRAZIONE MARCA
                try:
                    marca = new_soup.find("span", attrs={"class": "a-size-base po-break-word"}).text.strip()
                except AttributeError as ae:
                    try:
                        table = new_soup.find('table', id='productDetails_techSpec_section_1')

                        # Trova tutte le righe della tabella
                        rows = table.find_all('tr')

                        marca = None

                        # Cerca il nome della marca nelle righe della tabella
                        for row in rows:
                            th = row.find('th')
                            td = row.find('td')
                            if th and td and th.get_text(strip=True) == 'Marca':
                                marca = td.get_text(strip=True)
                                break
                    except AttributeError as ae:
                        marca = None

                print(marca)
                print(asin)
                # SE ESISTE ESTRAZIONE DEL PREZZO CONSIGLIATO
                try:
                    prezzo_consigliato = new_soup.find("span", attrs={"class": "a-price a-text-price a-size-base"}). \
                        find("span", attrs={"class": "a-offscreen"}).text.strip()
                except AttributeError as ae:
                    prezzo_consigliato = None
                # ESTRAZIONE nome prodotto
                try:
                    nome_prodotto = new_soup.find("span", attrs={"id": "productTitle"}).text.strip()
                except AttributeError as ae:
                    continue
                # ESTRAZIONE prezzo prodotto
                sconto = 0
                try:
                    prezzo_prodotto = new_soup.find("span",
                                                    attrs={
                                                        "class": "a-price a-text-price a-size-medium apexPriceToPay"}). \
                        find("span", attrs={"class": "a-offscreen"}).text.strip()
                except AttributeError as ae:
                    prezzo_prodotto = prezzo_consigliato
                if prezzo_prodotto and prezzo_consigliato:
                    print(f"Prezzo prodotto {prezzo_prodotto}")
                    print(f"Prezzo consigliato {prezzo_consigliato}")
                    prezzo_prodotto_float = prezzo_prodotto.replace("€", "").replace(",", ".")
                    prezzo_consigliato_float = prezzo_consigliato.replace("€", "").replace(",", ".")
                    # Converti la stringa in un numero float
                    prezzo_prodotto_float = float(prezzo_prodotto_float)
                    prezzo_consigliato_float = float(prezzo_consigliato_float)
                    sconto = (prezzo_consigliato_float - prezzo_prodotto_float) * 100 / prezzo_consigliato_float
                    sconto = "{:.2f}".format(sconto)
                    sconto = (str(sconto) + "%")
                elif (not prezzo_prodotto) and (not prezzo_consigliato):
                    try:
                        prezzo_prodotto = new_soup.find("span",
                                                        attrs={
                                                            "class": "a-price aok-align-center reinventPricePriceToPayMargin priceToPay"}). \
                            find("span", attrs={"aria-hidden": "true"}).text.strip()
                    except AttributeError as ae:
                        prezzo_prodotto = None

                if sconto == 0:
                    sconto = None

                print(prezzo_prodotto)
                print(f"Prezzo consigliato {prezzo_consigliato}")
                print(f"Sconto {sconto}")
                seller_link = new_soup.find("a", attrs={"id": "sellerProfileTriggerId"})
                if not seller_link:
                    print("Venditore Amazon")
                    azienda = dict.fromkeys(azienda.keys(), None)
                    azienda['ASIN'] = asin
                    azienda['Marca'] = marca
                    azienda['Nome azienda:'] = "Amazon"
                    azienda['Nome prodotto'] = nome_prodotto
                    azienda['Prezzo'] = prezzo_prodotto
                    azienda['Sconto'] = sconto
                    azienda['Prezzo consigliato'] = prezzo_consigliato
                else:
                    seller_link = "https://amazon.it" + seller_link.get('href')
                    print(seller_link)
                    # PAGINA DEL VENDITORE
                    seller_webpage = requests.get(seller_link, headers=HEADERS)
                    new_soup = BeautifulSoup(seller_webpage.content, "html.parser")
                    # Vedo ESISTE la VETRINA del venditore
                    link_element = new_soup.find('a', string=lambda text: text and 'Vetrina' in text)
                    link_vetrina = None
                    if link_element:
                        link_vetrina = link_element.get('href')
                        if cerca_elemento(link_vetrina, group_by_vetrina):
                            continue
                        print(f"link vetrina {link_vetrina}")
                        group_by_vetrina.append(link_vetrina)
                        # Numerp di prodotti in vetrina
                        num_prodotti_vetrina = None
                        num_prodotti_vetrina = estrazioneNumProdotti(link_vetrina)
                    # Estraggo il NUMERO DI VALUTAZIONI del venditore
                    link_valutazioni = new_soup.find('a',
                                                     class_='a-link-normal feedback-detail-description no-text-decoration')
                    print(f"link valutazioni {link_valutazioni}")
                    valutazioni = None
                    if link_valutazioni:
                        match = re.search(r'\((\d+) valutazioni\)', link_valutazioni.text)
                        if match:
                            valutazioni = match.group(1)
                            print(f"valutazioni {valutazioni}")
                    # parto da ramo più alto per identificare la "box" con i dati del venditore
                    try:
                        dati_azienda = new_soup.find("div", attrs={"id": "page-section-detail-seller-info"}).text
                    except AttributeError as ae:
                        dati_azienda = None
                    print("----------------------------DATI VENDITORE----------------------------------")
                    # Estrazione delle informazioni dal testo HTML
                    print(dati_azienda)
                    testo_pulito = dati_azienda
                    azienda = dict.fromkeys(azienda.keys(), None)
                    # inserisco i dati nel dizionario
                    azienda['ASIN'] = asin
                    if link_element:
                        azienda['Vetrina'] = "https://amazon.it" + link_vetrina
                        azienda['Num prodotti vetrina'] = num_prodotti_vetrina
                    azienda['Marca'] = marca
                    azienda['Nome prodotto'] = nome_prodotto
                    azienda['Prezzo'] = prezzo_prodotto
                    azienda['Sconto'] = sconto
                    azienda['Prezzo consigliato'] = prezzo_consigliato
                    try:
                        nome_azienda_match = re.search(r'Nome azienda:\n(.+)', testo_pulito)
                        azienda['Nome azienda:'] = nome_azienda_match.group(1).strip() if nome_azienda_match else None
                        azienda['N. Feed Back'] = valutazioni
                        tipo_attivita_match = re.search(r'Tipo di attività:\n(.+)', testo_pulito)
                        azienda['Tipo di attività:'] = tipo_attivita_match.group(
                            1).strip() if tipo_attivita_match else None

                        numero_iscrizione_match = re.search(r'Numero di iscrizione al registro delle imprese:\n(.+)',
                                                            testo_pulito)
                        azienda['Numero di iscrizione al registro delle imprese:'] = numero_iscrizione_match.group(
                            1).strip() if numero_iscrizione_match else None
                        # FILTRO P.IVA SE GIA' ESISTE
                        numero_partita_iva_match = re.search(r'Numero di partita IVA:\n(.+)', testo_pulito)
                        azienda['Numero di partita IVA:'] = numero_partita_iva_match.group(
                            1).strip() if numero_partita_iva_match else None

                        if cerca_elemento(azienda['Numero di partita IVA:'], group_by_IVA):
                            continue
                        group_by_IVA.append(azienda['Numero di partita IVA:'])

                        numero_telefono_match = re.search(r'Numero di telefono:\n(.+)', testo_pulito)
                        azienda['Numero di telefono:'] = numero_telefono_match.group(
                            1).strip() if numero_telefono_match else None

                        indirizzo_servizio_clienti_match = re.search(r'Indirizzo Servizio clienti:\n(.+)', testo_pulito)
                        azienda['Indirizzo Servizio clienti:'] = indirizzo_servizio_clienti_match.group(
                            1).strip() if indirizzo_servizio_clienti_match else None

                        indirizzo_aziendale_match = re.search(r'Indirizzo aziendale:\n(.+)', testo_pulito)
                        azienda['Indirizzo aziendale:'] = indirizzo_aziendale_match.group(
                            1).strip() if indirizzo_aziendale_match else None
                        # formattazione
                        parole_da_eliminare = list(azienda.keys())
                        for chiave, valore in azienda.items():
                            if valore is not None:
                                for parola in parole_da_eliminare:
                                    valore = valore.replace(parola, '')
                                valore = html.unescape(valore)
                                azienda[chiave] = valore
                    except TypeError as te:
                        continue

                    print("-------TROVO EMAIL----------")
                    html_content = seller_webpage.text

                    # Decodifica il testo HTML
                    decoded_html = html.unescape(html_content)
                    # Utilizza un'espressione regolare per trovare gli indirizzi email nel testo
                    email_regex = r'\b[-\s]?[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
                    azienda['Emails'] = re.findall(email_regex, decoded_html)
                print(azienda)

                # Creazione di un DataFrame temporaneo con il dizionario azienda come riga
                df_temp = pd.DataFrame([azienda])

                # Concatenazione del DataFrame temporaneo con il DataFrame principale
                df = pd.concat([df, df_temp], ignore_index=True)
                # Aggiungi il contenuto del dizionario al file CSV
                filename_csv = './reportAmazon.csv'  # Sostituisci con il nome del file desiderato
                # ESPORTO DATI SIA IN .CSV che .XLSX
                # .CSV
                with open(filename_csv, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=azienda.keys())

                    if file.tell() == 0:  # Se il file è vuoto, scrivi l'intestazione
                        writer.writeheader()

                    writer.writerow(azienda)  # Scrivi i dati del dizionario

                print(f"Il contenuto del dizionario è stato aggiunto al file '{filename_csv}' in formato CSV.")
        except KeyboardInterrupt as ki:
            break

        print("EXIT")
        try:
            new_URL = soup.find("a", attrs={
                'class': "s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"})
            URL = new_URL.get('href')
            URL = "https://amazon.it" + URL
        except AttributeError as ae:
            break
    file_name = file_name.replace(" ", "_")
    df.to_excel(f'reportAmazon{file_name}.xlsx', index=False)
    print(f"Aggiornamento file EXCEL...reportAmazon{file_name}.xlsx")
    scraping.formatta_file_excel(f'reportAmazon{file_name}.xlsx')
    print("-----------------------DONE-------------------------")
