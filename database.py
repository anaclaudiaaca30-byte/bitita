import sqlite3


# ================= CONEXÃO =================
def conectar():
    return sqlite3.connect("estudantes.db")


# ================= CRIAR TABELA =================
def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        nacionalidade TEXT,
        geracao TEXT,
        acolhimento TEXT
    )
    """)

    conn.commit()
    conn.close()


# ================= INSERIR =================
def inserir(nome, nacionalidade, geracao, acolhimento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO estudantes (nome, nacionalidade, geracao, acolhimento)
    VALUES (?, ?, ?, ?)
    """, (nome, nacionalidade, geracao, acolhimento))

    conn.commit()
    conn.close()


# ================= LISTAR =================
def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudantes")
    dados = cursor.fetchall()

    conn.close()
    return dados


# ================= BUSCAR =================
def buscar(nome):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudantes WHERE nome LIKE ?", ('%' + nome + '%',))
    dados = cursor.fetchall()

    conn.close()
    return dados


# ================= ATUALIZAR =================
def atualizar(id, nome, nacionalidade, geracao, acolhimento):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE estudantes 
    SET nome=?, nacionalidade=?, geracao=?, acolhimento=?
    WHERE id=?
    """, (nome, nacionalidade, geracao, acolhimento, id))

    conn.commit()
    conn.close()


# ================= EXCLUIR =================
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM estudantes WHERE id = ?", (id,))
    conn.commit()
    conn.close()


# ================= GRÁFICO =================
def contar_por_nacionalidade():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nacionalidade, COUNT(*)
    FROM estudantes
    GROUP BY nacionalidade
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados