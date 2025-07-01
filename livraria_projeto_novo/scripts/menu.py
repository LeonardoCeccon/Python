import pandas as pd
from adicionar_livro import adicionar_livro
from buscar_livro import buscar_livro
from excluir_livro import excluir_livro
from atualizar_livros import atualizar_livros

import pandas as pd

# Caminho do arquivo Excel
caminho_arquivo = "../data/livros_dados.xlsx"

# Carregar o DataFrame
df = pd.read_excel(caminho_arquivo)

def menu():
    global df  # Define df como global para garantir que a variável seja acessada corretamente em todas as funções

    while True:
        print("=====MENU=====")
        print("1. Adicionar livro")
        print("2. Buscar livro")
        print("3. Excluir livro")
        print("4. Atualizar livro")
        print("5. Sair do programa")

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            # Adicionar livro
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            categoria = input("Categoria: ").strip()
            estoque = int(input("Estoque: "))
            preco = float(input("Preço: "))
            paginas = int(input("Número de páginas: "))
            # Função para adicionar livro
            df = adicionar_livro(df, caminho_arquivo, titulo, autor, categoria, estoque, preco, paginas)

        elif escolha == "2":
            # Buscar livro
            campo = input("Buscar por (título / autor / categoria): ").strip().lower()
            if campo == "autor":
                valor = input("Quem é o autor? ").strip()
            elif campo == "titulo":
                valor = input("Qual é o título? ").strip()
            elif campo == "categoria":
                valor = input("Qual é a categoria? ").strip()
            else:
                print("Campo inválido! Escolha entre 'título', 'autor', ou 'categoria'.")
                continue
            # Função para buscar livro
            df = buscar_livro(df, campo, valor)

        elif escolha == "3":
            # Excluir livro
            campo = input("Excluir por (título / autor / categoria): ").strip().lower()
            if campo == "autor":
                valor = input("Quem é o autor? ").strip()
            elif campo == "titulo":
                valor = input("Qual é o título? ").strip()
            elif campo == "categoria":
                valor = input("Qual é a categoria? ").strip()
            else:
                print("Campo inválido! Escolha entre 'título', 'autor', ou 'categoria'.")
                continue
            # Função para excluir livro
            df = excluir_livro(df, caminho_arquivo, campo, valor)

        elif escolha == "4":
            # Atualizar livro
            campo = input("Atualizar por (título / autor / categoria): ").strip().lower()
            if campo == "autor":
                valor = input("Quem é o autor? ").strip()
            elif campo == "titulo":
                valor = input("Qual é o título? ").strip()
            elif campo == "categoria":
                valor = input("Qual é a categoria? ").strip()
            else:
                print("Campo inválido! Escolha entre 'título', 'autor', ou 'categoria'.")
                continue
            # Função para atualizar livro
            df = atualizar_livros(df, caminho_arquivo, campo, valor)

        elif escolha == "5":
            # Sair
            print("Saindo...")
            break

        else:
            print("Opção inválida! Tente novamente.")


# Inicia o menu principal
if __name__ == "__main__":
    menu()
