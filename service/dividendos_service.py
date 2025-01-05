from flask import render_template, redirect, url_for, flash, session, request
from werkzeug.utils import secure_filename
from datetime import datetime
from collections import defaultdict
import os
import pandas as pd

import app as app
import repository.dividendos_repository as dividendos_repository

# Configuração das extensões permitidas para o upload
EXTENSOES_PERMITIDAS = {'csv', 'xlsx'}

def upload_dividendos(request):
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
        
        if valida_arquivo_permitido(file.filename):
            caminho_arquivo = salvar_arquivo(file)
            if caminho_arquivo:
                importar_dividendos(caminho_arquivo, session['user_id'])
                flash('Dividendos importados com sucesso!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Erro ao salvar o arquivo.', 'danger')
    return render_template('upload_dividendos.html')

def valida_arquivo_permitido(filename):
    """Valida se o arquivo possui uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS

def salvar_arquivo(file):
    """Salva o arquivo no diretório configurado para uploads."""
    if not os.path.exists(app.app.config['UPLOAD_FOLDER']):
        os.makedirs(app.app.config['UPLOAD_FOLDER'])
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filepath

def importar_dividendos(filepath, user_id):
    """Importa os dividendos a partir do arquivo especificado."""
    df = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)
    for _, row in df.iterrows():
        if not dividendos_repository.consulta_dividendos(user_id, row):
            dividendos_repository.incluir_dividendo(user_id, row)
    os.remove(filepath)

def consulta_dividendos():
    """Consulta e organiza os dividendos por código de ativo."""
    dividendos = dividendos_repository.consulta_todos_dividendos()
    
    dividendos_por_codigo = {}
    totais_dividendos = {
        "total_por_codigo": {},
        "recebido_por_codigo": {},
        "provisionado_por_codigo": {}
    }
    
    mensal_recebidos = defaultdict(float)
    mensal_provisionados = defaultdict(float)
    data_atual = datetime.now().date()
    
    for dividendo in dividendos:
        codigo_ativo, valor_total, data_com, data_pagamento = dividendo[3], dividendo[9], dividendo[10], dividendo[11]
        valor_total = float(valor_total.replace(',', '.')) if isinstance(valor_total, str) else float(valor_total)
        data_com = datetime.strptime(data_com, "%d/%m/%Y")
        data_pagamento = datetime.strptime(data_pagamento, "%d/%m/%Y").date()
        
        if codigo_ativo not in dividendos_por_codigo:
            dividendos_por_codigo[codigo_ativo] = []
            totais_dividendos["total_por_codigo"][codigo_ativo] = 0
            totais_dividendos["recebido_por_codigo"][codigo_ativo] = 0
            totais_dividendos["provisionado_por_codigo"][codigo_ativo] = 0
        
        dividendos_por_codigo[codigo_ativo].append(dividendo)
        totais_dividendos["total_por_codigo"][codigo_ativo] += valor_total

        if data_pagamento <= data_atual:
            totais_dividendos["recebido_por_codigo"][codigo_ativo] += valor_total
            mensal_recebidos[data_pagamento.strftime('%Y-%m')] += valor_total
        else:
            totais_dividendos["provisionado_por_codigo"][codigo_ativo] += valor_total
            mensal_provisionados[data_pagamento.strftime('%Y-%m')] += valor_total

    totais_gerais = {
        "geral": round(sum(totais_dividendos["total_por_codigo"].values()), 2),
        "recebidos": round(sum(totais_dividendos["recebido_por_codigo"].values()), 2),
        "provisionados": round(sum(totais_dividendos["provisionado_por_codigo"].values()), 2)
    }

    return render_template(
        'dividendos.html',
        dividendos_por_codigo=dividendos_por_codigo,
        total_dividendos_por_codigo=totais_dividendos["total_por_codigo"],
        total_dividendos_recebido_por_codigo=totais_dividendos["recebido_por_codigo"],
        total_dividendos_provisionado_por_codigo=totais_dividendos["provisionado_por_codigo"],
        total_geral_dividendos=totais_gerais["geral"],
        total_geral_dividendos_recebidos=totais_gerais["recebidos"],
        total_geral_dividendos_provisionados=totais_gerais["provisionados"],
        mensal_recebidos=mensal_recebidos,
        mensal_provisionados=mensal_provisionados
    )
