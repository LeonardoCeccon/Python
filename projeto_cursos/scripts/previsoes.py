import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pathlib import Path
import warnings

# Configurações
warnings.filterwarnings("ignore")
plt.style.use('seaborn-v0_8')

# Configurar paths
current_dir = Path(__file__).parent
data_path = current_dir / "../data/dadoscursos.xlsx"
output_dir = current_dir / "../outputs/graficos/"
output_dir.mkdir(parents=True, exist_ok=True)

# 1. Carregar e preparar os dados
try:
    df = pd.read_excel(data_path, sheet_name="CURSOS", engine='openpyxl')
    if 'DATA CURSO' not in df.columns:
        raise KeyError("Coluna 'DATA CURSO' não encontrada no arquivo")

    df['DATA'] = pd.to_datetime(df['DATA CURSO'])
    ts_data = df.set_index('DATA')['IMPORTE CLIENTE'].resample('M').sum()

except Exception as e:
    print(f"Erro ao processar os dados: {e}")
    exit()

# 2. Modelagem ARIMA
try:
    model = ARIMA(ts_data, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.get_forecast(steps=12)
    forecast_mean = forecast.predicted_mean
    conf_int = forecast.conf_int()

except Exception as e:
    print(f"Erro na modelagem ARIMA: {e}")
    exit()

# 3. Visualização (APENAS CORES ALTERADAS AQUI)
plt.figure(figsize=(12, 6))
# Histórico - Azul original
plt.plot(ts_data, label='Histórico', color='#4C72B0', linewidth=2)

# Previsão - Mudado para verde escuro (#2ca02c)
plt.plot(forecast_mean, label='Previsão ARIMA', color='#2ca02c', linewidth=2, linestyle='--')

# Intervalo de confiança - Verde claro (#98df8a)
plt.fill_between(
    conf_int.index,
    conf_int.iloc[:, 0],
    conf_int.iloc[:, 1],
    color='#98df8a',
    alpha=0.3
)

# Configurações do gráfico
plt.title('Previsão de Faturamento Mensal (ARIMA)', pad=20)
plt.xlabel('Data')
plt.ylabel('Faturamento')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvar gráfico
plt.savefig(output_dir / "previsao_faturamento.png", dpi=300)
print(f"✅ Previsão concluída! Gráfico salvo em: {output_dir / 'previsao_faturamento.png'}")

forecast_df = pd.DataFrame({
    'Data': forecast_mean.index,
    'Previsão': forecast_mean.values,
    'Limite Inferior': conf_int.iloc[:, 0],
    'Limite Superior': conf_int.iloc[:, 1]
})
forecast_df.to_csv(output_dir / "previsao_dados.csv", index=False)