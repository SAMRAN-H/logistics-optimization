import numpy as np


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


def generate_random_numbers(low, high, size):
    numbers = np.random.random(size) * (high-low) + low

    return numbers


def plot_all(axis, alpha, beta, left, right, m, n):
    x = np.linspace(left, right, int(m) + 1)
    y = generate_random_numbers(left, right, int(n))

    vect_q_x_y = np.vectorize(q_x_y)
    y_q_x_y = np.array([vect_q_x_y(x_i, y, alpha, beta) for x_i in x])

    y_mc = monte_carlo(y_q_x_y, n)

    plot_default_q(axis, alpha, beta, left, right, 'blue')
    plot_monte_carlo(axis, x, y_mc, 'red')
    plot_deviation(axis, x, y_mc, y_q_x_y, n, 'purple')

    axis.set(xlabel=r'$x$', ylabel=r'$Q(x)$')
    axis.legend(frameon=False)
    axis.grid(True)


def plot_default_q(axis, alpha, beta, left, right, color):
    x = np.linspace(left, right, int(1e5))
    y = default_q(x, alpha, beta, left, right)

    plot_curve(axis, x, y, color, label=r'$Функция\ Q(x)$')
    plot_analytic_minima(axis, alpha, beta, left, right, color=color)


def plot_analytic_minima(axis, alpha, beta, A, B, color):
    x = (A*alpha + B*beta) / (alpha + beta)
    y = default_q(x, alpha, beta, A, B)

    axis.plot(x, y, 'o', color=color,
              label=rf'$Минимум\ Q(x)\ ({x:.3f}, {y:.3f})$')


def plot_monte_carlo(axis, x, y, color):
    plot_curve(axis, x, y, color, label=r'$Функция\ Q_{мк}(x)$')
    plot_minima(axis, x, y, color, label=lambda x,
                y: rf'$Минимум\ Q_{{мк}}(x)\ ({x:.3f}, {y:.3f})$')


def plot_deviation(axis, x, y_mc, y_q_x_y, n, color):
    y = [np.sqrt(1/n * np.sum((y_mc[i] - y_q_x_y[i])**2))
         for i in range(len(x))]

    plot_curve(axis, x, y, color, label=r'$Стандартное\ отклонение\ S(x)$')


def plot_curve(axis, x, y, color, label):
    axis.plot(x, y, color=color, label=label)


def plot_minima(axis, x, y, color, label):
    min_index = np.argmin(y)

    axis.plot(x[min_index], y[min_index], 'o', color=color,
              label=label(x[min_index], y[min_index]))


def q_x_y(x, y, alpha, beta):
    return alpha*(x - y) if x > y else beta*(y - x)


def default_q(x, alpha, beta, A, B):
    return 1 / (2 * (B - A)) * (alpha*(x-A)**2 + beta*(B-x)**2)


def monte_carlo(y, n):
    return 1 / n * np.array([np.sum(y_val) for y_val in y])
