import os
import sys
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Usa backend sem interface gráfica
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def executar():
    # Define o diretório base dependendo se está rodando como .exe ou .py
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS  # Usado por PyInstaller
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    # Caminho do arquivo Excel fora do .exe
    caminho_arquivo = os.path.join(base_dir, '..', 'data', 'livraria_estoque.xlsx')
    caminho_saida = os.path.join(base_dir, '..', 'outputs')
    os.makedirs(caminho_saida, exist_ok=True)

    # (opcional) Grava log para debug
    try:
        with open(os.path.join(caminho_saida, 'log_clustering.txt'), 'w') as f:
            f.write(f"base_dir: {base_dir}\n")
            f.write(f"caminho_arquivo: {caminho_arquivo}\n")
    except:
        pass

    # Lê os dados
    try:
        df = pd.read_excel(caminho_arquivo)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {caminho_arquivo}")
        return
    except Exception as e:
        print(f"❌ Erro ao abrir o arquivo Excel: {e}")
        return

    # Processamento
    if 'Ano de Cadastro' not in df.columns:
        df['Ano de Cadastro'] = pd.to_datetime(df['Data de Cadastro']).dt.year

    dados = df[['Ano de Cadastro', 'Preço']].dropna()

    scaler = StandardScaler()
    dados_escalados = scaler.fit_transform(dados)

    modelo = KMeans(n_clusters=3, random_state=42, n_init=10)
    modelo.fit(dados_escalados)
    df['Cluster'] = modelo.labels_

    # Gráfico
    plt.figure(figsize=(10, 6))
    cores = ['red', 'green', 'blue']
    for cluster_id in range(3):
        grupo = df[df['Cluster'] == cluster_id]
        plt.scatter(grupo['Ano de Cadastro'], grupo['Preço'],
                    color=cores[cluster_id], alpha=0.6, label=f'Cluster {cluster_id}')

    # Centroides
    centroides = scaler.inverse_transform(modelo.cluster_centers_)
    plt.scatter(
        centroides[:, 0],
        centroides[:, 1],
        marker='*',
        s=300,
        c='gold',
        label='Centróides',
        edgecolor='k',
        linewidth=0.8
    )

    plt.title('Clusters de livros por preço e ano de cadastro')
    plt.xlabel('Ano de Cadastro')
    plt.ylabel('Preço (R$)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    grafico_path = os.path.join(caminho_saida, 'clusters_livros.png')
    plt.savefig(grafico_path)
    plt.close()

    print(f"📊 Gráfico de clusters salvo em: {grafico_path}")
