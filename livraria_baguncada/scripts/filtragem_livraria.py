import pandas as pd

# Carrega os dados limpos
ddf = pd.read_excel("C:Users\lcecc\OneDrive\Desktop\Python\livraria_baguncada\data\livraria_limpa.xlsx")

# Confirma que está tudo certo
print(df.head())

# Fitro de livros com menos de 100 paginas
livros_pequenos = df[df['páginas'] < 100]
print("\nLivros com menos de 100 paginas:")
print(livros_pequenos)
