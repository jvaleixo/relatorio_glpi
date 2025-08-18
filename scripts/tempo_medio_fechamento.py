import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === LEITURA E PRÉ-PROCESSAMENTO ===
df = pd.read_csv('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv', sep=',', encoding='utf-8')

df.columns = df.columns.str.strip()

entidades_excluir = ['equip', 'lógico', 'físico', 'duplicidade','administrativo','eth1', 'cadastro', 'internet local','perda de dados','sgi','vpn - cliente']  

df['Plug-ins - Etiquetas'] = df['Plug-ins - Etiquetas'].str.strip().str.lower()

df_filtrado = df[~df['Plug-ins - Etiquetas'].isin(entidades_excluir)]

df_filtrado['Data de abertura'] = pd.to_datetime(df_filtrado['Data de abertura'], errors='coerce')
df_filtrado['Data de fechamento'] = pd.to_datetime(df_filtrado['Data de fechamento'], errors='coerce')

df_filtrado['tempo_fechamento'] = (df_filtrado['Data de fechamento'] - df_filtrado['Data de abertura']).dt.total_seconds() / 3600
df_filtrado['tempo_fechamento_dias'] = df_filtrado['tempo_fechamento'] / 24

# Remove chamados com tempo negativo ou nulo
df_filtrado = df_filtrado[df_filtrado['tempo_fechamento_dias'] > 0]

df_filtrado['Plug-ins - Etiquetas'] = df_filtrado['Plug-ins - Etiquetas'].str.split(',')
df_exploded = df_filtrado.explode('Plug-ins - Etiquetas')
df_exploded['Plug-ins - Etiquetas'] = df_exploded['Plug-ins - Etiquetas'].str.strip()

# === MÉDIAS E MEDIANAS POR ETIQUETA ===
media_por_etiqueta = df_exploded.groupby('Plug-ins - Etiquetas')['tempo_fechamento'].mean().sort_values(ascending=False) / 24
mediana_por_etiqueta = df_exploded.groupby('Plug-ins - Etiquetas')['tempo_fechamento'].median().sort_values(ascending=False) / 24

media_plot = media_por_etiqueta[~media_por_etiqueta.index.isin(entidades_excluir)]
mediana_plot = mediana_por_etiqueta[~mediana_por_etiqueta.index.isin(entidades_excluir)]

top_etiquetas = media_plot.head(10)
top_mediana = mediana_plot.loc[top_etiquetas.index]

# === DATA ATUAL ===
hoje = datetime.today()
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month - 1]

# === GRÁFICO 1: Tempo médio por etiqueta ===
plt.figure(figsize=(10, 6))
top_etiquetas.plot(kind='barh', color='blue')
plt.xlabel('Tempo médio para fechar (dias)')
plt.title(f'Etiquetas que mais demoram para fechar (média) - {hoje.year}')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_fechamento.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_fechamento_{labels}_{hoje.year}.png')

# === GRÁFICO 2: Comparação média vs mediana ===
df_comp = pd.DataFrame({
    'Média (dias)': top_etiquetas,
    'Mediana (dias)': top_mediana
})
df_comp.plot(kind='barh', figsize=(10, 6))
plt.xlabel('Tempo (dias)')
plt.title(f'Comparação: Média vs Mediana - {labels} {hoje.year}')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/comparacao_media_mediana.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/comparacao_media_mediana_{labels}_{hoje.year}.png')

# === GRÁFICO 3: Boxplot - Todos os tempos ===
plt.figure(figsize=(8, 5))
plt.boxplot(df_filtrado['tempo_fechamento_dias'].dropna(), vert=False, showfliers=True)
plt.xlabel('Tempo de fechamento (dias)')
plt.title('Boxplot - Todos os tempos de fechamento')
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/boxplot_tempo_fechamento_todos.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/boxplot_tempo_fechamento_todos_{labels}_{hoje.year}.png')
dias = 365
# === GRÁFICO 4: Boxplot - Sem valores extremos (> 90 dias) ===
valores_filtrados = df_filtrado[(df_filtrado['tempo_fechamento_dias'] < dias)]['tempo_fechamento_dias']
plt.figure(figsize=(8, 5))
plt.boxplot(valores_filtrados.dropna(), vert=False, showfliers=True)
plt.xlabel('Tempo de fechamento (dias)')
plt.title('Boxplot - Sem outliers (> 90 dias)')
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/boxplot_tempo_fechamento_filtrado.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/boxplot_tempo_fechamento_filtrado_{labels}_{hoje.year}.png')
# === GRÁFICO 5: Histograma - Distribuição dos tempos (< 90 dias) ===
plt.figure(figsize=(10, 5))
plt.hist(valores_filtrados, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Tempo de fechamento (dias)')
plt.ylabel('Quantidade de chamados')
plt.title(f'Histograma - Tempo de fechamento (filtrado, < {dias} dias)')
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/histograma_tempo_fechamento_filtrado.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/histograma_tempo_fechamento_filtrado_{labels}_{hoje.year}.png')
