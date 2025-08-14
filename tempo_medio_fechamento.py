import pandas as pd

import matplotlib.pyplot as plt
# Leitura do CSV
df = pd.read_csv('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv', sep=',', encoding='utf-8')

# Remove espaços dos nomes das colunas (caso existam)
df.columns = df.columns.str.strip()

entidades_excluir = ['equip', 'lógico', 'físico', 'duplicidade','administrativo','eth1', 'cadastro', 'internet local','perda de dados','sgi','vpn - cliente']  
# Padroniza os nomes: remove espaços extras e põe tudo em minúsculo
df['Plug-ins - Etiquetas'] = df['Plug-ins - Etiquetas'].str.strip().str.lower()

# Exclui as entidades
df_filtrado = df[~df['Plug-ins - Etiquetas'].isin(entidades_excluir)]
print(df_filtrado)
# Converte as datas
df_filtrado['Data de abertura'] = pd.to_datetime(df_filtrado['Data de abertura'], errors='coerce')
df_filtrado['Data de fechamento'] = pd.to_datetime(df_filtrado['Data de fechamento'], errors='coerce')

# Calcula o tempo de fechamento (em horas)
df_filtrado['tempo_fechamento'] = (df_filtrado['Data de fechamento'] - df_filtrado['Data de abertura']).dt.total_seconds() / 3600

# Divide as etiquetas em lista
df_filtrado['Plug-ins - Etiquetas'] = df_filtrado['Plug-ins - Etiquetas'].str.split(',')

# Explode as etiquetas para linhas individuais
df_exploded = df_filtrado.explode('Plug-ins - Etiquetas')

# Remove espaços extras das etiquetas
df_exploded['Plug-ins - Etiquetas'] = df_exploded['Plug-ins - Etiquetas'].str.strip()

# Agrupa por etiqueta e calcula o tempo médio de fechamento
media_por_etiqueta = df_exploded.groupby('Plug-ins - Etiquetas')['tempo_fechamento'].mean().sort_values(ascending=False)/24
media_plot = media_por_etiqueta[~media_por_etiqueta.index.isin(entidades_excluir)]
# Seleciona as top 10 etiquetas que mais demoram
top_etiquetas = media_plot.head(10)

# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]

print(hoje)

# Plota o gráfico
plt.figure(figsize=(10, 6))
top_etiquetas.plot(kind='barh', color='blue')
plt.xlabel('Tempo médio para fechar (dias)')
plt.title(f'Etiquetas que mais demoram para fechar - {hoje.year}')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_fechamento.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/tempo_fechamento_{labels}_{hoje.year}.png')
