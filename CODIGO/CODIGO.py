import tkinter as tk
import sqlite3
import os
import hashlib
from tkinter import messagebox

def obter_caminho_db():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "DATABASE.db")

def criar_banco_de_dados():
    caminho_db = obter_caminho_db()
    if not os.path.exists(caminho_db):
        conn = sqlite3.connect(caminho_db)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            usuario TEXT NOT NULL,
                            senha TEXT NOT NULL
                          )''')
        conn.commit()
        conn.close()

def exibir_mensagem(msg):
    messagebox.showinfo("Mensagem", msg)

def criptografar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def processar_usuario(usuario, senha_usuario, acao):
    caminho_db = obter_caminho_db()
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    senha_criptografada = criptografar_senha(senha_usuario)

    if acao == "cadastrar":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if not cursor.fetchone():
            cursor.execute('''CREATE TABLE usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                usuario TEXT NOT NULL,
                                senha TEXT NOT NULL
                              )''')
            conn.commit()

        cursor.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            exibir_mensagem("Este usuário já está cadastrado!")
            conn.close()
            return
        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_criptografada))
        conn.commit()
        exibir_mensagem("Cadastro realizado com sucesso!")
    
    elif acao == "login":
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND senha = ?", (usuario, senha_criptografada))
        if cursor.fetchone():
            exibir_mensagem(f"Bem-vindo, {usuario}!")
        else:
            exibir_mensagem("Usuário ou senha incorretos.")
    
    conn.close()

def cadastrar():
    usuario_input = usuario.get()
    senha_usuario = senha.get()
    if not usuario_input or not senha_usuario:
        exibir_mensagem("Por favor, preencha ambos os campos!")
    else:
        processar_usuario(usuario_input, senha_usuario, "cadastrar")

def login():
    usuario_input = usuario.get()
    senha_usuario = senha.get()
    if not usuario_input or not senha_usuario:
        exibir_mensagem("Por favor, preencha ambos os campos!")
    else:
        processar_usuario(usuario_input, senha_usuario, "login")

criar_banco_de_dados()

janela = tk.Tk()
janela.geometry("800x500")
janela.title("LOGIN COM TKINTER")

texto = tk.Label(janela, text="CADASTRO E LOGIN", font=("Arial", 16))
texto.pack(padx=10, pady=10)

label_usuario = tk.Label(janela, text="👤USUÁRIO:", font=("Arial", 12))
label_usuario.pack(padx=10, pady=5)

usuario = tk.Entry(janela, font=("Arial", 12), width=30)
usuario.pack(padx=10, pady=10)

label_senha = tk.Label(janela, text="🔒SENHA:", font=("Arial", 12))
label_senha.pack(padx=10, pady=5)

senha = tk.Entry(janela, font=("Arial", 12), width=30, show="*")
senha.pack(padx=10, pady=10)

botao_cadastrar = tk.Button(janela, text="CADASTRAR", font=("Arial", 12), command=cadastrar)
botao_cadastrar.pack(padx=10, pady=10)

botao_login = tk.Button(janela, text="LOGIN", font=("Arial", 12), command=login)
botao_login.pack(padx=10, pady=10)

janela.mainloop()
