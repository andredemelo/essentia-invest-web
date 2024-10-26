import repository.carteira_ideal_repository as carteira_ideal_repository

import util.yahoo_finance as yahoo_finance
import util.conversor as conversor

def atualiza_preco_atual():
    print('Atualização Iniciada!')
    ativos = carteira_ideal_repository.consulta_preco_atual_ativo()

    for ativo in ativos:
        classe = ativo[0]
        ticker = ativo[1]

        print('Atualiza Preço dos Atual')
        if classe != 'renda_fixa':
            preco_atual = round(yahoo_finance.obtem_preco_atual(ticker, classe), 2)
        elif classe == 'renda_fixa' and ticker == 'SUL AMERICA EXCLUSIVE FI RF REF DI':
            preco_atual = 113.07
        elif classe == 'renda_fixa' and ticker == 'TREND DI FIC FI RF SIMPLES':
            preco_atual = 1.28
        elif classe == 'renda_fixa' and ticker == 'TREND INB FIC FI RF SIMPLES':
            preco_atual = 1.45
        if classe == 'etf_eua': 
            preco_atual = round(conversor.dolar_para_real(preco_atual), 2)
        
        lpa = 0
        vpa = 0
        if classe == 'acao':
            print('Atualiza LPA e VPA para Ações do Brasil!')
            lpa = round(yahoo_finance.obtem_lpa(ticker, classe), 2)
            vpa = round(yahoo_finance.obtem_vpa(ticker, classe), 2)

        carteira_ideal_repository.atualiza_dados__ativo(classe, ticker, preco_atual, lpa, vpa)
    
    print('Atualização Concluída!')

