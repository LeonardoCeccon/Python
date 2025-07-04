import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
caminho_saida = os.path.join('..', 'outputs')
os.makedirs(caminho_saida, exist_ok=True)
df = pd.read_excel(caminho_arquivo)
df['Data de Cadastro'] = pd.to_datetime(df['Data de Cadastro'])
df['Ano de Cadastro'] = df['Data de Cadastro'].dt.year

#Preço médio por ano
preco_medio_por_ano = df.groupby('Ano de Cadastro')['Preço'].mean().reset_index()
print("\nPreço médio por ano : \n,", preco_medio_por_ano)

#Grafico
plt.figure(figsize = (10,5))
sns.lineplot(data=preco_medio_por_ano, x='Ano de Cadastro', y='Preço', marker='o',linewidth=2.5)
plt.title("Preço médio por ano")
plt.xlabel("Ano")
plt.xlabel("Preço Méddio (R$)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'preco_medio_por_ano.png'))
plt.close()

print("Grafico salvo em outputs/preço_medio_por_ano.png")

#Tendencias de categorias ao longo dos anos
categorias_por_ano = df.groupby(['Ano de Cadastro', 'Categoria']).size().unstack(fill_value=0)
print("\nLivros por categoria ao longo dos anos")
print(categorias_por_ano)

#Grafico
plt.figure(figsize = (12,6))
categorias_por_ano.plot(kind='line', marker= 'o')
plt.title("Quantidade de Livros por categoria ao longo dos anos")
plt.xlabel("Ano de cadastro")
plt.ylabel("Quantidade de Livros")
plt.grid(True)
plt.legend(title='Categoria', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'categorias_por_ano.png'))
plt.close()

print("Grafico de categorias por ano salvo em outputs/categorias_por_ano.png")

#Normaliza as categorias no DataFrame
df['Categoria'] = df['Categoria'].str.strip().str.title()

#Categorias para prever(regressão linear)
categorias_para_prever = ['Tecnologia', 'História', 'Ficção', 'Ciência', 'Infantil', 'Não-Ficção',
 'Literatura Brasileira', 'Arte']
anos_previstos = np.arange(2025, 2031)  # de 2025 até 2030 inclusive

plt.figure(figsize=(12, 6))

#Controle para saber se alguma categoria foi plotada
categorias_com_dados = []

for categoria in categorias_para_prever:
    #Filtra livros da categoria atual
    cat_df = df[df['Categoria'] == categoria]

    #Calcula o preço médio por ano
    preco_por_ano = cat_df.groupby('Ano de Cadastro')['Preço'].mean().reset_index()

    #Prepara dados para regressão
    x = preco_por_ano['Ano de Cadastro'].values.reshape(-1, 1)
    y = preco_por_ano['Preço'].values

    #Verifica se há dados suficientes
    if x.size == 0 or y.size == 0:
        print(f"⚠️ Categoria '{categoria}' não possui dados suficientes para previsão.")
        continue
    else:
        categorias_com_dados.append(categoria)

    #Treina o modelo
    modelo = LinearRegression()
    modelo.fit(x, y)

    #Faz previsões para 2025–2030
    previsoes = modelo.predict(anos_previstos.reshape(-1, 1))
    print(f"\n📘 Previsões de preço médio para categoria '{categoria}':")
    for ano, valor in zip(anos_previstos, previsoes):
        print(f"  - {ano}: R$ {valor:.2f}")

    # Plota linha de tendência com dados atuais
    plt.plot(x, modelo.predict(x), label=f'Tendência {categoria}')

    # Plota linha pontilhada com previsões
    plt.plot(anos_previstos, previsoes, '--', label=f'Previsão {categoria} (2025–2030)')

    # Plota pontos previstos
    plt.scatter(anos_previstos, previsoes, s=60)

#Gráfico
plt.title('Previsão do Preço Médio (2025–2030)')
plt.xlabel('Ano')
plt.ylabel('Preço Médio (R$)')
plt.grid(True)

#Só exibe a legenda se houver categorias com dados
if categorias_com_dados:
    plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'previsoes_2025_2030.png'))
plt.close()

print(df['Categoria'].unique())

#Categorias para prever(regressão polinomial)
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
    else:
        categorias_com_dados.append(categoria)

    #Pipeline com transformação polinomial + regressão
    modelo = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
    modelo.fit(x, y)

    previsoes = modelo.predict(anos_previstos.reshape(-1, 1))

    #Mostra as previsões no terminal
    print(f"\n📘 Previsões polinomiais (grau 2) para categoria '{categoria}':")
    for ano, valor in zip(anos_previstos, previsoes):
        print(f"  - {ano}: R$ {valor:.2f}")

    #Plota a curva ajustada nos dados reais
    x_todos = np.concatenate([x, anos_previstos.reshape(-1, 1)])
    x_todos_ordenado = np.sort(np.unique(x_todos), axis=0)
    y_todos_pred = modelo.predict(x_todos_ordenado.reshape(-1, 1))

    plt.plot(x_todos_ordenado, y_todos_pred, label=f'Curva {categoria}')
    plt.scatter(x, y, label=f'Dados {categoria}')
    plt.scatter(anos_previstos, previsoes, s=60)

#Gráfico final
plt.title('Previsão Polinomial do Preço Médio (2025–2030)')
plt.xlabel('Ano')
plt.ylabel('Preço Médio (R$)')
plt.grid(True)

if categorias_com_dados:
    plt.legend()

plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'previsoes_polinomial_2025_2030.png'))
plt.close()