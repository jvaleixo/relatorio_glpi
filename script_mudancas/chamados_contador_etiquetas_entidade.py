import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# === CONFIGURAÇÕES ===
etiqueta_base = 'inv'  # <- Mude aqui para a etiqueta que deseja analisar
caminho_csv = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_mudancas/naosolucionado.csv'

# === CARREGAR O CSV ===
df = pd.read_csv(caminho_csv, sep=';')

COLUNA_STATUS = 'Status'
COLUNA_ETIQUETAS = 'Plug-ins - Etiquetas'

# Normaliza status e etiquetas
df[COLUNA_STATUS] = df[COLUNA_STATUS].fillna('').apply(
    lambda x: [e.strip() for e in str(x).split(';') if e.strip()]
)
df[COLUNA_ETIQUETAS] = df[COLUNA_ETIQUETAS].astype(str).str.lower()

# Filtra linhas que contêm a etiqueta_base
df_filtrado = df[df[COLUNA_ETIQUETAS].str.contains(fr'\b{etiqueta_base}\b')]

# Inicializa contagem
contagens = defaultdict(lambda: defaultdict(int))  # {status: {etiqueta: count}}

# Conta coocorrências
for _, row in df_filtrado.iterrows():
    etiquetas = [e.strip() for e in row[COLUNA_ETIQUETAS].split(',') if e.strip()]
    if etiqueta_base not in etiquetas:
        continue  # segurança
    outras_etiquetas = [e for e in etiquetas if e != etiqueta_base]
    for status in row[COLUNA_STATUS]:
        for etiqueta in outras_etiquetas:
            contagens[status][etiqueta] += 1

# Transforma em DataFrame (todas as etiquetas)
df_contagens = pd.DataFrame(contagens).fillna(0).astype(int).sort_index()

# === GERA GRÁFICO ===
hoje = datetime.today()
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
mes_atual = nomes_meses[hoje.month - 1]

plt.figure(figsize=(12, max(6, len(df_contagens) * 0.3)))  # Ajusta altura com base na quantidade de etiquetas
largura_barra = 0.8 / len(df_contagens.columns)  # Divide espaço das barras pelo número de status
x = range(len(df_contagens.index))

for i, status in enumerate(sorted(df_contagens.columns)):
    plt.bar(
        [xi + i * largura_barra for xi in x],
        df_contagens[status].values,
        width=largura_barra,
        label=status
    )

plt.xticks([xi + largura_barra * (len(df_contagens.columns) / 2) for xi in x], df_contagens.index, rotation=80)
plt.title(f"Coocorrência com '{etiqueta_base}' por Status - {mes_atual} {hoje.year}")
plt.xlabel("Outras Etiquetas")
plt.ylabel("Frequência")
plt.legend(title="Status")
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)

# Caminhos de salvamento
caminho_base = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos_mudancas'
plt.savefig(f'{caminho_base}/coocorrencia_{etiqueta_base}_todas_por_status.png')
plt.savefig(f'{caminho_base}/coocorrencia_{etiqueta_base}_todas_por_status_{mes_atual}_{hoje.year}.png')
plt.show()
