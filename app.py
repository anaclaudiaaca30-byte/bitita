import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from openpyxl import Workbook
import matplotlib.pyplot as plt

# ================= BANCO =================

conn = sqlite3.connect("estudantes.db")
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

# ================= CORES =================

cor_fundo = "#0f3fa8"
cor_frame = "#0b2f7a"
cor_botao = "#2563eb"
cor_menu = "#082567"
cor_menu_botao = "#0b3ea8"
cor_vermelho = "#ef4444"
cor_verde = "#10b981"

id_selecionado = None

# ================= FUNÇÕES =================

def limpar_campos():
    global id_selecionado

    entry_nome.delete(0, tk.END)
    entry_nacionalidade.delete(0, tk.END)
    combo_geracao.set("")
    combo_acolhimento.set("")

    id_selecionado = None


def salvar():
    nome = entry_nome.get()
    nacionalidade = entry_nacionalidade.get()
    geracao = combo_geracao.get()
    acolhimento = combo_acolhimento.get()

    if nome == "":
        messagebox.showwarning("Aviso", "Digite o nome")
        return

    cursor.execute("""
    INSERT INTO estudantes(nome, nacionalidade, geracao, acolhimento)
    VALUES (?, ?, ?, ?)
    """, (nome, nacionalidade, geracao, acolhimento))

    conn.commit()

    atualizar_lista()
    limpar_campos()

    messagebox.showinfo("Sucesso", "Aluno cadastrado!")


def atualizar_lista():
    lista.delete(*lista.get_children())

    cursor.execute("SELECT * FROM estudantes")
    dados = cursor.fetchall()

    for item in dados:
        lista.insert("", tk.END, values=item)


def excluir():
    item = lista.selection()

    if not item:
        return

    dados = lista.item(item)["values"]
    aluno_id = dados[0]

    cursor.execute("DELETE FROM estudantes WHERE id=?", (aluno_id,))
    conn.commit()

    atualizar_lista()

    messagebox.showinfo("Sucesso", "Aluno excluído!")


def buscar():
    termo = entry_busca.get()

    lista.delete(*lista.get_children())

    cursor.execute("""
    SELECT * FROM estudantes
    WHERE nome LIKE ?
    """, ('%' + termo + '%',))

    dados = cursor.fetchall()

    for item in dados:
        lista.insert("", tk.END, values=item)


def grafico():
    cursor.execute("""
    SELECT nacionalidade, COUNT(*)
    FROM estudantes
    GROUP BY nacionalidade
    """)

    dados = cursor.fetchall()

    if not dados:
        messagebox.showwarning("Aviso", "Não há dados")
        return

    nomes = [d[0] for d in dados]
    valores = [d[1] for d in dados]

    cores = [
        "#2563EB",
        "#10B981",
        "#F59E0B",
        "#EF4444",
        "#8B5CF6",
        "#06B6D4",
        "#EC4899",
        "#84CC16"
    ]

    plt.figure(figsize=(8,8))

    plt.pie(
        valores,
        labels=nomes,
        autopct='%1.1f%%',
        startangle=90,
        colors=cores[:len(nomes)]
    )

    plt.title("Porcentagem por Nacionalidade")

    plt.show()


def exportar_excel():
    wb = Workbook()
    ws = wb.active

    ws.title = "Estudantes"

    ws.append([
        "ID",
        "Nome",
        "Nacionalidade",
        "Geração",
        "Acolhimento"
    ])

    cursor.execute("SELECT * FROM estudantes")

    dados = cursor.fetchall()

    for item in dados:
        ws.append(item)

    wb.save("relatorio_estudantes.xlsx")

    messagebox.showinfo("Sucesso", "Excel gerado!")


# ================= CADASTRO =================

def abrir_cadastro():
    global entry_nome
    global entry_nacionalidade
    global combo_geracao
    global combo_acolhimento
    global lista
    global entry_busca

    janela = tk.Toplevel()

    janela.title("Cadastro de Estudantes")
    janela.geometry("900x600")
    janela.configure(bg=cor_fundo)

    titulo = tk.Label(
        janela,
        text="Cadastro de Estudantes",
        font=("Arial", 20, "bold"),
        bg=cor_fundo,
        fg="white"
    )

    titulo.pack(pady=15)

    frame_form = tk.Frame(
        janela,
        bg=cor_frame,
        bd=2,
        relief="ridge"
    )

    frame_form.pack(
        padx=20,
        pady=10,
        fill="x"
    )

    # Nome
    tk.Label(
        frame_form,
        text="Nome:",
        bg=cor_frame,
        fg="white"
    ).grid(row=0, column=0, padx=10, pady=10)

    entry_nome = tk.Entry(frame_form, width=30)
    entry_nome.grid(row=0, column=1)

    # Nacionalidade
    tk.Label(
        frame_form,
        text="Nacionalidade:",
        bg=cor_frame,
        fg="white"
    ).grid(row=1, column=0, padx=10, pady=10)

    entry_nacionalidade = tk.Entry(frame_form, width=30)
    entry_nacionalidade.grid(row=1, column=1)

    # Geração
    tk.Label(
        frame_form,
        text="Geração:",
        bg=cor_frame,
        fg="white"
    ).grid(row=2, column=0, padx=10, pady=10)

    combo_geracao = ttk.Combobox(
        frame_form,
        values=["1ª geração", "2ª geração"]
    )

    combo_geracao.grid(row=2, column=1)

    # Acolhimento
    tk.Label(
        frame_form,
        text="Acolhimento:",
        bg=cor_frame,
        fg="white"
    ).grid(row=3, column=0, padx=10, pady=10)

    combo_acolhimento = ttk.Combobox(
        frame_form,
        values=["Sim", "Não"]
    )

    combo_acolhimento.grid(row=3, column=1)

    # Botões
    frame_botoes = tk.Frame(
        janela,
        bg=cor_fundo
    )

    frame_botoes.pack(pady=10)

    tk.Button(
        frame_botoes,
        text="Salvar",
        bg=cor_verde,
        fg="white",
        width=15,
        command=salvar
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        frame_botoes,
        text="Excluir",
        bg=cor_vermelho,
        fg="white",
        width=15,
        command=excluir
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        frame_botoes,
        text="Excel",
        bg=cor_botao,
        fg="white",
        width=15,
        command=exportar_excel
    ).grid(row=0, column=2, padx=10)

    # Busca
    frame_busca = tk.Frame(
        janela,
        bg=cor_fundo
    )

    frame_busca.pack(pady=10)

    tk.Label(
        frame_busca,
        text="Buscar:",
        bg=cor_fundo,
        fg="white"
    ).pack(side=tk.LEFT)

    entry_busca = tk.Entry(frame_busca)
    entry_busca.pack(side=tk.LEFT, padx=5)

    entry_busca.bind(
        "<KeyRelease>",
        lambda e: buscar()
    )

    # Lista
    frame_lista = tk.Frame(janela)
    frame_lista.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    lista = ttk.Treeview(
        frame_lista,
        columns=(
            "ID",
            "Nome",
            "Nacionalidade",
            "Geração",
            "Acolhimento"
        ),
        show="headings"
    )

    for col in lista["columns"]:
        lista.heading(col, text=col)

    lista.pack(fill="both", expand=True)

    atualizar_lista()


# ================= MENU =================

root = tk.Tk()

root.title("Sistema Escolar Bitita")
root.geometry("950x600")
root.configure(bg=cor_fundo)

menu_lateral = tk.Frame(
    root,
    bg=cor_menu,
    width=220
)

menu_lateral.pack(
    side="left",
    fill="y"
)

logo = tk.Label(
    menu_lateral,
    text="BITITA",
    bg=cor_menu,
    fg="white",
    font=("Arial", 24, "bold")
)

logo.pack(pady=30)

subtitulo = tk.Label(
    menu_lateral,
    text="Sistema Escolar",
    bg=cor_menu,
    fg="#dbeafe",
    font=("Arial", 10)
)

subtitulo.pack(pady=5)

area_principal = tk.Frame(
    root,
    bg=cor_fundo
)

area_principal.pack(
    side="right",
    expand=True,
    fill="both"
)

titulo = tk.Label(
    area_principal,
    text="Painel Principal",
    bg=cor_fundo,
    fg="white",
    font=("Arial", 26, "bold")
)

titulo.pack(pady=40)


def botao_menu(texto, comando):
    tk.Button(
        menu_lateral,
        text=texto,
        command=comando,
        bg=cor_menu_botao,
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        width=18,
        height=2
    ).pack(pady=12)


botao_menu("📚 Alunos", abrir_cadastro)
botao_menu("📊 Gráfico", grafico)
botao_menu("📥 Excel", exportar_excel)
botao_menu("❌ Sair", root.destroy)

mensagem = tk.Label(
    area_principal,
    text="Bem-vinda ao Sistema Escolar Bitita",
    bg=cor_fundo,
    fg="#dbeafe",
    font=("Arial", 16)
)

mensagem.pack(pady=20)

root.mainloop()