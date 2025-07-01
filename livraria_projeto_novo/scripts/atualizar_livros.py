import pandas as pd

def atualizar_livros(df, caminho_arquivo, campo, valor):
    campos_validos = ['titulo', 'autor', 'categoria']

    # Verifica se o campo é válido
    if campo not in campos_validos:
        print(f'Campo inválido. Escolha entre: {", ".join(campos_validos)}')
        return df

    # Remover espaços extras no nome das colunas
    df.columns = df.columns.str.strip()

    # Verificar se a coluna existe no DataFrame
    if campo not in df.columns:
        print(f"A coluna '{campo}' não foi encontrada no DataFrame.")
        return df

    # Filtra os resultados
    resultados = df[df[campo].str.contains(valor, case=False, na=False)]

    if resultados.empty:
        print(f"Nenhum livro foi encontrado para {campo} = {valor}")
        return df

    print(f"\nLivros encontrados para atualização:")
    print(resultados)

    if len(resultados) > 1:
        idx = input("Digite o índice a ser atualizado: ").strip()
        if not idx.isdigit() or int(idx) not in resultados.index:
            print("Índice inválido.")
            return df
        idx = int(idx)
    else:
        idx = resultados.index[0]

    print("Preencha os novos dados:")

    for coluna in ['titulo', 'autor', 'categoria', 'preço', 'estoque', 'paginas']:
        valor_atual = df.at[idx, coluna]
        novo_valor = input(f"{coluna.capitalize()} (atual: {valor_atual}): ").strip()
        if novo_valor:
            try:
                if coluna == 'preço':
                    df.at[idx, coluna] = float(novo_valor)
                elif coluna in ['estoque', 'paginas']:
                    df.at[idx, coluna] = int(novo_valor)
                else:
                    df.at[idx, coluna] = novo_valor
            except ValueError:
                print(f"Valor inválido para {coluna}, mantendo valor atual.")

    nova_data = input("Nova data de cadastro (YYYY-MM-DD) [Enter para manter]: ").strip()
    if nova_data:
        try:
            df.at[idx, 'data_de_cadastro'] = pd.to_datetime(nova_data).date()
        except:
            print("Data inválida, mantendo valor atual.")

    df.to_excel(caminho_arquivo, index=False)
    print(f"\n✅ Livro atualizado com sucesso!")

    return df
