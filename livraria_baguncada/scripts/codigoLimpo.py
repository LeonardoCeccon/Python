# ========================================
# Visualização dos dados com gráficos
# ========================================
import pandas
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

# Carrega novamente o arquivo limpo
df = pd.read_excel("C:Users\lcecc\OneDrive\Desktop\Python\livraria_baguncada\data\livraria_limpa.xlsx")

# ---------- Gráfico de Barras ----------
# Calcula o preço médio por categoria
preco_medio = df.groupby('categoria')['preço'].mean().reset_index()

# Cria gráfico de barras com seaborn
plt.figure(figsize=(10, 6))
sns.barplot(data=preco_medio, x='categoria', y='preço', hue='categoria', palette='Blues_d', legend=False)
plt.title("Preço médio por categoria")
plt.xlabel("Categoria")
plt.ylabel("Preço médio (R$)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---------- Gráfico de Pizza ----------
# Soma total de estoque por categoria
estoque_categoria = df.groupby('categoria')['estoque'].sum()

# Cria gráfico de pizza
plt.figure(figsize=(7, 7))
plt.pie(estoque_categoria, labels=estoque_categoria.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribuição de estoque por categoria")
plt.axis('equal')  # Mantém o formato circular
plt.show()

# ---------- Gráfico de Linha ----------
# Conta quantos livros foram cadastrados por data
cadastros = df['data_de_cadastro'].value_counts().sort_index()

# Cria gráfico de linha mostrando os cadastros ao longo do tempo
plt.figure(figsize=(10, 5))
plt.plot(cadastros.index, cadastros.values, marker='o')
plt.title("Quantidade de livros cadastrados por data")
plt.xlabel("Data")
plt.ylabel("Quantidade de cadastrados")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
