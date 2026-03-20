import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from scipy.fft import fft, fftshift, fftfreq
import os

#праметри варіант 13
n = 500
Fs = 1000
F_max = 27
F_filter = 34

#створ папки figures
if not os.path.exists("figures"):
    os.makedirs("figures")


#-----ПРАКТИЧНА РОБОТА №2-----

#1. генерація випадкового сигналу
random_signal = np.random.normal(0, 10, n)

#2. часові відліки
time = np.arange(n) / Fs

#3. розрахунок ФНЧ (Butterworth)
w = F_max / (Fs / 2)   #нормована частота

sos = signal.butter(3, w, 'low', output='sos')

#4. фільтрація сигналу
filtered_signal = signal.sosfilt(sos, random_signal)

#функція побудови графіку
def plot_graph(x, y, name, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.plot(x, y)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.title(name)
    fig.savefig(f'./figures/{name}.png', dpi=600)
    plt.close()

#5. побудова сигналу
plot_graph(time, filtered_signal,"Filtered signal (F_max=27Hz)","Time (s)","Amplitude")

#6. розрахунок спектру
spectrum = fft(filtered_signal)
freqs = fftfreq(n, d=1/Fs)


#7. побудова спектру
plot_graph(fftshift(freqs), np.abs(fftshift(spectrum)),
           "Spectrum", "Frequency (Hz)", "Magnitude")

print("Графіки пр 2 успішно збережені у папку figures")



#-----ПРАКТИЧНА РОБОТА №3-----

Dt_values = [2, 4, 8, 16]

discrete_signals = []
discrete_spectrums = []
restored_signals = []
variances = []
snr_values = []


#частоти для спектру
freqs = fftfreq(n, d=1/Fs)
freqs_shifted = fftshift(freqs)

#---- Основний цикл ----
for Dt in Dt_values:

    #1. дискретний сигнал
    discrete_signal = np.zeros(n)

    for i in range(int(n / Dt)):
        discrete_signal[i * Dt] = filtered_signal[i * Dt]

    discrete_signals.append(discrete_signal)

    #2. спектр
    spectrum = fft(discrete_signal)
    discrete_spectrums.append(np.abs(fftshift(spectrum)))

    #3. відновлення сигналу
    w = F_filter / (Fs / 2)
    sos = signal.butter(3, w, 'low', output='sos')
    restored = signal.sosfiltfilt(sos, discrete_signal)
    restored_signals.append(restored)

    #4. похибка
    error = restored - filtered_signal

    var_signal = np.var(filtered_signal)
    var_error = np.var(error)

    variances.append(var_error)
    snr_values.append(var_signal / var_error if var_signal != 0 else 0)

    #--- Графік1: Дискретні сигнали ---
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    for axis, sig, dt in zip(ax.flat, discrete_signals, Dt_values):
        axis.plot(time, sig)
        axis.set_title(f"Dt = {dt}")
    fig.savefig('./figures/discrete_signals.png', dpi=600)
    plt.close()

    #--- Графік2: Спектри ---
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    for axis, spec, dt in zip(ax.flat, discrete_spectrums, Dt_values):
        axis.plot(freqs_shifted, spec)
        axis.set_title(f"Dt = {dt}")
    fig.savefig('./figures/discrete_spectrums.png', dpi=600)
    plt.close()

    #--- Графік3: Відновлені сигнали ---
    fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
    for axis, sig, dt in zip(ax.flat, restored_signals, Dt_values):
        axis.plot(time, sig)
        axis.set_title(f"Dt = {dt}")
    fig.savefig('./figures/restored_signals.png', dpi=600)
    plt.close()

    #--- Графік4: Дисперсія ---
    plt.figure(figsize=(21 / 2.54, 14 / 2.54))
    plt.plot(Dt_values[:len(variances)], variances, marker='o')
    plt.title("Variance vs Dt")
    plt.xlabel("Dt")
    plt.ylabel("Variance")
    plt.savefig('./figures/variance_vs_dt.png', dpi=600)
    plt.close()

    #--- Графік5: SNR ---
    plt.figure(figsize=(21 / 2.54, 14 / 2.54))
    plt.plot(Dt_values[:len(variances)], variances, marker='o')
    plt.title("SNR vs Dt")
    plt.xlabel("Dt")
    plt.ylabel("SNR")
    plt.savefig('./figures/snr_vs_dt.png', dpi=600)
    plt.close()

    print("Практична робота №3. Усі графіки збережені у папку figures")
