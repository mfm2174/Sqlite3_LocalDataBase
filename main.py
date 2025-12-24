from google.colab import drive
import sqlite3, pandas as pd, os

drive.mount('/content/drive', force_remount=True)

db_path = "/content/drive/MyDrive/Colab Notebooks/.../loja1.db"

# (Re)cria do zero para garantir consistência
if os.path.exists(db_path):
    os.remove(db_path)

conn = sqlite3.connect(db_path)
cur  = conn.cursor()

# ---------- Schema ----------
cur.executescript("""
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS livros;

CREATE TABLE clientes (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  nome      TEXT NOT NULL,
  email     TEXT UNIQUE
);

CREATE TABLE livros (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  nome      TEXT NOT NULL,
  genero    TEXT NOT NULL,
  preco     REAL NOT NULL,
  estoque   INTEGER NOT NULL
);
""")

# ---------- Dados de Clientes ----------
cur.executemany("INSERT INTO clientes (nome, email) VALUES (?,?)", [
  ("Ana Lima",     "ana@gmail.com"),
  ("Bruno Souza",  "bruno@yahoo.com"),
  ("Carla Dias",   "carla@gmail.com"),
  ("Diego Rocha",  "diego@hotmail.com"),
  ("Eva Santos",   "eva@gmail.com"),
  ("Fabio Nunes",  "fabio@outlook.com"),
  ("Gabi Alves",   "gabi@yahoo.com"),
  ("Helena Araújo","helena@gmail.com"),
  ("Igor Teles",   "igor@uol.com.br"),
  ("Joana Prado",  "joana@gmail.com"),
])

cur.executemany("INSERT INTO livros (nome, genero, preco, estoque) VALUES (?,?,?,?)", [
  ("Rir é o Melhor Remédio", "comédia",          39.90, 12),
  ("Amor em Tempos Difíceis", "romance",          59.00,  7),
  ("Noite Sem Fim",           "terror",           44.50,  5),
  ("O Enigma do Trem",        "suspense",         49.90,  9),
  ("Lágrimas do Norte",       "drama",            34.90,  8),
  ("Estrelas e Circuitos",    "ciência ficção",   69.00,  3),
  ("Pão Quentinho",           "padaria",          29.90, 20),
  ("Risos Garantidos",        "comédia",          35.00, 10),
  ("Corações ao Vento",       "romance",          55.00,  6),
  ("Sombras no Porão",        "terror",           42.00,  4),
])

conn.commit()

# ---------- KPIs CLIENTES ----------
kpi_clientes = pd.read_sql_query("""
SELECT
  (SELECT COUNT(*) FROM clientes)                    AS total_clientes,
  (SELECT COUNT(DISTINCT email) FROM clientes)       AS emails_unicos,
  (SELECT ROUND(AVG(LENGTH(nome)),2) FROM clientes)  AS media_tam_nome
""", conn)

dominios = pd.read_sql_query("""
SELECT
  LOWER(SUBSTR(email, INSTR(email,'@')+1)) AS dominio,
  COUNT(*) AS qtd
FROM clientes
GROUP BY dominio
ORDER BY qtd DESC, dominio;
""", conn)

print("=== KPIs: CLIENTES ===")
display(kpi_clientes)
print("Domínios de e-mail (frequência):")
display(dominios)

# ---------- KPIs LIVROS ----------
kpi_livros = pd.read_sql_query("""
SELECT
  COUNT(*)                              AS total_titulos,
  ROUND(AVG(preco),2)                   AS preco_medio,
  SUM(estoque)                          AS estoque_total
FROM livros;
""", conn)

por_genero = pd.read_sql_query("""
SELECT
  genero,
  COUNT(*)                AS qtd_titulos,
  ROUND(AVG(preco),2)     AS preco_medio,
  SUM(estoque)            AS estoque_total
FROM livros
GROUP BY genero
ORDER BY qtd_titulos DESC, genero;
""", conn)

print("=== KPIs: LIVROS ===")
display(kpi_livros)
print("Por gênero:")
display(por_genero)

conn.close()
