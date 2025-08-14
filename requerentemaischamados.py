import pandas as pd

arquivo = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/glpi.csv'

df = pd.read_csv(arquivo, sep = ';')

print("Colunas disponíveis:", df.columns.tolist())

col_requerente = 'Requerente - Requerente'

# Remove valores ausentes
df = df.dropna(subset=[col_requerente])

# Filtra requerentes que contêm 'time' (ignorando maiúsculas/minúsculas)
df_time = df[df[col_requerente].str.contains('time', case=False, na=False)]

# Conta chamados por esses requerentes
chamados_por_time = df_time[col_requerente].value_counts()

if chamados_por_time.empty:
    print("Nenhum requerente com 'time' no nome encontrado.")
else:
    top_requerente = chamados_por_time.idxmax()
    quantidade = chamados_por_time.max()

    print(f"\n👤 Requerente com mais chamados contendo 'time':")
    print(f"{top_requerente}: {quantidade} chamados")

    print("\n📊 Top 10 requerentes com 'time' no nome - Chamados não solucionados:")
    print(chamados_por_time.head(10))
