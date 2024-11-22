import repository.db_repository as db_repository

def consulta_data_preco_historico(classe, ticker, data):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT data FROM historico_preco_ativo_carteira_ideal WHERE classe_ativo = ? AND nome_ativo = ? AND data =?', (classe, ticker, data))
    result = cursor.fetchone() 
    if result:
        data_historico = result[0]
    else:
        data_historico = None
    return data_historico

def inclui_historico_preco(classe, ticker, data, preco):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('INSERT INTO historico_preco_ativo_carteira_ideal (classe_ativo, nome_ativo, data, preco) VALUES (?, ?, ?, ?)', (classe, ticker, data, preco))
    conn.commit()
    conn.close()
