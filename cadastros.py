import tkinter as tk
from tkinter import messagebox, ttk
import os
import re

ARQUIVO_DADOS = "dados.txt"

janela_dados_aberta = None

def salvar_dados(nome, sobrenome, telefone, email):
    with open(ARQUIVO_DADOS, "a") as f:
        f.write(f"{nome},{sobrenome},{telefone},{email}\n")
    messagebox.showinfo("Sucesso", "Dados cadastrados com sucesso!")

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, "r") as f:
        dados = [linha.strip().split(",") for linha in f.readlines()]
    return [d for d in dados if len(d) == 4]  

def formatar_telefone(event):
    telefone = entry_telefone.get()
    telefone = re.sub(r"\D", "", telefone)  
    if len(telefone) == 11:
        telefone_formatado = f"({telefone[:2]}){telefone[2:7]}-{telefone[7:]}"
        entry_telefone.delete(0, tk.END)
        entry_telefone.insert(0, telefone_formatado)

def mostrar_dados():
    global janela_dados_aberta 

    if janela_dados_aberta:
        janela_dados_aberta.destroy()

    dados = carregar_dados()
    janela_dados_aberta = tk.Toplevel(root)
    janela_dados_aberta.title("Registros Cadastrados")
    janela_dados_aberta.geometry("600x350")
    janela_dados_aberta.configure(bg="#f0f0f0")
    janela_dados_aberta.resizable(False, False)

    frame = tk.Frame(janela_dados_aberta, bg="#f0f0f0")
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    tree = ttk.Treeview(frame, columns=("Nome", "Sobrenome", "Telefone", "Email"), show="headings")
    tree.heading("Nome", text="Nome")
    tree.heading("Sobrenome", text="Sobrenome")
    tree.heading("Telefone", text="Telefone")
    tree.heading("Email", text="Email")
    
    for col in ("Nome", "Sobrenome", "Telefone", "Email"):
        tree.column(col, anchor="center", width=140)
    
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)
    
    for i, (nome, sobrenome, telefone, email) in enumerate(dados):
        if i % 2 == 0:
            tree.insert("", tk.END, values=(nome, sobrenome, telefone, email), tags=("even",))
        else:
            tree.insert("", tk.END, values=(nome, sobrenome, telefone, email), tags=("odd",))

    tree.tag_configure("even", background="#f2f2f2")  
    tree.tag_configure("odd", background="#ffffff")   

    btn_fechar = tk.Button(janela_dados_aberta, text="Fechar", command=janela_dados_aberta.destroy, font=("Arial", 12))
    btn_fechar.pack(pady=5)

def excluir_dado():
    janela_excluir = tk.Toplevel(root)
    janela_excluir.title("Excluir Registro")
    janela_excluir.geometry("300x180")  
    janela_excluir.configure(bg="#f0f0f0")
    janela_excluir.resizable(False, False)

    tk.Label(janela_excluir, text="DIGITE O NOME PARA EXCLUIR:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)

    entry_nome_excluir = tk.Entry(janela_excluir, font=("Arial", 12))
    entry_nome_excluir.pack(pady=5)

    def excluir():
        nome = entry_nome_excluir.get().strip()
        if not nome:
            messagebox.showerror("Erro", "Por favor, insira um nome.")
            return
        
        dados = carregar_dados()
        novos_dados = [d for d in dados if d[0] != nome]
        
        if len(dados) == len(novos_dados):
            messagebox.showwarning("Aviso", f"Nenhum registro encontrado para o nome {nome}.")
            return

        with open(ARQUIVO_DADOS, "w") as f:
            for nome, sobrenome, telefone, email in novos_dados:
                f.write(f"{nome},{sobrenome},{telefone},{email}\n")
        
        messagebox.showinfo("Excluído", "Registro excluído com sucesso!")
        entry_nome_excluir.delete(0, tk.END) 
        mostrar_dados()
    btn_excluir = tk.Button(janela_excluir, text="Excluir", command=excluir, font=("Arial", 12), width=15)
    btn_excluir.pack(pady=10)

    btn_fechar = tk.Button(janela_excluir, text="Fechar", command=janela_excluir.destroy, font=("Arial", 12))
    btn_fechar.pack(pady=5)

def cadastrar():
    nome = entry_nome.get().strip()
    sobrenome = entry_sobrenome.get().strip()
    telefone = entry_telefone.get().strip()
    email = entry_email.get().strip()
    
    if not nome or not sobrenome or not telefone or "@" not in email:
        messagebox.showerror("Erro", "Dados inválidos!")
        return
    salvar_dados(nome, sobrenome, telefone, email)
    entry_nome.delete(0, tk.END)
    entry_sobrenome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    mostrar_dados()

root = tk.Tk()
root.title("Cadastro de Usuários")
root.geometry("450x400")
root.configure(bg="#f0f0f0")

root.resizable(False, False)

frame_principal = tk.Frame(root, bg="#f0f0f0")
frame_principal.pack(pady=20)

tk.Label(frame_principal, text="Nome:", bg="#f0f0f0", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_nome = tk.Entry(frame_principal, font=("Arial", 12))
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_principal, text="Sobrenome:", bg="#f0f0f0", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5)
entry_sobrenome = tk.Entry(frame_principal, font=("Arial", 12))
entry_sobrenome.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_principal, text="Telefone:", bg="#f0f0f0", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5)
entry_telefone = tk.Entry(frame_principal, font=("Arial", 12))
entry_telefone.grid(row=2, column=1, padx=5, pady=5)
entry_telefone.bind("<FocusOut>", formatar_telefone)

tk.Label(frame_principal, text="Email:", bg="#f0f0f0", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5)
entry_email = tk.Entry(frame_principal, font=("Arial", 12))
entry_email.grid(row=3, column=1, padx=5, pady=5)

frame_botoes = tk.Frame(root, bg="#f0f0f0")
frame_botoes.pack(pady=10)

tk.Button(frame_botoes, text="Cadastrar", command=cadastrar, font=("Arial", 12), width=15).pack(pady=5)

tk.Button(frame_botoes, text="Consultar", command=mostrar_dados, font=("Arial", 12), width=15).pack(pady=5)

tk.Button(frame_botoes, text="Excluir", command=excluir_dado, font=("Arial", 12), width=15).pack(pady=5)

tk.Button(frame_botoes, text="Sair", command=root.quit, font=("Arial", 12), width=15).pack(pady=5)

root.mainloop()
