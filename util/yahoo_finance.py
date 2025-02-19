import yfinance as yf

# Função para ajustar o ticker com base na classe
def ajustar_ticker(ticker, classe):
    if classe in ['acao', 'fiis']:
        return ticker + '.SA'
    return ticker

# Função genérica para obter informações do ativo
def obter_info_ativo(ticker, classe):
    ticker = ajustar_ticker(ticker, classe)
    ativo = yf.Ticker(ticker)
    return ativo

# Verifica se o ativo existe no Yahoo Finance
def ativo_existe(ticker):
    ativo = yf.Ticker(ticker)
    try:
        info = ativo.history(period="1d")
        return not info.empty
    except Exception as e:
        print(f"[Erro] Falha ao verificar existência do ativo {ticker}: {e}")
        return False

# Obtém o preço atual do ativo
def obtem_preco_atual(ticker, classe, tentativas=3):
    ticker = ajustar_ticker(ticker, classe)
    
    if not ativo_existe(ticker):
        print(f"[X] Ativo {ticker} não encontrado. Pulando atualização.")
        return None
    
    for tentativa in range(tentativas):
        try:
            ativo = yf.Ticker(ticker)
            hist = ativo.history(period="1d")

            if not hist.empty:
                preco = hist['Close'].iloc[-1]
                print(f"[✓] Preço encontrado para {ticker}: R$ {preco:.2f}")
                return preco
                break
            else:
                print(f"[!] Nenhum dado encontrado para {ticker}. Tentativa {tentativa + 1}/{tentativas}")
            
        except Exception as e:
            print(f"[Erro] Falha ao obter preço de {ticker}: {e}")
        
        time.sleep(2)  # Pequena pausa antes de tentar novamente
    
    print(f"[X] Não foi possível obter preço para {ticker} após {tentativas} tentativas.")
    return None

# Função para buscar o Dividend Yield do ativo
def obtem_dividend_yield(ticker, classe):
    ativo = obter_info_ativo(ticker, classe)
    return (ativo.info.get('dividendYield') or 0) * 100

# Função para buscar o LPA (Lucro por Ação)
def obtem_lpa(ticker, classe):
    ativo = obter_info_ativo(ticker, classe)
    return ativo.info.get('trailingEps') or 0

# Função para buscar o VPA (Valor Patrimonial por Ação)
def obtem_vpa(ticker, classe):
    ativo = obter_info_ativo(ticker, classe)
    return ativo.info.get('bookValue') or 0

# Função para buscar o valor histórico dos ativos
def obter_dados_historicos_ativo(ticker, classe, data_inicial):
    ticker = ajustar_ticker(ticker, classe)
    dados = yf.download(ticker, start=data_inicial)
    
    if not dados.empty:
        dados = dados[['Adj Close']]
        dados.reset_index(inplace=True)
        return dados
    return f"Nenhum dado encontrado para '{ticker}' desde {data_inicial}."
