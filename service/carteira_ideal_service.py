from flask import render_template, redirect, url_for, flash

import repository.carteira_ideal_repository as carteira_ideal_repository

def consulta_carteira_ideal(session, request):
    user_id = session['user_id']

    if request.method == 'POST':
        classe_ativo = request.form['classe_ativo']
        porcentagem = float(request.form['porcentagem'])

        soma_porcentagem_atual = carteira_ideal_repository.consulta_soma_porcentagem(user_id)

        nova_soma = soma_porcentagem_atual + porcentagem

        porcentagem_existente = carteira_ideal_repository.consulta_porcentagem(user_id, classe_ativo)

        if porcentagem_existente:
            nova_soma = soma_porcentagem_atual - porcentagem_existente[0] + porcentagem

        if nova_soma > 100:
            flash('A soma das porcentagens não pode ultrapassar 100%', 'danger')
        else:
            if porcentagem_existente:
                carteira_ideal_repository.atualiza_porcentagem_classe_ativo(porcentagem, user_id, classe_ativo)
            else:
                carteira_ideal_repository.inclui_porcentagem_classe_ativo(user_id, classe_ativo, porcentagem)
            flash('Alocação atualizada com sucesso!', 'success')
    
    if request.method == 'GET':
        alocacoes = carteira_ideal_repository.consulta_alocacao_carteira_ideal(user_id)
        soma_total = carteira_ideal_repository.consulta_soma_porcentagem(user_id)

        alocacoes_json = {alocacao[0]: alocacao[1] for alocacao in alocacoes if alocacao[1] > 0}

        return render_template('carteira_ideal.html', alocacoes=alocacoes, soma_total=soma_total, alocacoes_json=alocacoes_json)

    return redirect(url_for('carteira_ideal'))

def editar_alocacao(session, request):
    user_id = session['user_id']
    classe_ativo = request.form['classe_ativo']
    porcentagem = float(request.form['porcentagem'])

    soma_atual = carteira_ideal_repository.consulta_soma_porcentagem(user_id)
    porcentagem_existente = carteira_ideal_repository.consulta_porcentagem(user_id, classe_ativo)

    if porcentagem_existente:
        nova_soma = soma_atual - porcentagem_existente[0] + porcentagem
    else:
        nova_soma = soma_atual + porcentagem

    if nova_soma > 100:
        flash('A soma das porcentagens não pode ultrapassar 100%', 'danger')
    else:
        carteira_ideal_repository.atualiza_porcentagem_classe_ativo(porcentagem, user_id, classe_ativo)
        flash('Alocação atualizada com sucesso!', 'success')
    
    return redirect('/carteira_ideal')

def excluir_alocacao(session, request):
    user_id = session['user_id']
    classe_ativo = request.form['classe_ativo']

    carteira_ideal_repository.excluir_porcentagem_classe_ativo(user_id, classe_ativo)
    flash('Alocação excluída com sucesso!', 'success')
    
    return redirect('/carteira_ideal')

def cadastrar_ativos(classe_ativo, session, request):
    user_id = session['user_id']
    
    if request.method == 'POST':
        nome_ativo = request.form['nome_ativo']
        nota_ativo = request.form['nota_ativo']
        
        carteira_ideal_repository.inclui_ativo(user_id, classe_ativo, nome_ativo, nota_ativo)
        
        flash('Ativo cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))
    
    ativos = carteira_ideal_repository.listar_ativos(user_id, classe_ativo)
    soma_notas = sum(float(ativo[1]) for ativo in ativos)
    
    return render_template('cadastrar_ativos.html', classe_ativo=classe_ativo, ativos=ativos, soma_notas=soma_notas)

def editar_ativo(session, request):
    user_id = session['user_id']

    classe_ativo = request.form['classe_ativo']
    ativo = request.form['nome_ativo']
    nota = float(request.form['nota_ativo'])

    carteira_ideal_repository.editar_ativo(user_id, ativo, nota)

    flash('Ativo atualizado com sucesso!', 'success')
    return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))

def excluir_ativo(session, request):
    user_id = session['user_id']

    classe_ativo = request.form['classe_ativo']
    ativo = request.form['nome_ativo']

    carteira_ideal_repository.remove_ativo(user_id, ativo)

    flash('Ativo excluído com sucesso!', 'success')
    return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))
