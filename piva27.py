import csv

csv_file = '27-clients.csv'
txt_file = '27-clients.txt'


with open(csv_file, 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Salta l'intestazione del file CSV

    with open(txt_file, 'w', encoding='utf-8') as output:
        for row in csv_reader:
            seventh_field = row[6]  # Indice 6 per il settimo campo
            data = seventh_field.split(':')[-1].strip()  # Taglia fino all'ultimo ":" e rimuove spazi iniziali/finali
            output.write(data + '\n')

print("Dati importati correttamente nel file:", txt_file)

