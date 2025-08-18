import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o CSV
caminho_csv = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_downloads/filtrado.csv'
df = pd.read_csv(caminho_csv, sep=',')

COLUNA_STATUS = 'Status'
#status_alvo = 'Pendente'
#status_alvo = 'Em atendimento (atribuído)'
status_alvo = 'Em atendimento (encaminhado)'
#status_alvo = 'Novo'
#status_alvo = 'Solucionado'
# Converte valores de Status para lista
df[COLUNA_STATUS] = df[COLUNA_STATUS].fillna('').apply(
    lambda x: [e.strip() for e in str(x).split(',') if e.strip()]
)

# Filtra linhas com o status desejado
df_com_xx = df[df[COLUNA_STATUS].apply(lambda etiquetas: status_alvo in etiquetas)]

# Normaliza a coluna de etiquetas
df_com_xx['Plug-ins - Etiquetas'] = df_com_xx['Plug-ins - Etiquetas'].astype(str).str.lower()

# Lista de etiquetas alvo
#etiquetas_alvo = ['gw', 'inv', 'mdx', 'solarimétrica', 'sw', 'tracker', 'utr']
etiquetas_alvo = ['administrativo', 'cadastro', 'config. ati', 'config. cliente', 'duplicidade', 'equip', 'eth1', 'eth2', 'físico', 'gw', 'internet local', 'inv', 'lógico','mdx', 'perda de dados', 'rede local', 'sgd', 'sgi', 'solarimétrica','sw', 'tracker', 'utr', 'vpn - cliente'] 
# Conta as ocorrências
contagem_resultado = {etiqueta: 0 for etiqueta in etiquetas_alvo}
for linha in df_com_xx['Plug-ins - Etiquetas'].dropna():
    etiquetas_linha = [e.strip() for e in linha.split(',')]
    for etiqueta in etiquetas_alvo:
        if etiqueta in etiquetas_linha:
            contagem_resultado[etiqueta] += 1

# Ordena os dados pela frequência (valor)
contagem_ordenada = dict(sorted(contagem_resultado.items(), key=lambda item: item[1], reverse=True))

# Exibe a contagem
print("Contagem de etiquetas específicas:")
for etiqueta, count in contagem_ordenada.items():
    print(f"{etiqueta}: {count}")

	
# === GERAÇÃO DO GRÁFICO ===
from datetime import datetime
# === DATA ATUAL ===
hoje = datetime.today()
inicio_ano = datetime(hoje.year, 1, 1)
nomes_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
labels = nomes_meses[hoje.month-1]
	
	
# 8. Gera gráfico
plt.figure(figsize=(8, 5))
plt.bar(contagem_ordenada.keys(), contagem_ordenada.values(), color='blue')
plt.title(f"Frequência das Etiquetas - Chamados {status_alvo} - 2025")
plt.xlabel("Etiquetas")
plt.ylabel("Frequência")
plt.xticks(rotation=80)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/contador_etiquetas_planejado.png')
plt.savefig(f'/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos/contador_etiquetas_planejado_{labels}_{hoje.year}.png')


