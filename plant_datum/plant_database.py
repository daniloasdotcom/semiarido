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