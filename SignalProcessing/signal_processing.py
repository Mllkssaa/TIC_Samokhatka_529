import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
import os

#праметри варіант 13
n = 500
Fs = 1000
F_max = 27

#створ папки figures
if not os.path.exists("figures"):
    os.makedirs("figures")

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
def plot_graph(x, y, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.plot(x, y, linewidth=1)
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    plt.title(title, fontsize=14)
    fig.savefig('./figures/' + title + '.png', dpi=600)
    plt.close()

#5. побудова сигналу
plot_graph(time, filtered_signal,
           "Filtered signal (F_max=27Hz)",
           "Time (s)",
           "Amplitude")

#6. розрахунок спектру
spectrum = fft.fft(filtered_signal)
spectrum_shifted = np.abs(fft.fftshift(spectrum))

freqs = fft.fftfreq(n, 1/Fs)
freqs_shifted = np.abs(fft.fftshift(freqs))

#7. побудова спектру
plot_graph(freqs_shifted, spectrum_shifted,
           "Spectrum (Fmax=27Hz)",
           "Frequency (Hz)",
           "Magnitude")

print("Графіки успішно збережені у папку figures")