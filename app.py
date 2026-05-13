import tkinter as tk
from tkinter import ttk, messagebox
import database

# ================= CONFIG =================
database.criar_tabela()
id_selecionado = None

# ================= FUNÇÕES =================

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

    dados = database.contar_por_nacionalidade()

    nomes = [d[0] for d in dados]
    valores = [d[1] for d in dados]

    plt.style.use("ggplot")

cores = ["#2563EB", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

plt.bar(
    nomes,
    valores,
    color=cores,
    edgecolor="black",
    linewidth=2

    plt.title("Estudantes por Nacionalidade")
    plt.xlabel("Nacionalidade")
    plt.ylabel("Quantidade")
    plt.show()


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


# ================= TELA CADASTRO =================

def abrir_cadastro():
    global entry_nome, entry_nacionalidade, combo_geracao, combo_acolhimento, lista, entry_busca

    janela = tk.Toplevel()
    janela.title("Cadastro de Estudantes")
    janela.geometry("850x550")
    janela.configure(bg="#e3f2fd")

    # Título
    tk.Label(janela, text="Cadastro de Estudantes",
             font=("Arial", 16, "bold"),
             bg="#e3f2fd").pack(pady=10)

    # Formulário
    frame_form = tk.Frame(janela, bg="white", bd=2, relief="groove")
    frame_form.pack(pady=10, padx=20, fill="x")

    tk.Label(frame_form, text="Nome:", bg="white").grid(row=0, column=0)
    entry_nome = tk.Entry(frame_form)
    entry_nome.grid(row=0, column=1)

    tk.Label(frame_form, text="Nacionalidade:", bg="white").grid(row=1, column=0)
    entry_nacionalidade = tk.Entry(frame_form)
    entry_nacionalidade.grid(row=1, column=1)

    tk.Label(frame_form, text="Geração:", bg="white").grid(row=2, column=0)
    combo_geracao = ttk.Combobox(frame_form, values=["1ª geração", "2ª geração"])
    combo_geracao.grid(row=2, column=1)

    tk.Label(frame_form, text="Acolhimento:", bg="white").grid(row=3, column=0)
    combo_acolhimento = ttk.Combobox(frame_form, values=["Sim", "Não"])
    combo_acolhimento.grid(row=3, column=1)

    # Botões
    tk.Button(
    janela,
    text="📊\nExcel",
    command=excel,
    bg="#10B981",
    fg="white",
    font=("Arial", 14, "bold"),
    width=14,
    height=4,
    activebackground="#047857",
    activeforeground="white"
)

    tk.Button(frame_form, text="Excluir", bg="#f44336", fg="white", command=excluir)\
        .grid(row=4, column=1)

    # Busca
    frame_busca = tk.Frame(janela, bg="#e3f2fd")
    frame_busca.pack(pady=5)

    tk.Label(frame_busca, text="Buscar:", bg="#e3f2fd").pack(side=tk.LEFT)

    entry_busca = tk.Entry(frame_busca)
    entry_busca.pack(side=tk.LEFT, padx=5)

    tk.Button(frame_busca, text="Buscar", command=buscar).pack(side=tk.LEFT)
    tk.Button(frame_busca, text="Mostrar todos", command=atualizar_lista).pack(side=tk.LEFT)

    # Tabela
    frame_lista = tk.Frame(janela)
    frame_lista.pack(fill="both", expand=True, padx=20, pady=10)

    lista = ttk.Treeview(frame_lista,
                         columns=("ID", "Nome", "Nacionalidade", "Geração", "Acolhimento"),
                         show="headings")

    for col in lista["columns"]:
        lista.heading(col, text=col)

    lista.pack(fill="both", expand=True)
    lista.bind("<ButtonRelease-1>", selecionar_item)

    atualizar_lista()


# ================= MENU PRINCIPAL =================

root = tk.Tk()
root.title("Sistema Escolar")
root.geometry("400x500")
root.configure(bg="#e3f2fd")

frame_menu = tk.Frame(root, bg="#e3f2fd")
frame_menu.pack(pady=40)

def card(texto, comando, linha, coluna):
    tk.Button(frame_menu,
              text=texto,
              font=("Arial", 12, "bold"),
              width=15,
              height=5,
              bg="white",
              relief="raised",
              command=comando).grid(row=linha, column=coluna, padx=10, pady=10)

# Cards estilo app
card("📚\nAlunos", abrir_cadastro, 0, 0)
card("📊\nGráfico", grafico, 0, 1)
card("📥\nExcel", exportar_excel, 1, 0)
card("❌\nSair", root.destroy, 1, 1)

# ================= START =================
root.mainloop()