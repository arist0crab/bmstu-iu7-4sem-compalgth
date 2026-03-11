import numpy as np


def newton_coefficients(x_nodes, y_nodes):
    n = len(x_nodes)
    coefficients = y_nodes.copy()

    for j in range(1, n):
        for i in range(n - 1, j - 1, -1):
            coefficients[i] = (coefficients[i] - coefficients[i - 1]) / (x_nodes[i] - x_nodes[i - j])

    return coefficients


def newton_evaluate(coefficients, x_nodes, x):
    n = len(coefficients)
    result = coefficients[-1]

    for i in range(n - 2, -1, -1):
        result = result * (x - x_nodes[i]) + coefficients[i]

    return result


def _find_nearest_indices(x_nodes, x, n_needed):
    idx = np.searchsorted(x_nodes, x)

    left = max(0, idx - n_needed // 2)
    right = min(len(x_nodes), left + n_needed)

    if right - left < n_needed:
        if left == 0:
            right = min(len(x_nodes), n_needed)
        else:
            left = max(0, len(x_nodes) - n_needed)

    return left, right


def _select_nodes(x_nodes, y_nodes, x, degree):
    n_nodes = degree + 1

    if len(x_nodes) <= n_nodes:
        return x_nodes, y_nodes

    left, right = _find_nearest_indices(x_nodes, x, n_nodes)

    return x_nodes[left:right], y_nodes[left:right]


def interpolate_1d(x_nodes, y_nodes, x, degree=3):
    if degree < 0:
        raise ValueError("Degree must be non-negative")

    if degree == 0:
        idx = np.argmin(np.abs(x_nodes - x))
        return y_nodes[idx]

    x_sel, y_sel = _select_nodes(x_nodes, y_nodes, x, degree)
    coefficients = newton_coefficients(x_sel, y_sel)

    return newton_evaluate(coefficients, x_sel, x)


def interpolate_2d(t_nodes, p_nodes, values, t, p, t_degree=2, p_degree=2):
    n_pressures = len(p_nodes)
    temp_values = np.zeros(n_pressures)

    for i in range(n_pressures):
        temp_values[i] = interpolate_1d(t_nodes, values[:, i], t, t_degree)

    return interpolate_1d(p_nodes, temp_values, p, p_degree)


def interpolate_current(time_nodes, current_nodes, t, degree=3):
    return interpolate_1d(time_nodes, current_nodes, t, degree)


def create_interpolators(raw_data, t_degree=2, p_degree=2, time_degree=3):
    def current_interp(t):
        return interpolate_current(
            raw_data['current']['time'],
            raw_data['current']['current'],
            t, time_degree
        )

    def nh_interp(t, p):
        return interpolate_2d(
            raw_data['nh']['temperatures'],
            raw_data['nh']['pressures'],
            raw_data['nh']['values'],
            t, p, t_degree, p_degree
        )

    def sigma_interp(t, p):
        return interpolate_2d(
            raw_data['sigma']['temperatures'],
            raw_data['sigma']['pressures'],
            raw_data['sigma']['values'],
            t, p, t_degree, p_degree
        )

    def c_interp(t, p):
        return interpolate_2d(
            raw_data['c']['temperatures'],
            raw_data['c']['pressures'],
            raw_data['c']['values'],
            t, p, t_degree, p_degree
        )

    def q_interp(t, p):
        return interpolate_2d(
            raw_data['q']['temperatures'],
            raw_data['q']['pressures'],
            raw_data['q']['values'],
            t, p, t_degree, p_degree
        )

    return {
        'current': current_interp,
        'nh': nh_interp,
        'sigma': sigma_interp,
        'c': c_interp,
        'q': q_interp
    }
