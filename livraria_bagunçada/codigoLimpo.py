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

#Pie Graph- Total stock by tag
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
