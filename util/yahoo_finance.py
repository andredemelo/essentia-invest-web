import yfinance as yf
import pandas as pd

# Função para buscar o preço atual do ativo usando Yahoo Finance
def obtem_preco_atual(ticker, classe):
    if classe == 'acao' or classe == 'fiis':
        ticker = ticker + '.SA'
    ativo = yf.Ticker(ticker)
    hist = ativo.history(period="1d")
    if not hist.empty:
        return hist['Close'][-1]
    return 0

# Função para buscar o Dividend Yield do ativo usando Yahoo Finance
def obtem_dividend_yield(ticker, classe):
    if classe == 'acao' or classe == 'fiis':
        ticker = ticker + '.SA'
    if classe == 'etf_eua':
        ticker = ticker + '.F'

    ativo = yf.Ticker(ticker)
    try:
        return ativo.info['dividendYield'] * 100
    except KeyError:
        return 0

# Função para buscar o LPA (Lucro por Ação) do ativo usando Yahoo Finance
def obtem_lpa(ticker, classe):
    if classe == 'acao' or classe == 'fiis':
        ticker = ticker + '.SA'
    if classe == 'etf_eua':
        ticker = ticker + '.F'
    
    ativo = yf.Ticker(ticker)
    try:
        return ativo.info['trailingEps']
    except KeyError:
        return 0

# Função para buscar o VPA (Valor Patrimonial por Ação) do ativo usando Yahoo Finance
def obtem_vpa(ticker, classe):
    if classe == 'acao' or classe == 'fiis':
        ticker = ticker + '.SA'
    if classe == 'etf_eua':
        ticker = ticker + '.F'
    
    ativo = yf.Ticker(ticker)
    try:
        return ativo.info['bookValue']
    except KeyError:
        return 0