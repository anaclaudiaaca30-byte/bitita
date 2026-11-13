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
cor_botao_hover = "#1d4ed8"
cor_verde = "#10b981"
cor_laranja = "#f59e0b"
cor_vermelho = "#ef4444"
cor_texto = "#0f172a"
cor_branco = "#ffffff"
cor_fundo_painel = "#f8fafc"

# ================= FUNÇÕES AUXILIARES =================

def limpar_texto(valor):
    if valor is None:
        return ""
    return str(valor).strip()


def normalizar_quantidade(valor):
    try:
        if valor is None:
            return 0
        texto = str(valor).strip().replace(".", "").replace(",", ".")
        return max(0, int(float(texto)))
    except (TypeError, ValueError):
        return 0


def atualizar_status(mensagem, cor="#e2e8f0"):
    if "status_label" in globals():
        status_label.config(text=mensagem, fg=cor)


# ================= JANELA =================

root = tk.Tk()
root.title("Sistema Escolar Bitita")
root.geometry("1400x800")
root.configure(bg=cor_fundo)
root.minsize(1100, 650)

frame_menu = tk.Frame(root, bg=cor_menu, width=240)
frame_menu.pack(side="left", fill="y")

frame_principal = tk.Frame(root, bg=cor_fundo)
frame_principal.pack(side="right", fill="both", expand=True)

titulo_menu = tk.Label(
    frame_menu,
    text="BITITA",
    font=("Arial", 26, "bold"),
    bg=cor_menu,
    fg="white",
    pady=20
)
titulo_menu.pack(fill="x")

status_label = tk.Label(
    root,
    text="Sistema pronto para uso.",
    bg=cor_fundo,
    fg="white",
    anchor="w",
    justify="left",
    padx=20,
    pady=8,
    font=("Arial", 10, "bold")
)
status_label.pack(fill="x", side="bottom")

# ================= CADASTRO =================

def abrir_alunos():
    janela = tk.Toplevel()
    janela.title("Cadastro de Estudantes")
    janela.geometry("1100x700")
    janela.configure(bg=cor_fundo)
    janela.minsize(900, 600)
    janela.transient(root)
    janela.grab_set()

    aluno_id = tk.StringVar()

    frame = tk.Frame(janela, bg=cor_fundo_painel)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tk.Label(
        frame,
        text="Cadastro de Estudantes",
        font=("Arial", 18, "bold"),
        bg=cor_fundo_painel,
        fg=cor_texto
    ).grid(row=0, column=0, columnspan=5, pady=20)

    tk.Label(frame, text="Nome:", bg=cor_fundo_painel, fg=cor_texto, font=("Arial", 10, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
    entry_nome = tk.Entry(frame, width=35, font=("Arial", 11))
    entry_nome.grid(row=1, column=1, padx=10, sticky="ew")

    tk.Label(frame, text="Nacionalidade:", bg=cor_fundo_painel, fg=cor_texto, font=("Arial", 10, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
    entry_nacionalidade = tk.Entry(frame, width=35, font=("Arial", 11))
    entry_nacionalidade.grid(row=2, column=1, padx=10, sticky="ew")

    tk.Label(frame, text="Geração:", bg=cor_fundo_painel, fg=cor_texto, font=("Arial", 10, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="w")
    combo_geracao = ttk.Combobox(frame, values=["1ª geração", "2ª geração"], width=32, state="readonly")
    combo_geracao.grid(row=3, column=1, padx=10, sticky="ew")

    tk.Label(frame, text="Acolhimento:", bg=cor_fundo_painel, fg=cor_texto, font=("Arial", 10, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="w")
    combo_acolhimento = ttk.Combobox(frame, values=["Sim", "Não"], width=32, state="readonly")
    combo_acolhimento.grid(row=4, column=1, padx=10, sticky="ew")

    tabela = ttk.Treeview(frame, columns=("ID", "Nome", "Nacionalidade", "Geração", "Acolhimento"), show="headings")
    for col in tabela["columns"]:
        tabela.heading(col, text=col)
        tabela.column(col, width=180, anchor="center")
    tabela.grid(row=7, column=0, columnspan=5, padx=10, pady=20, sticky="nsew")

    for coluna in range(2):
        frame.grid_columnconfigure(coluna, weight=1)
    frame.grid_rowconfigure(7, weight=1)

    def atualizar_tabela():
        for item in tabela.get_children():
            tabela.delete(item)
        cursor.execute("SELECT * FROM estudantes ORDER BY id")
        for linha in cursor.fetchall():
            tabela.insert("", "end", values=linha)

    def limpar():
        aluno_id.set("")
        entry_nome.delete(0, tk.END)
        entry_nacionalidade.delete(0, tk.END)
        combo_geracao.set("")
        combo_acolhimento.set("")
        entry_nome.focus_set()
        atualizar_status("Formulário limpo e pronto para um novo cadastro.")

    def incluir():
        nome = limpar_texto(entry_nome.get())
        nacionalidade = limpar_texto(entry_nacionalidade.get())
        geracao = limpar_texto(combo_geracao.get())
        acolhimento = limpar_texto(combo_acolhimento.get())

        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do estudante antes de salvar.")
            entry_nome.focus_set()
            return

        cursor.execute(
            """
            INSERT INTO estudantes (nome, nacionalidade, geracao, acolhimento)
            VALUES (?, ?, ?, ?)
            """,
            (nome, nacionalidade, geracao, acolhimento)
        )
        conn.commit()
        atualizar_tabela()
        limpar()
        messagebox.showinfo("Sucesso", "Estudante incluído com sucesso!")
        atualizar_status("Estudante incluído com sucesso.")

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
        atualizar_status(f"Estudante selecionado: {dados[1]}.")

    def editar():
        if aluno_id.get() == "":
            messagebox.showwarning("Aviso", "Selecione um estudante para editar.")
            return

        nome = limpar_texto(entry_nome.get())
        nacionalidade = limpar_texto(entry_nacionalidade.get())
        geracao = limpar_texto(combo_geracao.get())
        acolhimento = limpar_texto(combo_acolhimento.get())

        if not nome:
            messagebox.showwarning("Aviso", "O nome do estudante não pode ficar vazio.")
            entry_nome.focus_set()
            return

        cursor.execute(
            """
            UPDATE estudantes
            SET nome=?, nacionalidade=?, geracao=?, acolhimento=?
            WHERE id=?
            """,
            (nome, nacionalidade, geracao, acolhimento, aluno_id.get())
        )
        conn.commit()
        atualizar_tabela()
        limpar()
        messagebox.showinfo("Sucesso", "Estudante atualizado com sucesso!")
        atualizar_status("Dados do estudante atualizados.")

    def excluir():
        if aluno_id.get() == "":
            messagebox.showwarning("Aviso", "Selecione um estudante para excluir.")
            return

        resposta = messagebox.askyesno("Confirmar exclusão", "Deseja realmente excluir o estudante selecionado?")
        if not resposta:
            return

        cursor.execute("DELETE FROM estudantes WHERE id=?", (aluno_id.get(),))
        conn.commit()
        atualizar_tabela()
        limpar()
        messagebox.showinfo("Sucesso", "Estudante excluído com sucesso!")
        atualizar_status("Estudante removido do cadastro.")

    tabela.bind("<<TreeviewSelect>>", selecionar)
    entry_nome.bind("<Return>", lambda event: incluir())
    entry_nacionalidade.bind("<Return>", lambda event: incluir())
    combo_geracao.bind("<Return>", lambda event: incluir())
    combo_acolhimento.bind("<Return>", lambda event: incluir())

    def botao_acao(texto, comando, cor, linha, coluna):
        btn = tk.Button(
            frame,
            text=texto,
            bg=cor,
            fg="white",
            width=15,
            font=("Arial", 10, "bold"),
            command=comando,
            bd=0,
            highlightthickness=0,
            activebackground=cor
        )
        btn.grid(row=linha, column=coluna, padx=8, pady=20)
        btn.bind("<FocusIn>", lambda event: event.widget.config(highlightbackground=cor))
        return btn

    botao_acao("Incluir", incluir, cor_verde, 5, 0)
    botao_acao("Editar", editar, cor_botao, 5, 1)
    botao_acao("Excluir", excluir, cor_vermelho, 5, 2)
    botao_acao("Limpar", limpar, cor_laranja, 5, 3)

    atualizar_tabela()
    entry_nome.focus_set()
    janela.bind("<Escape>", lambda event: limpar())

# ================= IMPORTAR CSV =================

def importar_csv():
    arquivo = filedialog.askopenfilename(
        title="Escolha o arquivo CSV",
        filetypes=[("CSV", "*.csv"), ("Arquivos de texto", "*.txt")]
    )
    if not arquivo:
        return

    try:
        df = pd.read_csv(arquivo, sep=";", encoding="latin1", dtype=str)
        if df.empty:
            messagebox.showwarning("Aviso", "O arquivo CSV está vazio.")
            return

        df.columns = [limpar_texto(col) for col in df.columns]

        colunas_necessarias = {
            "DE": "diretoria",
            "MUN": "municipio",
            "NOMESC": "escola",
            "DS_PAIS": "pais",
            "Nº ALUNOS": "quantidade",
        }

        mapeamento = {}
        for coluna_original, alias in colunas_necessarias.items():
            coluna_encontrada = next((col for col in df.columns if col.strip().upper() == coluna_original), None)
            if coluna_encontrada is not None:
                mapeamento[alias] = coluna_encontrada

        colunas_faltando = [nome for nome, _ in colunas_necessarias.items() if nome not in {c.upper() for c in df.columns}]
        if colunas_faltando:
            raise ValueError(f"Colunas obrigatórias ausentes: {', '.join(colunas_faltando)}")

        dados = pd.DataFrame({
            "diretoria": df[mapeamento["diretoria"]].fillna(""),
            "municipio": df[mapeamento["municipio"]].fillna(""),
            "escola": df[mapeamento["escola"]].fillna(""),
            "pais": df[mapeamento["pais"]].fillna(""),
            "quantidade": df[mapeamento["quantidade"]].fillna("0"),
        })

        dados["diretoria"] = dados["diretoria"].astype(str).str.strip()
        dados["municipio"] = dados["municipio"].astype(str).str.strip()
        dados["escola"] = dados["escola"].astype(str).str.strip()
        dados["pais"] = dados["pais"].astype(str).str.strip()
        dados["quantidade"] = dados["quantidade"].apply(normalizar_quantidade)

        dados_validos = dados[(dados["pais"] != "") & (dados["quantidade"] > 0)].copy()
        linhas_ignoradas = len(dados) - len(dados_validos)

        cursor.execute("DELETE FROM alunos_estrangeiros")

        for _, linha in dados_validos.iterrows():
            cursor.execute(
                """
                INSERT INTO alunos_estrangeiros (diretoria, municipio, escola, pais, quantidade)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    linha["diretoria"],
                    linha["municipio"],
                    linha["escola"],
                    linha["pais"],
                    int(linha["quantidade"]),
                )
            )

        conn.commit()

        mensagem = (
            f"CSV importado com sucesso.\n"
            f"Registros válidos: {len(dados_validos)}\n"
            f"Registros ignorados: {linhas_ignoradas}"
        )
        messagebox.showinfo("Sucesso", mensagem)
        atualizar_status("Importação concluída com análise de qualidade aplicada.")

    except Exception as erro:
        messagebox.showerror("Erro", f"Não foi possível importar o CSV.\n{erro}")
        atualizar_status("Falha na importação do CSV.", "#fca5a5")

# ================= DASHBOARD =================

def dashboard_csv():
    cursor.execute(
        """
        SELECT pais, SUM(quantidade) AS total
        FROM alunos_estrangeiros
        WHERE pais IS NOT NULL AND TRIM(pais) <> ''
        GROUP BY pais
        ORDER BY total DESC
        LIMIT 10
        """
    )
    dados = cursor.fetchall()

    if not dados:
        messagebox.showwarning("Aviso", "Não há dados importados para gerar o dashboard.")
        return

    nomes = [d[0] for d in dados]
    valores = [int(d[1]) for d in dados]
    total_registros = sum(valores)
    pais_lider = nomes[0]
    total_paises = len(nomes)

    janela = tk.Toplevel()
    janela.title("Dashboard de Alunos Estrangeiros")
    janela.geometry("1300x800")
    janela.configure(bg=cor_fundo)
    janela.minsize(1000, 650)
    janela.transient(root)
    janela.grab_set()

    tk.Label(
        janela,
        text="Dashboard de Alunos Estrangeiros",
        font=("Arial", 24, "bold"),
        bg=cor_fundo,
        fg="white"
    ).pack(pady=18)

    resumo = (
        f"Total de estudantes: {total_registros} | "
        f"Países representados: {total_paises} | "
        f"Maior volume: {pais_lider}"
    )
    tk.Label(
        janela,
        text=resumo,
        bg=cor_fundo,
        fg="white",
        font=("Arial", 11, "bold"),
        wraplength=1100,
        justify="center"
    ).pack(pady=(0, 12))

    painel = tk.Frame(janela, bg="white")
    painel.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    tree = ttk.Treeview(painel, columns=("Pais", "Total"), show="headings")
    tree.heading("Pais", text="País")
    tree.heading("Total", text="Total")
    tree.column("Pais", width=400, anchor="center")
    tree.column("Total", width=160, anchor="center")
    tree.pack(side="left", fill="y", padx=10, pady=10)

    for pais, total in zip(nomes, valores):
        tree.insert("", "end", values=(pais, total))

    chart_frame = tk.Frame(painel, bg="white")
    chart_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    fig = plt.Figure(figsize=(10, 5), dpi=100)
    cores = [
        "#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6",
        "#06b6d4", "#ec4899", "#84cc16", "#14b8a6", "#f97316"
    ]

    ax1 = fig.add_subplot(121)
    ax1.barh(nomes, valores, color=cores[: len(nomes)])
    ax1.set_title("Top 10 países")
    ax1.invert_yaxis()
    ax1.set_xlabel("Quantidade")

    ax2 = fig.add_subplot(122)
    ax2.pie(valores, labels=nomes, autopct="%1.1f%%", colors=cores[: len(nomes)])
    ax2.set_title("Distribuição percentual")

    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    janela.bind("<Escape>", lambda event: janela.destroy())

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
        height=2,
        activebackground=cor_botao_hover,
        width=18,
        bd=0,
        highlightthickness=0,
        cursor="hand2"
    )
    btn.pack(fill="x", padx=12, pady=8)
    btn.bind("<FocusIn>", lambda event: btn.config(bg=cor_botao_hover))
    btn.bind("<FocusOut>", lambda event: btn.config(bg=cor_botao))
    return btn

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
    text="Sistema Escolar com Dashboard e análise robusta de dados",
    font=("Arial", 18),
    bg=cor_fundo,
    fg="white"
)
sub.pack(pady=10)

# Atalhos de teclado para melhorar a acessibilidade
root.bind("<Control-q>", lambda event: root.destroy())
root.bind("<Alt-a>", lambda event: abrir_alunos())
root.bind("<Alt-c>", lambda event: importar_csv())
root.bind("<Alt-d>", lambda event: dashboard_csv())
root.focus_set()

root.mainloop()