import repository.carteira_ideal_repository as carteira_ideal_repository
import repository.historico_carteira_ideal_repository as historico_carteira_ideal_repository

import util.yahoo_finance as yahoo_finance
import util.conversor as conversor

from datetime import datetime, timedelta

RENDA_FIXA_PRECOS_ESPECIAIS = {
    'SUL AMERICA EXCLUSIVE FI RF REF DI': 113.55,
    'TREND DI FIC FI RF SIMPLES': 1.28,
    'TREND INB FIC FI RF SIMPLES': 1.46
}

def obter_preco_atual(ticker, classe):
    """Obtém o preço atual de um ativo com base na classe e ticker."""
    if classe == 'renda_fixa' and ticker in RENDA_FIXA_PRECOS_ESPECIAIS:
        return RENDA_FIXA_PRECOS_ESPECIAIS[ticker]
    
    preco = yahoo_finance.obtem_preco_atual(ticker, classe)
    if classe == 'etf_eua':
        preco = conversor.dolar_para_real(preco)
    return round(preco, 2)

def obter_lpa_vpa(classe, ticker):
    """Obtém o LPA e VPA de uma ação caso a classe seja 'acao'."""
    if classe != 'acao':
        return 0, 0
    lpa = yahoo_finance.obtem_lpa(ticker, classe)
    vpa = yahoo_finance.obtem_vpa(ticker, classe)
    return round(lpa, 2), round(vpa, 2)

def atualiza_preco_atual():
    print('Iniciando atualização de preços...')
    ativos = carteira_ideal_repository.consulta_preco_atual_ativo()

    for ativo in ativos:
        classe, ticker = ativo[0], ativo[1]
        print(f'Atualizando preço atual para o ativo: {ticker} ({classe})')
        
        preco_atual = obter_preco_atual(ticker, classe)
        lpa, vpa = obter_lpa_vpa(classe, ticker)
        
        carteira_ideal_repository.atualiza_dados__ativo(classe, ticker, preco_atual, lpa, vpa)
    
    print('Atualização concluída!')

def atualiza_historico_preco():
    print('Iniciando atualização de histórico de preço...')
    
    ativos = carteira_ideal_repository.consulta_preco_atual_ativo()

    for ativo in ativos:
        classe, ticker = ativo[0], ativo[1]
        print(f'Atualizando preço atual para o ativo: {ticker} ({classe})')

        if classe != 'renda_fixa':
            data_atual = datetime.now()
            dia_anterior = data_atual - timedelta(days=1)
            data_formatada = dia_anterior.strftime("%d/%m/%Y")

            preco_historico = historico_carteira_ideal_repository.consulta_data_preco_historico(classe, ticker, data_formatada)

            if preco_historico is None:
                dados = yahoo_finance.obter_dados_historicos_ativo(ticker, classe, dia_anterior)

                if isinstance(dados, str):
                    print(f"Erro ao buscar dados para o ativo {ticker}: {dados}")
                    continue
                
                for _, row in dados.iterrows():
                    data = row['Date'].strftime("%d-%m-%Y")
                    preco = round(row['Adj Close'], 2)
                    historico_carteira_ideal_repository.inclui_historico_preco(classe, ticker, data, preco)
            else:
                print('Preço já cadastrado no banco de dados!')

    print('Atualização concluída!')
