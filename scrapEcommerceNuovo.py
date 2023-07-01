import time

import fake_useragent
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import csv
import scraping
from fake_useragent import UserAgent

lista_item = []
ripetizione = False
what_cms = "https://whatcms.org/?s="
e_commerces_xlsx = { "Nome prodotto" : None, "Prospect": None }
# Creazione di un DataFrame vuoto
df = pd.DataFrame(columns=e_commerces_xlsx.keys())
#COOKIES
cookies = {
    'SID': 'XQjSQ_O_8X4HiOwdjryPtcVaf-PBRug54dGoGfV4cdaZ2i1Nj8RnpgO-FlFwKTUdKuB1eA.',
    '__Secure-1PSID': 'XQjSQ_O_8X4HiOwdjryPtcVaf-PBRug54dGoGfV4cdaZ2i1Najl_nGjjdiouOYV--SJ9Gg.',
    '__Secure-3PSID': 'XQjSQ_O_8X4HiOwdjryPtcVaf-PBRug54dGoGfV4cdaZ2i1NtE8g3rM4tpIb_yvr1A1FdA.',
    'HSID': 'A9e4q1hDOfOIBqATY',
    'SSID': 'Ap4HnZ7Cp5MSztt62',
    'APISID': '_82_NyQVqZbx4Ye0/An4WYiYpCrC4oatDq',
    'SAPISID': 'WNi07BllWnalHJ8x/A8SgYM1cw5CaZaXT-',
    '__Secure-1PAPISID': 'WNi07BllWnalHJ8x/A8SgYM1cw5CaZaXT-',
    '__Secure-3PAPISID': 'WNi07BllWnalHJ8x/A8SgYM1cw5CaZaXT-',
    '__Secure-1PSIDTS': 'sidts-CjEBLFra0sDjKnTy6EEv5WwVf3gp7jRPcPWzv8Ch2RCkwNTwRrDdH95j1LQXAsKMDV_KEAA',
    '__Secure-3PSIDTS': 'sidts-CjEBLFra0sDjKnTy6EEv5WwVf3gp7jRPcPWzv8Ch2RCkwNTwRrDdH95j1LQXAsKMDV_KEAA',
    'SIDCC': 'AP8dLtydvkLooFYi95benMq-8iioT9ngDMOJRGvL6I91UpSRhO4BnC2EoFERF5hy1DG1R5X6qQ',
    '__Secure-1PSIDCC': 'AP8dLtxsKHP1-tZDZKUtWqH8BlRdpH9u9Q04Ud4qaNhNb62HRFbenOtC3m9cs6PI-NmmN83XmNw',
    '__Secure-3PSIDCC': 'AP8dLtw2NgPiruafIk8iW63iCYYzyldOWuxB3YK8ai57CjE8ocajSvhxm3grg91nDPZdPZZmL87j',
    'SEARCH_SAMESITE': 'CgQItJgB',
    'OTZ': '7054360_48_52_123900_48_436380',
    '__gsas': 'ID=cdecc4552f3ff8f0:T=1685918430:RT=1685918430:S=ALNI_MaLhapnPUDiCCKwx-tPxJyFRoskyw',
    'NID': '511=WOnvdn8pQiAT0ygK9euRpDDdOea19k6ent6t84zX_iXB6kE355KmEstcv6W4dfWeHm85uXsik-89uy9oqM_k9Zo_lB0uDRBhgxGr7kUbW2fE4PqHmV7J7eAojmWA54bLI2KdYzeupxf6MRQbnwmgTgS2uo187Y3tm8-IS9zANsGHJkA71pBZJs6wOklxOi244iBpuG0fs3tIiWr6jYLYd0R3sIsMZZAPXdYWBbStb6HXnKddf2IdKBjY4IgcTgD6M3lqZYeJnJjHP0JaermDmA',
    '__Secure-ENID	': '12.SE=FTpnicQXI1_NjHNh3oNsl5sGpRgldWJfj0ykMhEAscFlSILsn2-LgaPZrbKtdl2x1KMh_j3FbvMXL-FIG8UffsyH0FTgqSLoxf39d4_dMT6ak1-W9L32YOORwcR0hj6oRkXrbn1AwZzyL9uvitNt9TQnbfYEJqOVi-JpLWezN_mC7IDsGpj-ini43Yw6BPLsmyi194kMnuVDHeuThJ65aIMCwxdNPpUcWb7DS-PxL8ST4ZooaAoqZeEALw5opz_QM3w0PQMJ_dRZY5yFq-WcHg',
    'AEC': 'AUEFqZdaz0iDA5tF6v9MBsa0gwDod-gpApFEGYEziX6LS4DdWf_KcbKqYg',
    'OGPC': '19022552-1:',
    'OGP': '-19022552:',
    'DV': 'M73XoMoJYiZVIBy4P1MyROsgMBanjRgijpdIBVqZhgMAAGAUsbpzQL8yIwEAAICIXxvmwpdnVwAAACZXk6Owkfa-GgAAAA',
    '1P_JAR': '2023-6-20-20',
    'S': 'cookie_value1',
    'cookie_name2': 'billing-ui-v3=q7K8z5oGBy0iVwZFetKca4EeG2ol9LBJ:billing-ui-v3-efe=q7K8z5oGBy0iVwZFetKca4EeG2ol9LBJ'
}

def leggi_file_csv(nome_file):
    dati = []
    with open(nome_file, 'r') as file_csv:
        lettore = csv.reader(file_csv)
        for riga in lettore:
             dati.append(riga)
    return dati


def ricerca_e_commerce(item):
    e_commerces = []
    print("--------INIZIO RICERCA E-COMMERCE------------")
    ua = UserAgent()
    user_agent = ua.random
    headers = {
        'User-Agent': user_agent,
        'Cookie': '; '.join([f'{name}={value}' for name, value in cookies.items()])
    }
    query = {'q': f"{item} shop on line -site:amazon.* -site:ebay.* -site:trovaprezzi.it -site:collistar.it -site:idealo.it -inurl:\"category/sponsored-post\""}
    google_url = 'https://www.google.com/search'
    html = requests.get(google_url, headers=headers, params=query)
    soup = BeautifulSoup(html.content, 'html.parser')
    print(soup)
    links = soup.find_all("div", attrs={'class': "yuRUbf"})
    print(f'links trovati {links}')
    for link_i in links:
        href = link_i.a.get('href')
        print(href)
        print("LINK")
        e_commerces.append(href)
    print(f"Fine ITEM {item}")
    print("------FINE---------")
    return e_commerces

if __name__ == '__main__':
    # Apertura file
    nome_file_csv = 'reportAmazon.csv'
    dati_csv = leggi_file_csv(nome_file_csv)
    print("LETTURA DATI")
    for riga in dati_csv:
        if riga[7] == 'Amazon':
            # riga3 nome_prodotto
            print(riga[3])
            lista_item.append(riga[3])
    print("FINE LETTURA DATI")
    try:

        for item in lista_item:
            lista_ecommerce = ricerca_e_commerce(item)
            for sito_i in lista_ecommerce:
                if not ripetizione:
                    e_commerces_xlsx['Nome prodotto'] = item
                    ripetizione = True
                else:
                    e_commerces_xlsx['Nome prodotto'] = ''
                e_commerces_xlsx['Prospect'] = sito_i
                # Creazione di un DataFrame temporaneo con il dizionario azienda come riga
                df_temp = pd.DataFrame([e_commerces_xlsx])
                # Concatenazione del DataFrame temporaneo con il DataFrame principale
                df = pd.concat([df, df_temp], ignore_index=True)
                print(f"DATI CORRENTI {e_commerces_xlsx}")
            ripetizione = False
            # DELAY for Google SERP
            time.sleep(5)
    except KeyboardInterrupt:
        print("SCRITTURA su file reportAmazonProspetto.xlsx")
    df.to_excel(f'reportAmazonProspetto.xlsx', index=False)
    scraping.formatta_file_excel(f'reportAmazonProspetto.xlsx')
