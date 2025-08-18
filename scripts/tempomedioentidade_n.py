import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === CONFIGURAÇÕES ===
arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'
col_entidade = 'Atribuído - Técnico'
col_abertura = 'Data de abertura'
col_fechamento = 'Data de fechamento'

# === LÊ O CSV ===
df = pd.read_csv(arquivo, sep=',', encoding='utf-8')

# === PREPARA OS DADOS ===
df[col_entidade] = df[col_entidade].str.strip().str.lower()

# Filtro: entidades que não contêm "time" e começam com r, p ou n
df_sem_time = df[
    ~df[col_entidade].str.contains('time', case=False, na=False) &
	~df[col_entidade].str.contains('nayara', case=False, na=False) &
	~df[col_entidade].str.contains('ana', case=False, na=False) &
    df[col_entidade].str.match(r'^[rpn]', na=False)
]


# Converte datas
df_sem_time[col_abertura] = pd.to_datetime(df_sem_time[col_abertura], errors='coerce', dayfirst=True)
df_sem_time[col_fechamento] = pd.to_datetime(df_sem_time[col_fechamento], errors='coerce', dayfirst=True)

# Remove linhas incompletas
df_sem_time = df_sem_time.dropna(subset=[col_abertura, col_fechamento, col_entidade])

# Calcula tempo de resolução em dias
df_sem_time['tempo_resolucao'] = (df_sem_time[col_fechamento] - df_sem_time[col_abertura]).dt.total_seconds() / 86400

# Remove tempos negativos (casos com erro de data)
df_sem_time = df_sem_time[df_sem_time['tempo_resolucao'] >= 0]

# Agrupa por entidade
agrupado = df_sem_time.groupby(col_entidade)['tempo_resolucao']

# Calcula média e mediana
media = agrupado.mean().sort_values(ascending=False)
mediana = agrupado.median().sort_values(ascending=False)

# === GERAÇÃO DOS GRÁFICOS ===
hoje = datetime.today()
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes_nome = nomes_meses[hoje.month - 1]

caminho_base = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos'

# === 1. GRÁFICO: MÉDIA VS MEDIANA COM VALORES CORRETOS ===
# Ordena entidades pela média (decrescente)
entidades_ordenadas = media.sort_values(ascending=False).index.tolist()
media_ordenada = media.loc[entidades_ordenadas]
mediana_ordenada = mediana.loc[entidades_ordenadas]

plt.figure(figsize=(12, 6))

indices = range(len(entidades_ordenadas))
largura_barra = 0.4

# Barras de média
plt.bar([i for i in indices], media_ordenada.values, width=largura_barra, label='Média', align='center')

# Barras de mediana
plt.bar([i + largura_barra for i in indices], mediana_ordenada.values, width=largura_barra, label='Mediana', color='orange', align='center')

# Adiciona valores
for i, valor in enumerate(media_ordenada.values):
    plt.text(i, valor + 0.2, f'{valor:.1f}', ha='center', va='bottom', fontsize=8)

for i, valor in enumerate(mediana_ordenada.values):
    plt.text(i + largura_barra, valor + 0.2, f'{valor:.1f}', ha='center', va='bottom', fontsize=8)

# Eixos e legendas
plt.xticks([i + largura_barra / 2 for i in indices], entidades_ordenadas, rotation=90)
plt.ylabel('Tempo de resolução (dias)')
plt.title(f'Tempo médio e mediano - Colaboradores - {hoje.year}')
plt.xticks(rotation=70)
plt.legend()
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)

# Salva
plt.savefig(f'{caminho_base}/media_vs_mediana_rpn.png')
plt.savefig(f'{caminho_base}/media_vs_mediana_rpn_{mes_nome}_{hoje.year}.png')
plt.show()


# === 2. GRÁFICO: BOXPLOT POR ENTIDADE ===
dados_boxplot = [grupo['tempo_resolucao'].values for _, grupo in df_sem_time.groupby(col_entidade)]
rotulos = list(df_sem_time.groupby(col_entidade).groups.keys())

plt.figure(figsize=(12, max(6, len(rotulos)*0.25)))
plt.boxplot(dados_boxplot, labels=rotulos, vert=True, patch_artist=True)
plt.xticks(rotation=70)
plt.ylabel('Tempo de resolução (dias)')
plt.title(f'Boxplot Tempo médio e mediano - Colaboradores - {hoje.year}')
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig(f'{caminho_base}/boxplot_tempo_resolucao_sem_time.png')
plt.savefig(f'{caminho_base}/boxplot_tempo_resolucao_sem_time_{mes_nome}_{hoje.year}.png')
plt.show()

# === SAÍDA NO TERMINAL ===
print("\n📊 Média de tempo de resolução (em dias):")
print(media.round(2))

print("\n📊 Mediana de tempo de resolução (em dias):")
print(mediana.round(2))
