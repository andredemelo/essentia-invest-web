from functools import wraps
from flask import render_template, redirect, url_for, flash, session, request
import repository.autenticacao_repository as autenticacao_repository

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def efetuar_login(request):
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('password')
        
        usuario = autenticacao_repository.consulta_usuario(email, senha)
        if usuario:
            session.update({
                'logged_in': True,
                'user_id': usuario[0],
                'user_name': usuario[1]
            })
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        
        flash('E-mail ou senha incorretos', 'danger')
    
    return render_template('login.html')

def cadastra_usuario(request):
    if request.method == 'POST':
        nome = request.form.get('nome')
        cpf = request.form.get('cpf')
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirmar_senha = request.form.get('confirmarSenha')
        
        if senha != confirmar_senha:
            flash('As senhas não coincidem', 'danger')
            return redirect(url_for('cadastro'))

        if autenticacao_repository.existe_email(email) == 0:
            autenticacao_repository.cadastrar_usuario(nome, cpf, email, senha)
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        
        flash('E-mail já cadastrado!', 'danger')
        return redirect(url_for('cadastro'))
    
    return render_template('cadastro.html')

def recuperacao_senha(request):
    if request.method == 'POST':
        email = request.form.get('email')
        if autenticacao_repository.consulta_email(email):
            flash('Um e-mail de recuperação foi enviado para você.', 'success')
        else:
            flash('E-mail não encontrado', 'danger')
    
    return render_template('esqueci_senha.html')

def efetua_logout():
    session.clear()
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('login'))
