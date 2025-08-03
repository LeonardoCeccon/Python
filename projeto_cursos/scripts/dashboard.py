import streamlit as st
from PIL import Image
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import KMeans
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
import warnings

# Configurações iniciais
warnings.filterwarnings("ignore")
plt.style.use('seaborn-v0_8')
sns.set_theme(style="whitegrid", palette="pastel")
st.set_page_config(layout="wide", page_title="Dashboard de Cursos", page_icon="📊")


# Funções auxiliares
@st.cache_data
def carregar_dados():
    try:
        path = Path(__file__).parent.parent / "data" / "dadoscursos.xlsx"
        df = pd.read_excel(path, sheet_name="CURSOS", engine='openpyxl')
        df['DATA CURSO'] = pd.to_datetime(df['DATA CURSO'])
        df['ANO'] = df['DATA CURSO'].dt.year
        df['MES'] = df['DATA CURSO'].dt.month
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()


def carregar_imagem(nome_arquivo):
    try:
        caminho = Path(__file__).parent.parent / "outputs" / "graficos" / nome_arquivo
        return Image.open(caminho)
    except Exception as e:
        st.error(f"Erro ao carregar {nome_arquivo}: {str(e)}")
        return None


def plot_clusters(df):
    cluster_data = df.groupby('CURSO').agg({
        'IMPORTE CLIENTE': 'mean',
        'DURAÇÃO': 'mean',
        'CÓD CURSO': 'count'
    }).rename(columns={'CÓD CURSO': 'FREQUENCIA'})

    if len(cluster_data) < 2:
        st.warning("Não há dados suficientes para clusterização")
        return None

    n_clusters = min(3, len(cluster_data))
    kmeans = KMeans(n_clusters=n_clusters)
    cluster_data['CLUSTER'] = kmeans.fit_predict(cluster_data)

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        cluster_data['FREQUENCIA'],
        cluster_data['IMPORTE CLIENTE'],
        c=cluster_data['CLUSTER'],
        cmap='viridis',
        s=100
    )

    for i, curso in enumerate(cluster_data.index):
        ax.annotate(curso,
                    (cluster_data['FREQUENCIA'][i] + 0.5,
                     cluster_data['IMPORTE CLIENTE'][i]),
                    fontsize=8)

    plt.title("Clusterização de Cursos")
    plt.xlabel("Frequência")
    plt.ylabel("Valor Médio (R$)")
    plt.colorbar(scatter, label='Cluster')
    return fig


def plot_forecast(df):
    ts = df.set_index('DATA CURSO')['IMPORTE CLIENTE'].resample('M').sum()
    model = ARIMA(ts, order=(1, 1, 1)).fit()
    forecast = model.get_forecast(steps=12)

    fig, ax = plt.subplots(figsize=(10, 4))
    ts.plot(ax=ax, label='Histórico')
    forecast.predicted_mean.plot(ax=ax, label='Previsão')
    ax.fill_between(forecast.conf_int().index,
                    forecast.conf_int()['lower IMPORTE CLIENTE'],
                    forecast.conf_int()['upper IMPORTE CLIENTE'],
                    alpha=0.1)
    plt.title("Previsão de Faturamento (12 meses)")
    plt.legend()
    return fig


# Interface principal
st.title("📊 Dashboard Analítico de Cursos")

# Carrega dados
df = carregar_dados()

# Sidebar com filtros
with st.sidebar:
    st.header("🔍 Filtros Interativos")

    # Filtros básicos
    pais = st.selectbox("País", ["Todos"] + list(df['PAÍS'].unique()))
    curso = st.selectbox("Curso", ["Todos"] + list(df['CURSO'].unique()))

    # Filtros temporais
    anos = st.multiselect("Anos", options=sorted(df['ANO'].unique(), reverse=True),
                          default=sorted(df['ANO'].unique(), reverse=True)[0])

    # Filtros numéricos
    min_valor, max_valor = st.slider("Faixa de Valores (R$)",
                                     float(df['IMPORTE CLIENTE'].min()),
                                     float(df['IMPORTE CLIENTE'].max()),
                                     (float(df['IMPORTE CLIENTE'].min()),
                                      float(df['IMPORTE CLIENTE'].max())))

    st.divider()
    st.markdown("**Visualização:**")
    show_interactive = st.checkbox("Mostrar gráfico interativo", True)

# Aplica filtros
filtered_df = df.copy()
if pais != "Todos":
    filtered_df = filtered_df[filtered_df['PAÍS'] == pais]
if curso != "Todos":
    filtered_df = filtered_df[filtered_df['CURSO'] == curso]
if anos:
    filtered_df = filtered_df[filtered_df['ANO'].isin(anos)]
filtered_df = filtered_df[(filtered_df['IMPORTE CLIENTE'] >= min_valor) &
                          (filtered_df['IMPORTE CLIENTE'] <= max_valor)]

# Gráfico interativo
if show_interactive and not filtered_df.empty:
    st.header("📊 Visão Interativa")

    fig = px.scatter(
        filtered_df,
        x='DURAÇÃO',
        y='IMPORTE CLIENTE',
        size='IMPORTE CLIENTE',
        color='CURSO',
        hover_name='CURSO',
        size_max=30,
        labels={
            'DURAÇÃO': 'Duração (horas)',
            'IMPORTE CLIENTE': 'Valor (R$)',
            'CURSO': 'Curso'
        }
    )

    st.plotly_chart(fig, use_container_width=True)

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Análise", "📊 Gráficos", "🧩 Segmentação", "🔮 Previsão"])

with tab1:
    st.header("Análise Temporal")
    monthly = filtered_df.set_index('DATA CURSO')['IMPORTE CLIENTE'].resample('M').sum()
    st.line_chart(monthly)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total de Cursos", filtered_df.shape[0])
    with col2:
        st.metric("Faturamento Médio", f"R${filtered_df['IMPORTE CLIENTE'].mean():.2f}")

with tab2:
    st.header("Visualizações Salvas")

    col1, col2 = st.columns(2)
    with col1:
        img_pop = carregar_imagem("popularidade_cursos.png")
        if img_pop:
            st.image(img_pop, caption="Popularidade dos Cursos", use_container_width=True)

    with col2:
        img_duracao = carregar_imagem("duracao_cursos.png")
        if img_duracao:
            st.image(img_duracao, caption="Duração dos Cursos", use_container_width=True)

with tab3:
    st.header("Segmentação de Cursos")
    cluster_plot = plot_clusters(filtered_df)
    if cluster_plot:
        st.pyplot(cluster_plot)

    img_cluster = carregar_imagem("cluster_cursos.png")

with tab4:
    st.header("Previsões")
    img_previsoes = carregar_imagem("previsao_faturamento.png")
    forecast_plot = plot_forecast(filtered_df)
    if forecast_plot:
        st.pyplot(forecast_plot)


# Rodapé
st.divider()
st.caption("Dashboard desenvolvido para análise de cursos - Leonardo Sanches Ceccon - 2025©")

#para rodar: streamlit run scripts/dashboard.py
