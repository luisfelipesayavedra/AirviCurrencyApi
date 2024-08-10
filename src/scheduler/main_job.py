import requests
import json
import logging
import os

logging.basicConfig(level=logging.INFO)


def fetch_and_save_currency_data():
    
    logging.info("[SCHEDULER]:: Currencies Querying Process Initialized")
    # Variables bases
    api_key = os.environ["CURRENCYAPI_KEY"]
    url = os.environ["CURRENCYAPI_URI"]
    base_currency = os.environ["CURRENCY_BASE"]
    currencies = os.environ["CURRENCY_LIST"]
    
    # Parámetros de la consulta
    params = {
        "apikey": api_key,
        "currencies": currencies,
        "base_currency": base_currency
    }

    try:
        # Realizar la solicitud GET
        response = requests.get(url, params=params)
        
        # Verificar si la solicitud fue exitosa
        response.raise_for_status()
        
        # Obtener los datos JSON
        data = response.json()
        
        # Crear un nombre de archivo con la fecha actual
        filename = f"src/files/currency_data.json"
        
        # Guardar los datos en un archivo JSON
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        
        logging.info("[SCHEDULER]:: Currencies Querying Data Saved Succesfully")
    except requests.RequestException as e:
        logging.error(f"Error al realizar la solicitud: {e}")
    except json.JSONDecodeError:
        logging.error("Error al decodificar la respuesta JSON")
    except IOError:
        logging.error("Error al escribir en el archivo")
