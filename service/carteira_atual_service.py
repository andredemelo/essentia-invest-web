from flask import render_template
from datetime import datetime
import math
import util.conversor as conversor
import repository.carteira_ideal_repository as carteira_ideal_repo
import repository.transacao_repository as transacao_repo
import repository.dividendos_repository as dividendos_repo

def consulta_carteira_atual(session):
    user_id = session['user_id']
    ativos_carteira = carteira_ideal_repo.consulta_ativos_carteira(user_id)

    # Organizar os ativos por classe de ativo
    ativos_por_classe = {}
    for ativo in ativos_carteira:
        classe = ativo[0]
        ativos_por_classe.setdefault(classe, []).append(ativo)

    dados_ativos = []
    total_patrimonio = 0
    consolidado_classe = {}

    # Processar cada classe de ativo
    for classe, ativos in ativos_por_classe.items():
        total_notas = round(sum(ativo[2] for ativo in ativos), 2)
        total_valor_classe, total_investido_valor_classe = 0, 0
        
        for ativo in ativos:
            ticker = ativo[1]
            preco_atual = ativo[3] or 0
            quantidade, preco_medio, preco_atual = obter_quantidade_preco_medio_preco_atual(user_id, ticker, ativo[0], preco_atual)
            nota = ativo[2]

            total_investido = preco_medio * quantidade
            total_atual = preco_atual * quantidade
            total_valor_classe += total_atual
            total_investido_valor_classe += total_investido

            preco_justo_bazin = calcular_preco_justo_bazin(user_id, ticker, classe)
            preco_justo_graham = calcula_preco_justo_benjamin_graham(user_id, ticker, classe)

            dados_ativos.append({
                'classe': classe,
                'ticker': ticker,
                'quantidade': quantidade,
                'preco_medio': round(preco_medio, 2),
                'nota': nota,
                'preco_atual': round(preco_atual, 2),
                'preco_justo_bazin': round(preco_justo_bazin, 2),
                'preco_justo_graham': round(preco_justo_graham, 2),
                'valor_diferenca': round(total_atual - total_investido, 2),
                'total_atual': round(total_atual, 2),
                'total_investido': round(total_investido, 2),
                'porcentagem_ideal': 0
            })

        # Ajustar valores de ativos em dólares para reais
        if classe in {'etf_eua', 'stocks'}:
            total_investido_valor_classe = conversor.dolar_para_real(total_investido_valor_classe)
        
        consolidado_classe[classe] = {
            'total_valor': round(total_valor_classe, 2),
            'total_investido': round(total_investido_valor_classe, 2),
            'total_diferenca': round(total_valor_classe - total_investido_valor_classe, 2),
            'total_notas': total_notas
        }
        
        total_patrimonio += total_valor_classe

    # Calcular porcentagens ideais e necessidade de aporte para cada classe
    soma_porcentagem_atual, soma_porcentagem_ideal = 0, 0
    for classe, dados in consolidado_classe.items():
        porcentagem_ideal = carteira_ideal_repo.consulta_porcentagem(user_id, classe)[0] or 0
        porcentagem_atual = (dados['total_valor'] / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        diferenca_porcentagem = round(porcentagem_ideal - porcentagem_atual, 2)

        consolidado_classe[classe].update({
            'porcentagem_atual': round(porcentagem_atual, 2),
            'porcentagem_ideal': porcentagem_ideal,
            'necessidade_aporte': 'Aportar' if porcentagem_atual < porcentagem_ideal else 'Esperar',
            'diferenca_aporte': diferenca_porcentagem
        })

        soma_porcentagem_atual += porcentagem_atual
        soma_porcentagem_ideal += porcentagem_ideal

    # Atualizar porcentagem ideal em dados_ativos e necessidade de aporte
    for ativo in dados_ativos:
        classe = ativo['classe']
        nota = ativo['nota']
        porcentagem_ideal = consolidado_classe[classe]['porcentagem_ideal']
        porcentagem_ideal_atualizado = round((nota * 100) / consolidado_classe[classe]['total_notas'], 2) if consolidado_classe[classe]['total_notas'] != 0 else 0
        ativo['porcentagem_ideal'] = porcentagem_ideal_atualizado

        # Calcular porcentagem atual e necessidade de aporte
        porcentagem_atual = (ativo['total_atual'] / total_patrimonio) * 100 if total_patrimonio != 0 else 0
        ativo.update({
            'porcentagem_atual': round(porcentagem_atual, 2),
            'necessidade_aporte': 'Aportar' if porcentagem_atual < porcentagem_ideal_atualizado else 'Esperar',
            'diferenca_aporte': round(porcentagem_ideal_atualizado - porcentagem_atual, 2)
        })

    # Calcular totais
    soma_total_valor = round(sum(dados['total_valor'] for dados in consolidado_classe.values()), 2)
    soma_total_valor_investido = round(sum(dados['total_investido'] for dados in consolidado_classe.values()), 2)
    soma_total_valor_diferenca = round(sum(dados['total_diferenca'] for dados in consolidado_classe.values()), 2)

    return render_template('carteira_atual.html', dados_ativos=dados_ativos, consolidado_classe=consolidado_classe,
                           soma_total_valor=soma_total_valor, soma_total_valor_investido=soma_total_valor_investido,
                           soma_total_valor_diferenca=soma_total_valor_diferenca)

def obter_quantidade_preco_medio_preco_atual(user_id, ticker, classe, preco_atual):
    if classe == 'renda_fixa':
        return precos_renda_fixa(ticker, preco_atual)
    elif classe == 'fiis' and ticker == 'BCFF11':
        return calcula_quantidade_ativo(user_id, ticker), 8.73, 7.28
    elif classe == 'fiis' and ticker == 'VINO11':
        return calcula_quantidade_ativo(user_id, ticker), 9.26, preco_atual
    return calcula_quantidade_ativo(user_id, ticker), calcula_preco_medio(user_id, ticker), preco_atual

def precos_renda_fixa(ticker, preco_atual):
    precos = {
        'SUL AMERICA EXCLUSIVE FI RF REF DI': (185.00, 98.52, preco_atual),
        'TREND DI FIC FI RF SIMPLES': (10129.60, 1.25, preco_atual),
        'TREND INB FIC FI RF SIMPLES': (698.85, 1.37, preco_atual)
    }
    return precos.get(ticker, (0, 0, preco_atual))

def calcula_quantidade_ativo(user_id, ticker):
    transacoes = transacao_repo.consulta_transacoes_ativo(user_id, ticker)
    quantidade_total = sum(float(t[1].replace(',', '.')) * (1 if t[0] in {'C', 'B'} else -1) for t in transacoes)
    return round(quantidade_total, 2)

def calcula_preco_medio(user_id, ticker):
    transacoes = transacao_repo.consulta_transacoes_ativo(user_id, ticker)
    valor_total, quantidade_total = 0, 0
    for operacao, quantidade, preco in transacoes:
        quantidade = float(quantidade.replace(',', '.'))
        preco = float(preco.replace(',', '.'))
        if operacao in {'C', 'B'}:
            quantidade_total += quantidade
            valor_total += preco * quantidade
        elif operacao == 'V':
            quantidade_total -= quantidade
            valor_total -= preco * quantidade
    return round(valor_total / quantidade_total, 2) if quantidade_total else 0.0

def calcular_preco_justo_bazin(user_id, ticker, classe):
    ano_consulta = str(datetime.now().year - 1)
    dividendos = dividendos_repo.consulta_dividendos_do_ano(ticker, ano_consulta)
    valor_dividendo_anual = sum(
        float(d[0].replace(',', '.')) if isinstance(d[0], str) else d[0]  # Verifica se é uma string
        for d in dividendos
    )
    dividend_yield_desejado = carteira_ideal_repo.consulta_dividendo_desejado_carteira_ideal(user_id, classe)[0] or 0
    return valor_dividendo_anual / (dividend_yield_desejado / 100) if dividend_yield_desejado else 0

def calcula_preco_justo_benjamin_graham(user_id, ticker, classe):
    lpa, vpa = next(iter(carteira_ideal_repo.consulta_indicadores_ativo(user_id, classe, ticker)), (0, 0))
    return math.sqrt(22.5 * lpa * vpa) if lpa and vpa else 0
