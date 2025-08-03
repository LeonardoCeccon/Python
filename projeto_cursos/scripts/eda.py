import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings

# Configurações iniciais
warnings.filterwarnings("ignore", category=UserWarning)  # Ignorar avisos do openpyxl
warnings.filterwarnings("ignore", category=FutureWarning)  # Ignorar avisos futuros do seaborn

sns.set_theme(style="whitegrid", palette="pastel")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['savefig.dpi'] = 300

# Configurar paths
current_dir = Path(__file__).parent
output_dir = current_dir / "../outputs/graficos/"
output_dir.mkdir(parents=True, exist_ok=True)

# Carregar dados
try:
    df = pd.read_excel(
        current_dir / "../data/dadoscursos.xlsx",
        sheet_name="CURSOS",
        engine='openpyxl'  # Especificar engine para evitar warnings
    )
except Exception as e:
    print(f"Erro ao carregar arquivo: {e}")
    exit()

# Verificar colunas essenciais
required_cols = ['CURSO', 'DATA CURSO', 'IMPORTE CLIENTE', 'DURAÇÃO', 'PAÍS']
if not all(col in df.columns for col in required_cols):
    print(f"Erro: Colunas obrigatórias não encontradas. Verifique: {required_cols}")
    exit()

# Análise Inicial
print("\n=== Resumo Estatístico ===")
print(df[['DURAÇÃO', 'IMPORTE CLIENTE', 'IMPORTE PROFESSOR']].describe())

# Gráficos Aprimorados
# Top 10 Cursos (Horizontal)
plt.figure()
top_cursos = df['CURSO'].value_counts().nlargest(10)
ax = sns.barplot(
    x=top_cursos.values,
    y=top_cursos.index,
    palette="pastel",
    orient='h'
)
plt.title('Top 10 Cursos Mais Populares', pad=20)
plt.xlabel('Quantidade de Cursos')
plt.ylabel('')
sns.despine(left=True)
plt.tight_layout()
plt.savefig(output_dir / "popularidade_cursos.png")

# Evolução Anual (com preenchimento)
df['ANO'] = pd.to_datetime(df['DATA CURSO']).dt.year
faturamento_ano = df.groupby('ANO')['IMPORTE CLIENTE'].sum()

plt.figure()
ax = sns.lineplot(
    x=faturamento_ano.index,
    y=faturamento_ano.values,
    marker='o',
    linewidth=2.5,
    color='#4C72B0'
)
plt.fill_between(
    faturamento_ano.index,
    faturamento_ano.values,
    color='#4C72B0',
    alpha=0.1
)
plt.title('Evolução do Faturamento Anual', pad=20)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(output_dir / "faturamento_anual.png")

# 3. Boxplot Modernizado (Top 5)
plt.figure(figsize=(10, 6))
top_5_cursos = df['CURSO'].value_counts().nlargest(5).index
df_top5 = df[df['CURSO'].isin(top_5_cursos)]

ax = sns.boxplot(
    data=df_top5,
    x='DURAÇÃO',
    y='CURSO',
    hue='CURSO',
    palette="pastel",
    legend=False
)
plt.title('Distribuição da Duração por Curso (Top 5)', pad=20)
plt.xlabel('Duração (horas)')
plt.ylabel('')
sns.despine(left=True)
plt.tight_layout()
plt.savefig(output_dir / "duracao_cursos.png")

print(f"\nAnálise concluída! Gráficos salvos em: {output_dir.resolve()}")
