from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.utils import secure_filename
from util import conversor
from collections import defaultdict
from datetime import datetime

import os
import pandas as pd
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

def lista_transacoes(session):
    user_id = session['user_id']
    consulta_transacoes = transacao_repository.listar_todas_transacoes(user_id)
    transacoes = {}
    totais = {'compras': 0, 'vendas': 0, 'bonificacoes': 0}
    totais_por_mes = defaultdict(lambda: {'compras': 0, 'vendas': 0, 'bonificacoes': 0})

    for transacao in consulta_transacoes:
        codigo_ativo = transacao[4]
        operacao = transacao[5]
        quantidade = conversor.convert_to_float(transacao[6])
        preco_unitario = conversor.convert_to_float(transacao[7])
        valor = round(preco_unitario * quantidade, 2)
        
        # Data da operação formatada
        data_operacao = datetime.strptime(transacao[2], "%d/%m/%Y")
        mes_ano = data_operacao.strftime("%Y-%m")

        # Organização de transações por ativo
        if codigo_ativo not in transacoes:
            transacoes[codigo_ativo] = {'transacoes': [], 'total_quantidade': 0}
        
        transacoes[codigo_ativo]['transacoes'].append(transacao)
        
        # Cálculo dos totais por tipo de operação
        if operacao == 'C':
            totais['compras'] += valor
            totais_por_mes[mes_ano]['compras'] += valor
        elif operacao == 'V':
            totais['vendas'] += valor
            totais_por_mes[mes_ano]['vendas'] += valor
        elif operacao == 'B':
            totais['bonificacoes'] += valor
            totais_por_mes[mes_ano]['bonificacoes'] += valor

    totais = {k: round(v, 2) for k, v in totais.items()}
    total_movimentacao = round(totais['compras'] - totais['vendas'], 2)

    # Converte totais por mês para JSON serializável
    totais_por_mes = dict(sorted(totais_por_mes.items()))

    return render_template(
        'transacoes.html',
        transacoes=transacoes,
        totais=totais,
        total_movimentacao=total_movimentacao,
        totais_por_mes=totais_por_mes
    )
