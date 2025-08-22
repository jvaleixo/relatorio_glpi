import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# === CONFIGURAÇÕES ===
caminho_csv = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/glpi_mudancas/naosolucionados.csv'  # Substitua pelo caminho real
coluna_id = 'ID'
coluna_titulo = 'Título'
coluna_status = 'Status'
coluna_data_abertura = 'Data de abertura'
coluna_etiquetas = 'Plug-ins - Etiquetas'
status_fechados = ['Fechado']
valor_mensal = 2500  # R$ por mês

# === CARREGAR DADOS ===
df = pd.read_csv(caminho_csv, sep=';')

# === CONVERTER DATA DE ABERTURA PARA datetime ===
df[coluna_data_abertura] = pd.to_datetime(df[coluna_data_abertura], errors='coerce', dayfirst=True)

# === FILTRAR CHAMADOS ABERTOS ===
df[coluna_status] = df[coluna_status].astype(str).str.lower().str.strip()
df_abertos = df[~df[coluna_status].isin(status_fechados)].copy()

# === CALCULAR DIAS EM ABERTO ===
hoje = pd.Timestamp(datetime.today())
df_abertos['dias em aberto'] = (hoje - df_abertos[coluna_data_abertura]).dt.days

# === ESTIMAR VALOR PERDIDO ===
df_abertos['valor perdido (R$)'] = (df_abertos['dias em aberto'] / 30 * valor_mensal).round(2)

# === ORDENAR PELOS MAIS ANTIGOS ===
df_top10_antigos = df_abertos.sort_values(by='dias em aberto', ascending=False).head(10)

# === EXIBIR RESULTADO NO TERMINAL ===
print("Top 10 mudanças mais antigas ainda abertas:\n")
print(df_top10_antigos[[coluna_id, coluna_titulo, coluna_status, coluna_data_abertura, 'dias em aberto', 'valor perdido (R$)']])

# === GERAR GRÁFICO ===
plt.figure(figsize=(14, 7))

# Título composto: id + título
rotulos = df_top10_antigos.apply(lambda row: f"{row[coluna_id]} - {row[coluna_titulo]}", axis=1)
dias_abertos = df_top10_antigos['dias em aberto']
valores_perdidos = df_top10_antigos['valor perdido (R$)']

# Gráfico horizontal
barras = plt.barh(rotulos, dias_abertos, color='blue')

# Aumenta limite do eixo x em 15% para não cortar os rótulos
max_dias = dias_abertos.max()
plt.xlim(0, max_dias * 1.15)

# Adiciona rótulos dentro da barra, alinhados à direita
for barra, dias, valor in zip(barras, dias_abertos, valores_perdidos):
    plt.text(
        barra.get_width() - 5,  # ligeiramente antes da borda da barra
        barra.get_y() + barra.get_height() / 2,
        f"{dias} dias | R$ {valor:,.2f}",
        va='center',
        ha='right',
        fontsize=9,
        color='white',
        fontweight='bold'
    )

plt.xlabel('Dias em Aberto')
plt.ylabel('Mudança')
plt.title('Top 10 mudanças mais antigas ainda abertas')
plt.gca().invert_yaxis()  # Mais antigo no topo
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.tight_layout()
# === SALVAR GRÁFICO ===
caminho_grafico = '/home/aleixo/Documents/pcantigo/Documents/estatistica-glpi/relatorio_mensal/graficos_mudancas/top10_chamados_antigos_valor.png'  # Altere se quiser
plt.savefig(caminho_grafico)
plt.show()
