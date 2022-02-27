import numpy as np
import seaborn as sns

sns.set_theme()


def plot_curve(axis, alpha, beta, left, right, color):
    x = np.linspace(left, right, int(1e5))
    y = curve_function(x, alpha, beta, left, right)

    axis.plot(x, y, color=color, label='функция Q(x)')
    plot_minima(axis, alpha, beta, left, right)

    axis.set(xlabel=r'x',
             ylabel=r'Q(x)')

    axis.legend()


def curve_function(x, alpha, beta, A, B):
    return 1 / (2 * (B - A)) * (alpha*(x-A)**2 + beta*(B-x)**2)


def plot_minima(axis, alpha, beta, A, B, color='green'):
    x = (A*alpha + B*beta) / (alpha + beta)
    y = curve_function(x, alpha, beta, A, B)

    axis.plot(x, y, 'o', color=color, label=f'минимум ({x}, {y})')
