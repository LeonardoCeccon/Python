import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

def executar():
    caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
    caminho_saida = os.path.join('..', 'outputs')
    os.makedirs(caminho_saida, exist_ok=True)

    df = pd.read_excel(caminho_arquivo)

    if 'Ano de Cadastro' not in df.columns:
        df['Ano de Cadastro'] = pd.to_datetime(df['Data de Cadastro']).dt.year

    anos_futuros = np.arange(2026, 2031)
    categorias = df['Categoria'].unique()
    categorias_com_dados = []
    plt.figure(figsize=(12, 6))
    previsoes_dict = {}

    for categoria in categorias:
        df_categoria = df[df['Categoria'] == categoria]
        livros_por_ano = df_categoria.groupby('Ano de Cadastro').size().reset_index(name='Quantidade')
        x = livros_por_ano['Ano de Cadastro'].values.reshape(-1, 1)
        y = livros_por_ano['Quantidade'].values

        if x.size == 0 or y.size == 0 or len(x) < 2:
            print(f"⚠️ Categoria '{categoria}' não possui dados suficientes.")
            continue

        categorias_com_dados.append(categoria)

        modelo = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
        modelo.fit(x, y)

        y_pred_treino = modelo.predict(x)
        r2 = r2_score(y, y_pred_treino)
        rmse = mean_squared_error(y, y_pred_treino) ** 0.53

        todos_os_anos = np.concatenate([x.ravel(), anos_futuros])
        todos_os_anos_ordenado = np.sort(np.unique(todos_os_anos))
        x_todos = todos_os_anos_ordenado.reshape(-1, 1)
        y_predito = modelo.predict(x_todos)

        print(f"\n📘 Previsão de livros para categoria '{categoria}':")
        print(f"- R²: {r2:.3f}")
        print(f"- RMSE: {rmse:.2f}")

        plt.plot(x_todos, y_predito, label=categoria)
        plt.scatter(x, y, alpha=0.6)

        previsoes = []
        for ano in anos_futuros:
            qtd_prevista = modelo.predict(np.array([[ano]]))[0]
            previsoes.append(int(round(qtd_prevista)))
            print(f"  - {ano}: {int(round(qtd_prevista))} livros")

        if len(previsoes) == len(anos_futuros):
            previsoes_dict[categoria] = previsoes

    plt.title('Previsão da quantidade de livros por categoria (2026–2030)')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de livros cadastrados')
    plt.grid(True)

    if categorias_com_dados:
        plt.legend()
        plt.tight_layout()
        grafico_path = os.path.join(caminho_saida, 'livros_por_categoria.png')
        plt.savefig(grafico_path)
        plt.close()
        print(f"\n📊 Gráfico salvo em: {grafico_path}")
    else:
        print("⚠️ Nenhuma categoria com dados suficientes para plotar o gráfico.")

    if previsoes_dict:
        df_previsoes = pd.DataFrame(previsoes_dict, index=anos_futuros)
        df_previsoes.index.name = 'Ano'
        arquivo_excel = os.path.join(caminho_saida, 'previsoes_categorias.xlsx')
        df_previsoes.to_excel(arquivo_excel)
        print(f"📁 Previsões salvas em: {arquivo_excel}")
    else:
        print("⚠️ Nenhuma previsão foi gerada.")
