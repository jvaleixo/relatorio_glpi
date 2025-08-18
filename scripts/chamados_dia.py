#FC:12:2C:D1:D5:C7
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
# ====== CONFIGURAÇÕES ======
CAMINHO_ARQUIVO = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'          # Altere para o caminho do seu CSV
COLUNA_DATA = 'Data de abertura'                  # Nome da coluna com a data
DATA_INICIO = datetime(2025, 1, 1)

# ====== 1. CARREGAR OS DADOS ======
df = pd.read_csv(CAMINHO_ARQUIVO)
df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], dayfirst=True, errors='coerce')
df = df.dropna(subset=[COLUNA_DATA])

# ====== 2. FILTRAR CHAMADOS DESDE 01/01/2025 ======
df_filtrado = df[df[COLUNA_DATA] >= DATA_INICIO]

# ====== 3. AGRUPAR POR DIA ======
chamados_por_dia = df_filtrado[COLUNA_DATA].dt.date.value_counts().sort_index()
chamados_por_dia.index = pd.to_datetime(chamados_por_dia.index)

# ====== 4. CALCULAR MÉDIA MENSAL DE CHAMADOS POR DIA ======
media_mensal = chamados_por_dia.groupby(chamados_por_dia.index.to_period('M')).mean()
media_mensal.index = media_mensal.index.to_timestamp()


# Expande média mensal para todos os dias do mês (para suavizar no gráfico)
media_mensal_diaria = media_mensal.reindex(chamados_por_dia.index, method='pad')

# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]


# ====== 5. PLOTAR O GRÁFICO ======
plt.figure(figsize=(12, 6))
plt.plot(chamados_por_dia.index, chamados_por_dia.values, marker='o', linestyle='-', label='Chamados por Dia')
plt.plot(media_mensal_diaria.index, media_mensal_diaria.values, linestyle='--', color='red', label='Média Mensal Diária')

# Personalização
plt.title(f'Chamados GLPI Abertos por Dia e Média Mensal - {hoje.year}')
plt.xlabel('Data')
plt.ylabel('Número de Chamados')
plt.grid(True)
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

# (Opcional) salvar imagem
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/chamados_com_media_mensal.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/chamados_com_media_mensal_{labels}_{hoje.year}.png')


