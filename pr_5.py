import numpy as np
import matplotlib.pyplot as plt

T = 200
x = np.zeros(T)
x[:T//2] = 1
x[T//2:] = -1

t = np.arange(T)

plt.figure(figsize=(8, 3))
plt.plot(x)
plt.grid(True)
plt.title('Прямокутний сигнал')
plt.show()

def fourier_coeff(signal, n_harmonics):
    """Обчислення коефіцієнтів Фур'є a_n та b_n"""
    T = len(signal)
    t = np.arange(T)

    coeffs = []

    a0 = 2 / T * np.sum(signal)
    coeffs.append([a0, 0])

    for n in range(1, n_harmonics + 1):
        an = 2 / T * np.sum(signal * np.cos(2 * np.pi * n * t / T))
        bn = 2 / T * np.sum(signal * np.sin(2 * np.pi * n * t / T))
        coeffs.append([an, bn])

    return np.array(coeffs)

def reconstruct(T, coeffs):
    """Відновлення сигналу за коефіцієнтами"""
    t = np.arange(T)
    y = np.ones(T) * coeffs[0, 0] / 2

    for n in range(1, len(coeffs)):
        an, bn = coeffs[n]
        y += an * np.cos(2 * np.pi * n * t / T)
        y += bn * np.sin(2 * np.pi * n * t / T)

    return y

Fcoeff = fourier_coeff(x, 20)

plt.figure(figsize=(10, 5))
plt.plot(x, 'b', label='Початковий сигнал', lw=2)
plt.plot(t, reconstruct(T, Fcoeff[:5]), label='5 гармонік')
plt.plot(t, reconstruct(T, Fcoeff[:20]), label='20 гармонік')
plt.grid(True)
plt.ylabel('$x(t)$')
plt.xlabel('$t$')
plt.legend()
plt.title('Відновлення прямокутного сигналу рядом Фур\'є')
plt.show()