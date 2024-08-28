import repository.db_repository as db_repository

def consulta_dividendos(user_id, row):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('''
            SELECT * FROM dividendo 
            WHERE user_id = ? AND data_com = ? AND data_pagamento = ? AND categoria = ? AND codigo_ativo = ? AND tipo = ? AND corretora = ?
        ''', (user_id, row['Data com'], row['Pagamento'], row['CATEGORIA'], row['Ativo'], row['Tipo'], row['Corretora/banco']))
    dividendo = cursor.fetchall()
    conn.close()
    return dividendo

def incluir_dividendo(user_id, row):
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('''
                INSERT INTO dividendo (user_id, categoria, codigo_ativo, corretora, tipo, quantidade, valor , valor_total, valor_total_liquido, data_com, data_pagamento)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                row['CATEGORIA'],
                row['Ativo'],
                row['Corretora/banco'],
                row['Tipo'],
                row['Quantidade'],
                row['Valor'],
                row['Total'],
                row['Total líq.'],
                row['Data com'],
                row['Pagamento']
            ))
    conn.commit()
    conn.close()

def consulta_todos_dividendos():
    conn, cursor = db_repository.inicializa_conexao_db()
    cursor.execute('SELECT * FROM dividendo ORDER BY codigo_ativo, date(data_pagamento) ASC')
    devidendos = cursor.fetchall()
    conn.close()
    return devidendos