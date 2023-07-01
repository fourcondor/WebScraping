import requests
from openpyxl import Workbook

# COSTANTI
api_url = 'https://imprese.openapi.it/advance/{}'

# Partita IVA, codice fiscale o ID azienda di interesse
# piva_cf_or_id = '02080418021'

# Token di autenticazione
token = '64823de304358d4c3f00d2fb'



headers = {
    'Authorization': f'Bearer {token}'
}


def flatten_json(json_data, parent_key='', flattened_dict=None):
    if flattened_dict is None:
        flattened_dict = {}
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            new_key = parent_key + '_' + key if parent_key else key
            if isinstance(value, dict):
                flatten_json(value, new_key, flattened_dict)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    new_item_key = new_key + '_' + str(i)
                    if isinstance(item, dict):
                        flatten_json(item, new_item_key, flattened_dict)
                    else:
                        flattened_dict[new_item_key] = item
            else:
                flattened_dict[new_key] = value
    return flattened_dict


if __name__ == '__main__':
    print("Inserisci Partita IVA, codice fiscale o ID azienda di interesse:")
    piva_cf_or_id = input()
    while not str.isdigit(piva_cf_or_id):
        print("Dato errato!!!")
        print("Inserisci Partita IVA, codice fiscale o ID azienda di interesse:")
        piva_cf_or_id = input()

    url = api_url.format(piva_cf_or_id)
    response = requests.get(url, headers=headers)

    # Ottieni la risposta dell'API
    api_response = response.json()
    #  ESTRAGGO I DATI DAL JSON E IMPORTO SU EXCEL
    dati_excel = flatten_json(api_response)
    print(dati_excel)
    # CONVERTO JSON IN EXCEL
    excel_file = f'dati_impresa{dati_excel["data_denominazione"]}.xlsx'

    wb = Workbook()

    sheet = wb.active

    field_names = list(dati_excel.keys())
    sheet.append(field_names)

    field_values = list(dati_excel.values())
    sheet.append(field_values)

    wb.save(excel_file)
    print(f"FILE dati_impresa{dati_excel['data_denominazione']}.xlsx SALVATO!")
