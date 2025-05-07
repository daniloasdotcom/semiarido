import sqlite3

def conectar():
    return sqlite3.connect('xerofilas.db')

def criar_tabela():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS plantas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cientifico TEXT,
            nome_popular TEXT,
            origem TEXT,
            uso TEXT,
            caracteristicas_adaptativas TEXT,
            observacoes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_receitas():
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS receitas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            planta_id INTEGER,
            titulo TEXT,
            descricao TEXT,
            FOREIGN KEY (planta_id) REFERENCES plantas (id)
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_planta(nome_cientifico, nome_popular, origem, uso, caracteristicas, observacoes):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        INSERT INTO plantas (nome_cientifico, nome_popular, origem, uso, caracteristicas_adaptativas, observacoes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nome_cientifico, nome_popular, origem, uso, caracteristicas, observacoes))
    conn.commit()
    conn.close()

def listar_plantas():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM plantas')
    dados = c.fetchall()
    conn.close()
    return dados

def buscar_por_nome(nome):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM plantas WHERE nome_popular LIKE ?", ('%' + nome + '%',))
    dados = c.fetchall()
    conn.close()
    return dados

def atualizar_planta(id, nome_cientifico, nome_popular, origem, uso, caracteristicas, observacoes):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        UPDATE plantas
        SET nome_cientifico = ?, nome_popular = ?, origem = ?, uso = ?, caracteristicas_adaptativas = ?, observacoes = ?
        WHERE id = ?
    ''', (nome_cientifico, nome_popular, origem, uso, caracteristicas, observacoes, id))
    conn.commit()
    conn.close()

def adicionar_receita(planta_id, titulo, descricao):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        INSERT INTO receitas (planta_id, titulo, descricao)
        VALUES (?, ?, ?)
    ''', (planta_id, titulo, descricao))
    conn.commit()
    conn.close()

def listar_receitas(planta_id):
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT id, titulo, descricao FROM receitas WHERE planta_id = ?', (planta_id,))
    receitas = c.fetchall()
    conn.close()
    return receitas

def atualizar_receita(receita_id, novo_titulo, nova_descricao):
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        UPDATE receitas
        SET titulo = ?, descricao = ?
        WHERE id = ?
    ''', (novo_titulo, nova_descricao, receita_id))
    conn.commit()
    conn.close()

def deletar_planta(planta_id):
    conn = conectar()
    c = conn.cursor()
    c.execute('DELETE FROM receitas WHERE planta_id = ?', (planta_id,))
    c.execute('DELETE FROM plantas WHERE id = ?', (planta_id,))
    conn.commit()
    conn.close()

def deletar_receita(receita_id):
    conn = conectar()
    c = conn.cursor()
    c.execute('DELETE FROM receitas WHERE id = ?', (receita_id,))
    conn.commit()
    conn.close()