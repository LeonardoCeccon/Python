from sklearn.cluster import KMeans
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Preparação de dados
df = pd.read_excel("../data/dadoscursos.xlsx")
cluster_data = df.groupby('CURSO').agg({
    'IMPORTE CLIENTE': 'mean',
    'DURAÇÃO': 'mean',
    'CÓD CURSO': 'count'  # Frequência
}).rename(columns={'CÓD CURSO': 'FREQUENCIA'})

# Normalizar dados
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
cluster_data_scaled = scaler.fit_transform(cluster_data)

# Clusterização
kmeans = KMeans(n_clusters=3, random_state=42)
cluster_data['CLUSTER'] = kmeans.fit_predict(cluster_data_scaled)

# Visualização com legendas
plt.figure(figsize=(12, 8))
ax = sns.scatterplot(
    data=cluster_data,
    x='FREQUENCIA',
    y='IMPORTE CLIENTE',
    hue='CLUSTER',
    palette='viridis',
    s=100
)

# Legendas
for line in range(len(cluster_data)):
    ax.text(
        x=cluster_data['FREQUENCIA'].iloc[line] + 0.5,
        y=cluster_data['IMPORTE CLIENTE'].iloc[line],
        s=cluster_data.index[line],
        fontsize=8,
        color='black',
        alpha=0.7
    )

plt.title('Clusterização de Cursos - Valor vs. Frequência', pad=20)
plt.xlabel('Frequência de Oferta')
plt.ylabel('Valor Médio (R$)')
plt.legend(title='Cluster')
plt.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()

# Salvar
plt.savefig("../outputs/graficos/cluster_cursos.png", dpi=300, bbox_inches='tight')
