import numpy as np
import seaborn as sns


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
        'label': r'$Q_{мк}(x)$ треугольное',
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
    'monte_carlo_uniform': {
        'color': '#1bde4f',
        'alpha': 1.0,
        'marker': '+',
        'markersize': 12,
        'label': r'$Q_{мк}(x)$ равномерное',
    },
    'monte_carlo_uniform_minima': {
        'color': '#1bde4f',
        'alpha': 1.0,
        'marker': '*',
        'markersize': 12,
    },
    'monte_carlo_uniform_minima_label': lambda x, y: rf'$Минимум\ Q_{{мк}}(x)\ ({x:.3f}, {y:.3f})$',
    'mean': r'$\bar{x}$ =',
    'std': r'$\sigma$ ='
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
    C = params['c']

    x = np.linspace(left, right, int(m) + 1)
    y = get_real_distribution(left, right, int(n), C)

    vect_q_x_y = np.vectorize(q_x_y)
    y_q_x_y = np.array([vect_q_x_y(x_i, y, alpha, beta) for x_i in x])

    y_mc = monte_carlo(y_q_x_y, n)

    plot_monte_carlo(axis, x, y_mc, GLOBAL_PROPS['monte_carlo'],
                     GLOBAL_PROPS['monte_carlo_minima'], GLOBAL_PROPS['monte_carlo_minima_label'])
    plot_deviation(axis, x, y_mc, y_q_x_y, n)

    axis.set(xlabel=r'$x$', ylabel=r'$Q(x)$')


def plot_monte_carlo(axis, x, y, params, minima_params, label):
    global GLOBAL_PROPS

    plot_curve(axis, x, y, **params)

    plot_minima(
        axis, x, y, label=label, **minima_params)


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


def get_real_distribution(A, B, n, C):
    rng = np.random.default_rng()

    z = np.vectorize(distribution)
    h = 1 / ((B - C) + (C - A)/2)

    res_x = np.array([])

    while True:
        w = rng.random(1)[0] * h

        if len(res_x) < n:
            x = generate_random_numbers(A, B, int(B - A))
            x = x[w < z(x, A, B, C)]
            res_x = np.concatenate((res_x, x))
        else:
            res_x = res_x[0:n]
            break

    return res_x


def plot_real_distribution(axis, params):
    A = params['left']
    B = params['right']
    C = params['c']
    n = int(params['n'])
    set_mean = params['set_mean']
    set_std = params['set_std']

    x = get_real_distribution(A, B, n, C)

    sns.histplot(x, bins=20, ax=axis, stat="density", **GLOBAL_PROPS['hist'])

    set_mean(np.mean(x))
    set_std(np.std(x))

    axis.set(xlabel=r'$x$', ylabel=r'$\phi(x)$')


def distribution(y, A, B, C):

    h = 1 / ((B - C) + (C - A)/2)
    if (y < C):
        return h / 2
    else:
        return h


def plot_analytic_distribution(axis, params):
    A = params['left']
    B = params['right']
    C = params['c']

    z_vect = np.vectorize(distribution)
    x = np.linspace(A, B, int(params['n']))
    y = z_vect(x, A, B, C)

    plot_curve(axis, x, y, **GLOBAL_PROPS['analytic'])


def generate_random_numbers(low, high, size):
    numbers = np.random.random(size) * (high-low) + low

    return numbers


def plot_uniform_mc(axis, params):
    alpha = params['alpha']
    beta = params['beta']
    left = params['left']
    right = params['right']
    n = int(params['n'])
    m = int(params['m'])

    x = np.linspace(left, right, int(m) + 1)
    y = generate_random_numbers(left, right, n)

    vect_q_x_y = np.vectorize(q_x_y)
    y_q_x_y = np.array([vect_q_x_y(x_i, y, alpha, beta) for x_i in x])

    y_mc = monte_carlo(y_q_x_y, n)

    plot_monte_carlo(axis, x, y_mc, GLOBAL_PROPS['monte_carlo_uniform'],
                     GLOBAL_PROPS['monte_carlo_uniform_minima'], GLOBAL_PROPS['monte_carlo_uniform_minima_label'])
