import pandas as pd

def excluir_livro(df, caminho_arquivo, campo, valor):
    campos_validos = ['título', 'autor', 'categoria']
    if campo not in campos_validos:
        print(f"Campo inválido. Escolha entre: {', '.join(campos_validos)}.")
        return df

    if not valor.strip():
        print("Valor de busca não pode estar vazio")
        return df

    resultados = df[df[campo].str.contains(valor, case=False, na=False)]

    if resultados.empty:
        print(f"Nenhum livro encontrado para {campo} = '{valor}'")
        return df

    print(f"\nLivros encontrados para exclusão por {campo} = '{valor}':")
    print(resultados)

    confirmacao = input("\nDeseja excluir esses livros? (s/n): ").strip().lower()
    if confirmacao != "s":
        print("Ação cancelada.")
        return df

    df = df.drop(resultados.index).reset_index(drop=True)
    df.to_excel(caminho_arquivo, index=False)

    print(f"{len(resultados)} Livro(s) excluído(s) com sucesso.")
    return df
