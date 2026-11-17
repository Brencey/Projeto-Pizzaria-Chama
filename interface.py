import customtkinter as ctk
from tkinter import messagebox
from supabase import create_client

# Criando conexão com banco de dados supabase
URL = "https://pgosxbgipxvmhrqiglme.supabase.co"
KEY = "sb_publishable_vADNI49osRfrEBdCO9K3SQ_C_EjMo3i"

supabase = create_client(URL, KEY)


# Configurações
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

AMARELO = "#FFC928"
LARANJA = "#F28C28"
PRETO = "#242424"
BRANCO = "#FFFFFF"

carrinho = []
total = 0
nome_pizza = []
total_conta = 0.0
nome = ""
cpf = ""

# Cardápio
cardapio = {
    "Calabresa": 39.90,
    "Mussarela": 60.00,
    "Frango com Catupiry": 44.90,
    "Portuguesa": 50.00,
    "Quatro Queijos": 46.90,
    "PATO FRITO": 900.00
}

def janela_principal():
    firstFrame.destroy()

    # Janela principal
    app = firstApp
    app.title("CHAMA | Pizzaria")
    app.geometry("900x750")
    app.configure(fg_color=AMARELO)

    # Cabeçalho
    titulo = ctk.CTkLabel(
        app,
        text="🔥 CHAMA PIZZARIA 🍕",
        font=("Arial", 32, "bold"),
        text_color=PRETO
    )
    titulo.pack(pady=20)

    subtitulo = ctk.CTkLabel(
        app,
        text="A paixão pela pizza começa aqui!",
        font=("Arial", 16),
        text_color=PRETO
    )
    subtitulo.pack()

    frame = ctk.CTkFrame(app, fg_color=BRANCO)
    frame.pack(pady=25, padx=30, fill="both", expand=True)

    ctk.CTkLabel(
        frame,
        text="🍕 NOSSO CARDÁPIO",
        font=("Arial", 23, "bold"),
        text_color=PRETO
    ).pack(pady=15)

    lista = ctk.CTkFrame(frame, fg_color="transparent")
    lista.pack()

    # Carrinho
    ctk.CTkLabel(
        frame,
        text="🛒 SEU PEDIDO",
        font=("Arial", 20, "bold"),
        text_color=PRETO
    ).pack(pady=10)

    pedidos = ctk.CTkLabel(
        frame,
        text="Seu carrinho está vazio.",
        font=("Arial", 14),
        text_color=PRETO
    )
    pedidos.pack()

    valor = ctk.CTkLabel(
        frame,
        text="Total: R$ 0.00",
        font=("Arial", 20, "bold"),
        text_color=PRETO
    )
    valor.pack(pady=10)

    def adicionar(nome, preco):
        carrinho.append((nome, preco))
        atualizar_carrinho()

        global nome_pizza
        nome_pizza.append((nome))

    def atualizar_carrinho():
        global total
        total = sum(preco for nome, preco in carrinho)

        texto = "\n".join(
            [f"{nome} - R$ {preco:.2f}" for nome, preco in carrinho]
        )

        pedidos.configure(
            text=texto if texto else "Seu carrinho está vazio."
        )

        valor.configure(text=f"Total: R$ {total:.2f}")

    for nome, preco in cardapio.items():
        linha = ctk.CTkFrame(lista, fg_color="transparent")
        linha.pack(fill="x", pady=5)

        ctk.CTkLabel(
            linha,
            text=f"{nome} - R$ {preco:.2f}",
            font=("Arial", 16),
            text_color=PRETO,
            width=280,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            linha,
            text="Adicionar +",
            fg_color=AMARELO,
            hover_color=LARANJA,
            text_color=PRETO,
            command=lambda n=nome, p=preco: adicionar(n, p)
        ).pack(side="right", padx=10)


    def finalizar():
        if not carrinho:
            messagebox.showwarning("CHAMA", "Adicione uma pizza primeiro!")
            return

        messagebox.showinfo(
            "CHAMA",
            f"Pedido realizado!\nTotal: R$ {total:.2f}"
        )
        global total_conta
        total_conta = total

        carrinho.clear()
        atualizar_carrinho()

    ctk.CTkButton(
        frame,
        text="FINALIZAR PEDIDO",
        fg_color=PRETO,
        hover_color=LARANJA,
        text_color=BRANCO,
        font=("Arial", 16, "bold"),
        command=finalizar
    ).pack(pady=15)


#Tela de Cadastro de Dados
firstApp =  ctk.CTk()
firstApp.title("Cadastro")
firstApp.geometry("500x450")
firstApp.configure(fg_color=AMARELO)
firstApp.resizable(False, False)

firstFrame = ctk.CTkFrame(firstApp, fg_color=BRANCO)
firstFrame.pack(pady=25, padx=30, fill="both", expand=True)


firstTitulo = ctk.CTkLabel(
    firstFrame,
    text="Digite seus dados",
    font=("Arial", 30, "bold")
)
firstTitulo.pack(pady=(55,20))

firstNome = ctk.CTkEntry(
    firstFrame,
    placeholder_text="Nome Completo",
    width= 300,
    height= 60
)
firstNome.pack(pady=10)

def entry_numero(valor):
    return valor.isdigit() and len(valor) <= 11 or valor == ""

firstCPF = ctk.CTkEntry(
    firstFrame,
    placeholder_text="CPF",
    validate="key",
    validatecommand=(firstFrame.register(entry_numero),"%P"),
    width= 300,
    height= 60
)
firstCPF.pack(pady=10)

def verificar():
    nome_user = firstNome.get()
    CPF_user = firstCPF.get()

    global nome
    global cpf

    nome = nome_user
    cpf = CPF_user

    if not nome_user or not CPF_user:
        messagebox.showwarning(
            "INVALID",
            "PREENCHA TODOS OS CAMPOS!!!!!"
        )
        return
    janela_principal()

firstBotao = ctk.CTkButton(
    firstFrame,
    text="ENVIAR",
    fg_color=AMARELO,
    hover_color=LARANJA,
    text_color=PRETO,
    width=280,
    height=40,
    command=verificar
)
firstBotao.pack(pady=10)

firstApp.mainloop()

#Inserindo dados do pedido no banco de dados Supabase
supabase.table("pedidos").insert({
   "Nome": nome,
   "Pizza": nome_pizza,
   "Total": total_conta,
   "CPF": cpf
}).execute()
