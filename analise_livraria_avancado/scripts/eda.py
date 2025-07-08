import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.pyplot import savefig

def executar():
    # Caminho do arquivo de dados
    caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
    caminho_saida = os.path.join('..', 'outputs')
    os.makedirs(caminho_saida, exist_ok=True)

    # Carregar os dados
    df = pd.read_excel(caminho_arquivo)

    # EDA - Análise Exploratória de Dados
    print(df.head())
    print("Formato", df.shape)
    print("Tipos de dados:\n", df.dtypes)
    print("Valores ausentes:\n", df.isnull().sum())
    print("\nEstatísticas dos preços:\n", df['Preço'].describe())
    print("\nCadastro entre: ", df['Data de Cadastro'].min(), "e", df['Data de Cadastro'].max())
    print("\nLivros por categoria: \n", df['Categoria'].value_counts())

    # Criação da coluna "Ano de cadastro"
    df['Ano de cadastro'] = df['Data de Cadastro'].dt.year

    #=== Gráficos ===

    # Gráfico de distribuição de preços
    plt.figure(figsize=(10, 5))
    sns.histplot(df['Preço'], bins=30, kde=True, color='skyblue')
    plt.title("Distribuição de Preços")
    plt.xlabel("Preço (R$)")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'distribuicao_precos.png'))
    plt.close()

    # Gráfico de contagem por categoria
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='Categoria', hue='Categoria', order=df['Categoria'].value_counts().index, palette="Set2", legend=False)
    plt.title("Quantidade de Livros por Categoria")
    plt.xticks(rotation=45)
    plt.ylabel("Quantidade")
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'livros_por_categoria.png'))
    plt.close()

    # Gráfico de cadastros por ano
    plt.figure(figsize=(10, 5))
    sns.countplot(data=df, x='Ano de cadastro', hue='Ano de cadastro', palette="coolwarm", legend=False)
    plt.title("Livros Cadastrados por Ano")
    plt.ylabel("Quantidade")
    plt.tight_layout()
    savefig(os.path.join(caminho_saida, 'cadastros_por_ano.png'))
    plt.close()

    print("Análises salvas na pasta outputs")
