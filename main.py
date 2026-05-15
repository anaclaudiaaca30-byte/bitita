import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

cursor.execute("""
CREATE TABLE IF NOT EXISTS alunos_estrangeiros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    diretoria TEXT,
    municipio TEXT,
    escola TEXT,
    pais TEXT,
    quantidade INTEGER
)
""")

conn.commit()

# ================= CORES =================

cor_fundo = "#0f2b7a"
cor_menu = "#0a1f5c"
cor_botao = "#2563eb"
cor_verde = "#10b981"
cor_laranja = "#f59e0b"
cor_vermelho = "#ef4444"

# ================= JANELA =================

root = tk.Tk()
root.title("Sistema Escolar Bitita")
root.geometry("1400x800")
root.configure(bg=cor_fundo)

frame_menu = tk.Frame(root, bg=cor_menu, width=220)
frame_menu.pack(side="left", fill="y")

frame_principal = tk.Frame(root, bg=cor_fundo)
frame_principal.pack(side="right", fill="both", expand=True)

titulo_menu = tk.Label(
    frame_menu,
    text="BITITA",
    font=("Arial", 26, "bold"),
    bg=cor_menu,
    fg="white"
)

titulo_menu.pack(pady=30)

# ================= CADASTRO =================

def abrir_alunos():

    janela = tk.Toplevel()
    janela.title("Cadastro de Estudantes")
    janela.geometry("1000x650")
    janela.configure(bg=cor_fundo)

    aluno_id = tk.StringVar()

    frame = tk.Frame(janela, bg="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(
        frame,
        text="Cadastro de Estudantes",
        font=("Arial", 18, "bold"),
        bg="white"
    ).grid(row=0, column=0, columnspan=5, pady=20)

    # CAMPOS

    tk.Label(frame, text="Nome:", bg="white").grid(row=1, column=0, padx=10, pady=10)

    entry_nome = tk.Entry(frame, width=35)
    entry_nome.grid(row=1, column=1)

    tk.Label(frame, text="Nacionalidade:", bg="white").grid(row=2, column=0)

    entry_nacionalidade = tk.Entry(frame, width=35)
    entry_nacionalidade.grid(row=2, column=1)

    tk.Label(frame, text="Geração:", bg="white").grid(row=3, column=0)

    combo_geracao = ttk.Combobox(
        frame,
        values=["1ª geração", "2ª geração"],
        width=32
    )

    combo_geracao.grid(row=3, column=1)

    tk.Label(frame, text="Acolhimento:", bg="white").grid(row=4, column=0)

    combo_acolhimento = ttk.Combobox(
        frame,
        values=["Sim", "Não"],
        width=32
    )

    combo_acolhimento.grid(row=4, column=1)

    # TABELA

    tabela = ttk.Treeview(
        frame,
        columns=("ID", "Nome", "Nacionalidade", "Geração", "Acolhimento"),
        show="headings"
    )

    for col in tabela["columns"]:
        tabela.heading(col, text=col)
        tabela.column(col, width=160)

    tabela.grid(row=7, column=0, columnspan=5, pady=20)

    # FUNÇÕES

    def atualizar_tabela():

        for item in tabela.get_children():
            tabela.delete(item)

        cursor.execute("SELECT * FROM estudantes")
        dados = cursor.fetchall()

        for linha in dados:
            tabela.insert("", "end", values=linha)

    def limpar():

        aluno_id.set("")

        entry_nome.delete(0, tk.END)
        entry_nacionalidade.delete(0, tk.END)

        combo_geracao.set("")
        combo_acolhimento.set("")

    def incluir():

        nome = entry_nome.get()

        if nome == "":
            messagebox.showwarning("Aviso", "Digite o nome")
            return

        cursor.execute("""
        INSERT INTO estudantes
        (nome, nacionalidade, geracao, acolhimento)
        VALUES (?, ?, ?, ?)
        """, (
            entry_nome.get(),
            entry_nacionalidade.get(),
            combo_geracao.get(),
            combo_acolhimento.get()
        ))

        conn.commit()

        atualizar_tabela()
        limpar()

        messagebox.showinfo("Sucesso", "Aluno incluído!")

    def selecionar(event):

        item = tabela.selection()

        if not item:
            return

        dados = tabela.item(item[0])["values"]

        aluno_id.set(dados[0])

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados[1])

        entry_nacionalidade.delete(0, tk.END)
        entry_nacionalidade.insert(0, dados[2])

        combo_geracao.set(dados[3])
        combo_acolhimento.set(dados[4])

    def editar():

        if aluno_id.get() == "":
            messagebox.showwarning("Aviso", "Selecione um aluno")
            return

        cursor.execute("""
        UPDATE estudantes
        SET nome=?, nacionalidade=?, geracao=?, acolhimento=?
        WHERE id=?
        """, (
            entry_nome.get(),
            entry_nacionalidade.get(),
            combo_geracao.get(),
            combo_acolhimento.get(),
            aluno_id.get()
        ))

        conn.commit()

        atualizar_tabela()
        limpar()

        messagebox.showinfo("Sucesso", "Aluno editado!")

    def excluir():

        if aluno_id.get() == "":
            messagebox.showwarning("Aviso", "Selecione um aluno")
            return

        resposta = messagebox.askyesno(
            "Confirmar",
            "Deseja excluir?"
        )

        if resposta:

            cursor.execute(
                "DELETE FROM estudantes WHERE id=?",
                (aluno_id.get(),)
            )

            conn.commit()

            atualizar_tabela()
            limpar()

            messagebox.showinfo("Sucesso", "Aluno excluído!")

    tabela.bind("<<TreeviewSelect>>", selecionar)

    # BOTÕES

    tk.Button(
        frame,
        text="Incluir",
        bg=cor_verde,
        fg="white",
        width=15,
        command=incluir
    ).grid(row=5, column=0, pady=20)

    tk.Button(
        frame,
        text="Editar",
        bg=cor_botao,
        fg="white",
        width=15,
        command=editar
    ).grid(row=5, column=1)

    tk.Button(
        frame,
        text="Excluir",
        bg=cor_vermelho,
        fg="white",
        width=15,
        command=excluir
    ).grid(row=5, column=2)

    tk.Button(
        frame,
        text="Limpar",
        bg=cor_laranja,
        fg="white",
        width=15,
        command=limpar
    ).grid(row=5, column=3)

    atualizar_tabela()

# ================= IMPORTAR CSV =================

def importar_csv():

    arquivo = filedialog.askopenfilename(
        title="Escolha o CSV",
        filetypes=[("CSV", "*.csv")]
    )

    if not arquivo:
        return

    try:

        df = pd.read_csv(
            arquivo,
            sep=";",
            encoding="latin1"
        )

        df.columns = df.columns.str.strip()

        cursor.execute("DELETE FROM alunos_estrangeiros")

        for _, linha in df.iterrows():

            quantidade = linha.get("Nº ALUNOS", 0)

            try:
                quantidade = int(quantidade)
            except:
                quantidade = 0

            cursor.execute("""
            INSERT INTO alunos_estrangeiros
            (diretoria, municipio, escola, pais, quantidade)
            VALUES (?, ?, ?, ?, ?)
            """, (
                str(linha.get("DE", "")),
                str(linha.get("MUN", "")),
                str(linha.get("NOMESC", "")),
                str(linha.get("DS_PAIS", "")),
                quantidade
            ))

        conn.commit()

        messagebox.showinfo(
            "Sucesso",
            "CSV importado!"
        )

    except Exception as erro:

        messagebox.showerror(
            "Erro",
            str(erro)
        )

# ================= DASHBOARD =================

def dashboard_csv():

    cursor.execute("""
    SELECT pais, SUM(quantidade)
    FROM alunos_estrangeiros
    GROUP BY pais
    ORDER BY SUM(quantidade) DESC
    LIMIT 10
    """)

    dados = cursor.fetchall()

    if not dados:
        messagebox.showwarning(
            "Aviso",
            "Importe o CSV primeiro"
        )
        return

    nomes = [d[0] for d in dados]
    valores = [d[1] for d in dados]

    janela = tk.Toplevel()
    janela.title("Dashboard")
    janela.geometry("1200x700")
    janela.configure(bg=cor_fundo)

    tk.Label(
        janela,
        text="Dashboard de Alunos Estrangeiros",
        font=("Arial", 24, "bold"),
        bg=cor_fundo,
        fg="white"
    ).pack(pady=20)

    frame = tk.Frame(janela, bg="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    fig = plt.Figure(figsize=(12, 5), dpi=100)

    cores = [
        "#2563eb",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6",
        "#06b6d4",
        "#ec4899",
        "#84cc16",
        "#14b8a6",
        "#f97316"
    ]

    ax1 = fig.add_subplot(121)

    ax1.barh(
        nomes,
        valores,
        color=cores[:len(nomes)]
    )

    ax1.set_title("Top 10 Países")
    ax1.invert_yaxis()

    ax2 = fig.add_subplot(122)

    ax2.pie(
        valores,
        labels=nomes,
        autopct="%1.1f%%",
        colors=cores[:len(nomes)]
    )

    ax2.set_title("Porcentagem")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(
        fig,
        master=frame
    )

    canvas.draw()

    canvas.get_tk_widget().pack(
        fill="both",
        expand=True
    )

# ================= MENU =================

def criar_botao(texto, comando):

    btn = tk.Button(
        frame_menu,
        text=texto,
        command=comando,
        bg=cor_botao,
        fg="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        height=2
    )

    btn.pack(fill="x", padx=10, pady=8)

criar_botao("👨‍🎓 Alunos", abrir_alunos)
criar_botao("🌍 Importar CSV", importar_csv)
criar_botao("📊 Dashboard CSV", dashboard_csv)
criar_botao("❌ Sair", root.destroy)

# ================= TELA =================

titulo = tk.Label(
    frame_principal,
    text="Painel Principal",
    font=("Arial", 32, "bold"),
    bg=cor_fundo,
    fg="white"
)

titulo.pack(pady=40)

sub = tk.Label(
    frame_principal,
    text="Sistema Escolar com Dashboard",
    font=("Arial", 18),
    bg=cor_fundo,
    fg="white"
)

sub.pack()

root.mainloop()