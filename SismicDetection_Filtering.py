import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog, Tk, Button, Label, Entry, StringVar
from obspy import read
from obspy.signal.trigger import classic_sta_lta, trigger_onset
from datetime import datetime, timedelta

#cat_directory= r'E:\braym\Downloads\Club\NasaChallenge\space_apps_2024_seismic_detection\space_apps_2024_seismic_detection\data\mars\training\catalogs/'

#cat_file= cat_directory + 'Mars_InSight_training_catalog_final.csv'

#cat = pd.read_csv(cat_file)

#row = cat.iloc[0]
#arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'], '%Y-%m-%dT%H:%M:%S.%f')

#test_filename = row.filename
#test_filename = test_filename.replace('.csv', '.mseed')
#data_directory = r'E:\braym\Downloads\Club\NasaChallenge\space_apps_2024_seismic_detection\space_apps_2024_seismic_detection\data\mars\training\data/'
#mseed_file = f'{data_directory}{test_filename}'
#st = read(mseed_file)
#st[0].stats

#tr = st.traces[0].copy()
#tr_times = tr.times()
#tr_data = tr.data

##starttime = tr.stats.starttime.datetime
#arrival = (arrival_time - starttime).total_seconds()

#fig,ax = plt.subplots(1,1,figsize=(10,3))

#ax.plot(tr_times,tr_data)

#ax.axvline(x = arrival, color= 'red', label='Rel. Arrival')
#ax.legend(loc='upper left')

#ax.set_xlim([min(tr_times),max(tr_times)])
#ax.set_ylabel('Velocity (m/s)')
#ax.set_xlabel('Time (s)')
#ax.set_title(f'{test_filename}', fontweight='bold')
#plt.show()"""



# Crear ventana principal usando Tkinter
root = Tk()
root.title("Sismic Analizer")
root.geometry("400x300")

# Variables para almacenar las entradas del usuario

minfreq_var = StringVar(value="0")
maxfreq_var = StringVar(value="0")
sta_len_var = StringVar(value="0")
lta_len_var = StringVar(value="0")
thr_on_var = StringVar(value="0")
thr_off_var = StringVar(value="0")
file_path_var = StringVar()

# Función para seleccionar el archivo .mseed
    
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("MSEED files", "*.mseed")])
    file_path_var.set(file_path)

# Función para realizar el análisis con los parámetros del usuario
def analyze():
    file_path = file_path_var.get()
    minfreq = float(minfreq_var.get())
    maxfreq = float(maxfreq_var.get())
    sta_len = float(sta_len_var.get())
    lta_len = float(lta_len_var.get())
    thr_on = float(thr_on_var.get())
    thr_off = float(thr_off_var.get())

    # Mantener el resto de tu código original aquí con los parámetros seleccionados
    st = read(file_path)
    tr = st.traces[0].copy()
    tr_times = tr.times()
    tr_data = tr.data
    ##starttime = tr.stats.starttime.datetime

    # Aplicar filtro de banda paso
    st_filt = st.copy()
    st_filt.filter('bandpass', freqmin=minfreq, freqmax=maxfreq)
    tr_filt = st_filt.traces[0].copy()
    tr_times_filt = tr_filt.times()
    tr_data_filt = tr_filt.data

    # Calcular STA/LTA
    df = tr.stats.sampling_rate
    cft = classic_sta_lta(tr_data, int(sta_len * df), int(lta_len * df))

    # Definir umbrales para detección de eventos
    on_off = np.array(trigger_onset(cft, thr_on, thr_off))

    # Graficar todo en un solo plot
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    #ax.plot(tr_times, tr_data, label='Seismogram')
    ax.plot(tr_times, cft, color='blue', label='STA/LTA Characteristic', alpha=0.75)

    # Marcar los triggers "on" y "off"
    for i in np.arange(0, 1):
        triggers = on_off[i]
        ax.axvline(x=tr_times[triggers[0]], color='green', label='Trig. On' if i == 0 else "")
        ax.axvline(x=tr_times[triggers[1]], color='purple', label='Trig. Off' if i == 0 else "")

    ax.set_xlim([min(tr_times), max(tr_times)])
    ax.set_ylabel('Velocity / STA/LTA')
    ax.set_xlabel('Time (s)')
    ax.set_title(f'Seismogram and STA/LTA Detection for {file_path}')
    ax.legend()

    plt.show()

#
    

# Interfaz para seleccionar archivo
Label(root, text="MSEED Document:", font=("Helvetica", 12, "bold")).pack(pady=5)
Button(root, text="Select Document", command=select_file, font=("Helvetica", 12)).pack(pady=5)

# Parámetros de filtro
Label(root, text="Min Frequency (Hz):", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=minfreq_var, font=("Helvetica", 12)).pack(pady=5)

Label(root, text="Max Frequency (Hz):", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=maxfreq_var, font=("Helvetica", 12)).pack(pady=5)

# Parámetros de STA/LTA
Label(root, text="STA Len (s):", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=sta_len_var, font=("Helvetica", 12)).pack(pady=5)

Label(root, text="LTA Len (s):", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=lta_len_var, font=("Helvetica", 12)).pack(pady=5)

# Umbrales para eventos
Label(root, text="Threshold On:", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=thr_on_var, font=("Helvetica", 12)).pack(pady=5)

Label(root, text="Threshold Off:", font=("Helvetica", 12)).pack(pady=5)
Entry(root, textvariable=thr_off_var, font=("Helvetica", 12)).pack(pady=5)

# Botón para ejecutar el análisis
Button(root, text="Create", command=analyze, font=("Helvetica", 12, "bold")).pack(pady=20)

# Iniciar el loop de la interfaz
root.mainloop()
