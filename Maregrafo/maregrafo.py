import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


with open('C:/Users/luima/OneDrive/Documentos/dados_python/maregrafo/IMB201014.txt') as io:
    linhas = io.readlines()
    print(linhas)

guarda_linhas = []

for line in linhas:
    linha_corrigida = line.strip().replace(',', '.')

    if not linha_corrigida:
        continue

    linha_quebrada = linha_corrigida.split(';')

    if len(linha_quebrada) < 4:
        print(f"Formato incorreto na linha: {linha_corrigida}")
        continue

    linha_corrigida = line.replace(',', '.')
    linha_quebrada = linha_corrigida.split(';')

    ldata = linha_quebrada[0].split('/')
    lhora = linha_quebrada[1].split(':')
    var1 = linha_quebrada[2].split('.')
    var2 = linha_quebrada[3].split('.')

    dia = int(ldata[0])
    mes = int(ldata[1])
    ano = int(ldata[2])
    hora = int(lhora[0])
    minuto = int(lhora[1])
    segundo = int(lhora[2])
    var1 = float(var1[0])
    var2 = float(var2[1])

    nova_linha = [ano, mes, dia, hora, minuto, segundo, var1, var2]

    guarda_linhas.append(nova_linha)

dados = np.array(guarda_linhas)

tempo = []
for i in range(len(dados)):
    monta_tempo = datetime.datetime(int(dados[i, 0]),
                                    int(dados[i, 1]),
                                    int(dados[i, 2]),
                                    int(dados[i, 3]),
                                    int(dados[i, 4]),
                                    int(dados[i, 5]))
    tempo.append(monta_tempo)

fig, ax = plt.subplots()
ax.plot(tempo,dados[:,6], label='var 1')
ax.plot(tempo,dados[:,7], label='var 2')

formato = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(formato)

ax.set_xlabel('Tempo')
ax.set_ylabel('Nivel(m)')

plt.legend()
plt.show()
