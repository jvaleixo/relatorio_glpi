
import pandas as pd

CAMINHO_CSV = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/glpi.csv'             # Caminho do arquivo original
ARQUIVO_SAIDA = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'      # Caminho para salvar o resultado filtrado

# 1. Ler CSV (ajuste separador se necessário)
df = pd.read_csv(CAMINHO_CSV, sep=';', encoding='utf-8')
df.columns = df.columns.str.strip()  # Remove espaços extras dos nomes das colunas

# 2. Converter a coluna de data para datetime
df['Data de abertura'] = pd.to_datetime(df['Data de abertura'], dayfirst=True, errors='coerce')

# 3. Remover linhas com datas inválidas (NaT)
df = df.dropna(subset=['Data de abertura'])

# 4. Definir a data inicial do filtro
data_inicio = pd.Timestamp('2025-01-01')

# 5. Filtrar as linhas com data igual ou depois de 01/01/2025
df_filtrado = df[df['Data de abertura'] >= data_inicio]
df_filtrado['Status'] = df_filtrado['Status'].str.replace('(planejado)','(encaminhado)',regex=False) 
df_filtrado['Status'] = df_filtrado['Status'].str.replace('(atribuído)','(suporte)',regex=False)
df_filtrado['Atribuído - Técnico'] = df_filtrado['Atribuído - Técnico'].str.replace('<br>','& ',regex=False)
# 6. Salvar o DataFrame filtrado em CSV (sem índice)
df_filtrado.to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8')

print(f"Arquivo filtrado salvo em: {ARQUIVO_SAIDA}")
