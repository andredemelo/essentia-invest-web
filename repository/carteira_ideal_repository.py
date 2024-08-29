import repository.db_repository as db_repository

def consulta_soma_porcentagem(user_id):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT SUM(porcentagem) FROM carteira_ideal WHERE user_id = ?', (user_id,))
    soma_atual = cursor.fetchone()[0] or 0.0
    conn.close()
    return soma_atual

def consulta_porcentagem(user_id, classe_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT porcentagem FROM carteira_ideal WHERE user_id = ? AND classe_ativo = ?', (user_id, classe_ativo))
    porcentagem_existente = cursor.fetchone()
    conn.close()
    return porcentagem_existente

def inclui_porcentagem_classe_ativo(user_id, classe_ativo, porcentagem):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('INSERT INTO carteira_ideal (user_id, classe_ativo, porcentagem) VALUES (?, ?, ?)', (user_id, classe_ativo, porcentagem))
    conn.commit()
    conn.close()

def atualiza_porcentagem_classe_ativo(porcentagem, user_id, classe_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('UPDATE carteira_ideal SET porcentagem = ? WHERE user_id = ? AND classe_ativo = ?', (porcentagem, user_id, classe_ativo))
    conn.commit()
    conn.close()

def consulta_alocacao_carteira_ideal(user_id):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT classe_ativo, porcentagem FROM carteira_ideal WHERE user_id = ?', (user_id,))
    alocacoes = cursor.fetchall()
    conn.close()
    return alocacoes

def excluir_porcentagem_classe_ativo(user_id, classe_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('DELETE FROM carteira_ideal WHERE user_id = ? AND classe_ativo = ?', (user_id, classe_ativo))
    conn.commit()
    conn.close()

def inclui_ativo(user_id, classe_ativo, nome_ativo, nota_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('INSERT INTO ativos_carteira_ideal (user_id, classe_ativo, nome_ativo, nota_ativo)  VALUES (?, ?, ?, ?)', (user_id, classe_ativo, nome_ativo, nota_ativo))
    conn.commit()
    conn.close()

def listar_ativos(user_id, classe_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT nome_ativo, nota_ativo FROM ativos_carteira_ideal WHERE user_id = ? AND classe_ativo = ?', (user_id, classe_ativo))
    ativos = cursor.fetchall()
    conn.close()
    return ativos

def editar_ativo(user_id, ativo, nota):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('UPDATE ativos_carteira_ideal SET nota_ativo = ? WHERE nome_ativo = ? AND user_id = ?', (nota, ativo, user_id))
    conn.commit()
    conn.close()

def remove_ativo(user_id, ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('DELETE FROM ativos_carteira_ideal WHERE user_id = ? AND nome_ativo = ?', (user_id, ativo))
    conn.commit()
    conn.close()

def consulta_ativos_carteira(user_id):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT classe_ativo, nome_ativo, nota_ativo, preco_atual FROM ativos_carteira_ideal WHERE user_id = ?', (user_id,))
    ativos = cursor.fetchall()
    conn.close()
    return ativos

def consulta_preco_atual_ativo():
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT classe_ativo, nome_ativo FROM ativos_carteira_ideal')
    ativos = cursor.fetchall()
    conn.close()
    return ativos

def atualiza_preco_atual_ativo(classe, ticker, preco):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('UPDATE ativos_carteira_ideal SET preco_atual = ? WHERE nome_ativo = ? AND classe_ativo = ?', (preco, ticker, classe))
    conn.commit()
    conn.close()
