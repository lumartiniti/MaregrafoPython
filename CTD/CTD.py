import os
import numpy as np
import matplotlib.pyplot as plt
import datetime

from IPython import display
from jedi.api.refactoring import inline

from CTD.testectd import depth, oxygen
from distr_sal_vertical import carrega_ctd

path = r'C:/Users/luima/OneDrive/Documentos/dados_python/ODV_data/csv/'

mydir = os.listdir(path) # Lista os arquivos e diretório do caminho.

ctd_file = []
for file in mydir:
    if file.endswith('.Csv'):
        ctd_file.append(file)

def carrega_ctd(path, ctd_file):
    with open(path + ctd_file[0]) as file: # abre o arquivo especificado.
        c = 0

        depth = []
        temperature = []
        salinity = []
        chlorophyll = []
        turbidity = []
        oxygen_sat = []
        oxygen = []

        for line in file:

            if line[0:10] == "StartTime=":

                date_time = line

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
                chlorophyll.append(float(line_break[8]))
                turbidity.append(float(line_break[9]))
                oxygen_sat.append(float(line_break[10]))
                oxygen.append(float(line_break[11]))

    return ctd_time, depth, salinity, temperature, chlorophyll, turbidity, oxygen_sat, oxygen

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
ax3.plot(chlorophyll, depth_g)
ax4.plot(turbidity, depth_g)
ax5.plot(oxygen_sat, depth_g)

axes = [ax1, ax2, ax3, ax4, ax5]
labs = ['Salinity (psu)', 'Temperature (°C)', 'Chlorophyll-a (g/L)', 'Turbidity (FTU)', 'Oxygen (%)']

for i in range(len(axes)):
    axes[i].set_xlabel(labs[i])
    if i > 0:
        axes[i].set_yticklabels('')

ax1.set_ylabel('Depth (m)')
plt.show()

# Gera imagem 1

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
    ax3.plot(chlorophyll, depth_g)
    ax4.plot(turbidity, depth_g)
    ax5.plot(oxygen, depth_g)

    axes = [ax1, ax2, ax3, ax4, ax5]
    labs = ['Salinity (psu)', 'Temperature (°C)', 'Chlorophyll-a (g/L)', 'Turbidity (FTU)', 'Oxygen (%)']

    for i in range(len(axes)):
        axes[i].set_xlabel(labs[i])
        if i > 0:
            axes[i].set_yticklabels('')

    ax1.set_ylabel('Depth (m)')
    plt.show()

