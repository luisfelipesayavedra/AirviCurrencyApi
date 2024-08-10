from flask import Blueprint, abort, jsonify, request
import json
import os

currencies_bp = Blueprint('user', __name__)

@currencies_bp.route('/currency_value', methods=['GET'])
def get_currency_value():
    try:
        # Lee el archivo JSON
        with open('src/files/currency_data.json', 'r') as file:
            data = json.load(file)
        
        # Obtiene la sección de 'data'
        data_section = data.get('data', {})

        # Verifica si la sección 'data' está vacía
        if not data_section:
            abort(404, description="No se encontró la sección 'data' en el archivo JSON")
        
        # Obtiene los parámetros de consulta (query)
        requested_currencies = request.args.getlist('currency')

        # Si no se proporcionan monedas, devuelve todas
        if not requested_currencies:
            base_currencies = os.environ["CURRENCY_LIST"].split(",")
            print(base_currencies)
            filtered_data = {
                currency: {**data_section[currency], 'value': 1 / data_section[currency]['value']}
                for currency in base_currencies
                if currency in data_section
            }
            return jsonify(filtered_data)

        # Filtra las monedas solicitadas
        filtered_data = {
            currency: {**data_section[currency], 'value': 1 / data_section[currency]['value']}
            for currency in requested_currencies
            if currency in data_section
        }

    
        # Verifica si se encontraron las monedas solicitadas
        if not filtered_data:
            abort(404, description="No se encontraron las monedas solicitadas")
        return jsonify(filtered_data)
    except json.JSONDecodeError:
        abort(500, description="Error al decodificar el archivo JSON")

@currencies_bp.route('/convert', methods=['GET'])
def convert_currency():
    try:

        # Lee el archivo JSON
        with open('src/files/currency_data.json', 'r') as file:
            data = json.load(file)
        
        # Obtiene la sección de 'data'
        data_section = data.get('data', {})

        # Verifica si la sección 'data' está vacía
        if not data_section:
            abort(404, description="No se encontró la sección 'data' en el archivo JSON")
        
        # Obtiene los parámetros de consulta (query)
        currency = request.args.get('currency')
        amount = request.args.get('amount', type=float)
        direction = request.args.get('direction', 'COP_to_currency')

        # Verifica si se proporcionaron los parámetros necesarios
        if not currency or amount is None:
            abort(400, description="Faltan parámetros requeridos: 'currency', 'amount', y 'direction'")
        
        # Verifica si la moneda solicitada está disponible
        if currency not in data_section:
            abort(404, description="La moneda solicitada no se encuentra disponible")
        
        conversion_rate = data_section[currency]['value']

        # Realiza la conversión de acuerdo a la dirección especificada
        if direction == 'COP_to_currency':
            converted_amount = amount * conversion_rate
        elif direction == 'currency_to_COP':
            converted_amount = amount / conversion_rate
        else:
            abort(400, description="Dirección de conversión inválida. Use 'COP_to_currency' o 'currency_to_COP'.")

        # Devuelve el resultado de la conversión
        result = {
            "currency": currency,
            "amount": amount,
            "direction": direction,
            "converted_amount": converted_amount
        }

        return jsonify(result)

    except json.JSONDecodeError:
        abort(500, description="Error al decodificar el archivo JSON")

# Manejadores de errores personalizados
@currencies_bp.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@currencies_bp.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

@currencies_bp.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400