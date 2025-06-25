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
