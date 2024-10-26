from flask import render_template
from datetime import datetime

import math

import repository.carteira_ideal_repository as carteira_ideal_repository
import repository.transacao_repository as transacao_repository
import repository.dividendos_repository as dividendos_repository

def consulta_balanceamento_carteira(session):
    user_id = session['user_id']
    ativos_carteira = carteira_ideal_repository.consulta_ativos_carteira(user_id)

    # Organizar os ativos por classe de ativo
    ativos_por_classe = {}
    for ativo in ativos_carteira:
        classe = ativo[0]
        if classe not in ativos_por_classe:
            ativos_por_classe[classe] = []
        ativos_por_classe[classe].append(ativo)
    
    # Calcula total atual
    dados_ativos = []
    total_patrimonio = 0
    consolidado_classe = {}
    for classe, ativos in ativos_por_classe.items():
        total_notas = round(sum([ativo[2] for ativo in ativos]), 2)
        total_valor_classe = 0
        for ativo in ativos:
            ticker = ativo[1]
            if ativo[0] != 'renda_fixa':
                if ativo[1] == 'BCFF11':
                    quantidade = 950.0
                    preco_medio = 8.73
                elif ativo[1] == 'VINO11':
                    quantidade = 1747.0
                    preco_medio = 9.26
                else:
                    quantidade = calcula_quantidade_ativo(user_id, ticker)
                    preco_medio = calcula_preco_medio(user_id, ticker)
            elif ativo[0] == 'renda_fixa':
                if ativo[1] == 'SUL AMERICA EXCLUSIVE FI RF REF DI' :
                    quantidade = 198.23
                    preco_medio = 98.52
                elif ativo[1] == 'TREND DI FIC FI RF SIMPLES':
                    quantidade = 8770.28
                    preco_medio = 1.24
                elif ativo[1] == 'TREND INB FIC FI RF SIMPLES':
                    quantidade = 648.42
                    preco_medio = 1.36
            else:
                preco_medio = 0
            
            nota = ativo[2]
            preco_atual = ativo[3]

            total_atual = preco_atual * quantidade if preco_atual else 0
            total_valor_classe += total_atual
            valor_diferenca = (preco_atual * quantidade) - (preco_medio * quantidade)
            
            dados_ativos.append({
                'classe': classe,
                'ticker': ticker,
                'nota': nota,
                'valor_diferenca': round(valor_diferenca, 2),
                'total_atual': round(total_atual, 2),
                'porcentagem_ideal': 0
            })
        total_patrimonio += total_valor_classe
        consolidado_classe[classe] = {
            'total_valor': round(total_valor_classe, 2),
            'total_notas': total_notas
        }
    
    # Calcular porcentagem ideal para cada classe de ativo e necessidade de aporte/espera
    for classe, dados in consolidado_classe.items():
        porcentagem_ideal = carteira_ideal_repository.consulta_porcentagem(user_id, classe)
        porcentagem_ideal = porcentagem_ideal[0] if porcentagem_ideal else 0
        porcentagem_atual = (dados['total_valor'] / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        necessidade_aporte = 'Aportar' if porcentagem_atual < porcentagem_ideal else 'Esperar'
        diferenca_porcentagem = round(porcentagem_ideal - porcentagem_atual, 2)
        consolidado_classe[classe].update({
            'porcentagem_atual': round(porcentagem_atual, 2),
            'porcentagem_ideal': porcentagem_ideal,
            'necessidade_aporte': necessidade_aporte,
            'diferenca_aporte': diferenca_porcentagem
        })

    # Calcular soma
    soma_total_notas = round(sum(dados['total_notas'] for dados in consolidado_classe.values()), 2)

    for ativo in dados_ativos:
        # Atualizar porcentagem ideal em dados_ativos
        classe = ativo['classe']
        nota = ativo['nota']
        porcentagem_ideal = consolidado_classe[classe]['porcentagem_ideal']
        porcentagem_ideal_atualizado = round((nota * 100) / soma_total_notas, 2) if soma_total_notas != 0 else 0
        ativo['porcentagem_ideal'] = porcentagem_ideal_atualizado

        # Calcular porcentagem atual
        total_atual = float(ativo.get('total_atual', 0))
        porcentagem_atual = (total_atual / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        ativo['porcentagem_atual'] = round(porcentagem_atual, 2)

        # Adiciona Ação de Aportar ou Esperar
        necessidade_aporte = 'Aportar' if porcentagem_atual < porcentagem_ideal_atualizado else 'Esperar'
        ativo['necessidade_aporte'] = necessidade_aporte

        diferenca_aporte = porcentagem_ideal_atualizado - porcentagem_atual
        ativo['diferenca_aporte'] = round(diferenca_aporte, 2)

    return render_template('balanceamento_carteira.html', dados_ativos=dados_ativos, consolidado_classe=consolidado_classe)

def calcula_quantidade_ativo(user_id, ticker):
    transacoes = transacao_repository.consulta_transacoes_ativo(user_id, ticker)
    quantidade_total = 0.0
    for transacao in transacoes:
        quantidade = float(transacao[1].replace(',', '.'))
        if transacao[0] == 'C' or transacao[0] == 'B':
            quantidade_total = quantidade_total + quantidade
        elif transacao[0] == 'V':
            quantidade_total = quantidade_total - quantidade
    return round(quantidade_total, 2)

def calcula_preco_medio(user_id, ticker):
    transacoes = transacao_repository.consulta_transacoes_ativo(user_id, ticker)
    quantidade_total = 0.0
    valor_total_compra = 0.0
    for transacao in transacoes:
        operacao = transacao[0]
        quantidade = float(transacao[1].replace(',', '.'))
        preco = float(transacao[2].replace(',', '.'))
        if operacao == 'C' or operacao == 'B':
            quantidade_total = quantidade_total + quantidade
            valor_total_compra = valor_total_compra + (preco * quantidade)
        elif operacao == 'V':
            quantidade_total = quantidade_total - quantidade
            valor_total_compra = valor_total_compra - (preco * quantidade)
    
    if quantidade_total == 0:
        return 0.0

    return round(valor_total_compra / quantidade_total, 2)
