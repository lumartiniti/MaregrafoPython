import os
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import IPython.display as display
from fontTools.misc.cython import returns
from scipy.interpolate import griddata

path = r'C:/Users/luima/OneDrive/Documentos/dados_python/ODV_data/csv/'

mydir = os.listdir(path)

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

    return ctd_time, depth, salinity, temperature, chlorophyll, turbidity, oxygen_sat, oxygen
