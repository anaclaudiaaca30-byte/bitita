from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()


# ================= BANCO =================

def conectar():
    return sqlite3.connect("escola.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS estudantes
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       nome
                       TEXT,
                       nacionalidade
                       TEXT,
                       geracao
                       TEXT,
                       acolhimento
                       TEXT
                   )
                   """)

    conn.commit()
    conn.close()


criar_tabela()


# ================= MODELO =================

class Estudante(BaseModel):
    nome: str
    nacionalidade: str
    geracao: str
    acolhimento: str


# ================= ROTAS =================

@app.get("/")
def home():
    return {"mensagem": "API Escolar Rodando"}


@app.post("/estudantes/")
def criar(estudante: Estudante):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
                   INSERT INTO estudantes (nome, nacionalidade, geracao, acolhimento)
                   VALUES (?, ?, ?, ?)
                   """, (estudante.nome, estudante.nacionalidade,
                         estudante.geracao, estudante.acolhimento))

    conn.commit()
    conn.close()

    return {"status": "ok"}


@app.get("/estudantes/")
def listar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM estudantes")
    dados = cursor.fetchall()

    conn.close()
    return dados
