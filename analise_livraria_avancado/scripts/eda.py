import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from matplotlib.pyplot import savefig

caminho_arquivo = os.path.join('..', 'data', 'livraria_estoque.xlsx')
caminho_saida = os.path.join('..', 'outputs')
os.makedirs(caminho_saida, exist_ok=True)
df = pd.read_excel(caminho_arquivo)

#EDA
print(df.head())
print("Formato", df.shape)
print("Tipos de dados:\n", df.dtypes)
print("Valores ausentes:\n,", df.isnull().sum())
print("\nEstatisticas dos preços:\n", df['Preço'].describe())
print("\nCadastro entre: ", df['Data de Cadastro'].min(), "e", df['Data de Cadastro'].max())
print("\nLivros por categoria: \n", df['Categoria'].value_counts())
df['Ano de cadastro'] = df['Data de Cadastro'].dt.year

#===Gráficos===

#Historico de preços
plt.figure(figsize = (10,5))
sns.histplot(df['Preço'], bins= 30, kde=True, color = 'skyblue')
plt.title("Distribuilção de preços")
plt.xlabel("Preço (R$)")
plt.ylabel("Quantidade")
plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'distribuição_precos.png'))
plt.close()

#Contagem por categoria
plt.figure(figsize = (10,5))
sns.countplot(data=df, x='Categoria', hue='Categoria', order=df['Categoria'].value_counts().index, palette="Set2", legend=False)
plt.title("Quantidade de livros por categoria")
plt.xticks(rotation=45)
plt.title("Quantidade")
plt.tight_layout()
plt.savefig(os.path.join(caminho_saida, 'livros_por_categoria.png'))
plt.close()

#Cadastros por ano
plt.figure(figsize = (10,5))
sns.countplot(data=df, x='Ano de cadastro', hue='Ano de cadastro', palette="coolwarm", legend=False)
plt.title("Livros cadastrados por ano")
plt.ylabel("Quantidade")
plt.tight_layout()
savefig(os.path.join(caminho_saida, 'Cadastros_por_ano.png'))
plt.close()

print("Analises salvas na pasta outputs")