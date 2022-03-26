import numpy as np
import seaborn as sns

C = 18

# виды маркеров https://matplotlib.org/stable/api/markers_api.html
GLOBAL_PROPS = {
    'hist': {
        'color': '#69e089',
        'alpha': 0.8,
        'edgecolor': '#1ca340',
        'label': r'Реальное распределение',
    },
    'analytic': {
        'color': '#3f35d4',
        'alpha': 1.0,
        'linewidth': 2,
        'label': r'Аналитическое распределение',
    },
    'monte_carlo': {
        'color': '#d42086',
        'alpha': 1.0,
        'marker': '1',
        'markersize': 12,
        'label': r'$Функция\ Q_{мк}(x)$',
    },
    'monte_carlo_minima': {
        'color': '#d42086',
        'alpha': 1.0,
        'marker': 'd',
        'markersize': 12,
    },
    'monte_carlo_minima_label': lambda x, y: rf'$Минимум\ Q_{{мк}}(x)\ ({x:.3f}, {y:.3f})$',
    'deviation': {
        'color': '#16adc4',
        'alpha': 1.0,
        'marker': '.',
        'markersize': 12,
        'label': r'$Стандартное\ отклонение\ S(x)$'
    },
}


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


def plot_mc_and_deviation(axis, params):
    alpha = params['alpha']
    beta = params['beta']
    left = params['left']
    right = params['right']
    m = params['m']
    n = params['n']

    rng = np.random.default_rng()
    x = np.linspace(left, right, int(m) + 1)
    y = rng.triangular(left, C, right, int(n))

    vect_q_x_y = np.vectorize(q_x_y)
    y_q_x_y = np.array([vect_q_x_y(x_i, y, alpha, beta) for x_i in x])

    y_mc = monte_carlo(y_q_x_y, n)

    plot_monte_carlo(axis, x, y_mc)
    plot_deviation(axis, x, y_mc, y_q_x_y, n)

    axis.set(xlabel=r'$x$', ylabel=r'$Q(x)$')


def plot_monte_carlo(axis, x, y):
    global GLOBAL_PROPS

    plot_curve(axis, x, y, **GLOBAL_PROPS['monte_carlo'])

    plot_minima(
        axis, x, y, label=GLOBAL_PROPS['monte_carlo_minima_label'], **GLOBAL_PROPS['monte_carlo_minima'])


def plot_deviation(axis, x, y_mc, y_q_x_y, n):
    global GLOBAL_PROPS

    y = [np.sqrt(1/n * np.sum((y_mc[i] - y_q_x_y[i])**2))
         for i in range(len(x))]

    plot_curve(axis, x, y, **GLOBAL_PROPS['deviation'])


def plot_curve(axis, x, y, color, label, alpha, linewidth=2, marker='none', markersize=12):
    axis.plot(x, y, marker, color=color, label=label,
              markersize=markersize, alpha=alpha, linewidth=linewidth)


def plot_minima(axis, x, y, color, label, marker, markersize, alpha):
    min_index = np.argmin(y)

    axis.plot(x[min_index], y[min_index], marker, color=color, markersize=markersize,
              label=label(x[min_index], y[min_index]), alpha=alpha)


def q_x_y(x, y, alpha, beta):
    return alpha*(x - y) if x > y else beta*(y - x)


def monte_carlo(y, n):
    return 1 / n * np.array([np.sum(y_val) for y_val in y])


def plot_triangle_distribution(axis, params):
    global C

    rng = np.random.default_rng()

    x = rng.triangular(
        params['left'], C, params['right'], int(params['n']))

    sns.histplot(x, bins=20, ax=axis, stat='density', **GLOBAL_PROPS['hist'])

    axis.set(xlabel=r'$x$', ylabel=r'$\phi(x)$')


def plot_analytic_triangle(axis, params):
    global C

    A = params['left']
    B = params['right']

    def z(y):
        if (y < C):
            return 2 * (y - A) / ((B - A)*(C - A))
        else:
            return 2 * (y - B) / ((B - A)*(C - B))

    z_vect = np.vectorize(z)
    x = np.linspace(A, B, int(params['n']))
    y = z_vect(x)

    plot_curve(axis, x, y, **GLOBAL_PROPS['analytic'])
