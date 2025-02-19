from flask import render_template
from datetime import datetime
import math

import util.conversor as conversor

import repository.carteira_ideal_repository as carteira_ideal_repository
import repository.transacao_repository as transacao_repository
import repository.dividendos_repository as dividendos_repository

def consulta_balanceamento_carteira(session):
    user_id = session['user_id']
    ativos_carteira = carteira_ideal_repository.consulta_ativos_carteira(user_id)
    
    # Organizar os ativos por classe de ativo
    ativos_por_classe = agrupar_ativos_por_classe(ativos_carteira)
    
    dados_ativos, total_patrimonio, consolidado_classe = calcular_total_ativos(user_id, ativos_por_classe)
    
    # Calcular porcentagem ideal e necessidade de aporte
    consolidado_classe = calcular_balanceamento_classe(user_id, consolidado_classe, total_patrimonio)
    
    # Calcular porcentagem ideal para cada ativo individualmente
    soma_total_notas = sum(dados['total_notas'] for dados in consolidado_classe.values())
    dados_ativos = calcular_balanceamento_individual(dados_ativos, consolidado_classe, soma_total_notas, total_patrimonio)

    return render_template('balanceamento_carteira.html', dados_ativos=dados_ativos, consolidado_classe=consolidado_classe)

def agrupar_ativos_por_classe(ativos_carteira):
    ativos_por_classe = {}
    for ativo in ativos_carteira:
        classe = ativo[0]
        if classe not in ativos_por_classe:
            ativos_por_classe[classe] = []
        ativos_por_classe[classe].append(ativo)
    return ativos_por_classe

def calcular_total_ativos(user_id, ativos_por_classe):
    dados_ativos = []
    total_patrimonio = 0
    consolidado_classe = {}
    
    for classe, ativos in ativos_por_classe.items():
        total_notas = sum(ativo[2] for ativo in ativos)
        total_valor_classe = 0
        
        for ativo in ativos:
            ticker = ativo[1]
            quantidade, preco_medio, preco_atual = obter_dados_ativo(user_id, ativo)
            total_atual = preco_atual * quantidade if preco_atual else 0
            total_valor_classe += total_atual
            valor_diferenca = (preco_atual - preco_medio) * quantidade
            
            dados_ativos.append({
                'classe': classe,
                'ticker': ticker,
                'nota': ativo[2],
                'valor_diferenca': round(valor_diferenca, 2),
                'total_atual': round(total_atual, 2),
                'porcentagem_ideal': 0
            })
        
        total_patrimonio += total_valor_classe
        consolidado_classe[classe] = {
            'total_valor': round(total_valor_classe, 2),
            'total_notas': round(total_notas, 2)
        }
    
    return dados_ativos, total_patrimonio, consolidado_classe

def obter_dados_ativo(user_id, ativo):
    ticker = ativo[1]
    classe = ativo[0]
    preco_atual = ativo[3]
    
    if classe != 'renda_fixa':
        if ticker == 'BTHF11':
            return 760, 10.21, 7.89
        elif ticker == 'VINO11':
            return 1747.0, 9.26, preco_atual
        elif classe == 'etf_eua': 
            return calcula_quantidade_ativo(user_id, ticker), round(calcula_preco_medio(user_id, ticker)), round(preco_atual, 2)
        else:
            return calcula_quantidade_ativo(user_id, ticker), calcula_preco_medio(user_id, ticker), preco_atual
    elif classe == 'renda_fixa' and ticker == 'TREND DI FIC FI RF SIMPLES':
        return 36286.43, 1.28, 1.32
    elif classe == 'renda_fixa' and ticker == 'TREND INB FIC FI RF SIMPLES':
        return 838.70, 1.39, 1.50

def calcular_balanceamento_classe(user_id, consolidado_classe, total_patrimonio):
    for classe, dados in consolidado_classe.items():
        porcentagem_ideal = carteira_ideal_repository.consulta_porcentagem(user_id, classe)
        porcentagem_ideal = porcentagem_ideal[0] if porcentagem_ideal else 0
        porcentagem_atual = (dados['total_valor'] / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        necessidade_aporte = 'Aportar' if porcentagem_atual < porcentagem_ideal else 'Esperar'
        diferenca_porcentagem = round(porcentagem_ideal - porcentagem_atual, 2)

        dados.update({
            'porcentagem_atual': round(porcentagem_atual, 2),
            'porcentagem_ideal': porcentagem_ideal,
            'necessidade_aporte': necessidade_aporte,
            'diferenca_aporte': diferenca_porcentagem
        })
    
    return consolidado_classe

def calcular_balanceamento_individual(dados_ativos, consolidado_classe, soma_total_notas, total_patrimonio):
    for ativo in dados_ativos:
        classe = ativo['classe']
        nota = ativo['nota']
        porcentagem_ideal_atualizado = round((nota * 100) / soma_total_notas, 2) if soma_total_notas != 0 else 0
        ativo['porcentagem_ideal'] = porcentagem_ideal_atualizado

        total_atual = ativo['total_atual']
        porcentagem_atual = (total_atual / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        ativo['porcentagem_atual'] = round(porcentagem_atual, 2)

        necessidade_aporte = 'Aportar' if porcentagem_atual < porcentagem_ideal_atualizado else 'Esperar'
        ativo['necessidade_aporte'] = necessidade_aporte

        diferenca_aporte = porcentagem_ideal_atualizado - porcentagem_atual
        ativo['diferenca_aporte'] = round(diferenca_aporte, 2)

    return dados_ativos

def calcula_quantidade_ativo(user_id, ticker):
    transacoes = transacao_repository.consulta_transacoes_ativo(user_id, ticker)
    quantidade_total = sum(
        float(transacao[1].replace(',', '.')) if transacao[0] in ('C', 'B') else -float(transacao[1].replace(',', '.'))
        for transacao in transacoes
    )
    return round(quantidade_total, 2)

def calcula_preco_medio(user_id, ticker):
    transacoes = transacao_repository.consulta_transacoes_ativo(user_id, ticker)
    quantidade_total = 0.0
    valor_total_compra = 0.0
    for operacao, quantidade_str, preco_str in transacoes:
        quantidade = float(quantidade_str.replace(',', '.'))
        preco = float(preco_str.replace(',', '.'))
        if operacao in ('C', 'B'):
            quantidade_total += quantidade
            valor_total_compra += preco * quantidade
        elif operacao == 'V':
            quantidade_total -= quantidade
            valor_total_compra -= preco * quantidade
    
    return round(valor_total_compra / quantidade_total, 2) if quantidade_total != 0 else 0.0
