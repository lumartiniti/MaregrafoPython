import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def limpa_linha(linha):
    return linha.strip().replace(',', '.')


try:
    with open('C:/Users/luima/OneDrive/Documentos/dados_python/maregrafo/IMB201014.txt') as io:
        linhas = io.readlines()
except FileNotFoundError:
    print("Erro: O arquivo não foi encontrado.")
    exit()
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    exit()

guarda_linhas = []
for line in linhas:
    linha_corrigida = limpa_linha(line)

    # Ignore linhas vazias
    if not linha_corrigida:
        continue

    linha_quebrada = linha_corrigida.split(';')

    if len(linha_quebrada) < 4:  # Checa se há pelo menos 4 colunas
        print(f"Formato incorreto na linha: {linha_corrigida}")
        continue

    try:
        dia, mes, ano = map(int, linha_quebrada[0].split('/'))
        hora, minuto, segundo = map(int, linha_quebrada[1].split(':'))
        var1 = float(linha_quebrada[2])
        var2 = float(linha_quebrada[3])
    except ValueError as e:
        print(f"Erro ao processar a linha: {linha_corrigida}. Detalhes: {e}")
        continue

    nova_linha = [ano, mes, dia, hora, minuto, segundo, var1, var2]
    guarda_linhas.append(nova_linha)

if not guarda_linhas:
    print("Nenhum dado válido encontrado no arquivo.")
    exit()

dados = np.array(guarda_linhas)

# Criação de `tempo` com list comprehension
tempo = [datetime.datetime(row[0], row[1], row[2], row[3], row[4], row[5]) for row in dados]

# Criação do gráfico
fig, ax = plt.subplots()
ax.plot(tempo, dados[:, 6], label='var 1')
ax.plot(tempo, dados[:, 7], label='var 2')

formato = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(formato)

ax.set_xlabel('Tempo')
ax.set_ylabel('Nível (m)')
plt.legend()
plt.show()
