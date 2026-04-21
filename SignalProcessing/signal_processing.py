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


#-----ПРАКТИЧНА РОБОТА №4-----
quantized_signals = []
variances_q = []
snr_q = []

for M in [4, 16, 64, 256]:

    bits = []

    #--- крок квантування ---
    delta = (np.max(filtered_signal) - np.min(filtered_signal)) / (M - 1)

    #--- квантування ---
    quantize_signals = delta * np.round(filtered_signal / delta)

    #--- рівні ---
    quantize_levels = np.arange(np.min(quantize_signals),
                                np.max(quantize_signals) + delta,
                                delta)
    #--- біти ---
    quantize_bit = np.arange(0, M)
    n_bits = int(np.log2(M))
    quantize_bit = [format(b, '0' + str(n_bits) + 'b') for b in quantize_bit]

    #--- таблиця ---
    quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

    fig, ax = plt.subplots(figsize=(14/2.54, M/2.54))
    table = ax.table(cellText=quantize_table,
                     colLabels=['Signal value', 'Code'],
                     loc='center')
    table.set_fontsize(10)
    table.scale(1, 1.5)
    ax.axis('off')
    fig.savefig('./figures/quant_table_M{M}.png', dpi=600)

    #--- кодування сигналу ---
    for s in quantize_signals:
        for i, val in enumerate(quantize_levels[:M]):
            if np.round(abs(s - val), 5) == 0:
                bits.append(quantize_bit[i])
                break

    #--- перетворення у масив бітів ---
    bits = [int(b) for b in ''.join(bits)]

    #--- графік бітів ---
    fig, ax = plt.subplots(figsize=(21/2.54, 14/2.54))
    ax.step(np.arange(len(bits)), bits, linewidth=0.5)
    ax.set_title(f'Bit sequence M={M}')
    ax.set_xlabel('Index')
    ax.set_ylabel('Bit')
    fig.savefig('./figures/bits_M{M}.png', dpi=600)
    plt.close()

    #--- дисперсія ---
    noise = filtered_signal - quantize_signals
    variance = np.var(noise)
    variances_q.append(variance)

    #--- SNR ---
    signal_power = np.mean(filtered_signal**2)
    noise_power = np.mean(noise**2)
    snr_value = signal_power / noise_power if noise_power != 0 else 0
    snr_q.append(snr_value)

    quantized_signals.append(quantize_signals)

#--- графік сигналів ---
plt.figure(figsize=(21/2.54, 14/2.54))
for i, M in enumerate([4, 16, 64, 256]):
    plt.plot(time, quantized_signals[i], label=f'M={M}')
plt.legend()
plt.title('Quantized signals')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.savefig('./figures/quantized_signals.png', dpi=600)
plt.close()

#--- дисперсія ---
plt.figure(figsize=(21/2.54, 14/2.54))
plt.plot([4, 16, 64, 256], variances_q, marker='o')
plt.title('Variances vs M')
plt.xlabel('M')
plt.ylabel('Variance')
plt.savefig('./figures/variances_vs_M.png', dpi=600)
plt.close()

#--- SNR ---
plt.figure(figsize=(21/2.54, 14/2.54))
plt.plot([4, 16, 64, 256], snr_q, marker='o')
plt.title('SNRs vs M')
plt.xlabel('M')
plt.ylabel('SNR')
plt.savefig('./figures/snr_vs_M.png', dpi=600)
plt.close()

print("Практична робота №4. Усі графіки збережено у папку figures")
