from datetime import datetime
import pandas as pd

def adicionar_livro(df, caminho_arquivo, titulo, autor, categoria, estoque, preco, paginas=None, data_de_cadastro=None):
    if not titulo or not autor or not categoria:
        print("Título, autor e categoria são obrigatórios")
        return df

    if not isinstance(estoque, int) or estoque < 0:
        print("Estoque deve ser um número inteiro não negativo")
        return df

    if not isinstance(preco, (int, float)) or preco < 0:
        print("Preço deve ser um número positivo")
        return df

    if paginas is None or not isinstance(paginas, int) or paginas <= 0:
        print("Número de páginas deve ser informado e maior que zero!")
        return df

    if not data_de_cadastro:
        data_cadastro_formatada = datetime.today().date()
    else:
        try:
            data_cadastro_formatada = pd.to_datetime(data_de_cadastro).date()
        except:
            print("Data inválida! Use o formato AAAA-MM-DD.")
            return df

    novo_livro = {
        "título": titulo,
        "autor": autor,
        "categoria": categoria,
        "preço": float(preco),
        "estoque": int(estoque),
        "páginas": int(paginas),
        "data_de_cadastro": data_cadastro_formatada
    }

    df = pd.concat([df, pd.DataFrame([novo_livro])], ignore_index=True)
    df.to_excel(caminho_arquivo, index=False)
    print(f"\n✅ Livro '{titulo}' adicionado com sucesso!")

    return df
