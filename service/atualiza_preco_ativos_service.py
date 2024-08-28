import repository.carteira_ideal_repository as carteira_ideal_repository

import util.yahoo_finance as yahoo_finance
import util.conversor as conversor

def atualiza_preco_atual():
    print('Atualização Iniciada!')
    ativos = carteira_ideal_repository.consulta_preco_atual_ativo()

    for ativo in ativos:
        classe = ativo[0]
        ticker = ativo[1]

        if classe != 'renda_fixa':
            preco_atual = round(yahoo_finance.obtem_preco_atual(ticker, classe), 2)
        elif classe == 'renda_fixa' and ticker == 'SUL AMERICA EXCLUSIVE FI RF REF DI':
            preco_atual = 110.99
        elif classe == 'renda_fixa' and ticker == 'TREND DI FIC FI RF SIMPLES':
            preco_atual = 1.25
        elif classe == 'renda_fixa' and ticker == 'TREND INB FIC FI RF SIMPLES':
            preco_atual = 1.42
            
        if classe == 'etf_eua': 
            preco_atual = round(conversor.dolar_para_real(preco_atual), 2)
        
        carteira_ideal_repository.atualiza_preco_atual_ativo(classe, ticker, preco_atual)
    
    print('Atualização Concluída!')

