import numpy as np
from matplotlib import pyplot as plt

#дані
X = np.linspace(-np.pi, np.pi, 256, endpoint=True)
C, S = np.cos(X), np.sin(X)

#subplot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))

#---графік cos---
ax1.set_title('Функція cos(x)', fontsize=12)
ax1.plot(X, C, color='pink', label='cos(x)', linewidth=2)

#екстремуми cos
cos_max_x = 0
cos_min_x = np.pi

ax1.scatter([cos_max_x, cos_min_x], [1, -1], color='pink')
ax1.vlines([cos_max_x, cos_min_x], 0, [1, -1],
           linestyles='dashed', color='pink')

ax1.set_xlim(-np.pi, np.pi)
ax1.set_ylim(-1.2, 1.2)
ax1.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax1.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
ax1.set_ylabel('Амплітуда')
ax1.legend()
ax1.grid(True)

#---графік sin---
ax2.set_title('Функція sin(x)', fontsize=12)
ax2.plot(X, S, color='black', label='sin(x)', linewidth=2)

#екстремуми sin
sin_max_x = np.pi / 2
sin_min_x = np.pi / 2

ax2.scatter([sin_max_x, sin_min_x], [1, -1], color='black')
ax2.vlines([sin_max_x, sin_min_x], 0, [1, -1],
           linestyles='dashed', color='black')

#оформлення
ax2.set_xlim(-np.pi, np.pi)
ax2.set_ylim(-1.2, 1.2)
ax2.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
ax2.set_xticklabels([r'$-\pi$', r'$-\pi/2$', r'$0$', r'$+\pi/2$', r'$+\pi$'])
ax2.set_xlabel('Кут (радіани)')
ax2.set_ylabel('Амплітуда')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
