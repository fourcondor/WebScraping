import openpyxl
import argparse
import subprocess
import scrapEcommerce

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


def formatta_file_excel(file_name):
    # Apri il file Excel esistente
    workbook = openpyxl.load_workbook(file_name)

    # Seleziona il foglio di lavoro su cui desideri applicare la formattazione
    sheet = workbook.active

    # Ridimensiona automaticamente le colonne in base ai dati
    for column_cells in sheet.columns:
        max_length = 0
        column = column_cells[0].column_letter
        for cell in column_cells:
            if cell.value is not None:
                cell_value = str(cell.value)
                if len(cell_value) > max_length:
                    max_length = len(cell_value)
        adjusted_width = (max_length + 2) * 1.2
        sheet.column_dimensions[column].width = adjusted_width

    # Salva le modifiche nel file Excel
    workbook.save(file_name)


if __name__ == '__main__':
    main()
