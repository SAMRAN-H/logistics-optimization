import numpy as np
import seaborn as sns


def set_axis_props(axis, facecolor='white', tick_color='black', spine_color='black', grid_color='grey', hide_ticks=True):
    axis.set_facecolor(facecolor)
    axis.tick_params(axis='x', colors=tick_color)
    axis.tick_params(axis='y', colors=tick_color)

    axis.spines['bottom'].set_color(spine_color)
    axis.spines['left'].set_color(spine_color)
    axis.spines['top'].set_color(None)
    axis.spines['right'].set_color(None)

    if hide_ticks:
        axis.tick_params(length=0)

    axis.grid(color=grid_color, linestyle='-', linewidth=0.25, alpha=0.6)


def plot_curve(axis, alpha, beta, left, right, color):
    x = np.linspace(left, right, int(1e5))
    y = curve_function(x, alpha, beta, left, right)

    axis.plot(x, y, color=color, label='функция Q(x)')
    plot_minima(axis, alpha, beta, left, right)

    axis.set(xlabel=r'x',
             ylabel=r'Q(x)')

    axis.legend(frameon=False)
    axis.grid(True)


def curve_function(x, alpha, beta, A, B):
    return 1 / (2 * (B - A)) * (alpha*(x-A)**2 + beta*(B-x)**2)


def plot_minima(axis, alpha, beta, A, B, color='green'):
    x = (A*alpha + B*beta) / (alpha + beta)
    y = curve_function(x, alpha, beta, A, B)
    y_lim = axis.get_ylim()

    axis.plot(x, y, 'o', color=color, label=f'Минимум функции')
    axis.annotate(rf'$({x:.2f}, {y:.2f})$',
                  (x, y + (y_lim[1] - y_lim[0]) / 30), ha='center')
