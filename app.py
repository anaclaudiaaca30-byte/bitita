import tkinter as tk
from tkinter import ttk, messagebox
import database

database.criar_tabela()
id_selecionado = None

# ================= CORES AZUIS =================
cor_fundo = "#0f3fa8"
cor_frame = "#0b2f7a"
cor_botao = "#2563eb"
cor_menu = "#082567"
cor_menu_botao = "#0b3ea8"
cor_texto = "white"
cor_vermelho = "#ef4444"
cor_verde = "#10b981"


def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_nacionalidade.delete(0, tk.END)
    combo_geracao.set("")
    combo_acolhimento.set("")


def salvar():
    global id_selecionado

    nome = entry_nome.get()
    nacionalidade = entry_nacionalidade.get()
    geracao = combo_geracao.get()
    acolhimento = combo_acolhimento.get()

    if not nome:
        messagebox.showwarning("Aviso", "Preencha o nome")
        return

    if id_selecionado is None:
        database.inserir(nome, nacionalidade, geracao, acolhimento)
    else:
        database.atualizar(id_selecionado, nome, nacionalidade, geracao, acolhimento)
        id_selecionado = None

    atualizar_lista()
    limpar_campos()


def excluir():
    global id_selecionado

    if id_selecionado is None:
        messagebox.showwarning("Aviso", "Selecione um aluno")
        return

    if messagebox.askyesno("Confirmar", "Deseja excluir?"):
        database.deletar(id_selecionado)
        id_selecionado = None
        atualizar_lista()
        limpar_campos()


def buscar():
    nome = entry_busca.get()
    dados = database.buscar(nome)

    lista.delete(*lista.get_children())
    for linha in dados:
        lista.insert("", tk.END, values=linha)


def atualizar_lista():
    dados = database.listar()

    lista.delete(*lista.get_children())
    for linha in dados:
        lista.insert("", tk.END, values=linha)


def selecionar_item(event):
    global id_selecionado

    item = lista.focus()
    dados = lista.item(item, "values")

    if dados:
        id_selecionado = dados[0]

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados[1])

        entry_nacionalidade.delete(0, tk.END)
        entry_nacionalidade.insert(0, dados[2])

        combo_geracao.set(dados[3])
        combo_acolhimento.set(dados[4])


def grafico():
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    dados = database.contar_por_nacionalidade()

    if not dados:
        messagebox.showwarning("Aviso", "Não há dados para gerar gráfico")
        return

    nomes = [d[0] for d in dados]
    valores = [d[1] for d in dados]
    total = sum(valores)

    janela_grafico = tk.Toplevel()
    janela_grafico.title("Dashboard de Gráficos")
    janela_grafico.geometry("1000x650")
    janela_grafico.configure(bg=cor_fundo)

    tk.Label(
        janela_grafico,
        text="📊 Dashboard de Estudantes",
        font=("Arial", 24, "bold"),
        bg=cor_fundo,
        fg="white"
    ).pack(pady=15)

    frame_cards = tk.Frame(janela_grafico, bg=cor_fundo)
    frame_cards.pack(pady=10)

    def card_info(titulo, valor, cor):
        frame = tk.Frame(frame_cards, bg=cor, width=220, height=80)
        frame.pack(side=tk.LEFT, padx=15)
        frame.pack_propagate(False)

        tk.Label(frame, text=titulo, bg=cor, fg="white", font=("Arial", 11, "bold")).pack(pady=5)
        tk.Label(frame, text=valor, bg=cor, fg="white", font=("Arial", 22, "bold")).pack()

    card_info("Total de Alunos", total, "#2563eb")
    card_info("Nacionalidades", len(nomes), "#10b981")
    card_info("Categorias", len(valores), "#f59e0b")

    frame_graficos = tk.Frame(janela_grafico, bg="white")
    frame_graficos.pack(fill="both", expand=True, padx=20, pady=20)

    fig = plt.Figure(figsize=(10, 5), dpi=100)

    cores = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#06B6D4"]

    # Gráfico de barras
    ax1 = fig.add_subplot(121)
    ax1.bar(nomes, valores, color=cores[:len(nomes)])
    ax1.set_title("Estudantes por Nacionalidade")
    ax1.set_xlabel("Nacionalidade")
    ax1.set_ylabel("Quantidade")

    for i, valor in enumerate(valores):
        ax1.text(i, valor + 0.1, str(valor), ha="center", fontweight="bold")

    # Gráfico de pizza
    ax2 = fig.add_subplot(122)
    ax2.pie(
        valores,
        labels=nomes,
        autopct="%1.1f%%",
        startangle=90,
        colors=cores[:len(nomes)]
    )
    ax2.set_title("Porcentagem por Nacionalidade")

    canvas = FigureCanvasTkAgg(fig, master=frame_graficos)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)


def exportar_excel():
    from openpyxl import Workbook

    dados = database.listar()

    wb = Workbook()
    ws = wb.active
    ws.title = "Estudantes"

    ws.append(["ID", "Nome", "Nacionalidade", "Geração", "Acolhimento"])

    for linha in dados:
        ws.append(linha)

    wb.save("relatorio_estudantes.xlsx")
    messagebox.showinfo("Sucesso", "Excel gerado!")


def abrir_cadastro():
    global entry_nome, entry_nacionalidade, combo_geracao, combo_acolhimento, lista, entry_busca

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

    frame_form = tk.Frame(janela, bg=cor_frame, bd=2, relief="ridge")
    frame_form.pack(padx=20, pady=10, fill="x")

    tk.Label(frame_form, text="Nome:", bg=cor_frame, fg="white").grid(row=0, column=0, padx=10, pady=10)
    entry_nome = tk.Entry(frame_form, width=30)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame_form, text="Nacionalidade:", bg=cor_frame, fg="white").grid(row=1, column=0, padx=10, pady=10)
    entry_nacionalidade = tk.Entry(frame_form, width=30)
    entry_nacionalidade.grid(row=1, column=1)

    tk.Label(frame_form, text="Geração:", bg=cor_frame, fg="white").grid(row=2, column=0, padx=10, pady=10)
    combo_geracao = ttk.Combobox(frame_form, values=["1ª geração", "2ª geração"])
    combo_geracao.grid(row=2, column=1)

    tk.Label(frame_form, text="Acolhimento:", bg=cor_frame, fg="white").grid(row=3, column=0, padx=10, pady=10)
    combo_acolhimento = ttk.Combobox(frame_form, values=["Sim", "Não"])
    combo_acolhimento.grid(row=3, column=1)

    frame_botoes = tk.Frame(janela, bg=cor_fundo)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Salvar", bg=cor_verde, fg="white", width=15, font=("Arial", 10, "bold"), command=salvar).grid(row=0, column=0, padx=10)
    tk.Button(frame_botoes, text="Excluir", bg=cor_vermelho, fg="white", width=15, font=("Arial", 10, "bold"), command=excluir).grid(row=0, column=1, padx=10)
    tk.Button(frame_botoes, text="Excel", bg=cor_botao, fg="white", width=15, font=("Arial", 10, "bold"), command=exportar_excel).grid(row=0, column=2, padx=10)

    frame_busca = tk.Frame(janela, bg=cor_fundo)
    frame_busca.pack(pady=10)

    tk.Label(frame_busca, text="Buscar:", bg=cor_fundo, fg="white").pack(side=tk.LEFT)

    entry_busca = tk.Entry(frame_busca)
    entry_busca.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_busca, text="Buscar", command=buscar).pack(side=tk.LEFT)
    tk.Button(frame_busca, text="Mostrar Todos", command=atualizar_lista).pack(side=tk.LEFT)

    frame_lista = tk.Frame(janela)
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    lista = ttk.Treeview(
        frame_lista,
        columns=("ID", "Nome", "Nacionalidade", "Geração", "Acolhimento"),
        show="headings"
    )

    for col in lista["columns"]:
        lista.heading(col, text=col)

    lista.pack(fill="both", expand=True)
    lista.bind("<ButtonRelease-1>", selecionar_item)

    atualizar_lista()


# ================= MENU PRINCIPAL =================

root = tk.Tk()
root.title("Sistema Escolar Bitita")
root.geometry("950x600")
root.configure(bg=cor_fundo)

menu_lateral = tk.Frame(root, bg=cor_menu, width=220)
menu_lateral.pack(side="left", fill="y")

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

area_principal = tk.Frame(root, bg=cor_fundo)
area_principal.pack(side="right", expand=True, fill="both")

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
        activebackground=cor_botao,
        activeforeground="white",
        font=("Arial", 12, "bold"),
        relief="flat",
        width=18,
        height=2,
        cursor="hand2"
    ).pack(pady=12)


botao_menu("📚  Alunos", abrir_cadastro)
botao_menu("📊  Gráficos", grafico)
botao_menu("📥  Excel", exportar_excel)
botao_menu("❌  Sair", root.destroy)

mensagem = tk.Label(
    area_principal,
    text="Bem-vinda ao Sistema Escolar Bitita",
    bg=cor_fundo,
    fg="#dbeafe",
    font=("Arial", 16)
)
mensagem.pack(pady=20)

root.mainloop()