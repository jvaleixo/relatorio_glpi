import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === CARREGAR DADOS ===
caminho_csv = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_mudancas/naosolucionados.csv'
df = pd.read_csv(caminho_csv, sep=';')

COLUNA_STATUS = 'Status'
COLUNA_ETIQUETAS = 'Plug-ins - Etiquetas'

# Normaliza status (separados por ";") e etiquetas (separadas por ",")
df[COLUNA_STATUS] = df[COLUNA_STATUS].fillna('').apply(
    lambda x: [e.strip() for e in str(x).split(';') if e.strip()]
)
df[COLUNA_ETIQUETAS] = df[COLUNA_ETIQUETAS].astype(str).str.lower()

# Lista de etiquetas alvo
etiquetas_alvo = [
    'gw', 'inv', 'mdx', 'solarimétrica', 'sw', 'tracker', 'utr','falta de info', 'energização', 'fibra óptica',
    'datalogger', 'combinerbox', 'relé de trafo','relé de proteção',
    'multimedidor','medidor','internet local','roteador','cftv'
]

# Coleta todos os status únicos no dataset
todos_status = set()
df[COLUNA_STATUS].apply(lambda lista: todos_status.update(lista))

# Inicializa dicionário de contagem por etiqueta e status
contagens = {status: {et: 0 for et in etiquetas_alvo} for status in todos_status}

# Preenche as contagens
for _, row in df.iterrows():
    etiquetas_linha = [e.strip() for e in row[COLUNA_ETIQUETAS].split(',')]
    for status in row[COLUNA_STATUS]:
        for etiqueta in etiquetas_alvo:
            if etiqueta in etiquetas_linha:
                contagens[status][etiqueta] += 1

# Converte para DataFrame
df_contagens = pd.DataFrame(contagens).fillna(0).astype(int)

# === CONTAGEM TOTAL POR ETIQUETA (SOMANDO TODOS OS STATUS) ===
total_por_etiqueta = df_contagens.sum(axis=1).sort_values(ascending=False)

# === GERAÇÃO DOS GRÁFICOS ===
hoje = datetime.today()
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes_atual = nomes_meses[hoje.month - 1]

# Caminho para salvar gráficos
caminho_base = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos_mudancas'

# === GRÁFICO DE BARRAS AGRUPADAS POR STATUS ===
plt.figure(figsize=(12, 6))
largura_barra = 0.1
x = range(len(etiquetas_alvo))

for i, status in enumerate(sorted(df_contagens.columns)):
    valores = df_contagens[status].values
    plt.bar(
        [xi + i * largura_barra for xi in x],
        valores,
        width=largura_barra,
        label=status
    )

plt.xticks([xi + largura_barra * (len(df_contagens.columns) / 2) for xi in x], etiquetas_alvo, rotation=80)
plt.title(f"Contagem de Etiquetas por Status - {mes_atual} {hoje.year}")
plt.xlabel("Etiquetas")
plt.ylabel("Frequência")
plt.legend(title="Status")
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Salva as imagens do gráfico por status
plt.savefig(f'{caminho_base}/contador_etiquetas_todos_status.png')
plt.savefig(f'{caminho_base}/contador_etiquetas_todos_status_{mes_atual}_{hoje.year}.png')
plt.show()

# === GRÁFICO DE TOTAL DE OCORRÊNCIAS POR ETIQUETA (SOMANDO TODOS STATUS) ===
plt.figure(figsize=(12, 6))
total_por_etiqueta.plot(kind='bar', color='steelblue')

plt.title(f'Total de Ocorrências por Etiqueta - {mes_atual} {hoje.year}')
plt.xlabel('Etiqueta')
plt.ylabel('Total de Ocorrências')
plt.xticks(rotation=75)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Salva o gráfico total por etiqueta
plt.savefig(f'{caminho_base}/total_ocorrencias_etiquetas_{mes_atual}_{hoje.year}.png')
plt.show()

# === TOP 10 ETIQUETAS MAIS FREQUENTES ===
top10_etiquetas = total_por_etiqueta.head(10)

# Exibe no terminal (opcional)
print("Top 10 etiquetas mais frequentes:")
print(top10_etiquetas)

# === GRÁFICO DO TOP 10 ===
plt.figure(figsize=(10, 5))
top10_etiquetas.plot(kind='bar', color='coral')

plt.title(f'Top 10 Etiquetas Mais Frequentes - {mes_atual} {hoje.year}')
plt.xlabel('Etiqueta')
plt.ylabel('Total de Ocorrências')
plt.xticks(rotation=75)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Salva o gráfico
plt.savefig(f'{caminho_base}/top10_ocorrencias_etiquetas_{mes_atual}_{hoje.year}.png')
plt.show()
