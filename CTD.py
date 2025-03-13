import os
import numpy as np
import matplotlib.pyplot as plt
import datetime

from CTD import date_time, oxygen_sat, depth
from teste import salinidades

path = r'C:\Users\luima\OneDrive\Documentos\dados_python\csv\\'

mydir = os.listdir(path) # retorna uma lista contendo os nomes de todos os arquivos e subdiretórios dentro do diretório especificado.

ctd_file = [] # Cria uma lista vazia.
for file in mydir: # A variável file recebe, um por um, os nomes dos arquivos contidos em mydir -> Percorre mydir.
    if file.endswith('.Csv'): # Verifica se o nome do arquivo termina com ".csv".
        ctd_file.append(file) # Se a condição for verdadeira, o nome do arquivo é adicionado à lista ctd_file.

#with open(path + ctd_file[0]) as file:
    # forma de contar as linhas
#    lines = file.readlines()

    # Outra forma de contar.
#   c = 0 # Ela serve para contar o número de linhas do arquivo.
#    for line in lines: # Essa linha cria um laço de repetição para iterar sobre cada linha do arquivo, que está armazenada na lista lines.
#        c += 1 #a variável c é incrementada em 1 a cada iteração, ou seja, cada vez que uma linha é processada, o contador c aumenta. Isso serve para contar quantas linhas existem no arquivo.

# print(len(lines))
# print(c)
# print(lines[43])

with (open(path + ctd_file[0]) as file): # abre o arquivo especificado.

    c = 0
    date_time = None # Inicializa a variável com um valor padrão

    depth = []
    temp = []
    sal = []
    chl = []
    turb = []
    oxygen_sat = []
    oxygen = []

    for line in file: # itera sobre cada linha do arquivo, ou seja, percorre o arquivo linha por linha.

        if line.startswith("StartTime="): # Usa startswith() para verificar se a linha começa com "StartTime=" (mais seguro do que line[0:10]).

            date_time = line.strip() # Remove espaços em branco e \n no final da linha.

            year = int(date_time[10:14])
            month = int(date_time[15:17])
            day = int(date_time[18:20])
            hour = int(date_time[21:23])
            minute = int(date_time[24:26])

            ctd_time = datetime.datetime(year, month, day, hour, minute)

        c += 1
        if c >= 45:

            line_break = line.split(',')

            depth.append(float(line_break[0]))
            temp.append(float(line_break[1]))
            sal.append(float(line_break[2]))
            chl.append(float(line_break[8]))
            turb.append(float(line_break[9]))
            oxygen_sat.append(float(line_break[10]))
            oxygen.append(float(line_break[11]))

print(line_break)

if date_time is not None:
    print(date_time) # Exibe a linha encontrada
else:
    print("Erro: 'StartTime=' não encontrado no arquivo.") # Mensagem caso a linha não exista

# print(date_time, type(date_time))
# print(ctd_time, type(ctd_time))

fig = plt.figure(figsize=(10, 5))

px = .1
py = .1
dx = .15
dy = .8
intervalo = .02

ax1 = fig.add_axes([px, py, dx, dy])
ax2 = fig.add_axes([px +(dx + intervalo), py, dx, dy])
ax3 = fig.add_axes([px +(dx + intervalo)*2, py, dx, dy])
ax4 = fig.add_axes([px +(dx + intervalo)*3, py, dx, dy])
ax5 = fig.add_axes([px +(dx + intervalo)*4, py, dx, dy])

depth_g = -np.array(depth)

ax1.plot(sal, depth_g)
ax2.plot(temp, depth_g)
ax3.plot(chl, depth_g)
ax4.plot(turb, depth_g)
ax5.plot(oxygen_sat, depth_g)

axes = [ax1, ax2, ax3, ax4, ax5]
labs = ['Salinity (psu)', 'Temperature (°C)', 'Chlorophyll-a (g/L)', 'Turbidity (FTU)', 'Oxygen (%)']

for i in range(len(axes)):
    axes[i].set_xlabel(labs[i])
    if i > 0:
        axes[i].set_yticklabels('')

ax1.set_ylabel('Depth (m)')
plt.show()
