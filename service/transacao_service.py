from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
from util import conversor
import app
import repository.transacao_repository as transacao_repository

# Extensões permitidas para upload de arquivos
EXTENSOES_PERMITIDAS = {'csv', 'xlsx'}

def upload_transacoes(request):
    if request.method == 'POST':
        file = request.files.get('file')
        
        # Validações de upload
        if not file or file.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        
        if valida_arquivos_permitidos(file.filename):
            upload_folder = app.app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            import_transacoes(filepath, session['user_id'])
            flash('Transações importadas com sucesso!', 'success')
            return redirect(url_for('dashboard'))
    
    return render_template('upload_transacoes.html')

def valida_arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def import_transacoes(filepath, user_id):
    ext = filepath.rsplit('.', 1)[1].lower()
    df = pd.read_csv(filepath) if ext == 'csv' else pd.read_excel(filepath)

    for _, row in df.iterrows():
        if not transacao_repository.consulta_transacoes(user_id, row):
            transacao_repository.inserir_transacao(user_id, row)
    
    os.remove(filepath)

def lista_transacoes():
    consulta_transacoes = transacao_repository.listar_todas_transacoes()
    transacoes = {}
    totais = {'compras': 0, 'vendas': 0, 'bonificacoes': 0}

    for transacao in consulta_transacoes:
        codigo_ativo = transacao[4]
        operacao = transacao[5]
        quantidade = conversor.convert_to_float(transacao[6])
        preco_unitario = conversor.convert_to_float(transacao[7])
        valor = round(preco_unitario * quantidade, 2)

        # Organização de transações por ativo
        if codigo_ativo not in transacoes:
            transacoes[codigo_ativo] = {'transacoes': [], 'total_quantidade': 0}
        
        transacoes[codigo_ativo]['transacoes'].append(transacao)
        
        # Cálculo dos totais por tipo de operação
        if operacao == 'C':
            totais['compras'] += valor
        elif operacao == 'V':
            totais['vendas'] += valor
        elif operacao == 'B':
            totais['bonificacoes'] += valor

    totais = {k: round(v, 2) for k, v in totais.items()}
    total_movimentacao = round(totais['compras'] - totais['vendas'], 2)

    return render_template('transacoes.html', transacoes=transacoes, totais=totais, total_movimentacao=total_movimentacao)
