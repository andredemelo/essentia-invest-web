import sqlite3

def inicializa_conexao_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor 

def cria_tabelas():
    conn, cursor = inicializa_conexao_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carteira_ideal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            classe_ativo TEXT NOT NULL,
            porcentagem REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos_carteira_ideal (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            classe_ativo TEXT NOT NULL,
            nome_ativo TEXT NOT NULL,
            nota_ativo REAL NOT NULL,
            preco_atual REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            data_operacao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            codigo_ativo TEXT NOT NULL,
            operacao TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            corretora TEXT NOT NULL,
            corretagem REAL NOT NULL,
            taxas REAL NOT NULL,
            impostos REAL NOT NULL,
            irrf REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dividendo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            codigo_ativo TEXT NOT NULL,
            corretora TEXT NOT NULL,
            tipo TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL,
            valor_total REAL NOT NULL,
            valor_total_liquido REAL NOT NULL,
            data_com TEXT NOT NULL,
            data_pagamento TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pergunta_avaliacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            classe_ativo TEXT NOT NULL,
            identificador TEXT NOT NULL,
            texto_pergunta TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user(id)
        )
    ''')
    conn.commit()
    conn.close()