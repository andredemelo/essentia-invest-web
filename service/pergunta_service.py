from flask import render_template, redirect, url_for, flash, session, request
import repository.pergunta_repository as pergunta_repository

def cadastrar_pergunta(classe_ativo, session, request):
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        identificador = request.form.get('identificador')
        texto_pergunta = request.form.get('texto_pergunta')
        
        pergunta_repository.inclui_pergunta(user_id, classe_ativo, identificador, texto_pergunta)
        
        flash('Pergunta cadastrada com sucesso!', 'success')
        return redirect(url_for('pergunta', classe_ativo=classe_ativo))

    perguntas = pergunta_repository.listar_perguntas(user_id, classe_ativo)
    return render_template('cadastrar_pergunta.html', classe_ativo=classe_ativo, perguntas=perguntas)

def editar_pergunta(request, id, classe_ativo):
    if request.method == 'POST':
        identificador = request.form.get('identificador')
        texto_pergunta = request.form.get('texto_pergunta')
        
        pergunta_repository.update_pergunta(id, identificador, texto_pergunta)
        flash('Pergunta editada com sucesso!', 'success')
        
    return redirect(url_for('pergunta', classe_ativo=classe_ativo))

def excluir_pergunta(id, classe_ativo):
    pergunta_repository.delete_pergunta(id)
    flash('Pergunta excluída com sucesso!', 'success')
    
    return redirect(url_for('pergunta', classe_ativo=classe_ativo))
