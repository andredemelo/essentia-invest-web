from flask import Flask, render_template, request, session

from apscheduler.schedulers.background import BackgroundScheduler

import service.db_service as db_service
import service.atualiza_preco_ativos_service as atualiza_preco_ativos_service
import service.autenticaccao_service as autenticacao_service
import service.carteira_ideal_service as carteira_ideal_service
import service.balanceamento_carteira_service as balanceamento_carteira_service
import service.transacao_service as transacao_service
import service.dividendos_service as dividendos_service
import service.pergunta_service as pergunta_service

app = Flask(__name__)
app.secret_key = 'EssentiaInvest'
DIRETORIO_UPLOAD = 'uploads'
app.config['UPLOAD_FOLDER'] = DIRETORIO_UPLOAD

def init_db():
    print('Iniciando Criação de Tabelas!')
    db_service.inicializa_tabelas()
    print('Finalizando Criação de Tabelas!')

def scheduler_atualiza_preco_atual():
    atualiza_preco_ativos_service.atualiza_preco_atual()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return autenticacao_service.efetuar_login(request)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    return autenticacao_service.cadastra_usuario(request)

@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    return autenticacao_service.recuperacao_senha(request)

@app.route('/dashboard')
@autenticacao_service.login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/carteira_ideal', methods=['GET', 'POST'])
@autenticacao_service.login_required
def carteira_ideal():
    return carteira_ideal_service.consulta_carteira_ideal(session, request)

@app.route('/editar_alocacao', methods=['POST'])
@autenticacao_service.login_required
def editar_alocacao():
    return carteira_ideal_service.editar_alocacao(session, request)

@app.route('/excluir_alocacao', methods=['POST'])
@autenticacao_service.login_required
def excluir_alocacao():
    return carteira_ideal_service.excluir_alocacao(session, request)

@app.route('/carteira_ideal/cadastrar_ativos/<classe_ativo>', methods=['GET', 'POST'])
@autenticacao_service.login_required
def cadastrar_ativos(classe_ativo):
    return carteira_ideal_service.cadastrar_ativos(classe_ativo, session, request)

@app.route('/editar_ativo', methods=['POST'])
@autenticacao_service.login_required
def editar_ativo():
    return carteira_ideal_service.editar_ativo(session, request)

@app.route('/excluir_ativo', methods=['POST'])
@autenticacao_service.login_required
def excluir_ativo():
    return carteira_ideal_service.excluir_ativo(session, request)

@app.route('/carteira_ideal/pergunta/<classe_ativo>', methods=['GET', 'POST'])
@autenticacao_service.login_required
def pergunta(classe_ativo):
    return pergunta_service.cadastrar_pergunta(classe_ativo, session, request)

@app.route('/cadastrar_pergunta/<classe_ativo>', methods=['POST'])
@autenticacao_service.login_required
def cadastrar_pergunta(classe_ativo):
    return pergunta_service.cadastrar_pergunta(classe_ativo, session, request)

@app.route('/editar_pergunta/<id>/<classe_ativo>', methods=['POST'])
@autenticacao_service.login_required
def editar_pergunta(id, classe_ativo):
    return pergunta_service.editar_pergunta(request, id, classe_ativo)

@app.route('/excluir_pergunta/<id>/<classe_ativo>', methods=['POST'])
@autenticacao_service.login_required
def excluir_pergunta(id, classe_ativo):
    return pergunta_service.excluir_pergunta(id, classe_ativo)

@app.route('/balanceamento_carteira', methods=['GET', 'POST'])
@autenticacao_service.login_required
def balanceamento_carteira():
    return balanceamento_carteira_service.consulta_balanceamento_carteira(session)

@app.route('/upload_transacoes', methods=['GET', 'POST'])
@autenticacao_service.login_required
def upload_transacoes():
    return transacao_service.upload_transacoes(request)

@app.route('/transacoes')
@autenticacao_service.login_required
def transacoes():
    return transacao_service.lista_transacoes()

@app.route('/upload_dividendos', methods=['GET', 'POST'])
@autenticacao_service.login_required
def upload_dividendos():
    return dividendos_service.upload_dividendos(request)

@app.route('/dividendos')
@autenticacao_service.login_required
def dividendos():
    return dividendos_service.consulta_dividendos()

@app.route('/logout')
def logout():
    return autenticacao_service.efetua_logout()

if __name__ == '__main__':
    init_db()
    
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduler_atualiza_preco_atual, 'cron', hour=12, minute=7)
    scheduler.start()

    app.run(debug=True)
