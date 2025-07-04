import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

#Caminhos do arquivo de dados e da pasta de saída
caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
caminho_saida = os.path.join('..', 'outputs')
os.makedirs(caminho_saida, exist_ok=True)

#Carrega os dados do Excel
df = pd.read_excel(caminho_arquivo)

#Garante que a coluna "Ano de Cadastro" exista
if 'Ano de Cadastro' not in df.columns:
    df['Ano de Cadastro'] = pd.to_datetime(df['Data de Cadastro']).dt.year

#Define anos futuros para previsão
anos_futuros = np.arange(2026, 2031)

# Lista todas as categorias únicas
categorias = df['Categoria'].unique()

#Lista para controle de categorias válidas
categorias_com_dados = []

#Prepara gráfico
plt.figure(figsize=(12, 6))

#Dicionário para armazenar previsões por categoria
previsoes_dict = {}

#Para cada categoria, aplicar regressão polinomial
for categoria in categorias:
    #Filtra DataFrame por categoria
    df_categoria = df[df['Categoria'] == categoria]

    #Agrupa por ano e conta a quantidade de livros cadastrados
    livros_por_ano = df_categoria.groupby('Ano de Cadastro').size().reset_index(name='Quantidade')

    #Prepara X e Y para regressão
    x = livros_por_ano['Ano de Cadastro'].values.reshape(-1, 1)
    y = livros_por_ano['Quantidade'].values

    #Verifica se tem dados suficientes
    if x.size == 0 or y.size == 0 or len(x) < 2:
        print(f"⚠️ Categoria '{categoria}' não possui dados suficientes.")
        continue

    #Adiciona à lista de categorias com dados
    categorias_com_dados.append(categoria)

    #Cria modelo de Regressão Polinomial (grau 2)
    modelo = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    modelo.fit(x, y)

    #Concatena anos históricos com futuros
    todos_os_anos = np.concatenate([x.ravel(), anos_futuros])
    todos_os_anos_ordenado = np.sort(np.unique(todos_os_anos))
    x_todos = todos_os_anos_ordenado.reshape(-1, 1)

    #Gera previsões para todos os anos (históricos + futuros)
    y_predito = modelo.predict(x_todos)

    #Plotagem da linha de tendência e dos pontos reais
    plt.plot(x_todos, y_predito, label=categoria)
    plt.scatter(x, y)

    #Gera previsões apenas para anos futuros
    previsoes = []
    print(f"\nPrevisão de livros para categoria '{categoria}':")
    for ano in anos_futuros:
        qtd_prevista = modelo.predict(np.array([[ano]]))[0]
        previsoes.append(int(round(qtd_prevista)))
        print(f"  - {ano}: {int(round(qtd_prevista))} livros")

    #Só adiciona ao dicionário se a lista estiver completa
    if len(previsoes) == len(anos_futuros):
        previsoes_dict[categoria] = previsoes

#Configurações finais do gráfico
plt.title('Previsão da quantidade de livros por categoria (2026–2030)')
plt.xlabel('Ano')
plt.ylabel('Quantidade de livros cadastrados')
plt.grid(True)

#Se houve categorias válidas, salva o gráfico
if categorias_com_dados:
    plt.legend()
    plt.tight_layout()
    grafico_path = os.path.join(caminho_saida, 'livros_por_categoria.png')
    plt.savefig(grafico_path)
    plt.close()
    print(f"\nGráfico salvo em: {grafico_path}")
else:
    print("Nenhuma categoria com dados suficientes para plotar o gráfico.")

#Gera planilha Excel com as previsões
if previsoes_dict:
    df_previsoes = pd.DataFrame(previsoes_dict, index=anos_futuros)
    df_previsoes.index.name = 'Ano'
    arquivo_excel = os.path.join(caminho_saida, 'previsoes_categorias.xlsx')
    df_previsoes.to_excel(arquivo_excel)
    print(f"Previsões salvas em: {arquivo_excel}")
else:
    print("Nenhuma previsão foi gerada.")
