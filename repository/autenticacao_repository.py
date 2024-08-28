import repository.db_repository as db_repository

def consulta_usuario(email, senha):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT * FROM users WHERE email = ? AND senha = ?', (email, senha))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def existe_email(email):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
    resultados = cursor.fetchall()
    conn.close()
    return len(resultados)

def cadastrar_usuario(nome, cpf, email, senha):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('INSERT INTO users (nome, cpf, email, senha) VALUES (?, ?, ?, ?)', (nome, cpf, email, senha))
    conn.commit()
    conn.close()

def consulta_email(email):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT email FROM users WHERE email = ?', (email,))
    email = cursor.fetchone()
    conn.close()
    return email