import os
import numpy as np
import matplotlib.pyplot as plt
import datetime

path = r'C:/Users/luima/OneDrive/Documentos/dados_python/ODV_data/csv/'

mydir = os.listdir(path) # Lista os arquivos e diretório do caminho.

ctd_file = []
for file in mydir:
    if file.endswith('.Csv'):
        ctd_file.append(file)

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

import time
import pylab as pl
from IPython import display
for i in range(3):
    pl.plot(pl.randn(100))
    display.clear_output(wait=True)
    display.display(pl.gcf())
    time.sleep(1.0)

time =[]
depth = []
temperature = []
salinity = []
chlorophyll = []
turbidity = []
oxygen_sat = []
oxygen = []

for i in range(len(ctd_file) - 1):
    a, b, c, d, e, f, g, h = carrega_ctd(path, ctd_file[i])

    time_b = a.hour + a.minute / 60
    time_b = np.linspace(time_b, time_b, len(b))

    time_b = time_b[5:-1]
    b = b[5:-1]
    c = c[5:-1]
    d = d[5:-1]
    e = e[5:-1]
    f = f[5:-1]
    g = g[5:-1]
    h = h[5:-1]

    time = np.append(time, time_b)
    depth = np.append(depth, b)
    salinity = np.append(salinity, c)
    temperature = np.append(temperature, d)
    chlorophyll = np.append(chlorophyll, e)
    turbidity = np.append(turbidity, f)
    oxygen_sat = np.append(oxygen_sat, g)
    oxygen = np.append(oxygen, h)

ti = np.linspace(np.min(time), np.max(time), 20)
zi = np.linspace(np.min(depth), np.max(depth), 20)

tt, zz = np.meshgrid(ti, zi)

points = [time, depth]
points = np.reshape(points, (2, -1))
points = np.transpose(points)

salinity_i = griddata(points, salinity, (tt, zz), method='linear')


plt.rcParams.update({'font.size': 18})
fig = plt.figure(figsize=(10, 5))

ax1 = fig.add_axes([.1, .1, .8, .8])
ax1cb = fig.add_axes([.92, .1, .03, .8])

ax1.plot(time, -depth, 'k', markesize=1)

cont = ax1.contourf(ti, -zi, salinity_i, cmap='rainbow')
plt.colorbar(cont, cax=ax1cb)

ax1.set_xlabel('Time (hrs)')
ax1.set_ylabel('Depth (m)')
ax1.set_title('Salinity (psu)')
plt.show()