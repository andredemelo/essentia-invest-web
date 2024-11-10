import requests

# Função para obter a taxa de câmbio do Dólar para Real
def obter_taxa_dolar_para_real():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get('rates', {}).get('BRL', 0)
    except requests.exceptions.RequestException:
        return 0
    except ValueError:
        return 0

# Função para converter de Dólar para Real
def dolar_para_real(valor_em_dolar):
    taxa_dolar_para_real = obter_taxa_dolar_para_real()
    
    if taxa_dolar_para_real == 0:
        return 0
    return valor_em_dolar * taxa_dolar_para_real

# Função para converter uma string para float
def convert_to_float(value):
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return 0.0
