import requests

# URL del sito web
url = 'https://www.ufficiocamerale.it/'

# Dati del form
form_data = {
    'search_input': '04862970755'
}

# Crea una sessione per gestire i cookie
session = requests.Session()

# Invia una richiesta GET per impostare i cookie iniziali
response = session.get(url)

# Verifica lo stato della risposta
if response.status_code == 200:
    # Invia una richiesta POST per accettare i cookie
    response = session.post(url, data=form_data)

    # Verifica lo stato della risposta
    if response.status_code == 200:
        # Ottieni il contenuto HTML della risposta
        html_content = response.text

        # Fai qualcosa con il contenuto HTML ricevuto
        print(html_content)
    else:
        print('Si è verificato un errore durante l\'invio della richiesta POST.')
else:
    print('Si è verificato un errore durante l\'invio della richiesta GET.')
