import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np

# Configurações
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Carregar dados
current_dir = Path(__file__).parent
df = pd.read_excel(current_dir / "../data/dadoscursos.xlsx", sheet_name="CURSOS", engine='openpyxl')

# Análise Temporal Detalhada
df['DATA'] = pd.to_datetime(df['DATA CURSO'])
df['MES_ANO'] = df['DATA'].dt.to_period('M')

# Agrupar por mês
faturamento_mensal = df.groupby('MES_ANO')['IMPORTE CLIENTE'].sum().reset_index()
faturamento_mensal['MES_ANO'] = faturamento_mensal['MES_ANO'].dt.to_timestamp()

# Identificação de Anomalias (Método estatistico)
media = faturamento_mensal['IMPORTE CLIENTE'].mean()
std = faturamento_mensal['IMPORTE CLIENTE'].std()
limite_superior = media + 3 * std

anomalias = faturamento_mensal[faturamento_mensal['IMPORTE CLIENTE'] > limite_superior]
print("\n=== Anomalias Detectadas ===")
print(anomalias.to_string())

# Gráfico Detalhado
plt.figure()
ax = sns.lineplot(
    data=faturamento_mensal,
    x='MES_ANO',
    y='IMPORTE CLIENTE',
    marker='o',
    color='#4C72B0'
)

# Destacar anomalias
ax.scatter(
    anomalias['MES_ANO'],
    anomalias['IMPORTE CLIENTE'],
    color='red',
    s=100,
    label='Anomalias'
)

plt.axhline(limite_superior, color='red', linestyle='--', label='Limite de Anomalia (3σ)')
plt.title('Faturamento Mensal com Anomalias Destacadas', pad=20)
plt.xlabel('Data')
plt.ylabel('Faturamento')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()

# Salvar gráfico
output_dir = current_dir / "../outputs/graficos/"
output_dir.mkdir(exist_ok=True)
plt.savefig(output_dir / "anomalias_faturamento.png", dpi=300)
plt.close()

# Investigar os registros específicos
if not anomalias.empty:
    meses_anomalos = anomalias['MES_ANO'].dt.to_period('M')
    registros_anomalos = df[df['MES_ANO'].isin(meses_anomalos)].sort_values('IMPORTE CLIENTE', ascending=False)

    print("\n=== Registros Completos das Anomalias ===")
    print(registros_anomalos[['DATA', 'CURSO', 'IMPORTE CLIENTE', 'CLIENTE', 'PAÍS']].to_string())

    # Exportar para análise
    registros_anomalos.to_csv(output_dir / "registros_anomalos.csv", index=False)
    print(f"\n✅ Registros anomalos exportados para: {output_dir / 'registros_anomalos.csv'}")

print(f"\nAnálise concluída! Gráfico salvo em: {output_dir / 'anomalias_faturamento.png'}")
