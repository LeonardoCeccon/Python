import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def executar():
    caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
    caminho_saida = os.path.join('..', 'outputs')
    os.makedirs(caminho_saida, exist_ok=True)

    df = pd.read_excel(caminho_arquivo)
    df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro'])
    df['Ano de Cadastro'] = df['Data de Cadastro'].dt.year
    df['Categoria'] = df['Categoria'].str.strip().str.title()  # Normaliza as categorias

    # Preço médio por ano
    preco_medio_por_ano = df.groupby('Ano de Cadastro')['Preço'].mean().reset_index()
    print("\nPreço médio por ano:\n", preco_medio_por_ano)

    # Gráfico 1 - Preço médio por ano
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=preco_medio_por_ano, x='Ano de Cadastro', y='Preço', marker='o', linewidth=2.5)
    plt.title("Preço médio por ano")
    plt.xlabel("Ano")
    plt.ylabel("Preço Médio (R$)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'preco_medio_por_ano.png'))
    plt.close()
    print("Gráfico salvo em outputs/preco_medio_por_ano.png")

    # Gráfico 2 - Tendência de categorias ao longo dos anos
    categorias_por_ano = df.groupby(['Ano de Cadastro', 'Categoria']).size().unstack(fill_value=0)
    print("\nLivros por categoria ao longo dos anos:\n", categorias_por_ano)

    plt.figure(figsize=(12, 6))
    categorias_por_ano.plot(kind='line', marker='o')
    plt.title("Quantidade de Livros por categoria ao longo dos anos")
    plt.xlabel("Ano de cadastro")
    plt.ylabel("Quantidade de Livros")
    plt.grid(True)
    plt.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'categorias_por_ano.png'))
    plt.close()
    print("Gráfico salvo em outputs/categorias_por_ano.png")

    # Regressão Linear - Previsões por categoria
    categorias_para_prever = ['Tecnologia', 'História', 'Ficção', 'Ciência', 'Infantil', 'Não-Ficção',
                              'Literatura Brasileira', 'Arte']
    anos_previstos = np.arange(2025, 2031)

    plt.figure(figsize=(12, 6))
    categorias_com_dados = []

    for categoria in categorias_para_prever:
        cat_df = df[df['Categoria'] == categoria]
        preco_por_ano = cat_df.groupby('Ano de Cadastro')['Preço'].mean().reset_index()
        x = preco_por_ano['Ano de Cadastro'].values.reshape(-1, 1)
        y = preco_por_ano['Preço'].values

        if x.size == 0 or y.size == 0:
            print(f"⚠️ Categoria '{categoria}' não possui dados suficientes.")
            continue

        categorias_com_dados.append(categoria)
        modelo = LinearRegression()
        modelo.fit(x, y)
        previsoes = modelo.predict(anos_previstos.reshape(-1, 1))

        print(f"\n📘 Previsões de preço médio para categoria '{categoria}':")
        for ano, valor in zip(anos_previstos, previsoes):
            print(f"  - {ano}: R$ {valor:.2f}")

        plt.plot(x, modelo.predict(x), label=f'Tendência {categoria}')
        plt.plot(anos_previstos, previsoes, '--', label=f'Previsão {categoria}')
        plt.scatter(anos_previstos, previsoes, s=60)

    plt.title('Previsão do Preço Médio (2025–2030)')
    plt.xlabel('Ano')
    plt.ylabel('Preço Médio (R$)')
    plt.grid(True)
    if categorias_com_dados:
        plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'previsoes_2025_2030.png'))
    plt.close()

    # Regressão Polinomial
    plt.figure(figsize=(12, 6))
    categorias_com_dados = []

    for categoria in categorias_para_prever:
        cat_df = df[df['Categoria'] == categoria]
        preco_por_ano = cat_df.groupby('Ano de Cadastro')['Preço'].mean().reset_index()
        x = preco_por_ano['Ano de Cadastro'].values.reshape(-1, 1)
        y = preco_por_ano['Preço'].values

        if x.size == 0 or y.size == 0:
            print(f"⚠️ Categoria '{categoria}' não possui dados suficientes.")
            continue

        categorias_com_dados.append(categoria)
        modelo = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        modelo.fit(x, y)
        previsoes = modelo.predict(anos_previstos.reshape(-1, 1))

        print(f"\n📘 Previsões polinomiais (grau 2) para categoria '{categoria}':")
        for ano, valor in zip(anos_previstos, previsoes):
            print(f"  - {ano}: R$ {valor:.2f}")

        x_todos = np.concatenate([x, anos_previstos.reshape(-1, 1)])
        x_todos_ordenado = np.sort(np.unique(x_todos), axis=0)
        y_todos_pred = modelo.predict(x_todos_ordenado.reshape(-1, 1))

        plt.plot(x_todos_ordenado, y_todos_pred, label=f'Curva {categoria}')
        plt.scatter(x, y, label=f'Dados {categoria}')
        plt.scatter(anos_previstos, previsoes, s=60)

    plt.title('Previsão Polinomial do Preço Médio (2025–2030)')
    plt.xlabel('Ano')
    plt.ylabel('Preço Médio (R$)')
    plt.grid(True)
    if categorias_com_dados:
        plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(caminho_saida, 'previsoes_polinomial_2025_2030.png'))
    plt.close()
