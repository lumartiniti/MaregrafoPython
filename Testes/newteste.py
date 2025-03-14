import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
from scipy.interpolate import griddata

# 1. Definir diretório dos dados e verificar existência
path = r'C:/Users/luima/OneDrive/Documentos/dados_python/ODV_data/csv/'
if not os.path.exists(path):
    raise FileNotFoundError(f"O diretório especificado não existe: {path}")

files = [f for f in os.listdir(path) if f.endswith('.csv')]
if not files:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado no diretório especificado.")


# 2. Função para carregar dados do arquivo
def carrega_ctd(filename):
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Extrair data e hora do perfil
    ctd_time = None
    for line in lines:
        if line.startswith("StartTime="):
            date_time = line.split('=')[1].strip()
            try:
                ctd_time = datetime.datetime.strptime(date_time, "%Y/%m/%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Formato de data inválido no arquivo {filename}: {date_time}")
            break
    if ctd_time is None:
        raise ValueError(f"Data e hora não encontradas no arquivo {filename}")

    # Carregar dados do perfil
    depth, temp, sal, chl, turb, do_sat, do_mg = [], [], [], [], [], [], []
    for line in lines[44:]:  # Ignorar cabeçalho
        values = line.strip().split(',')
        if len(values) < 7:
            continue  # Pular linhas incompletas
        try:
            depth.append(float(values[0]))
            temp.append(float(values[1]))
            sal.append(float(values[2]))
            chl.append(float(values[3]))
            turb.append(float(values[4]))
            do_sat.append(float(values[5]))
            do_mg.append(float(values[6]))
        except ValueError:
            continue  # Ignorar linhas com valores inválidos

    return ctd_time, np.array(depth), np.array(temp), np.array(sal), np.array(chl), np.array(turb), np.array(
        do_sat), np.array(do_mg)


# 3. Função para gerar gráfico de perfil vertical
def grafico_perfil(depth, variable, label, title):
    plt.figure(figsize=(5, 7))
    plt.plot(variable, depth, marker='o')
    plt.gca().invert_yaxis()
    plt.xlabel(label)
    plt.ylabel("Profundidade (m)")
    plt.title(title)
    plt.grid()
    plt.show()


# 4. Processar arquivos e gerar gráficos individuais
for file in files:
    ctd_time, depth, temp, sal, chl, turb, do_sat, do_mg = carrega_ctd(file)
    print(f"Processando {file} - {ctd_time}")

    # Gerar gráficos
    grafico_perfil(depth, temp, "Temperatura (°C)", f"Perfil de Temperatura - {ctd_time}")
    grafico_perfil(depth, sal, "Salinidade (PSS-78)", f"Perfil de Salinidade - {ctd_time}")
    grafico_perfil(depth, chl, "Clorofila (ug/L)", f"Perfil de Clorofila - {ctd_time}")
    grafico_perfil(depth, turb, "Turbidez (NTU)", f"Perfil de Turbidez - {ctd_time}")
    grafico_perfil(depth, do_sat, "Oxigênio Dissolvido (%)", f"Perfil de OD Saturação - {ctd_time}")
    grafico_perfil(depth, do_mg, "Oxigênio Dissolvido (mg/L)", f"Perfil de OD - {ctd_time}")

# 5. Interpolação para matriz regular
tempo_total, profundidade_total, salinidade_total = [], [], []
for file in files:
    ctd_time, depth, _, sal, _, _, _, _ = carrega_ctd(file)
    tempo_total.extend([ctd_time.timestamp()] * len(depth))
    profundidade_total.extend(depth)
    salinidade_total.extend(sal)

# Criar malha de interpolação
tempo_grid = np.linspace(min(tempo_total), max(tempo_total), 20)
profundidade_grid = np.linspace(min(profundidade_total), max(profundidade_total), 20)
T, P = np.meshgrid(tempo_grid, profundidade_grid)

# Interpolação dos dados
sal_interp = griddata((tempo_total, profundidade_total), salinidade_total, (T, P), method='cubic')

# 6. Gerar gráfico final de distribuição de salinidade
plt.figure(figsize=(10, 6))
plt.contourf(T, P, sal_interp, cmap='viridis', levels=20)
plt.colorbar(label='Salinidade (PSS-78)')
plt.xlabel('Tempo (s)')
plt.ylabel('Profundidade (m)')
plt.gca().invert_yaxis()
plt.title('Distribuição Temporal e Vertical da Salinidade')
plt.grid()
plt.show()
