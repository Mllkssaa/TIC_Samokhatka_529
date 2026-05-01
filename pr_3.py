import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, norm, rayleigh, poisson


#ПАРАМЕТРИ(варіант 13)
variant = 13

a, b = 2, 6          #рівномірний
mu, sigma = 12, 13   #нормальний
rayleigh_sigma = variant
poisson_lambda = variant

N_values = [1000, 10000, 100000]


#ФУНКЦІЇ
def analyze(data, title, N):
    print(f"\n--- {title} (N={N}) ---")
    print("Mean:", np.mean(data))
    print("Variance:", np.var(data))
    print("Skewness:", skew(data))
    print("Kurtosis:", kurtosis(data))


def plot_hist(data, dist_func, title, N):
    plt.figure()
    plt.hist(data, bins=50, density=True, alpha=0.6)

    x = np.linspace(min(data), max(data), 1000)
    plt.plot(x, dist_func(x), 'r')

    plt.title(f"{title} (N={N})")
    plt.grid()
    plt.show()


#ЛІНІЙНИЙ КОНГРУЕНТНИЙ МЕТОД
def lcg(n, seed=1, a=1664525, c=1013904223, m=2**32):
    numbers = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        numbers.append(x / m)
    return np.array(numbers)



#ОСНОВНИЙ ЦИКЛ
for N in N_values:
    print(f"\n========== N = {N} ==========")

    #1.РІВНОМІРНИЙ
    uniform = np.random.uniform(a, b, N)
    analyze(uniform, "Uniform", N)
    plot_hist(
        uniform,
        lambda x: np.ones_like(x) * (1 / (b - a)),
        "Uniform",
        N
    )

    #2.НОРМАЛЬНИЙ
    normal = np.random.normal(mu, sigma, N)
    analyze(normal, "Normal", N)
    plot_hist(
        normal,
        lambda x: norm.pdf(x, mu, sigma),
        "Normal",
        N
    )

    #3.РЕЛЕЯ
    ray = rayleigh.rvs(scale=rayleigh_sigma, size=N)
    analyze(ray, "Rayleigh", N)
    plot_hist(
        ray,
        lambda x: rayleigh.pdf(x, scale=rayleigh_sigma),
        "Rayleigh",
        N
    )

    #4.ПУАССОН
    pois = poisson.rvs(mu=poisson_lambda, size=N)
    analyze(pois, "Poisson", N)

    plt.figure()
    plt.hist(pois, bins=30, density=True, alpha=0.6)
    x = np.arange(min(pois), max(pois) + 1)
    plt.plot(x, poisson.pmf(x, poisson_lambda), 'r')
    plt.title(f"Poisson (N={N})")
    plt.grid()
    plt.show()

    #5.LCG (рівномірний)
    lcg_data = lcg(N)
    analyze(lcg_data, "LCG Uniform", N)

    plt.figure()
    plt.hist(lcg_data, bins=50, density=True, alpha=0.6)
    plt.title(f"LCG Uniform (N={N})")
    plt.grid()
    plt.show()