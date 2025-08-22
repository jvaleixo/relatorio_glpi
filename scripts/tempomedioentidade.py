import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from scipy.stats import trim_mean

# === CAMINHOS E CONFIGS ===
arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'
caminho_base = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos'

col_entidade = 'Requerente - Requerente'
col_abertura = 'Data de abertura'
col_fechamento = 'Data de fechamento'

entidades_excluir = ['time weg', 'time carvalho', 'time oi', 'time atc', 'marcelo neves', 'tasso foresti', 'matheus mendes']

# === LEITURA DO CSV ===
df = pd.read_csv(arquivo, sep=',', encoding='utf-8')
df[col_entidade] = df[col_entidade].str.strip().str.lower()

# === FILTRAGEM ===
df_sem_time = df[
    ~df[col_entidade].str.contains('tasso', case=False, na=False) &
    ~df[col_entidade].str.contains('marcelo', case=False, na=False) &
    ~df[col_entidade].str.contains('matheus', case=False, na=False) &
    ~df[col_entidade].str.contains('weg', case=False, na=False) &
    ~df[col_entidade].str.contains('carvalho', case=False, na=False) &
    ~df[col_entidade].str.contains('oi', case=False, na=False) &
    ~df[col_entidade].str.contains('atc', case=False, na=False) &
    df[col_entidade].str.match(r'^[time]', na=False)
]

# === CONVERSÃO DE DATAS E TEMPO DE RESOLUÇÃO ===
df_sem_time[col_abertura] = pd.to_datetime(df_sem_time[col_abertura], errors='coerce', dayfirst=True)
df_sem_time[col_fechamento] = pd.to_datetime(df_sem_time[col_fechamento], errors='coerce', dayfirst=True)
df_sem_time = df_sem_time.dropna(subset=[col_abertura, col_fechamento, col_entidade])
df_sem_time['tempo_resolucao'] = (df_sem_time[col_fechamento] - df_sem_time[col_abertura]).dt.total_seconds() / 86400
df_sem_time = df_sem_time[df_sem_time['tempo_resolucao'] >= 0]

# === AGRUPAMENTO POR ENTIDADE ===
agrupado = df_sem_time.groupby(col_entidade)['tempo_resolucao']
media = agrupado.mean().sort_values(ascending=False)
mediana = agrupado.median().sort_values(ascending=False)

# === MÉDIA GERAL E APARADA ===
media_geral = df_sem_time['tempo_resolucao'].mean()
media_aparada = trim_mean(df_sem_time['tempo_resolucao'], proportiontocut=0.1)

# === CONFIGURAÇÃO DE DATA ===
hoje = datetime.today()
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes_nome = nomes_meses[hoje.month - 1]

# === GERAÇÃO DO GRÁFICO MÉDIA VS MEDIANA ===
entidades_ordenadas = media.sort_values(ascending=False).index.tolist()
media_ordenada = media.loc[entidades_ordenadas]
mediana_ordenada = mediana.loc[entidades_ordenadas]

plt.figure(figsize=(12, 6))
indices = range(len(entidades_ordenadas))
largura_barra = 0.4

# Barras de média e mediana
plt.bar([i for i in indices], media_ordenada.values, width=largura_barra, label='Média', align='center')
plt.bar([i + largura_barra for i in indices], mediana_ordenada.values, width=largura_barra, label='Mediana', color='orange', align='center')

# Textos nos valores
for i, valor in enumerate(media_ordenada.values):
    plt.text(i, valor + 0.2, f'{valor:.1f}', ha='center', va='bottom', fontsize=8)
for i, valor in enumerate(mediana_ordenada.values):
    plt.text(i + largura_barra, valor + 0.2, f'{valor:.1f}', ha='center', va='bottom', fontsize=8)

# Linhas da média geral e aparada
plt.axhline(media_geral, color='red', linestyle='--', label=f'Média geral ({media_geral:.1f} dias)')
plt.axhline(media_aparada, color='green', linestyle='--', label=f'Média aparada 10% ({media_aparada:.1f} dias)')

# Eixos, legendas, formatação
plt.xticks([i + largura_barra / 2 for i in indices], entidades_ordenadas, rotation=70)
plt.ylabel('Tempo de resolução (dias)')
plt.title(f'Tempo médio e mediano - Clientes - {hoje.year}')
plt.legend()
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Salva gráfico
plt.savefig(f'{caminho_base}/media_vs_mediana_clientes.png')
plt.savefig(f'{caminho_base}/media_vs_mediana_clientes_{mes_nome}_{hoje.year}.png')
plt.show()

# === GRÁFICO BOXPLOT POR ENTIDADE ===
dados_boxplot = [grupo['tempo_resolucao'].values for _, grupo in df_sem_time.groupby(col_entidade)]
rotulos = list(df_sem_time.groupby(col_entidade).groups.keys())

plt.figure(figsize=(12, max(6, len(rotulos)*0.25)))
plt.boxplot(dados_boxplot, labels=rotulos, vert=True, patch_artist=True)
plt.xticks(rotation=70)
plt.ylabel('Tempo de resolução (dias)')
plt.title(f'Boxplot Tempo médio e mediano - clientes - {hoje.year}')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig(f'{caminho_base}/boxplot_tempo_resolucao_clientes.png')
plt.savefig(f'{caminho_base}/boxplot_tempo_resolucao_clientes_{mes_nome}_{hoje.year}.png')
plt.show()

# === SAÍDA NO TERMINAL ===
print("\n📊 Média de tempo de resolução (em dias):")
print(media.round(2))

print("\n📊 Mediana de tempo de resolução (em dias):")
print(mediana.round(2))

print(f"\n📉 Média aparada (10%): {media_aparada:.2f} dias")
