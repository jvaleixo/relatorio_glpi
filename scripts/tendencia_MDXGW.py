import pandas as pd
import matplotlib.pyplot as plt
import datetime
# Caminho do arquivo
arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'

# Lista de equipamentos para buscar no título
equipamentos = ['GW', 'MDX']  # Edite conforme necessário

try:
    # Tenta ler o CSV ignorando linhas com erro de formatação
    df = pd.read_csv(arquivo, sep=',', encoding='utf-8', engine='python')
except Exception as e:
    print(f"Erro ao ler o CSV: {e}")
    exit()

# Visualize as colunas disponíveis
print("Colunas disponíveis:", df.columns.tolist())

# Ajuste os nomes de coluna conforme necessário
col_titulo = 'Plug-ins - Etiquetas'
col_data = 'Data de abertura'

# Converte coluna de data
df[col_data] = pd.to_datetime(df[col_data], errors='coerce', dayfirst=True)
df = df.dropna(subset=[col_data])  # Remove datas inválidas

# Converte data para período mensal
df['mes'] = df[col_data].dt.to_period('M')


# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]


# Inicia gráfico
plt.figure(figsize=(12, 6))

for equipamento in equipamentos:
    # Filtra linhas cujo título contém o nome do equipamento
    df_eqp = df[df[col_titulo].str.contains(equipamento, case=False, na=False)]
    contagem_mensal = df_eqp.groupby('mes').size()
    contagem_mensal.index = contagem_mensal.index.to_timestamp()
    plt.plot(contagem_mensal.index, contagem_mensal.values, marker='o', label=equipamento.capitalize())

# Finaliza gráfico
plt.title("Tendência mensal de chamados por equipamento - 2025")
plt.xlabel("Mês")
plt.ylabel("Quantidade de chamados")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
# Data a ser marcada
data_marcada = datetime(2025, 4, 9)
# Linha vertical no gráfico
plt.axvline(data_marcada, color='black', linestyle='--', linewidth=2, label='Evento 09/04')
# Anotação opcional
plt.annotate('Nova versão dos gateways - 09/04/25',
             xy=(data_marcada, plt.ylim()[1]*0.95),
             xytext=(8, 8),
             textcoords='offset points',
             arrowprops=dict(arrowstyle='->', color='black'),
             color='black')
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tendencia_mdxgw.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tendencia_mdxgw_{labels}_{hoje.year}.png')

