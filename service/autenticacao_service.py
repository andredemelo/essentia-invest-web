from functools import wraps
from flask import render_template, redirect, url_for, flash, session

import repository.autenticacao_repository as autenticacao_repository

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def efetuar_login(request):
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        usuario = autenticacao_repository.consulta_usuario(email, senha)
        if usuario:
            session['logged_in'] = True
            session['user_id'] = usuario[0]
            session['user_name'] = usuario[1]
            return redirect(url_for('dashboard'))
        else:
            flash('E-mail ou senha incorretos', 'danger')
    return render_template('login.html')

def cadastra_usuario(request):
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmarSenha']
        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'danger')
            return redirect(url_for('cadastro'))
        if autenticacao_repository.existe_email(email) == 0:
            autenticacao_repository.cadastrar_usuario(nome, cpf, email, senha)
            flash('Cadastro realizado com sucesso!', 'success')
        else:
            flash('E-mail já cadastrado!', 'danger')
            return redirect(url_for('login'))
    return render_template('cadastro.html')

def recuperacao_senha(request):
    if request.method == 'POST':
        email = request.form['email']
        email_envio = autenticacao_repository.consulta_email(email)
        if email_envio:
            flash('Um e-mail de recuperação foi enviado para você.', 'success')
        else:
            flash('E-mail não encontrado', 'danger')
    return render_template('esqueci_senha.html')

def efetua_logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('login'))