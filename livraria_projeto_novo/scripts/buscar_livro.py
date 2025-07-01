def buscar_livro(df, campo, valor):
    campos_validos = ['título', 'autor', 'categoria']
    if campo not in campos_validos:
        print(f"Campo inválido! Escolha entre: {', '.join(campos_validos)}.")
        return

    if not valor.strip():
        print("Valor de busca não pode estar vazio!")
        return

    resultados = df[df[campo].str.contains(valor, case=False, na=False)]

    if not resultados.empty:
        print(f"\nLivros encontrados por {campo} contendo '{valor}':")
        print(resultados)
    else:
        print(f"Nenhum livro encontrado para {campo} = '{valor}'")
