import yfinance as yf
from datetime import datetime

# Função para ajustar o ticker com base na classe
def ajustar_ticker(ticker, classe):
    if classe in ['acao', 'fiis']:
        return ticker + '.SA'
    return ticker

# Função para buscar o preço atual do ativo usando Yahoo Finance
def obtem_preco_atual(ticker, classe):
    ticker = ajustar_ticker(ticker, classe)
    ativo = yf.Ticker(ticker)
    hist = ativo.history(period="1mo")  
    if not hist.empty:
        return hist['Close'].iloc[-1]
    return 0

# Função para buscar o Dividend Yield do ativo usando Yahoo Finance
def obtem_dividend_yield(ticker, classe):
    ticker = ajustar_ticker(ticker, classe)
    ativo = yf.Ticker(ticker)
    try:
        return ativo.info.get('dividendYield', 0) * 100
    except KeyError:
        return 0

# Função para buscar o LPA (Lucro por Ação) do ativo usando Yahoo Finance
def obtem_lpa(ticker, classe):
    ticker = ajustar_ticker(ticker, classe)
    ativo = yf.Ticker(ticker)
    try:
        return ativo.info.get('trailingEps', 0)
    except KeyError:
        return 0

# Função para buscar o VPA (Valor Patrimonial por Ação) do ativo usando Yahoo Finance
def obtem_vpa(ticker, classe):
    ticker = ajustar_ticker(ticker, classe)
    ativo = yf.Ticker(ticker)
    try:
        return ativo.info.get('bookValue', 0)
    except KeyError:
        return 0

# Função para buscar o valor histórico dos ativos
def obter_dados_historicos_ativo(ticker, classe, data_inicial):
    ticker = ajustar_ticker(ticker, classe)
    dados = yf.download(ticker, start=data_inicial)

    if not dados.empty:
        dados = dados[['Adj Close']]
        dados.reset_index(inplace=True)
        return dados
    else:
        return f"Nenhum dado encontrado para o ativo '{ticker}' desde {data_inicial}."
