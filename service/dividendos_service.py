from flask import render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename

import os
import pandas as pd

import app as app
import repository.dividendos_repository as dividendos_repository

EXTENSOES_PERMITIDAS = {'csv', 'xlsx'}

def upload_dividendos(request):
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
            import_dividendos(filepath, session['user_id'])
            flash('Dividendos importadas com sucesso!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload_dividendos.html')

def valida_arquivos_permitidos(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def import_dividendos(filepath, user_id):
    ext = filepath.rsplit('.', 1)[1].lower()
    if ext == 'csv':
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)

    # Convertendo colunas de datas para string
    df['Data com'] = pd.to_datetime(df['Data com']).dt.strftime('%d-%m-%Y')
    df['Pagamento'] = pd.to_datetime(df['Pagamento']).dt.strftime('%d-%m-%Y')

    for index, row in df.iterrows():
        consulta_dividendo = dividendos_repository.consulta_dividendos(user_id, row)

        if consulta_dividendo is None or len(consulta_dividendo) == 0:
            dividendos_repository.incluir_dividendo(user_id, row)
    
    os.remove(filepath)

def consulta_dividendos():
    dividendos = dividendos_repository.consulta_todos_dividendos()
    
    dividendos_por_codigo = {}
    total_dividendos_por_codigo = {}
    
    for dividendo in dividendos:
        codigo_ativo = dividendo[3]
        valor_total_liquido = dividendo[9]
        
        if codigo_ativo not in dividendos_por_codigo:
            dividendos_por_codigo[codigo_ativo] = []
            total_dividendos_por_codigo[codigo_ativo] = 0
        
        dividendos_por_codigo[codigo_ativo].append(dividendo)
        total_dividendos_por_codigo[codigo_ativo] += valor_total_liquido
    
    total_dividendos_por_codigo = {k: round(v, 2) for k, v in total_dividendos_por_codigo.items()}
    
    # Calcula o total geral dos dividendos recebidos
    total_geral_dividendos = round(sum(total_dividendos_por_codigo.values()), 2)
    
    return render_template('dividendos.html', dividendos_por_codigo=dividendos_por_codigo, total_dividendos_por_codigo=total_dividendos_por_codigo, total_geral_dividendos=total_geral_dividendos)