import sqlite3

conn = sqlite3.connect("xerofilas.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE plantas ADD COLUMN plantio_manejo TEXT;")
except sqlite3.OperationalError:
    print("Coluna 'plantio_manejo' já existe.")

try:
    c.execute("ALTER TABLE plantas ADD COLUMN aplicacoes_agroflorestais TEXT;")
except sqlite3.OperationalError:
    print("Coluna 'aplicacoes_agroflorestais' já existe.")

conn.commit()
conn.close()

print("✅ Atualização concluída.")