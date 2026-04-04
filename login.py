import tkinter as tk
from tkinter import messagebox

def verificar_login():
    usuario = entry_user.get()
    senha = entry_pass.get()

    if usuario == "admin" and senha == "123":
        root.destroy()
        import app
    else:
        messagebox.showerror("Erro", "Login inválido")

root = tk.Tk()
root.title("Login - Sistema Escolar")
root.geometry("300x200")

tk.Label(root, text="Usuário").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack()

tk.Label(root, text="Senha").pack(pady=5)
entry_pass = tk.Entry(root, show="*")
entry_pass.pack()

tk.Button(root, text="Entrar", command=verificar_login).pack(pady=15)

root.mainloop()