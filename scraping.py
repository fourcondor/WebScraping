import argparse
import subprocess

from fake_useragent import UserAgent


def generate_random_user_agent():
    ua = UserAgent()
    return ua.random


def main():
    # Definisci le opzioni da riga di comando
    parser = argparse.ArgumentParser(description='Collegamento tra script scrapingAmazon e scrapingEbay')

    # Aggiungi le opzioni desiderate
    parser.add_argument('--scrape', type=str, choices=['amazon', 'ebay'],
                        help='Specifica quale script di scraping avviare')

    # Parsa le opzioni da riga di comando
    args = parser.parse_args()

    # Controlla quale opzione è stata selezionata
    if args.scrape == 'amazon':
        subprocess.call(['python', 'scrapingAmazon.py'])
    elif args.scrape == 'ebay':
        subprocess.call(['python', 'scrapingEbay.py'])
    else:
        print('Opzione non valida')


if __name__ == '__main__':
    main()
