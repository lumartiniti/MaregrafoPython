import os  # gerar lista com o nome dos arquivos de CTD e carregá-los -> pacote OS permite trabalhar com arquivos no sistema de diretórios do sistema.
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
from IPython.display import clear_output, display
from scipy.interpolate import griddata

path = r'C:\Users\luima\OneDrive\Documentos\dados_python\csv\\'
mydir = os.listdir(path) # retorna uma lista contendo os nomes de todos os arquivos e subdiretórios dentro do diretório especificado.

ctd_file = []
for file in mydir: # A variável file recebe, um por um, os nomes dos arquivos contidos em mydir -> Percorre mydir.
    if file.endswith('.Csv'): # Verifica se o nome do arquivo termina com ".csv".
        ctd_file.append(file) # Se a condição for verdadeira, o nome do arquivo é adicionado à lista ctd_file.

def carrega_ctd(path, ctd_file):
    with open(path + ctd_file) as file:
        c = 0

        depth = []
        temperature = []
        salinity = []
        chlrophyll = []
        turbidity = []
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
                temperature.append(float(line_break[1]))
                salinity.append(float(line_break[2]))
                chlrophyll.append(float(line_break[8]))
                turbidity.append(float(line_break[9]))
                oxygen_sat.append(float(line_break[10]))
                oxygen.append(float(line_break[11]))

    return ctd_time, depth, salinity, temperature, chlrophyll, turbidity, oxygen_sat, oxygen


def grafico_perfis(depth, salinity, temperature, chlrophyll, turbidity, oxygen_sat, oxygen, n_perfil):

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

    ax1.plot(salinity, depth_g)
    ax2.plot(temperature, depth_g)
    ax3.plot(chlrophyll, depth_g)
    ax4.plot(turbidity, depth_g)
    ax5.plot(oxygen_sat, depth_g)

    axes = [ax1, ax2, ax3, ax4, ax5]
    labs = ['Salinity (psu)', 'Temperature (°C)', 'Chlorophyll (\u00b5g/L)', 'Turbidity (FTU)', 'Oxygen (%)']

    for i in range(len(axes)):
        axes[i].set_xlabel(labs[i])
        if i > 0:
            axes[i].set_yticklabels('')

    ax1.set_ylabel('Depth (m)')
    plt.show()

    ax6 = fig.add_axes([.1, .9, .1, .1])
    ax6.axis('off')
    ax6.text(.5, .5, 'Perfil' + str(n_perf), size=14, weight='bold')

    return fig
    plt.show()

for i in range(len(ctd_file)):
    a, b, c, d, e, f, g, h = carrega_ctd(path, ctd_file[i])

    fig = grafico_perfis(b, c, d, e, f, g, n_perfil)

    display.clear_output(wait=True)
    display.display(plt.gcf())
    time.sleep(.5)
    plt.close()
