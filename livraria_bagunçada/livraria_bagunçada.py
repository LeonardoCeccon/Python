import pandas as pd
import os
print(os.getcwd())

from pandas.plotting import autocorrelation_plot

import pandas as pd

df = pd.read_excel("livraria_baguncada.xlsx")
print(df.head())
print(df.isnull().sum())

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

df['autor'] = df['categoria'].astype(str).str.strip().str.title()
df['categoria'] = df['categoria'].str.strip().str.title()
df.replace(["", "none", "nan"], pd.NA, inplace=True)

df['preço'] = pd.to_numeric(df['preço'], errors='coerce')
df['estoque'] = pd.to_numeric(df['estoque'], errors='coerce')
df['páginas'] = pd.to_numeric(df['páginas'], errors='coerce')
df['data_de_cadastro'] = pd.to_datetime(df['data_de_cadastro'], errors='coerce')

df['estoque'] = df['estoque'].fillna(0)
df.dropna(subset=['autor','preço'], inplace=True)

df = df[df['preço'] >= 30]
df = df[df['estoque'] > 0]
df = df[df['categoria'].notnull()]

df.to_excel("livraria_limpa.xlsx")

#no terminal: pip install matplotlib seaborn plotly

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Bar Graph - Avr. price by tag
df = pd.read_excel("livraria_limpa.xlsx")

preco_medio = df.groupby('categoria')['preço'].mean().reset_index()

plt.figure(figsize = (10,6))
sns.barplot(data=preco_medio, x='categoria', y='preço', hue='categoria', palette='Blues_d', legend=False)
plt.title("Preço medio por categoria")
plt.xlabel("Categoria")
plt.xlabel("Preço medio (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#Pie Grap - Total stock by tag
estoque_categoria = df.groupby('categoria')['estoque'].sum()

plt.figure(figsize = (7,7))
plt.pie(estoque_categoria, labels=estoque_categoria.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribuição de estoque por categoria")
plt.axis('equal')
plt.show()

#Line Graph - N° of registers by date
cadastros = df['data_de_cadastro'].value_counts().sort_index()

plt.figure(figsize = (10,5))
plt.plot(cadastros.index, cadastros.values, marker='o')
plt.title("Quantidade de livros cadastrados por data")
plt.xlabel("Data")
plt.ylabel("Quantidade de cadastrados")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
