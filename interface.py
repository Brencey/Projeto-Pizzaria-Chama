
import customtkinter as ctk
from tkinter import messagebox

# Configurações
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

AMARELO = "#FFC928"
LARANJA = "#F28C28"
PRETO = "#242424"
BRANCO = "#FFFFFF"

# Janela principal
app = ctk.CTk()
app.title("CHAMA | Pizzaria")
app.geometry("900x650")
app.configure(fg_color=AMARELO)

carrinho = []
total = 0

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

# Cardápio
cardapio = {
    "Calabresa": 36.90,
    "Quatro Queijos": 42.90,
    "Frango com Catupiry": 39.90,
    "Portuguesa": 38.90,
    "Margherita": 34.90
}

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

def adicionar(nome, preco):
    carrinho.append((nome, preco))
    atualizar_carrinho()

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

def finalizar():
    if not carrinho:
        messagebox.showwarning("CHAMA", "Adicione uma pizza primeiro!")
        return

    messagebox.showinfo(
        "CHAMA",
        f"Pedido realizado!\nTotal: R$ {total:.2f}"
    )

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

app.mainloop()
