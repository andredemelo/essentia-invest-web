import repository.db_repository as db_repository

def inclui_pergunta(user_id, classe_ativo, identificador, texto_pergunta):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('INSERT INTO pergunta_avaliacao (user_id, classe_ativo, identificador, texto_pergunta) VALUES (?, ?, ?, ?)', (user_id, classe_ativo, identificador, texto_pergunta))
    conn.commit()
    conn.close()

def listar_perguntas(user_id, classe_ativo):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT * FROM pergunta_avaliacao WHERE user_id = ? AND classe_ativo = ?', (user_id, classe_ativo))
    perguntas = cursor.fetchall()
    conn.close()
    return perguntas

def update_pergunta(id, identificador, texto_pergunta):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('UPDATE pergunta_avaliacao SET identificador = ?, texto_pergunta = ? WHERE id = ?', (identificador, texto_pergunta, id))
    conn.commit()
    conn.close()

def delete_pergunta(id):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('DELETE FROM pergunta_avaliacao WHERE id = ?', (id,))
    conn.commit()
    conn.close()