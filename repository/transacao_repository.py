import repository.db_repository as db_repository

def consulta_transacoes_ativo(user_id, ticket):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT operacao, quantidade, preco_unitario FROM  transacao WHERE user_id = ? AND  codigo_ativo = ?', (user_id, ticket))
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

def consulta_transacoes(user_id, row):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('''
                   SELECT * FROM transacao 
                   WHERE user_id = ? AND data_operacao = ? AND categoria = ? AND codigo_ativo = ? AND operacao = ? AND quantidade =? AND preco_unitario = ? AND corretora = ?
                    ''', (user_id, row['Data operação'], row['Categoria'], row['Código Ativo'], row['Operação C/V/B'], row['Quantidade'], row['Preço unitário'], row['Corretora']))
    transacao = cursor.fetchone()
    conn.close()
    return transacao

def inserir_transacao(user_id, row):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('''
                INSERT INTO transacao (user_id, data_operacao, categoria, codigo_ativo, operacao, quantidade, preco_unitario, corretora, corretagem, taxas, impostos, irrf)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                row['Data operação'],
                row['Categoria'],
                row['Código Ativo'],
                row['Operação C/V/B'],
                row['Quantidade'],
                row['Preço unitário'],
                row['Corretora'],
                row['Corretagem'],
                row['Taxas'],
                row['Impostos'],
                row['IRRF']
            ))
    conn.commit()
    conn.close()

def listar_todas_transacoes():
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT * FROM transacao ORDER BY codigo_ativo ASC, date(data_operacao) ASC')
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes