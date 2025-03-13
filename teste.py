import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import datetime
import time
from IPython.display import display, clear_output

diretorio = r'C:/Users/luima/OneDrive/Documentos/dados_python.csv'
mydir = os.listdir(diretorio)
ctd_file = []

for file in mydir:
    if file.endswith('.Csv'):
        ctd_file.append(file)

print(ctd_file)


def carregar_dados_ctd(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("StartTime="):
            date_time = line.split('=')[1].strip()
            ctd_time = datetime.datetime.strptime(date_time, "%Y/%m/%d %H:%M:%S")
            break

    depth = []
    temp = []
    sal = []
    chl = []
    turb = []
    do_sat = []
    do_mgl = []

    data_section = False
    for line in lines:
        if data_section:
            values = line.strip().split(',')
            depth.append(float(values[0]))
            temp.append(float(values[1]))
            sal.append(float(values[2]))
            chl.append(float(values[3]))
            turb.append(float(values[4]))
            do_sat.append(float(values[5]))
            do_mgl.append(float(values[6]))

        if line.startswith("Depth [m]"):
            data_section = True

    return ctd_time, depth, temp, sal, chl, turb, do_sat, do_mgl


def plot_perfil(depth, temp, sal, chl, turb, do_sat, do_mgl, filename):
    fig, axs = plt.subplots(1, 6, figsize=(15, 5), sharey=True)
    axs[0].plot(temp, depth, 'r-')
    axs[0].set_xlabel("Temp (°C)")
    axs[1].plot(sal, depth, 'b-')
    axs[1].set_xlabel("Salinidade")
    axs[2].plot(chl, depth, 'g-')
    axs[2].set_xlabel("Chl-a")
    axs[3].plot(turb, depth, 'y-')
    axs[3].set_xlabel("Turbidez")
    axs[4].plot(do_sat, depth, 'c-')
    axs[4].set_xlabel("DO [%]")
    axs[5].plot(do_mgl, depth, 'm-')
    axs[5].set_xlabel("DO [mg/L]")

    for ax in axs:
        ax.invert_yaxis()

    plt.suptitle(filename)
    plt.show()
    return fig


tempos = []
profundidades = []
salinidades = []

for file in ctd_file:
    filepath = os.path.join(diretorio, file)
    ctd_time, depth, temp, sal, chl, turb, do_sat, do_mgl = carregar_dados_ctd(filepath)
    tempos.extend([ctd_time.timestamp() ] * len(depth))
    profundidades.extend(depth)
    salinidades.extend(sal)

time_grid = np.linspace(min(tempos), max(tempos), 20)
prof_grid = np.linspace(min(profundidades), max(profundidades), 100)
time_mesh, prof_mesh = np.meshgrid(time_grid, prof_grid)

salinidade_interp = griddata((tempos, profundidades), salinidades, (time_mesh, prof_mesh), method='cubic')

plt.figure(figsize=(10, 6))
plt.contourf(time_mesh, prof_mesh, salinidade_interp, cmap='viridis')
plt.colorbar(label="Salinidade (PSU)")
plt.xlabel("Tempo")
plt.ylabel("Profundidade (m)")
plt.title("Distribuição Temporal e Vertical da Salinidade")
plt.gca().invert_yaxis()
plt.show()


