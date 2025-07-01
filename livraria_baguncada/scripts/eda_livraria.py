import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel("C:Users\lcecc\OneDrive\Desktop\Python\livraria_baguncada\data\livraria_limpa.xlsx")

#Limpa espaços extras dos nomes das colunas
df.columns = df.columns.str.strip()

#Boas praticas para verificação de nomenclaturas
print("Colunas disponíveis:", df.columns.tolist())

#Converte colunas numéricas para tipo correto
df['preço'] = pd.to_numeric(df['preço'], errors='coerce')
df['estoque'] = pd.to_numeric(df['estoque'], errors='coerce')
df['páginas'] = pd.to_numeric(df['páginas'], errors='coerce')

#Estatísticas descritivas das colunas numéricas
print("\nESTATÍSTICAS BÁSICAS:")
print(df.describe())

#Calculo de quantidade de cada categoria
print("\nContagem de livros por categoria:")
print(df.categoria.value_counts())

#Calculo de media de preços por categoria
print("\nMedia de preços por categoria:")
print(df.groupby('categoria')["preço"].mean())

#Calculo de estoque por categoria
print("\nEstoque total por categoria:")
print(df.groupby('categoria')["estoque"].sum())

#Média de preço por categoria
media_preco_categoria = df.groupby('categoria')['preço'].mean()

#Grafico em barras
plt.figure(figsize=(8,6))
sns.barplot(x=media_preco_categoria.index, y=media_preco_categoria.values,hue=media_preco_categoria.index, palette='Blues_d')

plt.title('Media de preços por categoria')
plt.xlabel('Categoria')
plt.xlabel('Preço meédio')
plt.xticks(rotation=45)
plt.show()
