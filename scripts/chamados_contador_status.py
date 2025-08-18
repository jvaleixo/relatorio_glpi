import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
# 1. Caminho para seu CSV
caminho_csv = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'

# 2. Lê o CSV
df = pd.read_csv(caminho_csv, sep =',')

COLUNA_STATUS = 'Status'


# Converte etiquetas em listas (trata células vazias)
df[COLUNA_STATUS] = df[COLUNA_STATUS].fillna('').apply(
    lambda x: [e.strip() for e in str(x).split(',') if e.strip()]
)

# 4. Lista de etiquetas específicas que queremos contar
etiquetas_alvo = ['Novo', 'Em atendimento (encaminhado)', 'Em atendimento (suporte)', 'Pendente']  # Edite conforme necessário

# 5. Inicializa o contador
contagem_resultado = {etiqueta: 0 for etiqueta in etiquetas_alvo}

# 6. Conta as ocorrências
for linha in df['Status'].dropna():
    etiquetas_linha = linha
    for etiqueta in etiquetas_alvo:
        if etiqueta in etiquetas_linha:
            contagem_resultado[etiqueta] += 1

# 7. Exibe contagem
print("Contagem de etiquetas específicas:")
for etiqueta, count in contagem_resultado.items():
    print(f"{etiqueta}: {count}")
mes_numeral = datetime.month

# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]


# 8. Gera gráfico
plt.figure(figsize=(8, 5))
plt.bar(contagem_resultado.keys(), contagem_resultado.values(), color='blue')
plt.title(f'Contagem de status dos chamados não solucionados - {labels} ')
plt.xlabel("Status")
plt.ylabel("Frequência")
plt.gca().invert_xaxis()
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/chamados_contador_status.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/chamados_contador_status_{labels}_{hoje.year}.png')

