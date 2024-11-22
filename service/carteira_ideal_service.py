from flask import render_template, redirect, url_for, flash
import repository.carteira_ideal_repository as repo

def consulta_carteira_ideal(session, request):
    user_id = session.get('user_id')
    if not user_id:
        flash('Usuário não autenticado', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        classe_ativo = request.form.get('classe_ativo')
        porcentagem = float(request.form.get('porcentagem', 0))
        dividendo_desejado = request.form.get('dividendo_desejado')

        soma_atual, nova_soma = calcula_nova_soma(user_id, classe_ativo, porcentagem)
        
        if nova_soma > 100:
            flash('A soma das porcentagens não pode ultrapassar 100%', 'danger')
        else:
            atualizar_ou_incluir_alocacao(user_id, classe_ativo, porcentagem, dividendo_desejado)
            flash('Alocação atualizada com sucesso!', 'success')

    if request.method == 'GET':
        return render_template_alocacoes(user_id)

    return redirect(url_for('carteira_ideal'))

def editar_alocacao(session, request):
    user_id = session.get('user_id')
    if not user_id:
        flash('Usuário não autenticado', 'danger')
        return redirect(url_for('login'))

    classe_ativo = request.form.get('classe_ativo')
    porcentagem = float(request.form.get('porcentagem', 0))
    dividendo_desejado = request.form.get('dividendo_desejado')

    soma_atual, nova_soma = calcula_nova_soma(user_id, classe_ativo, porcentagem)

    if nova_soma > 100:
        flash('A soma das porcentagens não pode ultrapassar 100%', 'danger')
    else:
        repo.atualiza_porcentagem_classe_ativo(porcentagem, user_id, classe_ativo, dividendo_desejado)
        flash('Alocação atualizada com sucesso!', 'success')
    
    return redirect(url_for('carteira_ideal'))

def excluir_alocacao(session, request):
    user_id = session.get('user_id')
    classe_ativo = request.form.get('classe_ativo')

    repo.excluir_porcentagem_classe_ativo(user_id, classe_ativo)
    flash('Alocação excluída com sucesso!', 'success')
    
    return redirect(url_for('carteira_ideal'))

def cadastrar_ativos(classe_ativo, session, request):
    user_id = session.get('user_id')
    if not user_id:
        flash('Usuário não autenticado', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome_ativo = request.form.get('nome_ativo')
        nota_ativo = request.form.get('nota_ativo', type=float)
        
        repo.inclui_ativo(user_id, classe_ativo, nome_ativo, nota_ativo)
        flash('Ativo cadastrado com sucesso!', 'success')
        return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))
    
    return render_template_ativos(user_id, classe_ativo)

def editar_ativo(session, request):
    user_id = session.get('user_id')
    classe_ativo = request.form.get('classe_ativo')
    ativo = request.form.get('nome_ativo')
    nota = float(request.form.get('nota_ativo', 0))

    repo.editar_ativo(user_id, ativo, nota)
    flash('Ativo atualizado com sucesso!', 'success')
    return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))

def excluir_ativo(session, request):
    user_id = session.get('user_id')
    classe_ativo = request.form.get('classe_ativo')
    ativo = request.form.get('nome_ativo')

    repo.remove_ativo(user_id, ativo)
    flash('Ativo excluído com sucesso!', 'success')
    return redirect(url_for('cadastrar_ativos', classe_ativo=classe_ativo))

def calcula_nova_soma(user_id, classe_ativo, porcentagem):
    soma_atual = repo.consulta_soma_porcentagem(user_id)
    porcentagem_existente = repo.consulta_porcentagem(user_id, classe_ativo)
    nova_soma = soma_atual - (porcentagem_existente[0] if porcentagem_existente else 0) + porcentagem
    return soma_atual, nova_soma

def atualizar_ou_incluir_alocacao(user_id, classe_ativo, porcentagem, dividendo_desejado):
    if repo.consulta_porcentagem(user_id, classe_ativo):
        repo.atualiza_porcentagem_classe_ativo(porcentagem, user_id, classe_ativo, dividendo_desejado)
    else:
        repo.inclui_porcentagem_classe_ativo(user_id, classe_ativo, porcentagem)

def render_template_alocacoes(user_id):
    alocacoes = repo.consulta_alocacao_carteira_ideal(user_id)
    soma_total = repo.consulta_soma_porcentagem(user_id)
    alocacoes_json = {alocacao[0]: alocacao[1] for alocacao in alocacoes if alocacao[1] > 0}
    return render_template('carteira_ideal.html', alocacoes=alocacoes, soma_total=soma_total, alocacoes_json=alocacoes_json)

def render_template_ativos(user_id, classe_ativo):
    ativos_consulta = repo.listar_ativos(user_id, classe_ativo)
    porcentagem_total = repo.consulta_soma_porcentagem(user_id)
    soma_notas = sum(float(ativo[1]) for ativo in ativos_consulta)
    
    ativos = [
        (
            ativo[0],
            float(ativo[1]),
            round((float(ativo[1]) / soma_notas) * 100 if soma_notas > 0 else 0, 2),
            round((float(ativo[1]) / porcentagem_total) * 100 if porcentagem_total > 0 else 0, 2)
        ) for ativo in ativos_consulta
    ]

    return render_template('cadastrar_ativos.html', classe_ativo=classe_ativo, ativos=ativos, soma_notas=soma_notas)
