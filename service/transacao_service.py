from flask import render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

import os
import pandas as pd

import app as app

import util.conversor as conversor
import repository.transacao_repository as transacao_repository

EXTENSOES_PERMITIDAS = {'csv', 'xlsx'}

def upload_transacoes(request):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        if file and valida_arquivos_permitidos(file.filename):
            if not os.path.exists(app.app.config['UPLOAD_FOLDER']):
                os.makedirs(app.app.config['UPLOAD_FOLDER'])
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            import_transacoes(filepath, session['user_id'])
            flash('Transações importadas com sucesso!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload_transacoes.html')

def valida_arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def import_transacoes(filepath, user_id):
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'csv':
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    for row in df.iterrows():
        existe_transacao = transacao_repository.consulta_transacoes(user_id, row)

        if not existe_transacao:
            transacao_repository.inserir_transacao(user_id, row)
    os.remove(filepath)

def lista_transacoes():
    consulta_transacoes = transacao_repository.listar_todas_transacoes()

    transacoes = {}
    totais = {
        'compras': 0,
        'vendas': 0,
        'bonificacoes': 0
    }

    for transacao in consulta_transacoes:
        codigo_ativo = transacao[4]
        operacao = transacao[5]
        quantidade = conversor.convert_to_float(transacao[6])
        preco_unitario = conversor.convert_to_float(transacao[7])
        valor = preco_unitario * quantidade

        if codigo_ativo not in transacoes:
            transacoes[codigo_ativo] = {
                'transacoes': [],
                'total_quantidade': 0
            }
        
        transacoes[codigo_ativo]['transacoes'].append(transacao)

        if operacao == 'C':
            totais['compras'] += valor
        elif operacao == 'V':
            totais['vendas'] += valor
        elif operacao == 'B':
            totais['bonificacoes'] += valor

    # Arredondar os totais para 2 casas decimais
    totais = {k: round(v, 2) for k, v in totais.items()}

    # Calcular o total de movimentação
    total_movimentacao = totais['compras'] - totais['vendas']
    total_movimentacao = round(total_movimentacao, 2)

    return render_template('transacoes.html', transacoes=transacoes, totais=totais, total_movimentacao=total_movimentacao)