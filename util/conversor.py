import requests

# Converte de Dolar para Real
def dolar_para_real(valor_em_dolar):
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        # Fazendo a requisição GET para obter os dados da taxa de câmbio
        response = requests.get(url)
        data = response.json()

        # Verificando se a requisição foi bem sucedida
        if response.status_code == 200:
            # Obtendo a taxa de câmbio do dólar para real (BRL)
            taxa_dolar_para_real = data['rates']['BRL']
            # Convertendo o valor em dólar para real
            valor_em_real = valor_em_dolar * taxa_dolar_para_real
            return valor_em_real
        else:
            return 0

    except Exception as e:
        return 0
    
def convert_to_float(value):
        try:
            return float(value.replace(',', '.'))
        except ValueError:
            return 0.0