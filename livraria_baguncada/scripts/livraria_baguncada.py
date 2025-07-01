import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt

print(os.getcwd())

#Carrega a planilha original da livraria
df = pd.read_excel("C:/Users/lcecc/OneDrive/Desktop/Python/livraria_baguncada/data/livraria_baguncada'.xlsx")

print(df.head())

#Verifica a quantidade de valores ausentes por coluna
print(df.isnull().sum())

#Formatação de colunas
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df['autor'] = df['categoria'].astype(str).str.strip().str.title()
df['categoria'] = df['categoria'].str.strip().str.title()
df.replace(["", "none", "nan"], pd.NA, inplace=True)

#Converte colunas numéricas para tipo numérico (valores inválidos viram NaN)
df['preço'] = pd.to_numeric(df['preço'], errors='coerce')
df['estoque'] = pd.to_numeric(df['estoque'], errors='coerce')
df['páginas'] = pd.to_numeric(df['páginas'], errors='coerce')

#Converte a coluna de datas para o tipo datetime
df['data_de_cadastro'] = pd.to_datetime(df['data_de_cadastro'], errors='coerce')

#Preenche valores ausentes em estoque com 0
df['estoque'] = df['estoque'].fillna(0)

# Remove linhas que não têm autor ou preço definido
df.dropna(subset=['autor', 'preço'], inplace=True)

# Filtra: mantém apenas livros com preço >= 30, estoque > 0 e categoria não nula
df = df[df['preço'] >= 30]
df = df[df['estoque'] > 0]
df = df[df['categoria'].notnull()]

# Salva a base de dados tratada em um novo arquivo Excel
df.to_excel("livraria_limpa.xlsx", index=False)
