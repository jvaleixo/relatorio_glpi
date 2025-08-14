import pandas as pd
import matplotlib.pyplot as plt


# Caminho do CSV
arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'

# Lê o CSV
df = pd.read_csv(arquivo, sep=',',encoding='utf-8')



# Nomes das colunas (ajuste se necessário)
col_entidade = 'Requerente - Requerente'
col_abertura = 'Data de abertura'
col_fechamento = 'Data de fechamento'

entidades_excluir = ['time weg', 'time carvalho', 'time oi', 'time atc']
# Padroniza os nomes: remove espaços extras e põe tudo em minúsculo
df[col_entidade] = df[col_entidade].str.strip().str.lower()

# Exclui as entidades
df_filtrado = df[~df[col_entidade].isin(entidades_excluir)]


# Converte colunas de data
df_filtrado[col_abertura] = pd.to_datetime(df_filtrado[col_abertura], errors='coerce', dayfirst=True)
df_filtrado[col_fechamento] = pd.to_datetime(df_filtrado[col_fechamento], errors='coerce', dayfirst=True)

# Remove linhas com dados ausentes
df_filtrado = df_filtrado.dropna(subset=[col_abertura, col_fechamento, col_entidade])

# Filtra apenas entidades que têm 'Time' no nome (case-insensitive)
df_time = df_filtrado[df_filtrado[col_entidade].str.contains('Time', case=False, na=False)]

# Calcula tempo de resolução
df_time['tempo_resolucao'] = df_time[col_fechamento] - df_time[col_abertura]

# Agrupa por entidade e calcula média
media_por_time = df_time.groupby(col_entidade)['tempo_resolucao'].mean().sort_values(ascending=False)

# Converte timedelta para dias
media_por_time_dias = media_por_time.dt.total_seconds() / 86400
# Remove entidades indesejadas do resultado já calculado
media_plot = media_por_time_dias[~media_por_time_dias.index.isin(entidades_excluir)]

# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]


# Exibe o resultado
print("\n📊 Média de tempo de resolução por entidades com 'Time' no nome (em dias):")
print(media_plot.round(2))

# Plota o gráfico
plt.figure(figsize=(10, 6))
media_plot.plot(kind='bar', color='blue')
plt.xlabel('Tempo médio para solucionar (dias)')
plt.title('Clientes com maior demora no fechamento de chamados - 2025')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_medio.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_medio_{labels}_{hoje.year}.png')

