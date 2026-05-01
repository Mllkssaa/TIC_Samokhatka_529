import numpy as np
import matplotlib.pyplot as plt

# функція побудови графіків
#----------
def select_plot(plot_type, t, signal, linewidth=1.0):

    if plot_type == 'continuous':
        plt.plot(t, signal, linewidth=linewidth)
    elif plot_type == 'discrete':
        plt.stem(t, signal)

    plt.grid()


#1. cos сигнал
#----------
SAMPLES = 3200
t = np.linspace(0, 5, SAMPLES, endpoint=True)

signal_cos = np.cos(2 * np.pi * t)

plt.figure(figsize=(8, 3))
select_plot('continuous', t, signal_cos, 2.0)
plt.title("cos(2nt)")
plt.show()


#2. дельта-послідовність
#----------
delta_40 = np.zeros(SAMPLES)
delta_50 = np.zeros(SAMPLES)
delta_100 = np.zeros(SAMPLES)

delta_40[::40] = 1
delta_50[::50] = 1
delta_100[::100] = 1


#3. дискретизація
#----------
sampled_40 = signal_cos * delta_40
sampled_50 = signal_cos * delta_50
sampled_100 = signal_cos * delta_100


#4. графіки
#----------
plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
select_plot('discrete', t, sampled_40)
plt.title("n = 40")

plt.subplot(3, 1, 2)
select_plot('discrete', t, sampled_50)
plt.title("n = 50")

plt.subplot(3, 1, 3)
select_plot('discrete', t, sampled_100)
plt.title("n = 100")

plt.tight_layout()
plt.show()


#5. квантування
#----------
def quantize_uniform(signal_ampl, quant_min=-1.0, quant_max=1.0, quant_level=4):
    x_normalize = (signal_ampl - quant_min) * (quant_level - 1) / (quant_max - quant_min)

    x_normalize[x_normalize > quant_level - 1] = quant_level - 1
    x_normalize[x_normalize < 0] = 0

    x_normalize_quant = np.around(x_normalize)

    x_quant = x_normalize_quant * (quant_max - quant_min) / (quant_level - 1) + quant_min

    return x_quant


#6. функція графіка квантування
#----------
def plot_graph_quant_function(axis, quant_min=-1.0, quant_max=1.0, quant_level=256):
    x_cont = np.linspace(quant_min, quant_max, 1000)
    x_quant = quantize_uniform(x_cont, quant_min, quant_max, quant_level)

    error = np.abs(x_quant - x_cont)

    axis.plot(x_cont, x_cont, label='Original')
    axis.plot(x_cont, x_quant, label='Quantized')
    axis.plot(x_cont, error, '--', label='Error')

    axis.set_title(f"L={quant_level}")
    axis.grid()
    axis.legend()


#7. L = 8,16,32,64
#----------
plt.figure(figsize=(16, 4))

levels = [8, 16, 32, 64]

for i, in enumerate(levels):
    ax = plt.subplot(1, 4, i + 1)
    plot_graph_quant_function(ax, quant_level=L)

plt.tight_layout()
plt.show()


#8. квантування синусоїди
#----------
signal_sin = np.sin(2 * np.pi * t)

x_quant = quantize_uniform(signal_sin, -1, 1, 8)

plt.figure(figsize=(8, 3))
plt.plot(t, signal_sin, label='Original')
plt.plot(t, x_quant, '.', label='Quantized')

plt.legend()
plt.grid()
plt.show()